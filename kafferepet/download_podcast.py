import feedparser
import requests
from pathlib import Path
import json
import socket
import time
import gc
import whisper

# Define the log file path
log_file_path = Path(__file__).parent / "application.log"


def log_message(message, duration=None):
    hostname = f"[{socket.gethostname()}]"
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    duration = f"{f' Took: {seconds_to_string(duration)}' if duration else ''}"
    with log_file_path.open("a", encoding="utf-8") as log_file:
        log_file.write(f"[{timestamp}] {hostname:<18} {message:<80}{duration}\n")


def seconds_to_string(input_seconds):
    result = ""
    min, seconds = divmod(input_seconds, 60)
    hours, min = divmod(min, 60)
    if hours > 0:
        result += f"{int(hours)}h:"
    if min > 0 or hours > 0:
        result += f"{int(min)}m:"

    result += f"{round(seconds,2)}s"
    return result


def download_podcast_episodes(rss_feed_url, download_folder):
    # Parse the RSS feed
    feed = feedparser.parse(rss_feed_url)

    # Create the download folder if it doesn't exist
    download_folder = Path(download_folder)
    download_folder.mkdir(parents=True, exist_ok=True)
    count = 0

    downloaded_files = []  # List to store file paths of downloaded episodes

    # Iterate through all episodes in the feed
    for index, entry in enumerate(reversed(feed.entries), start=1):
        # Skip episodes where the title starts with "Brända kakor"
        # Get the episode title and audio URL
        title = entry.title
        audio_url = entry.enclosures[0].href if entry.enclosures else None
        print(f"({index}/{len(feed.entries)}) Downloading: {title}")

        if title.lower().startswith("teaser"):
            print(f"Skipping: {title}")
            continue

        count += 1
        if not audio_url:
            print(f"No audio URL found for {title}. Skipping...")
            continue

        filename = (
            f"{count:03d}_{title}.mp3".replace("/", "-")
            .replace("\\", "-")
            .replace(" ", " ")
            # .replace("- ", "-")
            .replace(" - ", "-")
            .replace(" – ", "-")
            .replace("–", "-")
            .replace(". ", "_")
            .replace(" ", "_")
            .replace("?", "")
            .replace('"', "")
        )
        filepath = download_folder / filename

        # Add a temporary suffix while downloading
        temp_filepath = filepath.with_suffix(filepath.suffix + ".temp")

        if filepath.exists():
            print(f"Episode already downloaded: {filepath}")
            downloaded_files.append(filepath)  # Add existing file to the list
            continue

        log_message(f"Starting download:  ({index}/{len(feed.entries)}) {title}")
        start_time = time.time()

        temp_filepath.unlink(missing_ok=True)  # Remove any existing temp file
        response = requests.get(audio_url, stream=True)
        with temp_filepath.open("wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        # Rename the file to remove the temporary suffix after download
        temp_filepath.rename(filepath)

        duration = time.time() - start_time
        log_message(f"Completed download: {title}", duration=duration)
        print("Done!")

        downloaded_files.append(filepath)  # Add newly downloaded file to the list

    return downloaded_files  # Return the list of downloaded file paths


def transcribe_audio(filepaths):
    def transcribe(filepath):
        beam_size = 5
        model_name = "large-v3-turbo"  # Use a larger model for better accuracy
        transcription_file = (
            filepath.parent / f"{filepath.stem}_{model_name}_{beam_size}.json"
        )
        dummy_file = transcription_file.with_suffix(".json.temp")

        if dummy_file.exists():
            print(f"Transcription in progress or already started: {dummy_file}")
            return

        if transcription_file.exists():
            print(f"Episode already transcribed: {transcription_file}")
            return

        # Create a dummy file to indicate transcription is in progress
        dummy_file.touch()

        log_message(
            f"Starting transcription:  {filepath.name} {model_name} {beam_size}"
        )
        start_time = time.time()

        try:
            model = whisper.load_model(
                model_name
            )  # Use a larger model for better accuracy
            result = model.transcribe(
                str(filepath),
                language="sv",  # Specify the language explicitly
                verbose=False,
                word_timestamps=True,
                beam_size=beam_size,  # Increase beam size for better decoding
                best_of=beam_size,  # Consider more decoding paths for higher accuracy
            )
            duration = time.time() - start_time
            log_message(
                f"Completed transcription: {filepath.name} {model_name} {beam_size}",
                duration=duration,
            )

            result["duration"] = duration
            with transcription_file.open("w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=4)

            print(f"Transcription saved: {transcription_file}")
        finally:
            # Remove the dummy file after transcription is complete
            dummy_file.unlink(missing_ok=True)

    for index, filepath in enumerate(filepaths, start=1):
        print(f"Transscribing {filepath.name} ({index}/{len(filepaths)})")
        transcribe(filepath)


if __name__ == "__main__":
    # Example usage
    rss_feed_url = "https://feeds.acast.com/public/shows/kafferepet"
    download_folder = Path(__file__).parent / "downloads"
    downloaded_files = download_podcast_episodes(rss_feed_url, download_folder)
    transcribe_audio(downloaded_files)
