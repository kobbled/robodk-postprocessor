RoboDK
======
   
The RoboDK package implements the RoboDK API for Python. 
The package allows creating simulations for industrial robots, specific mechanisms and generating vendor-specific programs for robots.
While RoboDK's graphical user interface can be used to create programs, it is possible to extend the robot controller limitations by using a universal programming language such as Python.

With the RoboDK API for Python it is possible to simulate and program any industrial robot using Python programming language. 
This avoids using vendor-specific programming languages.

The package contains the following 2 modules:
 * The `robolink module <https://robodk.com/doc/en/PythonAPI/robolink.html>`_ is the link between RoboDK and Python. Any item from the RoboDK item tree can be retrieved. Items are represented by the object Item. An item can be a robot, a reference frame, a tool, an object or a specific project.
 * The `robodk module <https://robodk.com/doc/en/PythonAPI/robodk.html>`_ is a robotics toolbox for Python, inspired from Peter Corke's Robotics Toolbox: http://petercorke.com/Robotics_Toolbox.html.

The following website provides an overview of the RoboDK API for Python:
https://robodk.com/offline-programming

RoboDK can be used for a wide range of applications, such as 3D printing, robot machining, synchronizing multiple robots, pick and place...
 * Examples: https://robodk.com/examples
 * Blog: https://robodk.com/blog

How to install
==============

Type::

  pip install robodk


Requirements
============

RoboDK must be installed:
 * RoboDK Simulation Software: https://robodk.com/download

The Python API can be used with a free RoboDK license.


Example
=======

The following script shows an example that uses the RoboDK package for robot simulation and offline programming::

  from robolink import *    # RoboDK's API
  from robodk import *      # Math toolbox for robots
   
  # Start the RoboDK API:
  RDK = Robolink()
   
  # Get the robot item by name:
  robot = RDK.Item('Fanuc LR Mate 200iD', ITEM_TYPE_ROBOT)
   
  # Get the reference target by name:
  target = RDK.Item('Target 1')
  target_pose = target.Pose()
  xyz_ref = target_pose.Pos()
   
  # Move the robot to the reference point:
  robot.MoveJ(target)
   
  # Draw a hexagon around the reference target:
  for i in range(7):
      ang = i*2*pi/6 #ang = 0, 60, 120, ..., 360
      
      # Calculate the new position around the reference:
      x = xyz_ref[0] + R*cos(ang) # new X coordinate
      y = xyz_ref[1] + R*sin(ang) # new Y coordinate
      z = xyz_ref[2]              # new Z coordinate    
      target_pos.setPos([x,y,z])
      
      # Move to the new target:
      robot.MoveL(target_pos)
   
  # Trigger a program call at the end of the movement
  robot.RunCode('Program_Done')
   
  # Move back to the reference target:
  robot.MoveL(target)

The same script used for simulation can be used for offline programming, which means that the appropriate program can be generated for the robot being used. RoboDK supports a large number of robot controllers and it is easy to include compatibility for new robot controllers using Post Processors.

For more information about robot post processors:
 * https://robodk.com/help#PostProcessor
 * https://robodk.com/doc/en/Post-Processors.html
 * https://robodk.com/doc/en/PythonAPI/postprocessor.html

For more Examples:
 * https://robodk.com/doc/en/PythonAPI/examples.html


Documentation
=============

 * `RoboDK package for Python <https://robodk.com/doc/en/PythonAPI/index.html>`_
 * `Introduction to RoboDK for robot simulation and offline programming <https://robodk.com/offline-programming>`_
 * `RoboDK API documentation <https://robodk.com/doc/en/RoboDK-API.html#PythonAPI>`_


Supported robots
================

The following list includes the robot controllers supported by RoboDK:
 * ABB RAPID IRC5: for ABB IRC5 robot controllers
 * ABB RAPID S4C: for ABB S4C robot controllers
 * Adept Vplus: for Adept V+ programming language
 * Allen Bradley Logix5000: for Allen Bradley Logix5000 PCL
 * CLOOS: for CLOOS robot controllers
 * Comau C5G: for Comau C5G robot controllers
 * Denso PAC: for Denso RC7 (and older) robot controllers (PAC programming language)
 * Denso RC8: for Denso RC8 (and newer) robot controllers (PacScript programming language)
 * Dobot: for educational Dobot robots
 * Fanuc R30iA: for Fanuc R30iA and R30iB robot controllers
 * Fanuc R30iA Arc: for Fanuc Arc welding
 * Fanuc RJ3: for Fanuc RJ3 robot controllers
 * GCode BnR: for B&R robot controllers
 * GSK: for GSK robots
 * HIWIN HRSS: for HIWIN robots
 * KAIRO: for Keba Kairo robot controllers
 * KUKA IIWA: for KUKA IIWA sunrise programming in Java
 * KUKA KRC2: for KUKA KRC2 robot controllers
 * KUKA KRC2 CamRob: for KUKA CamRob milling option
 * KUKA KRC2 DAT: for KUKA KRC2 robot controllers including DAT data files
 * KUKA KRC4: for KUKA KRC4 robot controllers
 * KUKA KRC4 Config: for KUKA KRC4 robot controllers with configuration data in each line
 * KUKA KRC4 DAT: for KUKA KRC4 robot controllers including DAT data files
 * Kawasaki: for Kawasaki AS robot controllers
 * Mecademic: for Mecademic Meca500 robot
 * Motoman/Yaskawa: For Motoman robot controllers (JBI II and JBI III programming)
 * Mitsubishi: for Mitsubishi robot controllers
 * Nachi AX FD: for Nachi AX and FD robot controllers
 * Daihen OTC: for Daihen OTC robot controllers
 * Precise: for Precise Scara robots
 * Siemens Sinumerik: for Siemens Sinumerik ROBX robot controller
 * Staubli VAL3: for Staubli VAL3 robot programs (CS8 controllers and later)
 * Staubli VAL3 InlineMove: to generate Staubli VAL3 programs with inline movement data
 * Staubli S6: for Staubli S6 robot controllers
 * Toshiba: for Toshiba robots
 * Universal Robots: for UR robots, generates linear movements as pose targets
 * Universal Robots RobotiQ: for UR robots including support for RobotiQ gripper
 * Universal Robots joints: for UR robots, generates linear movements as joint targets
 * Yamaha: for Yamaha robots


