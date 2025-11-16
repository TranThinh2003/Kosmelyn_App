from flet import *
import numpy as np
from PIL import Image as PILImage

from Extract_Img import Extract_Img
from Firestore_db import queries, save_user_analysis, get_product_data
from question import question

from views.camera_view import CameraView
from views.quiz_view import QuestionView
from views.prod_detail_view import ProductDetailView
from views.filter_view import FilterView

def main(page: Page):
    page.title = "Skincare Analysis Demo"
    page.padding = 0 
    page.bgcolor = "#041955"

    question_index = 0
    answers = {}
    all_query_results = []

    box_items = ListView(expand=True, spacing=10, padding=10, auto_scroll=True)
    loading_status_text = Text("Starting analysis...", color="black", size=14, italic=True)
    loading_ring = ProgressRing(width=32, height=32, stroke_width=4)
    loading_container = Container(
        content=Column(
            [loading_ring, Container(height=20), loading_status_text],
            horizontal_alignment=CrossAxisAlignment.CENTER,
            alignment=MainAxisAlignment.CENTER
        ),
        alignment=alignment.center, expand=True, visible=False
    )


    def reset_state():
        nonlocal question_index, answers
        question_index = 0
        answers = {}
        box_items.controls.clear()
        if hasattr(camera_view_instance, 'stop_camera_logic'):
            camera_view_instance.stop_camera_logic()
        if hasattr(question_view_instance, 'view_will_appear'):
            question_view_instance.question_index = 0
            question_view_instance.answers = {}
        print("State has been reset.")


    def update_prodList_ui(prod_list):
        box_items.controls.clear()

        if not prod_list:
            box_items.controls.append(Text("No products match the selected filter.", color="black54", text_align="center"))
        else:
            for prod in prod_list:
                product_card = Container(
                    on_click=lambda e, col=prod['collection'], doc_id=prod['id']: page.go(f"/product/{col}/{doc_id}"),
                    content=Row(
                        controls=[
                            Image(src=prod.get("Image_URL", "https://picsum.photos/200/200?0"), width=80, height=80, fit=ImageFit.COVER, border_radius=border_radius.all(10)),
                            Column(
                                controls=[
                                    Text(prod.get('Product_Name', 'N/A'), size=14, weight="bold", color="black"),
                                    Text(prod.get("collection", 'N/A'), size=12, color="black54"),
                                    Text(prod.get('Brand', 'N/A'), size=12, color="black54"),
                                    Text(prod.get('Price', 'N/A'), size=12, color="black54"),
                                    Text(", ".join(prod.get('Skin_Type', []) if isinstance(prod.get('Skin_Type'), list) else []), size=12, color="black54")                                ],
                                alignment=MainAxisAlignment.CENTER, expand=True, spacing=5
                            ),
                        ],
                        vertical_alignment=CrossAxisAlignment.CENTER,
                    ),
                    height=150, bgcolor="white", padding=10, border_radius=15,                )
                box_items.controls.append(product_card)
        page.update()
    

    filter_view_instance = FilterView(update_prodList_ui)

    def build_and_show_results(user_status: list = None, user_answers: dict = None):
        nonlocal all_query_results

        box_items.controls.clear()
        loading_status_text.value = "Finding suitable products..."
        page.update()
        
        all_query_results = []

        collection_ref = ["Moisturizers", "Cleansers", "Treatments"]
        all_results_for_saving = []

        for ref in collection_ref:
            query_docs = queries(ref, user_status=user_status, user_answers=user_answers)
            for doc in query_docs:
                doc_dict = doc.to_dict()
                
                doc_dict['id'] = doc.id
                doc_dict['collection'] = ref
                all_query_results.append(doc_dict)

                all_results_for_saving.append(doc_dict)
                product_card = Container(
                    on_click=lambda e, col=ref, doc_id=doc.id: page.go(f"/product/{col}/{doc_id}"),
                    content=Row(
                        controls=[
                            Image(src=doc_dict.get("Image_URL", "https://picsum.photos/200/200?0"), width=80, height=80, fit=ImageFit.COVER, border_radius=border_radius.all(10)),
                            Column(
                                controls=[
                                    Text(doc_dict.get('Product_Name', 'N/A'), size=14, weight="bold", color="black"),
                                    Text(doc_dict.get("collection", 'N/A'), size=12, color="black54"),
                                    Text(doc_dict.get('Brand', 'N/A'), size=12, color="black54"),
                                    Text(doc_dict.get('Price', 'N/A'), size=12, color="black54"),
                                    Text(", ".join(doc_dict.get('Skin_Type', []) if isinstance(doc_dict.get('Skin_Type'), list) else []), size=12, color="black54")
                                ],
                                alignment=MainAxisAlignment.CENTER, expand=True, spacing=5
                            ),
                        ],
                        vertical_alignment=CrossAxisAlignment.CENTER,
                    ),
                    height=150, bgcolor="white", padding=10, border_radius=15                )
                box_items.controls.append(product_card)
        
        filter_view_instance.update_data_and_options(all_query_results)
        initial_result = filter_view_instance.apply_filters()
        update_prodList_ui(initial_result)
        if not box_items.controls:
            box_items.controls.append(Text("No suitable products found.", color="white", text_align="center"))
        loading_container.visible = False
        page.update()

    def process_image(e: FilePickerResultEvent):
        if not e.files: return
        loading_status_text.value = "Analyzing your skin..."
        loading_container.visible = True
        page.go("/results")

        img_path = e.files[0].path
        img = PILImage.open(img_path)
        skin_status_from_img = Extract_Img(np.array(img))
        
        if not skin_status_from_img:
            page.snack_bar = SnackBar(content=Text("Unable to analyze skin condition."), bgcolor="red")
            page.snack_bar.open = True
            page.go("/")
            return
        build_and_show_results(user_status=skin_status_from_img)



    file_picker = FilePicker(on_result=process_image)
    page.overlay.append(file_picker)
    page_main = Container(
        alignment=alignment.center,
        content=Column(
            controls=[
                Text("Skincare Analysis", size=28, weight="bold", color="black"),
                Text("Get personalized skincare recommendations", size=16, color="black"),
                Container(height=20),
                ElevatedButton("Analyze with Camera", icon=Icons.CAMERA_ENHANCE, on_click=lambda _: (reset_state(), page.go("/camera")), height=50),
                ElevatedButton("Upload Face Photo", icon=Icons.UPLOAD_FILE, on_click=lambda _: (reset_state(), file_picker.pick_files(allow_multiple=False, allowed_extensions=["jpg", "png"])), height=50),
                ElevatedButton("Answer a Quick Quiz", icon=Icons.QUESTION_ANSWER, on_click=lambda _: (reset_state(), page.go("/quiz")), height=50),
                Container(height=20),
                Text("Disclaimer: This is a demo application. For accurate skin analysis, please consult a dermatologist.", size=12, color="black54", text_align="center")
            ],
            horizontal_alignment=CrossAxisAlignment.CENTER, spacing=15
        )
    )



    page_results = Container(                          
        padding=10, expand=True,
        content=Column(
            expand=True,
            controls=[
                filter_view_instance,
                Stack(controls=[box_items, loading_container], expand=True)
            ]
        )
    )
    

    camera_view_instance = CameraView(page, Extract_Img,build_and_show_results, loading_container, loading_status_text) 
    question_view_instance = QuestionView(page, question, build_and_show_results, loading_container, loading_status_text)
    product_detail_view_instance = ProductDetailView(page)
    


    def route_change(route):
        page.views.clear()
        page.views.append(View("/", [page_main], padding=20))
        
        if page.route == "/quiz":
            question_view_instance.view_will_appear()
            page.views.append(
                            View(
                                "/quiz",
                                [question_view_instance],
                                appbar=AppBar(
                                            leading=IconButton(Icons.ARROW_BACK, on_click=lambda _: page.go("/")),
                                            title=Text("Skincare Quiz"),
                                            ),
                            padding=20,
                            bgcolor="#041955"
                            )
                        ) 
        elif page.route == "/camera":
            camera_view_instance.view_will_appear()
            page.views.append(
                            View(
                                "/camera",
                                [camera_view_instance],
                                appbar=AppBar(
                                            leading=IconButton(Icons.ARROW_BACK, on_click=lambda _: page.go("/")),
                                            title=Text("Camera Analysis"),
                                            ),
                            padding=20,
                            bgcolor="#041955"
                            )
                        )                
        elif page.route == "/results":

            page.views.append(View("/results", [
                AppBar(title=Text("Results"), leading=IconButton(Icons.ARROW_BACK, on_click=lambda _: page.go("/"))),
                page_results
            ]))
        elif page.route.startswith("/product/"):
            parts = page.route.split("/")
            if len(parts) == 4:
                collection, doc_id = parts[2], parts[3]
                product_data = get_product_data(collection, doc_id)
                product_detail_view_instance.update_product_data(product_data)

                page.views.append(
                    View(
                        page.route,
                        [
                            AppBar(
                                title=Text("Product Details"),
                                leading=IconButton(Icons.ARROW_BACK, on_click=lambda _: page.go("/results"))
                            ),
                            product_detail_view_instance
                        ],
                        padding=20,
                        bgcolor="#041955"
                    )
                )
        page.update()
    
    def view_pop(view):

        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


if __name__ == "__main__":
    app(target=main,assets_dir="assets")
    