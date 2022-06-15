import requests
 
from fastapi import FastAPI, File, Form, UploadFile 

app = FastAPI()

@app.post("/files/")
async def create_file(
    file: bytes = File(), fileb: UploadFile = File(), token: str = Form()
):

    url = "https://api-test.lotuspay.com/v1/physical_mandate_images/"

    payload={'reference1': 'SC0011R17VZMF4'}
    files=[
    ('file',('5DFE7165-FEE4-49E5-B441-002F9148D4A3.jpeg',open('/C:/Users/DELL/Downloads/projects/lotuspaydvara-master/lotuspaydvara-master/static/5DFE7165-FEE4-49E5-B441-002F9148D4A3.jpeg','rb'),'image/jpeg'))
    ]
    headers = {
    'Authorization': 'Basic c2tfdGVzdF81a0NmUHUzV3g2VkJOWnNiYzZhNlRpYlM6'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)
