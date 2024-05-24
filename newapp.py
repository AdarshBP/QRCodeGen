import streamlit as st
from segno import make
from PIL import Image
from io import BytesIO

def generate_qr(data, error="M"):
    qr_code = make(data, error=error)
    return qr_code

st.title("QR Code Generator")

data_input = st.text_input("Enter data to encode:")
error_correction = st.selectbox("Error Correction Level", ("L", "M", "Q", "H"))
size_factor = st.slider("Size Factor (1-10)", 1, 10)

if st.button("Generate QR Code"):
  if data_input:
    qr_image = generate_qr(data_input, error=error_correction)
    qr_image.save("qr_code.png",scale=size_factor)

    st.image(qr_image, use_column_width=True)
  else:
    st.warning("Please enter data to encode.")

