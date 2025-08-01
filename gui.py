import json
import os
import random
import tkinter as tk
from tkinter import messagebox, simpledialog

FILENAME = "song_list.json"
file_path = os.path.expanduser("song_list.json")

moods = {
    1: "happy",
    2: "sad",
    3: "relaxed",
    4: "energetic",
    5: "romantic",
    6: "angry"
}

def save_songs(filename, songs):
    try:
        with open(filename, "w") as f:
            json.dump(songs, f, indent=4)
    except Exception as e:
        messagebox.showerror("Save Error", f"Error saving {filename}: {e}")

def load_songs(filename):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return {mood: [] for mood in moods.values()}
    except Exception as e:
        messagebox.showerror("Load Error", f"Error loading {filename}: {e}")
        return {mood: [] for mood in moods.values()}

def song_exists(song_list, new_song):
    new_title = new_song['title'].strip().lower()
    new_artist = new_song['artist'].strip().lower()
    return any(
        s['title'].strip().lower() == new_title and s['artist'].strip().lower() == new_artist
        for s in song_list
    )

class MoodifyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Moodify")
        self.geometry("400x300")
        self.songs = load_songs(file_path)

        tk.Label(self, text="Welcome to Moodify!", font=("Helvetica", 16)).pack(pady=10)

        tk.Button(self, text="Select Mood (Play Random Song)", command=self.select_mood).pack(fill='x', padx=20, pady=5)
        tk.Button(self, text="Add New Songs", command=self.add_song).pack(fill='x', padx=20, pady=5)
        tk.Button(self, text="List Songs by Mood", command=self.list_songs).pack(fill='x', padx=20, pady=5)
        tk.Button(self, text="Delete a Song", command=self.delete_song).pack(fill='x', padx=20, pady=5)
        tk.Button(self, text="Exit", command=self.destroy).pack(fill='x', padx=20, pady=5)

    def select_mood(self):
        mood = self.ask_mood("Select mood to play a random song")
        if mood:
            mood_songs = self.songs[mood]
            if not mood_songs:
                messagebox.showinfo("No songs", f"No songs in the '{mood}' mood yet.")
                return
            song = random.choice(mood_songs)
            messagebox.showinfo("Random Song",
                f"Here's a random {mood} song:\n\n{song['title']} by {song['artist']}")

    def add_song(self):
        mood = self.ask_mood("Select mood to add a new song")
        if not mood:
            return

        title = simpledialog.askstring("Song Title", "Enter the title of the new song:")
        if not title or not title.strip():
            messagebox.showwarning("Input Error", "Title cannot be empty.")
            return

        artist = simpledialog.askstring("Artist", "Enter the artist of the new song:")
        if not artist or not artist.strip():
            messagebox.showwarning("Input Error", "Artist cannot be empty.")
            return

        song = {"title": title.strip(), "artist": artist.strip()}
        if song_exists(self.songs[mood], song):
            messagebox.showinfo("Duplicate", "This song already exists in that category.")
            return

        self.songs[mood].append(song)
        save_songs(file_path, self.songs)
        messagebox.showinfo("Song Added", f"Added '{title}' by {artist} to {mood} songs.")

    def list_songs(self):
        mood = self.ask_mood("Select mood to list songs from")
        if not mood:
            return
        mood_songs = self.songs[mood]
        if not mood_songs:
            messagebox.showinfo("No songs", f"No songs in the '{mood}' category.")
            return

        song_list = "\n".join(f"{i+1}. {s['title']} by {s['artist']}" for i, s in enumerate(mood_songs))
        messagebox.showinfo(f"Songs in {mood.capitalize()} Mood",
                            f"{song_list}\n\nTotal songs: {len(mood_songs)}")

    def delete_song(self):
        mood = self.ask_mood("Select mood to delete a song from")
        if not mood:
            return

        mood_songs = self.songs[mood]
        if not mood_songs:
            messagebox.showinfo("No songs", f"No songs in the '{mood}' category to delete.")
            return

        del_win = tk.Toplevel(self)
        del_win.title(f"Delete Song from {mood.capitalize()}")
        del_win.geometry("350x300")

        tk.Label(del_win, text=f"Songs in '{mood}' mood:", font=("Helvetica", 14)).pack(pady=10)

        listbox = tk.Listbox(del_win, width=40, height=10)
        for song in mood_songs:
            listbox.insert(tk.END, f"{song['title']} by {song['artist']}")
        listbox.pack(pady=5)

        def delete_selected():
            sel = listbox.curselection()
            if not sel:
                messagebox.showwarning("No selection", "Please select a song to delete.")
                return
            idx = sel[0]
            song = mood_songs[idx]
            confirm = messagebox.askyesno("Confirm Delete",
                                          f"Are you sure you want to delete '{song['title']}' by {song['artist']}?")
            if confirm:
                mood_songs.pop(idx)
                save_songs(file_path, self.songs)
                listbox.delete(idx)
                messagebox.showinfo("Deleted", f"Deleted '{song['title']}' by {song['artist']}.")
                if not mood_songs:
                    del_win.destroy()

        tk.Button(del_win, text="Delete Selected Song", command=delete_selected).pack(pady=10)
        tk.Button(del_win, text="Close", command=del_win.destroy).pack()

    def ask_mood(self, prompt):
        mood_win = tk.Toplevel(self)
        mood_win.title(prompt)
        mood_win.geometry("300x300")
        mood_win.grab_set()  # make modal

        var = tk.StringVar(value="")

        tk.Label(mood_win, text=prompt, font=("Helvetica", 12)).pack(pady=10)

        for key, mood in moods.items():
            tk.Radiobutton(mood_win, text=mood.capitalize(), variable=var, value=mood).pack(anchor='w', padx=20)

        selected = []

        def on_confirm():
            choice = var.get()
            if not choice:
                messagebox.showwarning("Selection Required", "Please select a mood.")
                return
            selected.append(choice)
            mood_win.destroy()

        tk.Button(mood_win, text="OK", command=on_confirm).pack(pady=15)
        self.wait_window(mood_win)

        return selected[0] if selected else None

if __name__ == "__main__":
    app = MoodifyApp()
    app.mainloop()
