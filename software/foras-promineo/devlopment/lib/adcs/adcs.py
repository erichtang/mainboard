"""
top level adcs implementation
"""

from .interface import Interface
from . import cdh
from .types import controller_options_t, ekf_data_t, fuzzy_guidance_options_t, ring_meas_t, status_t, state_t, trans_criteria_t, adcs_data_t, transition_t
from . import state_actions
from . import state_transitions


class ADCS:

    # maybe find somewhere better to store constants that will never change?

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
        # not in love with defininf this data type then declaring it's inital values here but whatever
        # commented out init values for now
        # look at crycubeadcs.c line 1849 for inital values for all this junk, there is probably a more elegant way to init this....
            # look into using msgpack and the config lib i've wrote already?

        self.data : adcs_data_t

        # init values to self.data from paramater file
            #use msgack and config lib?
        """
        # state machine information / control
        self.data.status = status_t.ERROR
        self.data.state = state_t.Safe1
        self.data.commanded_state = state_t.Safe1
        self.data.go_to_commanded_state_f = False
        self.data.state_attempt = 0
        self.data.next_time = 0 # TODO how to get time for this?

        # attitude model
        self.data.TLE = 0
        self.data.I = [float[float]*3]*3
        self.data.irgf_g = 0 
        self.data.irgf_dg = 0 
        self.data.irgf_h = 0 
        self.data.irgf_dh = 0 
        self.data.irgf_epoch = 0 


        # on-reset values -- maybe move these elsewhere for more coherence?
        # these are constants that will probably be stored on SD
        self.data.reset_ang_vel_est = 0
        self.data.reset_q_est = 0
        self.data.reset_covar_est = 0
        self.data.reset_t0 = 0
        self.data.reset_t1 = 0
        self.data.reset_ang_vel_meas1 = 0
        self.data.reset_ang_vel_meas2 = 0
        self.data.reset_mag_meas1 = 0
        self.data.reset_mag_meas2 = 0
        self.data.reset_m = 0

        self.data.reset_nom_start = 0
        self.data.reset_irw = 0
        self.data.reset_Q = 0
        self.data.reset_r1 = 0
        self.data.reset_r2 = 0
        self.data.reset_muE = 0
        self.data.reset_rho = 0
        self.data.reset_c = 0
        self.data.reset_A = 0
        self.data.reset_rcp = 0

        # nom values -- mabe move elsewhere for coherence?
        self.data.nom_to_reset = 0
        self.data.nom_start = 0 
        self.data.nom_irw = 0
        self.data.nom_Q = 0
        self.data.nom_r2 =0
        self.data.nom_r2 = 0
        self.data.nom_muE = 0
        self.data.nom_rho = 0
        self.data.nom_A = 0
        self.data.nom_rcp = 0

        self.data.orbit_params = 0
        self.data.bdot_control_const = 0
        self.data.k_primary = 0
        self.data.k_secondary = 0
        self.data.max_m_moment_cmd =0
        self.data.fuzzy_sv_string = 0
        self.data.fuzzy_gs_string = 0
        self.data.fuzzy_sv_gs_string = 0
        self.data.fuzzy_ac_string = 0
        self.data.state_delays = 0
        self.data.trans_crit0 = 0
        self.data.trans_crit1 = 0
        self.data.trans_crit2 = 0
        self.data.trans_crit3 = 0
        self.data.trans_crit4 = 0
        self.data.trans_crit5 = 0
        self.data.trans_crit6 = 0
        self.data.trans_crit7 = 0
        self.data.primary_imu_select = 0

        # sensor measurements
        self.data.mag1_meas = ring_meas_t
        self.data.mag2_meas = ring_meas_t
        self.data.gyro1_meas = [float]*3
        self.data.gyro2_meas = [float]*3

        # state estimate
        self.data.bdot_est = [float]*3
        self.data.ekf_data = ekf_data_t
        self.data.ekf_data_rst_values = ekf_data_t

        # guidance (desired state calculated as part of control algorithm)
        self.data.q_des = [float]*4
        self.data.ang_vel_ddes = [float]*3
        
        # controller information
        self.data.controller_options = controller_options_t.PRIMARY_MODERN
        self.data.fuzzy_guidance_option = fuzzy_guidance_options_t.FUZZY_SV
        self.data.bdot_control = float
        self.data.K_primary = modern_controller_t
        self.data.K_secondary = modern_controller_t

        # control output
        self.data.M_moment_out = [float]*3
        self.data.max_M_moment_out = [float]*3

            # and many more.....
    """

    # start state machine....
        # TBR

    # method for reporting and clearing adcs state errors
    def state_error(self):
        pass

    # method for determineing where or not to retry adcs state or enter safe mode
    def retry_state(self):
        pass

    # //generic mode transition function (should be used in all transXxxTransition states)
    # //checks for commanded mode, then checks for errors, otherwise returns nominal transition
    def mode_transition(self, ideal_state : state_t):
        pass

    # see cryocubefunptrrpl.c
    def executeADCSaction(self, action : int):
        match action:
            case state_t.SAFE1:
                state_actions.safe1(self)
                
            ### fill in the rest if these,,,,,

            case _:
                # undefined state called....
                pass
    # see cryocubefunptrrpl.c
    def executeADCStransition(self, transition : int):
        match transition:
            case transition_t.TRANS_SAFE1:
                self.data.state = state_transitions.transSafe1(self)

            ### fill in the rest if these,,,,,

            case _:
                # undefined state called....
                pass

    # see tele_read.c line 732
    def processADCSevents(self):
        # if time >= adcs delay time
            # execute adcs action
            # adcs delay = self.data.state.delay
            # execute adcs transition
        pass