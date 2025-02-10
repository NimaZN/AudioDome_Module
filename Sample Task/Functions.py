# Functions __________________________________________________________
# Importing packages
import pyfirmata
import numpy as np
import keyboard
import time

# Arduino Communication Functions__________________________________________________________
# Arduino is used to control the fixation LEDs. One of the LEDs is fixed at the central speaker and the other is mobile. This experiment only uses the central LED.
# Arduino Nano should be loaded with the communication protocol before these paramters are complied.
def arduino_comm(port):
    # Port initiation
    board = pyfirmata.Arduino(port)
    fixation_led_mobile = board.get_pin("d:2:o") # Black pin
    fixation_led_origin = board.get_pin("d:4:o") # Red pin

    return board, fixation_led_mobile, fixation_led_origin

def switch_fixation_LED(fixation_point,
                        status):
    if status == "on":
        fixation_point.write(1)
        
    elif status == "off":
        fixation_point.write(0)

    return


# Experiment Functions__________________________________________________________
# Set trial parameters
def set_trial(trial_info,
              cond2scene,
              fixation_point,
              settling_delay):
    # trial_info should be a row of a dataframe including probe point panning method, location, and cue ID information
    # select the appropriate scene
    selectedScene = cond2scene[trial_info.Condition]

    # based on the panning method set the channel or (azimuth, elevation pair)
    # Burst 1
    selectedScene.objects[1].set_azimuth(trial_info.azi) # will be overwritten in nearest conditions when channel is set - just to make sure it's compatible
    selectedScene.objects[1].set_elevation(trial_info.ele) # will be overwritten in nearest conditions when channel is set - just to make sure it's compatible
    # Burst 2
    selectedScene.objects[2].set_azimuth(trial_info.azi) # will be overwritten in nearest conditions when channel is set - just to make sure it's compatible
    selectedScene.objects[2].set_elevation(trial_info.ele) # will be overwritten in nearest conditions when channel is set - just to make sure it's compatible

    # select up and down channels in catch trials
    if trial_info.Condition == "catch":
        # Burst 1
        selectedScene.objects[1].set_channel(trial_info.up_ch)
        # Burst 2
        selectedScene.objects[2].set_channel(trial_info.down_ch)
    # otherwise select the horizontal channel
    else:
        # Burst 1
        if trial_info.Burst1Panning == "nearest":
            selectedScene.objects[1].set_channel(trial_info.channel)
        # Burst 2
        if trial_info.Burst2Panning == "nearest":
            selectedScene.objects[2].set_channel(trial_info.channel)
    
    # select the cue
    selectedScene.objects[1].select_cue(int(trial_info.Burst1_cue_idx))
    selectedScene.objects[2].select_cue(int(trial_info.Burst2_cue_idx))

    # settling delay wait
    time.sleep(settling_delay)
    switch_fixation_LED(fixation_point, "on")
    return selectedScene

# Run the Trial and Collect the Response
def run_trial(selectedScene,
              fixation_point,
              resp_collect_init,
              timeout):
    
    resp = "None"
    RT = 0
    selectedScene.play()
    time.sleep(resp_collect_init)
    timeout_start = time.time()
    
    while time.time() <= timeout_start + timeout:  # making a loop waiting for single character response
        try:  # used try so that if user pressed other than the given key error will not be shown
            if keyboard.is_pressed("8"):  # if key "8" is pressed 
                resp = "up"
                RT = time.time()-timeout_start
                
            elif keyboard.is_pressed("2"):  # if key "2" is pressed 
                resp = "down"
                RT = time.time()-timeout_start
                
        except:
            break
    
    selectedScene.stop()
    switch_fixation_LED(fixation_point, "off")
    return resp, RT

# Run an entire block of trials
def run_block(cond2scene,
              instructionScene,
              Block_trials,
              fixation_point,
              resp_collect_init,
              timeout,
              ITI,
              settling_delay):
    
    # Instruction scene - participant confirmation pending
    instructionScene.objects[1].select_cue(1)
    instructionScene.play()
    proceed_block = 0

    print("_____Participant pending...")
    while True:
        try:    
            if keyboard.is_pressed("2"):  # if key "2" is pressed 
                proceed_block = 1
                break
                
        except:
            break

    if proceed_block:
        instructionScene.stop()
        time.sleep(1)
        trials = Block_trials.copy()
        trials["Response"] = np.nan
        trials["ReactionTime"] = np.nan
        print(f"\tBlock initiated successfully.")
        trial_cnt = 0
        total_trials = len(trials)
        for trial_num, trial_info in trials.iterrows():
            trial_cnt = trial_cnt+1
            print(f"\t\tTrial {trial_cnt} of {total_trials} - condition: {trial_info.Condition} at {trial_info.ProbePoint}")
            selectedScene = set_trial(trial_info, cond2scene, fixation_point, settling_delay)
            trials.at[trial_num, "Response"], trials.at[trial_num, "ReactionTime"] = run_trial(selectedScene, fixation_point, resp_collect_init, timeout)
            time.sleep(ITI)

        print(f"\tBlock finished.\n")
        return trials

    else:
        print("_____Failed to initiate the block.")
        return    