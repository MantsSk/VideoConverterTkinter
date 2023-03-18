import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from pathlib import Path
from PIL import ImageTk
import ffmpeg
import threading
from tkinter.messagebox import showinfo


root = tk.Tk()

root.title("Video Converter")
root.resizable(False, False)
root.geometry(f"600x400")
root.configure(background='#FEF6E9')

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.rowconfigure(5, weight=4)

bg_colour = "#3d6466"
format_list = ["mp3", "mp4", "mkv", "avi", "mov"]
selected_video = ""

def select_video_dialog():
    selected_video_path = filedialog.askopenfilename(initialdir="", title="Select a video")
    selected_video_label.configure(text=selected_video_path)

def select_output_path(output_format):
    output_path = filedialog.asksaveasfilename(defaultextension=output_format)
    return output_path

def file_already_exists(output_path):
    if Path(output_path).exists():
        messagebox.showerror("Error", "File already exists")
        return True
    return False

def toggle_ui_elements(converting):
    if converting:
        progress_bar.start()
        convert_btn['state'] = "disabled"
        project_btn['state'] = "disabled"
        format_combobox['state'] = "disabled"
    else:
        format_combobox['state'] = "normal"
        convert_btn['state'] = "normal"
        project_btn['state'] = "normal"
        progress_bar.stop()
        showinfo(message='Video conversion was completed!')

def convert_video(video_path, output_format):
    toggle_ui_elements(True)
    try:
        if not video_path:
            raise ValueError("No video selected")
        video_ext = Path(video_path).suffix.lower()
        if video_ext not in ['.mp4', '.avi', '.mkv']:
            raise ValueError("Not a valid video file")
        output_path = select_output_path(output_format)
        if file_already_exists(output_path):
            raise ValueError("File already exists")
        new_file = output_path
        ffmpeg.input(video_path).output(new_file).run()
    except Exception as e:
        error_msg = str(e)
        messagebox.showerror("Error", error_msg)
    toggle_ui_elements(False)


def convert_button_command():
    video_path = selected_video_label.cget("text")
    output_format = format_combobox.get()
    t = threading.Thread(target=convert_video, args=(video_path, output_format)).start()

logo_img = ImageTk.PhotoImage(file="logo.png")
logo_widget = tk.Label(root, image=logo_img, bg="#FEF6E9")
logo_widget.image = logo_img
logo_widget.grid(column=1, row=0,  sticky='nswe')

format_combobox = ttk.Combobox(values=format_list)
format_combobox.set("Pick a format")
format_combobox.grid(column=1, row=1, sticky='nswe', padx=5, pady=5)

project_btn = tk.Button(text="Select a video", command=select_video_dialog, highlightbackground="#FEF6E9")
project_btn.grid(column=1, row=2,  sticky='nswe', padx=5, pady=5)

selected_video_label = tk.Label(text="", bg="#FEF6E9")
selected_video_label.grid(column=1, row=3, sticky='nswe', padx=5, pady=5)

# style = ttk.Style.configure("bar.Horizontal.TProgressbar", troughcolor="FEF6E9",
#                 bordercolor="FEF6E9", background="FEF6E9", lightcolor="FEF6E9",
#                 darkcolor="FEF6E9")
s = ttk.Style()
s.theme_use('default')
s.configure("red.Horizontal.TProgressbar", bordercolor="#FEF6E9", darkcolor="#FEF6E9", lightcolor="#FEF6E9", foreground='#FEF6E9', background='#FEF6E9')
progress_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, mode='determinate', style="red.Horizontal.TProgressbar")
progress_bar.grid(column=1, row=6, sticky='nswe', padx=5, pady=5)

convert_btn = ttk.Button(text="CONVERT!", command=convert_button_command, highlightbackground="#FEF6E9")
convert_btn.grid(column=1, row=5,  sticky='swe', padx=5, pady=5)

root.mainloop()
