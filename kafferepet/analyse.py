from pathlib import Path
import json
from pydub import AudioSegment


def file_exists(filepath: Path) -> Path:
    if not filepath.is_file() and not filepath.is_dir():
        raise FileNotFoundError(f"Cannot find file: {filepath}")
    return filepath


def validate_path_length(filepath: Path) -> Path:
    # On windows paths with more than 256 characters are not allowed.
    if not len(str(filepath)) < 256:
        raise ValueError(
            f"Path too long, {len(filepath)} characters (Max: 256) {filepath}"
        )
    return filepath


def load_json(json_file_path):
    file_exists(validate_path_length(json_file_path))
    with open(json_file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path, file):
    validate_path_length(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(file, f, indent=4, sort_keys=False, ensure_ascii=False)


def load_json_files(file_path):
    jsons = {}
    files = sorted(list(file_path.glob(f"*{TRANSCRIPT_LEVEL}.json")))
    for i, file in enumerate(files, start=1):
        print(f"({i}/{len(files)}) Loading {file.name}")
        json_file = load_json(file)
        jsons[file.stem.replace(TRANSCRIPT_LEVEL, "")] = {
            "transcript": json_file,
            "audio_path": str(
                file_path / (file.stem.replace(TRANSCRIPT_LEVEL, "") + ".mp3")
            ),
        }
    return jsons


def sanitize(word):
    return word.lower().strip().translate(str.maketrans("", "", ",_-.!?"))


def find_segments(transcript, keywords, limit=None):
    print("Finding segments...")
    for i, (file, content) in enumerate(transcript.items(), start=1):
        print(f"({i}/{len(transcript)}) Loading {file}")
        transcript[file]["timestamps"] = {}
        for phrase in keywords:
            for segment in content["transcript"]["segments"]:
                text = sanitize(segment["text"])
                if phrase.lower() in text:
                    keyword = phrase.split()
                    first_word_index = [
                        idx
                        for idx, word in enumerate(segment["words"])
                        if sanitize(word["word"]) == sanitize(keyword[0])
                    ]

                    for idx in first_word_index:
                        if idx + len(keyword) <= len(segment["words"]):
                            if all(
                                sanitize(segment["words"][idx + i]["word"])
                                == sanitize(keyword[i])
                                for i in range(len(keyword))
                            ):
                                if phrase not in transcript[file]["timestamps"]:
                                    transcript[file]["timestamps"][phrase] = []
                                transcript[file]["timestamps"][phrase].append(
                                    {
                                        "start": segment["words"][idx]["start"],
                                        "end": segment["words"][idx + len(keyword) - 1][
                                            "end"
                                        ],
                                    }
                                )

        if limit and i == limit:
            break

    return transcript


def merge_timestamps(result):
    print("Merging timestamps...")

    for i, (file, content) in enumerate(result.items(), start=1):
        if "timestamps" not in content:
            continue
        print(f"({i}/{len(result)}) Flattening: {file}")
        all_timestamps = []
        for phrase, timestamps in content["timestamps"].items():
            all_timestamps.extend(timestamps)
        result[file]["timestamps"]["all_timestamps"] = all_timestamps

    for i, (file, content) in enumerate(result.items()):
        if "timestamps" not in content:
            continue
        print(f"({i}/{len(result)}) Merging: {file}")
        all_timestamps = []
        for phrase, timestamps in content["timestamps"].items():
            all_timestamps.extend(timestamps)

        # Sort timestamps by start time
        all_timestamps.sort(key=lambda x: x["start"])

        # Merge overlapping or adjacent timestamps within a threshold
        merged_timestamps = []
        threshold = 0.5
        for timestamp in all_timestamps:
            if (
                not merged_timestamps
                or merged_timestamps[-1]["end"] + threshold < timestamp["start"]
            ):
                merged_timestamps.append(timestamp)
            else:

                merged_timestamps[-1]["end"] = max(
                    merged_timestamps[-1]["end"], timestamp["end"]
                )

        result[file]["timestamps"]["all_timestamps"] = merged_timestamps
        result[file]["timestamps"]["total_count"] = len(merged_timestamps)
        result[file]["audio_path"] = str(download_folder / (file + ".mp3"))

    for file in result:
        result[file]["transcript"] =[]

    write_json(f"statistics.json", result)
    return result


def audio(result, start_padding=0.1, end_padding=0.1):
    concatenated_audio = AudioSegment.empty()
    for i, (key, data) in enumerate(result.items(), start=1):
        print(f"Processing ({i}/{len(result)}) {key}")
        audio_path = Path(data["audio_path"])
        if not audio_path.is_file():
            print(f"\tAudio file not found: {audio_path}")
            continue
        if "timestamps" not in data or "all_timestamps" not in data["timestamps"]:
            print(f"\tNo timestamps found for {key}")
            continue
        audio = AudioSegment.from_file(audio_path)

        for idx, timestamp in enumerate(data["timestamps"]["all_timestamps"], start=1):
            print(f"\tSegment: ({idx}/{len(data['timestamps']['all_timestamps'])})")
            start_ms = max(0, int((timestamp["start"] - start_padding) * 1000))
            end_ms = int((timestamp["end"] + end_padding) * 1000)
            segment = audio[start_ms:end_ms]
            concatenated_audio += segment

    print(f"Exporting concatenated audio")
    concatenated_audio.export(
        download_folder.parent / f"concatenated2.mp3", format="mp3"
    )


if __name__ == "__main__":
    download_folder = Path(__file__).parent / "downloads"
    TRANSCRIPT_LEVEL = "_large-v3-turbo_5"

    avista_keywords = [
        "vista",
        "avista",
        "prima",
        "aprim",
        "aprima",
        "prima vista",
        "aprima vista",
        "aprima avista",
        "a vista",
        "a prima avista",
        "a prima a vista",
        "a primaa avista",
        "Allvista",
        "All prima vista",
        "All prima avista",
        "first time ever",
        "for the first time ever",
        "the first time ever",
    ]
    jsons = load_json_files(download_folder)
    avista_segments = find_segments(jsons, avista_keywords)
    result = merge_timestamps(avista_segments)
    audio(result, 0.0, 0.0)
