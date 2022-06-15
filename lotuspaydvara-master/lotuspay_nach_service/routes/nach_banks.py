from fastapi import APIRouter, Depends, status, Body
from fastapi.responses import JSONResponse
from datetime import datetime

import requests

from lotuspay_nach_service.commons import get_env_or_fail
from lotuspay_nach_service.resource.generics import response_to_dict

router = APIRouter()

LOTUSPAY_SERVER = 'lotus-pay-server'

@router.get("/nach_banks", status_code=status.HTTP_200_OK,  tags=["Nach_banks"])
async def get_nach_banks(
    bank_id : str
   
):
    validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
    api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
    url = validate_url + f'/nach_banks/{bank_id}'
    nach_response = requests.get(url, auth=(api_key, ''))
    nach_dict = response_to_dict(nach_response)
    return nach_dict 


@router.get("/nach_banks_list/text", status_code=status.HTTP_200_OK,  tags=["Nach_banks"])
async  def get_nach_banks_list():
    validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
    api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
    url = validate_url + f'/nach_banks?filter=variant_api'
    nach_res = requests.get(url, auth=(api_key,''))
    print(nach_res)
    print (type(nach_res))
    print(nach_res.json())
    # nach_dict = response_to_dict(nach_response)
    nach_dic=nach_res.json()
    return nach_dic
