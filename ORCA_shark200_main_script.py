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


def checkConnection(host): # A simple function to check if the Modbus connection is open
                           #...using the pyModbus.ModbusClient.is_open() method.
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


# Setup logging directory and 'root' logger for script-wide errors
#--------------------------------------------------------------------------------------
if 'logs' not in os.listdir('.'):
    os.mkdir('logs')
    
    logging.basicConfig(filename='logs/primary_log.log', format='%(asctime)s-%(levelname)s: %(message)s', level=logging.INFO)
#--------------------------------------------------------------------------------------
    

def main():  # Primary function that contains the data collection loop

    logging.basicConfig(filename='logs/primary_log.log', format='%(asctime)s-%(levelname)s: %(message)s', level=logging.INFO)

        # Importing the specified timestep
    #---------------------------------------------------------------------------------
    timestep = shark_200_meter_settings.TIMESTEP
    #---------------------------------------------------------------------------------
       
       
       # Importing the settings from the settings file
    #---------------------------------------------------------------------------------
    settings = shark_200_meter_settings.settings
    
    for meter in settings:
        
        if len([char for char in meter[1] if ((char >= '0') & (char <= '9')) | (char == '.')]) != len(meter[1]):
            logging.error('Invalid host name for ' + meter[0] + ': ' + meter[1])
            exit()
    #---------------------------------------------------------------------------------
    
    
        # Importing the meter names for logging purposes
    #---------------------------------------------------------------------------------   
    meter_names_list = [array[0].strip() for array in settings]
    #---------------------------------------------------------------------------------
           
           
        # Logging
    #---------------------------------------------------------------------------------    
    logger_list = [logging.getLogger(name) for name in meter_names_list]
    
    for logger in logger_list:
        handler = logging.FileHandler('./logs/' + logger.name + '.log')
        handler.setLevel(logging.INFO)
        handler_formatter = logging.Formatter('%(asctime)s-%(levelname)s: %(message)s')
        handler.setFormatter(handler_formatter)
        logger.addHandler(handler)
        
        # See https://docs.python.org/3/library/logging.html for more info in valid LogRecord attributes
        #...to pass as the format argument
        
        # By default, the basic logger only reports logs of level 'WARNING' and above, so here,
        #...since we want information on routine events like the creation of a new .csv file,
        #...we set lvel to logging.INFO.
    #--------------------------------------------------------------------------------- 
     
        # Creating the directory to store .csv files
    #---------------------------------------------------------------------------------
    if 'data' not in os.listdir('.'):
        try:
            os.mkdir('data')
        except:
            logging.error('Could not create data directory', exc_info=True)
    #---------------------------------------------------------------------------------
    ###################################################################################
    ###################################################################################
    while True:     # Data collection loop
        
            # Start Timer
        ##############################
        start = timeit.default_timer()
        ##############################
        
            # Beginning of the message printed after each loop
        #--------------------------------------------------------------------------------- 
        print('')
        print(datetime.datetime.now())
        print('---------------------------------------------------')
        #--------------------------------------------------------------------------------- 
               
        for meter_name, host, port, decimal_places, readings in settings:
            logger = [logger for logger in logger_list if logger.name == meter_name][0]
        
            while True:
                if checkConnection(host) == True:
                    print('connection to ' + meter_name + ' good')
                    break
                else:
                    print('Could not connect to {} at {}'.format(meter_name, host) + ' Retrying...')
                    logger.error('Could not connect to {} at {}'.format(meter_name, host) + ' Retrying...')
                    time.sleep(10)
        
        
            
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
                logger.error('Modbus query returned no data')
                continue
            else:
                try:
                    primary_readings_data = format32BitFloat(primary_readings_modbus_data)
                except:
                    logger.error('format32BitFLoat() failed to format data'
                                   + '\n' + 'Received Data Type: {}'.format(type(primary_readings_modbus_data)), exc_info=True)
                              
            
            temp_dict = {}     # Dictionary that will take in the new data on each loop and be cleared on each iteration.
            
            for index, name in enumerate(primary_readings_columns):     # Here we loop through all the possible columns in this block and add them to the dictionary
                if name == 'timestamp':
                    temp_dict[name] = [timestamp]
                else:
                    temp_dict[name] = [round(primary_readings_data[index - 1], decimal_places)]     # Here we need to reduce the index by 1
                                                                                                    #...to account for the added timestamp column
                                                                
            
            temp_df = pd.DataFrame(temp_dict)     # Make a pandas.DataFrame from the dictionary                 
            temp_df = temp_df[readings]           # Filters out all columns that weren't specified in the 'readings' variable
            
                
            
            if file_name not in os.listdir('./data'):                                                # '.' indicates 'current directory'
                with open(file_path, 'a') as data_file:                                              # 'a' indicates 'append' to the file
                    temp_df[temp_df['timestamp'] == 0].to_csv(data_file, header=True, index=False)     # This is a quick and dirty way to write the column headers to the .csv          
                if file_name in os.listdir('./data'):
                    logger.info('New CSV file: ' + file_name + ' successfully created')                                                                                                               
                                    
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
            
            
                                                            
            
        
            
            
                
            # Text to be printed
        ##########################################    
        print('\n' + 'Data successfully logged' + '\n')
        print('Loop Runtime: ', stop - start)
        print('---------------------------------------------------')
        print('')
        
        
        
        
    ###################################################################################
    ###################################################################################
    
        
if __name__ == '__main__':
    main()


