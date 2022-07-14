from dataclasses import dataclass
from enum import Enum
from turtle import delay

# ADCS implementation constants
RING_SIZE = 4

""" figure this out with trans_criteria_t
# define bit fields for checking various mode transition criteria
CHECK_MIN_BDOT_TRANS_CRIT               = 0x0001
CHECK_MAX_BDOT_TRANS_CRIT               = 0x0002
CHECK_MIN_ANG_ERR_TRANS_CRIT            = 0x0004
CHECK_MAX_ANG_ERR_TRANS_CRIT            = 0x0008
CHECK_MIN_ANG_VEL_ERR_TRANS_CRIT        = 0x0010
CHECK_MAX_ANG_VEL_ERR_TRANS_CRIT        = 0x0020
CHECK_MIN_RW_ANG_VEL_TRANS_CRIT         = 0x0040
CHECK_MAX_RW_ANG_VEL_TRANS_CRIT         = 0x0080
CHECK_MIN_STATE_COVAR_DIAG_TRANS_CRIT   = 0x0100
CHECK_MAX_STATE_COVAR_DIAG_TRANS_CRIT   = 0x0200
"""

# enumerate ADCS states with unique names
class state_t(Enum):

    Safe1                                   = 0
    Safe2                                   = 1

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

# enumerate ADCS status (either ok/nominal or error)
class status_t(Enum):
    OK      = 0
    ERROR   = 1

# enumerate ADCS controller options
class controller_options_t(Enum):
    PRIMARY_MODERN      = 0
    SECONDARY_MODERN    = 1
    PRIMARY_FUZZY       = 2

# enumerate ADCS guidance system fuzzy options
class fuzzy_guidance_options_t(Enum):
    FUZZY_SV        = 0
    FUZZY_GS        = 1
    FUZZY_SVGS      = 2

# fill array, then loop back to beginning (overwriting data)
@dataclass
class ring_meas_t:
    iterator        : int
    time            : float[RING_SIZE]
    data            : float[RING_SIZE][3]

@dataclass
class ekf_data_t:
    ang_vel         : float[3] # [rad/s] latest estimated angular velocity
    q               : float[4] # latest estimated attitude quaternion (wrt reference)
    p               : float[6][6] # latest estimated state covariance matrix
    satrec          : elsetrec # orbit model WHERE IS ELSETREC DEFINED
    t0              : float # [s] time of last measurement/estimate (time after TLE epoch - jdsatepoch in elsetrec)
    t1              : float # [s] time of this measurement/estimate (time after TLE epoch - jdsatepoch in elsetrec)
    ang_vel_meas1   : float[3] # [rad/s] angular velocity measurement from IMU 1
    ang_vel_meas2   : float[3] # [rad/s] angular velocity measurement from IMU 2
    mag_meas_1      : float[3] # [tesla] magnetic field measurement from IMU 1
    mag_meas_2      : float[3] # [tesla] magnetic field measurement from IMU 2
    M               : float[3] # [A*m^2] magnetic moment (control effort) over last time interval [t0 t1]
    I               : float[3][3] # [kg*m^2] spacecraft mass moment of inertia tensor
    Q               : float[6][6] # [kg*m^2] reaction wheel mass moment of inertia
    R               : float[12][12] # state noise covariance matrix
    muE             : float # measurement noise covariance matrix
    rho             : float # [m^3/s^2] equal to 3.986004418e14 m^3/s^2
    CD              : float # [kg/m^3] atmospheric density
    A               : float[3] # [m^2] projected areas
    rcp             : float[3] # [m] center of pressure

@dataclass
class control_state_t:
    action      : int
    transition  : int
    delay       : int

# define/name operational mode transitions
class mode_transition_enum(Enum):
    Detumble2EKFRestart = 0
    EKFStart2DartStart = 1
    ControlStartBack2EKFStart = 2
    ControlStart2Control = 3
    ControlBack2ControlStart = 4

@dataclass
class trans_criteria_t:
    min_bdot            : float
    max_bdot            : float
    min_ang_err         : float
    max_ang_err         : float
    min_and_vel_err     : float[3]
    max_and_vel_err     : float[3]
    min_P_diag          : float[6]
    max_P_diag          : float[6]
    _or                 : bool



@dataclass
class data_t(Enum):
    STATUS                          = 0
    COMMANDED_STATE                 = 1
    GO_TO_COMMANDED_STATE           = 2
    NEXT_TIME                       = 3
    IS_DEPLOYED                     = 4
    FUZZY_GUIDANCE_OPTION           = 5
    CONTROLLER_OPTION               = 6
    # to arc tlm num ?
    # telem_num?
    TELEM_START                     = 7
    TLE                             = 8
    IRGF_G                          = 9
    IRGF_DG                         = 10
    IRGF_H                          = 11
    # TODO fill in the reset of this from cryocubeADCS.h line 272

    pass

# "quick" and dirty mapping of data numbers to their instantiated values in the ADCS class. 
# i have yet to determine if mapping these to numbers instead of an enumerated type is a better coding
# self here is in reference to adcs instance calling this....
data_enum_map = {
    data_t.STATUS                : self.status,
    data_t.COMMANDED_STATE       : self.commanded_state,
    data_t.GO_TO_COMMANDED_STATE : self.go_to_commanded_state,
    data_t.NEXT_TIME             : self.next_time,
    data_t.IS_DEPLOYED           : self.is_deployed,
    data_t.FUZZY_GUIDANCE_OPTION : self.fuzzy_guidance_option,
    data_t.CONTROLLER_OPTION     : self.controller_option,
    # to arc tlm num ?
    # telem_num?
    data_t.TELEM_START           : self.telem_start,
    data_t.TLE                   : self.tle,
    data_t.IRGF_G                : self.irgf_g,
    data_t.IRGF_DG               : self.irgf_dg,
    data_t.IRGF_H                : self.irgf_h,
    # TODO fill in the reset of this dict
}
