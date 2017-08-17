################################################################################################################################################################
#  spectrum_test.py
#  Joseph Estrada
#  EPRI Engineer/Scientist I
#  20170814
#  
#  This python script will implement the spectrum testing for the HackRF One SDR.  The purpose is to understand the noise floor of the following frequencies:
#    902 MHz to 928 MHz
#    2400 MHz to 2500 MHz
#    3655 MHz to 3700 MHz
#    5170 MHz to 5838 MHz
#
#  This will enable utilities to identify frequencies that would be optimal for use in the unlicensed bands.
#
#  The script will funciton in a number of ways.  In general, the script will record a log od all commands executed on the SDR.  It will order
#  the SDR to conduct a frequency sweep in order to obtain signal strength values in the frequency range selected.  Then it will send
#  the data to a remote storage device.
#
#  ---------WHETHER OR NOT PROCESING IS DONE LOCALLY OR NOT HAS YET TO BE DETERMINED------------------------
#
#  The first part of this will be to construct the log file.  While constructing this log file, commands will be executed on the SDR
#  as they are recorded.  The log file creation mechanism will flow as such: 
#    open and name a unique logfile
#    record the position of the SRD onto the log
#    write the hackrf commands that are executed to file
#    write hackrf_sweep filename that will store signal data to the log file
#    write start time of the frequency sweep to file
#    run a particular hackrf_sweep (eg. sweep the 900 Mhz band for 5 minutes)
#    stop hackrf
#    log stop time
#    repeat for next frequency block or blocks on a new file
#
###############################################################################################################################################################

import time
import os
from multiprocessing import Process
import threading
import signal
import subprocess


if __name__ == '__main__':

  #set the frequency ranges that will be executed upon
  frequencies = [902, 928, 2400, 2500, 3566, 3700, 5170, 5838]
  #determine the current location
  #determine the hackrf commands' arguments
  commands = ["hackrf_sweep -f ", "hackrf_sweep -f ", "hackrf_sweep -f ", "hackrf_sweep -f "]
  
  i = 0
  j = 0
  while i < 8:
    #determine a filename for the file that will store the data
    freqFileName = str(frequencies[i]) + "_to_" + str(frequencies[i+1])
    dataFileName = freqFileName + "_data.txt"
  
    #change the commands to match what we need
    commands[j] = commands[j] + str(frequencies[i]) + ":" + str(frequencies[i+1]) + " -w 200000 -r " + dataFileName + " &"

    #create the log file that will be used using the data filename
    logfile = open(freqFileName + "_log.txt", "w+")
    #insert the location information into the log file
    logfile.write("Location: \n")
    #insert the commands that will be used into the log file
    logfile.write("The following command was executed:\n" + "     " + commands[j] + "\n")
    
    #calculate the start time
    start = time.strftime("%c")
    #execute the appropriate hackrf methods
    proc = subprocess.Popen(commands[j], shell = True, preexec_fn=os.setsid)
    if i == 6:
      time.sleep(900)
    else:
      time.sleep(300)
    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
    #calculate the stop time
    stop = time.strftime("%c")
    #insert the filename of the data file into the log file
    logfile.write("Data is contained in the follwoing file: " + dataFileName + "\n")
    #insert the start time into the log file
    logfile.write("Start Time: " + start + "\n")
    #insert the stop time into th elog file
    logfile.write("Stop Time: " + stop + "\n")
    #close the log file
    logfile.close()

    i = i + 2
    j = j + 1
