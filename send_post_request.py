import base64
import json
import requests

from convert_file import convert_xml_file


def encode_in_base64(file_to_encode):
    with open(file_to_encode, 'rb') as f_in:
        encoded = base64.encodebytes(f_in.read()).decode('utf-8')

    return encoded


def post_request(file_input, file_output):
    annot_id, xml_to_encode = convert_xml_file(file_input, file_output)
    data_json = {"annotationId": annot_id,
                 "content": encode_in_base64(xml_to_encode)}

    r = requests.post('https://my-little-endpoint.ok/rossum', data=data_json)

