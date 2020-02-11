"""
############################################################################################################
############################################################################################################
Electro Industries/GaugeTech Shark 200 Data Logging Settings


--------------------------------------------------------------------------------------
Below you will find a python 'list' object called 'settings'. Each item in this list is a
python 'tuple' object that represents a Shark 200 meter that you wish to pull data from. Each tuple also requires several parameters that must
be entered in manually:


     # Explanation of Parameters:
    --------------------------------------------------------------------------------------
 - METER NAME: This is for your convenience, only effects the names of the .csv files that contain the data, and may be left blank if you so choose.
     -- If you do choose to assign meter names for each meter, please try to avoid characters that are not valid for windows/linux filenames.

 - HOST: This is the IP address of the meter you wish to pull data from. Please enter it as a string (with '' around it).

 - PORT: The port the specific device is using for Modbus communication. Usually 502 or 503.

 - TIMESTEP: Here you can choose the interval between data measurements (in seconds). You unfortunately you must choose the same timestep for each meter.

 - NUMBER OF DECIMAL PLACES: Here you can choose how many decimal places to round your data.

 - VALUES: The final item in each tuple is a list containing every value currently available for measurement. If you only want specific values,
           please comment out any you do not wish to include.
    --------------------------------------------------------------------------------------


    # Instructions
    --------------------------------------------------------------------------------------
    I. Set your timestep(in seconds). This value will be applied accross all your meters.

    II. In the 'settings' list, you will find a meter called 'test_meter' already entered complete with all required paramters.
        A. Copy and paste this tuple for each meter you wish to pull data from.
            1. Fill in the required parameters (meter name, host, port,and number of decimal places) for each meter you add.
                i. PLEASE USE REASONABLE NAMES FOR YOUR METERS!!! (meter_1, meter_2, test_meter) <-- Good examples
            2. For each meter, comment out any unwanted measured values in the MEASURED VALUES column.
        B. The test meter is only for reference purposes and connects to the Electro Industries internet-connected
            Shark 200 meter which you can view at www.mynexusmeter.com:8081
            Feel free to remove the test meter if you so choose.

    III. If using an IDE, Run 'shark_200_meter_settings.py' to make sure there are no syntax errors, otherwise, check the logs in the main script for syntax errors.

    IV. Save 'shark_200_meter_settings.py'

    V. Close the file
    --------------------------------------------------------------------------------------


--------------------------------------------------------------------------------------


############################################################################################################
############################################################################################################
"""







    # Set your Desired Timestep
#------------------------------------------------------
TIMESTEP = 4
#------------------------------------------------------


settings = [

# EXAMPLE:

#             (str)     (str)   (int)        (int)                (int)         MEASURED VALUES:
#        ('METER NAME', 'HOST', PORT, NUMBER OF DECIMAL PLACES, UNIT ID, (
#                                                                                 'Volts A-N',
#                                                                                 'Volts B-N',
#                                                                                 'Volts C-N',
#                                                                                 'Volts A-B',
#                                                                                 'Volts B-C',
#                                                                                 'Volts C-A',
#                                                                                 'Amps A',
#                                                          Commented-out values   #'Amps B',
#                                                          will not show up in    #'Amps C',
#                                                          the final .csv files   #'Watts 3-Ph total',
#                                                                                 'VARs 3-Ph total',
#                                                                                 'VAs 3-Ph total',
#                                                                                 'Power Factor 3-Ph total',
#                                                                                 'Frequency',
#                                                                                 'Neutral Current',
#                                                                                 'Watts Phase A',
#                                                                                 'Watts Phase B',
#                                                                                 'Watts Phase C',
#                                                                                 'VARs Phase A',
#                                                                                 'VARs, Phase B',
#                                                                                 'VARs Phase C',
#                                                                                 'VAs Phase A',
#                                                                                 'VAs Phase B',
#                                                                                 'VAs Phase C',
#                                                                                 'Power Factor Phase A',
#                                                                                 'Power Factor Phase B',
#                                                                                 'Power Factor Phase C',
#                                                                                 'Symmetrical Component Magnitude 0 Seq',
#                                                                                 'Symmetrical Component Magnitude + Seq',
#                                                                                 'Symmetrical Component Magnitude - Seq')
##             ),


    ('Galena_1', '169.254.102.39', 502, 3, 1, [
                                                         'Volts A-N',
                                                         'Volts B-N',
                                                         'Volts C-N',
                                                         'Volts A-B',
                                                         'Volts B-C',
                                                         'Volts C-A',
                                                         'Amps A',
                                                         'Amps B',
                                                         'Amps C',
                                                         'Watts 3-Ph total',
                                                         'VARs 3-Ph total',
                                                         'VAs 3-Ph total',
                                                         'Power Factor 3-Ph total',
                                                         'Frequency',
                                                         'Neutral Current',
                                                         'Watts Phase A',
                                                         'Watts Phase B',
                                                         'Watts Phase C',
                                                         'VARs Phase A',
                                                         'VARs, Phase B',
                                                         'VARs Phase C',
                                                         'VAs Phase A',
                                                         'VAs Phase B',
                                                         'VAs Phase C',
                                                         'Power Factor Phase A',
                                                         'Power Factor Phase B',
                                                         'Power Factor Phase C',
                                                         'Symmetrical Component Magnitude 0 Seq',
                                                         'Symmetrical Component Magnitude + Seq',
                                                         'Symmetrical Component Magnitude - Seq']
             ),

    ('Galena_2', '169.254.102.39', 502, 3, 2, [
        'Volts A-N',
        'Volts B-N',
        'Volts C-N',
        'Volts A-B',
        'Volts B-C',
        'Volts C-A',
        'Amps A',
        'Amps B',
        'Amps C',
        'Watts 3-Ph total',
        'VARs 3-Ph total',
        'VAs 3-Ph total',
        'Power Factor 3-Ph total',
        'Frequency',
        'Neutral Current',
        'Watts Phase A',
        'Watts Phase B',
        'Watts Phase C',
        'VARs Phase A',
        'VARs, Phase B',
        'VARs Phase C',
        'VAs Phase A',
        'VAs Phase B',
        'VAs Phase C',
        'Power Factor Phase A',
        'Power Factor Phase B',
        'Power Factor Phase C',
        'Symmetrical Component Magnitude 0 Seq',
        'Symmetrical Component Magnitude + Seq',
        'Symmetrical Component Magnitude - Seq']
     ),

]
