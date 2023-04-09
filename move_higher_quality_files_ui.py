import os
import shutil
from mutagen.easyid3 import EasyID3
import tkinter as tk
from tkinter import filedialog


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Move Higher Quality Music Files")
        self.geometry("400x200")
        self.source_folder = tk.StringVar()
        self.destination_folder = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        # Source folder
        tk.Label(self, text="Source folder").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        tk.Entry(self, textvariable=self.source_folder, width=30).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self, text="Browse", command=self.browse_source_folder).grid(row=0, column=2, padx=10, pady=10)

        # Destination folder
        tk.Label(self, text="Destination folder").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        tk.Entry(self, textvariable=self.destination_folder, width=30).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(self, text="Browse", command=self.browse_destination_folder).grid(row=1, column=2, padx=10, pady=10)

        # Move files button
        tk.Button(self, text="Move Higher Quality Files", command=self.move_files).grid(row=2, column=1, padx=10, pady=10)

    def browse_source_folder(self):
        folder_path = filedialog.askdirectory()
        self.source_folder.set(folder_path)

    def browse_destination_folder(self):
        folder_path = filedialog.askdirectory()
        self.destination_folder.set(folder_path)

    def move_files(self):
        source_folder = self.source_folder.get()
        destination_folder = self.destination_folder.get()

        if source_folder and destination_folder:
            if os.path.exists(source_folder) and os.path.exists(destination_folder):
                move_higher_quality_files(source_folder, destination_folder)
                self.status_label.config(text="Files moved successfully!")
            else:
                self.status_label.config(text="Error: source and/or destination folder does not exist.")
        else:
            self.status_label.config(text="Error: source and/or destination folder not selected.")


def move_higher_quality_files(source_folder, destination_folder):
    """
    This function moves higher quality files to the destination folder.
    """
    print("Starting move_higher_quality_files...")
    files_to_move = {}
    for filename in os.listdir(source_folder):
        source_file = os.path.join(source_folder, filename)
        if os.path.isfile(source_file):
            source_quality = get_file_quality(source_file)
            print(f"Processing file: {filename} ({source_quality})")

            try:
                tags = EasyID3(source_file)
                song_name = tags['title'][0].strip()
            except Exception as e:
                print(f"Error getting metadata for {filename}: {e}")
                song_name, _ = os.path.splitext(filename)
                song_name = clean_song_name(song_name)
            else:
                song_name = clean_song_name(song_name)

            if song_name not in files_to_move.keys():
                files_to_move[song_name] = (source_file, source_quality)
                print(f"Adding {filename} ({source_quality}) to files to move")
            else:
                current_quality = files_to_move[song_name][1]
                if current_quality == ".mp3" and source_quality == ".flac":
                    print(f"Replacing {song_name}{current_quality} with {filename}{source_quality}")
                    files_to_move[song_name] = (source_file, source_quality)
                elif current_quality == ".m4a" and source_quality == ".flac":
                    print(f"Skipping {filename} ({source_quality}), already have higher quality .m4a version")
                elif current_quality == ".m4a" and source_quality == ".mp3":
                    print(f"Replacing {song_name}{current_quality} with {filename}{source_quality}")
                    files_to_move[song_name] = (source_file, source_quality)
                else:
                    print(f"Skipping {filename} ({source_quality}), already have higher quality version")

    for song_name, (source_file, source_quality) in files_to_move.items():
        destination_file = os.path.join(destination_folder, f"{song_name}{source_quality}")
        shutil.move(source_file, destination_file)
        print(f"Moved {song_name}{source_quality} to {destination_folder}")

    print("Finished move_higher_quality_files.")


def get_file_quality(file_path):
    """
    This function returns the quality of a file based on its extension.
    """
    _, extension = os.path.splitext(file_path)
    if extension in [".flac", ".wav"]:
        return extension
    elif extension == ".mp3":
        return extension
    elif extension == ".m4a":
        tags = EasyID3(file_path)
        if 'tool' in tags.keys() and 'Apple' in tags['tool'][0]:
            return ".m4a"
    else:
        return None


def clean_song_name(song_name):
    """
    This function cleans up the song name by removing any unwanted characters.
    """
    illegal_chars = ["\\", "/", ":", "*", "?", "\"", "<", ">", "|"]
    for char in illegal_chars:
        song_name = song_name.replace(char, "")
    return song_name.strip()


if __name__ == "__main__":
    app = App()
    app.mainloop()