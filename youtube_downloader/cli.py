#!/usr/bin/env python3
"""
Command-line interface for YouTube Downloader.
"""

import os
import sys
import argparse
from pytube import YouTube
from pytube.exceptions import PytubeError

from youtube_downloader.downloader import (
    get_available_resolutions,
    download_mp4,
    download_mp3
)


def main():
    """Main entry point for the CLI application."""
    parser = argparse.ArgumentParser(description="Download YouTube videos as MP3 or MP4")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("--format", choices=["mp3", "mp4"], default="mp4", help="Output format (mp3 or mp4)")
    parser.add_argument("--resolution", default="720p", help="Video resolution for MP4 (e.g., 360p, 480p, 720p, 1080p)")
    parser.add_argument("--output", "-o", default=".", help="Output directory")
    parser.add_argument("--list-resolutions", action="store_true", help="List available resolutions and exit")
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    try:
        # Create YouTube object
        yt = YouTube(args.url)
        
        # Just list available resolutions if requested
        if args.list_resolutions:
            print(f"Available resolutions for: {yt.title}")
            resolutions = get_available_resolutions(yt)
            for res in resolutions:
                print(f"Resolution: {res['resolution']}, FPS: {res['fps']}, itag: {res['itag']}")
            return
        
        # Download based on format choice
        if args.format == "mp3":
            print(f"Downloading audio for: {yt.title}")
            success, result = download_mp3(yt, args.output)
            if success:
                print(f"Converted to MP3: {result}")
            else:
                print(result)  # Error message
        else:  # mp4
            print(f"Downloading: {yt.title} ({args.resolution})")
            success, result = download_mp4(yt, args.resolution, args.output)
            if success:
                print(f"Downloaded to: {result}")
            else:
                print(result)  # Error message
            
    except PytubeError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
