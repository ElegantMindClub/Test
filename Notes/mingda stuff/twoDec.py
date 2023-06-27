## Base Program
from psychopy import visual, core, event, gui
import os, csv, time, random

#EMOTIV
#from psychopy.hardware import emotiv
#routineTimer = core.Clock()

#global variables
trials = 10 # must be even



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
headings = ('trial','trialType','reactionTime','correctness');
writer.writerow(headings);

# Create window
win =  visual.Window(fullscr=True, monitor = "TV");


# EMOTIV starts recording
#cortex_rec = visual.BaseVisualStim(win=win, name=expInfo['subject'])
#cortex_obj = emotiv.Cortex(subject= expInfo['subject'])


# Create instructions, fixation cross, and stimulus
instr = visual.TextStim(win = win, height = 0.2, text = "Press v if you see a blue circle and b if you see a red circle.", font = "arial", pos = [0,0], units = 'deg');
cross = visual.ShapeStim(win=win, name='Cross', vertices = 'cross', size = 0.1, fillColor = 'white', lineColor = 'white', units = 'deg');
blueStim = visual.Circle(win = win, pos = [0,0], fillColor = 'blue', units = 'deg');
redStim = visual.Circle(win = win, pos = [0,0], fillColor = 'red', units = 'deg');

# Draw instructions and update the screen
instr.draw();
win.flip();
core.wait(2);



# Create variable to store times
times = {'start': 0, 'end': 0}

#create list of stimuli
a = [0]*int(trials/2);
a += [1]*int(trials/2)
random.shuffle(a)

for i in range(trials):
    # Draw fixation cross and update the screen
    cross.draw();
    win.flip();
    
    waitTime = random.random()*2;
    core.wait(waitTime);
    
    # Draw stimulus and update the screen
    isBlue = (a[i]==0)
    if(isBlue):
        blueStim.draw();
        currTrialType = 'Blue';
    else:
        redStim.draw();
        currTrialType = 'Red';
    
    # EMOTIV
    #tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    #win.timeOnFlip(times, 'start')
    #win.flip();
    
    #t = routineTimer.getTime()
    #delta_time = tThisFlip-t

    
    #eegStuff[1].inject_marker(value=str('1'), label='stim', delta_time=delta_time)

    
    
    keysPressed = event.waitKeys(timeStamped = True);
    win.flip();
    # logic
    key = keysPressed[0];
    times['end'] = key[1];
    reactionTime = times['end'] - times['start']
    isV = (key[0] == 'v')
    if isV:
        isCorrect = isBlue
    else:
        isCorrect = ~isBlue

    # output
    trialOutput = (i,currTrialType,reactionTime,isCorrect);
    writer.writerow(trialOutput);
    
    core.wait(1)

# ends recording
cortex_obj.close_session()

csvFile.close();
core.quit()
