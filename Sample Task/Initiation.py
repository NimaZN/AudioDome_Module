# Initiation __________________________________________________________
# Packages and External Functions
from AudioDome_Module import *
from Functions import *
import pandas as pd
import numpy as np
import os
import re
import random

main_directory = os.getcwd()
# IMPORTANT: Reserved variable names! Don't use these names as new variables in your code.
#   clientName
#   ip
#   port

# Arduino communication setup
board, fixation_led_mobile, fixation_led_origin = arduino_comm("COM8") # output port may vary.

# Participant info__________________________________________________________
# Participant ID: Put the number you give to the participant on the master list.
ID = input("Plaese enter participant ID (put the number given to the participant on the master list):")
data_directory = os.path.join(main_directory, "Data")
if not os.path.exists(data_directory):
    os.mkdir(data_directory)
participant_directory = os.path.join(data_directory, "Participant_"+ID)
if not os.path.exists(participant_directory):
    os.mkdir(participant_directory)
    
# Experiment and Parameters Setup__________________________________________________________
# These parameters shuold be similar to paramters used for generating the stimuli in MATLAB.
condition_repetition_count = 20 # number of repetition times per condition: positive even integer
half_cue_cnt = 10 # number of unrepeated cues for each auditory object
block_cnt = 5 # number of blocks
settling_delay = 0.2 # settling delay required for the commands to be communicated to the AudioDome
burst_len = 0.45
SOA = 0.2
resp_collect_init = burst_len+SOA
RespT_max = 1.5
ITI = 0.2
timeout = burst_len+RespT_max # Response collection timeout (collection starts after the onset of the second noise burst)
trial_duration = burst_len+SOA+burst_len+RespT_max

# Summary print
print("Experiment Information and Parameters:")
print(f"Participant ID: {ID}")
print(f"Repetition Count: {condition_repetition_count}")

# Conditions Setup__________________________________________________________
# All possible conditions information
conditions_base = pd.DataFrame([["1", "nearest", "low", "nearest", "low"],
                           ["2", "nearest", "wide", "nearest", "wide"],
                           ["3", "nearest", "low", "ambi", "low"],
                           ["4", "nearest", "wide", "ambi", "wide"],
                           ["catch", "nearest", "low", "nearest", "low"]],
                          columns=["Condition", "Burst1Panning", "Burst1FreqContent", "Burst2Panning", "Burst2FreqContent"])

ProbePoints = {
    "C":    {"azi": 0,      "ele": 0.03,    "channel": 1,   "up_ch": 23,    "down_ch": 76,  "catch_ele_diff": 61.02},
    "L4":   {"azi":31.72,   "ele": 0,       "channel": 3,   "up_ch": 44,    "down_ch": 78,  "catch_ele_diff": 93.99}, # catch channels do not align with the azimuth angle
    "R4":   {"azi":-31.72,  "ele": 0,       "channel": 15,  "up_ch": 54,    "down_ch": 86,  "catch_ele_diff": 93.99}, # catch channels do not align with the azimuth angle
    "L6":   {"azi": 69.09,  "ele": 0,       "channel": 4,   "up_ch": 45,    "down_ch": 88,  "catch_ele_diff": 93.78}, # catch channels do not align with the azimuth angle
    "R6":   {"azi": -69.09, "ele": 0,       "channel": 14,  "up_ch": 53,    "down_ch": 91,  "catch_ele_diff": 93.78}, # catch channels do not align with the azimuth angle
    "L8":   {"azi": 90,     "ele": 0.46,    "channel": 5,   "up_ch": 46,    "down_ch": 79,  "catch_ele_diff": 79.63}, # catch channels do not align with the azimuth angle
    "R8":   {"azi": -90,    "ele": 0.03,    "channel": 13,  "up_ch": 52,    "down_ch": 85,  "catch_ele_diff": 78.86} # catch channels do not align with the azimuth angle
}

# Auditory Scenes Setup__________________________________________________________
# Experiment Scenes
# scene 1
mainScene1 = scene(1, "Elevation Discriminataion Task - SC low vs. SC low scene")
mainScene1.add_object(1,"Obj1_low-SC")
mainScene1.add_object(2,"Obj2_low-SC")

# scene 2
mainScene2 = scene(2, "Elevation Discriminataion Task - SC wide vs. SC wide scene")
mainScene2.add_object(1,"Obj1_wide-SC")
mainScene2.add_object(2,"Obj2_wide-SC")

# scene 3
mainScene3 = scene(3, "Elevation Discriminataion Task - SC low vs. ambi low scene")
mainScene3.add_object(1,"Obj1_low-SC")
mainScene3.add_object(2,"Obj2_low-ambi")

# scene 4
mainScene4 = scene(4, "Elevation Discriminataion Task - SC wide vs. ambi wide scene")
mainScene4.add_object(1,"Obj1_wide-SC")
mainScene4.add_object(2,"Obj2_wide-ambi")

# scene 5 - catch
mainScene5 = scene(5, "Elevation Discriminataion Task - SC low vs. SC low scene - catch")
mainScene5.add_object(1,"Obj1_low-SC")
mainScene5.add_object(2,"Obj2_low-SC")

cond2scene = {
    "1":    mainScene1,
    "2":    mainScene2,
    "3":    mainScene3,
    "4":    mainScene4,
    "catch":mainScene5
}

mainScenes = [mainScene1,
              mainScene2,
              mainScene3,
              mainScene4,
              mainScene5]

for Scene in mainScenes:
    for Obj in Scene.objects[1:]:
        # set panning
        if re.match(r".*SC", Obj.name):
            panning_acr = "SC"
            object_panning = "nearest"
        elif re.match(r".*ambi", Obj.name):
            panning_acr = "ambi"
            object_panning = "ambi"

        Obj.set_panning(object_panning)

        # add cues
        if re.match(r".*low.*", Obj.name):
            object_freq = "low"
        elif re.match(r".*wide.*", Obj.name):
            object_freq = "wide"
        
        for cue_idx in range(1, half_cue_cnt+1):
            Obj.add_cue(cue_idx, f"stim_{cue_idx}_{object_freq}-{panning_acr}_first.wav")
        
        for cue_idx in range(half_cue_cnt+1, 2*half_cue_cnt+1):
            Obj.add_cue(cue_idx, f"stim_{cue_idx}_{object_freq}-{panning_acr}_second.wav")

        Obj.select_cue(1)
        

# Instruction scene
instructionScene = scene(6, "Instructions for the Elevation Discrimination Task")
instructionScene.add_object(1,"Instructional Sounds")
instructionScene.objects[1].add_cue(1, "Block_Start.wav")
instructionScene.objects[1].set_elevation(90)
instructionScene.objects[1].set_gain(-20)


# Conditions and Trials Setup__________________________________________________________
# Conditions
conditions = pd.DataFrame(columns={})
for point in ProbePoints:
    conditions_temp = conditions_base.copy()
    conditions_temp.insert(0, "ID", ID)
    conditions_temp.insert(1, "ProbePoint", point)
    conditions_temp.insert(len(conditions_temp.columns), "azi", ProbePoints[point]["azi"])
    conditions_temp.insert(len(conditions_temp.columns), "ele", ProbePoints[point]["ele"])
    conditions_temp.insert(len(conditions_temp.columns), "channel", ProbePoints[point]["channel"])
    conditions_temp.insert(len(conditions_temp.columns), "up_ch", ProbePoints[point]["up_ch"])
    conditions_temp.insert(len(conditions_temp.columns), "down_ch", ProbePoints[point]["down_ch"])
    conditions_temp.insert(len(conditions_temp.columns), "catch_ele_diff", ProbePoints[point]["catch_ele_diff"])
    conditions = pd.concat([conditions, conditions_temp], ignore_index=True)

# Trials random cue assignment
trials = pd.DataFrame(columns={})
first_cues_idx = list(range(1, half_cue_cnt+1))
second_cues_idx = list(range(half_cue_cnt+1, 2*half_cue_cnt+1))
for idx, condition in conditions.iterrows():
    # first burst presented first
    rand_first_cues = first_cues_idx.copy()
    random.shuffle(rand_first_cues)
    rand_second_cues = second_cues_idx.copy()
    random.shuffle(rand_second_cues)
    Burst1_cue_idx = rand_first_cues+rand_second_cues
    # second burst presented first
    rand_first_cues = first_cues_idx.copy()
    random.shuffle(rand_first_cues)
    rand_second_cues = second_cues_idx.copy()
    random.shuffle(rand_second_cues)
    Burst2_cue_idx = rand_second_cues+rand_first_cues
    # order indicator
    FirstBurstPresented = [1]*half_cue_cnt+[2]*half_cue_cnt
    # movement direction
    if condition["Condition"] == "catch":
        MovementDir = ["down"]*half_cue_cnt+["up"]*half_cue_cnt
    else:
        MovementDir = [0]*(half_cue_cnt*2)

    # block assignment
    BlockNum = list(range(1,block_cnt+1))*(half_cue_cnt*2//block_cnt)
    # placement in trial information
    trial_temp = pd.DataFrame([condition.copy()]*(half_cue_cnt*2)) 
    trial_temp["FirstBurstPresented"] = FirstBurstPresented
    trial_temp["MovementDir"] = MovementDir
    trial_temp["BlockNum"] = BlockNum
    trial_temp["Burst1_cue_idx"] = Burst1_cue_idx
    trial_temp["Burst2_cue_idx"] = Burst2_cue_idx
    trials = pd.concat([trials, trial_temp], ignore_index=True)

conditions.to_csv(os.path.join(participant_directory, f"P{ID}_conditions.csv"), index=False)
trials.to_csv(os.path.join(participant_directory, f"P{ID}_trials.csv"), index=False)

del BlockNum
del Burst1_cue_idx, Burst2_cue_idx
del condition, condition_repetition_count, conditions_base, conditions_temp
del cue_idx, first_cues_idx, second_cues_idx, FirstBurstPresented, half_cue_cnt, idx, MovementDir, rand_first_cues, rand_second_cues
del Scene, Obj, object_freq, object_panning, panning_acr, point
del trial_temp