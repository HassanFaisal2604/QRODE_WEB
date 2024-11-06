import qrcode
from qrcode import constants
from PIL import Image
import streamlit as st
from io import BytesIO

# Inject custom CSS to reduce the length of text input boxes
st.markdown(
    """
    <style>
    .short-text-input input {
        width: 200px !important;  /* Adjust the width as needed */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Simple QR Code Generator")

# Prompt the user for the data to encode in the QR code
data = st.text_input("Paste URL to encode in the QR code", key="data_input", help="Enter the URL or text to encode")

# Create a QRCode object with customizable parameters
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # Higher error correction for added reliability
    box_size=10,
    border=4,
)

# Add the user-provided data to the QR code
if data:
    qr.add_data(data)
    qr.make(fit=True)

    # Specify custom colors for the QR code and background
    # Wrap the fill color input in a div with the custom class
    fill_color = st.text_input("Enter the QR code color (e.g., 'blue', '#FF0000', etc.):", 
                                key="fill_color", 
                                help="Enter the QR code color")
    
    # Add the short-text-input class to the fill color input
    st.markdown('<div class="short-text-input"></div>', unsafe_allow_html=True)

    # Wrap the background color input in a div with the custom class
    back_color = st.text_input("Enter the background color (e.g., 'white', '#00FF00', etc.):", 
                                key="back_color", 
                                help="Enter the background color")

    # Add the short-text-input class to the background color input
    st.markdown('<div class="short-text-input"></div>', unsafe_allow_html=True)

    # Validate color inputs
    if fill_color and back_color:
        try:
            # Create the QR code image with the user-specified colors
            img = qr.make_image(fill_color=fill_color, back_color=back_color)

            # Save the QR code image with a custom filename
            filename = st.text_input("Enter the filename to save the QR code (e.g., 'my_qr_code.png'): ", 
                                      key="filename", 
                                      help="Enter the filename to save the QR code")
            if filename:
                img.save(filename)
                st.success(f"The QR code with the data '{data}' has been generated and saved as '{filename}'.")

                # Display the generated QR code image
                buffer = BytesIO()
                img.save(buffer, format="PNG")
                st.image(buffer, caption="Generated QR Code")
        except ValueError as e:
            st.error(f"Invalid color value: {e}")
    else:
        st.warning("Please enter both QR code color and background color.")
else:
    st.warning("Please enter the data to encode in the QR code.")