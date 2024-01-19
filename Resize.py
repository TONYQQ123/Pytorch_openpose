import ffmpeg
import subprocess
import argparse
import sys
from pathlib import Path
from typing import NamedTuple
import copy
import numpy as np
import cv2
from glob import glob
import os
import argparse
import json

parser = argparse.ArgumentParser(
        description="Process a video annotating poses detected.")
parser.add_argument('file', type=str, help='Video file location to process.')
parser.add_argument('width',type=int)
parser.add_argument('height',type=int)
args = parser.parse_args()
video_file = args.file
w=args.width
h=args.height

class FFProbeResult(NamedTuple):
    return_code: int
    json: str
    error: str

def ffprobe(file_path) -> FFProbeResult:
    command_array = ["ffprobe",
                     "-v", "quiet",
                     "-print_format", "json",
                     "-show_format",
                     "-show_streams",
                     file_path]
    result = subprocess.run(command_array, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    return FFProbeResult(return_code=result.returncode,
                         json=result.stdout,
                         error=result.stderr)

def convert(input_f,out_f,w,h):
    command=[
    	'ffmpeg',
    	'-y',
    	'-i', input_f,
    	'-vf', f'scale={w}:{h}',
    	'-c:v', 'libx264',
    	out_f
    ]	
    subprocess.run(command)
out='convert'+video_file
convert(video_file,out,w,h)

# get video file info
ffprobe_result = ffprobe(args.file)
info = json.loads(ffprobe_result.json)
videoinfo = [i for i in info["streams"] if i["codec_type"] == "video"][0]
input_fps = videoinfo["avg_frame_rate"]
# input_fps = float(input_fps[0])/float(input_fps[1])
input_pix_fmt = videoinfo["pix_fmt"]
input_vcodec = videoinfo["codec_name"]

# define a writer object to write to a movidified file
postfix = info["format"]["format_name"].split(",")[0]
output_file = ".".join(video_file.split(".")[:-1])+".processed." + postfix

