from datetime import datetime
import requests
from lotuspay_nach_service.resource.generics import response_to_dict
from fastapi.responses import JSONResponse
from lotuspay_nach_service.data.database import insert_logs
from lotuspay_nach_service.commons import get_env_or_fail


LOTUSPAY_SERVER = 'lotus-pay-server'


async def lotus_pay_achdebit_post(context, data):
    """ Generic Post Method for lotuspay achdebit """
    try:
        print("comin inside lotuspay ach debit ")
        validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
        api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
        url = validate_url + f'/{context}/'
        print(url)
        str_url = str(url)
        str_data = str(data)
        achdebit_context_response = requests.post(url, data=data, auth=(api_key, ''))
        print(f"------achdebit_context_response------{achdebit_context_response}")
        achdebit_context_dict = response_to_dict(achdebit_context_response)
        print(f"-----achdebit_context_dict---{achdebit_context_dict}")
        achdebit_context_response_id = achdebit_context_dict.get('id')
        print(f"-----achdebit_context_response_id---------{achdebit_context_response_id}")
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, achdebit_context_response.status_code, achdebit_context_response.content, datetime.now())
        result = achdebit_context_response_id

    except Exception as e:
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, achdebit_context_response.status_code, achdebit_context_response.content, datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at LotusPay Post Method - {e.args[0]}"})

    return result


async def lotus_pay_achdebit_cancel(context, debit_id):
    """ Generic Post Method for lotuspay achdebit """
    try:
        validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
        api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
        url = validate_url + f'/{context}/{debit_id}/cancel'
        str_url = str(url)
        achdebit_context_response = requests.post(url, auth=(api_key, ''))
        achdebit_context_dict = response_to_dict(achdebit_context_response)
        achdebit_context_response_id = achdebit_context_dict.get('id')
        log_id = await insert_logs(str_url, 'LOTUSPAY', debit_id, achdebit_context_response.status_code, achdebit_context_response.content, datetime.now())
        result = achdebit_context_response_id

    except Exception as e:
        log_id = await insert_logs(str_url, 'LOTUSPAY', debit_id, achdebit_context_response.status_code, achdebit_context_response.content, datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at LotusPay Post Method - {e.args[0]}"})

    return result
