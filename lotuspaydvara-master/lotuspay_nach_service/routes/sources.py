from email import header
from wsgiref import headers
from fastapi import APIRouter, status, FastAPI
import requests
from fastapi.responses import HTMLResponse,FileResponse
from lotuspay_nach_service.commons import get_env_or_fail
from lotuspay_nach_service.resource.generics import response_to_dict
import logging
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from datetime import datetime
from sqlalchemy.sql import text
from databases import Database
from lotuspay_nach_service.data.database import get_database, sqlalchemy_engine, insert_logs
from lotuspay_nach_service.gateway.lotuspay_source import lotus_pay_post_source, lotus_pay_post_source2, lotus_pay_post_source3, lotus_pay_source_status, lotus_pay_post_source5
from .events_status import get_event_status
from lotuspay_nach_service.data.source_model import (
    sources,
    SourceBase,
    SourceCreate,
    SourceDB,
    Source2Create,
    Source3Create,
    Source5Create
)

router = APIRouter()

logger = logging.getLogger("arthmate-lender-handoff-service")

LOTUSPAY_SERVER = 'lotus-pay-server'

async def get_source_or_404(
    source: str,
    database: Database = Depends(get_database)
) -> SourceDB:
    select_query = sources.select().where(sources.c.source_id == source)
    raw_source = await database.fetch_one(select_query)

    if raw_source is None:
        return None

    return SourceDB(**raw_source)


@router.post("/source", status_code=status.HTTP_201_CREATED,  tags=["Sources"])
async def create_source(
    source: SourceCreate,
    database: Database = Depends(get_database)
) -> SourceDB:

    try:
        source_info = source.dict()
        source_id = source_info.get('source_id')

        verify_source_in_db = await get_source_or_404(source_id, database)
        if verify_source_in_db is None:
            response_source_id = await lotus_pay_post_source('sources', source_info)
            if response_source_id is not None:
                get_source_status = await get_event_status(response_source_id)
                source_status = get_source_status['type']
                store_record_time = datetime.now()
                save_source = source_info.get('nach_debit')
                nach_type = source_info.get('type')
                save_source['type'] = nach_type
                save_source['source_status'] = source_status
                save_source['source_id'] = response_source_id
                save_source['created_date'] = store_record_time
                insert_query = sources.insert().values(save_source)
                source_id = await database.execute(insert_query)

                result = JSONResponse(status_code=200, content={"source_id": response_source_id})
            else:
                log_id = await insert_logs('MYSQL', 'DB', 'NA', '400', 'problem with lotuspay parameters',
                                           datetime.now())
                result = JSONResponse(status_code=400, content={"message": 'problem with lotuspay parameters'})

        else:
            print('Source already exists in DB')
            log_id = await insert_logs('MYSQL', 'DB', 'NA', '200', 'Source Already Exists in DB',
                                       datetime.now())
            result = JSONResponse(status_code=200, content={"message": "Source Already Exists in DB"})

    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', '500', 'Error Occurred at DB level', datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at DB level - {e.args[0]}"})

    return result


@router.post("/source/{customer_id}", status_code=status.HTTP_201_CREATED,  tags=["Sources"])
async def customer_source(
    source2: Source2Create,
        database: Database = Depends(get_database)
) -> SourceDB:

    try:
        print('Coming inside of Customer')
        source_info = source2.dict()
        source_id = source_info.get('source_id')
        redirect = source_info.get('redirect')
        str_redirect = str(redirect)
        customer = source_info.get('customer')
        verify_source_in_db = await get_source_or_404(source_id, database)
        if verify_source_in_db is None:
            response_source_id = await lotus_pay_post_source2('sources', source_info)
            if response_source_id is not None:
                store_record_time = datetime.now()

                save_source = source_info.get('nach_debit')
                nach_type = source_info.get('type')
                save_source['type'] = nach_type
                save_source['source_id'] = response_source_id
                save_source['created_date'] = store_record_time
                save_source['redirect'] = str_redirect
                save_source['customer'] = customer
                insert_query = sources.insert().values(save_source)
                source_id = await database.execute(insert_query)

                result = JSONResponse(status_code=200, content={"source_id": response_source_id})
            else:
                log_id = await insert_logs('MYSQL', 'DB', 'NA', '400', 'problem with lotuspay parameters',
                                           datetime.now())
                result = JSONResponse(status_code=400, content={"message": 'problem with lotuspay parameters'})

        else:
            print('Source already exists in DB')
            log_id = await insert_logs('MYSQL', 'DB', 'NA', '200', 'Source Already Exists in DB',
                                       datetime.now())
            result = JSONResponse(status_code=200, content={"message": "Source Already Exists in DB"})

    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at DB level"})

    return result


@router.post("/source/{bank_account}", response_model=SourceDB, status_code=status.HTTP_201_CREATED,  tags=["Sources"])
async def source_bank_account(
    source3: Source3Create,
        database: Database = Depends(get_database)
) -> SourceDB:

    try:
        print('Coming inside of Bank Account')
        source_info = source3.dict()
        print('comingg isndfns')
        print(source_info)
        source_id = source_info.get('bank_account')
        redirect = source_info.get('redirect')
        str_redirect = str(redirect)
        bank_account = source_info.get('bank_account')
        # verify_source_in_db = await get_source_or_404(source_id, database)
        # if verify_source_in_db is None:
        response_source_id = await lotus_pay_post_source3('sources', source_info)
        if response_source_id is not None:
            store_record_time = datetime.now()

            save_source = source_info.get('nach_debit')
            nach_type = source_info.get('type')
            save_source['type'] = nach_type
            save_source['source_id'] = response_source_id
            save_source['created_date'] = store_record_time
            save_source['redirect'] = str_redirect
            save_source['bank_account'] = bank_account
            insert_query = sources.insert().values(save_source)
            source_id = await database.execute(insert_query)

            result = JSONResponse(status_code=200, content={"source_id": response_source_id})
        else:
            log_id = await insert_logs('MYSQL', 'DB', 'NA', '400', 'problem with lotuspay parameters',
                                       datetime.now())
            result = JSONResponse(status_code=400, content={"message": 'problem with lotuspay parameters'})

        # else:
        #     print('Source already exists in DB')
        #     log_id = await insert_logs('MYSQL', 'DB', 'NA', '200', 'Source Already Exists in DB',
        #                                datetime.now())
        #     result = JSONResponse(status_code=200, content={"message": "Source Already Exists in DB"})

    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at DB level"})

    return result


@router.patch("/source/{source_id}", status_code=status.HTTP_200_OK,  tags=["Sources"])
async def update_source_status(
    source_id: str,
    database: Database = Depends(get_database)
):
    try:

        source_status = await lotus_pay_source_status(source_id)
        if source_status is not None:

            get_source_status = await get_event_status(source_status)
            update_query = sources.select()
            # database.
            testing = await database.execute(update_query)
            print('dkjsafkdjs - ', testing)
            get_mandate_status = get_source_status['type']
            # print('text query', query)
            # source_id = await database.execute(text(query))
            print('printing mandate status from evennts - ', source_status, get_mandate_status)
        # print('coming in main patch request', source_status)

    except Exception as e:
        print(e.args[0])



@router.post("/source5/", response_model=SourceDB, status_code=status.HTTP_201_CREATED,  tags=["Sources"])
async def create_source5(
    source5: Source5Create,
    database: Database = Depends(get_database)) -> SourceDB:
    try:
        print('Coming inside of Customer')
        source_info = source5.dict()
        print(f"---------sourceinfo-----------{source_info}-")
        source_id = source_info.get('source_id')
        print(source_id)
        verify_source_in_db = await get_source_or_404(source_id, database)
        if verify_source_in_db is None:
            response_source_id = await lotus_pay_post_source5('sources', source_info)
            if response_source_id is not None:
                store_record_time = datetime.now()
                nach_debit = source_info.get('nach_debit')
                nach_type = source_info.get('type')
                nach_debit['type'] = nach_type
                nach_debit['source_id'] = response_source_id
                nach_debit['created_date'] = store_record_time
                insert_query = sources.insert().values(nach_debit)
                source_id = await database.execute(insert_query)
                result = JSONResponse(status_code=200, content={
                                      "source_id": response_source_id})
            else:
                log_id = await insert_logs('MYSQL', 'DB',  'NA', '400', 'problem with lotuspay parameters',
                                           datetime.now())
                result = JSONResponse(status_code=400, content={
                                      "message": 'problem with lotuspay parameters'})
        else:
            print('Source already exists in DB')
            log_id = await insert_logs('MYSQL', 'DB', 'NA', '200', 'Source Already Exists in DB',
                                       datetime.now())
            result = JSONResponse(status_code=200, content={
                                  "message": "Source Already Exists in DB"})
        return result
    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', 'NA', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={
                              "message": "Error Occurred at DB level"})
        return result


@router.get("/sources", status_code=status.HTTP_200_OK,  tags=["Sources"])
async def get_sources(
    source_id: str
    
):
    validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
    api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
    url = validate_url + f'/sources/{source_id}'
    source_response = requests.get(url, auth=(api_key, ''))
    source_dict = response_to_dict(source_response)
    return source_dict 

@router.get("/source_PDF", status_code=status.HTTP_200_OK, tags=["Sources"])
async def get_source_pdf(
    source_id : str
    
    
):
    validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
    api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
    url = url = validate_url + f'/sources/{source_id}/pdf'
    # headers = {
    #         "Content-Type": "text/html",
    #         "User-Agent":'My User Agent 1.0',
    #         "Accept":"*/*",
    #         "Accept-Encoding":"gzip, deflate, br",
    #         "Connection":"keep-alive",
    #         "Authorization": "Basic c2tfdGVzdF81a0NmUHUzV3g2VkJOWnNiYzZhNlRpYlM6"
    #     }
    # payload={}
    # files={}
    headers={
        'Content-Type': 'application/json',
        'Authorization': 'Basic c2tfdGVzdF81a0NmUHUzV3g2VkJOWnNiYzZhNlRpYlM6'
    }
    source_response = requests.get(url, headers=headers, auth=(api_key, ''))
    # print(source_response)
    print(type(source_response))
    # print(source_response.text)
    return source_response.text
    # return  FileResponse
   

@router.get("/source_search", status_code=status.HTTP_200_OK,  tags=["Sources"])
async def get_source_search(
    source_id: str
):
    validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
    api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
    url = validate_url + f'/sources/search/id/{source_id}'
    source_response = requests.get(url, auth=(api_key, ''))
    source_dict = response_to_dict(source_response)
    return source_dict 


@router.get("/source_list", status_code=status.HTTP_200_OK,  tags=["Sources"])
async def get_source_search(
    
):
    validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
    api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
    url = validate_url + f'/sources/'
    source_response = requests.get(url, auth=(api_key, ''))
    source_dict = response_to_dict(source_response)
    return source_dict 

