from psychopy import visual, core, data, event
import time

expInfo = {'subject': 'Mingda'}

fileName = expInfo['subject']
dataFile = open(fileName+'.csv', 'w')
dataFile.write('keyPressed,RT\n')

win =  visual.Window([500,500], monitor = "TV", units = "deg");
#grating = visual.GratingStim(win = win, mask = "circle", size = 1, pos = [0,0], sf = 3);

grating = visual.GratingStim(win = win, mask = "circle", size = 0.2, pos = [0,0], sf = 3, ori = 90);
grating.ori = 90;

#fixation = visual.GratingStim(win = win, size = 0.5, pos = [0,0], rgb = 1);
instr = visual.TextStim(win = win, text = "press right when you see the stimulus", font = "arial", pos = [0,0]);
instr.size = 0.1;

instr.draw()
win.flip();
core.wait(2);

resp = '';
times = {'start': 0, 'end': 0}

for i in range(2):
    grating.draw();
    win.timeOnFlip(times, 'start')
    win.flip();
    keys = event.waitKeys(timeStamped = True);
    key = keys[0];
    times['end'] = key[1]
    if (key[0] == 'right'):
        resp = 'r';
    else:
        resp = 'l';
    reactT = times['end'] - times['start'];
    dataFile.write(resp +  ',');
    dataFile.write(str(reactT));
    dataFile.write('\n');
    win.flip()
    core.wait(1);

