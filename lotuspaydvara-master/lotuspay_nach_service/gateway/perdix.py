from datetime import datetime
import requests
from lotuspay_nach_service.resource.generics import response_to_dict
from fastapi.responses import JSONResponse
from lotuspay_nach_service.data.database import insert_logs
from lotuspay_nach_service.gateway.lotuspay_source import lotus_pay_post_source5
from lotuspay_nach_service.commons import get_env_or_fail


PERDIX_SERVER = 'perdix-server'
LOTUSPAY_SERVER = 'lotus-pay-server'


async def perdix_post_login():
    """ Generic Post Method for perdix login """
    try:
        validate_url = get_env_or_fail(PERDIX_SERVER, 'perdix-base-url', PERDIX_SERVER + ' base-url not configured')
        username = get_env_or_fail(PERDIX_SERVER, 'username', PERDIX_SERVER + ' username not configured')
        password = get_env_or_fail(PERDIX_SERVER, 'password', PERDIX_SERVER + ' password not configured')
        # url = validate_url + f'/{context}/'
        url = validate_url + f'/oauth/token?client_id=application&client_secret=mySecretOAuthSecret&grant_type=password&password={password}&scope=read+write&skip_relogin=yes&username={username}'
        print(url)
        str_url = str(url)
        login_context_response = requests.post(url)
        print(login_context_response)
        login_context_dict = response_to_dict(login_context_response)
        access_token = login_context_dict.get('access_token')
        log_id = await insert_logs(str_url, 'PERDIX', 'LOGIN', login_context_response.status_code, login_context_response.content, datetime.now())
        result = access_token

    except Exception as e:
        log_id = await insert_logs(str_url, 'PERDIX', 'LOGIN', login_context_response.status_code, login_context_response.content, datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at Perdix Login - {e.args[0]}"})

    return result


async def perdix_fetch_customer(customer_id):
    """ Generic Post Method for perdix fetch customer """
    try:
        validate_url = get_env_or_fail(PERDIX_SERVER, 'perdix-base-url', PERDIX_SERVER + ' base-url not configured')
        print('coming after validate url')
        username = get_env_or_fail(PERDIX_SERVER, 'username', PERDIX_SERVER + ' username not configured')
        password = get_env_or_fail(PERDIX_SERVER, 'password', PERDIX_SERVER + ' password not configured')

        login_token = await perdix_post_login()
        url = validate_url + f'/api/enrollments/{customer_id}'
        headers = {
            "Content-Type": "application/json",
            "Content-Length":"0",
            "User-Agent":'My User Agent 1.0',
            "Accept":"*/*",
            "Accept-Encoding":"gzip, deflate, br",
            "Connection":"keep-alive",
            "Authorization": f"bearer {login_token}"
        }
        str_url = str(url)
        customer_context_response = requests.get(url, headers=headers)
        customer_context_dict = response_to_dict(customer_context_response)
        log_id = await insert_logs(str_url, 'PERDIX', 'FETCH-CUSTOMER', customer_context_response.status_code, customer_context_response.content, datetime.now())
        result = customer_context_dict
    except Exception as e:
        print(e.args[0])
        log_id = await insert_logs(str_url, 'PERDIX', 'FETCH-CUSTOMER', customer_context_response.status_code,
                                   customer_context_response.content, datetime.now())
        result = JSONResponse(status_code=500,
                              content={"message": f"Error Occurred at Perdix - Fetch Customer - {e.args[0]}"})
    return result


async def perdix_lotuspay_source_status(source_id):
    """Generic Get Method for lotuspay listing specific source withdraw for a specific customer"""
    try:
        print('coming inside of perdix source status')
        validate_url = get_env_or_fail(LOTUSPAY_SERVER , 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
        api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
        source_url = validate_url + f'/sources/{source_id}'
        event_url = validate_url + f'/events/'

        perdix_context_response = requests.get(source_url, auth=(api_key, ''))
        perdix_event_response = requests.get(event_url, auth=(api_key, ''))
        event_context_dict = response_to_dict(perdix_event_response)
        get_source_from_event = event_context_dict.get('data')
        found_element = next((item for item in get_source_from_event if item["resource_id"] == source_id), None)

        resource_status = found_element.get('type')

        if resource_status == 'source.submitted':
            perdix_context_dict = response_to_dict(perdix_context_response)
            perdix_mandate_response_id = perdix_context_dict.get('mandate')
            perdix_customer_response_id = perdix_context_dict.get('customer')

            perdix_mandate_response = requests.get(event_url, auth=(api_key, ''))
            mandate_context_dict = response_to_dict(perdix_mandate_response)
            get_mandate_from_event = mandate_context_dict.get('data')
            found_element = next((item for item in get_mandate_from_event if item["resource_id"] == perdix_mandate_response_id), None)
            mandate_status = found_element.get('type')
            result = perdix_mandate_response_id, mandate_status, perdix_customer_response_id
        else:
            # result = {"Source Status": "Source still pending "}
            result = 0, 'NA', 0
    except Exception as e:
        print(e.args[0])
        log_id = await insert_logs(source_url, 'PERDIX', 'SOURCE-STATUS', perdix_context_response.status_code,
                                   perdix_context_response.content, datetime.now())
        result = JSONResponse(status_code=500,
                              content={"message": f"Error Occurred at Perdix - Source Status - {e.args[0]}"})
    return result


async def perdix_update_customer(data):
    """ Generic put Method to update perdix customer """
    try:
        validate_url = get_env_or_fail(PERDIX_SERVER, 'perdix-base-url', PERDIX_SERVER + ' base-url not configured')
        print('coming after validate url')
        username = get_env_or_fail(PERDIX_SERVER, 'username', PERDIX_SERVER + ' username not configured')
        password = get_env_or_fail(PERDIX_SERVER, 'password', PERDIX_SERVER + ' password not configured')

        login_token = await perdix_post_login()
        url = validate_url + f'/api/enrollments/'
        headers = {
            "Content-Type": "application/json",
            "Content-Length":"0",
            "User-Agent":'My User Agent 1.0',
            "Accept":"*/*",
            "Accept-Encoding":"gzip, deflate, br",
            "Connection":"keep-alive",
            "Authorization": f"bearer {login_token}"
        }
        str_url = str(url)
        customer_update_response = requests.put(url, json=data, headers=headers)
        customer_context_dict = response_to_dict(customer_update_response)
        result = customer_context_dict
    except Exception as e:
        print(e.args[0])
        log_id = await insert_logs(str_url, 'PERDIX', 'FETCH-CUSTOMER', customer_update_response.status_code,
                                   customer_update_response.content, datetime.now())
        result = JSONResponse(status_code=500,
                              content={"message": f"Error Occurred at Perdix - Fetch Customer - {e.args[0]}"})
    return result