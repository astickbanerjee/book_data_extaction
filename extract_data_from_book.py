import os
from pdf2image import convert_from_path
import easyocr

# Paths and file settings
source_pdf = "D:\\MyProjects\\banglar_bidyalay\\data\\book_data\\books\\wb_class _6\\Ha Ja Ba Ra La Class VI.pdf"

temp_image_folder = "temp_images"  # Temporary folder to save images from PDF pages
output_md_file = "output2.md"

# Ensure temp folder exists
os.makedirs(temp_image_folder, exist_ok=True)

# PART 1: Convert PDF pages to images and save them in temp folder
print("Converting PDF pages to images...")
page_images = convert_from_path(source_pdf)  # Convert PDF pages to images

for i, page_image in enumerate(page_images):
    image_path = os.path.join(temp_image_folder, f"page_{i+1}.png")
    page_image.save(image_path, "PNG")  # Save each page as a separate image
    print(f"Saved page {i+1} as {image_path}")

# PART 2: Perform OCR on each saved image and write results to markdown
print("Performing OCR on images...")
reader = easyocr.Reader(['en','bn'])  # Initialize EasyOCR reader; add 'bn' for Bengali if needed

markdown_content = ""  # Initialize markdown content

for i, image_filename in enumerate(sorted(os.listdir(temp_image_folder)), start=1):
    image_path = os.path.join(temp_image_folder, image_filename)
    
    # Perform OCR on the image with EasyOCR
    ocr_result = reader.readtext(image_path, detail=0)  # Extract text without bounding box details
    ocr_text = "\n".join(ocr_result)
    
    # Add OCR text for this page to markdown content
    markdown_content += f"\n\n## Page {i} Image Text\n{ocr_text}\n"
    print(f"OCR completed for page {i}")

# Save the markdown content to a file
with open(output_md_file, "w", encoding="utf-8") as file:
    file.write(markdown_content)

print(f"Markdown content with OCR saved to {output_md_file}")

# Clean up: Optionally remove the temporary images
for file_name in os.listdir(temp_image_folder):
    os.remove(os.path.join(temp_image_folder, file_name))
os.rmdir(temp_image_folder)
print("Temporary images cleaned up.")
