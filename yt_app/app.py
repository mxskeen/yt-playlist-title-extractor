import streamlit as st
from typing import List

try:
    import yt_dlp
except Exception:
    yt_dlp = None  # Provided by Poetry dependency; handled at runtime


def fetch_video_titles(playlist_url: str) -> list[str]:
    titles: List[str] = []

    if yt_dlp is None:
        st.error("yt-dlp is not installed. Please run 'poetry install' to install dependencies.")
        return titles

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": True,
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
    except Exception as exc:
        st.error(f"Failed to fetch titles: {exc}")

    return titles


st.set_page_config(page_title="YT Playlist Titles", page_icon="🎬", layout="centered")
st.title("YouTube Playlist Video Titles Extractor")
st.caption("Enter a YouTube playlist URL to list all video titles.")

if "playlist_url" not in st.session_state:
    st.session_state["playlist_url"] = ""

def _clear_url() -> None:
    st.session_state["playlist_url"] = ""

playlist_url = st.text_input(
    "Enter YouTube Playlist URL",
    placeholder="https://www.youtube.com/playlist?list=...",
    key="playlist_url",
)

col1, col2 = st.columns([1, 1])
fetch_clicked = col1.button("Fetch Video Titles", type="primary")
clear_clicked = col2.button("Clear", on_click=_clear_url)

# No direct mutation of st.session_state["playlist_url"] after widget instantiation

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
            # Display as list
            for idx, title in enumerate(titles, start=1):
                st.write(f'video {idx} :- "{title}"')

            # Copy/Download utilities
            output_text = "\n".join([f'video {i} :- "{t}"' for i, t in enumerate(titles, start=1)])
            st.divider()
            st.subheader("Copy or Download")
            st.code(output_text, language=None)
            st.download_button(
                label="Download as text",
                data=output_text,
                file_name="playlist_titles.txt",
                mime="text/plain",
            )


