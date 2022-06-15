import logging
from starlette.responses import Response
from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import JSONResponse
from datetime import datetime
from databases import Database
from lotuspay_nach_service.data.database import get_database, sqlalchemy_engine, insert_logs
from lotuspay_nach_service.data.settings_model import settings
from lotuspay_nach_service.gateway.perdix import perdix_lotuspay_source_status, perdix_update_customer
from lotuspay_nach_service.routes.events_status import get_event_status
from lotuspay_nach_service.resource.generics import response_to_dict
from lotuspay_nach_service.gateway.perdix import perdix_post_login, perdix_fetch_customer
from lotuspay_nach_service.gateway.lotuspay_source import lotus_pay_post_source5
from lotuspay_nach_service.data.database import get_database, sqlalchemy_engine, insert_logs
from lotuspay_nach_service.data.source_model import perdix_customer, SourceDB
from lotuspay_nach_service.resource.generics import get_token_header
from sqlalchemy.sql import and_

router = APIRouter(
    # dependencies=[Depends(get_token_header)]
)


@router.post("/perdix/{customer_id}", status_code=status.HTTP_200_OK, tags=["Perdix"])
async def get_customer(customer_id,
                       request_info: Request,
                       x_token: str = Depends(get_token_header),
                       database: Database = Depends(get_database)
                       ) -> SourceDB:
    try:

        payload = await request_info.json()
        store_record_time = datetime.now()
        result = {}
        request_payload = {
            "type": "nach_debit"
        }
        get_perdix_data = await perdix_fetch_customer(customer_id)
        # print('getting customer', get_perdix_data)
        perdix_error = get_perdix_data.get('error')
        if perdix_error:
            result = {"error": "Customer details not found in Perdix"}
            log_id = await insert_logs('PERDIX', 'DB', 'CUSTOMER-DETAILS', '500',
                                       'customer details not found',
                                       datetime.now())
            return result
        else:
            perdix_save = {}
            enrollment_id = get_perdix_data.get("enrollmentId")
            firstName = (get_perdix_data.get("firstName") if get_perdix_data.get("firstName") else "")
            lastName = (get_perdix_data.get("lastName") if get_perdix_data.get("lastName") else "")
            result["debtor_account_name"] = firstName + '' + lastName
            result["amount_maximum"] = 10000
            result["debtor_email"] = (get_perdix_data.get("emailId") if get_perdix_data.get("emailId") else "")
            result["debtor_mobile"] = (get_perdix_data.get("mobilePhone") if get_perdix_data.get("mobilePhone") else "")
            customer_bank_details = get_perdix_data.get('customerBankAccounts')
            # print('customer bank account details', customer_bank_details, len(customer_bank_details))
            if len(customer_bank_details) > 0:
                print('yes found')
                # result["debtor_account_name"] = customer_bank_details[0].get("customerNameAsInBank")
                result["debtor_agent_mmbid"] = (
                    customer_bank_details[1].get("ifscCode") if customer_bank_details[1].get("ifscCode") else "")
                if result["debtor_agent_mmbid"] == "":
                    result = {"error": "Customer Bank IFSC not found in Perdix"}
                    log_id = await insert_logs('PERDIX', 'DB', 'CUSTOMER-DETAILS', '500',
                                               'customer Bank IFSC not found',
                                               datetime.now())
                    return result

                result["debtor_account_number"] = (
                    customer_bank_details[1].get("accountNumber") if customer_bank_details[1].get(
                        "accountNumber") else "")
                if result["debtor_account_number"] == "":
                    result = {"error": "Customer Bank Account Number not found in Perdix"}
                    log_id = await insert_logs('PERDIX', 'DB', 'CUSTOMER-DETAILS', '500',
                                               'customer Bank Account Number not found',
                                               datetime.now())
                    return result
                result["debtor_account_type"] = (
                    customer_bank_details[1].get("accountType").lower() if customer_bank_details[1].get(
                        "accountType") else "")
                if result["debtor_account_type"] == "":
                    result = {"error": "Customer Bank Account Type not found in Perdix"}
                    log_id = await insert_logs('PERDIX', 'DB', 'CUSTOMER-DETAILS', '500',
                                               'customer Bank Account Type not found',
                                               datetime.now())
                    return result
            else:
                print('not found')
                # result["debtor_account_name"] = "AMIT JAIN"
                # result["debtor_agent_mmbid"] = "ICIC0000001"
                # result["debtor_account_number"] = "12345678"
                # result["debtor_account_type"] = "savings"
                result = {"error": "customer bank details not found"}
                log_id = await insert_logs('PERDIX', 'DB', 'CUSTOMER-BANK-DETAILS', '500',
                                           'customer bank details not found',
                                           datetime.now())
                return result
            request_payload["nach_debit"] = result

            if 'return_url' in payload:
                request_payload["redirect"] = { 'return_url': payload['return_url'] }

            source_detail = await lotus_pay_post_source5('sources', request_payload, perdix=True)
            if source_detail.get('error'):
                print('printing the source ', source_detail.get('error').get('message'))
                result = {"error": source_detail.get('error').get('message')}
                return result
            else:
                source_id = source_detail.get('id')
                perdix_save['mandate_url'] = source_detail.get("redirect").get("url")
                perdix_save['source_id'] = source_detail.get('id')
                perdix_save['perdix_customer_id'] = customer_id
                perdix_save['source_status'] = source_detail.get('status')
                perdix_save['created_date'] = store_record_time
                perdix_save['perdix_enrollment_id'] = enrollment_id
                perdix_save['pending'] = 1
                perdix_save['iterations'] = 0
                insert_query = perdix_customer.insert().values(perdix_save)
                source_id = await database.execute(insert_query)

                result = {"mandate_url": perdix_save['mandate_url']}
    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', 'GET-CUSTOMER', '500', {e.args[0]},
                                   datetime.now())
        result = JSONResponse(status_code=500,
                              content={"message": f"Error Occurred at DB level GET-CUSTOMER - {e.args[0]}"})
    return result


async def update_pending_customers(src_id, mandate_id, mandate_status, customer_id):
    try:
        database = get_database()
        query = perdix_customer.update().where(perdix_customer.c.source_id == src_id).values(mandate_id=mandate_id,
                                                                                             mandate_status=mandate_status,
                                                                                             lotuspay_customer_id=customer_id,
                                                                                             pending=0)
        customer_updated = await database.execute(query)
        return customer_updated
    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', 'UPDATE-PENDING-CUSTOMERS', '500', {e.args[0]},
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at DB level - {e.args[0]}"})


async def update_iterations(src_id, iter_no):
    try:
        database = get_database()
        query = perdix_customer.update().where(perdix_customer.c.source_id == src_id).values(iterations=iter_no+1)
        customer_updated = await database.execute(query)
        return customer_updated
    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', 'UPDATE-ITERATIONS', '500', {e.args[0]},
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at DB level - {e.args[0]}"})


@router.post("/source-status", status_code=status.HTTP_200_OK, tags=["Perdix"])
async def update_perdix_status(src_id: str, cust_id: str, iter_no: int,  x_token: str = Depends(get_token_header),
                               database: Database = Depends(get_database)
                               ):
    try:
        mandate_id, mandate_status, customer_id = await perdix_lotuspay_source_status(src_id)
        if mandate_id is not None and mandate_id != 0:
            get_perdix_customer = await perdix_fetch_customer(cust_id)
            if "udf" in get_perdix_customer:
                get_perdix_customer['udf'] = {
                    'userDefinedFieldValues': {
                        'udf42': mandate_id,
                        'udf43': mandate_status
                    }
                }
                prepared_perdix_data = {
                    "enrollmentAction": "PROCEED",
                    "customer": get_perdix_customer
                }
                update_iteration = await update_iterations(src_id, iter_no)
                db_update_pending_customers = await update_pending_customers(src_id, mandate_id, mandate_status,
                                                                             customer_id)
                update_perdix_customer = await perdix_update_customer(prepared_perdix_data)
                result = {"mandate_id": mandate_id}

            else:
                log_id = await insert_logs('PERDIX', 'UDF', 'UDF-COLUMN-NOT-FOUND', '500', 'UDF-COLUMN-NOT-FOUND', datetime.now())
                result = {"error": "UDF key not found in customer dictionary"}
        else:
            update_iteration = await update_iterations(src_id, iter_no)
            result = {"error": "Not able to update"}
    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', 'UPDATE-SOURCE-STATUS', '500', {e.args[0]},
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at DB level - {e.args[0]}"})
    return result


async def get_settings():
    try:
        database = get_database()
        query = settings.select()
        settings_response = await database.fetch_all(query)
        return settings_response
    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', 'GET-SETTINGS', '500', {e.args[0]},
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at DB level - {e.args[0]}"})


async def get_pending_customers():
    try:
        settings_dict = await get_settings()
        for items in settings_dict:
            iterations_count = items[2]
            records_count = items[1]
        customer_array = []
        database = get_database()
        print('coming inside get_pending_customers ')
        query = perdix_customer.select().where(and_(perdix_customer.c.pending.is_(True), perdix_customer.c.iterations<=iterations_count))
        perdix_customer_array = await database.fetch_all(query)
        print('get_pending_customers ', perdix_customer_array)
        array_length = len(perdix_customer_array)
        if records_count >= array_length:
            customer_array = perdix_customer_array
        else:
            customer_array = perdix_customer_array[:records_count]
        return customer_array
    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', 'GET-PENDING-CUSTOMERS', '500', {e.args[0]},
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at DB level - {e.args[0]}"})


@router.post("/mandate-status", status_code=status.HTTP_200_OK, tags=["Perdix"])
async def pending_mandate_status(x_token: str = Depends(get_token_header), database: Database = Depends(get_database)
                                 ):
    try:
        perdix_customer_array = await get_pending_customers()
        for items in perdix_customer_array:
            update_perdix_customer = await update_perdix_status(items[1], items[6], items[11], 'fake-super-secret-token')

        result = {"Success": "Mandates Updated"}
    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', 'UPDATE-SOURCE-STATUS', '500', {e.args[0]},
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at DB level - {e.args[0]}"})
    return result
