
from dataclasses import dataclass
from enum import Enum

# ADCS implementation constants
RING_SIZE = 4

ADCS_RESET_VALS_PATH = "/sd/adcs_reset"

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
# used for self.adcs.executeADCSaction
class state_t(Enum):

    SAFE1                                   = 0
    SAFE2                                   = 1

    DETUMBLEPREPARE                         = 2
    DETUMBLEMEASURE1                        = 3
    DETUMBLEMEASURE2                        = 4
    DETUMBLEESTIMATE                        = 5
    DETUMBKETRANSITION                      = 6
    DETUMBLECALCULATECONTROL                = 7
    DETUMBLEAPPLYCONTROL                    = 8

    EKFRESTART                              = 9     # A one-state mode for EKF restart (re-initialize some EKF parameters, like P)

    EKFSTARTPREPARE                         = 10
    EKFSTARTMEASURE1                        = 11
    EKFSTARTESTIMATE1                       = 12
    EKFSTARTMEASURE2                        = 13
    EKFSTARTESTIMATE2                       = 14
    EKFSTARTCALCULATECONTROL                = 15
    EKFSTARTAPPLYCONTROL                    = 16
    EKFStartTransition                      = 17

    DARTSTARTPREPARE                        = 18
    DARTSTARTMEASURE                        = 19
    DARTSTARTESTIMATE                       = 20
    DARTSTARTGUIDANCE                       = 21
    DARTSTARTTRANSITION                     = 22
    DARTSTARTCALCULATECONTROL               = 23
    DARTSTARTAPPLYCONTROL                   = 24

    DARTPREPARE                             = 25
    DARTMEASURE                             = 26
    DARTESTIMATE                            = 27
    DARTGUIDANCE                            = 28
    DARTTRANSITION                          = 29
    DARTCALCULATECONTROL                    = 30
    DARTAPPLYCONTROL                        = 31

    FUZZYSTARTPREPARE                       = 32
    FUZZYSTARTMEASURE                       = 33
    FUZZYSTARTESTIMATE                      = 34
    FUZZYSTARTGUIDANCE                      = 35
    FUZZYSTARTTRANSITION                    = 36
    FUZZYSTARTCALCULATECONTROL              = 37
    FUZZYSTARTAPPLYCONTROL                  = 38

    FUZZYPREPARE                            = 39
    FUZZYMEASURE                            = 40
    FUZZYESTIMATE                           = 41
    FUZZYGUIDANCE                           = 42
    FUZZYTRANSITION                         = 43
    FUZZYCALCULATECONTROL                   = 44
    FUZZYAPPLYCONTROL                       = 45

    DESATURATEPREPARE                       = 46
    DESATURATEMEASURE                       = 47
    DESATURATETRANSITION                    = 48
    DESATURATECALCULATECONTROL              = 49
    DESATURATEAPPLYCONTROL                  = 50

    DESATURATESTOPWHEELS                    = 51    # Separate one-state mode for ensuring wheels are stopped

    DESAT4EKFRESTARTPREPARE                 = 52
    DESAT4EKFRESTARTMEASURE                 = 53
    DESAT4EKFRESTARTTRANSITION              = 54
    DESAT4EKFRESTARTCALCULATECONTROL        = 55
    DESAT4EKFRESTARTAPPLYCONTROL            = 56

    DESAT4EKFRESTARTSTOPWHEELS              = 57    # separate one-state mode for ensuring wheels are stopped

    numStates                               = 58    # when cast to an integer type, this should equal the total number of states

# enumerate ADCS state actions
# used for self.adcs.executeADCStransition
# what is a better name for this ? See cryocubefunptrrpl.c
# actually number these.....
class transition_t(Enum):
    SAFE1 = 0
    SAFE2 = 0
    TURN_OFF_MAGNETORQUERS = 0
    MEASUREB = 0
    DIFFERENTIATEB = 0
    DO_NOTHING = 0
    BDOT_CALCULATE_CONTROL = 0
    BDOT_APPLY_CONTROL = 0
    EKF_RESTART = 0
    MEASURE_ALL = 0
    NOMINAL_ESTIMATOR = 0
    EKF_START_EST2 = 0
    NOMINAL_GUIDANCE = 0
    NOMINAL_CALCULATE_CONTROL = 0
    NOMINAL_APPLY_CONTROL = 0
    FUZZY_GUIDANCE = 0
    DESATURATE_CALCULATE_CONTROL = 0
    STOP_WHEELS = 0

    TRANS_SAFE1 = 0
    TRANS_SAFE2 = 0
    TRANS_DETUMBLE_PREPARE = 0
    TRANS_DETUMBLE_MEASURE1 = 0
    TRANS_DETUMBLE_MEASURE2 = 0
    TRANS_DETUMBLE_ESTIMATE = 0
    TRANS_DETUMBLE_TRANSITION = 0
    TRANS_DETUMBLE_CALCULATE_CONTROL = 0
    TRANS_DETUMBLE_APPLY_CONTROL = 0
    TRANS_EKF_RESTART = 0
    TRANS_EKF_START_PREPARE = 0
    TRANS_EKF_START_MEASURE1 = 0
    TRANS_EKF_START_ESTIMATE1 = 0
    TRANS_EKF_START_MEASURE2 = 0
    TRANS_EKF_START_ESTIMATE2 = 0
    TRANS_EKF_START_CALCULATE_CONTROL = 0
    TRANS_EKF_START_APPLY_CONTROL = 0
    TRANS_EKF_START_TRANSITION = 0
    TRANS_DART_START_PREPARE = 0
    TRANS_DART_START_MEASURE = 0
    TRANS_DART_START_ESTIMATE = 0
    TRANS_DART_START_GUIDANCE = 0 
    TRANS_DART_START_TRANSITION = 0
    TRANS_DART_START_CALCULATE_CONTROL = 0
    TRANS_DART_START_APPLY_CONTROL = 0
    TRANS_DART_PREPARE = 0
    TRANS_DART_MEASURE = 0
    TRANS_DART_ESTIMATE = 0
    TRANS_DART_GUIDANCE = 0
    TRANS_DART_TRANSITION = 0
    TRANS_DART_CALCULATE_CONTROL = 0
    TRANS_DART_APPLY_CONTROL = 0

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

# structure to fill array, then loop back to beginning (overwriting data)
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
    #satrec          : elsetrec # orbit model WHERE IS ELSETREC DEFINED
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
    things2check        : int # TODO figuee out what this is for and if it can be implmented easier to understand in python # bit fields for 'this' mode's transition criteria
    min_bdot            : float # [tesla/s] minimum magnitude of Bdot required for mode transition
    max_bdot            : float # [tesla/s] maximum magnitude of Bdot required for mode transition
    min_ang_err         : float # [rad] minimum angular error (axis-angle representation) for mode transition
    max_ang_err         : float # [rad] maximum angular error (axis-angle representation) for mode transition 
    min_and_vel_err     : float[3] # [rad/s] minimum angular rate error required for mode transition
    max_and_vel_err     : float[3] # [rad/s] maximum angular rate error required for mode transition
    min_P_diag          : float[6] # [rad^2/s^2] and [] minimum state error variance (diagonal of covariance matrix)
    max_P_diag          : float[6] # [rad^2/s^2] and [] maximum state error variance (diagonal of covariance matrix)
    _or                 : bool # evaluate constraints using or (default and - i.e. all constraints must be satisfied)

# find this def
class modern_controller_t:
    pass

############################### ADCS DATA CONTAINER ##########################################

"""
container for storing all adcs data. 
TODO: correctly declare all type annotations inside this class
TODO: determine if additional members need to be added.
TODO: determine if "reset" or "nom" values can be saved on an SD as opposed to being stored with every instance of this type....
    TODO: a dict with msgpack would be an efficient way to store these initial values.....
"""
@dataclass
class adcs_data_t:
    status                      : status_t
    state                       : state_t
    commanded_state             : state_t
    go_to_commanded_state_f     : bool
    state_attempt               : int
    next_time                   : float
    
    # attitude model
    TLE                         : float # or int?
    I                           : float[3][3]
    irgf_g                      : float 
    irgf_dg                     : float
    irgf_h                      : float
    irgf_dh                     : float
    irgf_epoch                  : float


    # on-reset values -- maybe move these elsewhere for more coherence?
    # these are constants that will probably be stored on SD
    reset_ang_vel_est           : float
    reset_q_est                 : float
    reset_covar_est             : float
    reset_t0                    : float
    reset_t1                    : float
    reset_ang_vel_meas1         : float
    reset_ang_vel_meas2         : float
    reset_mag_meas1             : float
    reset_mag_meas2             : float
    reset_m                     : float

    reset_nom_start             : float
    reset_irw                   : float
    reset_Q                     : float
    reset_r1                    : float
    reset_r2                    : float
    reset_muE                   : float
    reset_rho                   : float
    reset_c                     : float
    reset_A                     : float
    reset_rcp                   : float

    # nom values -- mabe move elsewhere for coherence?
    nom_to_reset                : float
    nom_start                   : float
    nom_irw                     : float
    nom_Q                       : float
    nom_r2                      : float
    nom_r2                      : float
    nom_muE                     : float
    nom_rho                     : float
    nom_A                       : float
    nom_rcp                     : float

    orbit_params                : float
    bdot_control_const          : float
    k_primary                   : float
    k_secondary                 : float
    max_m_moment_cmd            : float
    fuzzy_sv_string             : float
    fuzzy_gs_string             : float
    fuzzy_sv_gs_string          : float
    fuzzy_ac_string             : float
    state_delays                : float
    trans_crit0                 : float
    trans_crit1                 : float
    trans_crit2                 : float
    trans_crit3                 : float
    trans_crit4                 : float
    trans_crit5                 : float
    trans_crit6                 : float
    trans_crit7                 : float
    primary_imu_select          : float

    # sensor measurements
    mag1_meas                   : ring_meas_t
    mag2_meas                   : ring_meas_t
    gyro1_meas                  : float[3]
    gyro2_meas                  : float[3]

    # state estimate
    bdot_est                    : float[3]
    ekf_data                    : ekf_data_t
    ekf_data_rst_values         : ekf_data_t

    # guidance (desired state calculated as part of control algorithm)
    q_des                       : float[4]
    ang_vel_ddes                : float[4]
    
    # controller information
    controller_options          : controller_options_t
    fuzzy_guidance_option       : fuzzy_guidance_options_t
    bdot_control                : float
    K_primary                   : modern_controller_t # define this type
    K_secondary                 : modern_controller_t

    # control output
    M_moment_out                : float[3]
    max_M_moment_out            : float[3]

        # and many more.....

############################## STATE ACTION & TRANSITION DEFINITIONS ##############################

class Safe1(control_state_t):
    action          = state_t.SAFE1
    transition      = transition_t.TRANS_SAFE1
    delay           = 10

    # fill this in for other states.....
    # see crycocubeADCS.c line 1721

############################## STATE TRANSITION CRITERION ##############################

class ekfStart2DartStart_stopDetumble(trans_criteria_t):
    min_bdot            = 0.0
    max_bdot            = 0.0000001
    min_ang_err         = 0.0
    max_ang_err         = 0.0
    min_and_vel_err     = [0.0, 0.0, 0.0]
    max_and_vel_err     = [0.0, 0.0, 0.0]
    min_P_diag          = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    max_P_diag          = [0.00000001, 0.00000001, 0.00000001, 0.0076, 0.0076, 0.0076]
    _or                 = False

class ekfStart2DartStart_keepDetumble(trans_criteria_t):
    min_bdot            = 0.0
    max_bdot            = 0.0000001
    min_ang_err         = 0.0
    max_ang_err         = 0.0
    min_and_vel_err     = [0.0, 0.0, 0.0]
    max_and_vel_err     = [0.0, 0.0, 0.0]
    min_P_diag          = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    max_P_diag          = [0.00000001, 0.00000001, 0.00000001, 0.0076, 0.0076, 0.0076]
    _or                 = False


class Detumble2EKFRestart(trans_criteria_t):
    min_bdot            = 0.0
    max_bdot            = 0.0000001
    min_ang_err         = 0.0
    max_ang_err         = 0.0
    min_and_vel_err     = [0.0, 0.0, 0.0]
    max_and_vel_err     = [0.0, 0.0, 0.0]
    min_P_diag          = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    max_P_diag          = [0.00000001, 0.00000001, 0.00000001, 0.0076, 0.0076, 0.0076]
    _or                 = False

class EKFStart2DartStart(trans_criteria_t):
    min_bdot            = 0.0
    max_bdot            = 0.0000001
    min_ang_err         = 0.0
    max_ang_err         = 0.0
    min_and_vel_err     = [0.0, 0.0, 0.0]
    max_and_vel_err     = [0.0, 0.0, 0.0]
    min_P_diag          = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    max_P_diag          = [0.00000001, 0.00000001, 0.00000001, 0.0076, 0.0076, 0.0076]
    _or                 = False

class ControlStartBack2EKFStart(trans_criteria_t):
    min_bdot            = 0.0
    max_bdot            = 0.0000001
    min_ang_err         = 0.0
    max_ang_err         = 0.0
    min_and_vel_err     = [0.0, 0.0, 0.0]
    max_and_vel_err     = [0.0, 0.0, 0.0]
    min_P_diag          = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    max_P_diag          = [0.00000001, 0.00000001, 0.00000001, 0.0076, 0.0076, 0.0076]
    _or                 = False

class ControlStart2Control(trans_criteria_t):
    min_bdot            = 0.0
    max_bdot            = 0.0000001
    min_ang_err         = 0.0
    max_ang_err         = 0.0
    min_and_vel_err     = [0.0, 0.0, 0.0]
    max_and_vel_err     = [0.0, 0.0, 0.0]
    min_P_diag          = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    max_P_diag          = [0.00000001, 0.00000001, 0.00000001, 0.0076, 0.0076, 0.0076]
    _or                 = False

class ControlBack2ControlStart(trans_criteria_t):
    min_bdot            = 0.0
    max_bdot            = 0.0000001
    min_ang_err         = 0.0
    max_ang_err         = 0.0
    min_and_vel_err     = [0.0, 0.0, 0.0]
    max_and_vel_err     = [0.0, 0.0, 0.0]
    min_P_diag          = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    max_P_diag          = [0.00000001, 0.00000001, 0.00000001, 0.0076, 0.0076, 0.0076]
    _or                 = False

class Mode2Desaturate(trans_criteria_t):
    min_bdot            = 0.0
    max_bdot            = 0.0000001
    min_ang_err         = 0.0
    max_ang_err         = 0.0
    min_and_vel_err     = [0.0, 0.0, 0.0]
    max_and_vel_err     = [0.0, 0.0, 0.0]
    min_P_diag          = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    max_P_diag          = [0.00000001, 0.00000001, 0.00000001, 0.0076, 0.0076, 0.0076]
    _or                 = False

class Mode2Desat4EKFRestart(trans_criteria_t):
    min_bdot            = 0.0
    max_bdot            = 0.0000001
    min_ang_err         = 0.0
    max_ang_err         = 0.0
    min_and_vel_err     = [0.0, 0.0, 0.0]
    max_and_vel_err     = [0.0, 0.0, 0.0]
    min_P_diag          = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    max_P_diag          = [0.00000001, 0.00000001, 0.00000001, 0.0076, 0.0076, 0.0076]
    _or                 = False
