from fastapi import APIRouter, Depends, status, Body
from fastapi.responses import JSONResponse
from datetime import datetime
import requests

from lotuspay_nach_service.commons import get_env_or_fail
from lotuspay_nach_service.resource.generics import response_to_dict
from databases import Database
from lotuspay_nach_service.data.database import get_database, sqlalchemy_engine, insert_logs
from lotuspay_nach_service.gateway.lotuspay_mandate import lotus_pay_patch_mandate, lotus_pay_mandate_cancel,lotus_pay_mandate_import


from lotuspay_nach_service.data.mandate_model import (
    mandates,
    MandateBase,
    MandateDB,
    mandates_cancel,
    mandates_import_external,
    MandateCancelCreate,
    MandateImportCreate
)


router = APIRouter()

LOTUSPAY_SERVER = 'lotus-pay-server'

@router.get("/mandates", status_code=status.HTTP_200_OK,  tags=["Mandates"])
async def get_mandates(
    mandate_id: str
):
    validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
    api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
    url = validate_url + f'/mandates/{mandate_id}'
    mandate_response = requests.get(url, auth=(api_key, ''))
    mandate_dict = response_to_dict(mandate_response)
    return mandate_dict 


@router.post("/mandate", response_model=MandateDB, status_code=status.HTTP_201_CREATED,  tags=["Mandates"])
async def update_mandate(
    id_token: str,
    mandate_id: str,
    payload: dict = Body({"metadata":{"key":"value"}}),
    database: Database = Depends(get_database)
) -> MandateDB:
    try:
        response_mandate_id = await lotus_pay_patch_mandate('mandates', mandate_id, id_token, payload)
        if response_mandate_id is not None:
            store_record_time = datetime.now()
            mandate_info = {
                'mandate_id': mandate_id,
                'metadata': str(payload),
                'created_date': store_record_time
            }
            insert_query = mandates.insert().values(mandate_info)
            mandate_db_id = await database.execute(insert_query)
        result = JSONResponse(status_code=200, content={"mandate_id": mandate_id})
    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', 'NA', '500', e.args[0],
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at DB level - {e.args[0]}"})
    return result


@router.post("/mandate-cancellation", status_code=status.HTTP_200_OK,  tags=["Mandates"])
async def mandate_cancellation(
        reason: MandateCancelCreate,
        mandate_id: str,
        database: Database = Depends(get_database)
) -> MandateDB:

    try:
        reason_info = reason.dict()
        response_mandate_id = await lotus_pay_mandate_cancel('mandates', mandate_id, reason_info)
        store_record_time = datetime.now()
        if response_mandate_id is not None:
            mandate_info = {
                'mandate_id': response_mandate_id,
                'created_date': store_record_time
            }
            delete_query = mandates_cancel.insert().values(mandate_info)
            db_mandate_id = await database.execute(delete_query)
            result = JSONResponse(status_code=200, content={"Customer_id": mandate_id})
        else:
            log_id = await insert_logs('MYSQL', 'DB', 'NA', '400', 'problem with lotuspay parameters',
                                       datetime.now())
            result = JSONResponse(status_code=500, content={"message": "Error Occurred at LotusPay level"})

    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', 'NA', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at DB level - {e.args[0]}"})
    return result


@router.post("/mandate-import_external", status_code=status.HTTP_200_OK,  tags=["Mandates"])
async def mandate_import(
        reason: MandateImportCreate,
        
        database: Database = Depends(get_database)
) -> MandateDB:

    try:
        reason_info = reason.dict()
        response_mandate_import = await lotus_pay_mandate_import('mandates', reason_info)
        store_record_time = datetime.now()
        if response_mandate_import is not None:
            mandate_info = {
                'mandate_id': response_mandate_import,
                'created_date': store_record_time
            }
            insert_query = mandates_import_external.insert().values(mandate_info)
            db_mandate_id = await database.execute(insert_query)
            result = JSONResponse(status_code=200, content={"mandate_id": response_mandate_import})
        else:
            log_id = await insert_logs('LOTUSPAY', 'DB', 'NA', '400', 'problem with lotuspay parameters',
                                       datetime.now())
            result = JSONResponse(status_code=400, content={"message": "Error Occurred at LotusPay level"})

    except Exception as e:
        log_id = await insert_logs('LOTUSPAY','DB',  'NA', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at DB level - {e.args[0]}"})
    return result



@router.get("/mandates_search", status_code=status.HTTP_200_OK,  tags=["Mandates"])
async def get_mandates(
    mandate_id: str
):
    validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
    api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
    url = validate_url + f'/mandates/search/id/{mandate_id}'
    mandate_response = requests.get(url, auth=(api_key, ''))
    mandate_dict = response_to_dict(mandate_response)
    return mandate_dict 

@router.get("/mandates_list", status_code=status.HTTP_200_OK,  tags=["Mandates"])
async def get_mandates_search(
   
):
    validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
    api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
    url = validate_url + f'/mandates/'
    mandate_response = requests.get(url, auth=(api_key, ''))
    mandate_dict = response_to_dict(mandate_response)
    return mandate_dict 

