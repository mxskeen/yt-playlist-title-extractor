# YouTube Playlist Titles (Streamlit + Poetry)

Extract and display video titles from a YouTube playlist using Streamlit, managed with Poetry. Implemented using `yt-dlp`.

## Requirements
- Python >=3.9 (i used 3.12 in local)
- Poetry

## Install
```bash
poetry install
```

## Run
```bash
poetry run streamlit run yt_app/app.py
```

Paste a YouTube playlist URL and click "Fetch Video Titles". Use the "Copy or Download" section to copy all titles at once or download a `.txt` file.

## Notes
- Large playlists may take time due to rate limiting.
- Titles are fetched via `yt-dlp` metadata extraction.
