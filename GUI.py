"""
Mice Automatic Behavior Analysis (MABA)
@ Juarez Culau Batista Pires
https://github.com/JuarezCulau/MABA

Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""
import os
import PySimpleGUI as sg
import tensorflow as tf
import cv2
import numpy as np
import sys
import time
from io import StringIO
from data_processing.frames import Config

#The GUI (Using PySimpleGUI)

def main():
    # Define the buttons layout
    buttons_layout = [
        [sg.Text('Track Multiple Zones')],
        [sg.Text('Off'),
         sg.Button(image_data=toggle_btn_off, key='-TrackZones?-',
                   button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0,
                   metadata=False),
         sg.Text('On')],
        [sg.Text('Dual Zones')],
        [sg.Text('Off'),
         sg.Button(image_data=toggle_btn_off, key='-DualZones-',
                   button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0,
                   metadata=False),
         sg.Text('On')],
        [sg.Text('Novel Object Recognition')],
        [sg.Text('Off'),
         sg.Button(image_data=toggle_btn_off, key='-RON?-',
                   button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0,
                   metadata=False),
         sg.Text('On')],
        [sg.Text('Crop Object Recognition')],
        [sg.Text('Off'),
         sg.Button(image_data=toggle_btn_off, key='-CropRON?-',
                   button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0,
                   metadata=False),
         sg.Text('On')],
        [sg.Text('Detect Interaction Novel Object Recognition')],
        [sg.Text('Off'),
         sg.Button(image_data=toggle_btn_off, key='-Interaction-',
                   button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0,
                   metadata=False),
         sg.Text('On')],
        [sg.Text('Locomotion Graph')],
        [sg.Text('Off'),
         sg.Button(image_data=toggle_btn_off, key='-LocomotionGraph?-',
                   button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0,
                   metadata=False),
         sg.Text('On')],
        [sg.Text('Freeze State')],
        [sg.Text('Off'),
         sg.Button(image_data=toggle_btn_off, key='-FreezeState?-',
                   button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0,
                   metadata=False),
         sg.Text('On')],
        [sg.Text('Crop Image (Freeze)')],
        [sg.Text('Off'),
         sg.Button(image_data=toggle_btn_off, key='-CropImage?-',
                   button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0,
                   metadata=False),
         sg.Text('On')],
        [sg.Text('Elevated Plus Maze')],
        [sg.Text('Off'),
         sg.Button(image_data=toggle_btn_off, key='-EPM?-',
                   button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0,
                   metadata=False),
         sg.Text('On')],
    ]

    global TrackZones, NovelObject, CropRon, CreateLocomotionGraph, DualZone, Interaction
    layout = [[sg.Text('Select the Model PB')],
              [sg.InputText(size=(50, 1), key='-ModelPB-'), sg.FileBrowse()],
              [sg.Text('Select the Video or Folder for Analysis')],
              [sg.InputText(size=(50, 1), key='-VideoFile-'), sg.FileBrowse(file_types=(("Video Files", "*.mp4;*.avi"),), target='-VideoFile-', enable_events=True), sg.FolderBrowse(target='-VideoFile-', enable_events=True)],
              [sg.Text('Analysis Folder')],
              [sg.InputText(size=(50, 1), key='-Folder-'), sg.FolderBrowse()],
              [sg.Text('Name Your Sample')],
              [sg.InputText(key='-Sample-')],

              [sg.Text('Analysis Options', font='Helvetica 12 bold')],
              [sg.Column(buttons_layout, size=(700, 300), scrollable=True, vertical_scroll_only=True, key='-BUTTON_COLUMN-')],
              [sg.Button('Run'), sg.Button('Exit')],
              ]

    window = sg.Window('MABA', layout, font='_ 14', finalize=True)

    while True:  # Event Loop
        event, values = window.read()
        #print(window['-TOGGLE-GRAPHIC-'].metadata)
        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        #First button logic
        elif event == '-TrackZones?-':  # if the graphical button that changes images
            window['-TrackZones?-'].metadata = not window['-TrackZones?-'].metadata
            window['-TrackZones?-'].update(image_data=toggle_btn_on if window['-TrackZones?-'].metadata else toggle_btn_off)
        if window['-TrackZones?-'].metadata:
            Config.TrackZones = True
        else:
            Config.TrackZones = False

        #Second Button logic
        if event == '-DualZones-':  # if the graphical button that changes images
            window['-DualZones-'].metadata = not window['-DualZones-'].metadata
            window['-DualZones-'].update(image_data=toggle_btn_on if window['-DualZones-'].metadata else toggle_btn_off)
        if window['-DualZones-'].metadata:
            Config.DualZone = True
        else:
            Config.DualZone = False

        #Third Button logic
        if event == '-RON?-':  # if the graphical button that changes images
            window['-RON?-'].metadata = not window['-RON?-'].metadata
            window['-RON?-'].update(image_data=toggle_btn_on if window['-RON?-'].metadata else toggle_btn_off)
        if window['-RON?-'].metadata:
            Config.NovelObject = True
        else:
            Config.NovelObject = False

        # Forth Button logic
        if event == '-CropRON?-':  # if the graphical button that changes images
            window['-CropRON?-'].metadata = not window['-CropRON?-'].metadata
            window['-CropRON?-'].update(image_data=toggle_btn_on if window['-CropRON?-'].metadata else toggle_btn_off)
        if window['-CropRON?-'].metadata:
            Config.CropRon = True
        else:
            Config.CropRon = False

        # Fifth Button logic
        if event == '-Interaction-':  # if the graphical button that changes images
            window['-Interaction-'].metadata = not window['-Interaction-'].metadata
            window['-Interaction-'].update(image_data=toggle_btn_on if window['-Interaction-'].metadata else toggle_btn_off)
        if window['-Interaction-'].metadata:
            Config.Interaction = True
        else:
            Config.Interaction = False

        # Sixth Button logic
        if event == '-LocomotionGraph?-':  # if the graphical button that changes images
            window['-LocomotionGraph?-'].metadata = not window['-LocomotionGraph?-'].metadata
            window['-LocomotionGraph?-'].update(image_data=toggle_btn_on if window['-LocomotionGraph?-'].metadata else toggle_btn_off)
        if window['-LocomotionGraph?-'].metadata:
            Config.CreateLocomotionGraph = True
        else:
            Config.CreateLocomotionGraph = False

        # Seventh Button logic
        if event == '-FreezeState?-':  # if the graphical button that changes images
            window['-FreezeState?-'].metadata = not window['-FreezeState?-'].metadata
            window['-FreezeState?-'].update(image_data=toggle_btn_on if window['-FreezeState?-'].metadata else toggle_btn_off)
        if window['-FreezeState?-'].metadata:
            Config.Freeze = True
        else:
            Config.Freeze = False

        # Eighth Button logic
        if event == '-CropImage?-':  # if the graphical button that changes images
            window['-CropImage?-'].metadata = not window['-CropImage?-'].metadata
            window['-CropImage?-'].update(image_data=toggle_btn_on if window['-CropImage?-'].metadata else toggle_btn_off)
        if window['-CropImage?-'].metadata:
            Config.CropImage = True
        else:
            Config.CropImage = False

        # Ninth Button logic
        if event == '-EPM?-':  # if the graphical button that changes images
            window['-EPM?-'].metadata = not window['-EPM?-'].metadata
            window['-EPM?-'].update(image_data=toggle_btn_on if window['-EPM?-'].metadata else toggle_btn_off)
        if window['-EPM?-'].metadata:
            Config.EPM = True
        else:
            Config.EPM = False

        # Check if it's only one video or folder
        selected_path = values['-VideoFile-']
        if selected_path:
            if os.path.isfile(selected_path):
                Config.SingleVideo = True
            elif os.path.isdir(selected_path):
                # Analyze all video files in the selected folder
                Config.SingleVideo = False

        #the process will begin here once "Run" is selected
        if event == 'Run':
            Config.setglobalvariables(values)

    window.close()

if __name__ == '__main__':
    # The base64 strings for the button images
    toggle_btn_off = b'iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAABmJLR0QA/wD/AP+gvaeTAAAED0lEQVRYCe1WTWwbRRR+M/vnv9hO7BjHpElMKSlpqBp6gRNHxAFVcKM3qgohQSqoqhQ45YAILUUVDRxAor2VAweohMSBG5ciodJUSVqa/iikaePEP4nj2Ovdnd1l3qqJksZGXscVPaylt7Oe/d6bb9/svO8BeD8vA14GvAx4GXiiM0DqsXv3xBcJU5IO+RXpLQvs5yzTijBmhurh3cyLorBGBVokQG9qVe0HgwiXLowdy9aKsY3g8PA5xYiQEUrsk93JTtjd1x3siIZBkSWQudUK4nZO1w3QuOWXV+HuP/fL85klAJuMCUX7zPj4MW1zvC0Ej4yMp/w++K2rM9b70sHBYCjo34x9bPelsgp/XJksZ7KFuwZjr3732YcL64ttEDw6cq5bVuCvgy/sje7rT0sI8PtkSHSEIRIKgCQKOAUGM6G4VoGlwiqoVd2Za9Vl8u87bGJqpqBqZOj86eEHGNch+M7otwHJNq4NDexJD+59RiCEQG8qzslFgN8ibpvZNsBifgXmFvJg459tiOYmOElzYvr2bbmkD509e1ylGEZk1Y+Ssfan18n1p7vgqVh9cuiDxJPxKPT3dfGXcN4Tp3dsg/27hUQs0qMGpRMYjLz38dcxS7Dm3nztlUAb38p0d4JnLozPGrbFfBFm79c8hA3H2AxcXSvDz7/+XtZE1kMN23hjV7LTRnKBh9/cZnAj94mOCOD32gi2EUw4FIRUMm6LGhyiik86nO5NBdGRpxYH14bbjYfJteN/OKR7UiFZVg5T27QHYu0RBxoONV9W8KQ7QVp0iXdE8fANUGZa0QAvfhhXlkQcmjJZbt631oIBnwKmacYoEJvwiuFgWncWnXAtuVBBEAoVVXWCaQZzxmYuut68b631KmoVBEHMUUrJjQLXRAQVSxUcmrKVHfjWWjC3XOT1FW5QrWpc5IJdQhDKVzOigEqS5dKHMVplnNOqrmsXqUSkn+YzWaHE9RW1FeXL7SKZXBFUrXW6jIV6YTEvMAUu0W/G3kcxPXP5ylQZs4fa6marcWvvZfJu36kuHjlc/nMSuXz+/ejxgqPFpuQ/xVude9eu39Jxu27OLvBGoMjrUN04zrNMbgVmOBZ96iPdPZmYntH5Ls76KuxL9NyoLA/brav7n382emDfHqeooXyhQmARVhSnAwNNMx5bu3V1+habun5nWdXhwJZ2C5mirTesyUR738sv7g88UQ0rEkTDlp+1wwe8Pf0klegUenYlgyg7bby75jUTITs2rhCAXXQ2vwxz84vlB0tZ0wL4NEcLX/04OrrltG1s8aOrHhk51SaK0us+n/K2xexBxljcsm1n6x/Fuv1PCWGiKOaoQCY1Vb9gWPov50+fdEqd21ge3suAlwEvA14G/ucM/AuppqNllLGPKwAAAABJRU5ErkJggg=='
    toggle_btn_on = b'iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAABmJLR0QA/wD/AP+gvaeTAAAD+UlEQVRYCe1XzW8bVRCffbvrtbP+2NhOD7GzLm1VoZaPhvwDnKBUKlVyqAQ3/gAkDlWgPeVQEUCtEOIP4AaHSI0CqBWCQyXOdQuRaEFOk3g3IMWO46+tvZ+PeZs6apq4ipON1MNafrvreTPzfvub92bGAOEnZCBkIGQgZOClZoDrh25y5pdjruleEiX+A+rCaQo05bpuvJ/+IHJCSJtwpAHA/e269g8W5RbuzF6o7OVjF8D3Pr4tSSkyjcqfptPDMDKSleW4DKIggIAD5Yf+Oo4DNg6jbUBlvWLUNutAwZu1GnDjzrcXzGcX2AHw/emFUV6Sfk0pqcKpEydkKSo9q3tkz91uF5aWlo1Gs/mYc+i7tz4//19vsW2AU9O381TiioVCQcnlRsWeQhD3bJyH1/MiFLICyBHiuzQsD1arDvypW7DR9nzZmq47q2W95prm+I9fXfqXCX2AF2d+GhI98Y8xVX0lnxvl2UQQg0csb78ag3NjEeD8lXZ7pRTgftmCu4864OGzrq+5ZU0rCa3m+NzXlzvoAoB3+M+SyWQuaHBTEzKMq/3BMbgM+FuFCDBd9kK5XI5PJBKqLSev+POTV29lKB8rT0yMD0WjUSYLZLxzNgZvIHODOHuATP72Vwc6nQ4Uiw8MUeBU4nHS5HA6TYMEl02wPRcZBJuv+ya+UCZOIBaLwfCwQi1Mc4QXhA+PjWRkXyOgC1uIhW5Qd8yG2TK7kSweLcRGKKVnMNExWWBDTQsH9qVmtmzjiThQDs4Qz/OUSGTwcLwIQTLW58i+yOjpXDLqn1tgmDzXzRCk9eDenjo9yhvBmlizrB3V5dDrNTuY0A7opdndStqmaQLPC1WCGfShYRgHdLe32UrV3ntiH9LliuNrsToNlD4kruN8v75eafnSgC6Luo2+B3fGKskilj5muV6pNhk2Qqg5v7lZ51nBZhNBjGrbxfI1+La5t2JCzfD8RF1HTBGJXyDzs1MblONulEqPDVYXgwDIfNx91IUVbAbY837GMur+/k/XZ75UWmJ77ou5mfM1/0x7vP1ls9XQdF2z9uNsPzosXPNFA5m0/EX72TBSiqsWzN8z/GZB08pWq9VeEZ+0bjKb7RTD2i1P4u6r+bwypo5tZUumEcDAmuC3W8ezIqSGfE6g/sTd1W5p5bKjaWubrmWd29Fu9TD0GlYlmTx+8tTJoZeqYe2BZC1/JEU+wQR5TVEUPptJy3Fs+Vkzgf8lemqHumP1AnYoMZSwsVEz6o26i/G9Lgitb+ZmLu/YZtshfn5FZDPBCcJFQRQ+8ih9DctOFvdLIKHH6uUQnq9yhFu0bec7znZ+xpAGmuqef5/wd8hAyEDIQMjAETHwP7nQl2WnYk4yAAAAAElFTkSuQmCC'

    main()