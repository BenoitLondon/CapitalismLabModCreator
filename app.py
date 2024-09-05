import streamlit as st
import pandas as pd
from PIL import Image
from io import BytesIO
import zipfile

# App title
st.title("Capitalism Lab Mod Creator")

# Sidebar for inputting product classes and names
st.sidebar.header("Add Product Classes and Names")

# Store product data
if "product_data" not in st.session_state:
    st.session_state.product_data = {"classes": {}, "images": {}}

# Input for product classes
new_class = st.sidebar.text_input("Enter New Product Class")

if st.sidebar.button("Add Class"):
    if new_class and new_class not in st.session_state.product_data["classes"]:
        st.session_state.product_data["classes"][new_class] = []
        st.success(f"Product class '{new_class}' added!")
    elif new_class in st.session_state.product_data["classes"]:
        st.warning(f"Product class '{new_class}' already exists.")
    else:
        st.error("Please enter a product class name.")

# Input for product names within a class
selected_class = st.sidebar.selectbox("Select Class to Add Products", list(st.session_state.product_data["classes"].keys()))

new_product_name = st.sidebar.text_input("Enter New Product Name")

if st.sidebar.button("Add Product"):
    if selected_class and new_product_name:
        if new_product_name not in st.session_state.product_data["classes"][selected_class]:
            st.session_state.product_data["classes"][selected_class].append(new_product_name)
            st.success(f"Product '{new_product_name}' added to class '{selected_class}'!")
        else:
            st.warning(f"Product '{new_product_name}' already exists in class '{selected_class}'.")
    else:
        st.error("Please select a class and enter a product name.")

# Show current products and classes
st.subheader("Current Product Classes and Products")
for product_class, products in st.session_state.product_data["classes"].items():
    st.write(f"### {product_class}")
    st.write(", ".join(products))

# Image Upload Section
st.subheader("Upload Images for Products")
uploaded_files = st.file_uploader("Choose images", accept_multiple_files=True, type=["png", "jpg", "jpeg"])

if uploaded_files:
    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file)
        st.session_state.product_data["images"][uploaded_file.name] = image
        st.image(image, caption=uploaded_file.name, use_column_width=True)

# Download the mod files as a zip
if st.button("Generate Mod Files"):
    with BytesIO() as buffer:
        with zipfile.ZipFile(buffer, 'w') as z:
            # Save product data as CSV
            product_df = pd.DataFrame([
                {"Class": cls, "Product": prod}
                for cls, products in st.session_state.product_data["classes"].items()
                for prod in products
            ])
            product_csv = product_df.to_csv(index=False)
            z.writestr("products.csv", product_csv)
            
            # Save images
            for image_name, image in st.session_state.product_data["images"].items():
                img_byte_arr = BytesIO()
                image.save(img_byte_arr, format='PNG')
                z.writestr(f"images/{image_name}", img_byte_arr.getvalue())

        # Provide the zip file to download
        st.download_button("Download Mod Package", buffer.getvalue(), "capitalism_lab_mod.zip", "application/zip")

