import pandas as pd
import numpy as np
import pyModbusTCP
from pyModbusTCP.client import ModbusClient
import struct
import logging
import timeit
import time
import datetime



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
    # Since the registers are taken as integers, we take the range between the start and end
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
    #...by 2^16 and add it to the first integer. We can then use the struct python library
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
        
        

garbo = datetime.datetime(2019,11, 18, 23, 2)
cc = garbo.timetuple()

print(cc[2])
    
    







start = timeit.default_timer()

abba = getModbusData('75.127.189.115', 503, 1000, 1035)
yumo = format32BitFloat(abba)

stop = timeit.default_timer()

print('Time: ', stop - start)
print(yumo[0])

logb = 1123
    