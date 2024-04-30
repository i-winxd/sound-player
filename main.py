import os
import subprocess
import time
import tkinter as tk
import webbrowser
from tkinter import Label, Tk, filedialog
from tkinter.font import Font

import platform
import pygame


def balance_file_paths(path_to_file: str) -> str:
    current_os = platform.system()
    if current_os == 'Windows':
        return path_to_file.replace("/", "\\")
    else:
        return path_to_file.replace("\\", "/")


class MyApp:
    root: Tk
    label: Label
    path_to_sounds: str = ""
    current_files: list[str]
    listbox: tk.Listbox
    button1: tk.Button
    button2: tk.Button
    last_played: float = 0.0
    slider: tk.Scale
    volume: int = 70
    frame_items: tk.Frame
    scrollbar: tk.Scrollbar
    button_frame: tk.Frame

    def __init__(self, tk_root: Tk) -> None:
        pygame.mixer.init()
        self.root = tk_root
        self.root.geometry("600x450")
        header_font = Font(size=15, weight="bold")
        self.label = Label(tk_root, text="AUDIO PLAYER", font=header_font)
        self.label.pack()

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack()

        self.button1 = tk.Button(self.button_frame, text="Select Folder", command=self.select_folder)
        self.button1.grid(row=0, column=0, padx=5)

        self.button2 = tk.Button(self.button_frame, text="Open Selected", command=self.open_selected)
        self.button2.grid(row=0, column=1, padx=5)

        self.button3 = tk.Button(self.button_frame, text="Stop", command=self.stop_audio)
        self.button3.grid(row=0, column=2, padx=5)

        self.slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=self.update_volume)
        self.slider.set(self.volume)
        self.slider.pack()

        self.frame_items = tk.Frame(self.root)
        self.frame_items.pack()

        self.scrollbar = tk.Scrollbar(self.frame_items)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(self.frame_items, width=50, height=20, yscrollcommand=self.scrollbar.set)
        self.listbox.bind('<Up>', self.refocus_selection_up)
        self.listbox.bind('<Down>', self.refocus_selection_down)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)

    def open_selected(self) -> None:
        curselection = self.listbox.curselection()
        if curselection:
            index = curselection[0]
            selected_text = self.listbox.get(index)
            path_to_sound = os.path.realpath(os.path.join(self.path_to_sounds, selected_text))
            os_name = platform.system()
            if os_name == "Windows":
                print(path_to_sound)
                subprocess.run(f'explorer /select,"{path_to_sound}"')
            else:
                dir_path = os.path.dirname(path_to_sound)
                webbrowser.open('file://' + os.path.realpath(dir_path))

    def refocus_selection_up(self, _event: tk.Event) -> None:
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            look_ahead = 6
            visible_index = max(index - look_ahead, 0)
            self.listbox.see(visible_index)

    def refocus_selection_down(self, _event: tk.Event) -> None:
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            look_ahead = 6
            visible_index = min(index + look_ahead, self.current_files.__len__() - 1)
            self.listbox.see(visible_index)

    def update_volume(self, vol: str) -> None:
        self.volume = int(vol)
        pygame.mixer.music.set_volume(self.volume / 100)

    def select_folder(self) -> None:
        folder_selected = filedialog.askdirectory()
        if folder_selected != "" and folder_selected is not None:
            self.path_to_sounds = folder_selected
            self.load_sounds()

    def on_select(self, _event: tk.Event) -> None:
        curselection = self.listbox.curselection()
        if curselection:
            index = curselection[0]
            selected_text = self.listbox.get(index)
            # print(f"You selected item {index}: {selected_text}")
            path_to_sound = os.path.join(self.path_to_sounds, selected_text)
            self.play_sound(path_to_sound)

    def load_sounds(self) -> None:
        working_file_formats = [".mp3", ".ogg", ".wav"]
        self.current_files = [f for f in os.listdir(self.path_to_sounds)
                              if any(f.endswith(ext) for ext in working_file_formats)]
        self.listbox.delete(0, tk.END)
        for item in self.current_files:
            self.listbox.insert(tk.END, item)

    def play_sound(self, path_to_sound: str) -> None:
        # path_to_sound is the absolute path to the audio file
        pygame.mixer.music.stop()
        current_time = time.perf_counter()
        if current_time - self.last_played < 0.07:
            return
        self.last_played = current_time
        pygame.mixer.music.load(path_to_sound)
        pygame.mixer.music.set_volume(self.volume / 100)
        pygame.mixer.music.play()

    def stop_audio(self) -> None:
        pygame.mixer.music.stop()

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    root = Tk()
    app = MyApp(root)
    app.run()
