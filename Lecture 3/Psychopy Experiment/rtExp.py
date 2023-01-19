## Base Program
from psychopy import visual, core


# Create window
win =  visual.Window([500,500], monitor = "TV", units = "deg");

# Create stimulus
stim = visual.shape.ShapeStim(win = win, pos = [0,0], fillColor = 'blue', lineColor = 'red');

# Draw stimulus and update the screen
stim.draw();
win.flip();
core.wait(2);