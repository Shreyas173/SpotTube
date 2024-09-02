# SpotTube 🎵📥

SpotTube is a Python-based application that lets you download songs from your Spotify playlists by extracting audio from YouTube. With a user-friendly GUI built using Tkinter, SpotTube makes playlist downloading easy and efficient. 🚀

# Features ✨
- **Spotify Authentication**: Securely log in to your Spotify account to access your playlists. 🔒
- **Custom Download Directory**: Choose where to save your downloaded songs. 📁
- **Real-time Progress Tracking**: View live updates on download progress. 📊
- **Threaded Downloads**: Keeps the UI responsive while handling downloads in the background. 🔄
- **User-Friendly Interface**: Simple and intuitive design. 🖥️
- **Spotify Developer Credentials Input**: Enter and securely store your Spotify Client ID and Client Secret. 🛡️

# Getting Started 🚀
1. **Set Up Spotify Developer Credentials**:
   - Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/create). 🌐
   - Log in and create a new app to obtain your Client ID and Client Secret. 🆔
2. **Download FFMPEG**:
   - Install [FFMPEG](https://ffmpeg.org/download.html) and provide the correct path in the script. 📥

# How It Works 🔧
- **Authentication**: Input your Spotify API credentials to gain access to playlists. 🔑
- **Playlist Retrieval**: Enter the Spotify playlist URL to get song details. 🎶
- **YouTube Search & Download**: yt-dlp searches YouTube for each song and downloads the best audio. 🎥
- **MP3 Conversion**: Converts downloaded audio to MP3 format using FFMPEG. 🎧

# Repository Contents 📦
- **Code**: Includes the full source code for SpotTube. 💻
- **Executable**: Pre-built executable file for Windows to run SpotTube without needing Python installed. 🏆

# Requirements 📋
- Python 3.x 🐍
- Spotipy 📦
- yt-dlp 📥
- FFMPEG 🎥

# Notes 📝
- The application is available as both source code and a pre-built executable. Use the executable for immediate use without Python installation. ⚙️
- Spotify credentials are required only during the initial setup. 🔐

#Feel free to contribute, open issues, or suggest features! 🛠️💬
