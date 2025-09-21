import streamlit as st
from typing import List, Optional, Dict

try:
    import yt_dlp
except Exception:
    yt_dlp = None  # Provided by Poetry dependency; handled at runtime


def _format_duration(seconds: Optional[int]) -> str:
    if seconds is None or seconds < 0:
        return ""
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def fetch_video_entries(playlist_url: str, include_duration: bool) -> List[Dict[str, Optional[str]]]:
    entries_out: List[Dict[str, Optional[str]]] = []

    if yt_dlp is None:
        st.error("yt-dlp is not installed. Please run 'poetry install' to install dependencies.")
        return entries_out

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        # If duration requested, do full metadata extraction (slower)
        "extract_flat": not include_duration,
        "noplaylist": False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(playlist_url, download=False)
            entries = info.get("entries", []) if isinstance(info, dict) else []
            for entry in entries:
                if not isinstance(entry, dict):
                    continue
                title = entry.get("title")
                if include_duration:
                    dur_seconds = entry.get("duration")
                    duration_str = _format_duration(dur_seconds) if isinstance(dur_seconds, int) else ""
                else:
                    duration_str = ""
                if title:
                    entries_out.append({"title": title, "duration": duration_str})
    except Exception as exc:
        st.error(f"Failed to fetch titles: {exc}")

    return entries_out


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

include_duration = st.checkbox("Include video length (might take extra time)", value=False)

# No direct mutation of st.session_state["playlist_url"] after widget instantiation

if fetch_clicked:
    if not playlist_url:
        st.warning("Please enter a valid YouTube playlist URL.")
    else:
        with st.spinner("Fetching video titles..."):
            entries = fetch_video_entries(playlist_url, include_duration=include_duration)
        if not entries:
            st.info("No videos found or unable to fetch titles.")
        else:
            st.success(f"Found {len(entries)} videos.")
            # Copy/Download utilities (shown first, no list above)
            lines: List[str] = []
            for i, item in enumerate(entries, start=1):
                t = item.get("title", "")
                d = item.get("duration") or ""
                lines.append(f'video {i} :- "{t}"{f" ({d})" if d else ""}')
            output_text = "\n".join(lines)
            st.subheader("Copy or Download")
            st.text_area(
                "Copy or Download",
                value=output_text,
                height=420,
                key="copy_download_text",
                label_visibility="collapsed",
            )
            st.caption("Tip: Click inside the box and press Ctrl+A to select only this text.")
            st.download_button(
                label="Download as text",
                data=output_text,
                file_name="playlist_titles.txt",
                mime="text/plain",
            )


