"""Enterprise-grade local text extraction engine parsing screen matrices."""
import logging
import cv2
import numpy as np
import easyocr

logger = logging.getLogger("client.ocr")

class LocalScreenParser:
    """Uses localized deep learning models to pull text characters out of compressed screen buffers."""
    def __init__(self):
        logger.info("Initializing local EasyOCR text extraction models...")
        # Initialize text parser for English language characters safely on CPU/GPU
        self.reader = easyocr.Reader(['en'], gpu=False) 
        logger.info("Local OCR processing core successfully loaded.")

    def extract_text_from_jpeg_bytes(self, jpeg_bytes: bytes) -> str:
        """Converts raw image bytes back to processing arrays and runs character extraction."""
        try:
            if not jpeg_bytes:
                return ""
            
            # Decode memory byte buffers back into standard NumPy image arrays
            nparr = np.frombuffer(jpeg_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
            
            # Execute localized semantic deep character reading loops
            results = self.reader.readtext(img, detail=0)
            
            # Reconstruct disparate text blocks into a single structured problem statement string
            parsed_payload = " ".join(results).strip()
            logger.info(f"OCR Extraction Cycle Complete. Parsed: {len(parsed_payload)} characters.")
            return parsed_payload
            
        except Exception as error:
            logger.error(f"Failed to process image matrix characters: {str(error)}")
            return ""

# Initialize global worker token
screen_ocr = LocalScreenParser()