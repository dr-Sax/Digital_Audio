# https://docs.opencv.org/3.4/d5/dc4/tutorial_adding_images.html

# Imports
import numpy as np
import cv2
import os
import time
from pygame import midi

midi.init()
default_id = midi.get_default_input_id()
midi_input = midi.Input(device_id = default_id)

# define a video capture object
vid = cv2.VideoCapture(0)
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 2000)
cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('frame', cv2.WND_PROP_AUTOSIZE, cv2.WINDOW_GUI_EXPANDED)


def create_frame(iterator, video, scale = 1000, frames_per_period = 100):

    # Constants:
    x_px = 1280
    y_px = 720
    img = 0 * np.ones(shape = (y_px, x_px))
    img_rgb = np.dstack((img, img, img))
    tau = 1
    T = 5
    impulse_thickness = 5
    y_displacement = int(y_px / 2)
    x_displacement = int(x_px / 2)
    impulse_count = 50
    impulse_spacing = 10
    
    # n-range from -impulse count to impulse count
    for n in np.arange(-impulse_count, impulse_count, 1):

        # Base Case, middle pulse
        if n == 0:
            # an is the amplitude varying by frame, scaled by an_s (200 px)
            # 100 is number of frames in export
            an = np.cos(iterator / frames_per_period * 2 * np.pi)
            an_s = abs(int(scale * tau / T * an))

            for c in range(0, an_s):
                y = y_displacement + c
                for t in range(0, impulse_thickness):
                   
                    x = x_displacement + t
                    if an > 0:
                        
                        img_rgb[y, x][0] = 255
                        img_rgb[y, x][1] = 255
                        img_rgb[y, x][2] = 255
                        
                    else:
                        img_rgb[-y, x][0] = 255
                        img_rgb[-y, x][1] = 255
                        img_rgb[-y, x][2] = 255

        else:
            an = 1/(n * np.pi) * np.sin(np.pi * n * tau / T) * np.cos(iterator / frames_per_period * 2 * np.pi)
            an_s = abs(int(an * scale))

            for c in range(0, an_s):
                for t in range(0, impulse_thickness):
                    if an > 0:
                        y = c + y_displacement
                        x = x_displacement + (impulse_spacing * n + t)
                        if y > 720 or x > 1280:
                            pass
                        else:
                            img_rgb[y, x][0] = 255
                            img_rgb[y, x][1] = 255
                            img_rgb[y, x][2] = 255
                    else:
                        y = y_displacement - c
                        x = x_displacement + (impulse_spacing * n + t)
                        if y > 720 or x > 1280:
                            pass
                        else:
                            img_rgb[y, x][0] = 255
                            img_rgb[y, x][1] = 255
                            img_rgb[y, x][2] = 255

    cv2.imshow('frame', img_rgb)# + video)
    cv2.waitKey(int(1/60 * 1000)) # 60 fps

i = 1
while True:
    if midi_input.poll():
            print(midi_input.read(num_events=16)[0][0][1])
    ret, frame = vid.read()
    create_frame(i, video = frame, scale = 720 * (i % 100) / 100, frames_per_period = 25)
    i += 1




