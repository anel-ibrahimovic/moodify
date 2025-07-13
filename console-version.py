import json
import os
import random

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
        print(f"{filename} saved successfully.")
    except Exception as e:
        print(f"Error saving {filename}: {e}")

def load_songs(filename):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        print(f"Loaded data from {filename}.")
        return data
    except FileNotFoundError:
        print(f"No saved data found in {filename}. Creating new data.")
        return {
            "happy": [],
            "sad": [],
            "relaxed": [],
            "energetic": [],
            "romantic": [],
            "angry": []
        }
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return []

def print_mood_menu():
    print("Select one of the following moods:")
    print("----------------")
    for key, mood in moods.items():
        print(f"{key}. {mood.capitalize()}")
    print("----------------")

def mood_selection(songs):
    print_mood_menu()

    while True:
        mood_choice = input("Enter your choice (1-6): ")
        try:
            mood_choice = int(mood_choice)
        except ValueError:
            print("Invalid choice. Please write a number 1-6.")
            continue

        if mood_choice not in moods:
            print("Invalid choice. Please write a number 1-6")
            continue

        mood_key = moods[mood_choice]
        if not songs[mood_key]:
            print(f"No songs in the '{mood_key}' yet. Try adding one first.")
            return

        song = random.choice(songs[mood_key])
        print(f"\n{song['title']} by {song['artist']}\n")
        break

def song_exists(song_list, new_song):
    new_title = new_song['title'].strip().lower()
    new_artist = new_song['artist'].strip().lower()
    return any(
        s['title'].strip().lower() == new_title and s['artist'].strip().lower() == new_artist
        for s in song_list
    )

def add_songs(songs):
    print_mood_menu()

    while True:
        category_input = input("Enter your choice (1-6): ")
        try:
            category_input = int(category_input)
        except ValueError:
            print("Invalid choice. Please write a number 1-6.")
            continue

        if category_input not in moods:
            print("Invalid choice. Please write a number 1-6.")
            continue

        title_input = input("Enter the title of the new song: ").strip()
        if not title_input:
            print("Title cannot be empty.")
            return

        artist_input = input("Enter the artist: ").strip()
        if not artist_input:
            print("Artist cannot be empty.")
            return

        song = {"title": title_input, "artist": artist_input}

        mood_key = moods[category_input]

        if song_exists(songs[mood_key], song):
            print("This song already exists in that category.")
            return

        songs[mood_key].append(song)
        save_songs(file_path, songs)
        print(f"Added '{title_input}' by {artist_input} to {mood_key} songs.")
        break

def list_songs(songs):
    print_mood_menu()

    while True:
        category_input = input("Select a mood to list songs from (1-6): ")
        try:
            category_input = int(category_input)
        except ValueError:
            print("Invalid choice. Please write a number 1-6.")
            continue

        if category_input not in moods:
            print("Invalid choice. Please write a number 1-6.")
            continue

        mood_key = moods[category_input]
        mood_songs = songs[mood_key]

        if not mood_songs:
            print(f"No songs in the '{mood_key}' category.")
            return

        print(f"\nSongs in '{mood_key}' mood:")
        print("---------------------------")
        for i, song in enumerate(mood_songs, 1):
            print(f"{i}. {song['title']} by {song['artist']}")
        print(f"\nTotal songs in '{mood_key}': {len(mood_songs)}\n")
        break

def delete_song(songs):
    print_mood_menu()

    while True:
        category_input = input("Select a mood to delete a song from (1-6): ")
        try:
            category_input = int(category_input)
        except ValueError:
            print("Invalid choice. Please write a number 1-6.")
            continue

        if category_input not in moods:
            print("Invalid choice. Please write a number 1-6.")
            continue

        mood_key = moods[category_input]
        mood_songs = songs[mood_key]

        if not mood_songs:
            print(f"No songs in the '{mood_key}' category to delete.")
            return

        print(f"\nSongs in '{mood_key}' mood:")
        print("---------------------------")
        for i, song in enumerate(mood_songs, 1):
            print(f"{i}. {song['title']} by {song['artist']}")

        while True:
            delete_input = input(f"Enter the number of the song to delete (1-{len(mood_songs)}) or 'c' to cancel: ")
            if delete_input.lower() == 'c' or delete_input.strip() == '':
                print("Deletion cancelled.")
                return
            try:
                delete_choice = int(delete_input)
            except ValueError:
                print("Invalid input. Enter a number or 'c' to cancel.")
                continue

            if 1 <= delete_choice <= len(mood_songs):
                removed_song = mood_songs[delete_choice - 1]
                confirm = input(f"Are you sure you want to delete '{removed_song['title']}' by {removed_song['artist']}? (y/n): ").lower()
                if confirm == 'y':
                    mood_songs.pop(delete_choice - 1)
                    save_songs(file_path, songs)
                    print(f"Deleted '{removed_song['title']}' by {removed_song['artist']} from {mood_key} songs.")
                else:
                    print("Deletion cancelled.")
                return
            else:
                print(f"Invalid choice. Enter a number between 1 and {len(mood_songs)}.")

def main():
    songs = load_songs(file_path)
    if not songs:
        return

    while True:
        print("Welcome to Moodify!")
        print("----------------")
        print("Select one of the following options:")
        print("1. Select mood (play random song)")
        print("2. Add New Songs")
        print("3. List Songs by Mood")
        print("4. Delete a Song")
        print("5. Exit")
        print("----------------")
        choice = input("Enter your choice (1-5): ")

        try:
            choice = int(choice)
        except ValueError:
            print("Invalid choice. Please write a number 1-5.")
            continue

        if choice == 1:
            mood_selection(songs)
        elif choice == 2:
            add_songs(songs)
        elif choice == 3:
            list_songs(songs)
        elif choice == 4:
            delete_song(songs)
        elif choice == 5:
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please write a number 1-5.")

if __name__ == "__main__":
    main()
