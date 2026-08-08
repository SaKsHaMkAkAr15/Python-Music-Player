import customtkinter as ctk
import pygame
import os

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Load songs
songs_folder = os.path.join(os.path.dirname(__file__), "songs")

# Create folder if it doesn't exist to prevent errors
if not os.path.exists(songs_folder):
    os.makedirs(songs_folder)

songs = [f for f in os.listdir(songs_folder) if f.endswith(".mp3")]
current_index = 0
is_playing = False
is_fullscreen = False

# App Setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("🎵 Music Player")
root.resizable(True, True) 

# Screen Size Adjustment
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 450
window_height = 600
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Top Bar (Header and Fullscreen Toggle)
top_frame = ctk.CTkFrame(root, fg_color="transparent")
top_frame.pack(fill="x", pady=(10, 0), padx=20)

header = ctk.CTkLabel(top_frame, text="🎵 Music Player", font=ctk.CTkFont(size=24, weight="bold"))
header.pack(side="left", expand=True, padx=(30, 0)) # Pad to keep it mostly centered

def toggle_fullscreen():
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    root.attributes("-fullscreen", is_fullscreen)
    
# fullscreen toggle button
fs_btn = ctk.CTkButton(top_frame, text="⛶", width=30, height=30, font=ctk.CTkFont(size=18), command=toggle_fullscreen)
fs_btn.pack(side="right")

# Song Label
song_label = ctk.CTkLabel(root, text="Select a song to play", font=ctk.CTkFont(size=13), wraplength=380, text_color="#a0aec0")
song_label.pack(pady=10)

# Album Art
art_frame = ctk.CTkFrame(root, width=180, height=180, corner_radius=20)
art_frame.pack(pady=10)
art_frame.pack_propagate(False)
art_label = ctk.CTkLabel(art_frame, text="🎵", font=ctk.CTkFont(size=60))
art_label.pack(expand=True)

# Control Buttons
btn_frame = ctk.CTkFrame(root, fg_color="transparent")
btn_frame.pack(pady=10)

prev_btn = ctk.CTkButton(btn_frame, text="⏮", width=60, height=60, corner_radius=30, font=ctk.CTkFont(size=20))
play_btn = ctk.CTkButton(btn_frame, text="▶", width=70, height=70, corner_radius=35, font=ctk.CTkFont(size=24))
next_btn = ctk.CTkButton(btn_frame, text="⏭", width=60, height=60, corner_radius=30, font=ctk.CTkFont(size=20))

prev_btn.grid(row=0, column=0, padx=10)
play_btn.grid(row=0, column=1, padx=10)
next_btn.grid(row=0, column=2, padx=10)

# Volume Slider
vol_frame = ctk.CTkFrame(root, fg_color="transparent")
vol_frame.pack(pady=10)

ctk.CTkLabel(vol_frame, text="🔊", font=ctk.CTkFont(size=14)).grid(row=0, column=0, padx=5)
volume_slider = ctk.CTkSlider(vol_frame, from_=0, to=100, width=250, command=lambda val: set_volume(val))
volume_slider.set(70)
volume_slider.grid(row=0, column=1, padx=5)
vol_label = ctk.CTkLabel(vol_frame, text="70%", font=ctk.CTkFont(size=12), text_color="#a0aec0")
vol_label.grid(row=0, column=2, padx=5)

# Playlist
ctk.CTkLabel(root, text="📋 Playlist", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)

# 3. Added fill="both" and expand=True so the playlist fills the screen when maximized
listbox_frame = ctk.CTkScrollableFrame(root, width=380, height=120)
listbox_frame.pack(pady=(5, 20), padx=20, fill="both", expand=True) 

# Functions
def play_song():
    global current_index, is_playing
    if not songs:
        return
    song_path = os.path.join(songs_folder, songs[current_index])
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(volume_slider.get() / 100)
    song_label.configure(text=f"Now Playing: {songs[current_index]}")
    play_btn.configure(text="⏸")
    is_playing = True

def toggle_play():
    global is_playing
    if not songs:
        return
    if is_playing:
        pygame.mixer.music.pause()
        play_btn.configure(text="▶")
        is_playing = False
    else:
        # Check if a song is loaded, if not play the first one
        if not pygame.mixer.music.get_busy() and current_index == 0:
            play_song()
        else:
            pygame.mixer.music.unpause()
            play_btn.configure(text="⏸")
            is_playing = True

def next_song():
    global current_index
    if songs:
        current_index = (current_index + 1) % len(songs)
        play_song()

def prev_song():
    global current_index
    if songs:
        current_index = (current_index - 1) % len(songs)
        play_song()

def set_volume(val):
    pygame.mixer.music.set_volume(float(val) / 100)
    vol_label.configure(text=f"{int(val)}%") 

def select_song(index):
    global current_index
    current_index = index
    play_song()

# Playlist Buttons
for i, song in enumerate(songs):
    btn = ctk.CTkButton(
        listbox_frame,
        text=f"🎵  {song}",
        anchor="w",
        fg_color="transparent",
        hover_color="#2d3748",
        font=ctk.CTkFont(size=12),
        command=lambda i=i: select_song(i)
    )
    btn.pack(fill="x", pady=2)

# Connect Buttons
play_btn.configure(command=toggle_play)
next_btn.configure(command=next_song)
prev_btn.configure(command=prev_song)

# Start
root.mainloop()