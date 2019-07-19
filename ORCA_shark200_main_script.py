import pandas as pd
import numpy as np
import pyModbusTCP
from pyModbusTCP.client import ModbusClient
import struct
import logging
import timeit
import time
import datetime
import copy
import csv
import os
import shark_200_meter_settings
import shark_200_readings_blocks


    
"""
--------------------------------------------------------------------------------------
Electro Industries/GaugeTech™ Shark® 200 Data Logging Script version 0.5.7.15

Developed for the Alaska Center for Energy and Power ORCA(Onsite Real-time Collection and Acquisition)
data collection project, summer 2019.
--------------------------------------------------------------------------------------

 - This script is designed to read, format, and output power data from the Shark 200 power meter using
ModbusTCP and various python libraries to organize the data and make it human readable. This script is
designed to be run on start-up and will automatically produce .csv files (with column headers) in its current directory

 - Before setting up the script to run on startup, please see the 'INPUTS:' section below. Here you will find several
 parameters that must be entered:
 
     *host: The ORCA meter is designed to be linked via ethernet to a powerhouse's network. The host is simply the
     specific







"""  
    
    
    
    
    
    
    
    
    #TODO:
#--------------------------------------------------------------------------------------
# - Create variable-length csv files? More/less than  one day
# - Setup a seperate logging file for each of the meters.
# - Make sure that the new .csv files are created at the beginning of the hour and aren't held up by connection issues.


# - At some point, change the readings section instructions to include more than the 1000-to-1059 range
# -- When that's done, change the output (to_csv) dataframe to be a seperate main dataframe that the
#....block-specific dataframes are appended to.
#--------------------------------------------------------------------------------------    
    
    

#--------------------------------------------------------------------------------------


    # Choose which values you want exported  
#--------------------------------------------------------------------------------------
readings =    ((                       # From here you can edit which values from the
                'Volts A-N',           #...shark200 you want. The full list can be found
                'Volts B-N',           #...in the shark200 user's manual, Appendix B,
                'Volts C-N',           #...pages MM-2 to MM-3, 'Primary Readings Block',
                'Volts A-B',           #...Modbus Address, Decimal: 1000 to 1053.
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
                'VARs Phase B',
                'VARs Phase C',
                'VAs Phase A',
                'VAs Phase B',
                'VAs, Phase C',
                'Power Factor Phase A',
                'Power Factor Phase B',
                'Power Factor Phase C',
                'Symmetrical Component Magnitude 0 Seq',
                'Symmetrical Component Magnitude + Seq',
                'Symmetrical Component Magnitude - Seq'
                ))
#--------------------------------------------------------------------------------------

    # Setup logging file
#--------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------


    # Column names for the variables listed in the Shark 200 user's manual.
    
    # !!! DO NOT CHANGE !!!
#--------------------------------------------------------------------------------------
#primary_readings_columns = (('timestamp',
#                                 'Volts A-N',
#                                 'Volts B-N',
#                                 'Volts C-N',
#                                 'Volts A-B',
#                                 'Volts B-C',
#                                 'Volts C-A',
#                                 'Amps A',
#                                 'Amps B',
#                                 'Amps C',
#                                 'Watts 3-Ph total',
#                                 'VARs 3-Ph total',
#                                 'VAs 3-Ph total',
#                                 'Power Factor 3-Ph total',
#                                 'Frequency',
#                                 'Neutral Current',
#                                 'Watts Phase A',
#                                 'Watts Phase B',
#                                 'Watts Phase C',
#                                 'VARs Phase A',
#                                 'VARs, Phase B',
#                                 'VARs Phase C',
#                                 'VAs Phase A',
#                                 'VAs Phase B',
#                                 'VAs Phase C',
#                                 'Power Factor Phase A',
#                                 'Power Factor Phase B',
#                                 'Power Factor Phase C',
#                                 'Symmetrical Component Magnitude 0 Seq',
#                                 'Symmetrical Component Magnitude + Seq',
#                                 'Symmetrical Component Magnitude - Seq'))

#--------------------------------------------------------------------------------------



    # Supporting Functions
#######################################################################################
#######################################################################################
def getModbusData(host, port, start_register, end_register):                                                               
    
    # Returns a list containing the data from each Modbus register between
    #...and including the start and end register
  
    # Depending on the format of any particular value you want, its data may be distributed
    #...over multiple registers and will require further formatting to be human-readable.
                                                              
    # This function only returns the data directly taken from the device's Modbus registers.
    
        # Setting up the client 
    #----------------------------------------------------
    client = ModbusClient()     # Creates a Modbus client opject 
    client.host(host)           # Assigns the specified host (IP) address to the client      
    client.port(port)           # Assigns the specified port to the client
    
    start_register -= 2     # The Modbus registers listed in the Shark200 User's manual
    end_register -= 2       #...are all offset by 2 from their actual values,
                            #...so we account for that here.
    
    num_of_registers = end_register - start_register + 1
    # Since the registers are taken as integers, we can take the range between the start and end
    #...registers and add 1 to get the total number of registers to query.
                                                                                                                            
    #----------------------------------------------------
        
        # Reading the device's Modbus registers
    #----------------------------------------------------
    

    
    client.open()     # Opens the connection
    
    response = client.read_holding_registers(start_register, num_of_registers)
                # This function returns a list of values, one for each of the Modbus registers specified.
                # It works even if some of the registers queried have data stored in different formats,
                #...so be careful not to automatically treat all data the same.
    
    client.close()     # Closes the connection
    
    #----------------------------------------------------
    
    
    return response




def format32BitFloat(array):
    
    # Most of the relevant values for most power/energy related uses are stored across
    #...two Modbus registers as integers with the first register containing the least
    #...significant data and the second containing the most significant.
    # In order to transform the two integers into one single precision floating-point
    #...number that is also easily human-readable, we must multiply the second integer
    #...by 2^16 and add it to the first integer. We can then use the 'struct' python library
    #...to pack the summed integer as binary data and unpack it as the format we want (i.e. float).
    
    output = []
    
    for index, item in enumerate(array):    # Enumerate to keep track of the index
        if index%2 == 0:                    # We want to begin with every even value
            
            packed = struct.pack('I', item + array[index+1]*2**16) 
            # 'I' indicates the input to be an unsigned integer. This is neccessary for
            #...dealing with negative numbers and will correctly display them as negative.
            unpacked = struct.unpack('f', packed) 
            # 'f' indicates the output to be float
            output.append(unpacked[0]) # the unpack() function returns a tuple, so we index
                                       #...the first item out and we have our fully formatted
                                       #...float value.       
    return output


def checkConnection(host):
    
    client = ModbusClient()
    client.host(host)
    client.open()
    
    if client.is_open():
        status = True
    else:
        status = False
        
    client.close()
    
    return status

#######################################################################################
#######################################################################################


def main():  # Primary function that contains the data collection loop

        # Logging
    #---------------------------------------------------------------------------------
    logging.basicConfig(filename='log.txt', format='%(asctime)s-%(levelname)s: %(message)s', level=logging.INFO)                     
    #--------------------------------------------------------------------------------- 
    
    
    
    ###################################################################################
    ###################################################################################
    while True:     # Data collection loop
        
            # Start Timer
        ##############################
        start = timeit.default_timer()
        ##############################
            
        
               
        for meter_name, host, port, timestep, decimal_places, readings in shark_200_meter_settings.settings:
        
            while True:
                if checkConnection(host) == True:
                    print('connection to ' + meter_name + ' good')
                    break
                else:
                    logging.error('Could not connect to {} at '{}'.'.format(meter_name, host) + 'Retrying...')
                    time.sleep(3)
        
        
            
                # Timestamp
            #---------------------------------------------------------------------------------   
            timestamp = time.time()  # Making the timestamp
            #---------------------------------------------------------------------------------   
            
                # Insert timestamp column
            #---------------------------------------------------------------------------------
            if readings[0] != 'timestamp':
                readings.insert(0, 'timestamp') # Makes sure the data has a column for the Unix time stamp
            #---------------------------------------------------------------------------------
            
                # Filtering out any unwanted commas from the list of desired columns
            #---------------------------------------------------------------------------------
            readings = [name.replace(',', '') for name in readings]
            #---------------------------------------------------------------------------------    
                
                # Creating the .csv file to be written to
            #---------------------------------------------------------------------------------
            now = datetime.datetime.now()
            
            file_name = (str(meter_name) + '_{}'*4 + '.csv').format(now.year, now.month, now.day, now.hour)
            file_path = './data/' + file_name
            #---------------------------------------------------------------------------------
               
               
               
                #Primary readings block -- Pages MM-2 to MM-3 of the shark200 user's manual
            #---------------------------------------------------------------------------------
            primary_readings_columns = shark_200_readings_blocks.primary_readings_block
            primary_readings_columns = [name.replace(',', '') for name in primary_readings_columns]
            
            primary_readings_modbus_data = getModbusData(host, port, start_register=1000, end_register=1059)
            
            if primary_readings_modbus_data == None:
                logging.error('Modbus query returned no data')
                continue
            else:
                try:
                    primary_readings_data = format32BitFloat(primary_readings_modbus_data)
                except:
                    logging.error('format32BitFLoat() failed to format data'
                                   + '\n' + 'Data Type: {}'.format(type(primary_readings_modbus_data)), exc_info=True)
                              
            
            temp_dict = {}     # Dictionary that will take in the new data on each loop and be cleared on each iteration.
            
            for index, name in enumerate(primary_readings_columns):     # Here we loop through all the possible columns in this block and add them to the dictionary
                if name == 'timestamp':
                    temp_dict[name] = [timestamp]
                else:
                    temp_dict[name] = [round(primary_readings_data[index - 1], decimal_places)]     # Here we need to reduce the index by 1
                                                                                                    #...to account for the added timestamp column
                                                                
            
            temp_df = pd.DataFrame(temp_dict)     # Make a pandas.DataFrame from the dictionary                 
            temp_df = temp_df[readings]           # Filters out all columns that weren't specified in the 'readings' variable
            
            if 'data' not in os.listdir('.'):
                os.mkdir('data')
                if 'data' in os.listdir('.'):
                    logging.info('Data directory successfully created')
                else:
                    logging.error('Error when creating data directory')
                    continue
                
            
            if file_name not in os.listdir('./data'):                                                # '.' indicates 'current directory'
                with open(file_path, 'a') as data_file:                                              # 'a' indicates 'append' to the file
                    temp_df[temp_df['timestamp'] == 0].to_csv(data_file, header=True, index=False)     # This is a quick and dirty way to write the column headers to the .csv          
                if file_name in os.listdir('./data'):
                    logging.info('New CSV file: ' + file_name + ' successfully created')                                                                                                               
                                    
            else:
                with open(file_path, 'a') as data_file:                      # 'a' indicates 'append' to the file
                    temp_df.to_csv(data_file, header=False, index=False)     # This will account for every other loop iteration and append the data to the .csv file
                
                    
            
            
            # End Timer
        ##########################################        
        stop = timeit.default_timer()
        ##########################################
        
        
            # Controlling the length of the time.sleep() call
        #---------------------------------------------------------------------------------
        run_time = stop - start
        if (timestep - run_time) >= 0:
            time.sleep(timestep - run_time)
        #---------------------------------------------------------------------------------
            
            
                                                            
            
        
            
            
                
            # End Timer
        ##########################################    
        print('success!')
        
        print('Time: ', stop - start)
        print('')
        
        
        
        
    ###################################################################################
    ###################################################################################
    
        
if __name__ == '__main__':
    main()




    
    