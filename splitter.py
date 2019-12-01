#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Splits a video into frames."""

# Meta
__author__ = "Arthur Borges"

# Imports
import os
import cv2


# Functions
def get_frames(vpath, fpath, fps=-1, seconds=1, fprefix="img_"):
    """Open a video file and divides it into various frames.

    Args:
        vpath (str): Path of video.
        fpath (str): Path of image files output.
        fps (int): Frames per second of video.
        fprefix (str): Prefix of image files.

    """
    capture = cv2.VideoCapture(vpath)
    fps = fps if fps > 0 else capture.get(cv2.CAP_PROP_FPS)
    print(f"Capture has {fps} FPS.")

    success, image = capture.read()
    count = 0

    while success:
        print(f"Saving on ~/{fpath}{fprefix}{count}.jpg")
        cv2.imwrite(f"{fpath}{fprefix}{count}.jpg", image)
        success, image = capture.read()

        count += 1
        capture.set(1, count * fps * seconds)
        print(f"Frame {count} read...")


def main():

    videos = filter(lambda x: x.find('.mp4') != -1, os.listdir('data'))
    for video in videos:
        zeros = len(video)
        name = video.split('.')[0][1:]

        if zeros == 7:
            zeros = 0
        else:
            zeros = 1
        print(name, zeros)
        get_frames(f"data/{video}", "data/imgs/", fprefix=f"img_v{'0'*zeros}{name}_", seconds=10)


if __name__ == "__main__":
    main()
