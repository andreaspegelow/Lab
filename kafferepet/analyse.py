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


download_folder = Path(__file__).parent / "downloads"
TRANSCRIPT_LEVEL = "_large-v3-turbo_5"


def find_segments():
    print("Finding segments...")
    result = {}
    files = list(download_folder.glob(f"*{TRANSCRIPT_LEVEL}.json"))
    for i, file in enumerate(files, start=1):
        print(f"({i}/{len(files)}) Loading {file.name}")
        json_file = load_json(file)

        keywords = [
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
            "a primaa avista",
            "Allvista",
            "All prima vista",
            "All prima avista",
            "first time ever",
        ]
        result[file.stem.replace(TRANSCRIPT_LEVEL, "")] = {}
        for phrase in keywords:
            result[file.stem.replace(TRANSCRIPT_LEVEL, "")][phrase] = []
            for segment in json_file.get("segments", []):
                text = (
                    segment.get("text", "")
                    .lower()
                    .strip()
                    .translate(str.maketrans("", "", ",_-.!?"))
                )
                if phrase.lower() in text:
                    keyword = phrase.split()
                    first_word_starts = [
                        (idx, word["start"])
                        for idx, word in enumerate(segment["words"])
                        if word["word"]
                        .lower()
                        .strip()
                        .translate(str.maketrans("", "", ",_-.!?"))
                        == keyword[0].lower().strip()
                    ]

                    for idx, start in first_word_starts:
                        if idx + len(keyword) <= len(segment["words"]):
                            if all(
                                segment["words"][idx + i]["word"]
                                .lower()
                                .strip()
                                .translate(str.maketrans("", "", ",_-.!?"))
                                == keyword[i].lower().strip()
                                for i in range(len(keyword))
                            ):
                                result[file.stem.replace(TRANSCRIPT_LEVEL, "")][
                                    phrase
                                ].append(
                                    {
                                        "start": segment["words"][idx]["start"],
                                        "end": segment["words"][idx + len(keyword) - 1][
                                            "end"
                                        ],
                                    }
                                )

        if i == 30:
            break
    result = dict(sorted(result.items()))
    return result


def merge_timestamps(result):
    print("Merging timestamps...")

    for i, (key, phrases) in enumerate(result.items(), start=1):
        print(f"({i}/{len(result)}) Loading {key}")
        all_timestamps = []
        for phrase, timestamps in phrases.items():
            all_timestamps.extend(timestamps)
        result[key]["all_timestamps"] = all_timestamps
    for key, phrases in result.items():
        all_timestamps = []
        for phrase, timestamps in phrases.items():
            all_timestamps.extend(timestamps)

        # Sort timestamps by start time
        all_timestamps.sort(key=lambda x: x["start"])

        # Merge overlapping or adjacent timestamps within a threshold
        merged_timestamps = []
        threshold = 0.1  # 0.1 seconds threshold for merging
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

        result[key]["all_timestamps"] = merged_timestamps
        result[key]["total_count"] = len(merged_timestamps)
        result[key]["audio_path"] = str(download_folder / (key + ".mp3"))

    write_json(f"statistics.json", result)
    return result


def audio(result):
    concatenated_audio = AudioSegment.empty()
    for i, (key, data) in enumerate(result.items(), start=1):
        print(f"Processing ({i}/{len(result)}) {key}")
        audio_path = Path(data["audio_path"])
        if not audio_path.is_file():
            print(f"Audio file not found: {audio_path}")
            continue
        if not data["all_timestamps"]:
            print(f"No timestamps found for {key}")
            continue
        audio = AudioSegment.from_file(audio_path)
        output_folder = download_folder / key
        output_folder.mkdir(parents=True, exist_ok=True)

        for idx, timestamp in enumerate(data["all_timestamps"], start=1):
            start_padding = 0.1
            end_padding = 0.1
            start_ms = max(0, int((timestamp["start"] - start_padding) * 1000))
            end_ms = int((timestamp["end"] + end_padding) * 1000)
            segment = audio[start_ms:end_ms]
            concatenated_audio += segment

    print(f"Exporting concatenated audio")
    concatenated_audio.export(download_folder.parent / f"concatenated.mp3", format="mp3")


segments = find_segments()
result = merge_timestamps(segments)
audio(result)
