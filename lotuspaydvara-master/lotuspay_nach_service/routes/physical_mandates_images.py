import json
from datetime import datetime
from fastapi import APIRouter, Depends, status
import os
import shutil
import ast
from lotuspay_nach_service.data.database import get_database, sqlalchemy_engine, insert_logs
from fastapi.responses import JSONResponse ,FileResponse
from databases import Database
from fastapi import FastAPI, File,UploadFile,Form
from fastapi import APIRouter, status
from lotuspay_nach_service.resource.generics import response_to_dict
import requests
from requests import Session, Request
from lotuspay_nach_service.commons import get_env_or_fail
from requests_toolbelt.multipart.encoder import MultipartEncoder
from lotuspay_nach_service.data.physical_mandates_models import (
    physical,
    PhyDB
)
 
# some_file_path="C:\Users\DELL\Downloads\projects\lotuspaydvara-master\lotuspaydvara-master\static"

router = APIRouter()

LOTUSPAY_SERVER = 'lotus-pay-server'

@router.post("/physical_mandates_image")
async def upload_file(
    file: UploadFile = File(...), reference1: str = Form(...),database: Database = Depends(get_database)
):
    

    validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
    api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
    url = validate_url + f'/physical_mandate_images/'
    
    headers = {
        'Authorization': 'Basic c2tfdGVzdF81a0NmUHUzV3g2VkJOWnNiYzZhNlRpYlM6'
        }
        
    file_name = file.filename
    print('filename is ', file, file_name)
    print('-------------FILE',file_name)
    
    file_path = os.path.abspath(('./static/'))
    
    print(file_path)
    with open('test', "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        shutil.copyfile('test', file_path + '/' + file_name)
        
    if not os.path.exists(file_path + 'test'):
        print('yes there is a file')
        print(file_path)
    
        os.remove(file_path + '/' + 'test')
        print("---removed-----")
        
       
        shutil.move('test', file_path)
        
    else:
        print("------file_path------", file_path)
        print("file is not there")
        shutil.move('test', file_path)
   

    with open(file_path + '\\' + file_name,"rb") as a_file:
        print('-----------------------------printing file name ', a_file)
        path_proper =  a_file.name
        
       
  
    files=[('file',(file_name,open(path_proper,'rb'),'image/jpeg'))]
    
    
    payload={'reference1': reference1}
    response = requests.request("POST", url, headers=headers, data=payload , files=files)
    print(f"------response----{response}")
    print(f"------response.e----{response.encoding}")
    response_context_dict=response.content
    print(f"------response.content----{response_context_dict}")
    
    # data=json.load(my_json)
    print(type(response_context_dict))
    # dict_str = response_context_dict.decode("UTF-8")
    response_dict=json.loads(response_context_dict.decode('utf-8'))
   

    response_id=response_dict.get('id')
    print('----------------ID',response_id)
    store_record_time = datetime.now()
    response_obj=response_dict.get('object')
    response_created=response_dict.get('created')
    response_source=response_dict.get('source')
    response_mandate=response_dict.get('mandate')
    response_ref=response_dict.get('reference1')
    if response_id is not None:
            phy_info = {
                
                'physical_id': response_id,
                'object': response_obj,
                'created': response_created,
                'mandate': response_mandate,
                'source': response_source,
                'reference1':response_ref,
                'created_date': store_record_time
            }
            insert_query = physical.insert().values(phy_info)
            db_token_id = await database.execute(insert_query)
            result = JSONResponse(status_code=200, content={"token_id": response_id})
    else:
            log_id = await insert_logs('MYSQL', 'DB', 'NA', '400', 'problem with lotuspay parameters',
                                       datetime.now())
            result = JSONResponse(status_code=500, content={"message": "Error Occurred at LotusPay level"})

   


    return response_id 




@router.get("/physical_mandate_image_file", status_code=status.HTTP_200_OK,  tags=["Physical "])
async def get_phy_file(
    phy_id: str
    
):
    validate_url = get_env_or_fail(LOTUSPAY_SERVER, 'base-url', LOTUSPAY_SERVER + ' base-url not configured')
    api_key = get_env_or_fail(LOTUSPAY_SERVER, 'api-key', LOTUSPAY_SERVER + ' api-key not configured')
    url = validate_url + f'/physical_mandate_images/{phy_id}/file'
    phy_response = requests.get(url, auth=(api_key, ''))
    print(phy_response)
    print(type(phy_response))
    return phy_response.text
    # print(phy_dict)
    # phy_dict = response_to_dict(phy_response)
    # return phy_dict       