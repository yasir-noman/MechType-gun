import os
import threading
import customtkinter as ctk
import pygame
from pynput import keyboard

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class AvroStyleMechApp(ctk.CTk):

  def __init__(self):
    super().__init__()

    
    self.geometry("320x50+500+20")
    self.overrideredirect(True)  
    self.wm_attributes("-topmost", True)  

    
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()

    self.is_enabled = True
    self.sounds_dir = "sounds"

    
    self.load_sounds()
    self.create_widgets()

    
    self.bind("<Button-1>", self.start_move)
    self.bind("<B1-Motion>", self.do_move)

   
    self.start_keyboard_listener()

  def load_sounds(self):
    
    default_path = os.path.join(self.sounds_dir, "default.mp3")
    if os.path.exists(default_path):
      self.default_sound = pygame.mixer.Sound(default_path)
    else:
      print("Warning: default.mp3 sounds not found!")
      self.default_sound = None

  def create_widgets(self):
    self.frame = ctk.CTkFrame(self, corner_radius=10, border_width=1)
    self.frame.pack(fill="both", expand=True, padx=2, pady=2)

    self.title_label = ctk.CTkLabel(
        self.frame, text="🎹 Mech", font=ctk.CTkFont(size=14, weight="bold")
    )
    self.title_label.pack(side="left", padx=(10, 5))

  
    self.switch_var = ctk.StringVar(value="on")
    self.toggle_switch = ctk.CTkSwitch(
        self.frame,
        text="ON",
        command=self.toggle_sound,
        variable=self.switch_var,
        onvalue="on",
        offvalue="off",
        width=40,
        font=ctk.CTkFont(size=12, weight="bold"),
    )
    self.toggle_switch.pack(side="left", padx=10)

   
    self.close_btn = ctk.CTkButton(
        self.frame,
        text="✕",
        width=25,
        height=25,
        fg_color="transparent",
        hover_color="red",
        command=self.destroy,
    )
    self.close_btn.pack(side="right", padx=5)

  def toggle_sound(self):
    if self.switch_var.get() == "on":
      self.is_enabled = True
      self.toggle_switch.configure(text="ON")
    else:
      self.is_enabled = False
      self.toggle_switch.configure(text="OFF")

  def start_move(self, event):
    self.x = event.x
    self.y = event.y

  def do_move(self, event):
    deltax = event.x - self.x
    deltay = event.y - self.y
    x = self.winfo_x() + deltax
    y = self.winfo_y() + deltay
    self.geometry(f"+{x}+{y}")

  def on_key_press(self, key):
    if self.is_enabled and self.default_sound:
      try:
        self.default_sound.play()
      except Exception as e:
        pass

  def start_keyboard_listener(self):
    def listen():
      with keyboard.Listener(on_press=self.on_key_press) as listener:
        listener.join()

    threading.Thread(target=listen, daemon=True).start()


if __name__ == "__main__":
  app = AvroStyleMechApp()
  app.mainloop()