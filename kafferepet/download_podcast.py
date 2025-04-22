import feedparser
import requests
from pathlib import Path
import json
import whisper


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
        print(f"Downloading {title} ({index}/{len(feed.entries)})")

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
            .replace(". ", "_")
            .replace(" ", "_")
        )
        filepath = download_folder / filename

        # Add a temporary suffix while downloading
        temp_filepath = filepath.with_suffix(filepath.suffix + ".temp")

        if filepath.exists():
            print(f"Episode already downloaded: {filepath}")
            downloaded_files.append(filepath)  # Add existing file to the list
            continue

        temp_filepath.unlink(missing_ok=True)  # Remove any existing temp file
        response = requests.get(audio_url, stream=True)
        with temp_filepath.open("wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        # Rename the file to remove the temporary suffix after download
        temp_filepath.rename(filepath)
        print("Done!")

        downloaded_files.append(filepath)  # Add newly downloaded file to the list

    return downloaded_files  # Return the list of downloaded file paths


def transcribe_audio(filepaths):
    def transcribe(filepath):
        transcription_file = filepath.with_suffix(".json")
        dummy_file = transcription_file.with_suffix(".json.temp")

        if dummy_file.exists():
            print(f"Transcription in progress or already started: {dummy_file}")
            return

        if transcription_file.exists():
            print(f"Episode already transcribed: {transcription_file}")
            return

        # Create a dummy file to indicate transcription is in progress
        dummy_file.touch()

        try:
            model = whisper.load_model(
                "large"
            )  # Use a larger model for better accuracy
            result = model.transcribe(
                str(filepath),
                language="sv",  # Specify the language explicitly
                verbose=False,
                word_timestamps=True,
                beam_size=5,  # Use beam search for better decoding
                best_of=5,  # Consider multiple decoding paths for higher accuracy
            )
            # Save transcription to a JSON file
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
    download_folder = Path(r"\\nas\DM\Work\Pegelow\kaffe\downloads")
    downloaded_files = download_podcast_episodes(rss_feed_url, download_folder)
    transcribe_audio(downloaded_files)
