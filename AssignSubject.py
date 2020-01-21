# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 19:18:55 2020

@author: lenovo
"""
import random
import pandas as pd
from Class import MTMSubjectMouse

# Create a list that includes all the subject mice

def getmicelist() -> list:
    """Randomize the subjects.
    """    
    subjectmice = []
    for i in range(48):
        subjectmice.append(MTMSubjectMouse(i))
    random.shuffle(subjectmice)
    return subjectmice


def getmicedict(subjectmice) -> dict:
# assign the randomized subjects to different slots in the stacks.
    MTMmice = {}
    stack1 = ["a", "b", "c", "d"]
    stack2 = ["a", "b", "c", "d"]
    for i in range(48):
        if i//6 < 4:
            slot = "s1" + stack1[i//6] + str((i+1)%6)
        else:
            slot = "s2" + stack2[i//6-4] + str((i+1)%6)
        if slot[-1] == '0':
            slot = slot[:-1]+'6'
        MTMmice[slot] = subjectmice[i]
    return MTMmice

def assigncondition(MTMmice) -> dict:
    """assign training and testing conditions to mice based on their slot.
    """
    for slot in MTMmice:
        if slot[0:2] == 's1':
            MTMmice[slot].settraintime("cpp", 4)
            MTMmice[slot].settraintime("cpa", 11)
        else:
            MTMmice[slot].settraintime("cpp", 11)
            MTMmice[slot].settraintime("cpa", 4)
        if slot[2] == "a":
            MTMmice[slot].setgroup("CPP", "ON")
        elif slot[2] == "b":
            MTMmice[slot].setgroup("CPA", "ON")
        elif slot[2] == "c":
            MTMmice[slot].setgroup("CPP", "OFF")
        else:
            MTMmice[slot].setgroup("CPA", "OFF")
        if int(slot[-1])%2 == 1:
            MTMmice[slot].setchambers("CPP", "plain", "circles")
        else:
            MTMmice[slot].setchambers("CPP", "circles", "plain")
        if slot[2] in ["a", "c"]:
            if slot[-1] in ["1", "4", "5"]:
                MTMmice[slot].setchambers("CPA", "striped", "checkered")
            else:
                MTMmice[slot].setchambers("CPA", "checkered", "striped")
        else:
            if slot[-1] in ["2", "3", "6"]:
                MTMmice[slot].setchambers("CPA", "striped", "checkered")
            else:
                MTMmice[slot].setchambers("CPA", "checkered", "striped")
    
def assigntesttime(MTMmice: dict) -> None:
    for slot in MTMmice:
        MTMmice[slot].settesttime()
        
def getdf(MTMmice: dict) -> pd.DataFrame:
    """output all information to a dataframe.
    """
    df_mice = pd.DataFrame()
    for slot in MTMmice:
        df_mouse = MTMmice[slot].outputdf(slot)
        df_mice = pd.concat([df_mice, df_mouse]).reset_index(drop=True)
    return df_mice


def getmouse(df, slot) -> MTMSubjectMouse:
    """Generate a MTMSubjectMouse based on the information of 
    the mouse kept in slot.
    """
    mouserow = df.loc[df['slot'] == slot]
    mouse = MTMSubjectMouse(mouserow.iloc[0]["subjectnum"])
    group = mouserow.iloc[0]["group"].split(" Test-")
    mouse.setgroup(group[0], group[1])
    print(group[0])
    cpp = mouserow.iloc[0]["CPP"].split(" at ")
    cpa = mouserow.iloc[0]["CPA"].split(" at ")
    mouse.settraintime("CPP", cpp[1])
    mouse.settraintime("CPA", cpa[1])
    print('hey')
    if cpp[0] == "plain":
        mouse.setchambers("CPP", "plain", "circles")
    else:
        mouse.setchambers("CPP", "circles", "plain")
    if cpa[0] == "striped":
        mouse.setchambers("CPA", "striped", "checkered")
    else:
        mouse.setchambers("CPA", "checkered", "striped")
    mouse.settesttime()
    mouse.recorddwelltime("habituation", mouserow.iloc[0]["hab-paired"], 
                          mouserow.iloc[0]["hab-unpaired"])
    mouse.recorddwelltime("test", mouserow.iloc[0]["test-paired"], 
                          mouserow.iloc[0]["test-unpaired"])
    return mouse


def updatedwelltime(df: pd.DataFrame, mouse: MTMSubjectMouse, slot) -> pd.DataFrame:
    """update the information of mouse to df_mice.
    """
    new_row = mouse.outputdf(slot)
    cols = list(df.columns)
    for col in cols[-4:]:
        df.loc[df.slot == slot, col] = new_row.iloc[0][col]
    
if __name__ == '__main__':
    mice = getmicelist()
    mice = getmicedict(mice)
    assigncondition(mice)
    assigntesttime(mice)
    df = getdf(mice)
    df.to_csv("MTMmice.csv", encoding='utf-8', index=False)
