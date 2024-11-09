import qrcode
from qrcode import constants
from PIL import Image
import streamlit as st
from io import BytesIO

# Custom CSS for layout and styling
st.markdown("""
    <style>
    /* Make text inputs shorter */
    .short-text-input input {
        width: 120px !important;
    }
    
    /* Remove padding from columns */
    .stColumn {
        padding: 0 !important;
    }
    
    /* Adjust image container */
    .stImage {
        margin-top: 20px;
    }
    
    /* Center the image in its column */
    [data-testid="column"] {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    /* Reduce vertical spacing between elements */
    .element-container {
        margin-bottom: 10px !important;
    }
    
    /* Make success/warning messages more compact */
    .stSuccess, .stWarning {
        padding: 5px !important;
    }
    
    /* Style download button */
    .stDownloadButton {
        margin-top: -0.7rem;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Simple QR Code Generator")

# Create two columns for layout
left_col, right_col = st.columns([1, 1])

# Left column - Input fields
with left_col:
    # Prompt the user for the data to encode in the QR code
    data = st.text_input(
        "Paste URL to encode in the QR code", 
        key="data_input", 
        help="Enter the URL or text to encode"
    )

    # Create a QRCode object with customizable parameters
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    if data:
        qr.add_data(data)
        qr.make(fit=True)

        fill_color = st.text_input(
            "QR code color:", 
            key="fill_color",
            help="Enter color (e.g., 'blue', '#FF0000')"
        )

        back_color = st.text_input(
            "Background color:", 
            key="back_color",
            help="Enter color (e.g., 'white', '#FFFFFF')"
        )

        filename = st.text_input(
            "Save filename:", 
            value="qr_code.png",
            key="filename",
            help="Enter filename (e.g., 'my_qr_code.png')"
        )

# Right column - QR Code display and download
with right_col:
    if data and fill_color and back_color:
        try:
            # Create the QR code image
            img = qr.make_image(fill_color=fill_color, back_color=back_color)
            
            # Save to buffer for display and download
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            
            # Display the generated QR code image
            st.image(buffer, caption="Generated QR Code", use_column_width=True)
            
            # Add download button
            st.download_button(
                label="Download QR Code",
                data=buffer,
                file_name=filename if filename.endswith('.png') else f"{filename}.png",
                mime="image/png"
            )
            
            if filename:
                # Save the QR code image locally
                img.save(filename)
                st.success(f"QR code saved as '{filename}'")
        
        except ValueError as e:
            st.error(f"Invalid color value: {e}")
    elif data:
        st.warning("Please enter both colors")
    else:
        st.warning("Please enter data for the QR code")