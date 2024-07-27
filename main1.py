import flet as ft
from flet import *
from flet_core import RoundedRectangleBorder, BorderSide
import cv2
import time
import os
from typing import Dict
from question import qt
from Extract_Img import Extract_Img
from Firestore_db import queries
# from flet.margin import Margin
def main(page: Page):
    question_index = 0
    answers = []
    genai = ""
    box_items = Column( height = 600, width= 360, scroll ="auto",alignment="center" ,horizontal_alignment="center",)
    button_ = ElevatedButton(text="Show Item", on_click=lambda e: page.go("/Items"), width=200, height=70)
    def load_question(index):
        """Load the question and options based on the current index."""
        # button.visible = False
        question_data = qt[index]
        question_label.value = question_data["question"]
        question_label.color = "white"
        for i, option in enumerate(option_buttons):
            if i < len(question_data["options"]):
                option.text = question_data["options"][i]
                option.visible = True
            else:
                option.visible = False
        page.update()
    def check_answer(e):
        nonlocal question_index
        selected_option = e.control.text
        answers.append(selected_option)
        question_index += 1
        if question_index < len(qt):
            load_question(question_index)
        else:
            feedback_label.value = "Quiz finished! Here are your skincare tips:"
            provide_advice()
            for option in option_buttons:
                option.visible = False
            button_.visible = True
        page.update()
    def provide_advice():
        """Provide skincare advice based on the user's answers."""
        advice = ""
        skin_problem = answers[0]
        if skin_problem == "Dry":
            advice += "\n- Use moisturizing products with hyaluronic acid."
        elif skin_problem == "Oily":
            advice += "\n- Use oil-free and non-comedogenic products."
        elif skin_problem == "Acne-prone":
            advice += "\n- Consider products with salicylic acid or benzoyl peroxide."
        elif skin_problem == "Sensitive":
            advice += "\n- Use gentle and fragrance-free products."

        sunscreen_usage = answers[1]
        if sunscreen_usage == "Yes":
            advice += "\n- Good job! Sunscreen helps protect your skin from harmful UV rays."
        elif sunscreen_usage == "No":
            advice += "\n- Consider using sunscreen daily to protect your skin from UV damage."

        makeup_removal = answers[2]
        if makeup_removal == "Yes":
            advice += "\n- Great! Removing makeup before bed helps prevent breakouts."
        elif makeup_removal == "No":
            advice += "\n- Make sure to remove makeup before bed to keep your skin clean."

        moisturizing_frequency = answers[3]
        if moisturizing_frequency == "Once":
            advice += "\n- Consider moisturizing twice a day to keep your skin hydrated."
        elif moisturizing_frequency == "Twice":
            advice += "\n- Excellent! Keep up the good work."
        elif moisturizing_frequency == "Never":
            advice += "\n- Moisturizing is important for maintaining healthy skin."

        feedback_label.value += advice
        page.update()
    question_label = Text()
    feedback_label = Text()
    feedback_label.color = "#FFFFFF"
    option_buttons = [ElevatedButton(text="", on_click=check_answer) for _ in range(4)]


    # def btr_quizz():

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
   
    # Pick files 
    
    def upload_files(e):
        upload_list = []
        if file_picker.result is not None and file_picker.result.files is not None:
            for f in file_picker.result.files:
                upload_list.append(
                    FilePickerUploadFile(
                        f.name,
                        upload_url=page.get_upload_url(f.name, 600),
                    )
                )
            file_picker.upload(upload_list)

    def file_picker_result(e: FilePickerResultEvent):
        upload_button.disabled = True if e.files is None else False
        page.update()

    file_picker = FilePicker(on_result=file_picker_result)
    upload_button = ElevatedButton("Upload",color = "#FFFFFF",  on_click=upload_files, disabled=True, visible = True)
    def removeallyouphoto():
        folder_path = "photo/"
        files = os.listdir(folder_path)
        for file in files:
            file_path = os.path.join(folder_path,file)
			# AND IF FOUND THEN REMOVE
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"YOU FILE SUUCESS REMOVE {file_path}")

        page.update()
       



    def capture_image(frame):
        timestamp = str(int(time.time()))
        myfileface = f"myFaceFile_{timestamp}.jpg"
        cv2.imwrite(f"photo/{myfileface}", frame)
        cv2.putText(frame, "YOU SUCCESSFULLY CAPTURED!", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow("Webcam", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        folder_path = "photo/"
        myimage.src = folder_path + myfileface
        page.update()
		
    def takemepicture(e):
        removeallyouphoto()
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        cv2.namedWindow("Webcam", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Webcam", 400, 400)

        timestamp = str(int(time.time()))
        myfileface = f"myFaceFile_{timestamp}.jpg"
        try:
            while True:
                ret, frame = cap.read()
                cv2.imshow("Webcam", frame)
                myimage.src = ""
                page.update()
                key = cv2.waitKey(1)
                if key == ord("q"):
                    break
                elif key == ord("s"):
                    capture_image(frame)
                    break

            cap.release()
            cv2.destroyAllWindows()
            page.update()

        except Exception as e:
            print(e)
            print("ERROR OCCURRED!")
    

    # click button to take a picture
    # box_items = Column( height = 550, width= 360, scroll ="auto",alignment="center" ,horizontal_alignment="center",)
    def capture_image_button(e):
        nonlocal genai, box_items
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        ret, frame = cap.read()
        genai = Extract_Img(frame)
        capture_image(frame)
        print(genai)
        collection_ref = ["Moisturizers","Cleansers","Treatments"]
        for ref in collection_ref:
            query = queries(ref, genai)
            for doc in query:
                doc_dict = doc.to_dict()
                box_items.controls.append(
                    Container(
                        content=Row(
                            controls=[
                                Image(
                                    src=f"https://picsum.photos/200/200?0",
                                    width=150,
                                    height=150,
                                    fit=ImageFit.NONE,
                                    repeat=ImageRepeat.NO_REPEAT,
                                    border_radius=border_radius.all(10),
                                ),
                                Column(
                                    controls=[
                                        Text(f"Category: {doc_dict.get('Category')}"),
                                        Text(f"Product Name: {doc_dict.get('Product_Name')}"),
                                        Text(f"Brand: {doc_dict.get('Brand')}"),
                                        Text(f"Price: {doc_dict.get('Price')}"),
                                        Text(f"Use for: {doc_dict.get('Use_for')}"),
                                        Text(f"Higlighted Ingredients: {doc_dict.get('Highlighted_Ingredients')}"),
                                        Text(f"Skincare Concerns: {doc_dict.get('Skincare_Concerns')}"),
                                        Text(f"Skin type: {doc_dict.get('Skin_Type')}")
                                    ],
                                    alignment=MainAxisAlignment.CENTER,
                                    expand=True,
                                ),
                            ],
                            alignment=MainAxisAlignment.START,
                            vertical_alignment=CrossAxisAlignment.CENTER,
                        ),
                        height=200,
                        width=400,  # Adjust width as necessary
                        bgcolor="white",
                        padding =15,
                        border_radius=35
                    )
                )
        cap.release()
        cv2.destroyAllWindows()
        page.update()
    
    def hidenev(e):
        sidemenu.offset = transform.Offset(-5,0)
        page.update()
    def shownav(e):
        sidemenu.offset = transform.Offset(0,0)
        page.update()


    # cam of pagecam ==========================================================
    myimage = Image(
        src=False,
        width=400,
        height=400,
        fit="cover",
        border_radius=border_radius.all(10)
    )
    folder_path = "photo/"
    

    
    sidemenu = Container(
                content=Column([
            Container(
                content=Text("Home", size=20), on_click=lambda e: page.go("/")),
            Container(
                content=Text("Setting", size=20), on_click=lambda e: page.go("/")
            ), 
        ]
        ),
        padding= 10,
        bgcolor="blue",
        border_radius=20,
        width = 100, height=100,
        offset= transform.Offset(-5,0),
        animate_offset = animation.Animation(500)
        
    )
    layer= Container(
        on_click=lambda e: hidenev(e),
        content = Column([
            Container(
                content = Row([ IconButton(icon ="menu", icon_color="white", on_click=shownav,)]),
            )
        ])
    )

    # show Item ===================================================
    # img_items= Image(
    #     src=f"/icons/icon-512.png",
    #     width=200,
    #     height=200,
    #     fit=ImageFit.CONTAIN,
    # )


    Item_page = Container(
        width=400,
        height=750,
        border_radius=35,
        on_click=lambda e: hidenev(e),
        bgcolor="#041955",
        content=Column(
            controls=[
                Container(height=20),
                
                layer,
                sidemenu,
                Container(
                    content=Text(load_question(question_index), size=20, color=colors.WHITE)
                ),
                Container(
                    content = box_items
                ),
            ],

        ),
    )
            
    # page __quizz ==============================================================================
    
    page_quizz = Container(
        width=400,
        height=750,
        border_radius=35,
        bgcolor="#041955",
        content=Column(
            controls=[
                Container(height=30),
                Container(content=layer),
                Container(content=sidemenu),
                Container(height=20),  # Spacer or padding
                question_label,
                *option_buttons,
                feedback_label,
                button_,
            ],
        ),
    )
    # choose picture available
    choose_page = Container(
            width=400,
            height=750,
            border_radius=35,
            bgcolor="#041955",
            content=Column(
               controls=[
                    Container(height=30),
                    Container(content=layer),
                    Container(content=sidemenu),
                    ElevatedButton(
                        "Select files...",
                        icon=icons.FOLDER_OPEN,
                        on_click=lambda _: file_picker.pick_files(allow_multiple=True),
                        ),
                        upload_button,
                        file_picker,
                        ElevatedButton(text="choose this image", on_click=lambda e: page.go("/page_quizz"),width=200,height=70),
                    ]
                    
                # horizontal_alignment="center",
            ),
        )
    #page cam =========================================================
    page_cam = Container(
        width=400,
        height=850,
        border_radius=35,
        on_click=lambda e: hidenev(e),
        bgcolor="#041955",
        
        content=Column(
            controls=[
                Container(height=20),
                layer,
                sidemenu,
                # page.update(),
                
                Container(
                    content=myimage,
                    margin=10,
                    padding=10,
                    border_radius=border_radius.all(10),
                    bgcolor="#ffffff",
                    shadow=BoxShadow(
                        spread_radius=2,
                        blur_radius=15,
                        color="#00000022",
                        offset=Offset(2, 2),
                        
                    )
                ),
                # ElevatedButton("Take my face", bgcolor="blue", color="white", on_click=takemepicture),
                ElevatedButton("Take my picture", bgcolor="blue", color="white", on_click=capture_image_button),
                
                button_,
                Column(
                        controls=[
                            ElevatedButton(text="choose this image", on_click=lambda e: page.go("/page_quizz"), width=200, height=70),
                        ]
                    ),
            ],
            # alignment="center",
            # horizontal_alignment="center",
   
        ),
    )


    # button of page main
    buttons = Column(
        controls=[
            ElevatedButton(text="Appcam", on_click=lambda e: page.go("/appcam"),width=200,height=70),
            ElevatedButton(text="choose file", on_click=lambda e: page.go("/choose_file"),width=200,height=70),
            # ElevatedButton(text="show Item", on_click=lambda e: page.go("/Items"),width=200,height=70),

        ],
        alignment="center",  # Center the buttons vertically
        horizontal_alignment="center"
    )
    connt= Container(
        width=400, height=850,
        border_radius=35,
        bgcolor="#041955",
    )
    page_main = Container(
        width=400, height=850,
        border_radius=35,
        bgcolor="#041955",
        
        content=buttons
    )
    
    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                controls=[page_main],
            )
        )
        sidemenu.offset = transform.Offset(-5,0)
        if page.route == "/appcam":
            
            page.views.append(
                ft.View(
                    "/appcam",
                    controls=[page_cam,]
                )
            )
        if page.route == "/choose_file":
          
            page.views.append(
                ft.View(
                    "/choose_file",
                    controls=[choose_page,]
                )
            )
        if page.route == "/page_quizz":
            
            page.views.append(
                ft.View(
                    "/page_quizz",
                    controls=[page_quizz,]
                )
            )
        if page.route == "/Items":
         
            page.views.append(
                ft.View(
                    "/Items",
                    controls=[Item_page,]
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

    ft.app(target=main, assets_dir="photo/", )
# print(qt)







