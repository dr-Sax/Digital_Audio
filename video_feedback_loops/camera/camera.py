# import the opencv library
import cv2
from pygame import midi

midi.init()
default_id = midi.get_default_input_id()
midi_input = midi.Input(device_id=default_id)
  
  
# define a video capture object
vid = cv2.VideoCapture(0)
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 2000)
cv2.namedWindow('frame', cv2.WINDOW_NORMAL)


i = 1  
keyboard_action = 1
while(True):
      
    # Capture the video frame
    # by frame
    if midi_input.poll():
            keyboard_action = midi_input.read(num_events=16)[0][0][1]


    ret, frame = vid.read()
    
    
  
    # Display the resulting frame
    cv2.imshow('frame', frame * keyboard_action )
      
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    i += 1
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()