## Base Program
from psychopy import visual, core, event, gui
import os, csv, time

# Create window
win =  visual.Window([500,500], monitor = "TV");

#record information
date = time.strftime("%m_%d");
startTime = time.time();
expInfo = {'subject': '', 'date' : date, 'start time' : startTime};
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title='user input')
if dlg.OK == False:
    core.quit();

# Write out into the output file
_thisDir = os.path.dirname(os.path.abspath(__file__));
os.chdir(_thisDir);
OUTPATH = os.path.join(os.getcwd(), 'Data');
if not os.path.isdir(OUTPATH):
    os.mkdir(OUTPATH)


outputFileName = expInfo['subject'] + '_' + expInfo['date'] + '.csv';
outputFilePath = os.path.join(OUTPATH, outputFileName);
csvFile = open(outputFilePath, 'w');
writer = csv.writer(csvFile);
headings = ('trial','keyPressed','reactionTime','correctness');
writer.writerow(headings);

# Create instructions, fixation cross, and stimulus

instr = visual.TextStim(win = win, text = "Press v when you see the stimulus", font = "arial", pos = [0,0]);
cross = visual.ShapeStim(win=win, name='Cross', vertices = 'cross', size = 0.1, fillColor = 'white', lineColor = 'white');
stim = visual.Circle(win = win, pos = [0,0], fillColor = 'blue');
# Draw instructions and update the screen
instr.draw();
win.flip();
core.wait(1);

# Create variable to store times
times = {'start': 0, 'end': 0}


for i in range(3):
    # Draw fixation cross and update the screen
    cross.draw();
    win.timeOnFlip(times, 'start')
    win.flip();
    core.wait(1);
    # Draw stimulus and update the screen
    stim.draw();
    win.flip();
    keysPressed = event.waitKeys(timeStamped = True);

    # logic
    key = keysPressed[0];
    times['end'] = key[1];
    reactionTime = times['end'] - times['start']
    isCorrect = (key[0] == 'v')

    # output
    trialOutput = (i,key[0],reactionTime,isCorrect);
    writer.writerow(trialOutput);


csvFile.close();