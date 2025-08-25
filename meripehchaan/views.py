# views.py - Enhanced version with PDF support and improved QR detection
import io
import requests
import cv2
import numpy as np
from PIL import Image
import xml.etree.ElementTree as ET
import re
import fitz  # PyMuPDF for PDF handling
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import base64

# API Setu credentials
CLIENT_ID = "XI865B1FF4"
CLIENT_SECRET = "f4140b280671c3210f04"
AUTH_URL = "https://api.apisetu.gov.in/uidai/verifyAadhaar/token"
VERIFY_URL = "https://api.apisetu.gov.in/uidai/verifyAadhaar"

def extract_images_from_pdf(pdf_file):
    """Extract images from PDF file"""
    try:
        pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
        images = []
        
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            
            # Get images from page
            image_list = page.get_images()
            
            for img_index, img in enumerate(image_list):
                # Get the XREF of the image
                xref = img[0]
                
                # Extract the image bytes
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                
                # Convert to PIL Image
                image = Image.open(io.BytesIO(image_bytes))
                images.append(image)
            
            # Also render the page as an image (in case QR is not an embedded image)
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom for better quality
            img_data = pix.tobytes("png")
            page_image = Image.open(io.BytesIO(img_data))
            images.append(page_image)
        
        pdf_document.close()
        return images
        
    except Exception as e:
        print(f"PDF extraction error: {e}")
        return []

def preprocess_image_for_qr(image):
    """Advanced image preprocessing for better QR detection"""
    try:
        # Convert PIL to OpenCV format
        if isinstance(image, Image.Image):
            image_array = np.array(image)
            if len(image_array.shape) == 3:
                if image_array.shape[2] == 4:  # RGBA
                    image_cv = cv2.cvtColor(image_array, cv2.COLOR_RGBA2BGR)
                elif image_array.shape[2] == 3:  # RGB
                    image_cv = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
                else:
                    image_cv = image_array
            else:
                image_cv = image_array
        else:
            image_cv = image.copy()

        # Convert to grayscale
        if len(image_cv.shape) == 3:
            gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
        else:
            gray = image_cv.copy()

        processed_images = []
        
        # Original grayscale
        processed_images.append(("original_gray", gray))
        
        # Noise reduction
        denoised = cv2.medianBlur(gray, 3)
        processed_images.append(("denoised", denoised))
        
        # Contrast enhancement using CLAHE
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        clahe_enhanced = clahe.apply(gray)
        processed_images.append(("clahe", clahe_enhanced))
        
        # Gamma correction
        gamma = 1.5
        gamma_corrected = np.array(255 * (gray / 255) ** gamma, dtype='uint8')
        processed_images.append(("gamma", gamma_corrected))
        
        # Bilateral filter for edge preservation
        bilateral = cv2.bilateralFilter(gray, 9, 75, 75)
        processed_images.append(("bilateral", bilateral))
        
        # Multiple threshold methods
        _, otsu_thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        processed_images.append(("otsu", otsu_thresh))
        
        # Adaptive thresholding variants
        adaptive_mean = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 10)
        processed_images.append(("adaptive_mean", adaptive_mean))
        
        adaptive_gaussian = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 10)
        processed_images.append(("adaptive_gaussian", adaptive_gaussian))
        
        # Morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        morph_close = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
        processed_images.append(("morph_close", morph_close))
        
        morph_open = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
        processed_images.append(("morph_open", morph_open))
        
        # Sharpening
        kernel_sharp = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        sharpened = cv2.filter2D(gray, -1, kernel_sharp)
        processed_images.append(("sharpened", sharpened))
        
        # Multiple scales
        height, width = gray.shape
        
        # Upscale for small images
        if height < 500 or width < 500:
            upscaled = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            processed_images.append(("upscaled_2x", upscaled))
            
            upscaled_3x = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
            processed_images.append(("upscaled_3x", upscaled_3x))
        
        # Downscale for very large images
        if height > 2000 or width > 2000:
            downscaled = cv2.resize(gray, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
            processed_images.append(("downscaled", downscaled))
        
        return processed_images
        
    except Exception as e:
        print(f"Preprocessing error: {e}")
        return [("original", gray if 'gray' in locals() else image)]

def detect_qr_with_multiple_detectors(image):
    """Try multiple QR detection methods"""
    detectors = []
    results = []
    
    try:
        # OpenCV QR Detector
        opencv_detector = cv2.QRCodeDetector()
        detectors.append(("opencv", opencv_detector))
        
        for detector_name, detector in detectors:
            try:
                if detector_name == "opencv":
                    data, vertices, _ = detector.detectAndDecode(image)
                    if data and vertices is not None:
                        results.append((detector_name, data, vertices))
                
            except Exception as e:
                print(f"{detector_name} detection failed: {e}")
                continue
    
    except Exception as e:
        print(f"Detector initialization error: {e}")
    
    return results

def decode_qr_enhanced(image):
    """
    Most comprehensive QR code detection with multiple methods and preprocessing
    """
    try:
        print(f"Starting enhanced QR detection...")
        
        # Get preprocessed versions of the image
        processed_images = preprocess_image_for_qr(image)
        print(f"Generated {len(processed_images)} preprocessed versions")
        
        all_detections = []
        
        # Try each preprocessed image with multiple detectors
        for method_name, processed_img in processed_images:
            try:
                detections = detect_qr_with_multiple_detectors(processed_img)
                for detector_name, data, vertices in detections:
                    if data and len(data.strip()) > 0:
                        combined_method = f"{detector_name}_{method_name}"
                        all_detections.append((combined_method, data))
                        print(f"QR detected with {combined_method}: {data[:50]}...")
                        
            except Exception as e:
                print(f"Detection failed for {method_name}: {e}")
                continue
        
        # Remove duplicates while preserving order
        seen_data = set()
        unique_detections = []
        for method, data in all_detections:
            if data not in seen_data:
                seen_data.add(data)
                unique_detections.append(create_qr_decoded(data))
        
        if unique_detections:
            print(f"Found {len(unique_detections)} unique QR codes")
            return unique_detections
        
        print("No QR codes detected with enhanced methods")
        return []
        
    except Exception as e:
        print(f"Enhanced QR decode error: {e}")
        return []

def create_qr_decoded(data_str):
    """Helper function to create QR decoded object"""
    class QRDecoded:
        def __init__(self, data_str):
            self.data = data_str.encode('utf-8')
            self.type = 'QRCODE'
    return QRDecoded(data_str)

def extract_aadhaar_from_qr(qr_data):
    """Extract Aadhaar number from QR code data with enhanced patterns"""
    try:
        print(f"Extracting Aadhaar from QR data (length: {len(qr_data)})")
        
        # Method 1: XML parsing with multiple attempts
        xml_attempts = [
            qr_data.strip(),  # Original
            qr_data.strip().lstrip('\ufeff'),  # Remove BOM
            qr_data.strip().replace('\x00', ''),  # Remove null bytes
            re.sub(r'[^\x20-\x7E\n\r\t]', '', qr_data).strip()  # Remove non-printable chars
        ]
        
        for attempt_data in xml_attempts:
            try:
                if attempt_data.startswith('<'):
                    root = ET.fromstring(attempt_data)
                    uid = root.get('uid')
                    if uid and len(uid) == 12 and uid.isdigit():
                        print(f"Aadhaar extracted via XML: {uid}")
                        return uid
                    
                    # Try different attribute names
                    for attr in ['aadhaar', 'id', 'number', 'card_number']:
                        uid = root.get(attr)
                        if uid and len(uid) == 12 and uid.isdigit():
                            print(f"Aadhaar extracted via XML attribute {attr}: {uid}")
                            return uid
                            
            except ET.ParseError:
                continue

        # Method 2: Enhanced regex patterns
        enhanced_patterns = [
            r'uid["\s:=]*["\']?(\d{12})["\']?',
            r'aadhaar["\s:=]*["\']?(\d{12})["\']?',
            r'"uid"\s*:\s*"(\d{12})"',
            r'"aadhaar"\s*:\s*"(\d{12})"',
            r'<.*uid\s*=\s*["\'](\d{12})["\']',
            r'(\d{4}[\s-]?\d{4}[\s-]?\d{4})',  # Formatted Aadhaar
            r'\b(\d{12})\b',  # Any 12-digit number
            r'(\d{2}\d{2}\d{2}\d{2}\d{2}\d{2})',  # Continuous 12 digits
        ]
        
        for pattern in enhanced_patterns:
            try:
                matches = re.findall(pattern, qr_data, re.IGNORECASE | re.MULTILINE | re.DOTALL)
                for match in matches:
                    # Clean the match
                    number = re.sub(r'[\s-]', '', str(match))
                    if len(number) == 12 and number.isdigit():
                        # Basic Aadhaar validation
                        if not number.startswith(('0', '1')) and number != '123456789012':
                            print(f"Aadhaar extracted via regex pattern: {number}")
                            return number
            except Exception as e:
                print(f"Pattern {pattern} failed: {e}")
                continue
        
        # Method 3: Extract all number sequences and validate
        all_numbers = re.findall(r'\d+', qr_data)
        for num in all_numbers:
            if len(num) == 12 and not num.startswith(('0', '1')) and num != '123456789012':
                # Additional validation - check if it's not a date/time
                if not (num.startswith('20') and num[2:4] in ['19', '20', '21', '22', '23', '24']):
                    print(f"Aadhaar extracted via number sequence: {num}")
                    return num
        
        # Method 4: Base64 decode attempt (some QR codes are base64 encoded)
        try:
            if len(qr_data) > 100:  # Base64 encoded data is usually longer
                decoded_data = base64.b64decode(qr_data).decode('utf-8')
                return extract_aadhaar_from_qr(decoded_data)  # Recursive call
        except Exception:
            pass
        
        print("No valid Aadhaar number found in QR data")
        print(f"QR data preview: {qr_data[:200]}...")
        return None
        
    except Exception as e:
        print(f"Error extracting Aadhaar: {e}")
        return None

class AadhaarVerifyAPIView(APIView):
    """Enhanced Aadhaar verification with PDF support"""
    
    def post(self, request, *args, **kwargs):
        try:
            if "image" not in request.FILES:
                return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)
            
            uploaded_file = request.FILES["image"]
            file_extension = uploaded_file.name.lower().split('.')[-1] if '.' in uploaded_file.name else ''
            
            images_to_process = []
            
            # Handle different file types
            if file_extension == 'pdf':
                print("Processing PDF file...")
                pdf_images = extract_images_from_pdf(uploaded_file)
                if not pdf_images:
                    return Response({
                        "error": "No images found in PDF or PDF processing failed"
                    }, status=status.HTTP_400_BAD_REQUEST)
                images_to_process = pdf_images
                
            else:
                # Handle image files (PNG, JPG, etc.)
                try:
                    img = Image.open(uploaded_file)
                    # Convert to RGB if necessary
                    if img.mode in ('RGBA', 'LA', 'P'):
                        img = img.convert('RGB')
                    images_to_process = [img]
                except Exception as e:
                    return Response({
                        "error": f"Invalid image file: {str(e)}"
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            print(f"Processing {len(images_to_process)} images...")
            
            # Process each image
            all_results = []
            
            for idx, img in enumerate(images_to_process):
                print(f"Processing image {idx + 1}/{len(images_to_process)} - Size: {img.size}, Mode: {img.mode}")
                
                # QR detection using enhanced method
                qr_codes = decode_qr_enhanced(img)
                
                if qr_codes:
                    # Extract Aadhaar number
                    for qr in qr_codes:
                        qr_data = qr.data.decode("utf-8")
                        aadhaar_number = extract_aadhaar_from_qr(qr_data)
                        
                        if aadhaar_number:
                            # Verify with API Setu
                            verification_result = self.verify_with_api_setu(aadhaar_number)
                            
                            result = {
                                "success": True,
                                "aadhaar_number": aadhaar_number,
                                "source": f"Image {idx + 1}" if len(images_to_process) > 1 else "Image",
                                "file_type": file_extension if file_extension else "image",
                                "verification": verification_result,
                                "qr_data_preview": qr_data[:100] + "..." if len(qr_data) > 100 else qr_data
                            }
                            
                            all_results.append(result)
            
            if all_results:
                return Response({
                    "results": all_results,
                    "total_found": len(all_results),
                    "message": "Aadhaar verification completed successfully"
                })
            
            # No QR codes found in any image
            return Response({
                "error": "No QR code found in any of the processed images",
                "debug_info": {
                    "file_type": file_extension if file_extension else "image",
                    "images_processed": len(images_to_process),
                    "message": "Try uploading a clearer image with a visible QR code"
                }
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                "error": "Unexpected error",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def verify_with_api_setu(self, aadhaar_number):
        """Verify Aadhaar number with API Setu"""
        try:
            # Get token
            token_payload = {
                "grant_type": "client_credentials",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET
            }
            
            token_res = requests.post(AUTH_URL, data=token_payload, timeout=30)
            if token_res.status_code != 200:
                return {
                    "error": "Failed to get access token",
                    "status": "failed",
                    "details": token_res.text
                }
            
            access_token = token_res.json().get("access_token")
            if not access_token:
                return {
                    "error": "Access token missing",
                    "status": "failed"
                }
            
            # Verify Aadhaar
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            verify_payload = {"aadhaar_number": aadhaar_number}
            
            verify_res = requests.post(VERIFY_URL, headers=headers, json=verify_payload, timeout=30)
            
            return {
                "status": "success" if verify_res.status_code == 200 else "failed",
                "response_code": verify_res.status_code,
                "result": verify_res.json() if verify_res.status_code == 200 else verify_res.text
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "error": "API verification failed",
                "status": "failed",
                "details": str(e)
            }