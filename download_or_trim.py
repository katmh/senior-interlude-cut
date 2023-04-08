import subprocess

# If true, will download songs into DOWNLOAD_DIR using yt-dl
SHOULD_DOWNLOAD = False
DOWNLOAD_DIR = "audio"

# If true, will trim songs from (start timestamp - PAD_START) to (end timestamp) and output into TRIM_DIR
SHOULD_TRIM = True
PAD_START = 5  # seconds
TRIM_DIR = "concat"

# Name, video link, start timestamp (minutes, seconds), end timestamp (minutes, seconds)
# Can be in arbitrary order
# Some songs have buffer manually added to end time
songs = [
    ("tt",      "https://www.youtube.com/watch?v=ePpPVE-GGJw",  (2, 26),    (3, 10+2)),
    ("hot",     "https://www.youtube.com/watch?v=gRnuFC4Ualw",  (2, 40),    (3, 17)),
    ("scars",   "https://www.youtube.com/watch?v=oUq2a6t258o",  (0, 48),    (1, 24+2)),
    ("akmu",    "https://www.youtube.com/watch?v=BydX3CHVPp8",  (1, 36),    (2, 8)),
    ("jiaren",  "https://www.bilibili.com/video/BV1DW4y1a7rm/", (0, 23),    (1, 1+2)),
    ("eight",   "https://www.youtube.com/watch?v=hWVDI4W15_4",  (0, 24),    (0, 56+2)),
    ("omg",     "https://www.youtube.com/watch?v=NzAYgldAaa0",  (2, 47),    (3, 32)),
    ("thanks",  "https://youtu.be/7xKwpPQiPGs",                 (3, 8),     (3, 49)),
]


def to_timestamp(tup):  # Input is (minutes, seconds) tuple
    min = tup[0]
    sec = tup[1]
    if len(str(sec)) == 1:
        sec = f"0{sec}"
    return f"{min}:{sec}"


if SHOULD_DOWNLOAD:
    for song in songs:
        name = song[0]
        video_link = song[1]

        # Thanks cut is pre-trimmed, Bilibili only sort of works with yt-dlp, so will manually do these
        if name.find("thanks") != -1 or video_link.find("bilibili") != -1:
            continue

        format = "-f bestaudio"
        cmd = f"yt-dlp {format} -o '{DOWNLOAD_DIR}/{name}.%(ext)s' '{video_link}' &"
        print(cmd)
        subprocess.run(cmd, shell=True)

if SHOULD_TRIM:
    for song in songs:
        name = song[0]
        if name.find("thanks") != -1:
            continue

        start = song[2]
        # WARNING: Breaks if start[1] is less than PAD_START
        start = (start[0], start[1] - PAD_START)

        end = song[3]
        cmd = f"ffmpeg -ss {to_timestamp(start)} -to {to_timestamp(end)} -i {DOWNLOAD_DIR}/{name}* {TRIM_DIR}/{name}.mp4 &"
        print(cmd)
        subprocess.run(cmd, shell=True)
