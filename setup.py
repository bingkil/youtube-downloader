from setuptools import setup, find_packages

setup(
    name="youtube-downloader",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pytube>=12.1.0",
        "streamlit>=1.21.0",
    ],
    entry_points={
        "console_scripts": [
            "youtube-downloader=youtube_downloader.cli:main",
            "youtube-downloader-app=youtube_downloader.app:main",
        ],
    },
    python_requires=">=3.7",
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool to download YouTube videos as MP3 or MP4",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/youtube-downloader",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
