#####################################################
#### Written By: SATYAKI DE                      ####
#### Written On: 25-Nov-2022                     ####
#### Modified On 30-Nov-2022                     ####
####                                             ####
#### Objective: This is the main calling         ####
#### python script that will invoke the          ####
#### clsPredictBodyLine class to initiate        ####
#### the predict capability in real-time         ####
#### from a cricket (Sports) streaming.          ####
#####################################################

# We keep the setup code in a different class as shown below.
import clsPredictBodyLine as pbdl

from clsConfigClient import clsConfigClient as cf

import datetime
import logging

def main():
    try:
        # Other useful variables
        debugInd = 'Y'
        var = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        var1 = datetime.datetime.now()

        print('Start Time: ', str(var))
        # End of useful variables

        # Initiating Log Class
        general_log_path = str(cf.conf['LOG_PATH'])

        # Enabling Logging Info
        logging.basicConfig(filename=general_log_path + 'predBodyLine.log', level=logging.INFO)

        print('Started predicting best bodyline deliveries from the Cricket Streaming!')

        # Passing source data csv file
        x1 = pbdl.clsPredictBodyLine()

        # Execute all the pass
        r1 = x1.processVideo(debugInd, var)

        if (r1 == 0):
            print('Successfully predicted body-line deliveries!')
        else:
            print('Failed to predict body-line deliveries!')

        var2 = datetime.datetime.now()

        c = var2 - var1
        minutes = c.total_seconds() / 60
        print('Total difference in minutes: ', str(minutes))

        print('End Time: ', str(var1))

    except Exception as e:
        x = str(e)
        print('Error: ', x)

if __name__ == "__main__":
    main()
