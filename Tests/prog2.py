# Type help("robolink") or help("robodk") for more information
# Press F5 to run the script
# Documentation: https://robodk.com/doc/en/RoboDK-API.html
# Reference:     https://robodk.com/doc/en/PythonAPI/index.html
# Note: It is not required to keep a copy of this file, your python script is saved with the station
from robolink import *    # RoboDK API
from robodk import *      # Robot toolbox
RDK = Robolink()

robot = RDK.Item('', ITEM_TYPE_ROBOT)

robot.MoveJ(robot.Pose())


robot.RunInstruction('resetLaserTimer', INSTRUCTION_CALL_PROGRAM)
#start powder
robot.RunInstruction('startExtrud', INSTRUCTION_CALL_PROGRAM)
#feed in
robot.MoveJ(robot.Pose())
robot.RunInstruction('startPassLoop', INSTRUCTION_CALL_PROGRAM)

# approach
robot.RunInstruction('moveApproach', INSTRUCTION_CALL_PROGRAM)
robot.MoveL(robot.Pose())
# laser start
robot.RunInstruction('toolOn', INSTRUCTION_CALL_PROGRAM)
robot.MoveL(robot.Pose())
#path
robot.RunInstruction('moveLaserOn', INSTRUCTION_CALL_PROGRAM)
robot.MoveL(robot.Pose())
robot.MoveL(robot.Pose())
robot.MoveL(robot.Pose())
robot.MoveL(robot.Pose())
# laser stop
robot.RunInstruction('toolOff', INSTRUCTION_CALL_PROGRAM)
robot.MoveL(robot.Pose())
#depart
robot.RunInstruction('moveDepart', INSTRUCTION_CALL_PROGRAM)
robot.MoveL(robot.Pose())
#linking
robot.RunInstruction('moveLink', INSTRUCTION_CALL_PROGRAM)
robot.MoveJ(robot.Pose())
robot.MoveJ(robot.Pose())
robot.MoveJ(robot.Pose())
#stop powder
robot.RunInstruction('stopExtrud', INSTRUCTION_CALL_PROGRAM)
