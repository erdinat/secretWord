import tkinter as tk
import random
import time
from datetime import datetime
import pygame.mixer
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# Görsel yükleme fonksiyonu
def load_image(image_path, size=None):
    try:
        image = Image.open(image_path)
        if size:
            image = image.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)
    except Exception as e:
        print(f"Görsel yüklenemedi: {e}")
        return None

pygame.mixer.init()

correct_sound = pygame.mixer.Sound("musics/correct.mp3")
wrong_sound = pygame.mixer.Sound("musics/wrong.mp3")
win_sound = pygame.mixer.Sound("musics/win.mp3")
lose_sound = pygame.mixer.Sound("musics/lose.mp3")

alien_attack = [
    "🚀 --------- 👽",
     "🚀 ------- 👽",
      "🚀 ----- 👽",
       "🚀 --- 👽",
        "🚀 - 👽",
    "     🚀👽     ",
]

phrases = [
    "rocket launch",
    "solar panel",
    "space mission",
    "alien invasion",
    "black hole"
]

class SpaceEscapeGame:
    def __init__(self, window):
        self.window = window
        self.window.title(" Uzaylıdan Kaçış Şifreli Mesaj")
        self.window.geometry("900x700")
        
        # Arka plan görseli
        self.bg_image = load_image("images/space_bg.jpg", (900, 700))
        if self.bg_image:
            self.bg_label = tk.Label(window, image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Ana container frame (yarı saydam)
        self.main_container = tk.Frame(window, bg="#0B0B2B")
        self.main_container.place(relx=0.5, rely=0.5, anchor="center", width=800, height=600)
        
        # Başlık frame
        self.title_frame = tk.Frame(self.main_container, bg="#0B0B2B")
        self.title_frame.pack(pady=20)
        
        # Uzaylı görseli
        self.alien_image = load_image("images/alien.png", (80, 80))
        if self.alien_image:
            self.alien_img_label = tk.Label(self.title_frame, image=self.alien_image, bg="#0B0B2B")
            self.alien_img_label.pack(side=tk.LEFT, padx=10)
        
        # Ana başlık
        self.title_label = tk.Label(
            self.title_frame,
            text=" UZAYLIDAN KAÇIŞ ",
            font=("Impact", 36, "bold"),
            fg="#00FF9F",
            bg="#0B0B2B"
        )
        self.title_label.pack(side=tk.LEFT, padx=10)
        
        # Roket görseli
        self.rocket_image = load_image("images/rocket.png", (80, 80))
        if self.rocket_image:
            self.rocket_img_label = tk.Label(self.title_frame, image=self.rocket_image, bg="#0B0B2B")
            self.rocket_img_label.pack(side=tk.LEFT, padx=10)
        
        # Gizli kelime frame
        self.secret_frame = tk.Frame(self.main_container, bg="#0B0B2B")
        self.secret_frame.pack(pady=20)
        
        # Gizli kelime gösterimi
        self.secret_label = tk.Label(
            self.secret_frame,
            font=("Impact", 36, "bold"),
            fg="#00FF9F",
            bg="#0B0B2B"
        )
        self.secret_label.pack()
        
        # Uzaylı animasyonu frame
        self.alien_frame = tk.Frame(self.main_container, bg="#0B0B2B")
        self.alien_frame.pack(pady=20)
        
        # Uzaylı animasyonu
        self.alien_label = tk.Label(
            self.alien_frame,
            font=("Impact", 36),
            fg="#FF6B6B",
            bg="#0B0B2B"
        )
        self.alien_label.pack()
        
        # Süre göstergesi frame
        self.timer_frame = tk.Frame(self.main_container, bg="#0B0B2B")
        self.timer_frame.pack(pady=10)
        
        # Süre göstergesi
        self.timer_label = tk.Label(
            self.timer_frame,
            font=("Impact", 24),
            fg="#00FF9F",
            bg="#0B0B2B"
        )
        self.timer_label.pack()
        
        # Harf girişi
        self.entry = tk.Entry(
            self.main_container,
            font=("Impact", 24),
            width=8,
            justify="center",
            bg="#1A1A3A",
            fg="#00FF9F",
            insertbackground="#00FF9F",
            relief="solid",
            borderwidth=2
        )
        self.entry.pack(pady=10)
        self.entry.bind('<Return>', lambda event: self.check_guess())
        
        # Butonlar için stil
        button_style = {
            "font": ("Impact", 16, "bold"),
            "width": 15,
            "height": 2,
            "borderwidth": 2,
            "relief": "raised",
            "cursor": "hand2"
        }
        
        # Butonlar frame
        self.buttons_frame = tk.Frame(self.main_container, bg="#0B0B2B")
        self.buttons_frame.pack(pady=10)
        
        # Tahmin butonu
        self.guess_button = tk.Button(
            self.buttons_frame,
            text="🚀 Tahmin Et",
            command=self.check_guess,
            bg="#2196F3",
            fg="#FF6B6B",
            activebackground="#1976D2",
            activeforeground="#FFFFFF",
            **button_style
        )
        self.guess_button.pack(side=tk.LEFT, padx=5)
        
        # İpucu butonu
        self.hint_button = tk.Button(
            self.buttons_frame,
            text="💡 İpucu Al",
            command=self.give_hint,
            bg="#4CAF50",
            fg="#FF6B6B",
            activebackground="#388E3C",
            activeforeground="#FFFFFF",
            **button_style
        )
        self.hint_button.pack(side=tk.LEFT, padx=5)
        
        # Yeni oyun butonu
        self.restart_button = tk.Button(
            self.buttons_frame,
            text="🔄 Yeni Oyun",
            command=self.start_game,
            bg="#F44336",
            fg="#FF6B6B",
            activebackground="#D32F2F",
            activeforeground="#FFFFFF",
            **button_style
        )
        self.restart_button.pack(side=tk.LEFT, padx=5)
        
        # Çıkış butonu
        self.exit_button = tk.Button(
            self.buttons_frame,
            text="❌ Çıkış",
            command=self.exit_game,
            bg="#9C27B0",  # Mor renk
            fg="#FF6B6B",
            activebackground="#7B1FA2",
            activeforeground="#FFFFFF",
            **button_style
        )
        self.exit_button.pack(side=tk.LEFT, padx=5)
        
        # Oyun değişkenleri
        self.selected_phrase = ""
        self.guessed_letters = []
        self.current_step = 0
        self.hint_used = False
        self.game_active = False
        self.start_time = 0
        self.remaining_time = 20
        self.timer_id = None
        
        # Oyunu başlat
        self.start_game()
    
    def start_game(self):
        self.selected_phrase = random.choice(phrases)
        self.guessed_letters = []
        self.current_step = 0
        self.hint_used = False
        self.game_active = True
        self.start_time = time.time()
        self.remaining_time = 20
        self.update_display()
        self.update_alien_art()
        self.entry.config(state='normal')
        self.guess_button.config(state='normal')
        self.hint_button.config(state='normal')
        if self.timer_id is not None:
            self.window.after_cancel(self.timer_id)
        self.start_countdown()
    
    def start_countdown(self):
        self.remaining_time = 20
        timer_text = f"Kalan Süre: {self.remaining_time}"
        self.timer_label.config(text=timer_text)
        if self.timer_id is not None:
            self.window.after_cancel(self.timer_id)
        self.timer_id = self.window.after(1000, self.countdown)
    
    def countdown(self):
        self.remaining_time -= 1
        timer_text = f"Kalan Süre: {self.remaining_time}"
        self.timer_label.config(text=timer_text)
        if self.remaining_time > 0:
            self.timer_id = self.window.after(1000, self.countdown)
        else:
            self.handle_timeout()
    
    def handle_timeout(self):
        self.process_wrong_guess()
        self.start_countdown()
    
    def process_wrong_guess(self):
        self.current_step += 1
        self.update_alien_art()
        wrong_sound.play()
        if self.current_step >= 6:
            self.end_game(False)
    
    def update_display(self):
        displayed = []
        for char in self.selected_phrase:
            if char.lower() in self.guessed_letters or char == ' ':
                displayed.append(char)
            else:
                displayed.append('_')
        display_text = ' '.join(displayed)
        self.secret_label.config(text=display_text)
    
    def update_alien_art(self):
        step = min(self.current_step, len(alien_attack) - 1)
        alien_text = alien_attack[step]
        self.alien_label.config(text=alien_text)
    
    def check_guess(self):
        if not self.game_active:
            return
        letter = self.entry.get().strip().lower()
        self.entry.delete(0, tk.END)
        if len(letter) != 1 or not letter.isalpha():
            return
        if letter in self.guessed_letters:
            return
        self.guessed_letters.append(letter)
        if letter in self.selected_phrase.lower():
            correct_sound.play()
            self.update_display()
            if self.check_win():
                self.end_game(True)
        else:
            if letter in ['x', 'z', 'j', 'q']:
                self.current_step += 2
            else:
                self.current_step += 1
            wrong_sound.play()
            self.update_alien_art()
            if self.current_step >= 6:
                self.end_game(False)
            self.update_display()
        self.window.after_cancel(self.timer_id)
        self.start_countdown()
    
    def check_win(self):
        for char in self.selected_phrase.lower():
            if char != ' ' and char not in self.guessed_letters:
                return False
        return True
    
    def give_hint(self):
        if not self.game_active or self.hint_used:
            return
        self.hint_used = True
        first_char = self.selected_phrase[0].lower()
        if first_char not in self.guessed_letters:
            self.guessed_letters.append(first_char)
        self.current_step += 1
        self.update_alien_art()
        wrong_sound.play()
        if self.current_step >= 6:
            self.end_game(False)
        self.update_display()
        self.hint_button.config(state='disabled')
    
    def end_game(self, won):
        self.update_display()
        self.game_active = False
        if self.timer_id is not None:
            self.window.after_cancel(self.timer_id)
        end_time = time.time()
        total_time = int(end_time - self.start_time)
        if won:
            win_sound.play()
        else:
            lose_sound.play()
        with open("scores.txt", "a", encoding="utf-8") as f:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            result = "KAZANDI" if won else "KAYBETTİ"
            f.write(f"{current_time} | {result} | {self.selected_phrase} | {total_time} saniye\n")
        message = "Tebrikler! Kazandınız!" if won else "Maalesef kaybettiniz."
        messagebox.showinfo("Oyun Bitti", message)
        self.entry.config(state='disabled')
        self.guess_button.config(state='disabled')
        self.hint_button.config(state='disabled')

    def exit_game(self):
        if messagebox.askyesno("Çıkış", "Oyundan çıkmak istediğinizden emin misiniz?"):
            self.window.quit()

if __name__ == "__main__":
    window = tk.Tk()
    game = SpaceEscapeGame(window)
    window.mainloop()