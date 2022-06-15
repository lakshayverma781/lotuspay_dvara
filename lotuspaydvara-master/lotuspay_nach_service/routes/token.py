from datetime import datetime
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from databases import Database
from lotuspay_nach_service.data.database import get_database, sqlalchemy_engine, insert_logs
from lotuspay_nach_service.gateway.lotuspay_token import lotus_pay_post_token,lotus_pay_post_token_partial
from lotuspay_nach_service.data.token_model import (
    BankAccount,
    TokenBase,
    TokenCreate,
    TokenCreate2,
    TokenDB,
    tokens
)

router = APIRouter()

   


@router.post("/tokenfull", response_model=TokenDB, status_code=status.HTTP_201_CREATED,  tags=["Tokens"])
async def create_token(
    token: TokenCreate, database: Database = Depends(get_database)
)-> TokenDB:

    try:
        token_info = token.dict()
        print('------------------TOKEN',token_info)
        response_token_id = await lotus_pay_post_token('token',  token_info)

        
        store_record_time = datetime.now()
      
        if response_token_id is not None:
            token_inf = {
                
                'token_id': response_token_id,
                
                'created_date': store_record_time
            }
            insert_query = tokens.insert().values(token_inf)
            db_token_id = await database.execute(insert_query)
            result = JSONResponse(status_code=200, content={"token_id": response_token_id})
        else:
            log_id = await insert_logs('MYSQL', 'DB', 'NA', '400', 'problem with lotuspay parameters',
                                       datetime.now())
            result = JSONResponse(status_code=500, content={"message": "Error Occurred at LotusPay level"})

    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', 'NA', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at DB level - {e.args[0]}"})
    return result



@router.post("/tokenpartial", response_model=TokenDB, status_code=status.HTTP_201_CREATED,  tags=["Tokens"])
async def create_token(
    token: TokenCreate2, database: Database = Depends(get_database)
)-> TokenDB:

    try:
        token_info = token.dict()
        response_token_id = await lotus_pay_post_token_partial('token',  token_info)
        store_record_time = datetime.now()
        name = token_info.get('bank_account').get('account_holder_name')
        acc_num=token_info.get('bank_account').get('account_number')
        acc_ifsc=token_info.get('bank_account').get('account_ifsc')
        
        # print('----------------------RRR',response_type)
        if response_token_id is not None:
            token_info = {
                'token_id': response_token_id,
                'account_holder_name': name,
                'account_number':acc_num,
                'account_ifsc':acc_ifsc,
                'created_date': store_record_time
            }
            insert_query = tokens.insert().values(token_info)
            db_token_id = await database.execute(insert_query)
            result = JSONResponse(status_code=200, content={"token_id": response_token_id})
        else:
            log_id = await insert_logs('MYSQL', 'DB', 'NA', '400', 'problem with lotuspay parameters',
                                       datetime.now())
            result = JSONResponse(status_code=500, content={"message": "Error Occurred at LotusPay level"})

    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', 'NA', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at DB level - {e.args[0]}"})
    return result    
