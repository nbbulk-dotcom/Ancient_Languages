import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'fullstack_translator', 'ancient_translator_backend', 'app'))

from specialized_ocr import (
    ocr_linear_a_subroutine,
    ocr_khitan_large_subroutine,
    ocr_proto_elamite_subroutine,
    ocr_indus_valley_subroutine,
    enhanced_image_preprocessing
)
import json
from utils.saver import save_json, save_image
from utils.logger import log_event

class GlyphOCRProcessor:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def process_image(self, image_data, script_type, image_name):
        """Process an ancient script image and extract glyphs"""
        
        ocr_functions = {
            'linear_a': ocr_linear_a_subroutine,
            'khitan': ocr_khitan_large_subroutine,
            'proto_elamite': ocr_proto_elamite_subroutine,
            'indus_valley': ocr_indus_valley_subroutine
        }
        
        if script_type not in ocr_functions:
            raise ValueError(f"Unsupported script type: {script_type}")
        
        try:
            extracted_text, processed_image = ocr_functions[script_type](image_data)
            
            processed_image_path = os.path.join(self.output_dir, f"{image_name}_processed.png")
            save_image(processed_image.tobytes(), processed_image_path)
            
            result = {
                "script_type": script_type,
                "image_name": image_name,
                "extracted_text": extracted_text,
                "processed_image_path": processed_image_path,
                "symbols_extracted": self._extract_symbols(extracted_text, script_type)
            }
            
            result_path = os.path.join(self.output_dir, f"{image_name}_ocr_result.json")
            save_json(result, result_path)
            
            log_event(f"OCR processing complete for {image_name} ({script_type})", 
                     os.path.join(self.output_dir, "ocr_log.txt"))
            
            return result
            
        except Exception as e:
            log_event(f"OCR processing failed for {image_name}: {str(e)}", 
                     os.path.join(self.output_dir, "ocr_log.txt"))
            raise
    
    def _extract_symbols(self, text, script_type):
        """Extract individual symbols from OCR text"""
        symbols = []
        
        if script_type == 'linear_a':
            symbols = [char for char in text if '\u10600' <= char <= '\u1077F']
        elif script_type == 'khitan':
            symbols = [char for char in text if '\U00018B00' <= char <= '\U00018CFF']
        elif script_type == 'proto_elamite':
            symbols = [char for char in text if '\u12000' <= char <= '\u123FF']
        elif script_type == 'indus_valley':
            symbols = text.split()
        
        return symbols
    
    def batch_process_images(self, image_directory, script_type):
        """Process all images in a directory"""
        results = []
        
        for filename in os.listdir(image_directory):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
                image_path = os.path.join(image_directory, filename)
                
                with open(image_path, 'rb') as f:
                    image_data = f.read()
                
                try:
                    result = self.process_image(image_data, script_type, filename)
                    results.append(result)
                except Exception as e:
                    log_event(f"Failed to process {filename}: {str(e)}", 
                             os.path.join(self.output_dir, "ocr_log.txt"))
        
        batch_result_path = os.path.join(self.output_dir, f"batch_ocr_results_{script_type}.json")
        save_json(results, batch_result_path)
        
        return results
