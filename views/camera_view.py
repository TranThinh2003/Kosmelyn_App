from flet import *
import cv2
import base64
import threading

class CameraView(Container):
    def __init__(self, page: Page, extract_img_func, build_results_func,loading_container: Container, loading_status_text: Text):
        super().__init__(expand=True, alignment=alignment.center)
        
        self.page = page
        self.extract_img = extract_img_func
        self.build_results = build_results_func
        self.loading_container = loading_container
        self.loading_status_text = loading_status_text

        self.cap = None
        self.is_camera_running = False

        self.camera_image = Image(fit=ImageFit.CONTAIN, src="camera_placeholder.jpg")
        self.start_button = ElevatedButton("Start Camera", on_click=self.start_camera_logic, icon=Icons.CAMERA_ALT)
        self.capture_button = ElevatedButton("Capture & Analyze", on_click=self.capture_and_process_logic, icon=Icons.PHOTO_CAMERA, visible=False)

        self.content = Column(
            controls=[
                Text("Live Camera", size=20, color="white"),
                Container(content=self.camera_image, expand=True, alignment=alignment.center),
                Row(controls=[self.start_button, self.capture_button], alignment=MainAxisAlignment.CENTER)
            ],
            horizontal_alignment=CrossAxisAlignment.CENTER,
            spacing=10  
        )


    def start_camera_logic(self, e):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.page.snack_bar = SnackBar(content=Text("Failed to open camera."), bgcolor="red")
            self.page.snack_bar.open = True
            self.page.update()
            return
        self.is_camera_running = True
        self.start_button.visible = False
        self.capture_button.visible = True
        self.page.update()
        
        def camera_loop():
            while self.is_camera_running:
                ret, frame = self.cap.read()
                if not ret:
                    print("Failed to grab frame")
                    self.stop_camera_logic()
                    break
                _, buffer = cv2.imencode('.jpg', frame)
                jpg_as_text = base64.b64encode(buffer).decode('utf-8')
                self.camera_image.src_base64 = jpg_as_text
                self.page.update()
        
        threading.Thread(target=camera_loop, daemon=True).start()

    def stop_camera_logic(self):
        if self.is_camera_running:
            self.is_camera_running = False
            if self.cap:
                self.cap.release()
                self.cap = None
            self.camera_image.src_base64 = None
            self.start_button.visible = True
            self.capture_button.visible = False
            self.page.update()
            self.start_button.visible = True
            self.capture_button.visible = False
            self.page.update()


    def capture_and_process_logic(self, e):
        if self.cap and self.is_camera_running:
            ret, frame = self.cap.read()

            if ret:
                self.stop_camera_logic()
                print("Image captured!")
                self.loading_container.visible = True
                self.loading_status_text.value = "Analyzing your skin..."
                self.page.go("/results")
                self.page.update()

                def analyze():
                    try:
                        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        skin_status = self.extract_img(rgb_frame)

                        if not skin_status:
                            if self.page:
                                self.page.snack_bar = SnackBar(content=Text("Failed to analyze image."), bgcolor="red")
                                self.page.snack_bar.open = True
                                self.page.go("/")
                                self.page.update()
                            else:
                                print("Failed to analyze image (no page available).")
                            return
                        self.build_results(user_status=skin_status)
                        if self.page:
                            self.page.update()
                        
                    except Exception as ex:
                        print(f'Analysis error: {ex}')
                        if self.page:
                            self.page.snack_bar = SnackBar(content=Text("Analysis failed."), bgcolor="red")
                            self.page.snack_bar.open = True
                            self.page.go("/")
                            self.page.update()
                        else:
                            print("Analysis failed and no page available.")

                threading.Thread(target=analyze, daemon=True).start()
            else:
                self.stop_camera_logic()

    def view_will_appear(self):
        self.start_button.visible = True
        self.capture_button.visible = False
        self.camera_image.src_base64 = None


    def view_did_disappear(self):
        self.stop_camera_logic()