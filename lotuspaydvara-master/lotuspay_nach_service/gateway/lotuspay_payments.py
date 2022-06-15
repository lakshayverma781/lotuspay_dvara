from datetime import datetime
import requests
from lotuspay_nach_service.resource.generics import response_to_dict
from fastapi.responses import JSONResponse
from lotuspay_nach_service.data.database import insert_logs
from lotuspay_nach_service.commons import get_env_or_fail


LOTUSPAY_SERVER = 'lotus-pay-server'


async def lotus_pay_payments_post(context, data):
    """ Generic Post Method for lotuspay payments """
    try:
        
        print("coming inside lotuspay payments ")
        validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
        api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
        url = validate_url + f'/{context}/'
        print(url)
        
        str_url = str(url)
        str_data = str(data)
        # print(str_url)
        # print(str_data)
        payments_context_response = requests.post(url, data=data, auth=(api_key, ''))
        print(f"----payments_context_response------{payments_context_response}")
        payments_context_dict = response_to_dict(payments_context_response)
        print(f"---------payments_context_dict-----{payments_context_dict}")
        payments_context_response_id = payments_context_dict.get('id')
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, payments_context_response.status_code, payments_context_response.content,
                                   datetime.now())
        result = payments_context_response_id
    except Exception as e:
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, payments_context_response.status_code, payments_context_response.content,
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at LotusPay Post Method - {e.args[0]}"})
    return result
        


async def lotus_pay_payments_cancel(context, payment_id):
    """ Generic Post Method for lotuspay payment """
    try:
        print("coming inside lotuspay payments ")
        validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
        api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
        url = validate_url + f'/{context}/{payment_id}/cancel'
       
        str_url = str(url)
        # str_data = str(data)
       
        payments_context_response = requests.post(url, auth=(api_key, ''))
        print(payments_context_response.status_code)
        payments_context_dict = response_to_dict(payments_context_response)
        print(f"-------payments_context_dict--------{payments_context_dict}")
        payments_context_response_id = payments_context_dict.get('id')
        log_id = await insert_logs(str_url, 'LOTUSPAY', payment_id, payments_context_response.status_code, payments_context_response.content, datetime.now())
        result = payments_context_response_id

    except:
        log_id = await insert_logs(str_url, 'LOTUSPAY', payment_id, payments_context_response.status_code, payments_context_response.content, datetime.now())
        result = JSONResponse(status_code=500, content={"message": "Error Occurred at LotusPay Post Method"})

    return result

