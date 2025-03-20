# YouTube Downloader

A simple, easy-to-use application to download YouTube videos as either MP3 audio or MP4 video with customizable resolution options.

![YouTube Downloader Screenshot](assets/screenshot.png)

## Features

- Download YouTube videos as MP3 audio or MP4 video
- Choose from available video resolutions
- Simple command-line interface
- User-friendly web interface powered by Streamlit
- Cross-platform compatibility (Windows, macOS, Linux)

## Installation

### Prerequisites

- Python 3.7 or higher
- FFmpeg (required for MP3 conversion)
  - **Windows**: 
    1. Download from the [official website](https://ffmpeg.org/download.html) (recommended: gyan.dev Windows builds, "Release Full")
    2. Extract the ZIP file to a permanent location (e.g., `C:\ffmpeg`)
    3. Add FFmpeg to your PATH:
       - Open the Start menu and search for "Edit the system environment variables"
       - Click "Environment Variables"
       - Under "System variables", find and select "Path", then click "Edit"
       - Click "New" and add the path to the bin folder (e.g., `C:\ffmpeg\bin`)
       - Click "OK" on all dialogs to save your changes
    4. Verify installation by opening a new Command Prompt window and typing `ffmpeg -version`
  - **macOS**: `brew install ffmpeg`
  - **Linux**: `sudo apt install ffmpeg` or equivalent for your distribution

### Option 1: Install from GitHub

```bash
# Clone the repository
git clone https://github.com/yourusername/youtube-downloader.git
cd youtube-downloader

# Install dependencies
pip install -e .
```

### Option 2: Install dependencies manually

```bash
# Clone the repository
git clone https://github.com/yourusername/youtube-downloader.git
cd youtube-downloader

# Install required packages
pip install -r requirements.txt
```

## Usage

### Command Line Interface

```bash
# List available resolutions for a video
python -m youtube_downloader.cli https://www.youtube.com/watch?v=EXAMPLE --list-resolutions

# Download a video as MP4 with 1080p resolution
python -m youtube_downloader.cli https://www.youtube.com/watch?v=EXAMPLE --format mp4 --resolution 1080p

# Download a video as MP3 audio
python -m youtube_downloader.cli https://www.youtube.com/watch?v=EXAMPLE --format mp3

# Save to a specific directory
python -m youtube_downloader.cli https://www.youtube.com/watch?v=EXAMPLE --output ~/Downloads
```

### Web Interface (Streamlit App)

```bash
# Start the Streamlit app
python -m youtube_downloader.app
```

Or if you installed with pip:

```bash
youtube-downloader-app
```

Then open your browser to the URL displayed in the terminal (typically http://localhost:8501).

## Legal Disclaimer

This tool is intended for personal use only. Please respect copyright laws and YouTube's Terms of Service. You should only download videos that you have permission to download, such as videos with Creative Commons licenses or your own videos.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [pytube](https://github.com/pytube/pytube) - The Python library that powers the downloading functionality
- [Streamlit](https://streamlit.io/) - The web framework used for the user interface
- [FFmpeg](https://ffmpeg.org/) - Used for audio conversion

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.