import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import sys
import threading
import yt_dlp
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import re
import webbrowser
import requests
from urllib.parse import urlencode

credentials_file = "spotify_credentials.json"
ffmpeg = 'F:/Study/SpotTube/ffmpeg-2024-08-28-git-b730defd52-essentials_build/bin' #change accordingly & download from https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z
redirect_uri = 'http://localhost:8888/callback/'

def get_playlist_info(playlist_id):
    try:
        playlist = sp.playlist(playlist_id)
        playlist_name = playlist['name']
        tracks = [f"{item['track']['name']} {item['track']['artists'][0]['name']}" for item in playlist['tracks']['items']]
        return playlist_name, tracks
    except Exception as e:
        messagebox.showerror("Error", f"Failed to get playlist info: {e}")
        return None, []

def update_progress(message, progress=None):
    progress_label.config(text=message)
    if progress is not None:
        progress_bar['value'] = progress
    root.update_idletasks()

def download_song(song_name, download_folder):
    timeout = 120
    download_success = threading.Event()
    
    def progress_hook(d):
        if d['status'] == 'downloading':
            percent = d['downloaded_bytes'] / d['total_bytes'] * 100
            message = f"Downloading: {song_name} ({percent:.2f}%)"
            root.after(0, update_progress, message, percent)
        elif d['status'] == 'finished':
            download_success.set()
            root.after(0, update_progress, f"Downloaded: {song_name}")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
        'quiet': True,
        'progress_hooks': [progress_hook],
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': ffmpeg,
    }

    def download_with_timeout():
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([f"ytsearch:{song_name}"])
        except Exception as e:
            root.after(0, update_progress, f"Error downloading {song_name}: {e}")
    
    root.after(0, listbox.insert, tk.END, song_name)
    download_thread = threading.Thread(target=download_with_timeout)
    download_thread.start()
    download_thread.join(timeout)
    
    if not download_success.is_set():
        update_progress(f"Skipped: {song_name} (timeout)")

def download_playlist(playlist_id, download_folder):
    playlist_name, tracks = get_playlist_info(playlist_id)
    if not playlist_name:
        return

    playlist_folder = os.path.join(download_folder, playlist_name)
    
    if not os.path.exists(playlist_folder):
        os.makedirs(playlist_folder)
    
    for track in tracks:
        download_song(track, playlist_folder)
    
    root.after(0, update_progress, "All songs downloaded!")

def extract_playlist_id(url):
    match = re.search(r'playlist/([a-zA-Z0-9]+)', url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid playlist URL")

def start_download():
    playlist_url = url_entry.get()
    
    download_folder = filedialog.askdirectory(title="Select Download Folder")
    
    if not download_folder:
        messagebox.showwarning("Warning", "No download folder selected. Download canceled.")
        return
    
    try:
        playlist_id = extract_playlist_id(playlist_url)
        progress_bar.pack(pady=10)
        threading.Thread(target=download_playlist, args=(playlist_id, download_folder), daemon=True).start()
        update_progress("Download started...",0)
    except ValueError as e:
        messagebox.showerror("Error", str(e))

def authenticate_spotify():
    if os.path.exists(credentials_file):
        with open(credentials_file, 'r') as f:
            credentials = json.load(f)
        client_id = credentials.get('client_id')
        client_secret = credentials.get('client_secret')
    else:
        credentials_popup()
        return
    
    try:
        global sp
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                       client_secret=client_secret,
                                                       redirect_uri=redirect_uri,
                                                       scope='playlist-read-private',
                                                       cache_path=".spotify_cache"))
        start_button.config(state=tk.NORMAL)
        messagebox.showinfo("Success", "Spotify API authenticated successfully!")
        root.deiconify()
    except spotipy.SpotifyException as e:
        messagebox.showerror("Error", f"Failed to authenticate Spotify API: {e}")
        credentials_popup()

def center_window(window, width, height):
    # Get the screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    # Calculate position
    x_position = (screen_width - width) // 2
    y_position = (screen_height - height) // 2
    
    # Set the window size and position
    window.geometry(f'{width}x{height}+{x_position}+{y_position}')

def show_info():
    # Create a new top-level window for instructions
    info_window = tk.Toplevel(root)
    info_window.title("How to Get Client ID and Client Secret")

    # Set dimensions for the info window
    info_width = 600
    info_height = 400
    center_window(info_window, info_width, info_height)

    # Create a Text widget with a hyperlink
    text_widget = tk.Text(info_window, wrap='word', height=10, width=50, padx=10, pady=10)
    text_widget.pack(expand=True, fill='both')

    # Instructions with a placeholder for the clickable link
    instructions = (
        "Set Up Spotify Developer Credentials:\n"
        "1. Go to the Spotify Developer Dashboard:\n"
        "2. Log in to your Spotify account and create a new app. Note down your Client ID and Client Secret."
    )
    text_widget.insert(tk.END, instructions)
    
    # Insert the clickable link
    link = "https://developer.spotify.com/dashboard/create"
    text_widget.insert(tk.END, f" {link}", "link")
    
    # Configure the link tag
    text_widget.tag_configure("link", foreground="blue", underline=1)
    
    # Bind the link tag to the click event
    text_widget.tag_bind("link", "<Button-1>", lambda e: webbrowser.open(link))

    # Disable editing in the text widget
    text_widget.config(state=tk.DISABLED)

    # Add a Close button
    tk.Button(info_window, text="Close", command=info_window.destroy).pack(pady=10)


def credentials_popup():
    popup = tk.Toplevel(root)
    popup.title("Enter Spotify Credentials")

    # Set dimensions for the popup window
    popup_width = 400
    popup_height = 250
    center_window(popup, popup_width, popup_height)

    # Create a frame for the title and question mark icon
    title_frame = tk.Frame(popup)
    title_frame.pack(pady=10)

    # Add the title label
    title_label = tk.Label(title_frame, text="Click here for help -> ")
    title_label.pack(side=tk.LEFT)

    # Add the question mark icon
    question_icon = tk.Label(title_frame, text="?", font=("Arial", 12, "bold"), fg="blue", cursor="hand2")
    question_icon.pack(side=tk.LEFT, padx=10)
    question_icon.bind("<Button-1>", lambda e: show_info())

    tk.Label(popup, text="Enter Spotify Client ID:").pack(pady=10)
    client_id_entry = tk.Entry(popup, width=50)
    client_id_entry.pack(pady=5)

    tk.Label(popup, text="Enter Spotify Client Secret:").pack(pady=10)
    client_secret_entry = tk.Entry(popup, width=50, show='*')
    client_secret_entry.pack(pady=5)

    def verify_credentials(client_id, client_secret):
        try:
            sp_test = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                                client_secret=client_secret,
                                                                redirect_uri=redirect_uri,
                                                                scope='playlist-read-private'))
            sp_test.current_user()
            return True
        except Exception:
            return False

    def save_credentials():
        client_id = client_id_entry.get()
        client_secret = client_secret_entry.get()

        if not client_id or not client_secret:
            messagebox.showerror("Error", "Client ID and Client Secret cannot be empty.")
            return

        if not verify_credentials(client_id, client_secret):
            messagebox.showerror("Error", "Invalid Client ID or Client Secret. Please try again.")
            return

        with open(credentials_file, 'w') as f:
            json.dump({"client_id": client_id, "client_secret": client_secret}, f)

        popup.destroy()
        authenticate_spotify()

    tk.Button(popup, text="Save", command=save_credentials).pack(pady=10)


root = tk.Tk()
root.withdraw()

root.title("Spotify Playlist Downloader")

window_width = 600
window_height = 500

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

root.geometry(f'{window_width}x{window_height}+{x_position}+{y_position}')

tk.Label(root, text="Enter Spotify Playlist URL:").pack(pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

progress_bar = ttk.Progressbar(root, orient='horizontal', length=500, mode='determinate')

start_button = tk.Button(root, text="Download Playlist", command=start_download)
start_button.pack(pady=10)
start_button.config(state=tk.DISABLED)

progress_label = tk.Label(root, text="")
progress_label.pack(pady=5)


frame = tk.Frame(root)
frame.pack(pady=10)
listbox = tk.Listbox(frame, width=80, height=15)
scrollbar = tk.Scrollbar(frame, orient="vertical", command=listbox.yview)
listbox.config(yscrollcommand=scrollbar.set)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

authenticate_spotify()

root.mainloop()

