import os
from pdf2image import convert_from_path
import easyocr
import shutil
import re

# Define main folders
# C:\Users\Astick\Documents\MyProjectsC_Drive\book_data\books
# source_folder = "C:\\Users\\Astick\\Documents\\MyProjectsC_Drive\\book_data\\books"
# output_folder = "C:\\Users\\Astick\\Documents\\MyProjectsC_Drive\\book_data\\book_scan_data"


source_folder = "/Users/astick/Library/CloudStorage/GoogleDrive-astick.banerjee@bbb.ac.in/Other computers/My_Laptop/MyProjectsC_Drive/book_data/books"
output_folder = "/Users/astick/Library/CloudStorage/GoogleDrive-astick.banerjee@bbb.ac.in/Other computers/My_Laptop/MyProjectsC_Drive/book_data/book_scan_data"

temp_image_folder = "temp_images"  # Folder to store images of each PDF

# Ensure output and temp folders exist
os.makedirs(output_folder, exist_ok=True)
os.makedirs(temp_image_folder, exist_ok=True)

# Initialize EasyOCR reader with English and Bengali, GPU=False to avoid memory issues
reader = easyocr.Reader(['en', 'bn'])

# Step 1: Convert all PDF pages to images if not already converted
print("Converting all PDF pages to images...")
for root, _, files in os.walk(source_folder):
    for file in files:
        if file.lower().endswith(".pdf"):
            pdf_name = os.path.splitext(file)[0]
            pdf_path = os.path.join(root, file)
            pdf_image_folder = os.path.join(temp_image_folder, pdf_name)
            
            # Check if the images for this PDF already exist
            if os.path.exists(pdf_image_folder) and os.listdir(pdf_image_folder):
                print(f"Images already exist for {pdf_name}, skipping conversion.")
                continue
            
            # Create folder to store images for each PDF
            os.makedirs(pdf_image_folder, exist_ok=True)
            print(f"Processing {pdf_path} to images...")

            try:
                # Convert PDF to images
                page_images = convert_from_path(pdf_path,thread_count=4,fmt="jpeg")
                for i, page_image in enumerate(page_images):
                    # Save each page as an image in the dedicated folder
                    image_path = os.path.join(pdf_image_folder, f"{pdf_name}_page_{i+1}.jpeg")
                    page_image.save(image_path, "JPEG")
                    print(f"Saved page {i+1} of {pdf_name} as {image_path}")
            except Exception as e:
                print(f"Error processing {pdf_path}: {e}")
                continue

# Helper function to sort files based on the page number in their filenames
def sort_by_page_number(filename):
    match = re.search(r'page_(\d+)', filename)
    if match:
        return int(match.group(1))
    return 0


# Step 2: Perform OCR on saved images and save to markdown files
print("\nStarting OCR on saved images...")
for pdf_name in os.listdir(temp_image_folder):
    pdf_image_folder = os.path.join(temp_image_folder, pdf_name)
    output_md_file = os.path.join(output_folder, f"{pdf_name}.md")
    
    # Check if the markdown file already exists
    if os.path.exists(output_md_file):
        print(f"OCR results already exist for {pdf_name}, skipping OCR.")
        continue
    
    if os.path.isdir(pdf_image_folder):
        markdown_content = ""  # Content for each markdown file
        
        # Get a sorted list of image files based on page number
        image_filenames = sorted(os.listdir(pdf_image_folder), key=sort_by_page_number)
        
        for i, image_filename in enumerate(image_filenames, start=1):
            image_path = os.path.join(pdf_image_folder, image_filename)
            
            # Perform OCR on the image
            print(f"Performing OCR on {image_path}")
            try:
                ocr_result = reader.readtext(image_path, detail=0)
                ocr_text = "\n".join(ocr_result)
                
                # Add OCR text for this page to markdown content
                markdown_content += f"\n\n## Page {i} of {pdf_name}\n{ocr_text}\n"
            except Exception as e:
                print(f"Error performing OCR on {image_path}: {e}")
                continue

        # Save markdown content to file
        with open(output_md_file, "w", encoding="utf-8") as file:
            file.write(markdown_content)
        
        print(f"OCR results saved for {pdf_name} to {output_md_file}")

# Optional: Clean up temporary images folder after OCR processing
# shutil.rmtree(temp_image_folder)
print("Temporary images cleaned up.")
