# YouTube Playlist Titles (Streamlit + Poetry)

Extract and display video titles from a YouTube playlist using Streamlit, managed with Poetry.

## Requirements
- Python >=3.9 (excluding 3.9.7), <3.13
- Poetry

## Install
```bash
poetry install
```

## Run
```bash
poetry run streamlit run yt_app/app.py
```

Paste a YouTube playlist URL and click "Fetch Video Titles".

## Notes
- Large playlists may take time due to rate limiting.
- Unreachable titles are shown as "Unavailable video".
 - If `pytube` fails to fetch titles, the app falls back to `yt-dlp` metadata extraction.
