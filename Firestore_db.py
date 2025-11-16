import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter
import os
from dotenv import load_dotenv
from typing import List, Dict
import cloudinary
import cloudinary.uploader
load_dotenv()


cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
if not cred_path:
    raise ValueError("FIREBASE_CREDENTIALS_PATH not found in .env file")
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
db = firestore.client()

cloudinary_cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
cloudinary_api_key = os.getenv("CLOUDINARY_API_KEY")
cloudinary_api_secret = os.getenv("CLOUDINARY_API_SECRET")

if not all([cloudinary_cloud_name, cloudinary_api_key, cloudinary_api_secret]):
    raise ValueError("Missing Cloudinary configuration in environment variables.")

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)



def add_prod(   
        name_collection: str, 
        Category: str, 
        Prod_Name: str, 
        Brand: str, 
        price: str, 
        Use_for: str, 
        h_ingre: str, 
        Skincare_Concerns: List[str], 
        Skin_Type: List[str], 
        local_image_path: str = None,
        Safe_For_All: bool = False
            ) -> str:

    required_string_fields = {
        "name_collection": name_collection,
        "Category": Category,
        "Prod_Name": Prod_Name,
        "Brand": Brand,
        "Use_for": Use_for,
        "h_ingre": h_ingre
    }
    for field_name, value in required_string_fields.items():
        if not value or not isinstance(value, str):
            raise ValueError(f"{field_name} must be a non-empty string.")

    if not isinstance(Skincare_Concerns, list) or not Skincare_Concerns:
        raise ValueError("Skincare_Concerns must be a non-empty list.")

    if not isinstance(Skin_Type, list) or not Skin_Type:
        raise ValueError("Skin_Type must be a non-empty list.")

    try:
        price_value = float(price)
        if price_value < 0:
            raise ValueError("Price must be a non-negative number.")
    except ValueError:
        raise ValueError("Price must be a valid number.")

    uploaded_image_url = None

    if local_image_path:
        try:
            print(f"Uploading image from: {local_image_path} to Cloudinary...")
            upload_result = cloudinary.uploader.upload(
                local_image_path, 
                folder=f"skincare_app/{name_collection}"
            )
            uploaded_image_url = upload_result.get("secure_url")
            print(f"Successfully uploaded. Image URL: {uploaded_image_url}")
        except Exception as e:
            print(f"Error uploading image to Cloudinary: {e}")

    data = {
        "Category": Category,
        "Product_Name": Prod_Name,
        "Brand": Brand,
        "Price": price,
        "Use_for": Use_for,
        "Highlighted_Ingredients": h_ingre,
        "Skincare_Concerns": Skincare_Concerns,
        "Skin_Type": Skin_Type,
        "Image_URL": uploaded_image_url,
        "Safe_For_All": Safe_For_All
    }
    
    doc_ref = db.collection(name_collection).document()
    doc_ref.set(data)
    print(f"Product data saved to Firestore with ID: {doc_ref.id}")
    return doc_ref.id


def save_user_analysis(user_id: str, skin_status: List[str], recommended_products: List[Dict]) -> str:
    try:
        data = {
            "user_id": user_id,
            "skin_status": skin_status,
            "recommended_products": recommended_products,
            "timestamp": firestore.SERVER_TIMESTAMP
        }
        doc_ref = db.collection("User_Analysis").document()
        doc_ref.set(data)
        print(f"Saved user analysis with ID: {doc_ref.id}")
        return doc_ref.id
    except Exception as e:
        print(f"Error saving user analysis: {e}")
        raise

ALL_CONCERNS = {
    "Acne", "Dryness", "Dullness", "Redness", "Oily", "Wrinkles", 
    "Large Pores", "Blackheads", "Dehydration", "Dark Spots"
}
ALL_SKIN_TYPES = {"Oily", "Dry", "Combination", "Normal"}


def queries(collections: str, user_status: List[str] = None, user_answers: Dict[str, str] = None,limit: int = 50) -> List:
    final_docs = []

    if user_status and user_status != [None]:
        concerns_from_user = [c for c in user_status if c in ALL_CONCERNS]
        types_from_user = [t for t in user_status if t in ALL_SKIN_TYPES]
        
        print(f"Querying for Concerns: {concerns_from_user}, Skin Types: {types_from_user}")

        if concerns_from_user:
            query = db.collection(collections).where(
                filter=FieldFilter("Skincare_Concerns", "array_contains_any", concerns_from_user)
            ).limit(limit)
            docs = query.get()

            types_from_user_set = set(types_from_user)
            for doc in docs:
                doc_dict = doc.to_dict()
                skin_types_in_doc_set = set(doc_dict.get("Skin_Type", []))
                
                if not types_from_user_set or not skin_types_in_doc_set.isdisjoint(types_from_user_set):
                    final_docs.append(doc)
    
    elif user_answers and user_answers.get("skin_type"):
        skin_type = user_answers.get("skin_type")
        concerns_to_check = {"Dryness", "Dullness"}
        query = db.collection(collections).where(
            filter=FieldFilter("Skin_Type", "array_contains_any", [skin_type])
        ).limit(limit)
        docs = query.get()
        for doc in docs:
            doc_dict = doc.to_dict()
            concerns_in_doc = set(doc_dict.get("Skincare_Concerns", []))
            if not concerns_in_doc.isdisjoint(concerns_to_check):
                final_docs.append(doc)
    
    else:
        query = db.collection(collections).where(filter=FieldFilter("Safe_For_All", "==", True)).limit(limit)
        final_docs = list(query.get())

    if not final_docs and user_status:
        print(f"No specific products found in '{collections}', falling back to 'Safe_For_All' products.")
        query = db.collection(collections).where(filter=FieldFilter("Safe_For_All", "==", True)).limit(limit)
        final_docs = list(query.get())
    
    return final_docs

def get_item_by_id(collection: str, doc_id: str):
    try:
        doc_ref = db.collection(collection).document(doc_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            print(f"No document found with ID: {doc_id} in collection: {collection}")
            return None
    except Exception as e:
        print(f"Error retrieving document: {e}")
        return None

def delete_all_user_data(confirm: bool = False):
    if not confirm:
        raise ValueError("Must explicitly confirm deletion with confirm=True to proceed.")
    try:
        users_ref = db.collection("User_Analysis")
        batch = db.batch()
        docs = users_ref.stream()
        cnt = 0
        for doc in docs:
            batch.delete(doc.reference)
            cnt += 1
            if cnt == 500:
                batch.commit()
                batch = db.batch()
                cnt = 0
        if cnt % 500 != 0:
            batch.commit()
        print(f'Delete {cnt} users analysis data successfully.')
    except Exception as e:
        print(f"Error deleting user data: {e}")
        raise

# def delete_all_products(): # in firestore
#     collections = ["Moisturizers", "Cleansers", "Treatments"]
#     for collection in collections:
#         coll_ref = db.collection(collection)
#         docs = coll_ref.stream()
#         for doc in docs:
#             doc.reference.delete()
#         print(f"All products deleted from {collection} collection.")

# def delete_all_images(): # in cloudinary
#     try:
#         result = cloudinary.api.delete_resources_by_prefix("skincare_app")
#         print(f"Deleted images from Cloudinary: {result}")
#     except Exception as e:
#         print(f"Error deleting images from Cloudinary: {e}")


def get_product_data(collection: str, doc_id: str, default = None) -> Dict:
    try:
        doc_ref = db.collection(collection).document(doc_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            print(f"No document found with ID: {doc_id} in collection: {collection}")
            return default
    except Exception as e:
        print(f"Error retrieving document: {e}")
        return default

