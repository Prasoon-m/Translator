import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image      # pip install pillow
from deep_translator import GoogleTranslator  # pip install deep-translator

# --- Setup Main Window ---
root = tk.Tk()
root.title('Modern Language Translator')
root.geometry('600x450')
root.resizable(False, False)
root.config(bg='#F0F8FF') # Light Alice Blue Background

# --- Fetch Languages (Name -> Code Mapping) ---
# We get the supported languages as a dictionary: {'afrikaans': 'af', ...}
try:
    translator_engine = GoogleTranslator(source='auto', target='en')
    langs_dict = translator_engine.get_supported_languages(as_dict=True)
    # Create a list of names for the dropdown (Capitalized)
    language_names = [lang.title() for lang in langs_dict.keys()]
except Exception as e:
    messagebox.showerror("Connection Error", "Please check your internet connection to load languages.")
    langs_dict = {}
    language_names = []

# --- Functions ---
def translate():
    input_text = source_text.get("1.0", "end-1c")
    target_lang_name = choose_language.get().lower() # Get name (e.g. "French")
    
    if not input_text.strip():
        messagebox.showwarning('Warning', 'Please enter text to translate.')
        return

    if not target_lang_name:
        messagebox.showwarning('Warning', 'Please select a target language.')
        return

    # Convert Name back to Code (e.g., "french" -> "fr")
    target_lang_code = langs_dict.get(target_lang_name)

    if not target_lang_code:
         messagebox.showerror('Error', 'Invalid Language Selected')
         return

    # Update Status
    status_label.config(text="Translating...", fg="orange")
    root.update()

    try:
        # Perform Translation
        translator = GoogleTranslator(source='auto', target=target_lang_code)
        output = translator.translate(input_text)
        
        # Display Output
        dest_text.delete(1.0, 'end')
        dest_text.insert('end', output)
        status_label.config(text="Translation Complete", fg="green")
        
    except Exception as e:
        status_label.config(text="Error", fg="red")
        messagebox.showerror('Translation Failed', f'Error: {e}')

def clear():
    source_text.delete(1.0, 'end')
    dest_text.delete(1.0, 'end')
    status_label.config(text="")

# --- GUI Layout ---

# 1. Header Section
header_frame = tk.Frame(root, bg='#F0F8FF')
header_frame.pack(pady=10)

# Try to load image, skip if not found
try:
    # Resizing image to fit better
    original_img = Image.open('translator.png')
    resized_img = original_img.resize((50, 50)) 
    img = ImageTk.PhotoImage(resized_img)
    img_label = tk.Label(header_frame, image=img, bg='#F0F8FF')
    img_label.pack(side=tk.LEFT, padx=10)
except Exception:
    pass # If image is missing, just skip it

title_label = tk.Label(header_frame, text="Language Translator", font=('Helvetica', 20, 'bold'), bg='#F0F8FF', fg='#333')
title_label.pack(side=tk.LEFT)

# 2. Main Content Area
content_frame = tk.Frame(root, bg='#F0F8FF')
content_frame.pack(pady=10)

# --- Left Side (Source) ---
left_frame = tk.Frame(content_frame, bg='#F0F8FF')
left_frame.pack(side=tk.LEFT, padx=20)

tk.Label(left_frame, text="Auto Detect", font=('Arial', 10, 'bold'), bg='#F0F8FF', fg='#555').pack(anchor=tk.W)
source_text = tk.Text(left_frame, width=30, height=10, borderwidth=2, relief=tk.GROOVE, font=('Arial', 11))
source_text.pack(pady=5)

# --- Right Side (Target) ---
right_frame = tk.Frame(content_frame, bg='#F0F8FF')
right_frame.pack(side=tk.LEFT, padx=20)

tk.Label(right_frame, text="Select Target Language:", font=('Arial', 10, 'bold'), bg='#F0F8FF', fg='#555').pack(anchor=tk.W)

# Combobox with Names
choose_language = ttk.Combobox(right_frame, width=28, values=language_names, state='readonly', font=('Arial', 10))
choose_language.set("Select Language") # Placeholder
choose_language.pack(pady=0)

dest_text = tk.Text(right_frame, width=30, height=10, borderwidth=2, relief=tk.GROOVE, font=('Arial', 11), bg='#f9f9f9')
dest_text.pack(pady=5)

# 3. Footer / Buttons
button_frame = tk.Frame(root, bg='#F0F8FF')
button_frame.pack(pady=20)

translate_btn = tk.Button(button_frame, text="Translate", font=('Arial', 12, 'bold'), 
                          bg='#4CAF50', fg='white', activebackground='#45a049', 
                          cursor="hand2", padx=15, pady=5, borderwidth=0, command=translate)
translate_btn.pack(side=tk.LEFT, padx=10)

clear_btn = tk.Button(button_frame, text="Clear", font=('Arial', 12, 'bold'), 
                      bg='#f44336', fg='white', activebackground='#d32f2f', 
                      cursor="hand2", padx=15, pady=5, borderwidth=0, command=clear)
clear_btn.pack(side=tk.LEFT, padx=10)

# 4. Status Bar
status_label = tk.Label(root, text="", bg='#F0F8FF', font=('Arial', 9, 'italic'))
status_label.pack(side=tk.BOTTOM, pady=5)

root.mainloop()