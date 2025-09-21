#!/usr/bin/env python3
"""
Extract and print titles of all videos in a YouTube playlist.

Usage:
  - Run without args and paste the playlist URL when prompted, or
  - Pass the playlist URL as a command-line argument.

Output format:
  video 1 :- "Video Title"
  video 2 :- "Video Title"
"""

import sys


def main() -> None:
    try:
        from pytube import Playlist, YouTube
    except Exception:
        print(
            "Error: Missing dependency 'pytube'. Install it with:\n"
            "  pip install -r requirements.txt\n"
            "or:\n"
            "  pip install pytube"
        )
        sys.exit(1)

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

    # Create Playlist object
    try:
        playlist = Playlist(playlist_url)
    except Exception as exc:
        print(f"Failed to load playlist: {exc}")
        sys.exit(1)

    # Try to get YouTube objects from the playlist
    try:
        videos = list(playlist.videos)
    except Exception:
        videos = []

    # Fallback: build YouTube objects from URLs
    if not videos:
        try:
            video_urls = list(getattr(playlist, "video_urls", []))
        except Exception:
            video_urls = []
        for url in video_urls:
            try:
                videos.append(YouTube(url))
            except Exception:
                # Skip videos we can't load
                continue

    if not videos:
        print("No videos found in the playlist.")
        sys.exit(0)

    # Print titles in requested format
    for index, video in enumerate(videos, start=1):
        title: str | None = None
        try:
            title = video.title
        except Exception:
            # Best-effort fallback using watch URL
            watch_url = getattr(video, "watch_url", None)
            if watch_url:
                try:
                    title = YouTube(watch_url).title
                except Exception:
                    title = None

        if not title:
            title = "Unavailable video"

        print(f'video {index} :- "{title}"')


if __name__ == "__main__":
    main()


