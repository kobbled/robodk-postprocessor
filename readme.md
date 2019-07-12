# robodk post processor for Fanuc laser welding robots

## is configured for running on a Fanuc R30iB robot controller

```python
|-> Posts  # Contains post processor files
|-> Python # Contains robodk package files
|-> Tests  # Contains test code for robodk modules
```

* set **GRP_TRACK**, or **GRP_TURNTABLE** to the group number the track or turntable is respectively. If track is incorperated into the robot "i.e. E1 = 100 mm" leave **GRP_TRACK = 0**


```python
    def MoveJ(self, pose, joints, conf_RLF=None):
    def MoveL(self, pose, joints, conf_RLF=None):
```

Needs both a pose object (transformation matrix) as well as a joint list
