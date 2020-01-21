import numpy as np
import pandas as pd
import os, sys
from psychopy import visual, core, event, gui, logging, event
import csv




# Exit whenever 'escape' is pressed
def exit_experiment():
    win.close()
    core.quit()
event.globalKeys.add(key='escape', func=exit_experiment)


# open a white full screen window
win = visual.Window(size=(1000, 600), fullscr=False, allowGUI=True, color='white', unit='height') 


# The visual Messages
background = visual.Rect(win, width=1.6, height=1.5, fillColor="grey")
MTMinfo = visual.TextStim(win, text = "This experiment is designed to record the activity of the mice during habituation phase and test session of the Multiple Time Memory Experiment.\nAfter entering the slot and session info, the corresponding videos manually collected during the behavioural experiment will be drawn out.\n\nPress any key to continue.", color = 'black')
instructinfo = visual.TextStim(win, text = "You can exit at any time by pressing 'escape'.", color = 'black')
experimentinfo = visual.TextStim(win, text = "The video of the left chamber will be shown on your left hand. Press 'left' when you see the mouse appear in this chamber, press 'down' when you see the mouse leave the chamber.\nThe video of the right chamber will be shown on your right hand. Press 'right' when you see the mouse appear in this chamber, press 'down' when you see the mouse leave the chamber.\n\nThe videos will last for 10 minutes.", wrapWidth=1.2, color = 'black')
error_csvnotfound = visual.TextStim(win, text = "Uh oh! The csv file for the multiple time memory experiment can not be found. Please exit this session and create an original csv file with 'AssignSubject.py' first.\n\nPress any key to exit this session.", color = 'black')
error_videonotfound = visual.TextStim(win, text = "Uh oh! The video file for this session of this animal can not be found!\n\nPress any key to continue.", color = 'black')
text_novideo = visual.TextStim(win, text = "The mouse activity videos used for this experiment has yet to be collected.\nIt is estimated that they will be collected during February.\nNow, a text stimulus will be placed in where the video should be to mimic the procedure.\n\nPress any key to continue.", color = 'black')
ending = visual.TextStim(win, text = "The dwell time for this mouse has been recorded!\nIt will be saved as a csv file.", color = 'black')

# Import the dataframe
try:
        df = pd.read_csv('MTMmice.csv')
except:
    background.draw()
    error_csvnotfound.draw()
    win.flip()
    event.waitKeys()
    win.close()

# Create subject number and session
background.draw()
MTMinfo.draw()
win.flip()
event.waitKeys()
background.draw()
instructinfo.draw()
win.flip()
event.waitKeys()

background.draw()
win.flip()
slot = None
session = None
while slot is None or session is None:
    mouse = gui.Dlg(title = "Information of the Subject Mouse")
    mouse.addText('Location Info')
    mouse.addField("Stack:", choices=["1", "2"])
    mouse.addField("Level:", choices=["a", "b", "c","d"])
    mouse.addField("slot:", choices=["1", "2","3","4","5","6"])
    mouse.addText('Session Info')
    mouse.addField("Session:", choices=["Habituation", "Test"])
    mouse.show()
    if mouse.OK:  # or if ok_data is not None
        slot = "s" + mouse.data[0] + mouse.data[1] + mouse.data[2]
        session = mouse.data[3]
        

# Create the video stimuli based on the info

if df.loc[df.slot==slot, "group"][0][:3] == "CPP":
    left_video = slot+"-"+session+"-Plain.avi"
    right_video = slot+"-"+session+"-Circles.avi"
else:
    left_video = slot+"-"+session+"-Striped.avi"
    right_video = slot+"-"+session+"-Checkered.avi"

# If the video exists, draw out the movie stimuli.
if os.path.isfile(left_video) and os.path.isfile(right_video):
    left_movie = visual.MovieStim3(win, left_video, pos = [-0.5, 0])
    right_movie = visual.MovieStim3(win, right_video, pos = [0.5, 0])
# Otherwise, use text stimuli to mimic the process
else:
    background.draw()
    error_videonotfound.draw()
    win.flip()
    event.waitKeys()
    background.draw()
    text_novideo.draw()
    win.flip()
    print("why")
    event.waitKeys()
    left_movie = visual.TextStim(win, text = "This is where the video of the left chamber will be.", pos = [-0.4, 0], wrapWidth=0.6, color='black')
    right_movie = visual.TextStim(win, text = "This is where the video of the right chamber will be.", pos = [0.4, 0],wrapWidth=0.6, color='black')



background.draw()
experimentinfo.draw()
win.flip()
event.waitKeys()
# Create the clocks
trialClock = core.Clock()
stimClock = core.Clock()

# record how long the mice spent in each chamber
background.draw()
left_movie.draw()
right_movie.draw()
win.flip()
event.waitKeys(keyList=['left','down','right'])
trialClock.reset()
dwelltime = pd.DataFrame(columns=["response","time"])
while trialClock.getTime() < 3600:
    stimClock.reset()
    response = event.waitKeys(keyList=['left','down','right'], timeStamped = stimClock)
    dwelltime = dwelltime.append({'response':response[0][0],'time':response[0][1]}, ignore_index=True)
print(dwelltime)
    
background.draw()
ending.draw()
win.flip()
event.waitKeys()

    

dwelltime.to_csv(slot+"-"+session+".csv", encoding='utf-8', index=False)