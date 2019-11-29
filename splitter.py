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
    get_frames("data/v15.mp4", "data/imgs/", fprefix="imgv16_", seconds=10)
    get_frames("data/v17.mp4", "data/imgs/", fprefix="imgv17_", seconds=10)
    get_frames("data/v18.mp4", "data/imgs/", fprefix="imgv18_", seconds=10)
    get_frames("data/v19.mp4", "data/imgs/", fprefix="imgv19_", seconds=10)
    get_frames("data/v20.mp4", "data/imgs/", fprefix="imgv20_", seconds=10)
    get_frames("data/v21.mp4", "data/imgs/", fprefix="imgv21_", seconds=10)
    get_frames("data/v22.mp4", "data/imgs/", fprefix="imgv22_", seconds=10)
    # get_frames("data/v14.mp4", "data/imgs/", fprefix="imgv14_", seconds=10)


if __name__ == "__main__":
    main()
