from datetime import datetime
import requests
from lotuspay_nach_service.resource.generics import response_to_dict
from fastapi.responses import JSONResponse
from lotuspay_nach_service.data.database import insert_logs
from lotuspay_nach_service.commons import get_env_or_fail


LOTUSPAY_SERVER = 'lotus-pay-server'


async def lotus_pay_patch_mandate(context, mandate_id, id_token, data):
    """ Generic Post Method for lotuspay mandates """
    try:
        validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
        api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
        url = validate_url + f'/{context}/{mandate_id}/update?id_token={id_token}'
        # print('coming inside of lotuspay mandate')
        # url = f'http://api-test.lotuspay.com/v1/{context}/{mandate_id}/update?id_token={id_token}'
        # print(url)
        str_url = str(url)
        str_data = str(data)
        mandate_context_response = requests.patch(url, json=data, auth=(api_key, ''))
        # print(mandate_context_response.status_code, mandate_context_response.content)
        mandate_context_dict = response_to_dict(mandate_context_response)
        mandate_context_response_id = mandate_context_dict.get('id')
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, mandate_context_response.status_code, mandate_context_response.content, datetime.now())
        result = mandate_context_response_id

    except Exception as e:
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, mandate_context_response.status_code, mandate_context_response.content, datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at LotusPay Post Method - {e.args[0]}"})

    return result


async def lotus_pay_mandate_cancel(context, mandate_id, data):
    """ Generic Post Method for lotuspay mandate """
    try:
        url = f'http://api-test.lotuspay.com/v1/{context}/{mandate_id}/cancel'
        str_url = str(url)
        # str_data = str(data)
        print(url)
        mandate_context_response = requests.post(url, json=data, auth=('sk_test_5kCfPu3Wx6VBNZsbc6a6TibS', ''))
        print(mandate_context_response)
        print(mandate_context_response.status_code)
        mandate_context_dict = response_to_dict(mandate_context_response)
        mandate_context_id = mandate_context_dict.get('id')
        print(mandate_context_response.content)
        log_id = await insert_logs(str_url, 'LOTUSPAY', mandate_id, mandate_context_response.status_code, mandate_context_response.content, datetime.now())
        # result = JSONResponse(status_code=200, content={"message": "Subscripton Deletion Accepted"})
        result = mandate_context_id
    except:
        log_id = await insert_logs(str_url, 'LOTUSPAY', mandate_id, mandate_context_response.status_code, mandate_context_response.content, datetime.now())
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at LotusPay Post Method"})

    return result




async def lotus_pay_mandate_import(context, data):
    """ Generic Post Method for lotuspay mandate """
    try:
        url = f'http://api-test.lotuspay.com/v1/mandates/import'
        
        str_data = str(data)
        print(url)
        mandate_context_response = requests.post(url, data=data, auth=('sk_test_5kCfPu3Wx6VBNZsbc6a6TibS', ''))
        print(mandate_context_response)
        print(mandate_context_response.status_code)
        mandate_context_dict = response_to_dict(mandate_context_response)
        mandate_context_id = mandate_context_dict.get('id')
        print(mandate_context_response.content)
        log_id = await insert_logs('DB', 'LOTUSPAY', str_data, mandate_context_response.status_code, mandate_context_response.content, datetime.now())
        # result = JSONResponse(status_code=200, content={"message": "Subscripton Deletion Accepted"})
        result = mandate_context_id
    except:
        log_id = await insert_logs('DB', 'LOTUSPAY', str_data , mandate_context_response.status_code, mandate_context_response.content, datetime.now())
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at LotusPay Post Method"})

    return result    