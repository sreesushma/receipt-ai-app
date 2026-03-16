# receipt-ai-app
A small project I built to experiment with OCR and document parsing.

The app lets you upload a receipt image, extracts useful information (store name, date, total, and items), and automatically logs the result into an Excel expense tracker.

The goal was to explore how OCR works in real applications and how messy real-world data can be.

Tech Stack:
* Python
* FastAPI
* Tesseract OCR
* OpenCV
* OpenPyXL
* TailwindCSS
* JavaScript

How it works
* Upload a receipt image through the web interface
* The backend preprocesses the image using OpenCV
* Tesseract OCR extracts the text from the receipt
* A parser tries to identify the store name, date, total, and items
* The extracted data is appended to an Excel file

Running the project

Install dependencies:
pip install fastapi uvicorn pytesseract opencv-python openpyxl python-multipart

Make sure Tesseract OCR is installed on your system.

Run the app:
uvicorn backend.main:app --reload

Then open:
http://127.0.0.1:8000

Challenges

Receipts are surprisingly hard to process because:
* OCR can misread characters (e.g. TOTAL → Totall)
* Different stores use completely different layouts
* Lighting and image quality affect accuracy
* Parsing useful information from raw OCR text is tricky
Improving results required experimenting with image preprocessing and parsing logic.

Future improvements

* Improve receipt parsing accuracy
* Better item detection
* Support more receipt formats
* Possibly train a model for receipt understanding

This is a work in progress, but it was a fun way to learn more about OCR pipelines and document AI.
