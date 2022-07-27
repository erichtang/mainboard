
#### trans criteria check functions 
def check_trans_bdot():
    pass

def check_trans_angerr():
    pass

def check_trans_angvel():
    pass

def check_trans_StateCovar():
    pass

#  function for determining whether state transition criteria are met (transition may occur)
def check_transition_criteria():
    """
    //group into upper-bound / lower-bound checks
	//for OR, checks must pass both upper and lower bounds (if checking both) to pass
		//if one (combined upper/lower-bound) check passes, then this returns true
		//if no (combined upper/lower-bound) checks pass, then this returns false (the default)
	//for AND, if any one check fails, this returns false
		//if all checks pass, then this returns true (the default)
    """
    pass

#### state transition functions ###
def mode_transition(self):
    pass

def transSafe1(self):
    pass

def transSafe2(self):
    pass

def transDetumblePrepare(self):
    pass

def transDetumbleMeasure1(self):
    pass

def transDetumbleMeasure2(self):
    pass

def transDetumbleEstimate(self):
    pass

def transDetumbleTransition(self):
    pass

def transDetumbleCalculateControl(self):
    pass

def transDetumbleApplyControl(self):
    pass

def transEKFrestart(self):
    pass

def transEKFStartPrepare(self):
    pass

def transEKFStartMeasure1(self):
    pass

def transEKFStartEstimate1(self):
    pass

def transEKFStartMeasure2(self):
    pass

def transEKFStartEstimate2(self):
    pass

def transEKFStartCalculateControl(self):
    pass

def transEKFStartApplyControl(self):
    pass

def transEKFStartTransition(self):
    pass

def transDartStartPrepare(self):
    pass

def transDartStartMeasure(self):
    pass

def transDartStartEstimate(self):
    pass

def transDartStartGuidance(self):
    pass

def transDartStartTransition(self):
    pass

def transDartStartApplyControl(self):
    pass

def transDartPrepare(self):
    pass

def transDartMeasure(self):
    pass

def transDartEstimate(self):
    pass

def transDartGuidance(self):
    pass

def transDartTransition(self):
    pass

def transDartCalculateControl(self):
    pass

def transDartApplyControl(self):
    pass

def transFuzzyStartPrepare(self):
    pass

def transFuzzyStartMeasure(self):
    pass

def transFuzzyStartEstimate(self):
    pass

def transFuzzyStartGuidance(self):
    pass

def transFuzzyStartTransition(self):
    pass

def transFuzzyStartCalculateControl(self):
    pass

def transFuzzyStartApplyControl(self):
    pass

def transFuzzyPrepare(self):
    pass

def transFuzzyMeasure(self):
    pass

def transFuzzyEstimate(self):
    pass

def transFuzzyGuidance(self):
    pass

def transFuzzyTransition(self):
    pass

def transFuzzyCalculateControl(self):
    pass

def transFuzzyApplyControl(self):
    pass

def transDesaturatePrepare(self):
    pass

def transDesaturateMeasure(self):
    pass

def transDesaturateTransition(self):
    pass

def transDesaturateCalculateControl(self):
    pass

def transDesaturateApplyControl(self):
    pass

def transDesat4EKFRePrepare(self):
    pass

def transDesat4EKFReMeasure(self):
    pass

def transDesat4EKFReTransition(self):
    pass

def transDesat4EKFReCalculateControl(self):
    pass

def transDesat4EKFReApplyControl(self):
    pass

def transDesat4EKFReStopWheels(self):
    pass

def transFuzzyStartEstimatetransFuzzyStartEstimate(self):
    pass

def transFuzzyStartEstimatetransFuzzyStartEstimate(self):
    pass

def transFuzzyStartEstimatetransFuzzyStartEstimate(self):
    pass

def transFuzzyStartEstimatetransFuzzyStartEstimate(self):
    pass

def transFuzzyStartEstimatetransFuzzyStartEstimate(self):
    pass

def transFuzzyStartEstimatetransFuzzyStartEstimate(self):
    pass