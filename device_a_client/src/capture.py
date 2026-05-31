"""Direct OS Graphic Pipeline Abstraction layer handling native pixel stream access buffers."""
import logging
import io
import mss
import cv2
import numpy as np

logger = logging.getLogger("client.capture")

class StealthScreenScanner:
    """
    High-performance memory-isolated display buffer capture engine.
    Bypasses standard Windows API window hooks to maintain zero desktop footprints.
    """
    def __init__(self):
        # Initialize the native multi-display mss capture context driver
        self.sct = mss.mss()
        # Grab primary monitor dimensions automatically
        self.monitor = self.sct.monitors[1]
        logger.info(f"Stealth capture engine initialized. Primary Display Bounds: {self.monitor}")

    def capture_frame_to_bytes(self, compression_quality: int = 80) -> bytes:
        """
        Captures raw screen pixel data directly into memory buffers.
        Converts to grayscale and applies JPEG compression to limit network signature.
        """
        try:
            # Extract raw screen bytes directly out of the OS graphics device pipeline
            screenshot = self.sct.grab(self.monitor)
            
            # Convert raw screen bytes directly into a fast, manageable NumPy array
            img = np.array(screenshot)
            
            # Performance Optimization: Drop from 4-channel BGRA down to 1-channel GRAYSCALE
            # This cuts our raw data array footprint down significantly before transmission
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
            
            # Downsample target resolution slightly to clean up any tiny text anti-aliasing artifacts
            # Downsampling speeds up text parsing accuracy for the local multimodal model
            height, width = gray_img.shape
            resized_img = cv2.resize(gray_img, (int(width * 0.9), int(height * 0.9)), interpolation=cv2.INTER_AREA)
            
            # Encode processing matrix array straight into an in-memory JPEG byte array
            success, byte_buffer = cv2.imencode('.jpg', resized_img, [int(cv2.IMWRITE_JPEG_QUALITY), compression_quality])
            
            if not success:
                logger.error("Failed to translate pixel matrix arrays into standardized JPEG compression byte vectors.")
                return b""
                
            return byte_buffer.tobytes()
            
        except Exception as error:
            logger.error(f"Critical system failure inside screen capture memory space: {str(error)}")
            return b""
