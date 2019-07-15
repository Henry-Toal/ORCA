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


    
"""
--------------------------------------------------------------------------------------
Electro Industries/GaugeTech™ Shark® 200 Data Logging Script version 0.6.7.15

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
# - Integrate the parameters dictionary into the rest of the program
# -- A for loop for each meter, etc.


# - At some point, change the readings section instructions to include more than the 1000-to-1053 range
# -- When that's done, change the output (to_csv) dataframe to be a seperate main dataframe that the
#....block-specific dataframes are appended to.
#--------------------------------------------------------------------------------------    
    
    
    # INPUTS:
    
    # Enter Device IP Address (host) as (str) and port number as (int).
    # Choose your timestep (in seconds) and number of decimal places for the output data.
#--------------------------------------------------------------------------------------

host = '75.127.189.115' #(str) # IP address of the power meter 
port = 503 #(int)              # port the device is using for modbus protocol. Usually 502 or 503. 

timestep = 1 #(int)            # The interval, in seconds, between data measurements. Below 5 seconds not recommended. 
decimal_places = 3 #(int)      # The number of decimal places the final .csv file will be rounded to. 
#--------------------------------------------------------------------------------------


    # Enter parameters for each power meter.
    
    #             (str)    (str) (int)   (int)            (int)
    # FORMAT: 'METER NAME':[HOST, PORT, TIMESTEP, NUMBER OF DECIMAL PLACES]
#--------------------------------------------------------------------------------------
parameters = ({
    
    #             (str)    (str) (int)   (int)                     (int)
    # FORMAT: 'METER NAME':[HOST, PORT, TIMESTEP(seconds), NUMBER OF DECIMAL PLACES]
    # Example:
            #  'Shark_1':['75.127.189.115', 503, 15, 3]
               'test_meter':['75.127.189.115', 503, 5, 3], 
               '':[],
               '':[],
               '':[],
               '':[],
               '':[],
               '':[],
               '':[],
               '':[],
               '':[]
           }) 
#--------------------------------------------------------------------------------------

    # Choose which values you want exported  
#--------------------------------------------------------------------------------------
readings =    ([                       # From here you can edit which values from the
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
                ])
#--------------------------------------------------------------------------------------


    # Column names for the variables listed in the Shark 200 user's manual.
    
    # !!! DO NOT CHANGE !!!
#--------------------------------------------------------------------------------------
primary_readings_columns = (['timestamp',
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
                                 'Symmetrical Component Magnitude - Seq'])

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


def checkConnection():
    pass

#######################################################################################
#######################################################################################


def main():  # Primary function that contains the data collection loop
    
    
    
    
        # Importing global variables
    #---------------------------------------------------------------------------------
    global host     # Import the host and port varibale into the main() function.
    global port
    global readings # The list of desired values to be measured
    global decimal_places
    global primary_readings_columns
    #---------------------------------------------------------------------------------
    
        # Removing commas from the column names list(s) and readings list
    #---------------------------------------------------------------------------------
    readings = [name.replace(',', '') for name in readings]
    
    primary_readings_columns = [name.replace(',', '') for name in primary_readings_columns]
    #---------------------------------------------------------------------------------
    
        # Insert timestamp column
    #---------------------------------------------------------------------------------
    readings.insert(0, 'timestamp') # Makes sure the data has a column for the Unix time stamp
    #---------------------------------------------------------------------------------
        
    while True:     # Data collection loop
        
        start = timeit.default_timer()
            
            
            # Timestamp
        #---------------------------------------------------------------------------------   
        timestamp = time.time()  # Making the timestamp
        #---------------------------------------------------------------------------------   
            
            
            # Creating the .csv file to be written to
        #---------------------------------------------------------------------------------
        now = datetime.datetime.now()
        
        file_name = ('shark200' + '_{}'*3 + '.csv').format(now.year, now.month, now.day)  
        #---------------------------------------------------------------------------------
           
            
            #Primary readings block -- Pages MM-2 to MM-3 of the shark200 user's manual
        #---------------------------------------------------------------------------------
        primary_readings_modbus_data = getModbusData(host, port, start_register=1000, end_register=1059)
        primary_readings_data = format32BitFloat(primary_readings_modbus_data)
        
        temp_dict = {}
        temp_list = []
        
        for index, name in enumerate(primary_readings_columns):
            if name == 'timestamp':
                temp_dict[name] = [timestamp]
            else:
                temp_dict[name] = [round(primary_readings_data[index - 1], decimal_places)]
                                                            # Here we need to reduce the index by 1
        temp_df = pd.DataFrame(temp_dict)                   #...to account for the added timestamp column
        temp_df = temp_df[readings]
        
        
                
        
        if file_name not in os.listdir('.'):        # '.' indicates 'current directory'
            with open(file_name, 'a') as data_file:
                temp_df[temp_df['timestamp'] == 0].to_csv(data_file, header=True)
                                # This is a quick and dirty way to write the column headers in without
                                #...any of the other data
        else:
            with open(file_name, 'a') as data_file:
                temp_df.to_csv(data_file, header=False)
            
                
            

                                                        
        
        
        
            
        stop = timeit.default_timer()
        print('Time: ', stop - start)
        print('')
        print('success!')
        print('Length of readings: {}'.format(len(readings)))
        time.sleep(timestep)
        
        #---------------------------------------------------------------------------------
        
    
    

        
        
   






    
    






    
    
