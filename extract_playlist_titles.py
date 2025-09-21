#!/usr/bin/env python3
"""
Extract and print titles of all videos in a YouTube playlist using yt-dlp only.

Usage:
  - Run without args and paste the playlist URL when prompted, or
  - Pass the playlist URL as a command-line argument.

Output format:
  video 1 :- "Video Title"
  video 2 :- "Video Title"
"""

import sys
from typing import List

try:
    import yt_dlp
except Exception:
    yt_dlp = None


def fetch_titles_with_ytdlp(playlist_url: str) -> List[str]:
    titles: List[str] = []
    if yt_dlp is None:
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
    except Exception:
        pass
    return titles


def main() -> None:
    # Accept URL via CLI arg or interactive prompt
    if len(sys.argv) > 1:
        playlist_url = " ".join(sys.argv[1:]).strip()
    else:
        try:
            playlist_url = input("Enter the YouTube playlist URL: ").strip()
        except EOFError:
            print("No input received.")
            sys.exit(1)

    if not playlist_url:
        print("Playlist URL cannot be empty.")
        sys.exit(1)

    titles = fetch_titles_with_ytdlp(playlist_url)
    if not titles:
        print("No videos found or unable to fetch titles.")
        sys.exit(0)

    for index, title in enumerate(titles, start=1):
        print(f'video {index} :- "{title}"')


if __name__ == "__main__":
    main()


