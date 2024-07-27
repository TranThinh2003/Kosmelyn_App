# import flet as ft

# def main(page: ft.Page):
#     page.title = "Skincare Consultation Quiz"
#     page.padding = 20

#     # Danh sách các câu hỏi và câu trả lời
#     questions = [
#         {
#             "question": "Loại da của bạn là gì? ",
#             "options": ["Khô", "Dầu", "Mụn", "Nhạy cảm"],
#             "answer": None
#         },
#         {
#             "question": "Bạn có thường xuyên tiếp xúc với ánh nắng mặt trời không?",
#             "options": ["Có", "Không", "Thỉnh thoảng"],
#             "answer": None
#         },
#         {
#             "question": "Bạn có sử dụng kem chống nắng hàng ngày không?",
#             "options": ["Có", "Không", "Thỉnh Thoảng"],
#             "answer": None
#         },
#         {
#             "question": "Bạn có thường xuyên trang điểm không?",
#             "options": ["Có", "Không", "Thỉnh Thoảng"],
#             "answer": None
#         },
#         {
#             "question": "Bạn có thói quen tẩy trang trước khi đi ngủ không?",
#             "options": ["Có", "Không"],
#             "answer": None
#         },
#         {
#             "question": "Bạn sử dụng sản phẩm sữa rửa mặt bao nhiêu lần một ngày?",
#             "options": ["Một lần", "Hai lần", "Nhiều lần", "Không bao giờ"],
#             "answer": None
#         },
#         {
#             "question": "Bạn sử dụng sản phẩm dưỡng ẩm bao nhiêu lần một ngày?",
#             "options": ["Một lần", "Hai lần", "Nhiều lần", "Không bao giờ"],
#             "answer": None
#         },
#         {
#             "question": "Bạn tẩy tế bào chết cho da bao nhiêu lần một tuần?",
#             "options": ["Một lần", "Hai lần", "Nhiều lần", "Không bao giờ"],
#             "answer": None
#         },
#         {
#             "question": "Bạn sử dụng mặt nạ cho da bao nhiêu lần một tuần?",
#             "options": ["Một lần", "Hai lần", "Nhiều lần", "Không bao giờ"],
#             "answer": None
#         },
#         {
#             "question": "Bạn có thường xuyên đi spa chăm sóc da không?",
#             "options": ["Có", "Không", "Thỉnh Thoảng"],
#             "answer": None
#         }
#     ]

#     question_index = 0
#     answers = []

#     def load_question(index):
#         question_data = questions[index]
#         question_label.value = question_data["question"]
#         for i, option in enumerate(option_buttons):
#             if i < len(question_data["options"]):
#                 option.text = question_data["options"][i]
#                 option.visible = True
#             else:
#                 option.visible = False
#         page.update()

#     def check_answer(e):
#         nonlocal question_index
#         selected_option = e.control.text
#         answers.append(selected_option)

#         question_index += 1
#         if question_index < len(questions):
#             load_question(question_index)
#         else:
#             feedback_label.value = "Quiz finished! Here are your skincare tips:"
#             provide_advice()
#             for option in option_buttons:
#                 option.visible = False

#         page.update()

#     def provide_advice():
#         advice = ""
#         skin_problem = answers[0]
#         if skin_problem == "Khô":
#             advice += "\n- Use moisturizing products with hyaluronic acid."
#         elif skin_problem == "Dầu":
#             advice += "\n- Use oil-free and non-comedogenic products."
#         elif skin_problem == "Mụn":
#             advice += "\n- Consider products with salicylic acid or benzoyl peroxide."
#         elif skin_problem == "Nhạy cảm":
#             advice += "\n- Use gentle and fragrance-free products."

#         sunscreen_usage = answers[1]
#         if sunscreen_usage == "Có":
#             advice += "\n- Good job! Sunscreen helps protect your skin from harmful UV rays."
#         elif sunscreen_usage == "Không":
#             advice += "\n- Consider using sunscreen daily to protect your skin from UV damage."

#         makeup_removal = answers[2]
#         if makeup_removal == "Có":
#             advice += "\n- Great! Removing makeup before bed helps prevent breakouts."
#         elif makeup_removal == "Không":
#             advice += "\n- Make sure to remove makeup before bed to keep your skin clean."

#         moisturizing_frequency = answers[3]
#         if moisturizing_frequency == "Một lần":
#             advice += "\n- Consider moisturizing twice a day to keep your skin hydrated."
#         elif moisturizing_frequency == "Hai lần":
#             advice += "\n- Excellent! Keep up the good work."
#         elif moisturizing_frequency == "Không bao giờ":
#             advice += "\n- Moisturizing is important for maintaining healthy skin."

#         feedback_label.value += advice
#         page.update()

#     question_label = ft.Text()
#     feedback_label = ft.Text()
#     option_buttons = [ft.ElevatedButton(text="", on_click=check_answer) for _ in range(4)]

#     # Thêm tất cả các điều khiển vào trang trước khi gọi load_question
#     page.add(
#         question_label,
#         *option_buttons,
#         feedback_label
#     )

#     load_question(question_index)

# ft.app(target=main)


import flet as ft

def main(page: ft.Page):
    page.title = "Skincare Consultation Quiz"
    page.padding = 20

    # List of questions and answers
    questions = [
        {
            "question": "What is your skin type?",
            "options": ["Dry", "Oily", "Acne-prone", "Sensitive"],
            "answer": None
        },
        {
            "question": "Do you often get exposed to sunlight?",
            "options": ["Yes", "No", "Sometimes"],
            "answer": None
        },
        {
            "question": "Do you use sunscreen daily?",
            "options": ["Yes", "No", "Sometimes"],
            "answer": None
        },
        {
            "question": "Do you often wear makeup?",
            "options": ["Yes", "No", "Sometimes"],
            "answer": None
        },
        {
            "question": "Do you have a habit of removing makeup before bed?",
            "options": ["Yes", "No"],
            "answer": None
        },
        {
            "question": "How many times a day do you use facial cleanser?",
            "options": ["Once", "Twice", "Multiple times", "Never"],
            "answer": None
        },
        {
            "question": "How many times a day do you use moisturizer?",
            "options": ["Once", "Twice", "Multiple times", "Never"],
            "answer": None
        },
        {
            "question": "How many times a week do you exfoliate your skin?",
            "options": ["Once", "Twice", "Multiple times", "Never"],
            "answer": None
        },
        {
            "question": "How many times a week do you use a face mask?",
            "options": ["Once", "Twice", "Multiple times", "Never"],
            "answer": None
        },
        {
            "question": "Do you often go to the spa for skin care?",
            "options": ["Yes", "No", "Sometimes"],
            "answer": None
        }
    ]

    question_index = 0
    answers = []

    def load_question(index):
        """Load the question and options based on the current index."""
        question_data = questions[index]
        question_label.value = question_data["question"]
        for i, option in enumerate(option_buttons):
            if i < len(question_data["options"]):
                option.text = question_data["options"][i]
                option.visible = True
            else:
                option.visible = False
        page.update()

    def check_answer(e):
        """Check the selected answer and proceed to the next question or finish the quiz."""
        nonlocal question_index
        selected_option = e.control.text
        answers.append(selected_option)

        question_index += 1
        if question_index < len(questions):
            load_question(question_index)
        else:
            feedback_label.value = "Quiz finished! Here are your skincare tips:"
            provide_advice()
            for option in option_buttons:
                option.visible = False

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

    question_label = ft.Text()
    feedback_label = ft.Text()
    option_buttons = [ft.ElevatedButton(text="", on_click=check_answer) for _ in range(4)]

    # Add all controls to the page before calling load_question
    page.add(
        question_label,
        *option_buttons,
        feedback_label
    )

    load_question(question_index)

ft.app(target=main)
