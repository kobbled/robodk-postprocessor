# Copyright 2015-2019 - RoboDK Inc. - https://robodk.com/
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# ----------------------------------------------------
# This file is a POST PROCESSOR for Robot Offline Programming to generate programs 
# for a generic Fanuc robot with RoboDK
#
# To edit/test this POST PROCESSOR script file:
# Select "Program"->"Add/Edit Post Processor", then select your post or create a new one.
# You can edit this file using any text editor or Python editor. Using a Python editor allows to quickly evaluate a sample program at the end of this file.
# Python should be automatically installed with RoboDK
#
# You can also edit the POST PROCESSOR manually:
#    1- Open the *.py file with Python IDLE (right click -> Edit with IDLE)
#    2- Make the necessary changes
#    3- Run the file to open Python Shell: Run -> Run module (F5 by default)
#    4- The "test_post()" function is called automatically
# Alternatively, you can edit this file using a text editor and run it with Python
#
# To use a POST PROCESSOR file you must place the *.py file in "C:/RoboDK/Posts/"
# To select one POST PROCESSOR for your robot in RoboDK you must follow these steps:
#    1- Open the robot panel (double click a robot)
#    2- Select "Parameters"
#    3- Select "Unlock advanced options"
#    4- Select your post as the file name in the "Robot brand" box
#
# To delete an existing POST PROCESSOR script, simply delete this file (.py file)
#
# ----------------------------------------------------
# More information about RoboDK Post Processors and Offline Programming here:
#     https://robodk.com/help#PostProcessor
#     https://robodk.com/doc/en/PythonAPI/postprocessor.html
# ----------------------------------------------------
# ----------------------------------------------------
# Import RoboDK tools
from robodk import *

# ----------------------------------------------------    
# Object class that handles the robot instructions/syntax
from Fanuc_R30iA import RobotPost as MainPost # sublassing the default post to change settings

# ----------------------------------------------------    
# Object class that handles the robot instructions/syntax
class RobotPost(MainPost):
    """Robot post object defined for Fanuc robots"""    
    
    # maximum number of lines per program. It will then generate multiple "pages" (files). 
    # This setting can be overriden by RoboDK settings (Tools-Options-Program)
    MAX_LINES_X_PROG = 9999    
    
    # Generate sub programs
    INCLUDE_SUB_PROGRAMS = True 
    
    # set default joint speed (percentage of the total speed)
    JOINT_SPEED = '20%'     
    
    # set default cartesian speed motion  
    SPEED = '200mm/sec'     
    
    # set default CNT value (all motion until smooth value is changed)
    # CNT_VALUE = 'CNT5' # 5% smoothing (set CNT1-CNT100)
    CNT_VALUE = 'FINE'      
    
    # Active UFrame Id (register)
    ACTIVE_UF = 9           
    
    # Active UTool Id (register)
    ACTIVE_UT = 9           
    
    # Spare Position register for calculations (such as setting UFRAME and UTOOL)
    SPARE_PR = 9
    
    # Set the turntable grup (usually GP2 or GP3)
    TURNTABLE_GROUP = 'GP2'
    #TURNTABLE_GROUP = 'GP3'
    
    # Set to True to generate programs compatible with RJ3 controllers (small difference in the program header)
    FANUC_RJ3_COMPATIBLE = True
    
    # Compile LS program to TP programs
    # More help here: https://robodk.com/doc/en/Robots-Fanuc.html#LSvsTP
    # Set the path to Roboguide WinOLPC tools, alternatively, set to None to prevent generating TP files
    # This step is ignored if the path does not exist
    PATH_MAKE_TP = 'C:/Program Files (x86)/FANUC/WinOLPC/bin/'
    #PATH_MAKE_TP = None # Ignore program compilation

    # Generate a drip feeder program: this will split long programs in subprograms and load them to the controller as they are executed
    # Set a file name to use an automatic dripfeeder: Files will be sent over FTP as they are executed
    # Right click a program and select "Send Program to Robot" to trigger the dripfeeding automatically
    DRIPFEED_FILE_NAME = "Fanuc_SendProgram_DripFeed.py"   
    #DRIPFEED_FILE_NAME = None       # Don't do any dripfeeding      
        
    # Always force user input to save the folder
    FORCE_POPUP_SAVE = True

# -------------------------------------------------
# ------------ For testing purposes ---------------   
def Pose(xyzrpw):
    [x,y,z,r,p,w] = xyzrpw
    a = r*math.pi/180
    b = p*math.pi/180
    c = w*math.pi/180
    ca = math.cos(a)
    sa = math.sin(a)
    cb = math.cos(b)
    sb = math.sin(b)
    cc = math.cos(c)
    sc = math.sin(c)
    return Mat([[cb*ca, ca*sc*sb - cc*sa, sc*sa + cc*ca*sb, x],[cb*sa, cc*ca + sc*sb*sa, cc*sb*sa - ca*sc, y],[-sb, cb*sc, cc*cb, z],[0,0,0,1]])

def test_post():
    """Test the post with a basic program"""

    robot = RobotPost('Fanuc_custom', 'Fanuc robot', 6)

    robot.ProgStart("Program")
    robot.RunMessage("Program generated by RoboDK", True)
    robot.setFrame(Pose([807.766544, -963.699898, 41.478944, 0, 0, 0]))
    robot.setTool(Pose([62.5, -108.253175, 100, -60, 90, 0]))
    robot.MoveJ(Pose([200, 200, 500, 180, 0, 180]), [-46.18419, -6.77518, -20.54925, 71.38674, 49.58727, -302.54752] )
    robot.MoveL(Pose([200, 250, 348.734575, 180, 0, -150]), [-41.62707, -8.89064, -30.01809, 60.62329, 49.66749, -258.98418] )
    robot.MoveL(Pose([200, 200, 262.132034, 180, 0, -150]), [-43.73892, -3.91728, -35.77935, 58.57566, 54.11615, -253.81122] )
    robot.RunMessage("Setting air valve 1 on")
    robot.RunCode("TCP_On", True)
    robot.Pause(1000)
    robot.MoveL(Pose([200, 250, 348.734575, 180, 0, -150]), [-41.62707, -8.89064, -30.01809, 60.62329, 49.66749, -258.98418] )
    robot.MoveL(Pose([250, 300, 278.023897, 180, 0, -150]), [-37.52588, -6.32628, -34.59693, 53.52525, 49.24426, -251.44677] )
    robot.MoveL(Pose([250, 250, 191.421356, 180, 0, -150]), [-39.75778, -1.04537, -40.37883, 52.09118, 54.15317, -246.94403] )
    robot.RunMessage("Setting air valve off")
    robot.RunCode("TCP_Off", True)
    robot.Pause(1000)
    robot.MoveL(Pose([250, 300, 278.023897, 180, 0, -150]), [-37.52588, -6.32628, -34.59693, 53.52525, 49.24426, -251.44677] )
    robot.MoveL(Pose([250, 200, 278.023897, 180, 0, -150]), [-41.85389, -1.95619, -34.89154, 57.43912, 52.34162, -253.73403] )
    robot.MoveL(Pose([250, 150, 191.421356, 180, 0, -150]), [-43.82111, 3.29703, -40.29493, 56.02402, 56.61169, -249.23532] )
    robot.ProgFinish("Program")
    # robot.ProgSave(".","Program",True)
    
    robot.PROG = robot.PROG_LIST.pop()
    for line in robot.PROG:
        print(line)
    
    if len(robot.LOG) > 0:
        mbox('Program generation LOG:\n\n' + robot.LOG)

    input("Press Enter to close...")

def test_post2():
    def p(v):
        return Pose(v)
    print('Total instructions: 25')
    r = RobotPost(r"""Fanuc_R30iA""",r"""Fanuc ARC Mate 120iC""",9,axes_type=['R','R','R','R','R','R','T','T','T'], pose_rail=p([2835.968412,3817.764593,1195.654333,-0.000000,-0.000000,180.000000]))
    #r = RobotPost(r"""Fanuc_R30iA""",r"""Fanuc ARC Mate 120iC""",9,axes_type=['R','R','R','R','R','R'], pose_rail=p([2835.968412,3817.764593,1195.654333,-0.000000,-0.000000,180.000000]))
    r.ProgStart(r"""Curve1""")
    r.RunMessage(r"""Program generated by RoboDK v3.5.3 for Fanuc ARC Mate 120iC on 10/11/2018 10:34:26""", True)
    r.RunMessage(r"""Using nominal kinematics.""", True)
    r.setFrame(p([-13114.312225,1641.490176,3032.967400,-89.429405,-0.828158,0.547393]),-1,r"""Part Local Ref""")
    r.setTool(p([6.579694,-0.871557,381.879694,-0.000000,45.000000,-0.000000]),-1,r"""Weld gun""")
    r.setSpeed(1000.000)
    r.MoveJ(None,[83.882578,-15.754442,-46.523597,49.296707,69.533346,-29.398461,2984.678090,2570.163700,563.830565],None)
    r.MoveL(p([-128.772331,15775.117798,-2955.672119,142.328568,35.043147,-175.776553]),[83.882578,-15.754442,-46.523597,49.296707,69.533346,-29.398461,2984.678090,2570.163700,563.830565],[0.0,0.0,1.0])
    r.RunCode(r"""ArcStart(2.0Hz,8.0mm,0.075s,0.075)""", True)
    r.MoveL(p([-87.947502,15734.292969,-3037.321777,142.328568,35.043147,-175.776553]),[87.328162,-15.924572,-40.474499,48.176067,63.664228,-32.552985,2984.678090,2570.163700,563.830565],[0.0,0.0,1.0])
    r.setSpeed(50.000)
    r.MoveL(p([-87.947502,15740.364258,-3038.315186,143.296306,39.222486,-169.641516]),[84.993829,-15.820725,-37.736589,57.497002,62.008852,-34.964581,2984.678090,2570.163700,563.830565],[0.0,0.0,1.0])
    r.MoveL(p([-87.947502,15753.342773,-3056.371826,162.364741,57.321011,-139.122540]),[83.865207,-17.204132,-23.104629,94.375731,49.260470,-53.900868,2984.678090,2570.163700,563.830565],[0.0,0.0,1.0])
    print('Done instruction: 10')
    sys.stdout.flush()
    r.MoveL(p([-87.947502,15753.342773,-3056.371826,162.364741,57.321011,-139.122540]),[83.865207,-17.204132,-23.104629,94.375731,49.260470,-53.900868,2984.678090,2570.163700,563.830565],[0.0,0.0,1.0])
    r.setSpeed(50.000)
    r.MoveL(p([-87.947502,15753.342773,-3323.071777,178.450701,-27.782697,-41.102688]),[91.280214,-24.514099,-7.482821,94.264844,27.576637,52.827242,2984.678090,2570.163700,563.830565],[0.0,0.0,1.0])
    r.MoveL(p([-87.947502,15734.292969,-3342.121826,115.212292,-23.920623,8.299772]),[82.536012,-9.623914,-3.656630,110.966378,66.076926,91.743683,2984.678090,2570.163700,563.830565],[0.0,0.0,1.0])
    r.setSpeed(50.000)
    r.MoveL(p([-87.947502,15467.592773,-3342.121826,106.861708,12.533873,22.086494]),[109.719609,2.464938,10.538370,161.900353,67.639292,65.645182,2984.678090,2570.163700,563.830565],[0.0,0.0,1.0])
    print('Done instruction: 20')
    sys.stdout.flush()
    r.setSpeed(1000.000)
    r.RunCode(r"""ArcEnd""", True)
    r.MoveL(p([-87.947502,15467.592773,-3342.121826,106.861708,12.533873,22.086494]),[109.719609,2.464938,10.538370,161.900353,67.639292,65.645182,2984.678090,2570.163700,563.830565],[0.0,0.0,1.0])
    r.MoveL(p([-93.977729,15961.562547,-2860.212507,106.861708,12.533873,22.086494]),[79.404467,-8.562284,-21.927019,140.074273,53.809210,114.164583,2984.678090,2570.163700,563.830565],[0.0,0.0,1.0])
    r.ProgFinish(r"""Curve1""")
    r.PROG = r.PROG_LIST.pop()
    for line in r.PROG:
        print(line)

    if len(r.LOG) > 0:
        mbox('Program generation LOG:\n\n' + robot.LOG)

    input("Press Enter to close...")

if __name__ == "__main__":
    """Function to call when the module is executed by itself: test"""
    test_post2()

