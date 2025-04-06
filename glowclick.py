import tkinter as tk
from tkinter import messagebox
from pynput import mouse, keyboard
import threading
import pyautogui
import time


pyautogui.FAILSAFE = False

click_loop_thread = None
click_loop_running = False
bind_key = None  

def toggle_click_loop():
    global click_loop_running, click_loop_thread, bind_key
    if bind_key is None:
        bind_key = ask_for_key()  
        if bind_key is None:
            messagebox.showwarning("Aucune touche liée", "Aucune touche n'a été sélectionnée pour l'activation.")
            return


    if click_loop_running:
        click_loop_running = False
        if click_loop_thread is not None and click_loop_thread.is_alive():
            click_loop_thread.join() 
        btn_click_loop.config(text="🔄 Démarrer le clic en boucle")
    else:
        click_loop_running = True
        click_loop_thread = threading.Thread(target=click_loop)
        click_loop_thread.start()
        btn_click_loop.config(text="⏹️ Stop clics en boucle")

def click_loop():
    interval = 1 / 30  
    while click_loop_running:
        pyautogui.click()  
        time.sleep(interval)  

def ask_for_key():
    global bind_key
    def on_key_press(key):
        global bind_key
        try:

            bind_key = key.char
            listener.stop()
        except AttributeError:
            bind_key = str(key)
            listener.stop()

    listener = keyboard.Listener(on_press=on_key_press)
    listener.start()

    messagebox.showinfo("Liaison de touche", "Veuillez appuyer sur une touche pour lier la boucle de clics.")
    listener.join()

    return bind_key

def on_press(key):
    global click_loop_running
    if hasattr(key, 'char') and key.char == bind_key:
        toggle_click_loop()
fenetre = tk.Tk()
fenetre.title("🎮 Macro Clic Automatique")
fenetre.geometry("250x150")

frame_btn = tk.Frame(fenetre)
frame_btn.pack(pady=30)
btn_click_loop = tk.Button(frame_btn, text="🔄 Démarrer le clic en boucle", command=toggle_click_loop)
btn_click_loop.pack()
label_footer = tk.Label(fenetre, text="by tr4x", font=("Arial", 8), fg="black", anchor="w")
label_footer.pack(side="left", padx=10, pady=5)
keyboard_listener = keyboard.Listener(on_press=on_press)
keyboard_listener.start()

fenetre.mainloop()
