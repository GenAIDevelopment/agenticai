import os
import pymupdf  # The import name for PyMuPDF

def extract_content_by_page(book_path):
    # Define directory paths
    text_dir = os.path.join("extracted", "text")
    image_dir = os.path.join("extracted", "images")
    
    # Create the directories if they don't exist
    os.makedirs(text_dir, exist_ok=True)
    os.makedirs(image_dir, exist_ok=True)
    
    # Open the PDF document
    doc = pymupdf.open(book_path)
    print(f"Processing: {book_path} ({len(doc)} pages)")

    for page_index, page in enumerate(doc):
        page_num = page_index + 1
        
        # 1. Extract and save text per page
        page_text = page.get_text("text")
        text_filename = f"page_{page_num}.txt"
        text_path = os.path.join(text_dir, text_filename)
        
        with open(text_path, "w", encoding="utf-8") as text_file:
            text_file.write(page_text)

        # 2. Extract and save images per page
        image_list = page.get_images(full_text=True)
        
        for img_index, img in enumerate(image_list, start=1):
            xref = img[0]  # Get the XREF (cross-reference) number
            
            # Extract raw image dictionary
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]  # e.g., 'png', 'jpeg'
            
            # Create a unique filename incorporating the page number
            img_filename = f"page_{page_num}_img_{img_index}.{image_ext}"
            img_path = os.path.join(image_dir, img_filename)
            
            # Save the binary data directly to disk
            with open(img_path, "wb") as img_file:
                img_file.write(image_bytes)

    print("Extraction complete! Files organized in 'extracted/text' and 'extracted/images'.")

# Usage
extract_content_by_page("example.pdf")
