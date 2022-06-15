from datetime import datetime
import requests
from lotuspay_nach_service.resource.generics import response_to_dict
from fastapi.responses import JSONResponse
from lotuspay_nach_service.data.database import get_database, sqlalchemy_engine, insert_logs
from lotuspay_nach_service.commons import get_env_or_fail
from starlette.responses import JSONResponse


LOTUSPAY_SERVER = 'lotus-pay-server'

async def lotus_pay_post_token(context, data):
    """ Generic Post Method for lotuspay Sources """
    try:
        validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
        api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
        url = 'http://api-test.lotuspay.com/v1/tokens/'
        str_url = str(url)
        str_data = str(data)
        token_context_response = requests.post(url, json=data, auth=(api_key, ''))
        token_context_dict = response_to_dict(token_context_response)
        token_context_response_id = token_context_dict.get('id')
        print(token_context_response.content)
       
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, token_context_response.status_code, token_context_response.content, datetime.now())

        result = token_context_response_id
      
        

    except Exception as e:
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, token_context_response.status_code, token_context_response.content, datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at LotusPay Post Method - {e.args[0]}"})
    return result



async def lotus_pay_post_token_partial(context, data):
    """ Generic Post Method for lotuspay Sources """
    try:
        validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
        api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
        url = validate_url + f'/tokens'
        str_url = str(url)
        str_data = str(data)
        token_context_response = requests.post(url, json=data, auth=(api_key, ''))
        token_context_dict = response_to_dict(token_context_response)
        token_context_response_id = token_context_dict.get('id')
        print(token_context_response.content)
       
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, token_context_response.status_code, token_context_response.content, datetime.now())

        result = token_context_response_id
      
        

    except Exception as e:
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, token_context_response.status_code, token_context_response.content, datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at LotusPay Post Method - {e.args[0]}"})
    return result