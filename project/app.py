import os

import streamlit as st
from PIL import Image

from image_pii import pipeline
from pii_list import *
from utils import delete_all_images


def gen_pii_checklist():
    pii_checklist = []

    st.sidebar.title("PII Selection")
    address_ = st.sidebar.checkbox(address, value=True)
    age_ = st.sidebar.checkbox(age)
    aws_access_ = st.sidebar.checkbox(aws_access)
    aws_secret_ = st.sidebar.checkbox(aws_secret)
    bank_acc_ = st.sidebar.checkbox(bank_acc, value=True)
    bank_route_ = st.sidebar.checkbox(bank_route)
    credit_cvv_ = st.sidebar.checkbox(credit_cvv)
    credit_expiry_ = st.sidebar.checkbox(credit_expiry)
    credit_no_ = st.sidebar.checkbox(credit_no, value=True)
    date_time_ = st.sidebar.checkbox(date_time)
    driver_id_ = st.sidebar.checkbox(driver_id, value=True)
    ip_add_ = st.sidebar.checkbox(ip_add)
    mac_add_ = st.sidebar.checkbox(mac_add)
    name_ = st.sidebar.checkbox(name)
    email_ = st.sidebar.checkbox(email, value=True)
    phone_ = st.sidebar.checkbox(phone, value=True)
    passport_ = st.sidebar.checkbox(passport, value=True)
    pin_ = st.sidebar.checkbox(pin)
    ssn_ = st.sidebar.checkbox(ssn, value=True)
    url_ = st.sidebar.checkbox(url)
    username_ = st.sidebar.checkbox(username)
    password_ = st.sidebar.checkbox(password)

    if address_: pii_checklist.append(address)
    if age_: pii_checklist.append(age)
    if aws_access_: pii_checklist.append(aws_access)
    if aws_secret_: pii_checklist.append(aws_secret)
    if bank_acc_: pii_checklist.append(bank_acc)
    if bank_route_: pii_checklist.append(bank_route)
    if credit_cvv_: pii_checklist.append(credit_cvv)
    if credit_expiry_: pii_checklist.append(credit_expiry)
    if credit_no_: pii_checklist.append(credit_no)
    if date_time_: pii_checklist.append(date_time)
    if driver_id_: pii_checklist.append(driver_id)
    if ip_add_: pii_checklist.append(ip_add)
    if mac_add_: pii_checklist.append(mac_add)
    if name_: pii_checklist.append(name)
    if email_: pii_checklist.append(email)
    if phone_: pii_checklist.append(phone)
    if passport_: pii_checklist.append(passport)
    if pin_: pii_checklist.append(pin)
    if ssn_: pii_checklist.append(ssn)
    if url_: pii_checklist.append(url)
    if username_: pii_checklist.append(username)
    if password_: pii_checklist.append(password)

    return pii_checklist



def main():
    st.title("Image PII Detector")
    st.text("Detect if PII is present in images. Uses AWS Textract & Comprehend APIs")
    input_folder = st.text_input("folder path to images")
    pii_checklist = gen_pii_checklist()
    if st.button("Start"):
        with st.spinner(text="Extracting PII..."):
            delete_all_images()
            df = pipeline(input_folder, pii_checklist, output_image=True)
            st.header("PII Report Summary")
            st.dataframe(df)

    if st.button("Display images with PII"):
        out_folder = "output"
        img_list = []
        for i in os.listdir(out_folder):
            if i.endswith(("jpg", "jpeg", "png")):
                image = Image.open(os.path.join(out_folder, i))
                img_list.append(image)
                
        st.image(img_list, caption=img_list)

if __name__ == "__main__":
    main()