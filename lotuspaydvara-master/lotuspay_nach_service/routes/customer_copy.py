import imp
from fastapi import APIRouter, status
import requests
import json
import ast
from lotuspay_nach_service.commons import get_env_or_fail
from lotuspay_nach_service.resource.generics import response_to_dict



LOTUSPAY_SERVER = 'lotus-pay-server'
router = APIRouter()


@router.get("/customer_copy", status_code=status.HTTP_200_OK,  tags=["Customer Copy"])
async def get_customer_copy(
    cus_id: str
):
    validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
    api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
    url = validate_url + f'/customers/{cus_id}'
    cust_response = requests.get(url, auth=(api_key, ''))
    cust_dict = response_to_dict(cust_response)
    # cust_dict = cust_response.content
    # response_decode = cust_dict.decode("UTF-8",errors="ignore")
    # json_acceptable_string = response_decode.replace("'", "\"")
    # convert_to_json = json.loads(json_acceptable_string)
    # response_dict = dict(convert_to_json)
    # return response_dict
    # cust_response.raise_for_status
    # jsonResponse=cust_response.json()

    # cust_dict=json.loads(cust_response.decode('utf-8'))
    return cust_dict
