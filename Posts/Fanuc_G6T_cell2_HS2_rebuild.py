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

    nAxes = 6 # Important: This is usually provided by RoboDK automatically. Otherwise, override the __init__ procedure. 
    AXES_TYPE = ['R','R','R','R','R','R','J'] # Important: This is usually set up by RoboDK automatically. Otherwise, override the __init__ procedure.
    HAS_TURNTABLE = True
    GRP_TURNTABLE = 3
    HAS_TRACK = False
    GRP_TRACK = -1
    JOINT_CONFIG = ['F','U','T']

    # timers
    LASER_TIMER = 1
    POWDER_TIMER = 3

    # sensors
    HEIGHT_SENSOR = 50

    # other variables
    PASS_LBL_REGISTER = 215
    J_LBL_REGISTER = 180
    PASS_COUNT = 0
    PASS_LBL_COUNT = 100

    TOOLON = False
    PROG_START_CELL = 'G0_LASER_ENABLE'
    PROG_STOP_CELL = 'G0_LASER_DISABLE'
    PROG_START_EXTRUD = 'G0_POWDER_START'
    PROG_STOP_EXTRUD = 'G0_POWDER_STOP'
    PROG_START_TOOL = 'RUN_LASER_START'
    PROG_STOP_TOOL = 'RUN_LASER_STOP'

    def toolOn(self):
        self.waitMS(200)
        self.startTimer(self.LASER_TIMER)
        code = self.PROG_START_TOOL
        self.setZoneData(100)
        self.TOOLON = True
        if self.USE_COORD_MOTION:
            self.COORD = True
        else:
            if hasattr(self, 'COORD'):
                del self.COORD
        self.P_OFFSET = self.OFFSET_START
        self.TIMEAFTER = (0, code)
    
    def laserStartSeq(self, start_speed=0):
        self.REPEAT_POSE = True
        self.toolOn()
        if start_speed > 0:
            self.setSpeed(start_speed, False)
        self.MoveL(self.LAST_POSE, self.LAST_JOINTS)
        self.moveLaserOn()
        self.MoveL(self.LAST_POSE, self.LAST_JOINTS)
        self.RETRACT = True
        self.REPEAT_POSE = False

    def laserStopSeq(self, stop_speed=0, dprt_speed=0):
        self.REPEAT_POSE = True
        self.toolOff()
        if stop_speed > 0:
            self.setSpeed(stop_speed, False)
        self.MoveL(self.LAST_POSE, self.LAST_JOINTS)
        self.moveDepart()
        self.MoveL(self.LAST_POSE, self.LAST_JOINTS)
        self.moveLink()
        if dprt_speed > 0:
            self.setSpeed(dprt_speed, False)
        self.RETRACT = False
        self.REPEAT_POSE = False


    def RunCode(self, code, is_function_call = False, checkProgSize=True):
        """Adds code or a function call"""
        if is_function_call:
            code.replace(' ', '_')
            if code.startswith('P_OFFSET'):
                # Customized P_OFFSET:
                value = code[len('P_OFFSET'):]
                if len(value) > 2:
                    exec('self.P_OFFSET=' + value)
                elif hasattr(self,'P_OFFSET'):
                    del self.P_OFFSET
            elif code.startswith('TOOL_OFFSET'):
                # Customized TOOL_OFFSET:
                value = code[len('TOOL_OFFSET'):]
                if len(value) > 2:
                    exec('self.TOOL_OFFSET=' + value)
                elif hasattr(self,'TOOL_OFFSET'):
                    del self.TOOL_OFFSET
            elif code.startswith('TIMEAFTER'):
                # Customized TIMEAFTER:
                value = code[len('TIMEAFTER'):]
                if len(value) > 2:
                    exec('self.TIMEAFTER=' + value)
                elif hasattr(self,'TIMEAFTER'):
                    # Any other program call
                    del self.TIMEAFTER
            elif code.startswith('REG_SPEED'):
                # Customized REG_SPEED:
                value = code[len('REG_SPEED'):]
                if len(value) > 2:
                    exec('self.REG_SPEED=' + value)
                elif hasattr(self, 'REG_SPEED'):
                    # Any other program call
                    del self.REG_SPEED
            elif code.startswith('CNT_VALUE'):
                value = code[len('CNT_VALUE'):]
                if len(value) > 2:
                    exec('self.CNT_VALUE=' + value)
            elif code.startswith('resetTimer'):
                value = code[len('resetTimer'):]
                if len(value) > 2:
                    exec('self.resetTimer' + value)
            # G6T specific calls
            elif code.startswith('toolOn'):
                exec('self.toolOn()')
            elif code.startswith('toolOff'):
                exec('self.toolOff()')
            elif code.startswith('moveLaserOn'):
                exec('self.moveLaserOn()')
            elif code.startswith('moveLaserOff'):
                exec('self.moveLaserOff()')
            elif code.startswith('moveApproach'):
                exec('self.moveApproach()')
            elif code.startswith('moveDepart'):
                exec('self.moveDepart()')
            elif code.startswith('moveLink'):
                exec('self.moveLink()')
            elif code.startswith('startExtrud'):
                exec('self.startExtrud()')
            elif code.startswith('stopExtrud'):
                exec('self.stopExtrud()')
            elif code.startswith('startPassLoop'):
                exec('self.startPassLoop()')
            elif code.startswith('stopPassLoop'):
                exec('self.stopPassLoop()')
            elif code.startswith('laserStartSeq'):
                exec('self.laserStartSeq(' + code.split("(")[1])
            elif code.startswith('laserStopSeq'):
                exec('self.laserStopSeq('+ code.split("(")[1])
            else:
                self.addline('CALL %s ;' % (code), checkProgSize=checkProgSize)
        else:
            if not code.endswith(';'):
                code = code + ';'
            self.addline(code, checkProgSize=checkProgSize)
