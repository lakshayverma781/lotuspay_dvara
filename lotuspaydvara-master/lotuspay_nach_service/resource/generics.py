import json
from fastapi import Header, HTTPException


def response_to_dict(response):
    """Converting bytes response to python dictionary"""
    response_content = response.content
    response.raise_for_status()
    response_decode = response_content.decode("UTF-8")
    json_acceptable_string = response_decode.replace("'", "\"")
    convert_to_json = json.loads(json_acceptable_string)
    response_dict = dict(convert_to_json)
    return response_dict


def get_token_header(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
