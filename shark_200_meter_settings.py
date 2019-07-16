"""
############################################################################################################
############################################################################################################
Electro Industries/GaugeTech™ Shark® 200 Data Logging Settings


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
 
 - TIMESTEP: Here you can choose the interval between data measurements (in seconds). Timesteps below 5 seconds are not recommended especially if you
             are pulling data from multiple meters.
             
 - NUMBER OF DECIMAL PLACES: Here you can choose how many decimal places to round your data.
 
 - VALUES: The final item in each tuble is another tuple containing every value currently available for measurement. If you only want specific values,
           please comment out any you do not wish to include.
    --------------------------------------------------------------------------------------
    
    
    # Instructions
    --------------------------------------------------------------------------------------
    I. In the 'settings' list, you will find a meter called 'test_meter' already entered complete with all required paramters. Please copy and paste
        This tuple for each meter you wish to pull data from and enter in the required parameters/comment out any unwanted measured values.
        
    II. Save 'shark_200_meter_settings.py'
    
    III. Close the file
    --------------------------------------------------------------------------------------
 

--------------------------------------------------------------------------------------


############################################################################################################
############################################################################################################
"""









 


settings = [

# EXAMPLE:

#             (str)     (str)   (int)        (int)               (int)          
#        ('METER NAME', 'HOST', PORT, TIMESTEP(seconds), NUMBER OF DECIMAL PLACES, (
#                                                                                 'Volts A-N',
#                                                                                 'Volts B-N',
#                                                                                 'Volts C-N',
#                                                                                 'Volts A-B',
#                                                                                 'Volts B-C',
#                                                                                 'Volts C-A',
#                                                                                 'Amps A',
#                                                                                 'Amps B',
#                                                                                 'Amps C',
#                                                                                 'Watts 3-Ph total',
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
    
            ('test_meter', '75.127.189.115', 503, 30, 3, (
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
                                                         'Symmetrical Component Magnitude - Seq')
             ), 
    
    ]