# Invoice Data Extractor

This Python script extracts structured data from invoice documents (PDFs and images) using a combination of PDF text extraction and OCR (Optical Character Recognition). It identifies key fields like vendor name, bill number, dates, amounts, and line items.

## Features

- Processes both PDF and image files (PNG, JPG, JPEG)
- Extracts common invoice fields using regex patterns
- Handles basic line item extraction from tables
- Outputs results to a structured CSV file

## Setup Instructions


1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Dependencies

- Python 3.6+
- Required packages:
  - `pdfplumber` (for PDF text extraction)
  - `pytesseract` (for OCR from images)
  - `opencv-python` (for image preprocessing)
  - `pandas` (for CSV output)
  - `Pillow` (image processing support)

## System Requirements

- Tesseract OCR installed on your system
  - On Ubuntu/Debian: `sudo apt install tesseract-ocr`
  - On macOS: `brew install tesseract`
  - On Windows: Download installer from [Tesseract GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

## How to Run the Script

1. Place your invoice files (PDFs/images) in a `bills` directory within the project folder

2. Run the script:
   ```bash
   python invoice_extractor.py
   ```

3. The extracted data will be saved to `extracted_bills.csv` in the project directory

## Assumptions

1. **Invoice Structure**: The script assumes invoices follow a common format with recognizable field labels (like "Bill Number:", "Due Date:", etc.)

2. **Text Quality**: For image files, assumes reasonable quality (300dpi or better) with clear text

3. **Field Locations**: Doesn't handle complex layouts - works best with simple, text-based invoices

4. **Line Items**: Basic table detection assumes items are in lines with quantity, unit price and total price

5. **Date Formats**: Recognizes common date formats but may need adjustment for non-standard formats

## Customization

To improve extraction accuracy:

1. Modify the regex patterns in `extract_fields()` to match your specific invoice formats
2. Add additional field extraction logic as needed
3. For better OCR results, preprocess images (adjust contrast, remove noise) before processing

## Limitations

- May not work well with scanned invoices that have complex layouts
- Hand-written invoices are not supported
- Currency symbols other than $ may need regex pattern updates

## Output Format

The script generates a CSV file with these columns:
- Vendor Name
- Bill Number
- Billing Date
- Due Date
- Total Amount
- Line Items (semicolon-separated)
- Source File (original filename)

## Troubleshooting

If you encounter issues:
- Verify Tesseract is installed and the path in the script is correct
- Check that input files are not password-protected
- For poor OCR results, try improving image quality before processing