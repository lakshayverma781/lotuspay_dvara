
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from datetime import datetime

from databases import Database
from lotuspay_nach_service.data.database import get_database, sqlalchemy_engine, insert_logs
from lotuspay_nach_service.gateway.lotuspay_bank_accounts import lotus_pay_post_bank_account
from lotuspay_nach_service.data.bankaccount_model import (
    bankaccounts,
    BankAccountBase,
    BankAccountDB,
    BankAccountCreate,
)

router = APIRouter()


async def get_bank_account_or_404(
    account_no: str, database: Database = Depends(get_database)
) -> BankAccountDB:
    select_query = bankaccounts.select().where(bankaccounts.c.account_number == account_no)
    raw_bank_account = await database.fetch_one(select_query)

    if raw_bank_account is None:
        return None

    return BankAccountDB(**raw_bank_account)


@router.post("", response_model=BankAccountDB, status_code=status.HTTP_201_CREATED, tags=["Bank Accounts"])
async def create_bank_account(
    bank_account: BankAccountCreate, database: Database = Depends(get_database)
) -> BankAccountDB:

    try:
        bank_account_info = bank_account.dict()
        request_account_number = bank_account_info.get('account_number')
        request_customer_id = bank_account_info.get('customer_id')
        verify_account_in_db = await get_bank_account_or_404(request_account_number, database)
        if verify_account_in_db is None:
            post_bank_data = {
                **bank_account.dict(),
                'id_token': request_customer_id
            }
            response_bank_account_id = await lotus_pay_post_bank_account('bank_accounts', request_customer_id, post_bank_data)
            if response_bank_account_id is not None:
                store_record_time = datetime.now()
                bank_account_info = {
                    **bank_account.dict(),
                    'bank_account_id': response_bank_account_id,
                    'created_date': store_record_time
                }
                insert_query = bankaccounts.insert().values(bank_account_info)
                bank_account_id = await database.execute(insert_query)
                result = JSONResponse(status_code=200, content={"Customer_id": response_bank_account_id})
            else:
                log_id = await insert_logs('MYSQL', 'DB', 'NA', '400', 'problem with lotuspay parameters',
                                           datetime.now())
                result = JSONResponse(status_code=400, content={"message": 'problem with lotuspay parameters'})
        else:
            log_id = await insert_logs('MYSQL', 'DB', 'NA', '200', 'Account Already Exists in DB',
                                       datetime.now())
            result = JSONResponse(status_code=200, content={"message": "Account Already Exists in DB"})

    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', 'NA', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at DB level - {e.args[0]}"})
    return result

