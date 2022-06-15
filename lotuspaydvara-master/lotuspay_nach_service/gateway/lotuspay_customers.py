from datetime import datetime
import requests
from lotuspay_nach_service.resource.generics import response_to_dict
from fastapi.responses import JSONResponse
from lotuspay_nach_service.data.database import insert_logs
from lotuspay_nach_service.commons import get_env_or_fail


LOTUSPAY_SERVER = 'lotus-pay-server'


async def lotuspay_post_customer(context, data):
    """ Generic Post Method for lotuspay customer """
    try:
        validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
        api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
        url = validate_url + f'/{context}/'
        str_url = str(url)
        str_data = str(data)
        customer_context_response = requests.post(url, data=data, auth=(api_key, ''))
        customer_context_dict = response_to_dict(customer_context_response)
        customer_context_response_id = customer_context_dict.get('id')
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, customer_context_response.status_code, customer_context_response.content, datetime.now())
        result = customer_context_response_id

    except Exception as e:
        print(e.args[0])
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, customer_context_response.status_code, customer_context_response.content, datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at LotusPay Post Method - {e.args[0]}"})

    return result

