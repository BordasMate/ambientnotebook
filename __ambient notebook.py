import tkinter as tk
import pygame
import os
import threading

def load_sounds(soundbank):
    sounds.clear()
    soundbank_path = f'soundbanks/{soundbank}'
    volume = soundbank_volumes.get(soundbank, default_volume)
    if os.path.exists(soundbank_path):
        for letter in 'abcdefghijklmnopqrstuvwxyzáéíóöőúüű':
            sound_path = f'{soundbank_path}/{letter}.wav'
            if os.path.exists(sound_path):
                sound = pygame.mixer.Sound(sound_path)
                sound.set_volume(volume)
                sounds[letter] = sound
            else:
                print(f"A '{sound_path}' hangfájl nem található.")

def load_sounds_async(soundbank):
    def load_task():
        load_sounds(soundbank)
        print(f"{soundbank} betöltve.")
    load_thread = threading.Thread(target=load_task)
    load_thread.start()

def on_soundbank_change(*args):
    selected_soundbank = soundbank_var.get()
    load_sounds_async(selected_soundbank)

def on_key_press(event):
    char = event.char.lower()
    if char in sounds:
        channel = pygame.mixer.find_channel(True)
        if channel:
            channel.play(sounds[char])
            print(f"Lejátszott hang: {char}")

# GUI inicializálása
root = tk.Tk()
root.title("Modern Jegyzettömb")

# Design elemek
background_color = "#282a36"
text_color = "#f8f8f2"
font_family = "Arial"
font_size = 12

root.configure(bg=background_color)

# Hangfájlok és mixer beállítása
pygame.mixer.init()
pygame.mixer.set_num_channels(15)
sounds = {}
default_volume = 0.5  # Alapértelmezett hangerőszint

# Soundbankok és hangerőszintek inicializálása
soundbank_volumes = {
    "ambient1": 0.6,
    "ambient2": 0.3,
    # További soundbankok és hangerőszintek...
}

# Hangbank választó
soundbank_var = tk.StringVar(root)
soundbanks = os.listdir('soundbanks')  # Feltételezve, hogy a hangbankok a "soundbanks" mappában vannak
soundbank_var.set(soundbanks[0])  # Alapértelmezett hangbank beállítása
soundbank_menu = tk.OptionMenu(root, soundbank_var, *soundbanks)
soundbank_menu.pack(padx=10, pady=10)
soundbank_var.trace("w", on_soundbank_change)

# Jegyzettömb
text = tk.Text(root, fg=text_color, bg=background_color, insertbackground=text_color, font=(font_family, font_size))
text.pack(expand=True, fill='both', padx=10, pady=10)

# Billentyűleütések figyelése
text.bind('<KeyPress>', on_key_press)

# Kezdeti hangbank betöltése
load_sounds_async(soundbanks[0])

# Az alkalmazás indítása
root.mainloop()
