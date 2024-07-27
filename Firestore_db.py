import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter,Or


from typing import List, Dict


cred = credentials.Certificate(r"C:\\Coding_file\\visual_code\\project_Cosmeme\\cosmeme-db-firebase-adminsdk-oz9lg-9d7cb26949.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# def add_skin_status():  
#     data = {
#         'Skin status' : res()
#     }
#     doc_ref = db.collection('Current of skin status').document()
#     doc_ref.set(data)
    #print(doc_ref.id)

def add_prod(name_collection : str,Category : str, Prod_Name : str, Brand : str, price : str, Use_for : str, h_ingre : str, Skincare_Concerns : List[str], Skin_Type : List[str]) -> Dict:
    data = {
        "Category" : Category,
        "Product_Name" : Prod_Name,
        "Brand" : Brand,    
        "Price" : price,
        "Use_for" : Use_for,
        "Highlighted_Ingredients" : h_ingre,
        "Skincare_Concerns" : Skincare_Concerns,
        "Skin_Type" : Skin_Type
    }
    doc_ref = db.collection(name_collection).document()
    doc_ref.set(data)
    print(doc_ref.id)


# add_prod("Treatments",
#          "Facial Peels",
#          "Watermelon Glow AHA Night Treatment",
#          "Glow Recipe",
#          "$40.00",
#          " A powerful overnight resurfacing mask to gently exfoliate, hydrate, and visibly brighten with a 2.5 percent pH-balanced AHA complex for smoother, firmer-looking skin.",
#          '''- pH-Balanced AHA Complex 2.5%: As efficacious as 10 percent glycolic acid to exfoliate while maintaining the skin barrier.
#             - Seven Weights of Hyaluronic Acid: Intensely hydrate skin layer by layer for plump-, bouncy-looking skin.
#             - Niacinamide and Quinoa Peptide: Minimizes the look of discoloration while visibly firming and brightening.''',
#          ["pores" , "acne", "blemishes",'blackheads'],
#          ["normal", "combination", "dry", "oily"]
#         )

# add_prod("Moisturizers",
#          "Face Oils",
#          "C.E.O Glow Vitamin C + Turmeric Face Oil",
#          "Sunday Riley",
#          "$80.00",
#          "An instantly absorbing face oil infused with advanced vitamin C (THD ascorbate), turmeric, and evening primrose oil, to brighten, hydrate, and leave skin glowing.",
#          "- Meadowfoam, Hemp, Sunflower, Cranberry, Olive, Broccoli, and Grapeseed Oils: Infuse skin with intense, soothing moisture.\n - Blackcurrant, Tsubaki, Sacha Inchi, and Sea Buckthorn Oils: Replenish, visibly plump, and reduce the look of fine lines.\n - Prickly Pear, Cucumber, Rosehip, Watermelon, and Pomegranate Oils: Support a strong skin barrier and protect against free-radical damage.\n",
#          ["Dryness", "Dullness","Loss of Firmness","Elasticity"],
#          ["Normal", "Dry", "Combination",  "Oily"])

# add_prod("Treatments",
#          "Facial Peels",
#          "AHA 30% + BHA 2 Exfoliating Peeling Solution",
#          "The Ordinary",
#          "$9.50",
#          "An exfoliating solution to help fight visible blemishes and improve the look of skin texture and radiance.",
#          '''- Glycolic Acid: Exfoliates the outer layers of skin.\n
#             - Lactic Acid: Exfoliates the outer layers of skin.\n
#             - Salicylic Acid: Exfoliates inside the pores to reduce congestion.''',
#          ["Dullness", "Uneven Texture",  "Acne", "Blemishes"],
#          ["Normal", "Combination",  "Oily","all-type"]
#         )


def queries(collections : str,user_stutus : List[str]):

    docs = db.collection(collections).where(filter=FieldFilter("Skin_Type", "array_contains_any", user_stutus)).get()

    docs1 = db.collection(collections).where(filter=FieldFilter("Skincare_Concerns", "array_contains_any", user_stutus)).get()

    docs2 = db.collection(collections).where(filter=FieldFilter("Skin_Type", "array_contains_any", ["all-type"])).get()
    

    def print_out(docs: list):

        print("***Types of products***", collections)
        cnt = 0
        for doc in docs:
            cnt += 1
            doc_dict = doc.to_dict()
            print(f"{cnt}/")
            print("Category:", doc_dict.get("Category"))
            print("Product_Name:", doc_dict.get("Product_Name"))
            print("Brand:", doc_dict.get("Brand"))
            print("Price:", doc_dict.get("Price"))
            print("Use for:", doc_dict.get("Use_for"))
            print("Highlighted Ingredients: \n", doc_dict.get("Highlighted_Ingredients"))
            print("Skincare Concerns:", doc_dict.get("Skincare_Concerns"))
            print("Skin Type:", doc_dict.get("Skin_Type"), "\n")
        
    # print(len(docs),len(docs1),len(docs2))    
    if len(docs) != 0 : 
        return docs
        print_out(docs)
    elif len(docs1) != 0: 
        return docs1
        print_out(docs1)
    else: 
        return docs2
        print_out(docs2)
    


collection_ref = ["Moisturizers","Cleansers","Treatments"]

arr = ['Dry']

# for i in collection_ref:
#     print("-" * 15)
#     queries(i,arr)
    





