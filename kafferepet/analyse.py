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


def load_json_files(file_path, limit=None):
    jsons = {}
    files = sorted(list(file_path.glob(f"*{TRANSCRIPT_LEVEL}.json")))
    for i, file in enumerate(files, start=1):
        print(f"({i}/{len(files)}) Loading {file.name}")
        json_file = load_json(file)
        jsons[file.stem.replace(TRANSCRIPT_LEVEL, "")] = json_file
        if limit and i == limit:
            break
    return jsons


def sanitize(word):
    return word.lower().strip().translate(str.maketrans("", "", ",_-.!?"))


def find_segments(jsons, phrases):
    print("Finding segments...")
    result = {}
    for i, (name, transcript) in enumerate(jsons.items(), start=1):
        print(f"({i}/{len(jsons)}) Finding segments: {name}")

        timesamps = []
        for phrase in phrases:
            for segment in transcript["segments"]:
                if sanitize(phrase) in sanitize(segment["text"]):
                    keyword = phrase.split()

                    for idx, word in enumerate(segment["words"]):
                        if sanitize(keyword[0]) == sanitize(word["word"]) and idx + len(
                            keyword
                        ) <= len(segment["words"]):
                            start_idx = idx

                            if all(
                                sanitize(keyword[j])
                                == sanitize(segment["words"][start_idx + j]["word"])
                                for j in range(len(keyword))
                            ):
                                start_ts = segment["words"][start_idx]["start"]
                                end_ts = segment["words"][start_idx + len(keyword) - 1][
                                    "end"
                                ]
                                timesamps.append({"start": start_ts, "end": end_ts})
                            break

        result[name] = timesamps
    return result


def merge_timestamps(segments, threshold=0.5):
    print("Merging timestamps...")

    for i, (name, timestamps) in enumerate(segments.items(), start=1):
        print(f"({i}/{len(segments)}) Merging: {name}")

        # Sort timestamps by start time
        timestamps.sort(key=lambda x: x["start"])

        merged = []
        for timestamp in timestamps:
            if not merged or merged[-1]["end"] + threshold < timestamp["start"]:
                merged.append(timestamp)
            else:
                merged[-1]["end"] = max(merged[-1]["end"], timestamp["end"])
        segments[name] = merged

    return segments


def process_audio_immediately(
    segments,
    file_name,
    start_padding=0.1,
    end_padding=0.1,
    crossfade=0.1,
):
    print("Processing audio...")
    concatenated_audio = AudioSegment.empty()

    for i, (name, timestamps) in enumerate(segments.items(), start=1):
        print(f"({i}/{len(segments)}) Processing audio: {name}")

        if not timestamps:
            print(f"\tNo timestamps found for {name}. Skipping...")
            continue

        audio_path = download_folder / (name + ".mp3")
        if not audio_path.is_file():
            print(f"\tAudio file not found: {audio_path}")
            continue

        print(f"\tLoading audio: {audio_path}")
        audio = AudioSegment.from_file(audio_path)

        for idx, timestamp in enumerate(timestamps, start=1):
            print(f"\tSegment: ({idx}/{len(timestamps)})")
            start_ms = max(0, int((timestamp["start"] - start_padding) * 1000))
            end_ms = int((timestamp["end"] + end_padding) * 1000)
            assert start_ms < len(
                audio
            ), f"Start time {start_ms} exceeds audio length {len(audio)}"
            assert end_ms <= len(
                audio
            ), f"End time {end_ms} exceeds audio length {len(audio)}"
            segment = audio[start_ms:end_ms]
            segment = segment.pan((1 if idx % 2 == 0 else -1) * 0.7)

            if concatenated_audio:
                if crossfade > 0:
                    if crossfade > len(segment):
                        crossfade = len(segment) / 2
                    concatenated_audio = concatenated_audio.append(
                        segment, crossfade=crossfade * 1000
                    )
                else:
                    concatenated_audio = concatenated_audio.append(
                        segment, crossfade=len(segment) / 2
                    )
            else:
                concatenated_audio += segment

    out_file = f"{file_name}.mp3"
    print(f"Exporting {out_file}")
    concatenated_audio.export(download_folder.parent / out_file, format="mp3")


if __name__ == "__main__":
    download_folder = Path(__file__).parent / "downloads"
    TRANSCRIPT_LEVEL = "_large-v3-turbo_5"

    avista_keywords = [
        "av vista",
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

    avista_keywords = [
        "stol",
        "trappa",
        "blå",
        "kuk",
        "bra",
        "tack",
        "va",
        "inte de",
        "fisk",
        "hemma",
        "Halmstad",
        "Gud",
        "trädet",
        "krogen",
        "Full",
        "vetelängd",
        "älskar",
    ]

    jsons = load_json_files(download_folder, limit=None)

    avista_segments = find_segments(jsons, avista_keywords)
    avista_segments = merge_timestamps(avista_segments, threshold=0.5)

    jsons.clear()

    start_padding = 0.1
    end_padding = 0.1
    process_audio_immediately(avista_segments, "random", start_padding, end_padding, -1)
    # process_audio_immediately(avista_segments, "avista", start_padding,end_padding, (start_padding + end_padding) / 2)
    # process_audio_immediately(avista_segments, "avista_cross", start_padding, end_padding, -1)
    # process_audio_immediately(avista_segments, "avista_no_padd", 0, 0, -1)
