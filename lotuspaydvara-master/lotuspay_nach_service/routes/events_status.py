from fastapi import APIRouter, status
import requests
from lotuspay_nach_service.commons import get_env_or_fail
from lotuspay_nach_service.resource.generics import response_to_dict


LOTUSPAY_SERVER = 'lotus-pay-server'
router = APIRouter()


@router.get("/status", status_code=status.HTTP_200_OK,  tags=["Status"])
async def get_event_status(
    resource_id: str
):
    validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
    api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
    url = validate_url + f'/events/'
    events_response = requests.get(url, auth=(api_key, ''))
    events_dict = response_to_dict(events_response)
    events_data = events_dict.get('data')
    for events in events_data:
        if events['resource_id'] == resource_id:
            get_info = events
    return get_info
