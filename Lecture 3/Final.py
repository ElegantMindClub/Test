## Base Program
from psychopy import visual, core

# Create window
win =  visual.Window([500,500], monitor = "TV");


# Create instructions, fixation cross, and stimulus
instr = visual.TextStim(win = win, text = "Press v when you see the stimulus", font = "arial", pos = [0,0]);
cross = visual.ShapeStim(win=win, name='Cross', vertices = 'cross', size = 0.1, fillColor = 'white', lineColor = 'white');
stim = visual.Circle(win = win, pos = [0,0], fillColor = 'blue', lineColor = 'red');

# Draw instructions and update the screen
instr.draw();
win.flip();
core.wait(1);
# Draw fixation cross and update the screen
cross.draw();
win.flip();
core.wait(1);
# Draw stimulus and update the screen
stim.draw();
win.flip();
core.wait(1);

