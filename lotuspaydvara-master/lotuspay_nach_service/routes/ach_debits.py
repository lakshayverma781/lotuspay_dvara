
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from datetime import datetime

from databases import Database
from lotuspay_nach_service.data.database import get_database, sqlalchemy_engine, insert_logs 
import requests
from lotuspay_nach_service.resource.generics import response_to_dict
from lotuspay_nach_service.commons import get_env_or_fail
from lotuspay_nach_service.gateway.lotuspay_ach_debit import lotus_pay_achdebit_post, lotus_pay_achdebit_cancel
from lotuspay_nach_service.data.achdebit_model import (
    achdebits,
    achdebits_cancel,
    ACHDebitBase,
    ACHDebitCreate,
    ACHDebitDB,
)

LOTUSPAY_SERVER = 'lotus-pay-server'
router = APIRouter()


@router.post("/achdebits", response_model=ACHDebitDB, status_code=status.HTTP_201_CREATED,  tags=["ACH Debits"])
async def create_ach_debits(
    achdebit: ACHDebitCreate, database: Database = Depends(get_database)
) -> ACHDebitDB:

    try:
        print("coming inside the ach debit")
        achdebit_info = achdebit.dict()
        print(f"-----achdebit_info-----{achdebit_info}")
        response_achdebit_id = await lotus_pay_achdebit_post('ach_debits', achdebit_info)
        print(f"-----{response_achdebit_id}")
        if response_achdebit_id is not None:
            achdebit_info = {
                **achdebit_info,
                'achdebit_id': response_achdebit_id,
                'created_date': datetime.now()
            }
            insert_query = achdebits.insert().values(achdebit_info)
            achdebit_id = await database.execute(insert_query)
            result = JSONResponse(status_code=200, content={"achdebit_id": response_achdebit_id})

        else:
            log_id = await insert_logs('MYSQL', 'DB', 'NA', '400', 'problem with lotuspay parameters',
                                       datetime.now())
            result = JSONResponse(status_code=400, content={"message": 'problem with lotuspay parameters'})

    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', 'NA', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at DB level - {e.args[0]}"})
    return result


@router.post("/achdebits-cancellation", status_code=status.HTTP_200_OK,  tags=["ACH Debits"])
async def create_ach_debits_cancellation(
    debit_id: str, database: Database = Depends(get_database)
) -> ACHDebitDB:

    try:
        response_achdebit_id = await lotus_pay_achdebit_cancel('ach_debits', debit_id)
        store_record_time = datetime.now()
        if response_achdebit_id is not None:
            subscription_info = {
                'achdebit_id': response_achdebit_id,
                'created_date': store_record_time
            }
            delete_query = achdebits_cancel.insert().values(subscription_info)
            achdebit_id = await database.execute(delete_query)
        else:
            log_id = await insert_logs('MYSQL', 'DB', 'NA', '400', 'problem with lotuspay parameters',
                                       datetime.now())
            result = JSONResponse(status_code=400, content={"message": 'problem with lotuspay parameters'})

        result = response_achdebit_id

    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', 'NA', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at DB level - {e.args[0]}"})
    return result


@router.get("/achdebits/test1",status_code=status.HTTP_200_OK, tags=["ACH Debits"])
async def get_achdebits(
    debit_id:str
):
    validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
    api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
    url = validate_url + f'/ach_debits/{debit_id}'
    ach_response = requests.get(url, auth=(api_key, ''))
    ach_dict = response_to_dict(ach_response)
    return ach_dict   


@router.get("/achdebits/text",status_code=status.HTTP_200_OK, tags=["ACH Debits"])
async def get_achdebits_list(
    limit:int
):
    validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
    api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
    url = validate_url + f'/ach_debits?limit=5'
    ach_response = requests.get(url, auth=(api_key, ''))
    ach_dict = response_to_dict(ach_response)
    return ach_dict 


@router.get("/achdebits/collections",status_code=status.HTTP_200_OK, tags=["ACH Debits"])
async def get_achdebits_collections(
    debit_id:str
):
    validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
    api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
    url = validate_url + f'/ach_debits/{debit_id}'
    ach_collection_response = requests.get(url, auth=(api_key, ''))
    ach_collection_dict = response_to_dict(ach_collection_response)
    return ach_collection_dict   


@router.get("/achdebits/collections/list",status_code=status.HTTP_200_OK, tags=["ACH Debits"])
async def get_achdebits_list(
    
):
    validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
    api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
    url = validate_url + f'/ach_debit_collections'
    ach_collection_response = requests.get(url, auth=(api_key, ''))
    ach_collection_dict = response_to_dict(ach_collection_response)
    return ach_collection_dict   
