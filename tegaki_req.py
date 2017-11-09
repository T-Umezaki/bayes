#!/usr/bin/python3

# Imports
import base64
import json
import requests
# from PIL import Image

TEGAKI_FORM_ENDPOINT = 'https://api.tegaki.ai/hwr/v1/form'
MY_API_KEY = '3bfeec98-8832-4f05-8477-7f8309f7b914'
PROXIES = {
        'http': 'http://Takeshi_Umezaki:umezaki6@192.168.236.23:8080',
        'https': 'https://Takeshi_Umezaki:umezaki6@192.168.236.23:8080',
        }

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


if __name__ == '__main__':
    print("start")
    json_str = ""
    with open('sisco_format_fax.json', 'r', encoding="utf-8") as json_file:
        json_str = str(json_file.read())

    print(len(json_str))
    image_file = open('ocr.jpg', "rb")

    post_form(json_str, image_file)
