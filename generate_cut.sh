#!/bin/sh
rm cut.mp4
ffmpeg -f concat -segment_time_metadata 1 -i concat_list.txt -vf select=concatdec_select -af aselect=concatdec_select,aresample=async=1 cut.mp4
open cut.mp4