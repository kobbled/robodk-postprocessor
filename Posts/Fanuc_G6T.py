# ----------------------------------------------------
# Base welding/cladding post processor
# ----------------------------------------------------

# Import RoboDK tools
from robodk import *
import math

# import fanuc post
from Fanuc_R30iA import RobotPost as MainClass


class RobotPost(MainClass):
    # speeds
    JOINT_SPEED = '20%'     # set joint speed motion (first pose)
    SPEED = '75mm/sec'     # set cartesian speed motion (approach pose)
    SPEED_REGISTER = 157
    TRAVEL_SPEED = 75
    APPRCH_SPEED = 25

    # offsets
    SPARE_PR = 9            # Spare Position register for calculations
    UTOOL_PR = 56
    UFRAME_PR = 16
    OFFSET_PR = 24
    OFFSET_START = 25
    OFFSET_STOP = 26
    OFFSET_APPROACH = 78
    OFFSET_DEPART = 76
    USE_COORD_MOTION = False  # flag coordinated motion

    # cell configuration
    ACTIVE_UF = 5           # Active UFrame Id (register)
    ACTIVE_UT = 3           # Active UTool Id (register)
    HAS_TURNTABLE = False
    GRP_TURNTABLE = 2
    HAS_TRACK = False
    GRP_TRACK = 0

    # timers
    LASER_TIMER = 4
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
        
    def startExtrud(self):
        self.RunCode(self.PROG_START_EXTRUD, True)
    
    def stopExtrud(self):
        self.RunCode(self.PROG_STOP_EXTRUD, True)

    def startPassLoop(self):
        self.RunCode(self.PROG_START_CELL, True)
        self.resetTimer(self.LASER_TIMER)
        self.RunCode(self.PROG_START_EXTRUD, True)
        self.RunCode('R[215:passLbl] = 100 + R[180:j]')
        self.ifOnJump('R[180:j]>=0', numReg=215)

    def stopPassLoop(self):
        self.RunCode(self.PROG_STOP_EXTRUD, True)
        self.RunCode(self.PROG_STOP_CELL, True)

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
        self.REG_SPEED = self.SPEED_REGISTER
        self.TIMEAFTER = (0, code)

    def toolOff(self):
        code = self.PROG_STOP_TOOL
        self.TOOLON = False
        self.P_OFFSET = self.OFFSET_STOP
        self.TIMEAFTER = (0, code)

    def moveApproach(self):
        self.setLBL('PASS_LBL_COUNT', 'pass%i' % (self.PASS_COUNT))
        self.setZoneData(-1)
        self.P_OFFSET = self.OFFSET_APPROACH
        #set approach speed
        if hasattr(self, 'REG_SPEED'):
                del self.REG_SPEED
        self.setSpeed(self.APPRCH_SPEED)
        if hasattr(self, 'TIMEAFTER'):
            del self.TIMEAFTER

    def moveDepart(self):
        self.setZoneData(-1)
        self.P_OFFSET = self.OFFSET_DEPART
        if hasattr(self, 'TIMEAFTER'):
            del self.TIMEAFTER

    def moveLink(self):
        self.stopTimer(self.LASER_TIMER)
        self.setZoneData(100)
        if self.USE_COORD_MOTION:
            if hasattr(self, 'COORD'):
                del self.COORD
        if hasattr(self, 'P_OFFSET'):
            del self.P_OFFSET
        #set travel speed
        if hasattr(self, 'REG_SPEED'):
                del self.REG_SPEED
        self.setSpeed(self.TRAVEL_SPEED)

    def moveLaserOn(self):
        self.P_OFFSET = self.OFFSET_PR
        self.TIMEAFTER = (0, self.HEIGHT_SENSOR)
    
    def RunCode(self, code, is_function_call = False):
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
            else:
                self.addline('CALL %s ;' % (code))
        else:
            if not code.endswith(';'):
                code = code + ';'
            self.addline(code)


# -------------------------------------------------
# ------------ For testing purposes ---------------
def _Pose(xyzrpw):
    [x, y, z, r, p, w] = xyzrpw
    a = r * math.pi / 180
    b = p * math.pi / 180
    c = w * math.pi / 180
    ca = math.cos(a)
    sa = math.sin(a)
    cb = math.cos(b)
    sb = math.sin(b)
    cc = math.cos(c)
    sc = math.sin(c)
    return Mat([[cb * ca, ca * sc * sb - cc * sa, sc * sa + cc * ca * sb, x], [cb * sa, cc * ca + sc * sb * sa, cc * sb * sa - ca * sc, y], [-sb, cb * sc, cc * cb, z], [0, 0, 0, 1]])


def _test_post():
    """Test the post with a basic program"""
    robot = RobotPost('Fanuc_custom', 'Fanuc robot', 6)
    robot.ProgStart("Program")

    robot.setFrame(_Pose([1544.5, 1295.0, 133.6, 90.3, 0, -90]))
    robot.setTool(_Pose([-38.1, -4.4, 840.9, 90.1, 0, -90]))
    robot.resetTimer(robot.LASER_TIMER)

    robot.RunCode(robot.PROG_START_EXTRUD, True)
    robot.MoveJ(_Pose([200, 200, 500, 180, 0, 180]), [-46.18419, -
                                                      6.77518, -20.54925, 71.38674, 49.58727, -302.54752])
    robot.startPassLoop()
    # pass1
        # approach
    robot.moveApproach()
    robot.MoveL(_Pose([200, 250, 348.734575, 180, 0, -150]),
                       [-41.62707, -8.89064, -30.01809, 60.62329, 49.66749, -258.98418])
        # laser start
    robot.toolOn()
    robot.MoveL(_Pose([200, 250, 348.734575, 180, 0, -150]),
                       [-41.62707, -8.89064, -30.01809, 60.62329, 49.66749, -258.98418])
        #path
    robot.moveLaserOn()
    robot.MoveL(_Pose([250, 300, 278.023897, 180, 0, -150]), [-37.52588, -6.32628, -
                                                              34.59693, 53.52525, 49.24426, -251.44677])
    robot.MoveL(_Pose([250, 300, 278.023897, 180, 0, -150]), [-37.52588, -6.32628, -
                                                              34.59693, 53.52525, 49.24426, -251.44677])
    robot.MoveL(_Pose([250, 300, 278.023897, 180, 0, -150]), [-37.52588, -6.32628, -
                                                              34.59693, 53.52525, 49.24426, -251.44677])
    robot.MoveL(_Pose([250, 300, 278.023897, 180, 0, -150]), [-37.52588, -6.32628, -
                                                              34.59693, 53.52525, 49.24426, -251.44677])
        # laser stop
    robot.toolOff()
    robot.MoveL(_Pose([200, 250, 348.734575, 180, 0, -150]),
                        [-41.62707, -8.89064, -30.01809, 60.62329, 49.66749, -258.98418])
        #depart
    robot.moveDepart()
    robot.MoveL(_Pose([200, 250, 348.734575, 180, 0, -150]),
                        [-41.62707, -8.89064, -30.01809, 60.62329, 49.66749, -258.98418])
        #linking
    robot.moveLink()
    robot.MoveJ(_Pose([200, 200, 500, 180, 0, 180]), [-46.18419, -
                                                      6.77518, -20.54925, 71.38674, 49.58727, -302.54752])
    robot.MoveJ(_Pose([200, 200, 500, 180, 0, 180]), [-46.18419, -
                                                      6.77518, -20.54925, 71.38674, 49.58727, -302.54752])
    robot.MoveJ(_Pose([200, 200, 500, 180, 0, 180]), [-46.18419, -
                                                      6.77518, -20.54925, 71.38674, 49.58727, -302.54752])

    robot.RunCode(robot.PROG_STOP_EXTRUD, True)
    robot.MoveL(_Pose([250, 300, 278.023897, 180, 0, -150]), [-37.52588, -6.32628, -
                                                              34.59693, 53.52525, 49.24426, -251.44677])
    robot.ProgFinish("Program")
    # robot.ProgSave(".","Program",True)

    robot.PROG = robot.PROG_LIST.pop()
    for line in robot.PROG:
        print(line)
    
    if len(robot.LOG) > 0:
        mbox('Program generation LOG:\n\n' + robot.LOG)

    input("Press Enter to close...")


if __name__ == "__main__":
    """Function to call when the module is executed by itself: test"""
    _test_post()
