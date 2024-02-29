import cv2
import dlib
import tkinter as tk
from tkinter import Canvas, Label, Button, filedialog, Scale, IntVar, Menu
from tkinter.ttk import Checkbutton
from PIL import Image, ImageTk
import os
import threading
import time

class FacialRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reconhecimento Facial")

        self.video_sources = self.get_available_cameras()
        self.current_camera_index = 0
        self.cap = cv2.VideoCapture(self.video_sources[self.current_camera_index])
        self.face_detector = dlib.get_frontal_face_detector()
        self.eye_detector = dlib.get_frontal_face_detector()

        self.night_mode_var = IntVar()
        self.recording = False
        self.photo_count = 0

        self.create_menu()
        self.create_interface()

        self.root.after(10, self.update)

    def create_menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        file_menu.add_command(label="Capturar Foto", command=self.capture_photo)
        file_menu.add_command(label="Iniciar/Parar Gravação", command=self.toggle_record)
        file_menu.add_command(label="Capturar Múltiplas Fotos", command=self.capture_multiple_photos)
        file_menu.add_command(label="Reiniciar", command=self.reset_app)
        file_menu.add_separator()
        file_menu.add_command(label="Fechar", command=self.close_app)

        options_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Opções", menu=options_menu)

        brightness_menu = Menu(options_menu, tearoff=0)
        options_menu.add_cascade(label="Ajuste de Iluminação", menu=brightness_menu)
        brightness_menu.add_command(label="Baixa", command=lambda: self.adjust_brightness(50))
        brightness_menu.add_command(label="Média", command=lambda: self.adjust_brightness(127))
        brightness_menu.add_command(label="Alta", command=lambda: self.adjust_brightness(200))

        contrast_menu = Menu(options_menu, tearoff=0)
        options_menu.add_cascade(label="Ajuste de Contraste", menu=contrast_menu)
        contrast_menu.add_command(label="Baixo", command=lambda: self.adjust_contrast(-32))
        contrast_menu.add_command(label="Médio", command=lambda: self.adjust_contrast(0))
        contrast_menu.add_command(label="Alto", command=lambda: self.adjust_contrast(32))

        smooth_menu = Menu(options_menu, tearoff=0)
        options_menu.add_cascade(label="Filtro de Suavização", menu=smooth_menu)
        smooth_menu.add_command(label="Baixo", command=lambda: self.apply_smooth_filter(3))
        smooth_menu.add_command(label="Médio", command=lambda: self.apply_smooth_filter(5))
        smooth_menu.add_command(label="Alto", command=lambda: self.apply_smooth_filter(9))

        options_menu.add_checkbutton(label="Modo Noturno", variable=self.night_mode_var, command=self.toggle_night_mode)

    def create_interface(self):
        self.canvas = Canvas(self.root)
        self.canvas.pack()

        self.face_count_label = Label(self.root, text="Rostos detectados: 0")
        self.face_count_label.pack()

        self.eye_count_label = Label(self.root, text="Olhos detectados: 0")
        self.eye_count_label.pack()

        self.smile_count_label = Label(self.root, text="Sorrisos detectados: 0")
        self.smile_count_label.pack()

        self.expression_label = Label(self.root, text="Expressão predominante:")
        self.expression_label.pack()

        self.setup_buttons()

    def setup_buttons(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        capture_photo_button = Button(button_frame, text="Capturar Foto", command=self.capture_photo)
        capture_photo_button.grid(row=0, column=0, padx=10)

        toggle_record_button = Button(button_frame, text="Iniciar/Parar Gravação", command=self.toggle_record)
        toggle_record_button.grid(row=0, column=1, padx=10)

        capture_multiple_button = Button(button_frame, text="Capturar Múltiplas Fotos", command=self.capture_multiple_photos)
        capture_multiple_button.grid(row=0, column=2, padx=10)

        reset_button = Button(button_frame, text="Reiniciar", command=self.reset_app)
        reset_button.grid(row=0, column=3, padx=10)

    def get_available_cameras(self):
        cameras = []
        for i in range(10):  # Verificar até 10 câmeras
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                cameras.append(i)
            cap.release()
        return cameras

    def update(self):
        ret, frame = self.cap.read()

        if ret:
            faces, eyes, smiles, expression = self.detect_faces_and_eyes(frame)
            smooth_filter_value = 5  # valor padrão
            frame = self.apply_smooth_filter(frame, smooth_filter_value)

            self.display_frame(frame, faces, eyes, smiles, expression)
            self.update_face_count(len(faces))
            self.update_eye_count(len(eyes))
            self.update_smile_count(len(smiles))
            self.update_expression(expression)

        self.root.after(10, self.update)

    def detect_faces_and_eyes(self, frame):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Adicione a detecção de sorrisos aqui
        smiles = []

        # Adicione o reconhecimento de expressões aqui
        expression = "N/A"

        faces = self.face_detector(gray_frame)
        eyes = self.eye_detector(gray_frame)

        return faces, eyes, smiles, expression

    def display_frame(self, frame, faces, eyes, smiles, expression):
        for face in faces:
            self.draw_rectangle(frame, face, (0, 255, 0))

        for eye in eyes:
            self.draw_rectangle(frame, eye, (255, 0, 0))

        for smile in smiles:
            self.draw_rectangle(frame, smile, (0, 0, 255))

        self.display_expression(frame, expression)

        self.adjust_brightness_frame(frame)
        photo = self.convert_frame_to_image(frame)
        self.display_on_canvas(photo)

    def display_expression(self, frame, expression):
        self.expression_label.config(text=f"Expressão predominante: {expression}")

    def draw_rectangle(self, frame, rect, color):
        x, y, w, h = rect.left(), rect.top(), rect.width(), rect.height()
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

    def convert_frame_to_image(self, frame):
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (int(self.cap.get(3)), int(self.cap.get(4))))

        # Use PIL para converter a imagem
        img_pil = Image.fromarray(img)
        img_tk = ImageTk.PhotoImage(image=img_pil)

        return img_tk

    def display_on_canvas(self, photo):
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.image = photo  # Salvar uma referência para evitar a coleta de lixo

    def update_face_count(self, count):
        self.face_count_label.config(text=f"Rostos detectados: {count}")

    def update_eye_count(self, count):
        self.eye_count_label.config(text=f"Olhos detectados: {count}")

    def update_smile_count(self, count):
        self.smile_count_label.config(text=f"Sorrisos detectados: {count}")

    def update_expression(self, expression):
        self.expression_label.config(text=f"Expressão predominante: {expression}")

    def close_app(self):
        if self.cap.isOpened():
            self.cap.release()
            if self.recording:
                self.stop_record()
        self.root.destroy()

    def switch_camera(self):
        if len(self.video_sources) > 1:
            self.cap.release()
            self.current_camera_index = (self.current_camera_index + 1) % len(self.video_sources)
            self.cap = cv2.VideoCapture(self.video_sources[self.current_camera_index])

    def capture_photo(self):
        ret, frame = self.cap.read()
        if ret:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                        filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                                                        title="Salvar Foto")
            if file_path:
                cv2.imwrite(file_path, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    def toggle_record(self):
        if not self.recording:
            self.start_record()
        else:
            self.stop_record()

    def start_record(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".avi",
                                                    filetypes=[("AVI files", "*.avi"), ("All files", "*.*")],
                                                    title="Salvar Vídeo")
        if file_path:
            self.out = cv2.VideoWriter(file_path, cv2.VideoWriter_fourcc(*'XVID'), 20.0, (int(self.cap.get(3)), int(self.cap.get(4))))
            self.recording = True
            self.record_start_time = time.time()
            self.update_record_timer()

    def stop_record(self):
        if self.recording:
            self.out.release()
            self.recording = False

    def update_record_timer(self):
        if self.recording:
            elapsed_time = int(time.time() - self.record_start_time)
            minutes, seconds = divmod(elapsed_time, 60)
            timer_text = f"Tempo de Gravação: {minutes:02d}:{seconds:02d}"
            self.root.after(1000, self.update_record_timer)

    def capture_multiple_photos(self):
        ret, frame = self.cap.read()
        if ret:
            self.photo_count += 1
            file_path = os.path.join(os.getcwd(), f"captured_photo_{self.photo_count}.png")
            cv2.imwrite(file_path, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    def reset_app(self):
        self.cap.release()
        self.cap = cv2.VideoCapture(self.video_sources[self.current_camera_index])
        self.recording = False
        self.photo_count = 0

    def adjust_brightness(self, value):
        value = int(value)
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, value / 255.0)

    def adjust_contrast(self, value):
        value = int(value)
        self.cap.set(cv2.CAP_PROP_CONTRAST, value / 64.0)

    def adjust_brightness_frame(self, frame):
        brightness_value = 127  # valor padrão
        frame = cv2.convertScaleAbs(frame, alpha=brightness_value/127.0, beta=255-brightness_value)

        contrast_value = 0  # valor padrão
        frame = cv2.convertScaleAbs(frame, alpha=1.0 + contrast_value / 64.0, beta=0)

        return frame

    def apply_smooth_filter(self, frame, kernel_size):
        if kernel_size % 2 == 0:
            kernel_size += 1  # Certifique-se de que o tamanho do kernel seja ímpar

        return cv2.GaussianBlur(frame, (kernel_size, kernel_size), 0)

    def toggle_night_mode(self):
        if self.night_mode_var.get() == 1:
            self.root.configure(bg="black")
        else:
            self.root.configure(bg="white")


if __name__ == "__main__":
    root = tk.Tk()
    app = FacialRecognitionApp(root)
    root.mainloop()
