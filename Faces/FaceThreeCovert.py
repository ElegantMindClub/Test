import psychopy
from psychopy import gui, visual, core, event, monitors, prefs
prefs.hardware['audioLib'] = ['ptb', 'pyo']
from psychopy.sound import Sound
from psychopy.event import waitKeys
import numpy as np  
import os, sys, time, random, math, csv

angles = [0, 5, 10, 15, 20, 25, 30, 35, 40]
directions = [0, 2] #0 is right, 2 is left
faces = [15]
trials = 10
prePracticeBreak = 10
postPracticeBreak = 10

def csvOutput(output, fileName):
    with open(fileName, 'a', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(output)
    csvFile.close()
    
def csvInput(fileName):
    with open(fileName) as csvFile:
        reader = csv.DictReader(csvFile, delimiter = ',')
        dict = next(reader)
    csvFile.close()
    return dict

_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
facefile = os.path.join(os.getcwd(), 'eccentricity_monitor_calibration.csv')     #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
if not os.path.isfile(facefile):
    print('You must run the eccentricity_calibration.py script to set up your monitor')
    time.sleep(5)
    core.quit()

tvInfo = csvInput(facefile)
 
#heightMult = float(tvInfo['height'])
distToScreen = float(tvInfo['Distance to screen'])
faceHeightMult = float(tvInfo['faceHeight'])
faceWidthMult = float(tvInfo['faceWidth'])

#distToScreen = float(tvInfo['Distance to screen'])
heightMult, spacer = float(tvInfo['height']), float(tvInfo['spacer'])
circleMult = float(tvInfo['circleRadius'])
centerX, centerY = float(tvInfo['centerx']), float(tvInfo['centery'])
rightXMult, leftXMult = float(tvInfo['rightx']), float(tvInfo['leftx'])
rightEdge, leftEdge = float(tvInfo['rightEdge']), float(tvInfo['leftEdge'])

def endExp():
    win.flip()
    logging.flush()
    win.close()
    core.quit()

datadlg = gui.Dlg(title='Record Data?', pos=None, size=None, style=None,\
     labelButtonOK=' Yes ', labelButtonCancel=' No ', screen=-1)
ok_data = datadlg.show()
recordData = datadlg.OK

if recordData:
    date = time.strftime("%m_%d")
    expName = 'Face Three Decision Covert'
    expInfo = {'Subject Name': ''}
    
    dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
    if dlg.OK == False:
        core.quit()
    
    OUTPATH = os.path.join(os.getcwd(), 'Data')
    if not os.path.isdir(OUTPATH):
        os.mkdir(OUTPATH)
    
    fileName = os.path.join(OUTPATH,\
        (expInfo['Subject Name'] + '_' + date + '_' + expName + '.csv'))
        

    dirExclusions = []

headers = ['Face', 'Direction', 'Eccentricity', 'Reaction Time (s)']
if not os.path.isfile(fileName):
    csvOutput(headers, fileName)

mon = monitors.Monitor('TV') # Change this to the name of your display monitor
mon.setWidth(float(tvInfo['Width (cm)']))
win = visual.Window(
    size=(int(tvInfo['Width (px)']), int(tvInfo['Height (px)'])), fullscr=True, screen=int(tvInfo['Screen number']), 
    winType='pyglet', allowGUI=True, allowStencil=False,
    monitor= mon, color='grey', colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='cm')
    
def genDisplay(displayInfo):
    displayText = visual.TextStim(win=win,
    text= displayInfo['text'],
    font='Arial',
    pos=(displayInfo['xPos'], displayInfo['yPos']),
    height=displayInfo['heightCm'],
    wrapWidth=500,
    ori=0, 
    color=displayInfo['color'],
    colorSpace='rgb',
    opacity=1, 
    languageStyle='LTR',
    depth=0.0)
    return displayText
    
def displaceCalc(angle):
    angleRad = np.deg2rad(angle)
    xDisp = np.tan(angleRad)*distToScreen
    return xDisp
    
def checkcorrect(response, face):
    if response == 'escape':
        endExp()
    elif response == 'v':
        ans = 13
    elif response == 'b':
        ans = 15
    elif response == 'n':
        ans = 17
    else:
        ans = -1
    return (ans == face)

cross = visual.ShapeStim(
    win=win, name='Cross', vertices='cross',units='cm', 
    size=(1, 1),
    ori=0, pos=(centerX, centerY),
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb',
    opacity=1, depth=-1.0, interpolate=True)
    
feedbackBeep = Sound(value='A', secs=0.5, octave=4, stereo=-1, volume=1.0)
    
def getFace():
    faceNum = random.choice(faces)
    imageFile = (os.path.join(os.getcwd(), 'Faces', ('face'+str(faceNum)+'.png')))
    return {'file': imageFile, 'facenum': faceNum}


def instructions():
    genDisplay({'text': 'Press "V" or "B" or "N" for the appropriate face',\
        'xPos': 0, 'yPos': centerY+2, 'heightCm': 1, 'color': 'white'}).draw()
    genDisplay({'text': 'Please keep your eyes fixed to the center',\
        'xPos': 0, 'yPos': centerY,'heightCm': 1, 'color': 'white'}).draw()
    genDisplay({'text': 'Press the spacebar to continue',\
        'xPos': 0, 'yPos': centerY-2,'heightCm': 1, 'color': 'white'}).draw()
    win.flip()
    keyy = event.waitKeys(keyList = ['space', 'escape']) 
    if keyy[0] == 'escape': 
        win.flip()
        logging.flush()
        win.close()
        core.quit()
        
faceHeight = displaceCalc(8)*faceHeightMult
faceWidth = displaceCalc(8)*faceWidthMult

facestuff = getFace()
facefile = facestuff['file']

drawface = visual.ImageStim( 
    win=win, units='cm', image= facefile, 
    size = (faceWidth,faceHeight),
    interpolate=True) 
    


def expBreak():
    dispInfo = {'text': 'Break', 'xPos': 0, 'yPos': centerY+4, 'heightCm': 3, 'color': 'white'}
    breakText = genDisplay(dispInfo)
    dispInfo = {'text': '', 'xPos': 0, 'yPos': centerY, 'heightCm': 3, 'color': 'white'}
    for i in range(20):
        breakText.draw()
        dispInfo['text'] = str(20-i) + ' seconds'
        genDisplay(dispInfo).draw()
        win.flip()
        time.sleep(1)
        
def inBounds(trialInfo):
    if trialInfo['dir'] in dirExclusions:
        return False
    if trialInfo['dir'] == 0:
        if ((centerX + displaceCalc(trialInfo['angle']))+(displaceCalc(8)*.5)) > rightEdge:
            return False
    elif trialInfo['dir'] == 2:
        if ((centerX - displaceCalc(trialInfo['angle']))-(displaceCalc(8)*.5)) < (-leftEdge):
            return False
    return True

def genPairs():
    pairs = list(range(0))
    for i in range(trials):
        for j in range(len(angles)):
            for k in range(len(directions)):
                pairs.append((j*10)+k)
    random.shuffle(pairs)
    return pairs
    
def interpretPair(pair):
    angle = angles[int(pair/10)]
    direction = directions[int(pair%10)]
    
    return {'angle': angle, 'dir': direction}
   
    
instructions()

pairs = genPairs()

def learningPeriod(desiredface, desiredkey):
    genDisplay({'text': ('You will have 30 seconds to memorize this face'),\
        'xPos': 0, 'yPos': 5, 'heightCm': 1.5*heightMult, 'color': 'white'}).draw()
    genDisplay({'text': 'which will be tied to the key '+ str(desiredkey),\
        'xPos': 0, 'yPos': 3, 'heightCm': 1.5*heightMult, 'color': 'white'}).draw()
    genDisplay({'text': 'Press spacebar to continue.',\
        'xPos': 0, 'yPos': -3, 'heightCm': 1.5*heightMult, 'color': 'white'}).draw()
    win.flip()
    key = waitKeys(keyList = ['space', 'escape'])
    if key[0] == 'escape':
        endExp()
    i = 0
    while i < 1:
        faceInfo = getFace()
        facefile = faceInfo['file']
        if faceInfo['facenum'] == desiredface:
            i+=1
    genDisplay({'text': str(desiredkey),\
        'xPos': 0, 'yPos': 7, 'heightCm': 1.5*heightMult, 'color': 'white'}).draw()
    drawface.image = facefile
    drawface.pos = (centerX, centerY)
    drawface.draw()

    win.flip()

    time.sleep(30)
    
practiceTrials = 10
def practiceRound(practiceTrials):
    #start practice round
    dispInfo = {'text': 'Practice round starts in:', 'xPos': 0, 'yPos': 4, 'heightCm': 3*heightMult, 'color': 'white'}
    practiceText = genDisplay(dispInfo)
    dispInfo = {'text': '', 'xPos': 0, 'yPos': -1, 'heightCm': 3*heightMult, 'color': 'white'}
    for i in range(prePracticeBreak):
        practiceText.draw()
        dispInfo['text'] = str(prePracticeBreak-i) + ' seconds'
        genDisplay(dispInfo).draw()
        win.flip()
        time.sleep(1)
    
    for i in range(practiceTrials):
        win.flip()
        time.sleep(1)
        
        cross.draw()
        win.flip()
        time.sleep(0.1)
        
        win.flip()
    
        delay = random.randint(6,16)/10
    
        time.sleep(delay)
    
        faceInfo = getFace()
        
        facefile = faceInfo['file']
        drawface.image = facefile

        drawface.draw()

        win.flip()

        keys = event.waitKeys(timeStamped = True) 

        key = keys[0]

        if key[0] == 'escape':
            core.quit()
        
        if checkcorrect(key[0], faceInfo['facenum']):
            genDisplay({'text': 'Correct!',\
                'xPos': 0, 'yPos': 0, 'heightCm': 1.5*heightMult, 'color': 'white'}).draw()
        else:
            feedbackBeep.play()
    dispInfo = {'text': 'Experiment starts in:', 'xPos': 0, 'yPos': -6, 'heightCm': 3*heightMult, 'color': 'white'}
    endpractice2 = genDisplay(dispInfo)
    dispInfo = {'text': '', 'xPos': 0, 'yPos': -10, 'heightCm': 3*heightMult, 'color': 'white'}
    for i in range(postPracticeBreak):
        endpractice2.draw()
        dispInfo['text'] = str(postPracticeBreak-i) + ' seconds'
        genDisplay(dispInfo).draw()
        win.flip()
        time.sleep(1)
 


#correct = 0
#incorrect = 1

learningPeriod(13, "V")
learningPeriod(15, "B")
learningPeriod(17, "N")
practiceRound(20)

run = 0
mistakes = 0

mistakedict = {}
facemistakes = {}


for pair in pairs:
    win.flip()
    faceInfo = getFace()
    facefile = faceInfo['file']
    trialInfo = interpretPair(pair)
    if not inBounds(trialInfo):
        continue
    cross.draw()
    time.sleep(.1)
    win.flip()
    interstimulus = random.uniform(.3,.8)
    time.sleep(interstimulus)
    displacement = displaceCalc(trialInfo['angle'])
    if trialInfo['dir'] == 0:
        xPos = centerX + displacement*rightXMult
    elif trialInfo['dir'] ==2:
        xPos = centerX + displacement*leftXMult
    drawface.image = facefile
    drawface.pos = (xPos, centerY)
    drawface.draw()
    times = {'start': 0, 'end': 0}
    win.timeOnFlip(times, 'start')
    win.flip()
    keys = event.waitKeys(timeStamped = True)
    key = keys[0]
    if key[0] == 'escape':
        endExp()
    times['end'] = key[1]
    reactionTime = times['end'] - times['start']
    buffer = 2.3 - interstimulus - reactionTime
    if buffer > 0:
        if checkcorrect(key[0], faceInfo['facenum']):
            output = (faceInfo['facenum'], trialInfo['dir'], trialInfo['angle'], reactionTime)
            csvOutput(output, fileName)
        else:
            mistakedict[mistakes] = trialInfo
            facemistakes[mistakes] = faceInfo
            output = (faceInfo['facenum'], trialInfo['dir'], trialInfo['angle'], 0)
            csvOutput(output, fileName)
            mistakes += 1
            feedbackBeep.play()
    else:
        mistakedict[mistakes] = trialInfo
        facemistakes[mistakes] = faceInfo
        output = (faceInfo['facenum'], trialInfo['dir'], trialInfo['angle'], 0)
        csvOutput(output, fileName)
        mistakes += 1
    run += 1
    win.flip()
    if run%52 == 0 and run != 208:
        expBreak()


run2 = 0
if mistakes > 0:
    genDisplay({'text': 'These trials are a make-up of your mistakes',\
        'xPos': 0, 'yPos': centerY+5, 'heightCm': 1, 'color': 'white'}).draw()
    genDisplay({'text': 'Please follow the same instructions',\
        'xPos': 0, 'yPos': centerY+3, 'heightCm': 1, 'color': 'white'}).draw()
    genDisplay({'text': 'and press Space to continue',\
        'xPos': 0, 'yPos': centerY+1, 'heightCm': 1, 'color': 'white'}).draw()
    win.flip()
    keyyy = event.waitKeys(keyList = ['space', 'escape'])
    if keyyy[0] == 'escape': 
        win.flip()
        logging.flush()
        win.close()
        core.quit()
    l = 0
    while l < mistakes:
        win.flip()
        trialInfo = mistakedict[l]
        faceInfo = facemistakes[l]
        facefile = faceInfo['file']
        if not inBounds(trialInfo):
            continue
        cross.draw()
        time.sleep(.1)
        win.flip()
        interstimulus2 = random.uniform(.3,.8)
        time.sleep(interstimulus2)
        displacement = displaceCalc(trialInfo['angle'])
        if trialInfo['dir'] == 0:
            xPos = centerX + displacement*rightXMult
        elif trialInfo['dir'] ==2:
            xPos = centerX + displacement*leftXMult
        drawface.image = facefile
        drawface.pos = (xPos, centerY)
        drawface.draw()
        times = {'start': 0, 'end': 0}
        win.timeOnFlip(times, 'start')
        win.flip()
        keys = event.waitKeys(timeStamped = True)
        key2 = keys[0]
        if key2[0] == 'escape':
            endExp()
        times['end'] = key2[1]
        reactionTime = times['end'] - times['start']
        buffer2 = 2.3 - interstimulus2 - reactionTime
        if buffer2 > 0:
            if checkcorrect(key2[0], faceInfo['facenum']):
                output = (faceInfo['facenum'], trialInfo['dir'], trialInfo['angle'], reactionTime)
                csvOutput(output, fileName)
            else:
                mistakedict[mistakes] = trialInfo
                facemistakes[mistakes] = faceInfo
                output = (faceInfo['facenum'], trialInfo['dir'], trialInfo['angle'], 0)
                csvOutput(output, fileName)
                mistakes += 1
                feedbackBeep.play()
        else:
            mistakedict[mistakes] = trialInfo
            facemistakes[mistakes] = faceInfo
            output = (faceInfo['facenum'], trialInfo['dir'], trialInfo['angle'], 0)
            csvOutput(output, fileName)
            mistakes += 1
        run2 += 1
        l += 1
        win.flip()
        if len (dirExclusions) == 0 and run2%52 == 0:
            expBreak()

        
strmistakes = str(mistakes)
print(strmistakes + ' mistakes')
endExp()


