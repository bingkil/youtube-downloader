#!/usr/bin/env python3
"""
Streamlit web interface for YouTube Downloader.
"""

import os
import tempfile
import time
import streamlit as st
from pytube import YouTube

from youtube_downloader.downloader import (
    get_available_resolutions,
    download_mp4,
    download_mp3,
    validate_youtube_url
)


def main():
    """Main entry point for the Streamlit application."""
    st.set_page_config(
        page_title="YouTube Downloader",
        page_icon="🎬",
        layout="centered"
    )
    
    st.title("YouTube Downloader")
    st.markdown("""
    Convert YouTube videos to MP3 audio or MP4 video with your preferred resolution.
    
    [![GitHub](https://img.shields.io/badge/GitHub-View_Source-lightgrey?logo=github&style=flat-square)](https://github.com/yourusername/youtube-downloader)
    """)
    
    # User input for YouTube URL
    youtube_url = st.text_input("Enter YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
    
    # Check if a valid URL was entered
    if youtube_url:
        if not validate_youtube_url(youtube_url):
            st.error("Please enter a valid YouTube URL")
        else:
            try:
                with st.spinner("Loading video information..."):
                    yt = YouTube(youtube_url)
                    
                    # Display video information
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.image(yt.thumbnail_url, use_column_width=True)
                    with col2:
                        st.subheader(yt.title)
                        st.write(f"Channel: {yt.author}")
                        st.write(f"Length: {yt.length // 60}m {yt.length % 60}s")
                        st.write(f"Views: {yt.views:,}")
                    
                    # Get available resolutions
                    resolutions = get_available_resolutions(yt)
                    resolution_options = [res["resolution"] for res in resolutions]
                    if not resolution_options:
                        resolution_options = ["720p"]  # Default if none found
                    
                    # Format selection
                    format_option = st.radio("Select Format", ["MP4 Video", "MP3 Audio"])
                    
                    # Resolution selection (only for MP4)
                    if format_option == "MP4 Video":
                        resolution = st.select_slider(
                            "Select Resolution",
                            options=sorted(resolution_options, key=lambda x: int(x.replace("p", ""))),
                            value=resolution_options[len(resolution_options)//2] if resolution_options else "720p"
                        )
                    
                    # Download button
                    if st.button("Download", type="primary"):
                        output_path = tempfile.mkdtemp()
                        
                        with st.spinner("Downloading..."):
                            progress_bar = st.progress(0)
                            
                            if format_option == "MP3 Audio":
                                success, result = download_mp3(yt, output_path)
                                file_type = "MP3 Audio"
                            else:  # MP4 Video
                                success, result = download_mp4(yt, resolution, output_path)
                                file_type = f"MP4 Video ({resolution})"
                            
                            # Simulate progress
                            for i in range(100):
                                time.sleep(0.01)
                                progress_bar.progress(i + 1)
                        
                        if success:
                            st.success(f"Download completed successfully!")
                            
                            # Create a download button for the file
                            with open(result, "rb") as file:
                                file_name = os.path.basename(result)
                                file_data = file.read()
                                st.download_button(
                                    label=f"Download {file_type}",
                                    data=file_data,
                                    file_name=file_name,
                                    mime="video/mp4" if format_option == "MP4 Video" else "audio/mp3"
                                )
                        else:
                            st.error(result)  # Display error message
                                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    
    # Instructions and requirements
    with st.expander("Requirements & Instructions"):
        st.markdown("""
        ### Requirements
        - **FFmpeg**: Required for MP3 conversion
            - **Windows**: Download from the official website and add to your PATH
            - **macOS**: `brew install ffmpeg`
            - **Linux**: `sudo apt install ffmpeg`
        
        ### Instructions
        1. Paste a YouTube URL in the text box
        2. Select MP3 or MP4 format
        3. For MP4, select your preferred resolution
        4. Click "Download"
        5. Once processing is complete, click the download button to save the file
        
        ### Legal Disclaimer
        This tool is intended for personal use only. Please respect copyright laws and YouTube's Terms of Service.
        You should only download videos that you have permission to download.
        """)


if __name__ == "__main__":
    main()
