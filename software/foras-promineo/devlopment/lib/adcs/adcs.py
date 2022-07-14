"""
top level adcs implementation
"""

from .interface import Interface
from . import cdh
from .types import controller_options_t, ekf_data_t, fuzzy_guidance_options_t, ring_meas_t, status_t, state_t


class ADCS:

    # Physical Constants
    EPOCH = 2459580.5 # temporary

    pi = 3.14159265358979323846
    rho = 3.986004418e14 # m^3/s^2

    # Implementation Constants
    MAX_ATTEMPTS = 4

    def __init__(self, satellite):

        self.cubesat = satellite

        # see line 2640 in cryocubeadcs.c for init

        ################# Definitions for accessing ADCS data for getting telemetry and setting values #################

        # state machine information / control
        self.status = status_t.ERROR
        self.state = state_t.Safe1
        self.commanded_state = state_t.Safe1
        self.go_to_commanded_state_f = False
        self.state_attempt = 0
        #self.next_time = 0 # TODO how to get time for this?
        

        # attitude model
        self.TLE = 0
        self.I = [float[float]*3]*3
        self.irgf_g = 0 
        self.irgf_dg = 0 
        self.irgf_h = 0 
        self.irgf_dh = 0 
        self.irgf_epoch = 0 


        # on-reset values -- maybe move these elsewhere for more coherence?
        # these are constants that will probably be stored on SD
        self.reset_ang_vel_est = 0
        self.reset_q_est = 0
        self.reset_covar_est = 0
        self.reset_t0 = 0
        self.reset_t1 = 0
        self.reset_ang_vel_meas1 = 0
        self.reset_ang_vel_meas2 = 0
        self.reset_mag_meas1 = 0
        self.reset_mag_meas2 = 0
        self.reset_m = 0

        self.reset_nom_start = 0
        self.reset_irw = 0
        self.reset_Q = 0
        self.reset_r1 = 0
        self.reset_r2 = 0
        self.reset_muE = 0
        self.reset_rho = 0
        self.reset_c = 0
        self.reset_A = 0
        self.reset_rcp = 0

        # nom values -- mabe move elsewhere for coherence?
        self.nom_to_reset = 0
        self.nom_start = 0 
        self.nom_irw = 0
        self.nom_Q = 0
        self.nom_r2 =0
        self.nom_r2 = 0
        self.nom_muE = 0
        self.nom_rho = 0
        self.nom_A = 0
        self.nom_rcp = 0

        self.orbit_params = 0
        self.bdot_control_const = 0
        self.k_primary = 0
        self.k_secondary = 0
        self.max_m_moment_cmd =0
        self.fuzzy_sv_string = 0
        self.fuzzy_gs_string = 0
        self.fuzzy_sv_gs_string = 0
        self.fuzzy_ac_string = 0
        self.state_delays = 0
        self.trans_crit0 = 0
        self.trans_crit1 = 0
        self.trans_crit2 = 0
        self.trans_crit3 = 0
        self.trans_crit4 = 0
        self.trans_crit5 = 0
        self.trans_crit6 = 0
        self.trans_crit7 = 0
        self.primary_imu_select = 0

        # sensor measurements
        self.mag1_meas = ring_meas_t
        self.mag2_meas = ring_meas_t
        self.gyro1_meas = [float]*3
        self.gyro2_meas = [float]*3

        # state estimate
        self.bdot_est = [float]*3
        self.ekf_data = ekf_data_t
        self.ekf_data_rst_values = ekf_data_t

        # guidance (desired state calculated as part of control algorithm)
        self.q_des = [float]*4
        self.ang_vel_ddes = [float]*3
        
        # controller information
        self.controller_options = controller_options_t.PRIMARY_MODERN
        self.fuzzy_guidance_option = fuzzy_guidance_options_t.FUZZY_SV
        self.bdot_control = float
        self.K_primary = modern_controller_t
        self.K_secondary = modern_controller_t

        # control output
        self.M_moment_out = [float]*3
        self.max_M_moment_out = [float]*3

            # and many more.....

    # start state machine....
        # TBR

    ################# State Action Functions ################# crucocubeadcs.c line 50

    # safe 1
    def safe1(self):
        pass

    # safe 2
    def safe2(self):
        pass

    def do_nothing(self): # used as an action function to transition states -- figure out if we need this
        pass

    def turn_off_magnetotorquers(self):
        pass
    
    def increment_ring_iterator(self):
        pass

    def measureB(self):
        pass

    def differentiateB(self):
        pass

    def bdot_calculate_control(self):
        pass

    def bdot_apply_control(self):
        pass

    def measure_all(self):
        pass

    def ekf_restart(self):
        pass

    def nominal_estimator(self):
        pass

    def ekf_start_est2(self):
        pass

    def nominal_guidance(self):
        pass

    def torque2control(self):
        pass

    def nominal_calculate_control(self):
        pass

    def nominal_apply_control(self):
        pass

    def fuzzy_guidance(self):
        pass

    def desaturate_calculate_control(self):
        pass

    # trans criteria 
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

    # these are instantiated in a list but that can be adjusted later if need be,,,,
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

    # trans criteria check functions 
    def check_trans_bdot():
        pass

    def check_trans_angerr():
        pass

    def check_trans_angvel():
        pass

    def check_trans_StateCovar():
        pass

    def check_transition_criteria():
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

    # define states
        ### ahhhhhh

    # method for reporting and clearing adcs state errors
    def state_error(self):
        pass

    # method for determineing where or not to retry adcs state or enter safe mode
    def retry_state(self):
        pass

    # adcs globals definitions
    # i think this would go in the init?

    def figure_out_adcs_param_gile_storage_functions_next(self):
        pass
        
        