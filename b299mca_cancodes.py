#
# B299MCA commands for controlling the KLIPPEL GmbH Test system
# Schema for the CAN sequence tuples are:
# command_tuple = ["ECU_REQ_ID", "command service", "DID", "parameter", "access level required", "data to be sent"]
#    access level 03 or 01 will trigger a mode 10 message to the ECU before command DID is sent - other values ignored.
#    command service, DID, parameter, access and data are passed to CAN message as example:
#    ECU_ID, command service, DID, parameter, access, data :  727 2F 61A1 03 0A
#    ECUreqID is blank then the default value on .ini file is used.
#

import configparser
#from ConfigFile import *

cfg = configparser.ConfigParser()
global canFunctionSets
canFunctionSets = []

def cancodes_init(config_file):
    global canFunctionSets
    # global config_file
    # config_file = c
    print("cancodes start...")
    #print("Command file loaded = Lou Master Test")
    # print("cancodes start..." + str(config_file))
    # fileOK = cfg.read("oobd_control_C346.ini")

    fileOK = cfg.read(config_file)
    if fileOK:
        print("ini file read in Can Codes = " + str(fileOK))
    else:
        print("Missing Config File!!")

    # steps for the percentage instead of 0-30 input
    volume_steps = ['00', '05', '0d', '16', '1e', '27', '2f', '38', '40', '49', '51', '5a', '62', '6b', '73', '7c', '84',
                    '8d', '95', '9e', 'a6', 'af', 'b7', 'c0', 'c8', 'd1', 'd9', 'e2', 'ea', 'f3', 'fb']
    # added by LVB to streamline hex formatting vs below.
    fm_freq = format((int(10 * float(cfg['DUT']['FM_FREQ'])) - 875), '02x')

    print("default freq  = " + cfg['DUT']['FM_FREQ'] + " hex = " + fm_freq)
    print("default ECU ID = " + cfg['CAN']['defaultReqID'])
    print("default volume front = " + cfg['DUT']['VOLUME_FRONT'])
    print("default volume rear = " + cfg['DUT']['VOLUME_REAR'])
    print("CAN Channel = " + cfg['CAN']['busType'])
    print("CAN Speed = " + cfg['CAN']['speed'])

    # set freq to value in ini file.
    set_freq = {"reqID": '727',
                "cmd": '2f',
                "DID": '61a1',
                "parameter": '03',
                "access": '03',
                "data": fm_freq}

    # Sets the volume to value given in the config
    set_volume_front = {"reqID": '727',
                    "cmd": '2e',
                    "DID": '833b',
                    "parameter": '03',
                    "access": '03',
                    "data": volume_steps[int(cfg['DUT']['VOLUME_FRONT'])]}

    # some visteon may use 0xFD28?? 2E
    # Sets the volume to value given in the config
    set_volume_rear = {"reqID": '727',
                   "cmd": '2e',
                   "DID": '833b',
                   "parameter": '03',
                   "access": '03',
                   "data": volume_steps[int(cfg['DUT']['VOLUME_REAR'])]}

    # ============================================================================================================
    # set freq to user defined value.  See 31.1.3.1    MMDIAG-IF00004-FM&TMC Tuner Test Mode_Common GGDS Interface
    set_freq_x = {"reqID": '727',
                  "cmd": '2f',
                  "DID": '61a1',
                  "parameter": '03',
                  "access": '03',
                  "data": ''}  # defined later



    # Sets the volume to value passed at function call
    set_volume_x = {"reqID": '727',
                    "cmd": '2f',
                    "DID": '833b',
                    "parameter": '03',
                    "access": '03',
                    "data": '00'}  # define default as 0




    # Sets the treble for Visteon
    # For Panasonic set DID fda2 AHU
    set_treb_visteon = {"reqID": '727',
                "cmd": '2e',
                "DID": 'fd2c',
                "parameter": '03',
                "access": '03',
                "data": '00'}


    # Sets the bass to maximum for Visteon
    # For Panasonic set DID fda3 AHU
    set_bass_visteon = {"reqID": '727',
                "cmd": '2e',
                "DID": 'fd2b',
                "parameter": '03',
                "access": '03',
                "data": '07'}

    # Sets the bass to value passed at function call
    # For Panasonic set DID fda3 AHU not fd2b
    set_bass_x_pana = {"reqID": '727',
                  "cmd": '2f',
                  "DID": 'fda3',
                  "parameter": '03',
                  "access": '03',
                  "data": ''}  # defined later

    # Sets the treble to value passed at function call
    # For Panasonic set DID fda2 AHU
    set_treb_x_pana = {"reqID": '727',
                  "cmd": '2f',
                  "DID": 'fda2',
                  "parameter": '03',
                  "access": '03',
                  "data": ''}  # defined later

    # Enables only the left front speaker
    # see "Global AHU SPSS ver2.3 4-21-2010.doc"  section 31.6.2.1    MMDIAG-IF00007-Speaker
    set_lf_on = {"reqID": '727',
                 "cmd": '2f',
                 "DID": '8003',
                 "parameter": '03',
                 "access": '03',
                 "data": 'fd ff ff ff ff ff ff ff'}

    # Enables only the left front speaker  for Clarion AHU uses 4 bytes only
    set_lf_on_4 = {"reqID": '727',
                   "cmd": '2f',
                   "DID": '8003',
                   "parameter": '03',
                   "access": '03',
                   "data": 'fdffffff'}

    # Enables left front speaker and left tweeter
    # see "Global AHU SPSS ver2.3 4-21-2010.doc"  section 31.6.2.1   Global AHU SPSS v2.17 Jun 9 2014  MMDIAG-IF00007-Speaker
    set_lf_on_twt = {"reqID": '727',
                     "cmd": '2f',
                     "DID": '8003',
                     "parameter": '03',
                     "access": '03',
                     "data": 'fdfdffffffffffff'}

    # Enables left front speaker and left tweeter  4 bytes for Clarion
    set_lf_on_twt_4 = {"reqID": '727',
                       "cmd": '2f',
                       "DID": '8003',
                       "parameter": '03',
                       "access": '03',
                       "data": 'fdfdffff'}

    # Enables all speakers  4 bytes for Clarion
    set_all_on_4 = {"reqID": '727',
                    "cmd": '2f',
                    "DID": '8003',
                    "parameter": '03',
                    "access": '03',
                    "data": '30fcffff'}

    # Enables all speakers  8 bytes for panasonic
    set_all_on = {"reqID": '727',
                  "cmd": '2f',
                  "DID": '8003',
                  "parameter": '03',
                  "access": '03',
                  "data": '30fcffffffffffff'}

    # Enables only the right front speaker
    set_rf_on = {"reqID": '727',
                 "cmd": '2f',
                 "DID": '8003',
                 "parameter": '03',
                 "access": '03',
                 "data": 'fe ff ff ff ff ff ff ff'}

    # Enables only the right front speaker 4 bytes for Clarion
    set_rf_on_4 = {"reqID": '727',
                   "cmd": '2f',
                   "DID": '8003',
                   "parameter": '03',
                   "access": '03',
                   "data": 'feffffff'}

    # Enables the right front speaker and right tweeter
    set_rf_on_twt = {"reqID": '727',
                     "cmd": '2f',
                     "DID": '8003',
                     "parameter": '03',
                     "access": '03',
                     "data": 'fefeffffffffffff'}

    # Enables the right front speaker and right tweeter 4 bytes for Clarion
    set_rf_on_twt_4 = {"reqID": '727',
                       "cmd": '2f',
                       "DID": '8003',
                       "parameter": '03',
                       "access": '03',
                       "data": 'fefeffff'}

    # Enables only the right rear speaker
    set_rr_on = {"reqID": '727',
                 "cmd": '2f',
                 "DID": '8003',
                 "parameter": '03',
                 "access": '03',
                 "data": 'fb ff ff ff ff ff ff ff'}

    # Enables only the right rear speaker 4 bytes for Clarion
    set_rr_on_4 = {"reqID": '727',
                   "cmd": '2f',
                   "DID": '8003',
                   "parameter": '03',
                   "access": '03',
                   "data": 'fbffffff'}

    # Enables only the left rear speaker
    set_lr_on = {"reqID": '727',
                 "cmd": '2f',
                 "DID": '8003',
                 "parameter": '03',
                 "access": '03',
                 "data": 'f7 ff ff ff ff ff ff ff'}

    # Enables only the left rear speaker    4 bytes for Clarion
    set_lr_on_4 = {"reqID": '727',
                   "cmd": '2f',
                   "DID": '8003',
                   "parameter": '03',
                   "access": '03',
                   "data": 'f7ffffff'}
    # Enables only the center speaker tweeter
    set_cntr_on_twt = {"reqID": '727',
                       "cmd": '2f',
                       "DID": '8003',
                       "parameter": '03',
                       "access": '03',
                       "data": 'ffefffffffffffff'}

    # Enables only the center speaker tweeter 4 bytes for Clarion
    set_cntr_on_twt_4 = {"reqID": '727',
                         "cmd": '2f',
                         "DID": '8003',
                         "parameter": '03',
                         "access": '03',
                         "data": 'ffefffff'}

    # Enables only the center speaker
    set_cntr_on = {"reqID": '727',
                   "cmd": '2f',
                   "DID": '8003',
                   "parameter": '03',
                   "access": '03',
                   "data": 'bfffffffffffffff'}
    # Enables only the center speaker 4 bytes for Clarion
    set_cntr_on_4 = {"reqID": '727',
                     "cmd": '2f',
                     "DID": '8003',
                     "parameter": '03',
                     "access": '03',
                     "data": 'bfffffff'}

    # Enables only the subwoofer
    set_subwoofer_on = {"reqID": '727',
                        "cmd": '2f',
                        "DID": '8003',
                        "parameter": '03',
                        "access": '03',
                        "data": '7fffffffffffffff'}

    # Enables only the subwoofer    4 bytes for Clarion
    set_subwoofer_on_4 = {"reqID": '727',
                          "cmd": '2f',
                          "DID": '8003',
                          "parameter": '03',
                          "access": '03',
                          "data": '7fffffff'}

    # reads VIN stored in AHU
    read_vin_ahu = {"reqID": '727',
                "cmd": '22',
                "DID": 'f190',
                "parameter": '',
                "access": '',
                "data": ''}  # defined later

    # reads VIN stored in SYNC
    read_vin_sync = {"reqID": '7D0',
                     "cmd": '22',
                     "DID": 'f190',
                     "parameter": '',
                     "access": '03',
                     "data": ''}  # defined later

    # reads VIN stored in ABS for S550
    read_vin_abs = {"reqID": '760',
                    "cmd": '22',
                    "DID": 'f190',
                    "parameter": '',
                    "access": '03',
                    "data": ''}  # defined later

    # reads VIN stored in BCM
    read_vin_bcm = {"reqID": '726',
                     "cmd": '22',
                     "DID": 'f190',
                     "parameter": '',
                     "access": '03',
                     "data": ''}  # defined later

    # reads VIN stored in AHU
    read_vin_ahu = {"reqID": '727',
                     "cmd": '22',
                     "DID": 'f190',
                     "parameter": '',
                     "access": '03',
                     "data": ''}  # defined later


    # reads VIN stored in Cluster
    read_vin_ipc = {"reqID": '720',
                     "cmd": '22',
                     "DID": 'f190',
                     "parameter": '',
                     "access": '03',
                     "data": ''}  # defined later

    # sends radio on command to MFD
    radio_on = {"reqID": '7a5',
                "cmd": '2f',
                "DID": '8051',
                "parameter": '03',
                "access": '03',
                "data": '10000000ffffffff'}

    # sends radio on command to AHU
    radio_on_ahu = {"reqID": '727',
                    "cmd": '2f',
                    "DID": '7215',
                    "parameter": '03',
                    "access": '03',
                    "data": '01'}

    # sends radio on command to SYNC for GEN3??
    radio_on_sync = {"reqID": '7D0',
                    "cmd": '2f',
                    "DID": '7215',
                    "parameter": '03',
                    "access": '03',
                    "data": '01'}

    canFunctionSets = {"setFreq": set_freq,
                       "setFreqX": set_freq_x,  # x in freq x 10 ex 983 = 98.3
                       "setVolumeFront": set_volume_front,
                       "setVolumeRear": set_volume_rear,
                       "setBass": set_bass_visteon,
                       "setTreb": set_treb_visteon,
                       "setBassX": set_bass_x_pana,  # x in hex
                       "setTrebX": set_treb_x_pana,  # x in hex
                       "readVIN": read_vin_ahu,
                       "readVINsync": read_vin_sync,  # sends VIN command to SYNC
                       "readVINabs": read_vin_abs,  # sends VIN command to abs
                       "readVINbcm": read_vin_bcm,  # sends VIN command to bcm
                       "readVINipc": read_vin_ipc,  # sends VIN command to cluster
                       "speakerEnableRF": set_rf_on,
                       "speakerEnableRFtwt": set_rf_on_twt,
                       "speakerEnableLF": set_lf_on,
                       "speakerEnableLFtwt": set_lf_on_twt,
                       "speakerEnableRR": set_rr_on,
                       "speakerEnableLR": set_lr_on,
                       "speakerEnableCntr": set_cntr_on,
                       "speakerEnableCntrtwt": set_cntr_on_twt,
                       "speakerEnableSub": set_subwoofer_on,
                       "speakerEnableRF4": set_rf_on_4,  # for clarion
                       "speakerEnableRFtwt4": set_rf_on_twt_4,
                       "speakerEnableLF4": set_lf_on_4,
                       "speakerEnableLFtwt4": set_lf_on_twt_4,
                       "speakerEnableRR4": set_rr_on_4,
                       "speakerEnableLR4": set_lr_on_4,
                       "speakerEnableCntr4": set_cntr_on_4,
                       "speakerEnableCntrtwt4": set_cntr_on_twt_4,
                       "speakerEnableSub4": set_subwoofer_on_4,
                       "speakerEnableAllOn4": set_all_on_4,
                       "speakerEnableAllOn": set_all_on,
                       "radioOn": radio_on,  # sends command to MFD
                       "radioOnSYNC": radio_on_sync,  # sends command to MFD
                       "radioOnahu": radio_on_ahu,  # GEN3 SYNC?
                       "setVolumeX": set_volume_x}  # x in hex 00 to 1D
