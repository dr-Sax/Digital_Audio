# Imports
import numpy as np
import cv2
import os



def create_frame(iterator, scale = 1000, frames_per_period = 100):

    # Constants:
    img = 0 * np.ones(shape = (1000, 1000))
    img_rgb = np.dstack((img, img, img))
    tau = 1
    T = 5
    impulse_thickness = 5
    y_displacement = 500
    x_displacement = 500
    impulse_count = 30
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
                for t in range(0, impulse_thickness):
                    if an > 0:
                        img_rgb[c + 500, 500 + t][0] = 255
                        img_rgb[c + 500, 500 + t][1] = 10
                        img_rgb[c + 500, 500 + t][2] = 27
                        
                    else:
                        img_rgb[-(c + 500), 500 + t][0] = 254
                        img_rgb[-(c + 500), 500 + t][1] = 27
                        img_rgb[-(c + 500), 500 + t][2] = 4

        else:
            an = 1/(n * np.pi) * np.sin(np.pi * n * tau / T) * np.cos(iterator / frames_per_period * 2 * np.pi)
            an_s = abs(int(an * scale))

            for c in range(0, an_s):
                for t in range(0, impulse_thickness):
                    if an > 0:
                        y = c + y_displacement
                        x = x_displacement + (impulse_spacing * n + t)
                        if y > 1000 or x > 1000:
                            pass
                        else:
                            img_rgb[y, x][0] = 255
                            img_rgb[y, x][1] = 21
                            img_rgb[y, x][2] = 155
                    else:
                        y = y_displacement - c
                        x = x_displacement + (impulse_spacing * n + t)
                        if y > 1000 or x > 1000:
                            pass
                        else:
                            img_rgb[y, x][0] = 255
                            img_rgb[y, x][1] = 255
                            img_rgb[y, x][2] = 255

    cv2.imwrite(f'sinc_anim/{iterator}.jpg', img_rgb)

for i in range(0, 100):
    create_frame(i, scale = 1800 * i / 100, frames_per_period = 25)



img_array = []
file_array = []
#base = '/Users/nicolasromano/Documents/code/AlgoRhythms/Digital_Audio/Fiesta_Red/sinc_anim/'
base = 'C:/Users/nicor/.vscode/Digital_Audio/Fiesta_Red/sinc_anim/'
frame_cnt = len([entry for entry in os.listdir(base) if os.path.isfile(os.path.join(base, entry))])


for i in range(0, 10*frame_cnt):
    file_array.append(base + str(i % 100) + '.jpg')

for i in range(0, len(file_array)):
    img = cv2.imread(file_array[i], 1)
    img_array.append(img)
    height, width, layers = img.shape
    size = (width,height)

out = cv2.VideoWriter(f'sinc_oscillate.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, size)

for i in range(len(img_array)):
    out.write(img_array[i])
out.release()