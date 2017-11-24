#!/usr/bin/python3

# Imports
import base64
import json
import requests
import os
# ワイルドカードを利用
from glob import glob

TEGAKI_FORM_ENDPOINT = 'https://api.tegaki.ai/hwr/v1/form'
MY_API_KEY = '3bfeec98-8832-4f05-8477-7f8309f7b914'
PROXIES = {
        'http': 'http://Takeshi_Umezaki:umezaki6@192.168.236.23:8080',
        'https': 'https://Takeshi_Umezaki:umezaki6@192.168.236.23:8080',
        }
FORM_JSON_FILE_NAME = "karisinsa.json"
IMAGE_DIR = "C:\\Users\\Takeshi_Umezaki\\Documents\\ocr\\demo\\forapi\\"
# wild card
# FILES = "MpfRcvImgTFS00000244_0001*.jpg"
FILES = "*.jpg"

_json_str = ""
_request_id = ""
_file_name = ""

 
# base64-encoding files


def encode_image(image):
    image_content = image.read()
    encoded_byte = base64.b64encode(image_content)
    encoded_str = encoded_byte.decode("UTF-8")
    return encoded_str

# Post request for a single form to Tegaki service


def post_form(template_json_file, form_image_file):
    # Read json file
    template_json_data = json.loads(template_json_file)

    # Inject the base64-encoded form image into the template json
    template_json_data['imageData'] = encode_image(form_image_file)

    # Send POST request to Tegaki service
    response = requests.post(TEGAKI_FORM_ENDPOINT,
                             headers={'Authorization': 'apikey ' + MY_API_KEY},
                             json=template_json_data, proxies=PROXIES)

    # Print the result
    print(response.status_code)
    print(response.json())
    dict_res_json = response.json()
    _request_id = dict_res_json['requestId']
    print(_file_name, _request_id)

    file_results = open("results.txt", "a", encoding="shift_jis")
    file_results.write(_file_name + "," + _request_id + "\n")
    file_results.close()


if __name__ == '__main__':
    print("start")
    os.chdir(IMAGE_DIR)

    with open(FORM_JSON_FILE_NAME, 'r', encoding="utf-8") as json_file:
        _json_str = str(json_file.read())

    print(len(_json_str))
    files = glob(FILES)
    for file_name in files:
        _file_name = file_name
        print(_file_name)
        image_file = open(_file_name, "rb")

        post_form(_json_str, image_file)

