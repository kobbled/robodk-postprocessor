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
    SPEED = '75mm/sec'     # set cartesian speed motion (approach pose)
    SPEED_REGISTER = 157
    TRAVEL_SPEED = 75
    APPRCH_SPEED = 25

    # offsets
    SPARE_PR = 290            # Spare Position register for calculations
    UTOOL_PR = 56
    UFRAME_PR = 16
    OFFSET_PR = 24
    OFFSET_START = 25
    OFFSET_STOP = 26
    OFFSET_APPROACH = 78
    OFFSET_DEPART = 76
    USE_COORD_MOTION = True  # flag coordinated motion

    # cell configuration
    ACTIVE_UF = 6           # Active UFrame Id (register)
    ACTIVE_UT = 3           # Active UTool Id (register)
    HAS_TURNTABLE = True
    GRP_TURNTABLE = 3
    HAS_TRACK = False
    GRP_TRACK = 0
    JOINT_CONFIG = ['F','U','T']

    # timers
    LASER_TIMER = 1
    POWDER_TIMER = 3

    # sensors
    HEIGHT_SENSOR = 50

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

    def setSpeed(self, speed_mms, check_event=True):

        #user certain speed changes to inject program events
        if check_event == True:
            if speed_mms >= 50 and self.RETRACT:
                self.laserStopSeq()
            elif speed_mms > 0.6 and speed_mms < 0.8:
                self.moveApproach()
            elif speed_mms > 1.3 and speed_mms < 1.5:
                self.laserStartSeq()

        """Changes the robot speed (in mm/s)"""
        if self.SPEED_BACKUP is None:
            # Set the normal speed
            self.SPEED = '%.0fmm/sec' % max(speed_mms, 0.01)
            # assume 5000 mm/s as 100%
            #self.JOINT_SPEED = '%.0f%%' % max(min(100.0*speed_mms/5000.0, 100.0), 1) # Saturate percentage speed between 1 and 100
        else:
            # Do not alter the speed as we are in ARC movement mode
            # skip speed settings if it has been overriden
            self.SPEED_BACKUP = '%.0fmm/sec' % max(speed_mms, 0.01)
            # assume 5000 mm/s as 100%
            #self.JOINT_SPEED = '%.0f%%' % max(min(100.0*speed_mms/5000.0, 100.0), 1) # Saturate percentage speed between 1 and 100
