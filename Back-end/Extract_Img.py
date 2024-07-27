import google.generativeai as genai
from PIL import Image
import base64 
import io 
from Firestore_db import queries

genai.configure(api_key="AIzaSyB9vOzZnbiRr5E25izsU2BxLm0Q9Mk6hV8")

collection_ref = ["Moisturizers","Cleansers","Treatments"]

def Read_Img(file_name : str):
    img = Image.open(file_name)
    byte_array = io.BytesIO()
    img.save(byte_array,format=img.format)
    byte_array = byte_array.getvalue()
    encoded_img_data = base64.b64encode(byte_array)

    img_blob = {
        "mime_type" : "image/jpeg",
        "data" : encoded_img_data.decode('utf-8')
    }
    
    model = genai.GenerativeModel('gemini-pro-vision')
    prompt = "give me a skin status of this picture by english language"
    response = model.generate_content([prompt, {"inline_data" : img_blob}],stream=True)
    response.resolve()

    model1 = genai.GenerativeModel("gemini-1.5-flash")
    prompt1 = "Give me a the words for skin conditions in the text above and show the ouput in one line \n " + response.text
    response1 = model1.generate_content(prompt1,stream=True)
    response1.resolve()
    result = response1.text.replace("\n","").split(", ")
    print(result)
    for i in collection_ref:
        print("-" * 15)
        queries(i,result)


def Extract_Img(image):
    img = Image.fromarray(image)
    byte_array = io.BytesIO()
    img.save(byte_array,format="JPEG")
    byte_array = byte_array.getvalue()
    encoded_img_data = base64.b64encode(byte_array)

    img_blob = {
        "mime_type" : "image/jpeg",
        "data" : encoded_img_data.decode('utf-8')
    }
    
    model = genai.GenerativeModel('gemini-pro-vision')
    prompt = "give me a skin status of this picture by english language"
    response = model.generate_content([prompt, {"inline_data" : img_blob}],stream=True)
    response.resolve()
    

    model1 = genai.GenerativeModel("gemini-1.5-flash")
    prompt1 = "Give me a the words for skin conditions in the text above and show the ouput in one line \n " + response.text
    response1 = model1.generate_content(prompt1,stream=True)
    response1.resolve()
    result = response1.text.replace("\n","").split(", ")
    return result
    # print(result)
    # for i in collection_ref:
    #     print("-" * 15)
    #     queries(i, result)