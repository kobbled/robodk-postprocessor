# Type help("robolink") or help("robodk") for more information
# Press F5 to run the script
# Documentation: https://robodk.com/doc/en/RoboDK-API.html
# Reference:     https://robodk.com/doc/en/PythonAPI/index.html
# Note: It is not required to keep a copy of this file, your python script is saved with the station
from robolink import *    # RoboDK API
from robodk import *      # Robot toolbox
RDK = Robolink()

robot = RDK.Item('', ITEM_TYPE_ROBOT)

robot.RunInstruction('TIMEAFTER(0,50)', INSTRUCTION_CALL_PROGRAM)
robot.RunInstruction('P_OFFSET(50)', INSTRUCTION_CALL_PROGRAM)
robot.MoveL(robot.Pose())
robot.RunInstruction('TIMEAFTER(0, "G0_LASER_START")', INSTRUCTION_CALL_PROGRAM)

robot.MoveL(robot.Pose())