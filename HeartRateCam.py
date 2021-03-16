# Resource
# https://medium.com/dev-genius/remote-heart-rate-detection-using-webcam-and-50-lines-of-code-2326f6431149#id_token=eyJhbGciOiJSUzI1NiIsImtpZCI6Ijg0NjJhNzFkYTRmNmQ2MTFmYzBmZWNmMGZjNGJhOWMzN2Q2NWU2Y2QiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJuYmYiOjE2MTU4ODk5MzAsImF1ZCI6IjIxNjI5NjAzNTgzNC1rMWs2cWUwNjBzMnRwMmEyamFtNGxqZGNtczAwc3R0Zy5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsInN1YiI6IjEwMTkyMzI5NzA3NTEzMjI5NTIwMyIsImVtYWlsIjoibWFyY28uYmF0dXJhbkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXpwIjoiMjE2Mjk2MDM1ODM0LWsxazZxZTA2MHMydHAyYTJqYW00bGpkY21zMDBzdHRnLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwibmFtZSI6Ik1hcmNvIEJhdHVyYW4iLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EtL0FPaDE0R2c5VFJXMnN3Zk1nNjBjVkh4NG50TFIzVlhkUHdBR0xTZXBoOHV6cXc9czk2LWMiLCJnaXZlbl9uYW1lIjoiTWFyY28iLCJmYW1pbHlfbmFtZSI6IkJhdHVyYW4iLCJpYXQiOjE2MTU4OTAyMzAsImV4cCI6MTYxNTg5MzgzMCwianRpIjoiZmMwOTgyMTJjYjMxNmI1NmZmMDAyZGY1MDA4ZGI4ZTBkNjgyODI0ZiJ9.S_cKGB4s40SZdqW2cyyRYzDh4VK92Xts3l-FaR3uS80eBZgFCMFQUBFZE-Xl70UvLuW8r0cLYlfZDWeLqDhlkcaWPXwmknM3yXOiGoAjdrGO2nJ4iK9ubiEr_fO-YPePzDIYpSqYN5sGxSlFGzO2EaUT8r2LgUdpZowAWs6KVv41fKmCpki61Bo8qHO-Keakw0WPinrosnDPZLaTyXT1FzeNxg4xWD6sGcSsZtG00trMZSL9gQXKgakiKez5VMA4SajuzbSAEmYJN9kVIbsAJNgvuT3fHzDrxQ9wZ1nol1K-4CZX6dx4umVdBCdbqMIaQVBHUxbMjqAnqoIUSx-koA
# Imports
import numpy as np
from matplotlib import pyplot as plt
import cv2
import io
import time
import PySimpleGUI as sg

# Camera stream
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1280)
cap.set(cv2.CAP_PROP_FPS, 30)

# Image crop
x, y, w, h = 800, 500, 100, 100
x, y, w, h = 950, 300, 100, 100
heartbeat_count = 128
heartbeat_values = [0]*heartbeat_count
heartbeat_times = [time.time()]*heartbeat_count

# Matplotlib graph surface
fig = plt.figure()
ax = fig.add_subplot(111)
list_pulses = []

# Defining final function for show results
def pop_up_average(list_pulses):
    """Pop up average pulse.
        
        Function for calling at the end.
        Received all data and make average
        calc. And show the result in a
        pop-up.
        
    """
    sum_lp =0
    for lp in list_pulses:
        sum_lp += int(lp[0])
        average_lp= sum_lp/len(list_pulses)
 
    sg.popup('Average heart rate:', int(average_lp))


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #crop_img = img[y:y + h, x:x + w] # run in python3.6
    # Update the data
    heartbeat_values = heartbeat_values[1:] + [np.average(img)] # p3.6 be crop_img
    heartbeat_times = heartbeat_times[1:] + [time.time()]
    # Draw matplotlib graph to numpy array
    ax.plot(heartbeat_times, heartbeat_values)
    fig.canvas.draw()
    plot_img_np = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    plot_img_np = plot_img_np.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    plt.cla()
    # Display the frames
    cv2.imshow('Crop', img) # p3.6 be crop_img
    cv2.imshow('Graph heart rate', plot_img_np)
    list_pulses.append(heartbeat_values[-1:])
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # breakcap.release() # Work in P3.6
        cv2.destroyAllWindows()
        # ¡Last line need improve to show at sametime with other windows!
        pop_up_average(list_pulses=list_pulses) 
