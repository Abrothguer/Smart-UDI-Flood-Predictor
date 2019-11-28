#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Splits a video into frames."""

# Meta
__author__ = "Arthur Borges"

# Imports
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
    get_frames("data/v1.mp4", "data/imgs/", fprefix="imgv1_", seconds=10)
    get_frames("data/v2.mp4", "data/imgs/", fprefix="imgv2_", seconds=10)
    get_frames("data/v3.mp4", "data/imgs/", fprefix="imgv3_", seconds=10)
    get_frames("data/v4.mp4", "data/imgs/", fprefix="imgv4_", seconds=10)
    get_frames("data/v5.mp4", "data/imgs/", fprefix="imgv5_", seconds=10)
    get_frames("data/v6.mp4", "data/imgs/", fprefix="imgv6_", seconds=10)


if __name__ == "__main__":
    main()
