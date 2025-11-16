from flet import *

class ProductDetailView(Container):
    def __init__(self, page: Page):
        super().__init__(expand=True, padding=20)
        self.page = page
        
        self.product_image = Image(
            src="", width=250, height=250, fit=ImageFit.COVER,
            border_radius=border_radius.all(15)
        )
        self.product_name = Text("", size=24, weight=FontWeight.BOLD, color="white")
        self.product_brand = Text("", size=18, italic=True, color="white54")
        self.product_price = Text("", size=16, color="white")
        self.product_description = Text("", color="white")
        self.product_ingredients = Text("", color="white")
        self.product_skin_types = Text("", color="white")
        self.product_concerns = Text("", color="white")

        self.content = Column(
            controls=[
                self.product_image,
                self.product_name,
                self.product_brand,
                Divider(),
                self.product_price,
                Divider(),
                Text("Description", weight=FontWeight.BOLD, size=16, color="white"),
                self.product_description,
                Divider(),
                Text("Highlighted Ingredients", weight=FontWeight.BOLD, size=16, color="white"),
                self.product_ingredients,
                Divider(),
                Text("Good for Skin Types:", weight=FontWeight.BOLD, size=16, color="white"),
                self.product_skin_types,
                Divider(),
                Text("Addresses Concerns:", weight=FontWeight.BOLD, size=16, color="white"),
                self.product_concerns,
            ],
            spacing=10,
            scroll=ScrollMode.AUTO 
        )
    
    def update_product_data(self, product_data: dict):
        if not product_data:
            self.product_name.value = "Product Not Found"
            return
        self.product_image.src = product_data.get("Image_URL", "https://picsum.photos/200/200?0")
        self.product_name.value = product_data.get("Product_Name", "N/A")
        self.product_brand.value = product_data.get("Brand", "N/A")
        self.product_price.value = f"Price: {product_data.get('Price', 'N/A')}"
        self.product_description.value = product_data.get("Use_for", "No description available.")
        self.product_ingredients.value = product_data.get("Highlighted_Ingredients", "N/A")
        
        self.product_skin_types.value = ", ".join(product_data.get("Skin_Type", []))
        self.product_concerns.value = ", ".join(product_data.get("Skincare_Concerns", []))

