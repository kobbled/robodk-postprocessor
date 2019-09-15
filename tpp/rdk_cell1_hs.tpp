#*****************
# robodk initialization
#-----------------
# Initialization program for transverse templates (eg. Bands, Spiral, Pads).
# -Sets UF and UT offsets. 
# -Convert any inch dimensions to mm
# -Include beam width into start and stop measurements
# -Calculate layer bevelling in the x-direction.
# -Calculate layer step offset
# -make PR's for start off set position, as well as a PR for the approch point
#*****************

TP_GROUPMASK = "1,*,1,1,*"
TP_COMMENT = "hs init"

#run parameter file
eval "CALL SR[2]"

#Call Home
#-----------
if !skipHTHome && !Hmi_Dry_Run
    #warn when indecies are <> 0
    indexSet()
    # abort when chuck is not zeroed.
    CheckRotZero()
    G1_HOME_RBT_HTSTOCK()
    G4_HOME_HT_STOCK()
end

if !Laser_Aiming_Beam
    # Turn aiming beam on
    turn_on Laser_Aiming_Beam
end

#Uframe rotation
UF_DIAMROT(diameter,&UF_zRot)
UF_zRot = -1*UF_zRot
#look into modifying the r of the leader frame
#default static frame
Rotate_Offset.group(4).x = UF_zRot

#Utool rotation
TOOLCHANGE()

#Set Frames
use_uframe 0
use_utool 1

#clear offset registers
CLRPR(&Offst_apprch)
CLRPR(&Offst_dprt)
CLRPR(&Start_Offset)
CLRPR(&Stop_Offset)


#might have to incorperate x & y offsets
# as well to keep 
#headstock offset
SETOFFST(&Offst_apprch,4,1,ofst_apr,1)
#depart offset
SETOFFST(&Offst_dprt,4,1,ofst_dpt,1)
#laser start
SETOFFST(&Start_Offset,4,1,ofst_lasStart,1)
#laser stop
SETOFFST(&Stop_Offset,4,1,ofst_lasStop,1)

#translational offsets
SETOFFST(&Rotate_Offset,4,1,ofst_xRot,1)
SETOFFST(&Rotate_Offset,3,1,ofst_zStart,0)
#x & y offsets would have to be modified
#on each index need to convert into cartesian
#space in background
SETOFFST(&Rotate_Offset,1,1,ofst_xStart,0)
SETOFFST(&Rotate_Offset,1,1,ofst_yStart,0)

#add trans offsets into start/stops
# ADD PR offsets
Start_Offset  += Rotate_Offset
Offst_apprch  += Start_Offset
Stop_Offset   += Rotate_Offset
Offst_dprt    += Stop_Offset

#initialize dimensions
Dim_Checks()

#Rail calculations
rail_calc()

#swap variables
lengthswap = length
pitchSwap = pitch
passSwap = passes
passPauseSwap = passPause
ofst_LayerXSwap = ofst_LayerX


reset tLaser
reset tPowder
G0_LASER_ENABLE()
POWDERATES()
LASERPOWER(HMI_Laser_Power)

if !Hmi_Dry_Run
    POS_HT_Powder1()
    start tPowder
    G0_POWDER_START()
end
if !skipHTHome
    POS_HT_INTER()
end

#start layer loop
l = lStart
while l < layers
    POWDERATES()
    SPEEDRATES(diameter)
    if (layers > 1) && (l < layers) && (l > lStart) && (isTest == 1)
        GST_HT_PAUSE()
        POS_HT_INTER()
    end
    m = mStart
    while m < bands
        k = kStart
        while k < pockets
            if (pocketPause > 0) && (k > kStart)
                if (k % pocketPause == 0)
                    GST_PAUSE()
                    POS_POS_APPR(tRadius)
                end
            end
            #add pocket offsets
            # add offsets
            Rotate_Offset = Ofst_UFRot + Rotate_Offset
            Rotate_Offset.group(4).x += pocketSep*k
            Start_Offset += Rotate_Offset
            Stop_Offset += Rotate_Offset
            Offst_apprch += Start_Offset
            Offst_dprt += Stop_Offset
            #start on pass
            j=jStart
            #call path program
            eval "CALL SR[3]"
            k += 1
        end # end pockets
        m += 1
    end # end bands
    l += 1
end # end layers


@exit
