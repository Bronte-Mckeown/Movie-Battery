
import os
import csv
import numpy as np
import pandas as pd
os.chdir("C:\\Users\\bront\\Documents\\CanadaPostdoc\\audio\\Movie-Battery")
graddict = {}
global sentimentdict
sentimentdict = {}

n_probes_per_clip = 4
num_esq = 16

probeorders= pd.read_csv("Tasks/taskScripts/resources/Movie_Task/csv/probetimes_orders_test.csv",header=None, index_col = False).to_dict()
probedurs = pd.read_csv("Tasks/taskScripts/resources/Movie_Task/csv/probe_durations_test.csv",header=None).to_dict()

line_dict= {"Task_name":None,
        "Participant #":None,
        "Runtime_mod":None,
        "Movie_time":None,
        "Absorption_response":None,
        "Other_response":None,
        "Problem_response":None,
        "Words_response":None,
        "Sounds_response":None,
        "Images_response":None,
        "Past_response":None,
        "Distracting_response":None,
        "Focus_response":None,
        "Intrusive_response":None,
        "Deliberate_response":None,
        "Detailed_response":None,
        "Future_response":None,
        "Emotion_response":None,
        "Self_response":None,
        "Knowledge_response":None,
        "Probe Version":None,
        "Probe Number":None,
        "Probe Time": None,
        "Probe Duration":None,
        }

if os.path.exists(os.path.join(os.getcwd(),"Analysis/output.csv")):
        os.remove(os.path.join(os.getcwd(),"Analysis/output.csv"))

with open(os.path.join(os.getcwd(),"Analysis/output.csv"), 'a', newline="") as outf:
    wr = csv.writer(outf)
    wr.writerow(list(line_dict.keys()))


def sortingfunction(exp,row,resps):
    global prevtime
    global en
    if exp == "Experience Sampling Questions":
        # Collect response time
        
        print(row)
        if row[3].split("_")[1] == "start":
            prevtime = float(row[1])
        elif row[3].split("_")[1] == "response":
            resptime = float(row[1]) - prevtime  
            resps[exp]["Response Time"].append(resptime)
        pass


for file in os.listdir("Tasks/log_file"):
    
    ftemp = file.split('.')[0]
    resps = {"Experience Sampling Questions":{"Response Time":[]},
             "GoNoGo Task":{"Response Time":[], "Accuracy - Go":[],"Accuracy - NoGo":[]},
             "Finger Tapping Task":{"Response Time":[], "Accuracy":[]},
             "Two-Back Task-faces":{"Response Time":[], "Accuracy":[]},
             "Two-Back Task-scenes":{"Response Time":[], "Accuracy":[]},
             "One-Back Task":{"Response Time":[], "Accuracy":[]},
             "Zero-Back Task":{"Response Time":[], "Accuracy":[]},
             "Hard Math Task":{"Response Time":[], "Accuracy":[]},
             "Easy Math Task":{"Response Time":[], "Accuracy":[]},
             "Friend Task":{"Response Time":[], "Sentiment":[]},
             "You Task":{"Response Time":[], "Sentiment":[]}
             }

    if not 'full' in ftemp.split('_'):
        line_dict= {"Task_name":None,
        "Participant #":None,
        "Runtime_mod":None,
        "Movie_time":None,
        "Absorption_response":None,
        "Other_response":None,
        "Problem_response":None,
        "Words_response":None,
        "Sounds_response":None,
        "Images_response":None,
        "Past_response":None,
        "Distracting_response":None,
        "Focus_response":None,
        "Intrusive_response":None,
        "Deliberate_response":None,
        "Detailed_response":None,
        "Future_response":None,
        "Emotion_response":None,
        "Self_response":None,
        "Knowledge_response":None,
        "Probe Version": None,
        "Probe Number": None,
        "Probe Time": None,
        "Probe Duration": None
        }
        import re
        probe_iteration = 0
        _,_,subject,seed = ftemp.split("_")
        subject = "subject_"+str(int(re.findall(r'\d+', subject)[0]))
        line_dict["Participant #"] = subject
        readstart = False
        initstart = True
        skipstart = False
        with open(os.path.join("Tasks/log_file",file)) as f:
            reader = csv.reader(f)
            
            # loop over rows in every log file with enumerate
            for en,row in enumerate(reader):
                # if it's the second row, extra probe order versions
                if en == 2:
                    probeversions = [row[1],row[2],row[3]]
                    # v = 0
                
                # on first row, this will always be false
                # but gets set to true below once 1st row value == 'start time'
                # from then on, goes into this if statement
                if readstart:
                    # if second column is not experience sampling questions
                    if not row[1] == "Experience Sampling Questions":
                        # and if skipstart is true
                        if skipstart:
                            # set readstart to false
                            readstart = False
                            skipstart = False
                        
                        # movie time is kinda pointless
                        # it is the difference between 'start time' of movie task and 'start time' of first ESQ item
                        line_dict["Movie_time"] = float(row[1])-float(starttime)
                        readstart = False
                    else:
                        skipstart = True;
                
                
                if row[0] == "Start Time":
                    starttime = row[1]
                    readstart = True
                
                if row[0] == 'Runtime Mod':
                    line_dict["Runtime_mod"] = row[1]
                
                if row[0] == 'ESQ':
                    enum +=1
                    # when ect is equal to 0, ready to receive ESQ data
                    if ect == 0:
                        task_name = row[10] # store task name
                        # increase probe_iteration by 1
                        probe_iteration += 1
                        if line_dict["Task_name"] is not None:
                            # when task name changes, probe_iteration is reset to zero
                            if line_dict["Task_name"] != task_name and "Movie Task-" + line_dict["Task_name"] != task_name:
                                
                                # v += 1
                                probe_iteration = 0
                        elif line_dict["Task_name"] is None:
                            probe_iteration = 0
                        line_dict["Task_name"] = task_name
                        ect = 1
                    if task_name == row[10]:
                        line_dict[row[3]]=row[4]
                    if enum == 16:
                        if task_name in ("Movie Task-Movie Task-test1", "Movie Task-test1"):
                            
                            line_dict["Task_name"] = "Movie Task-test1"
                            linenumber = 0

                        if task_name in ("Movie Task-Movie Task-test2", "Movie Task-test2"):
                            
                            line_dict["Task_name"] = "Movie Task-test2"
                            linenumber = 1
                        if task_name in ("Movie Task-Movie Task-test3", "Movie Task-test3"):
                            
                            line_dict["Task_name"] = "Movie Task-test3"
                            linenumber = 2

                        line_dict["Probe Version"] = probeversions[linenumber]
                        line_dict["Probe Number"] = probe_iteration

                        line_dict["Probe Duration"] = probedurs[probe_iteration][int(probeversions[linenumber])]
                        line_dict["Probe Time"] = probeorders[probe_iteration][int(probeversions[linenumber])+1]

                        with open("Analysis/output.csv", 'a', newline="") as outf:
                            wr = csv.writer(outf)
                            wr.writerow(list(line_dict.values()))
                            ect = 0
                            enum = 0
                        task_name = row[10]
                        line_dict[row[3]]=row[4]
                        line_dict["Task_name"] = task_name
                        skipstart = False
                    #print(row)
                else:
                    ect = 0
                    enum =0
                
        print(file)
    else:
        continue
        stats = {}
        expdict = {}
        captsubj = False
        ready = False
        resps.update({"Subject":subject})
        with open(os.path.join("Tasks/log_file",file)) as f:
            reader = csv.reader(f)
            
            for row in reader:
                
                # Subject name
                if captsubj == True:
                    stats.update({"Subject":row[2]})
                    captsubj = False
                if row[0] == "Block Runtime":
                    if row[2] == "Subject":
                        captsubj = True
                        
                # Experiment name
                elif row[0] == "EXPERIMENT DATA:":
                    expdict = {}
                    expdict.update({"Experiment":row[1]})
                    ready = False
                
                # Trigger start on next line
                elif row[0] == "Start Time":
                    ready = True
                elif ready == True:
                    if expdict["Experiment"] == 'Two-Back Task':
                        sortingfunction(expdict["Experiment"] + "-" + row[9],row,resps)  
                    else:
                        sortingfunction(expdict["Experiment"],row,resps)  
                    
                print(row)
