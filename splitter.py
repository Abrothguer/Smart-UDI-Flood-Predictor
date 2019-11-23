#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Splits a video into frames."""

# Meta
__author__ = "Arthur Borges"

# Imports
import cv2


# Functions
def get_frames(vpath, fpath, fps=-1, fprefix="img_"):
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
        cv2.imwrite(f"{fpath}{fprefix}{count}.jpg", image)
        success, image = capture.read()

        count += 1
        capture.set(1, count * fps)
        print(f"Frame {count} read...")
