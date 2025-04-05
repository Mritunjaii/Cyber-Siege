import os
import re
import pdfplumber
import pytesseract
import pandas as pd
import cv2
from PIL import Image

# For OCR
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Update path as needed

# CSV Output
csv_data = []

# Field Extraction Function
def extract_fields(text):
    fields = {
        'Vendor Name': None,
        'Bill Number': None,
        'Billing Date': None,
        'Due Date': None,
        'Total Amount': None,
        'Line Items': None
    }

    # Regex or heuristic-based extraction
    fields['Vendor Name'] = re.findall(r'(?i)(?:from|vendor name)[:\s]+([A-Za-z &]+)', text) 
    fields['Bill Number'] = re.findall(r'(?i)(?:invoice|bill)\s*(?:no|number)?[:#\s]*([A-Z0-9-]+)', text)
    fields['Billing Date'] = re.findall(r'(?i)(?:billing|invoice)?\s*date[:\s]*([0-9/.\-]+)', text)
    fields['Due Date'] = re.findall(r'(?i)(?:Due Date|Last Date)[:\s]*([0-9/.\-]+)', text)
    fields['Total Amount'] = re.findall(r'(?i)(?:total amount|amount\s*due)[:\s$]*([0-9,]+\.\d{2})', text)
    
    # Line items: naive capture of tabular lines with numbers
    # lines = text.split("\n")
    # item_lines = [line for line in lines if re.search(r'\d+.*\d+\.\d{2}', line)]
    lines = text.split("\n")
    line_items = []

    for line in lines:
        # Match lines with structure: Item Desc, Qty, Unit Price, Total Price
        match = re.match(r'(.+?)\s+(\d+)\s+\$?([\d,]+(?:\.\d{2})?)\s+\$?([\d,]+(?:\.\d{2})?)$', line.strip())
        if match:
            item_desc = match.group(1).strip()
            quantity = int(match.group(2))
            unit_price = float(match.group(3).replace(',', ''))
            total_price = float(match.group(4).replace(',', ''))

            line_items.append({
                "Item Description": item_desc,
                "Quantity": quantity,
                "Unit Price": unit_price,
                "Total Price": total_price
            })
    # Format line items nicely
    fields['Line Items'] = "; ".join([
        f"{item['Item Description']} x{item['Quantity']} @ {item['Unit Price']:.2f} = {item['Total Price']:.2f}"
        for item in line_items[:10]
        ])


    # Clean up values
    for k, v in fields.items():
        if isinstance(v, list):
            fields[k] = v[0] if v else None

    return fields

def process_pdf(file_path):
    try:
        with pdfplumber.open(file_path) as pdf:
            text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
            return extract_fields(text)
    except Exception as e:
        print(f"Error processing PDF {file_path}: {e}")
        return {'Error': str(e)}

def process_image(file_path):
    try:
        img = cv2.imread(file_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)
        return extract_fields(text)
    except Exception as e:
        print(f"Error processing image {file_path}: {e}")
        return {'Error': str(e)}

def process_files(input_dir):
    for file in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file)
        data = {}
        try:
            if file.lower().endswith('.pdf'):
                print(f"Processing PDF: {file}")
                data = process_pdf(file_path)
            elif file.lower().endswith(('.png', '.jpg', '.jpeg')):
                print(f"Processing Image: {file}")
                data = process_image(file_path)
            else:
                print(f"Unsupported file: {file}")
                continue

            data['Source File'] = file
            csv_data.append(data)
        except Exception as e:
            print(f"Error processing file {file}: {e}")

# Save to CSV
def save_csv(output_path):
    df = pd.DataFrame(csv_data)
    df.to_csv(output_path, index=False)
    print(f"\nSaved extracted data to {output_path}")

# Run
if __name__ == "__main__":
    input_dir = os.path.join(os.path.dirname(__file__), "bills")
    output_csv = os.path.join(os.path.dirname(__file__), "extracted_bills.csv")    
    process_files(input_dir)
    save_csv(output_csv)
