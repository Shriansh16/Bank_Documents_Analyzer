import os
import google.generativeai as genai
import fitz  # PyMuPDF
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

class PDFExtractor:
    """
    A class that extracts text from PDFs using different methods
    based on whether the document is scanned or native.
    """
    
    def __init__(self, gemini_api_key):
        """
        Initialize the extractor with Gemini API credentials.
        """
        
        # Configure Gemini
        genai.configure(api_key=gemini_api_key)
        # Initialize Gemini 2.0 flash - best for OCR tasks
        self.gemini_model = genai.GenerativeModel('gemini-2.0-flash')
        
    def convert_pdf_page_to_image(self, pdf_path, page_num):
        """
        Convert a PDF page to an image for Gemini processing
        """
        doc = fitz.open(pdf_path)
        page = doc[page_num]
        
        # Get the page's pixmap (higher DPI for better OCR)
        pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))
        
        # Convert to PIL Image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        doc.close()
        return img

    def extract_text_from_scanned_pdf(self, pdf_path):
        """
        Extract text from a scanned PDF using Gemini Vision.
        """
        try:
            doc = fitz.open(pdf_path)
            extracted_text = {}

            for page_num in range(len(doc)):
                # Convert PDF page to image
                img = self.convert_pdf_page_to_image(pdf_path, page_num)
                
                # Generate prompt for Gemini
                prompt = """
                You are an expert data extractor and document classifier. Your task is to meticulously extract all relevant information from the provided bank statement image, classify the document type,categorize transactions (if present) into one of the following categories: 'Income', 'Expenses', 'Loans', or 'Investments' and structure all the data into a JSON format suitable for storage in MongoDB.
                """
                
                # Generate content using Gemini
                response = self.gemini_model.generate_content([prompt, img])
                
                # Extract text from response
                if response.text:
                    extracted_text[page_num + 1] = response.text.strip()
                else:
                    extracted_text[page_num + 1] = ""

            doc.close()
            return extracted_text
            
        except Exception as e:
            raise Exception(f"Error analyzing PDF: {str(e)}")
    
    def extract_text(self, pdf_path):
        """
        Main method to extract text from a PDF, automatically choosing
        the appropriate extraction method.
        """
        try:
            extracted_text = self.extract_text_from_scanned_pdf(pdf_path)
            return extracted_text
        except Exception as e:
            raise Exception(f"Error analyzing PDF: {str(e)}")

"""if __name__ == "__main__":
    pdf_path = 'Bank Statement Example Final.pdf'
    obj = PDFExtractor(gemini_api_key=os.getenv("GEMINI_API_KEY"))
    
    try:
        extracted_text = obj.extract_text(pdf_path)

        eturn extracted_text

    except Exception as e:
        print(f"Error: {str(e)}")"""
