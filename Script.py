import os
import shutil
from mutagen.easyid3 import EasyID3

def main():
    source_folder = "source_folder"
    destination_folder = "destination_folder"
    move_higher_quality_files(source_folder, destination_folder)

def move_higher_quality_files(source_folder, destination_folder):
    """
    This function moves higher quality files to the destination folder.
    """
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

def get_file_quality(filename):
    """
    This function returns the quality of the audio file based on its file extension.
    """
    if filename.endswith(".mp3"):
        return ".mp3"
    elif filename.endswith(".m4a"):
        return ".m4a"
    elif filename.endswith(".flac"):
        return ".flac"
    else:
        return None

def clean_song_name(song_name):
    """
    This function cleans up the song name by removing any special characters or whitespace.
    """
    return "".join(c for c in song_name if c.isalnum() or c in "._- ").rstrip()

if __name__ == "__main__":
    main()