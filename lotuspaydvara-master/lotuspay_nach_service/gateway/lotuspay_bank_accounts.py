from datetime import datetime
import requests
from lotuspay_nach_service.resource.generics import response_to_dict
from fastapi.responses import JSONResponse
from lotuspay_nach_service.data.database import insert_logs
from lotuspay_nach_service.commons import get_env_or_fail


LOTUSPAY_SERVER = 'lotus-pay-server'


async def lotus_pay_post_bank_account(context, customer_id, data):
    """ Generic Post Method for lotuspay bank accounts """
    try:
        validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'customers-url', LOTUSPAY_SERVER + ' base-url not configured')
        api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
        url = validate_url + f'/{customer_id}/{context}/'
        str_url = str(url)
        str_data = str(data)
        bank_account_context_response = requests.post(url, data=data, auth=(api_key, ''))
        bank_account_context_dict = response_to_dict(bank_account_context_response)
        bank_account_context_response_id = bank_account_context_dict.get('id')
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, bank_account_context_response.status_code, bank_account_context_response.content,
                                   datetime.now())
        result = bank_account_context_response_id
    except Exception as e:
        log_id = await insert_logs(str_url, 'LOTUSPAY', str_data, bank_account_context_response.status_code, bank_account_context_response.content,
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at LotusPay Post Method - {e.args[0]}"})
    return result
