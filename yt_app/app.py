import streamlit as st
from pytube import Playlist, YouTube
from typing import List

try:
    import yt_dlp
except Exception:
    yt_dlp = None  # Optional fallback; handled at runtime


def fetch_video_titles(playlist_url: str) -> list[str]:
    titles: List[str] = []
    try:
        playlist = Playlist(playlist_url)
    except Exception as exc:
        st.error(f"Failed to load playlist: {exc}")
        return titles

    # Try playlist.videos first, fallback to video_urls if needed
    video_objects = []
    try:
        video_objects = list(playlist.videos)
    except Exception:
        video_objects = []

    if not video_objects:
        try:
            for url in getattr(playlist, "video_urls", []):
                try:
                    video_objects.append(YouTube(url))
                except Exception:
                    continue
        except Exception:
            pass

    for video in video_objects:
        try:
            titles.append(video.title)
        except Exception:
            titles.append("Unavailable video")

    if titles:
        return titles

    # Fallback: use yt-dlp to extract playlist entries
    if yt_dlp is None:
        return titles

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": True,  # Faster, metadata only
        "noplaylist": False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(playlist_url, download=False)
            entries = info.get("entries", []) if isinstance(info, dict) else []
            for entry in entries:
                title = entry.get("title") if isinstance(entry, dict) else None
                if title:
                    titles.append(title)
    except Exception:
        # If yt-dlp also fails, return whatever we have
        pass

    return titles


st.set_page_config(page_title="YT Playlist Titles", page_icon="🎬", layout="centered")
st.title("YouTube Playlist Video Titles Extractor")
st.caption("Enter a YouTube playlist URL to list all video titles.")

playlist_url = st.text_input("Enter YouTube Playlist URL", placeholder="https://www.youtube.com/playlist?list=...")

col1, col2 = st.columns([1, 1])
fetch_clicked = col1.button("Fetch Video Titles", type="primary")
clear_clicked = col2.button("Clear")

if clear_clicked:
    st.session_state.clear()

if fetch_clicked:
    if not playlist_url:
        st.warning("Please enter a valid YouTube playlist URL.")
    else:
        with st.spinner("Fetching video titles..."):
            titles = fetch_video_titles(playlist_url)
        if not titles:
            st.info("No videos found or unable to fetch titles.")
        else:
            st.success(f"Found {len(titles)} videos.")
            for idx, title in enumerate(titles, start=1):
                st.write(f'video {idx} :- "{title}"')


