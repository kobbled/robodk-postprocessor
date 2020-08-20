# ----------------------------------------------------
# Workcell specific post processor
# ----------------------------------------------------

# Import RoboDK tools
from robodk import *
import math

# import fanuc post
from Fanuc_G6T import RobotPost as G6TClass


class RobotPost(G6TClass):
    # speeds
    JOINT_SPEED = '20%'     # set joint speed motion (first pose)
    SPEED = '100mm/sec'     # set cartesian speed motion (approach pose)
    SPEED_REGISTER = 157
    TRAVEL_SPEED = 25
    APPRCH_SPEED = 100

    # offsets
    SPARE_PR = 290            # Spare Position register for calculations
    UTOOL_PR = 56
    UFRAME_PR = 16
    OFFSET_PR = 24
    OFFSET_START = 25
    OFFSET_STOP = 26
    OFFSET_APPROACH = 78
    OFFSET_DEPART = 76
    USE_COORD_MOTION = False  # flag coordinated motion

    # cell configuration
    nAxes = 6 # Important: This is usually provided by RoboDK automatically. Otherwise, override the __init__ procedure. 
    AXES_TYPE = ['R','R','R','R','R','R','J'] # Important: This is usually set up by RoboDK automatically. Otherwise, override the __init__ procedure.
    ACTIVE_UF = 9           # Active UFrame Id (register)
    ACTIVE_UT = 3           # Active UTool Id (register)
    HAS_TURNTABLE = False
    GRP_TURNTABLE = 0
    HAS_TRACK = False
    GRP_TRACK = 0

    # timers
    LASER_TIMER = 1
    POWDER_TIMER = 3

    # sensors
    ##HEIGHT_SENSOR = 50

    # other variables
    PASS_COUNT = 0
    PASS_LBL_COUNT = 100

    TOOLON = False
    PROG_START_CELL = 'G0_LASER_ENABLE'
    PROG_STOP_CELL = 'G0_LASER_DISABLE'
    PROG_START_EXTRUD = 'G0_POWDER_START'
    PROG_STOP_EXTRUD = 'G0_POWDER_STOP'
    PROG_START_TOOL = 'RUN_LASER_START'
    PROG_STOP_TOOL = 'RUN_LASER_STOP'

    def startPassLoop(self):
        self.RunCode(self.PROG_START_CELL, True)
        self.resetTimer(self.LASER_TIMER)

    def stopPassLoop(self):
        self.RunCode(self.PROG_STOP_CELL, True)
    
    def moveApproach(self):
        self.setZoneData(-1)
        self.P_OFFSET = self.OFFSET_APPROACH
        #set approach speed
        if hasattr(self, 'REG_SPEED'):
                del self.REG_SPEED
        self.setSpeed(self.APPRCH_SPEED, False)
        if hasattr(self, 'TIMEAFTER'):
            del self.TIMEAFTER

    def moveLaserOn(self):
        self.P_OFFSET = self.OFFSET_PR
        if hasattr(self, 'TIMEAFTER'):
            del self.TIMEAFTER
