"""
Core functionality for YouTube Downloader.
"""

import os
import subprocess
from typing import List, Dict, Optional, Tuple, Union

from pytube import YouTube
from pytube.exceptions import PytubeError


def get_available_resolutions(yt: YouTube) -> List[Dict[str, Union[str, int]]]:
    """
    Get available resolutions for the YouTube video.
    
    Args:
        yt: YouTube object
        
    Returns:
        List of dictionaries containing resolution information
    """
    streams = yt.streams.filter(progressive=True, file_extension="mp4")
    resolutions = []
    
    for stream in streams:
        resolutions.append({
            "itag": stream.itag,
            "resolution": stream.resolution,
            "fps": stream.fps
        })
    
    return resolutions


def download_mp4(yt: YouTube, resolution: str, output_path: str) -> Tuple[bool, Optional[str]]:
    """
    Download YouTube video in MP4 format with specified resolution.
    
    Args:
        yt: YouTube object
        resolution: Desired video resolution (e.g., "720p")
        output_path: Directory to save the file
        
    Returns:
        Tuple of (success, filename or error message)
    """
    try:
        # Get streams with progressive=True (audio and video in one file)
        streams = yt.streams.filter(progressive=True, file_extension="mp4")
        
        # Find the stream with the requested resolution
        target_stream = None
        for stream in streams:
            if stream.resolution == resolution:
                target_stream = stream
                break
        
        if not target_stream:
            available_resolutions = [s.resolution for s in streams]
            return False, f"Resolution {resolution} not available. Available resolutions: {', '.join(available_resolutions)}"
        
        # Download the video
        output_file = target_stream.download(output_path=output_path)
        
        # Rename file to include resolution
        base, ext = os.path.splitext(output_file)
        new_filename = f"{base}_{resolution}{ext}"
        os.rename(output_file, new_filename)
        
        return True, new_filename
        
    except PytubeError as e:
        return False, f"Error downloading video: {e}"


def download_mp3(yt: YouTube, output_path: str) -> Tuple[bool, Optional[str]]:
    """
    Download YouTube video and convert to MP3 audio.
    
    Args:
        yt: YouTube object
        output_path: Directory to save the file
        
    Returns:
        Tuple of (success, filename or error message)
    """
    try:
        # Get the highest quality audio stream
        stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        
        if not stream:
            return False, "No audio stream found."
        
        # Download the audio
        temp_file = stream.download(output_path=output_path)
        
        # Convert to MP3 using ffmpeg
        base, _ = os.path.splitext(temp_file)
        mp3_file = f"{base}.mp3"
        
        try:
            subprocess.run(
                ["ffmpeg", "-i", temp_file, "-vn", "-ab", "128k", "-ar", "44100", "-y", mp3_file],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
            # Remove the temporary file
            os.remove(temp_file)
            return True, mp3_file
        except subprocess.CalledProcessError:
            return False, "Error: FFmpeg conversion failed. Make sure FFmpeg is installed correctly."
        except FileNotFoundError:
            return False, "Error: FFmpeg not found. Please install FFmpeg and make sure it's in your PATH."
            
    except PytubeError as e:
        return False, f"Error downloading audio: {e}"


def validate_youtube_url(url: str) -> bool:
    """
    Validate if the URL is a YouTube URL.
    
    Args:
        url: URL to validate
        
    Returns:
        True if valid YouTube URL, False otherwise
    """
    try:
        if "youtube.com" in url or "youtu.be" in url:
            yt = YouTube(url)
            return True
        return False
    except:
        return False
