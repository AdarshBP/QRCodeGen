import streamlit as st
from io import BytesIO
import base64
import segno


# Define CSS style to center the button
css = """
    <style>
        .stButton,.stTitle{
            display: flex;
            justify-content: center;
        } 
    </style>
"""

def generate_qr_code(input_text):
    qr = segno.make(input_text,error="H")
    return qr

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
        geo_data = st.text_input("Enter Latitude,Longitude:")
        input_text = f"geo:{geo_data}"
    return input_text


def main():
    # Display the CSS style
    st.markdown(css, unsafe_allow_html=True)
    st.title("QR Code Generator")
    
    # Place controls in the sidebar
    with st.sidebar:

        # Dropdown for selecting QR type
        qr_type = st.sidebar.selectbox("Select QR Type", ["Text", "URL" ,"vCard", "WiFi", "WhatsApp", "Email","SMS","Phone","Geolocation"])

        input_text = generateText(qr_type)

        # Checkbox for toggling advanced options
        show_advanced_options = st.checkbox("Show Advanced Options")

        # Retrieve configuration options
        scale_size, rotate, border, transparent_bg, data_color, bg_color, uploaded_file = retrieve_configuration(show_advanced_options)

    
    # Generate QR button
    if st.sidebar.button("Generate QR"):
        if input_text:
            
            qr_image_bytes = BytesIO()
            qr_image = generate_qr_code(input_text)
            
            if transparent_bg:
                bg_color = None

            #To add image to the qr code
            if uploaded_file:
                qr_image.to_artistic(background=uploaded_file, target=qr_image_bytes, scale=scale_size,border=border,dark=data_color, light=bg_color, kind='PNG')
                st.image(qr_image_bytes)
            else:
                img = qr_image.to_pil(scale=scale_size,border=border,dark=data_color, light=bg_color).rotate(rotate)
                img.save(qr_image_bytes, format='PNG')
                st.image(qr_image_bytes)



            # Encode the binary data as Base64
            encoded_image = base64.b64encode(qr_image_bytes.getvalue()).decode()
            # Display the CSS style
            st.markdown(css, unsafe_allow_html=True)

            # Centered download button
            st.markdown(
                f"""<div >
                    <a href="data:image/png;base64,{encoded_image}" download="generated_qr_code.png">
                        <button class="css-1qrvfrg">Download QR Code</button>
                    </a>
                </div>""",
                unsafe_allow_html=True
            )
        else:
            st.warning("Please enter some text or URL.")

def advanced_options():
    # Slider for adjusting box size
    scale_size = st.slider("Box Size", min_value=1, max_value=30, value=10, key="Box_SIZE_KEY")
    # Rotate slider
    rotate = st.slider("Rotate", min_value=0, max_value=90, value=0, key="ROTATE_KEY")
    # Slider for adjusting border
    border = st.slider("Border", min_value=0, max_value=20, value=4, key="BORDER_KEY")
    # Background color with checkbox for transparent background
    transparent_bg = st.checkbox("Transparent Background", False)
    data_color = st.color_picker("Pick a Data color", "#000000")
    bg_color = st.color_picker("Pick a Background color", "#FFFFFF")
    # Image uploader 
    uploaded_file = st.file_uploader("Upload an image or GIF", type=["jpg", "jpeg", "png", "GIF"])

    return scale_size, rotate, border, transparent_bg, data_color, bg_color, uploaded_file


def retrieve_configuration(show_advanced_options):
    if show_advanced_options:
        return advanced_options()
    else:
        return 10, 0, 4, False, "#000000", "#FFFFFF", None  # Default values for basic options
    

if __name__ == "__main__":
    main()