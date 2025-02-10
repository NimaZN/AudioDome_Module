# RunExperiment __________________________________________________________
# Packages and Functions
import pandas as pd
import numpy as np
import os
import re

from AudioDome_Module import *
from Functions import *

# Experiment Block Setup__________________________________________________________
def run_experiment_block(block_cnt,
                         cond2scene,
                         instructionScene,
                         trials,
                         fixation_point,
                         resp_collect_init,
                         timeout,
                         ITI,
                         settling_delay,
                         participant_directory):
    
    block_num = 1
    for file_name in os.listdir(participant_directory):
        if re.match(r"experiment_block_\d+.csv", file_name):
                block_num = block_num+1

    if block_num>block_cnt:
        print("Experiment finished!")
    else:
        proceed = input(f"Block {block_num} is about to begin. Proceed? [y/n]")
        if proceed == "y":
            print(f"Block {block_num} (out of {block_cnt}) started!")
            block_trials = trials.loc[trials["BlockNum"] == block_num].copy()
            block_trials = block_trials.sample(frac=1)
            block_response = run_block(cond2scene,
                                    instructionScene,
                                    block_trials,
                                    fixation_point,
                                    resp_collect_init,
                                    timeout,
                                    ITI,
                                    settling_delay)

            # saving responses
            block_response.to_csv(os.path.join(participant_directory, "experiment_block_"+str(block_num)+".csv"), index=False)

            # block summary
            block_response["ResponseCheck"] = block_response.apply(lambda trial: "missed" if trial["Response"] == "None" else ("correct" if trial["Response"] == trial["MovementDir"] else "incorrect"), axis=1)

            missed_cnt = sum(block_response["ResponseCheck"] == "missed")
            missed_ratio = missed_cnt/len(block_response)
            catch_trials_correct_cnt = sum(block_response.loc[block_response["Condition"] == "catch"]["ResponseCheck"] == "correct")
            if sum(block_response.loc[block_response["Condition"] == "catch"]["ResponseCheck"] != "missed") == 0:
                catch_trials_correct_ratio = 0
            else:
                catch_trials_correct_ratio = catch_trials_correct_cnt/sum(block_response.loc[block_response["Condition"] == "catch"]["ResponseCheck"] != "missed")
            mean_RT = np.mean(block_response[block_response["ResponseCheck"] != "missed"]["ReactionTime"])

            print("Block Summary___________")
            print(f"\t{missed_cnt} trials missed ({missed_ratio*100:.2f}%)")
            print(f"\t{catch_trials_correct_cnt} catch trials responded correctly ({catch_trials_correct_ratio*100:.2f}%)")
            print(f"\tMean reaction time: {1000*mean_RT:.1f} ms")

        else:
            print("Experiment paused.")
    
    return