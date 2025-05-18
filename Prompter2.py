import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pyperclip
import json
import os
import time
from PIL import Image, ImageTk
from deep_translator import GoogleTranslator

import sys
import os

if getattr(sys, 'frozen', False):
    # PyInstaller .exe
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Standard .py
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE = os.path.join(BASE_DIR, "data", "config.json")
LANG_DIR = os.path.join(BASE_DIR, "data", "lang")




def show_splash(image_path=os.path.join(BASE_DIR, "data", "splash.png"), delay=3000):
    try:
        print(f"Loading splash: {image_path}")
        splash = tk.Tk()
        splash.overrideredirect(True)
        splash.geometry("640x480+{}+{}".format(
            (splash.winfo_screenwidth() - 640) // 2,
            (splash.winfo_screenheight() - 480) // 2))
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Splash not found: {image_path}")
        image = Image.open(image_path)
        splash_img = ImageTk.PhotoImage(image)
        panel = tk.Label(splash, image=splash_img, bg="black")
        panel.image = splash_img
        panel.pack()
        splash.after(delay, splash.destroy)
        splash.mainloop()
    except Exception as e:
        with open("error.log", "w", encoding="utf-8") as log:
            log.write(f"Failed to load splash screen: {e}\\n")


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"language": "en"}


def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f)


class PrompterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.config_data = load_config()
        self.current_lang = self.config_data.get("language", "en")
        self.translations = self.load_language(self.current_lang)

        self.title("Prompter 2 By Damizon")
        self.geometry("1350x780")
        self.resizable(False, False)

        self.field_keys = [
            "main_subject",
            "style_genre",
            "medium_technique",
            "realism_quality",
            "composition",
            "background",
            "lighting_mood",
            "colors_palette"
        ]
        self.text_boxes = {}
        self.labels_refs = []

        self._create_widgets()

    def load_language(self, lang_code):
        try:
            path = os.path.join(LANG_DIR, f"{lang_code}.py")
            data = {}
            with open(path, "r", encoding="utf-8") as f:
                exec(f.read(), data)
            return {
                "labels": data["labels"],
                "help_text": data["help_text"],
                "about": data["about"]
            }
        except Exception as e:
            messagebox.showerror("Language Error", str(e))
            return {"labels": {}, "help_text": "", "about": ""}

    def _create_widgets(self):
        top_frame = tk.Frame(self)
        top_frame.pack(fill=tk.X, padx=10, pady=5)

        help_btn = tk.Button(top_frame, text="?", width=3, command=self.show_help)
        help_btn.pack(side=tk.RIGHT, padx=5)

        langs = ["en", "cn", "de", "es", "fr", "it", "pl", "pt", "ua"]
        self.lang_var = tk.StringVar(value=self.current_lang)
        lang_menu = ttk.OptionMenu(top_frame, self.lang_var, self.current_lang, *langs, command=self.change_language)
        lang_menu.pack(side=tk.RIGHT)


        container = tk.Frame(self)
        container.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(container)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas)

        self.scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._create_main_fields()

        self.result_label = tk.Label(self, text=self.translations["labels"]["translated_prompt"])
        self.result_label.pack(anchor="w", padx=10, pady=(5, 0))
        self.result_txt = tk.Text(self, height=8, wrap="word")
        self.result_txt.pack(fill=tk.BOTH, padx=10, pady=(0, 10), expand=False)

        btn_frame = tk.Frame(self)
        btn_frame.pack(fill=tk.X, pady=10)

        self.generate_btn = tk.Button(btn_frame, text=self.translations["labels"]["generate_prompt"], command=self._on_ok)
        self.generate_btn.pack(side=tk.LEFT, padx=5)

        self.save_btn = tk.Button(btn_frame, text=self.translations["labels"]["save_txt"], command=self._save_to_file)
        self.save_btn.pack(side=tk.LEFT, padx=5)

        self.plus_btn = tk.Button(btn_frame, text=self.translations["labels"]["weight_plus"], command=lambda: self._wrap_weight(0.1))
        self.plus_btn.pack(side=tk.RIGHT, padx=5)

        self.minus_btn = tk.Button(btn_frame, text=self.translations["labels"]["weight_minus"], command=lambda: self._wrap_weight(-0.1))
        self.minus_btn.pack(side=tk.RIGHT, padx=0)

        
        self.weight_label = tk.Label(btn_frame, text=self.translations["labels"]["adjust_weight"])
        self.weight_label.pack(side=tk.RIGHT, padx=5)
        

    def _clear_main_fields(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.text_boxes.clear()
        self.labels_refs.clear()

    def _create_main_fields(self):
        for i in range(0, len(self.field_keys), 2):
            row_frame = tk.Frame(self.scroll_frame)
            row_frame.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)
            for key in self.field_keys[i:i + 2]:
                frame = tk.Frame(row_frame)
                frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
                lbl = tk.Label(frame, text=self.translations["labels"].get(key, key))
                lbl.pack(anchor="w")
                txt = tk.Text(frame, height=6, wrap="word")
                txt.pack(fill=tk.BOTH, expand=True)
                self.text_boxes[key] = txt
                self.labels_refs.append((lbl, key))

    def change_language(self, new_lang):
        self.translations = self.load_language(new_lang)
        self.config_data["language"] = new_lang
        save_config(self.config_data)

        self._clear_main_fields()
        self._create_main_fields()

        self.generate_btn.config(text=self.translations["labels"]["generate_prompt"])
        self.save_btn.config(text=self.translations["labels"]["save_txt"])
        self.result_label.config(text=self.translations["labels"]["translated_prompt"])
        self.weight_label.config(text=self.translations["labels"]["adjust_weight"])
        self.plus_btn.config(text=self.translations["labels"]["weight_plus"])
        self.minus_btn.config(text=self.translations["labels"]["weight_minus"])

    def show_help(self):
        win = tk.Toplevel(self)
        win.title(self.translations["labels"]["help"])
        win.resizable(False, False)  # wyłącza skalowanie
        win.attributes('-toolwindow', True)  # usuwa min/max

        text = tk.Text(win, wrap="word", height=25, width=80)
        text.insert(tk.END, self.translations["help_text"])
        text.pack(padx=10, pady=10)
        text.config(state=tk.DISABLED)


    def _wrap_weight(self, delta):
        widget = self.focus_get()
        if not isinstance(widget, tk.Text):
            return
        try:
            start = widget.index("sel.first")
            end = widget.index("sel.last")
        except tk.TclError:
            return
        selected = widget.get(start, end)
        import re
        m = re.match(r"^\((.*?):([0-9]+\.?[0-9]*)\)$", selected)
        if m:
            text = m.group(1)
            weight = float(m.group(2))
        else:
            text = selected
            weight = 1.0
        new_weight = round(max(0.1, min(weight + delta, 10.0)), 1)
        new = f"({text}:{new_weight})"
        widget.delete(start, end)
        widget.insert(start, new)
        end_index = f"{start} + {len(new)} chars"
        widget.tag_add(tk.SEL, start, end_index)
        widget.see(start)

    def _on_ok(self):
        contents = [txt.get("1.0", tk.END).strip() for txt in self.text_boxes.values() if txt.get("1.0", tk.END).strip()]
        raw_prompt = ", ".join(contents)

        try:
            translated = GoogleTranslator(source='auto', target='en').translate(raw_prompt)
        except Exception as e:
            messagebox.showerror("Translation Error", str(e))
            return

        try:
            pyperclip.copy(translated)
            messagebox.showinfo("Success", "Translated prompt copied to clipboard!")
        except Exception:
            messagebox.showwarning("Warning", "Failed to copy to clipboard.")

        self.result_txt.delete("1.0", tk.END)
        self.result_txt.insert(tk.END, translated)

    def _save_to_file(self):
        content = self.result_txt.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Empty", "There is no prompt to save.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not path:
            return
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            messagebox.showinfo("Saved", f"Prompt saved as {path}")
        except Exception as e:
            messagebox.showerror("Save Error", str(e))


if __name__ == '__main__':
    show_splash()
    try:
        app = PrompterApp()
        app.mainloop()
    except Exception as e:
        with open("error.log", "w", encoding="utf-8") as f:
            f.write(f"APP CRASH: {e}\\n")


        import tkinter as tk
        tk.Tk().withdraw()
        tk.messagebox.showerror("Fatal Error", str(e))
