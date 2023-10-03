# Set up
Run the .bat scripts in order on your first run. These will automatically set up a compatible Anaconda environment.

Once the environment has been set up, you shouldn't need to repeat the setup process again. 

The #3 .bat script will run the battery and automatically activate the python environment.

REQUIREMENTS: 

Anaconda

Ian's TODO:

### Refactoring
  - Create library of common functions
  - Rearrange the filesystem to make task scripts accessible at a higher level
  - Get rid off all unnecessary code (a lot)
  - Unit testing all functions
  - Document everything 
  - Create low level task schema (abstract class)
### New features
  - Create common config file which is human readable
  - Have a script to edit the config file through a gui
  - Modernize the data collection (SQL)?
  - Set new data collection to run in parallel to not interrupt current collection
  - SQL server??? 

####################### Notes specific to mp4 studies (e.g., movie watching, audiobook, music), written by Bronte ##########################################

Ok so here in the overview for how it all works (assume 3 clips):
- Each subject has a predefined probe order for each clip and this is set up and read in from 'counterbalanced_orders_n{nparticipants}.csv' (e.g., subject 17 has the order 0,3,1)
- When that subject number (e.g., 17) is entered into the GUI, probe orders are set to 0,3,1 for each clip respectively
- Each of these orders corresponds to a row number in 'resources/Movie_Task/csv/probe_orders.csv'
	- each row contains the time in seconds when each probe will be presented (so if there are 4 probes, 4 columns)
		- e.g. order 0 stops at 60,200,300,420 so the first clip would stop at those times to present a probe
- This information is also used to create the output file at the end (again, it uses subject number to get all this info)
- 'resources/Movie_Task/csv/probe_durations.csv' has the same structure as 'resources/Movie_Task/csv/probe_orders.csv' but is the duration between each probe in seconds
	- this is used in output file

Ok, so for making new studies, the following python scripts are relevant:
- Tasks/mainscript.py: this script calls the movieTask.py script and handles general things like the GUI, order of task presentation etc.
- Tasks/taskScripts/movieTask.py: this script deals with the specifics of presenting movie/mp4 stimuli.
- Tasks/taskScripts/resources/Movie_Task/csv/create_probe_orders_movie_task.py: this is the script that generates probe orders specific to your study requirements.

The following resources are also important:
- Tasks/taskScripts/resources/Movie_Task/videos: this is where you should put your stimuli.
- Tasks/taskScripts/resources/Movie_Task/csv/questions.csv: this is where you should put your comprehension questions if using
	- put the question in the 'question' column, the options in the 'options' column and which response is correct in the 'correct' column

Making new probe orders using Tasks/taskScripts/resources/Movie_Task/csv/create_probe_orders_movie_task.py:
- User input begins on line 166, where the heading says "User Input"
	- you need to change the 'directory' variable to absolute path of where you want to save probe order and duration csv files, which should be in Tasks/taskScripts/resources/Movie_Task/csv
	- you then need to change the experiment parameters based on your study requirements
		- set num_clips to how many clips you have in total in the study
		- set preclip_min to how many minutes you want to pass before the first probe is presented to any participant
		- set clip_min to how many minutes of probe coverage you need for each clip
		- set probe_coverage_duration_min to how often you want to interupt each person (this is just a rough guideline)
		- set probe_interval to how many seconds you want between probes across participants (e.g, 10 or 20 seconds)
		- set min_participant_break to the min amount of seconds you want between probes for each person
		- set num_samples_per_interval to how many probes you want at each probe interval across participants at the end of the study

This script will then use this parameters to calculate how many probe orders you need and how many participants.
It will generate random orders accordingly while making sure that certain requirements are adhered to including:
- making sure than within each order, probe durations do not repeat and that there is sufficient spacing between each probe within an order

It will save the following csvs:
- probe_order.csv: this is the unique probe orders that will be used (number of orders determined using parameters above); each row is a different order and each column is one probe.
- probe_duration.csv: this is the duration between each probe (same format as probe_order).
- counterbalanced_orders_n{num_participants_full_sample}.csv: this is the counterbalanced probe order across the sample for each clip; this will have a column for participant_number and then a column for each clip.
	-  this is generated between lines 250 and 362 under heading 'counterbalancing'
		- first section selects orders per clip across the min number of participants for full coverage (e.g., 6 participants), ensuring that for any one person, clip orders are not the same between clips
		and that, for each clip every N participants, one of the orders is used.
		- next section then randomizes this order X number of times to reach full sample.

Modifying Tasks/mainscript.py to work with new stimuli:
- scroll right down to the section starting with "if __name__ == "__main__":" (line 339)
	- these are the only lines that will need changing: 
	probeorders = pd.read_csv("taskScripts/resources/Movie_Task/csv/counterbalanced_orders_n120.csv") # change this to be the filename generated using create_probe_orders_movie_task.py explained above.

	# this will need updating if there are a different number of clips (remove if less than 3, add more if more than 3)
	# this is reading in probe order for each clip based on subject number inputted to GUI by user.
        probe1_version = probeorders.loc[probeorders['participant_number'] == int(metacoll.INFO['Subject']), 'Clip 1'].values 
        probe2_version = probeorders.loc[probeorders['participant_number'] == int(metacoll.INFO['Subject']), 'Clip 2'].values
        probe3_version = probeorders.loc[probeorders['participant_number'] == int(metacoll.INFO['Subject']), 'Clip 3'].values
    
        # the name of each mp4 clip will need changing as well as the number of clips if using a different number than 3 (remove if less than 3, add more if more than 3)
        movieTask1 = task(taskScripts.movieTask, datafile, ["resources/Movie_Task/csv/probe_orders.csv","resources/Movie_Task/videos/run1.mp4"],"Movie Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),'resources//Movie_Task//csv//sorted_filmList.csv', 1,int(probe1_version))
        movieTask2 = task(taskScripts.movieTask, datafile, ["resources/Movie_Task/csv/probe_orders.csv","resources/Movie_Task/videos/run2.mp4"],"Movie Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),'resources//Movie_Task//csv//sorted_filmList.csv', 2,int(probe2_version))
        movieTask3 = task(taskScripts.movieTask, datafile, ["resources/Movie_Task/csv/probe_orders.csv","resources/Movie_Task/videos/run3.mp4"],"Movie Task",  metacoll.sbINFO.data, int(metacoll.INFO['Block Runtime']),'resources//Movie_Task//csv//sorted_filmList.csv', 3,int(probe3_version))

	# this will only need changing if different number of clips used
        moviegroup = [movieTask1,movieTask2,movieTask3]

	# if you want the clip order to be randomized, you should uncomment out the following:
	random.shuffle(fulltasklist)

Modifying Tasks/taskScripts/movieTask.py to work with new stimuli:
	- modify instructions1 and instructions2 if you are using something other than audiobooks. 
		- currently set up so instructions1 is shown before 1st clip, instructions2 is shown after every other clip but this is set based on filename which might not be appropriate if you are randomizing clip presentation.
			- if you are randomizing presentation, just have one set of instructions and remove if statement:
				-     if filename[1] == "resources/Movie_Task/videos/run1.mp4":
        					stim.setText(instructions1)
    				      else:
        					stim.setText(instructions2)
	- this script is currently set up to present comprehension questions at the end of each clip.
		- the present_comprehension_question function presents the questions
			- questions presented are set in Tasks/taskScripts/resources/Movie_Task/csv/questions.csv file (see above)
		- the save_csv function is for saving responses to these questions
		- if you don't need comphrension questions, you can remove lines 218 to 245
			- these lines present questions at the end of each clip and save responses
		- if you want to present your own questions:
			- modify if statements to match the clip name
				- "if filename[1] == "resources/Movie_Task/videos/run1.mp4":"
			- repeat the responses_data and save_csv lines for as many questions you have for each clip and modify the question number

## ANALYSIS
Run Analysis/analysis.py to merge all ESQ output as well as comprehension output.
- creates a column for correct per run and a column for correct over all

Things to change/ might need to change:
- it reads in the counterbalanced probe order csv that is generated using Tasks/taskScripts/resources/Movie_Task/csv/create_probe_orders_movie_task.py
	- so this needs to match the filename created using that script
- the name of the output file
	- currently set to 'Analysis/audio_esq_output.csv' but can change to be specific to project
- if there are a different number of clips to 3, you would need to add to this section:
"probe1_version = probeversions_df.loc[probeversions_df['participant_number'] == int(subject), 'Clip 1'].values
 probe2_version = probeversions_df.loc[probeversions_df['participant_number'] == int(subject), 'Clip 2'].values
 probe3_version = probeversions_df.loc[probeversions_df['participant_number'] == int(subject), 'Clip 3'].values
 probeversions = [probe1_version[0], probe2_version[0], probe3_version[0]]"

- this section can be changed to have names that work for your project / whatever names are used in comprehension outputs:
"if task_name in ("Movie Task-Movie Task-run1", "Movie Task-run1"):
                            
                            line_dict["Task_name"] = "run1.mp4"
                            linenumber = 0

                        if task_name in ("Movie Task-Movie Task-run2", "Movie Task-run2"):
                            
                            line_dict["Task_name"] = "run2.mp4"
                            linenumber = 1
                        if task_name in ("Movie Task-Movie Task-run3", "Movie Task-run3"):
                            
                            line_dict["Task_name"] = "run3.mp4""
        


