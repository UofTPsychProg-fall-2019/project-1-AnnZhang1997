# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 19:03:44 2020

@author: Ann Zhang

This module contains the code for class MTMSubjectMice and its functions.
"""
import pandas as pd

class MTMSubjectMouse:
    """A mouse that is a subject in the multiple time memory experiment.

    === Attributes ===
    SubjectNum:
        The subject number of the mouse, which is a integer in the range 1-48.
    CPPchambers:
        The paired and unpaired chambers for MTMSubjectMouse during CPP.
    CPAchambers:
        The paired and unpaired chambers for MTMSubjectMouse during CPA.
    TrainTime:
        The time of day that mouse receives CPP and CPA training.
    Group:
        The stimulus the mouse is tested for, can be either "CPP" or "CPA".
        Whether the time of test matches the time of training, can be either "ON" or "OFF".
    habituation:
        A dictionary recording the total time the subject mouse spent in 
        the two chambers: "paired" and "unpaired" during habituation.
    test:
        A dictionary recording the total time the subject mouse spent in 
        the two chambers: "paired" and "unpaired" during testing.
    """
    
    SubjectNum: int
    CPPchambers: dict
    CPAchambers: dict
    TrainTime: dict
    Group: list
    TestTime: int
    habituation: dict
    test: dict
    
    def __init__(self, num: int) -> None:
        """Initialize a MTMSubjectMouse with subject number "num".
        """
        self.SubjectNum = num
        self.CPPchambers = {"paired":"", "unpaired":""}
        self.CPAchambers = {"paired":"", "unpaired":""}
        self.TrainTime = {"CPP": 0, "CPA": 0}
        self.Group = ["", ""]
        self.TestTime = 0
        self.habituation = {"paired": 0, "unpaired": 0}
        self.test = {"paired": 0, "unpaired": 0}
        
    
    def __repr__(self) -> str:
        return "Mouse {0} in {1} Test-{2} group.".format(self.SubjectNum, 
                                                    self.Group[0], 
                                                    self.Group[1])
    
    def __str__(self) -> str:
        return "Mouse {0} in {1} Test-{2} group.\n \
            CPP/CPA Train Time: {3}/{4}.\n \
            CPP/CPA paired chamber: {5}/{6} \n \
            Test time: {7}".format(self.SubjectNum, 
            self.Group[0], self.Group[1], self.TrainTime["CPP"], 
            self.TrainTime["CPA"],self.CPPchambers["paired"], 
            self.CPAchambers["paired"], self.TestTime)
    

    def setchambers(self, stimulus: str, paired: str, unpaired: str) -> None:
        """
        Update the paired and unpaired chambers for stimulus when stimulus is
        a valid stimulus.
        """
        try:
            if stimulus.lower() == "cpp":
                self.CPPchambers["paired"] = paired
                self.CPPchambers["unpaired"] = unpaired
            elif stimulus.lower() == "cpa":
                self.CPAchambers["paired"] = paired
                self.CPAchambers["unpaired"] = paired
        except:
            print ("This is not a valid stimulus!")        



    def settraintime(self, stimulus: str, time: int) -> None
        """
        Update the training time for stimulus if stimulus is a valid stimulus.
        """
        try:
            if stimulus.lower() == "cpp":
                self.TrainTime["CPP"] = time
            elif stimulus.lower() == "cpa":
                self.TrainTime["CPA"] = time
        except:
            print ("This is not a valid stimulus!")
    

    def setgroup(self, stimulus: str, teston: str) -> None:
        """
        Update the group of mouse, based on which stimulus it will be tested
        for and if testing time matches training time.
        """
        if stimulus == "CPP" or stimulus == "CPA":
            self.Group = [stimulus, teston]        
        else:
            print ("This is not a valid stimulus!")
    

    def isteston(self) -> bool:
        """
        Returns whether the mice is in a TEST ON (test time matches training 
        time) group or a TEST OFF (test time does not match training time)
        group.
        """
        if self.Group[-1] == "ON":
            return True
        elif self.Group[-1] == "OFF":
            return FALSE
        elif self.Group[-1] == "":
            print ("Test Group has not been set.")
        else:
            print ("The test Group" + self.Group[-1] + "is not valid.")
             
    def settesttime(self) -> None:
        """
        Update the test time for mouse, based on its group and training time.
        """
        if self.Group[0] == "CPP":
            if self.isteston:
                self.TestTime = self.TrainTime["CPP"]
            else:
                self.TestTime = self.TrainTime["CPA"]
        else:
            if self.isteston:
                self.TestTime = self.TrainTime["CPA"]
            else:
                self.TestTime = self.TrainTime["CPP"]
        

        
    def recorddwelltime(self, section: str, paired: int, unpaired: int) -> None:
        """Records the dwell time.
        section can be either "habituation" or "test".
        paired is the number of seconds the subject spent in the paired chamber.
        unpaired is the number of seconds the subject spent in the unpaired chamber.
        """
        if section.lower() == "habituation":
            self.habituation["paired"] = paired
            self.habituation["unpaired"] = unpaired
        elif section.lower() == "test":
            self.test["paired"] = paired
            self.test["unpaired"] = unpaired
        else:
            raise Exception("Not a valid section!")
    
    def outputdf(self, slot: str) -> pd.DataFrame:
        """Output a 1 x 9 dataframe.
        The columns are: slot, subjectnum, group, CPP, CPA, hab-paired, 
        hab-unpaired, test-paired, test-unpaired.
        Slot records which slot in the stack was the mouse housed in.
        Subjectnum records the subject number of mouse.
        Group records the stimulus and test-training time match.
        CPP records the CPP-paired chamber and CPP-training time.
        CPA records the CPA-paired chamber and CPP-training time.
        hab-paired and hab-unpaired records the number of seconds that mouse 
        spent in the test-stimulus-paired and -unpaired chambers during habituation.
        test-paired and test-unpaired records the number of seconds that mouse 
        spent in the test-stimulus-paired and -unpaired chambers during test.
        """
        group = self.Group[0] + " Test-" + self.Group[1]
        cpp = self.CPPchambers["paired"] + " at " + str(self.TrainTime["CPP"])
        cpa = self.CPAchambers["paired"] + " at " + str(self.TrainTime["CPA"])
        d = {"slot": [slot], "subjectnum": [self.SubjectNum], "group": [group],
             "CPP": [cpp], "CPA": [cpa], "hab-paired": [self.habituation["paired"]], 
             "hab-unpaired": [self.habituation["unpaired"]], "test-paired": 
             [self.test["paired"]], "test-unpaired": [self.test["unpaired"]]}
        df = pd.DataFrame(data = d)
        return df
        
        
        