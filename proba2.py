import face_recognition as fr
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class Recogniser(tk.Tk):

    def __init__(self):
        self.answers = []
        self.pic1 = None
        self.pic2 = None
        self.p1 = False
        self.p2 = False
        # Добавляем переменные для хранения ссылок на изображения
        self.img_tk1 = None
        self.img_tk2 = None

        super().__init__()
        
        self.title('Сравнение лиц на фотографиях')
        self.config(bg='grey')
        self.geometry('1200x600')
        self.resizable(False, False)

        self.ans_box = tk.Text(
            self, 
            width=40, 
            height=30,  
            bg='white',
            borderwidth=1,
            font=('Times New Roman', 12),
            fg="black",
        )
        self.ans_box.place(relx=0.85, rely=0.5, anchor=tk.CENTER)
        self.ans_box.config(state='disabled')

        # Создаем фреймы для изображений
        self.img_frame1 = tk.Frame(self, width=200, height=150, bg='lightgray')
        self.img_frame1.place(relx=0.2, rely=0.3, anchor=tk.CENTER)
        
        self.img_frame2 = tk.Frame(self, width=200, height=150, bg='lightgray')
        self.img_frame2.place(relx=0.4, rely=0.3, anchor=tk.CENTER)

        self.img1 = tk.Label(self.img_frame1)
        self.img1.pack(expand=True, fill='both')
        
        self.img2 = tk.Label(self.img_frame2)
        self.img2.pack(expand=True, fill='both')

        self.button1 = tk.Button(self, text='Выбери фото 1', width=20, height=1)
        self.button1.bind("<Button-1>", self.find_pic1)
        self.button1.place(relx=0.2, rely=0.7, anchor=tk.CENTER)

        self.button2 = tk.Button(self, text='Выбери фото 2', width=20, height=1)
        self.button2.bind("<Button-1>", self.find_pic2)
        self.button2.place(relx=0.4, rely=0.7, anchor=tk.CENTER)

        self.button_chk = tk.Button(self, text='Сравните фото', width=20, height=1)
        self.button_chk.bind("<Button-1>", self.check)
        self.button_chk.place(relx=0.3, rely=0.775, anchor=tk.CENTER)

        self.button_res = tk.Button(self, text='Очистка', width=10, height=1)
        self.button_res.bind("<Button-1>", self.reset)
        self.button_res.place(relx=0.6, rely=0.9, anchor=tk.CENTER)
    
    def check(self, event):
        if self.p1 and self.p2:
            self.ans_box.config(state='normal')
            if fr.compare_faces([self.pic1], self.pic2)[0]:  # Исправлено: pic1 должен быть в списке
                self.ans_box.insert(index=tk.END, chars='\n'+'Очень похожи!!!')
            else:
                self.ans_box.insert(index=tk.END, chars='\n'+'Совсем не похожи...')
            self.ans_box.config(state='disabled')
        elif not self.p1 and not self.p2:
            self.ans_box.config(state='normal')
            self.ans_box.insert(index=tk.END, chars='\n'+"Не загружено оба фото")
            self.ans_box.config(state='disabled')
        elif not self.p2:
            self.ans_box.config(state='normal')
            self.ans_box.insert(index=tk.END, chars='\n'+"Не загружено фото 2")
            self.ans_box.config(state='disabled')
        else:
            self.ans_box.config(state='normal')
            self.ans_box.insert(index=tk.END, chars='\n'+"Не загружено фото 1")
            self.ans_box.config(state='disabled')
    
    def find_pic1(self, event):
        p = filedialog.askopenfilename(title="Открыть файл изображения", filetypes=[("Файлы изображений", "*.png *.jpg *.jpeg")])
        if p:
            try:
                # Загружаем изображение для распознавания
                img = fr.load_image_file(p)
                encodings = fr.face_encodings(img)
                if encodings:
                    self.pic1 = encodings[0]
                    self.p1 = True
                    
                    # Загружаем изображение для отображения
                    img = Image.open(p)
                    img.thumbnail((200, 150))  # Масштабируем изображение
                    self.img_tk1 = ImageTk.PhotoImage(img)
                    self.img1.config(image=self.img_tk1)
                else:
                    self.ans_box.config(state='normal')
                    self.ans_box.insert(index=tk.END, chars='\n'+"На фото 1 не найдено лиц")
                    self.ans_box.config(state='disabled')
            except Exception as e:
                self.ans_box.config(state='normal')
                self.ans_box.insert(index=tk.END, chars='\n'+f"Ошибка загрузки фото 1: {str(e)}")
                self.ans_box.config(state='disabled')

    def find_pic2(self, event):
        p = filedialog.askopenfilename(title="Открыть файл изображения", filetypes=[("Файлы изображений", "*.png *.jpg *.jpeg")])
        if p:
            try:
                # Загружаем изображение для распознавания
                img = fr.load_image_file(p)
                encodings = fr.face_encodings(img)
                if encodings:
                    self.pic2 = encodings[0]
                    self.p2 = True
                    
                    # Загружаем изображение для отображения
                    img = Image.open(p)
                    img.thumbnail((200, 150))  # Масштабируем изображение
                    self.img_tk2 = ImageTk.PhotoImage(img)
                    self.img2.config(image=self.img_tk2)
                else:
                    self.ans_box.config(state='normal')
                    self.ans_box.insert(index=tk.END, chars='\n'+"На фото 2 не найдено лиц")
                    self.ans_box.config(state='disabled')
            except Exception as e:
                self.ans_box.config(state='normal')
                self.ans_box.insert(index=tk.END, chars='\n'+f"Ошибка загрузки фото 2: {str(e)}")
                self.ans_box.config(state='disabled')

    def reset(self, event):
        self.p1 = False
        self.p2 = False
        self.pic1 = None
        self.pic2 = None
        self.img_tk1 = None
        self.img_tk2 = None

        self.img1.config(image=None)
        self.img2.config(image=None)

        self.ans_box.config(state='normal')
        self.ans_box.delete('1.0', tk.END)
        self.ans_box.config(state='disabled')

if __name__ == '__main__':
    r = Recogniser()
    r.mainloop()