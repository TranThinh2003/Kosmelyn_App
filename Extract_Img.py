import google.generativeai as genai
from PIL import Image
import base64
import io
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")
genai.configure(api_key=api_key)

VALID_KEYWORDS = [
    "Acne", "Dryness", "Dullness", "Redness", "Oily", "Wrinkles", 
    "Large Pores", "Blackheads", "Dehydration", "Dark Spots",
    "Normal", "Combination"
]

def Extract_Img(image_array):
    try:
        img = Image.fromarray(image_array)
        img = img.resize((640, 480))
        byte_array = io.BytesIO()
        img.save(byte_array, format="JPEG", quality=85)
        byte_array = byte_array.getvalue()
        
        img_blob = {
            "mime_type": "image/jpeg",
            "data": base64.b64encode(byte_array).decode('utf-8')
        }
        
        valid_keywords_string = ", ".join(VALID_KEYWORDS)
        
        prompt = f"""
        You are an expert dermatology analysis assistant. Your task is to analyze the provided image of a person's skin and identify all relevant conditions.

        You MUST choose from the following list of valid keywords only: {valid_keywords_string}

        Based on the image, list all the keywords that apply. Your output MUST be ONLY a comma-separated list of the chosen keywords. Do not add any explanation, introduction, or other text.

        Example output: Acne, Oily, Redness
        """

        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content([prompt, img_blob],request_options={"timeout":30})
        
        if not response or not hasattr(response, 'text') or not response.text:
            print("Gemini API failed to return keywords.")
            return None
        raw_keywords = response.text.strip().split(',')
        result = [keyword.strip() for keyword in raw_keywords if keyword.strip() in VALID_KEYWORDS]
        
        print(f"Gemini Analysis Result (Constrained): {result}")
        return result if result else None
    
        
    except Exception as e:
        print(f"An error occurred during image extraction: {e}")
        return None
    

        