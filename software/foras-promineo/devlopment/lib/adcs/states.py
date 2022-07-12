from enum import Enum, auto

class States(Enum):

    safe1                                   = 0
    safe2                                   = 1

    DetumblePrepare                         = 2
    DetumbleMeasure1                        = 3
    DetumbleMeasure2                        = 4
    DetumbleEstimate                        = 5
    DetumbleTransition                      = 6
    DetumbleCalculateControl                = 7
    DetumbleApplyControl                    = 8

    EKFRestart                              = 9     # A one-state mode for EKF restart (re-initialize some EKF parameters, like P)

    EKFStartPrepare                         = 10
    EKFStartMeasure1                        = 11
    EKFStartEstimate1                       = 12
    EKFStartMeasure2                        = 13
    EKFStartEstimate2                       = 14
    EKFStartCalculateControl                = 15
    EKFStartApplyControl                    = 16
    EKFStartTransition                      = 17

    DartStartPrepare                        = 18
    DartStartMeasure                        = 19
    DartStartEstimate                       = 20
    DartStartGuidance                       = 21
    DartStartTransition                     = 22
    DartStartCalculateControl               = 23
    DartStartApplyControl                   = 24

    DartPrepare                             = 25
    DartMeasure                             = 26
    DartEstimate                            = 27
    DartGuidance                            = 28
    DartTransition                          = 29
    DartCalculateControl                    = 30
    DartApplyControl                        = 31

    FuzzyStartPrepare                       = 32
    FuzzyStartMeasure                       = 33
    FuzzyStartEstimate                      = 34
    FuzzyStartGuidance                      = 35
    FuzzyStartTransition                    = 36
    FuzzyStartCalculateControl              = 37
    FuzzyStartApplyControl                  = 38

    FuzzyPrepare                            = 39
    FuzzyMeasure                            = 40
    FuzzyEstimate                           = 41
    FuzzyGuidance                           = 42
    FuzzyTransition                         = 43
    FuzzyCalculateControl                   = 44
    FuzzyApplyControl                       = 45

    DesaturatePrepare                       = 46
    DesaturateMeasure                       = 47
    DesaturateTransition                    = 48
    DesaturateCalculateControl              = 49
    DesaturateApplyControl                  = 50

    DesaturateStopWheels                    = 51    # Separate one-state mode for ensuring wheels are stopped

    Desat4EKFRestartPrepare                 = 52
    Desat4EKFRestartMeasure                 = 53
    Desat4EKFRestartTransition              = 54
    Desat4EKFRestartCalculateControl        = 55
    Desat4EKFRestartApplyControl            = 56

    Desat4EKFRestartStopWheels              = 57    # separate one-state mode for ensuring wheels are stopped

    numStates                               = 58    # when cast to an integer type, this should equal the total number of states

