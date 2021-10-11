#!/usr/bin/env python3
import subprocess
import sys
import os
import math

def get_length(input_video):
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_video], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        return float(result.stdout)
    except Exception:
        print("Couldn't find file or it's duration.")
        sys.exit(2)

def split_with_ffmpeg(input_video, split_len, rewind, result_name):
    length = get_length(input_video)
    start = 0
    # number of clips
    num = int(math.ceil(length / split_len))
    # number of digits for naming clips
    digits = len(str(num))
    files = []
    for i in range(num):
        name  = result_name + '_' + str(i).zfill(digits) + os.path.splitext(input_video)[1]
        # set rewind
        if( i > 0 ):
            new_start = start - rewind
            new_split_len  = split_len + rewind
        else:
            new_start = start
            new_split_len = split_len

        print("\n\n\n\n" + str(new_start) + "\n\n\n\n")
        subprocess.run(['ffmpeg', '-i', input_video, '-ss', str(new_start), '-t', str(new_split_len), name])
        files.append(name)
        start = start + split_len

    subprocess.run(['zip', input_video + '.zip'] + files)
    subprocess.run(['rm'] + files)

if __name__ == "__main__":
    # Wrong number of arguments
    if(len(sys.argv) != 5):
        print("python visplit.py video_name split_len rewind_in_next_clip clip_name_without_extension")
        sys.exit(1)

    # Try spliting video
    try:
        split_with_ffmpeg(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
    except Exception:
        print("python visplit.py video_name split_len rewind_in_next_clip clip_name_without_extension")
