# SpotTube
This Python-based application allows users to download songs from their Spotify playlists by searching and extracting audio from YouTube. After authenticating with Spotify using your own credentials, simply enter the Spotify playlist URL, choose a destination folder, and the app handles the rest. The application features a GUI built with Tkinter, a progress bar, and a list of downloaded tracks. It's designed to be user-friendly, with features like credential input prompts and customizable download directories.

Features:
Spotify Authentication: Users can authenticate with their Spotify account to access private playlists.
Custom Download Directory: Users can select the directory where the downloaded songs will be stored.
Progress Tracking: Real-time progress updates are displayed during the download process.
Threaded Downloads: Downloads are handled in a separate thread to keep the UI responsive.
User-Friendly GUI: Built using Tkinter, the application features a simple and intuitive interface.
Spotify Developer Credentials Input: Users can input their Spotify Client ID and Client Secret, which are securely stored and verified.

Getting Started:
Set Up Spotify Developer Credentials:
Go to the Spotify Developer Dashboard.
Log in to your Spotify account and create a new app to obtain your Client ID and Client Secret.
Download FFMPEG: Ensure you have FFMPEG installed and provide the correct path in the script.

Run the Application:
The application will prompt you to enter your Spotify credentials during the first run.
Once authenticated, enter the Spotify playlist URL and choose the download directory.
Click the download button and let the app handle the rest!

Requirements:
Python 3.x
Spotipy
yt-dlp
FFMPEG

How It Works:
Authentication: Upon launching the app, you'll be prompted to input your Spotify API credentials. If valid, the app will allow you to access and download playlists.
Playlist Retrieval: Enter the Spotify playlist URL, and the app retrieves the song information.
YouTube Search & Download: For each song, yt-dlp searches YouTube and downloads the best available audio.
MP3 Conversion: The downloaded files are converted to MP3 format using FFMPEG.

Notes:
The app is packaged as an executable file, so no Python installation is required to run it.
Spotify credentials are stored locally and are only required during the initial setup.
Feel free to contribute, open issues, or suggest features!
