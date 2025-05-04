# Modern GUI for Computer Vision with CustomTkinter

![Python](https://img.shields.io/badge/python-3.10-blue.svg)
![GitHub License](https://img.shields.io/github/license/trflorian/ctk-opencv?style=flat)

![demo](https://github.com/user-attachments/assets/c8600663-3b1d-489d-a144-56179f811cc3)

This demo showcases a CTK component that can display opencv frames from a video or a webcam stream.
The implementation uses a thread-safe queue to synchronize the frame buffer between the video thread and the main gui thread.

## Comparison

| OpenCV    | CustomTkinter |
| -------- | ------- |
| ![gui_opencv](https://github.com/user-attachments/assets/ad916bc7-73a5-48bf-8ad2-7f70ad1b14c1) | ![gui_ctk](https://github.com/user-attachments/assets/908de05b-bbf2-43c6-8f67-1037627c38ad) |


## Prerequisites

- [uv](https://docs.astral.sh/uv/)

## Quickstart

You can run the `main.py` file using uv:

```bash
uv run main.py
```

You can specify the gui type with the `gui` argument if you want to compare opencv and the modern ctk look.

```
usage: main.py [-h] [--gui {ctk,opencv}]

Webcam Stream with Filters

options:
  -h, --help          show this help message and exit
  --gui {ctk,opencv}  Choose the GUI framework to use (ctk or opencv).
```

## Tests

Run the testsuite with pytest

```bash
uv run pytest
```
