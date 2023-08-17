#Written by Brontë McKeown and Theodoros Karapanagiotidis
from psychopy import visual 
import psychopy
psychopy.prefs.hardware['audioLib'] = ['PTB', 'pyo','pygame']
from matplotlib.pyplot import pause

import pandas as pd
from psychopy import gui, data, core,event
from taskScripts import ESQ
import os.path

import csv
import random

###################################################################################################
def save_csv(responses_data, participant_id):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    log_folder = os.path.join(current_directory, "..", "comp_file")
        
    csv_path = os.path.join(log_folder, f"{participant_id}_comp_output.csv")
    
    with open(csv_path, "w", newline="") as csvfile:
        fieldnames = ['idno', 'videoname', 'qnumber', 'response', 'correctness']
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(responses_data)

def present_comprehension_question(win, stim, question_number, participant_id, videoname, responses_data):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    questions_file_path = os.path.join(current_directory, "resources", "Movie_Task", "csv", "questions.csv")
    
    # Load questions from the CSV file
    with open(questions_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        questions = list(csv_reader)

    question_data = questions[question_number - 1]
    question_text = question_data['question']
    options = question_data['options'].split('|')
    correct_option = int(question_data['correct'])  # Convert to an integer

    # Present the question
    question_text = f"{question_text}\n"
    for idx, option in enumerate(options, start=1):
        question_text += f"{option}\n"

    stim.setText(question_text)
    stim.draw()
    win.flip()
    keys = event.waitKeys(keyList=[str(i) for i in range(1, len(options) + 1)])
    response = keys[0]  # Store the selected option

    correctness = "correct" if int(response) == correct_option else "incorrect"

    # Store the response data
    responses_data.append({
        'idno': participant_id,
        'videoname': videoname,
        'qnumber': question_number,
        'response': response,
        'correctness': correctness
    })
    return responses_data
    

def runexp(filename, timer, win, writer, resdict, runtime,dfile,seed,probever, participant_id):
    
    # set screen width and height based on window size information
    screen_width, screen_height = win.size
    
    # writer is for recording ESQ
    writera = writer[1]
    writer = writer[0]
    random.seed(seed) # this isn't important unlesss randomizing but keeping
    
    # write start time to dictionary for recording in log file
    resdict['Timepoint'], resdict['Time'] = 'Movie Task Start', timer.getTime()
    writer.writerow(resdict)
    resdict['Timepoint'], resdict['Time'] = None,None
    
    # Initialize a list to store the participant's responses to comp questions
    responses_data = []

    # user can update start screen text here if required
    # this comes after general introduction to task which is set at a higher level
    # see "Movie-Battery\Tasks\taskScripts\resources\group_inst\Movie_Task"
    
    # You can use if statement below to show slightly different instructions
    # depending on whether it is the first time or not
    instructions1 = """Throughout the audiobook, you will be prompted with questions about your thoughts.

                    \nPlease answer these questions as quickly and honestly as possible. There are no right or wrong answers.

                    \nUse the arrow keys to answer and enter/return key to submit your response. 
                    """
                    
    instructions2 = """You will now listen to the next clip. As before, while you listen, you will be prompted with questions about your thoughts.

                        \nPlease answer these questions as quickly and honestly as possible. There are no right or wrong answers.

                        \nUse the arrow keys to answer and enter/return key to submit your response. 
                        """
    # This is shown next
    start_screen =      """If you are ready to start listening, press enter.
                            """
    # create text stimuli to be updated for instructions.
    stim = visual.TextStim(win, "",
                           font='Arial',
                           anchorHoriz='center', anchorVert='center', wrapWidth=screen_width*0.6, ori=0, 
                           color='black', colorSpace='rgb', opacity=1, 
                           languageStyle='LTR',
                           depth=0.0)

    # update text stim to include instructions for task. 
    if filename[1] == "resources/Movie_Task/videos/test1.mp4":
        stim.setText(instructions1)
    else:
        stim.setText(instructions2)
    stim.draw()
    win.flip()
    # Wait for user to press enter to continue. 
    event.waitKeys(keyList=(['return']))

    # update text stim to include start screen for task. 
    stim.setText(start_screen)
    stim.draw()
    win.flip()
    
    # Wait for user to press enter to continue. 
    event.waitKeys(keyList=(['return']))
    
    # Write when it's initialized
    resdict['Timepoint'], resdict['Time'] = 'Movie Init', timer.getTime()
    writer.writerow(resdict)
    resdict['Timepoint'], resdict['Time'] = None,None
    
    # select video and select probe time points from filename variable
    trialvideo = os.path.join(os.getcwd(),"taskScripts",filename[1])
    trialsplits = pd.read_csv(os.path.join(os.getcwd(),"taskScripts",filename[0]))

    # store video name
    videoname = filename[1].rsplit("/",1)[-1]
    trialname = "Movie Task-" + trialvideo.split(".")[0].split("/")[-1]
    
    # select probe timings using number inputted into GUI (selects row)
    vern = probever
    trialsplit = trialsplits.iloc[vern]

    # present film using moviestim
    resdict['Timepoint'], resdict['Time'],resdict['Auxillary Data'] = 'Movie Start', timer.getTime(), videoname
    writer.writerow(resdict)
    resdict['Timepoint'], resdict['Time'],resdict['Auxillary Data'] = None,None,None
    
    # present loading text while it's loading
    text_inst = visual.TextStim(win=win, name='text_1',
                        text='Loading...',
                        font='Arial',
                        pos=(0, 0), height=0.1, wrapWidth=None, ori=0.0, 
                        color='black', colorSpace='rgb', opacity=None, 
                        languageStyle='LTR',
                        depth=0.0)
    text_inst.draw()
    win.flip()
    
    # present movie
    mov = visual.MovieStim3(win, trialvideo, size=(screen_width, screen_height), flipVert=False, flipHoriz=False, loop=False)
    
    # initiate clock for below
    expClock = core.Clock()
    
    timelimit = trialsplit[0] # time limit based on probe timings
    trialsplit = trialsplit.diff()[1:]
    # esqshown = False
    resettime = True
    en = 0
    timelimitpercent = int(100*(timelimit/runtime))
    
    while mov.status != visual.FINISHED:
        if expClock.getTime() < runtime:
            # time = expClock.getTime()
            if expClock.getTime() > timelimit:
                try:
                    timelimit = trialsplit.values[en]
                except:
                    timelimit = 10000
                    pass
                en += 1
                mov.pause()
                #timepause = runtime - expClock.getTime() # record time of pausing
                writera.writerow({'Timepoint':'EXPERIMENT DATA:','Time':'Experience Sampling Questions'})
                writera.writerow({'Timepoint':'Start Time','Time':timer.getTime()})
                
                # present ESQ
                ESQ.runexp(None,timer,win,[writer,writera],resdict,None,None,None,movietype=trialname)
                
                # record ESQ
                resdict['Assoc Task'] = None
                resdict['Timepoint'], resdict['Time'],resdict['Auxillary Data'] = 'Movie prompt {} {}'.format(en,videoname), timer.getTime(), timelimitpercent
                writer.writerow(resdict)
                resdict['Timepoint'], resdict['Time'],resdict['Auxillary Data'] = None,None,None             
                
                text_inst.draw()
                win.flip()

                # continue playing
                mov.play()
                resettime = True
                # esqshown = True

            if resettime:
                expClock.reset()
                resettime = False
            mov.draw()
            win.flip()
        else:
            break
        
    # at the end of each clip, present comprehension questions
    if filename[1] == "resources/Movie_Task/videos/test1.mp4":
        responses_data = present_comprehension_question(win, stim, 1, participant_id, videoname, responses_data)
        save_csv(responses_data, participant_id)
        responses_data = present_comprehension_question(win, stim, 2, participant_id, videoname, responses_data)
        save_csv(responses_data, participant_id)
        responses_data = present_comprehension_question(win, stim, 3, participant_id, videoname, responses_data)
        save_csv(responses_data, participant_id)
        responses_data = present_comprehension_question(win, stim, 4, participant_id, videoname, responses_data)
        save_csv(responses_data, participant_id)
    if filename[1] == "resources/Movie_Task/videos/test2.mp4":
        responses_data = present_comprehension_question(win, stim, 5, participant_id, videoname, responses_data)
        save_csv(responses_data, participant_id)
        responses_data = present_comprehension_question(win, stim, 6, participant_id, videoname, responses_data)
        save_csv(responses_data, participant_id)
        responses_data = present_comprehension_question(win, stim, 7, participant_id, videoname, responses_data)
        save_csv(responses_data, participant_id)
        responses_data = present_comprehension_question(win, stim, 8, participant_id, videoname, responses_data)
        save_csv(responses_data, participant_id)
    if filename[1] == "resources/Movie_Task/videos/test3.mp4":
        responses_data = present_comprehension_question(win, stim, 9, participant_id, videoname, responses_data)
        save_csv(responses_data, participant_id)
        responses_data = present_comprehension_question(win, stim, 10, participant_id, videoname, responses_data)
        save_csv(responses_data, participant_id)
        responses_data = present_comprehension_question(win, stim, 11, participant_id, videoname, responses_data)
        save_csv(responses_data, participant_id)
        responses_data = present_comprehension_question(win, stim, 12, participant_id, videoname, responses_data)
        save_csv(responses_data, participant_id)

    return trialname
