# https://docs.opencv.org/3.4/d5/dc4/tutorial_adding_images.html

# Imports
import numpy as np
import cv2
import os
import time
from pygame import midi

# INITIAL CONDITIONS / CONSTANTS
CAMERA_ON = False
SINC_Y_OFFSET = 0
SINC_X_OFFSET = 0
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
JOYSTICK_SPEED = 0.2

midi.init()
default_id = midi.get_default_input_id()
midi_input = midi.Input(device_id = default_id)

# define a video capture object
vid = cv2.VideoCapture(0)
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 2000)
cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('frame', cv2.WND_PROP_AUTOSIZE, cv2.WINDOW_GUI_EXPANDED)


def create_sinc_frame(iterator, video, y_offset = SINC_Y_OFFSET, x_offset = SINC_X_OFFSET, scale = 1000, frames_per_period = 100):

    # Constants:
    x_px = FRAME_WIDTH
    y_px = FRAME_HEIGHT
    img = 0 * np.ones(shape = (y_px, x_px))
    img_rgb = np.dstack((img, img, img))
    tau = 1
    T = 5
    impulse_thickness = 5
    y_displacement = int(y_px / 2) + y_offset
    x_displacement = int(x_px / 2) + x_offset
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
                if an < 0:
                    y = y_displacement - c
                else:
                    y = y_displacement + c
                for t in range(0, impulse_thickness):
                   
                    x = x_displacement + t
                    if an > 0:
                        
                        if y >= 720 or x >= 1280:
                            pass
                        else:
                            img_rgb[y, x][0] = 255
                            img_rgb[y, x][1] = 255
                            img_rgb[y, x][2] = 255
                        
                    else:
                        if y >= 720 or x >= 1280:
                            pass
                        else:
                            img_rgb[y, x][0] = 255
                            img_rgb[y, x][1] = 255
                            img_rgb[y, x][2] = 255

        else:
            an = 1/(n * np.pi) * np.sin(np.pi * n * tau / T) * np.cos(iterator / frames_per_period * 2 * np.pi)
            an_s = abs(int(an * scale))

            for c in range(0, an_s):
                for t in range(0, impulse_thickness):
                    if an > 0:
                        y = c + y_displacement
                        x = x_displacement + (impulse_spacing * n + t)
                        if y >= 720 or x >= 1280:
                            pass
                        else:
                            img_rgb[y, x][0] = 255
                            img_rgb[y, x][1] = 255
                            img_rgb[y, x][2] = 255
                    else:
                        y = y_displacement - c
                        x = x_displacement + (impulse_spacing * n + t)
                        if y >= 720 or x >= 1280:
                            pass
                        else:
                            img_rgb[y, x][0] = 255
                            img_rgb[y, x][1] = 255
                            img_rgb[y, x][2] = 255

    alpha = 0.995
    beta = (1.0 - alpha)
    img1 = np.asarray(img_rgb, np.float64)
    img2 = np.asarray(video, np.float64)
    dst = cv2.addWeighted(img1, alpha, img2, beta, 0.0)
    cv2.imshow('frame', dst)
    cv2.waitKey(int(1/60 * 1000)) # 60 fps

i = 1
previous_dial_offset = int(127/2)
last_pressed_drum_pad = None

while True:
    if midi_input.poll():
        input = midi_input.read(num_events = 16)
        pad = input[0][0][1]
        if pad >= 44 and pad <= 51:
            last_pressed_drum_pad = pad

        dial_offset = input[0][0][2]

        
        if last_pressed_drum_pad == 48 and CAMERA_ON:  # camera is currently not on and pad1 will turn it on
            CAMERA_ON = False
            
        elif last_pressed_drum_pad == 48 and not CAMERA_ON:  # camerA is on and pad1 will disable the camera
            CAMERA_ON = True

        elif pad == 1:
            try:
                if dial_offset > previous_dial_offset:
                    SINC_X_OFFSET += int(dial_offset * JOYSTICK_SPEED) 
                else:
                    SINC_X_OFFSET -= int(dial_offset * JOYSTICK_SPEED) 

                previous_dial_offset = dial_offset

            except IndexError:
                pass
            
        elif pad == 2:
            try:
                if dial_offset > previous_dial_offset:
                    SINC_Y_OFFSET += int(dial_offset * JOYSTICK_SPEED) 
                else:
                    SINC_Y_OFFSET -= int(dial_offset * JOYSTICK_SPEED) 

                previous_dial_offset = dial_offset

            except IndexError:
                pass
    

    if CAMERA_ON:
        ret, frame = vid.read()
        create_sinc_frame(i, video = frame, y_offset = SINC_Y_OFFSET, scale = 720 * (i % 100) / 100, frames_per_period = 25)
        i += 1
    else:
        frame = np.ones((FRAME_HEIGHT, FRAME_WIDTH))
        frame = np.dstack((frame, frame, frame))
        create_sinc_frame(i, video = frame, y_offset = SINC_Y_OFFSET, x_offset = SINC_X_OFFSET, scale = 720 * (i % 100) / 100, frames_per_period = 25)
        i += 1




