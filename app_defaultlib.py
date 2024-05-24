import streamlit as st
import qrcode
from io import BytesIO
import base64


# Define CSS style to center the button
css = """
    <style>
        .centered {
            display: flex;
            justify-content: center;
        }
    </style>
"""

def generate_qr_code(input_text, box_size, border,error_level):
    if error_level == "ERROR_CORRECT_L":
        error_correction = qrcode.constants.ERROR_CORRECT_L
    elif error_level == "ERROR_CORRECT_M":
        error_correction = qrcode.constants.ERROR_CORRECT_M
    elif error_level == "ERROR_CORRECT_Q":
        error_correction = qrcode.constants.ERROR_CORRECT_Q
    elif error_level == "ERROR_CORRECT_H":
        error_correction = qrcode.constants.ERROR_CORRECT_H
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=error_correction,
        box_size=box_size,
        border=border,
    )
    qr.add_data(input_text)
    qr.make(fit=True)

    qr_image = qr.make_image(fill_color="black", back_color="white")
    return qr_image

def generateText(qr_type):
    if qr_type == "Text":
        input_text = st.text_input("Enter text:")
    elif qr_type == "vCard":
        #  Define the vCard data
        # example vcard = """BEGIN:VCARD
        # VERSION:4.0
        # FN:John Smith
        # ORG:Example Company
        # TITLE:CEO
        # TEL;TYPE=WORK,VOICE:(555) 555-5555
        # EMAIL;TYPE=PREF,INTERNET:john.smith@example.com
        # URL:https://www.example.com
        # END:VCARD"""
        vcard_version = st.selectbox("vCard Version", ["2.1", "3.0", "4.0"])
        vcard_name = st.text_input("Name:")
        vcard_org = st.text_input("Organization:")
        vcard_title = st.text_input("Title:")
        vcard_tel = st.text_input("Telephone:")
        vcard_email = st.text_input("Email:")
        vcard_url = st.text_input("URL:")
        input_text = f"""BEGIN:VCARD VERSION:{vcard_version} FN:{vcard_name} ORG:{vcard_org} TITLE:{vcard_title} TEL;TYPE=WORK,VOICE:{vcard_tel} EMAIL;TYPE=PREF,INTERNET:{vcard_email} URL:{vcard_url} END:VCARD"""
    elif qr_type == "WiFi":
        # Define the WiFi data
        # example wifi = "WIFI:S:Example_Network;T:WPA;P:password123;;"
        wifi_ssid = st.text_input("WiFi SSID:")
        wifi_password = st.text_input("WiFi Password:")
        wifi_security = st.selectbox("Security", ["WEP", "WPA", "WPA2"])
        input_text = f"WIFI:S:{wifi_ssid};T:{wifi_security};P:{wifi_password};;"
    elif qr_type == "WhatsApp":
        # Define the WhatsApp data
        # example whatsapp = "https://wa.me/15551234567"
        whatsapp_number = st.text_input("WhatsApp Number:")
        input_text = f"https://wa.me/{whatsapp_number}"
    elif qr_type == "Email":
        # Define the Email data
        # example email = "mailto:
        email_address = st.text_input("Email Address:")
        email_subject = st.text_input("Subject:")
        email_body = st.text_area("Body:")
        input_text = f"mailto:{email_address}?subject={email_subject}&body={email_body}"
    elif qr_type == "SMS":
        # Define the SMS data
        # example sms = "SMSTO:15551234567:Hello%20World"
        sms_number = st.text_input("SMS Number:")
        sms_body = st.text_area("Body:")
        input_text = f"SMSTO:{sms_number}:{sms_body}"
    elif qr_type == "URL":
        input_text = st.text_input("Enter URL:")
    elif qr_type == "Phone":
        input_text = st.text_input("Enter Phone Number:")
    elif qr_type == "Geolocation":
        input_text = st.text_input("Enter Latitude,Longitude:")
    return input_text


def main():
    st.title("QR Code Generator")
    
    # Place controls in the sidebar
    with st.sidebar:

        # Dropdown for selecting QR type
        qr_type = st.selectbox("Select QR Type", ["Text", "URL" ,"vCard", "WiFi", "WhatsApp", "Email","SMS","Phone","Geolocation"])

        input_text = generateText(qr_type)

        # Dropdown for selecting error level
        error_level = st.selectbox("Select Error Correcetion Level", ["ERROR_CORRECT_L","ERROR_CORRECT_M","ERROR_CORRECT_Q","ERROR_CORRECT_H"])

        # Slider for adjusting box size
        box_size = st.slider("Box Size", min_value=1, max_value=30, value=10)


        # Slider for adjusting border
        border = st.slider("Border", min_value=0, max_value=20, value=4)

    
    # Generate QR button
    if st.sidebar.button("Generate QR") and ( box_size or border ):
        if input_text:
            qr_image = generate_qr_code(input_text, box_size, border,error_level)
            # Convert PIL image to bytes
            qr_image_bytes = BytesIO()
            qr_image.save(qr_image_bytes, format='PNG')
            st.image(qr_image_bytes, use_column_width=True)
            # Encode the binary data as Base64
            encoded_image = base64.b64encode(qr_image_bytes.getvalue()).decode()
            # Display the CSS style
            st.markdown(css, unsafe_allow_html=True)

            # Centered download button
            st.markdown(
                f"""<div class='centered'>
                    <a href="data:image/png;base64,{encoded_image}" download="generated_qr_code.png">
                        <button>Download QR Code</button>
                    </a>
                </div>""",
                unsafe_allow_html=True
            )
        else:
            st.warning("Please enter some text or URL.")



if __name__ == "__main__":
    main()