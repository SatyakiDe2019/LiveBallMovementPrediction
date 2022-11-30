################################################
#### Written By: SATYAKI DE                 ####
#### Written On:  15-May-2020               ####
#### Modified On: 25-Jul-2022               ####
####                                        ####
#### Objective: This script is a config     ####
#### file, contains all the keys for        ####
#### best bowling prediction from a sports  ####
#### streaming.                             ####
####                                        ####
################################################

import os
import platform as pl

class clsConfigClient(object):
    Curr_Path = os.path.dirname(os.path.realpath(__file__))

    os_det = pl.system()
    if os_det == "Windows":
        sep = '\\'
    else:
        sep = '/'

    conf = {
        'APP_ID': 1,
        'ARCH_DIR': Curr_Path + sep + 'arch' + sep,
        'PROFILE_PATH': Curr_Path + sep + 'profile' + sep,
        'LOG_PATH': Curr_Path + sep + 'log' + sep,
        'REPORT_PATH': Curr_Path + sep + 'output' + sep,
        'REPORT_DIR': 'output',
        'SRC_PATH': Curr_Path + sep + 'data' + sep,
        'FINAL_PATH': Curr_Path + sep + 'Target' + sep,
        'IMAGE_PATH': Curr_Path + sep + 'Scans' + sep,
        'TEMPLATE_PATH': Curr_Path + sep + 'Template' + sep,
        'APP_DESC_1': 'Predicting the direction of football!',
        'DEBUG_IND': 'N',
        'INIT_PATH': Curr_Path,
        'SUBDIR': 'data',
        'TITLE': "Predicting the direction of football!",
        'PATH' : Curr_Path,
        'BASE_FILE': 'CrickB.mp4',
        'BASE_IMAGE_FILE': 'CrickB.jpeg',
        'FORMAT': 'JSON',
        'RESOLUTION': 350,
        'THREAD_NUM': 1,
        'HSV': {'hmin': 173, 'smin':177, 'vmin':57, 'hmax':178, 'smax':255, 'vmax':255},
        'PAUSE': 0.5,
        'POINT_1': 575,
        'POINT_2': 380,
        'POINT_3': 730,
        'POINT_4': 725
    }
