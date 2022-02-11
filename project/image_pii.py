import os

import boto3
import pandas as pd

from util import label_image_pii
from pii_list import *

# boto3 clients
textract = boto3.client('textract')
comprehend = boto3.client('comprehend')


def textract_output(image, delimiter="    "):
    """using AWS Textract, get text from images & concat them together"""

    response = textract.detect_document_text(
                    Document={'Bytes': image})
    concat_text = ""
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            # add 4 spaces to separate each text pharse
            concat_text = concat_text + delimiter + item["Text"]
    return concat_text, response


def translate_pii_textract_coord(textr_results, pii_txt):
    """translate pii text from comprehend to coordinates from textract"""

    coordinates_list = []
    for textr_result in textr_results["Blocks"]:
        if textr_result["BlockType"] == "LINE":
            for pii in pii_txt:
                if pii in textr_result["Text"]:
                    coordinates = textr_result["Geometry"]["Polygon"]
                    coordinates_list.append(coordinates)
    return coordinates_list


def comprehend_pii(concat_text, pii_list, threshold=0.7, len_pii=3,
    language="en", delimiter="    "):
    """using AWS Comprehend, output pii detected, if any"""

    response = comprehend.detect_pii_entities(
                    Text=concat_text,
                    LanguageCode=language)["Entities"]
    pii_txt = []
    pii_types = []
    if len(response) > 0:
        for item in response:
            if item["Type"] in pii_list and item["Score"] > threshold:
                offset_txt = concat_text[item["BeginOffset"]:item["EndOffset"]]
                offset_txt = offset_txt.strip(delimiter)
                type = item["Type"]
                if delimiter not in offset_txt:
                    # ignore pii if length is less than specified
                    if len(offset_txt) >= len_pii:
                        pii_txt.append(offset_txt)
                        pii_types.append(type)
                else:
                    offset_split = offset_txt.split(delimiter)
                    for i in offset_split:
                        if len(i) >= len_pii:
                            pii_txt.append(i)
                            pii_types.append(type)

    return pii_types, pii_txt


def report_phrasing(filename, pii_types, pii_list):
    "generate content of each row of PII report dataframe"
    
    contents = {"filename": filename}
    if address in pii_types and pii_list: contents[address] = 1
    if age in pii_types and pii_list: contents[age] = 1
    if aws_access in pii_types and pii_list: contents[aws_access] = 1
    if aws_secret in pii_types and pii_list: contents[aws_secret] = 1
    if bank_acc in pii_types and pii_list: contents[bank_acc] = 1
    if bank_route in pii_types and pii_list: contents[bank_route] = 1
    if credit_cvv in pii_types and pii_list: contents[credit_cvv] = 1
    if credit_expiry in pii_types and pii_list: contents[credit_expiry] = 1
    if credit_no in pii_types and pii_list: contents[credit_no] = 1
    if date_time in pii_types and pii_list: contents[date_time] = 1
    if driver_id in pii_types and pii_list: contents[driver_id] = 1
    if email in pii_types and pii_list: contents[email] = 1
    if ip_add in pii_types and pii_list: contents[ip_add] = 1
    if mac_add in pii_types and pii_list: contents[mac_add] = 1
    if name in pii_types and pii_list: contents[name] = 1
    if passport in pii_types and pii_list: contents[passport] = 1
    if phone in pii_types and pii_list: contents[phone] = 1
    if pin in pii_types and pii_list: contents[pin] = 1
    if ssn in pii_types and pii_list: contents[ssn] = 1
    if url in pii_types and pii_list: contents[url] = 1
    if username in pii_types and pii_list: contents[username] = 1
    if password in pii_types and pii_list: contents[password] = 1
    return contents


def pipeline(image_folder,
                pii_list,
                output_report=True, 
                output_image=True,
                formats=(".jpeg", "jpg", "png")):
    """iterate folder, extract all images, and output PII report in csv"""
    
    # create empty df for report
    cols = ["filename"] + pii_list
    df = pd.DataFrame(columns=cols)
    
    # iterate through all images for PII detection
    for root, dirs, files in os.walk(image_folder):
        for i in files:
            if i.endswith(formats):
                img_path = os.path.join(root, i)
                with open(img_path, 'rb') as img:
                    img = bytearray(img.read())
                    # textract
                    message, res = textract_output(img)
                    if len(message) > 0:
                        # pii comprehend
                        pii_types, pii_txt = comprehend_pii(message, pii_list)

                        contents = report_phrasing(i, pii_types, pii_list)
                        df = df.append(contents, ignore_index=True)

                        if output_image:
                            coordinates_list = translate_pii_textract_coord(res, pii_txt)
                            if len(coordinates_list) > 0:
                                label_image_pii(img_path, coordinates_list, pii_types)

    if output_report:
        df.to_csv("pii_report.csv")

    return df




if __name__ == "__main__":
    pii_list = [address,
                bank_acc, bank_route, credit_cvv,
                credit_expiry, credit_no,
                driver_id, email,
                name, passport, password, phone,
                pin, ssn, username]

    input_folder = "images/"
    df = pipeline(input_folder, pii_list)
    print(df)
