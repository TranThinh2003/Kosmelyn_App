from flet import *

class QuestionView(Container):
    def __init__(self, page: Page, questions_data: list, on_quiz_complete, loading_container: Container, loading_status_text: Text):
        super().__init__(expand=True, alignment=alignment.center, padding=20)
        
        self.page = page
        self.questions_data = questions_data
        self.on_quiz_complete = on_quiz_complete 
        self.loading_container = loading_container
        self.loading_status_text = loading_status_text


        self.question_index = 0
        self.answers = {}

        self.question_label = Text(
                                    "", 
                                    weight=FontWeight.BOLD, 
                                    color="white", 
                                    size=18,
                                    text_align=TextAlign.CENTER
                                )
        

        self.option_buttons = [
            ElevatedButton(
                text="",
                on_click=self.check_answer_logic,
                visible=False,
                width=300, 
                height=45,
                style=ButtonStyle(
                    shape=RoundedRectangleBorder(radius=10),
                    bgcolor={"": "#1976d2"},
                    color="black"
                )
            ) 
            for _ in range(4)
        ]
        
        self.show_results_button = ElevatedButton(
            "Show Recommendations",
            on_click=self.show_quiz_results_logic,
            visible=False,
            width=250,
            height=50,
            icon=Icons.SEARCH
        )
        
        self.content = Column(
            controls=[
                self.question_label,
                *self.option_buttons,
                self.show_results_button
            ],
            horizontal_alignment=CrossAxisAlignment.CENTER,
            spacing=20,
            expand=True,
            alignment=MainAxisAlignment.CENTER
        )

    def load_question_logic(self):
        if self.question_index < len(self.questions_data):
            question_data = self.questions_data[self.question_index]
            self.question_label.value = question_data["question"]
            
            for i, option_btn in enumerate(self.option_buttons):
                if i < len(question_data["options"]):
                    option_btn.text = question_data["options"][i]
                    option_btn.visible = True
                    option_btn.data = question_data["options"][i] 
                else:
                    option_btn.visible = False
            if getattr(self, "page", None) is not None:
                self.page.update()


    def check_answer_logic(self, e: ControlEvent):
        selected_option = e.control.data
        question_key = self.questions_data[self.question_index]["key"]

        self.answers[question_key] = selected_option
        # print(f"Quiz answers so far: {self.answers}")
        
        self.question_index += 1
        
        if self.question_index < len(self.questions_data):
            self.load_question_logic()
        else:
            self.question_label.value = "Quiz finished! Thank you."
            for option in self.option_buttons:
                option.visible = False
            self.show_results_button.visible = True
        self.page.update()


    def show_quiz_results_logic(self, e):
        self.loading_status_text.value = "Analyzing your skin type..."
        self.loading_container.visible = True
        self.page.update()
        self.page.go("/results")
        self.on_quiz_complete(user_answers=self.answers)
    def view_will_appear(self):
        self.question_index = 0
        self.answers = {}
        self.show_results_button.visible = False
        self.load_question_logic()

    def view_did_disappear(self):
        print("Leaving quiz view.")