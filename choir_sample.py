#!/usr/bin/env python2


#this script uses ecasound to try and achieve the effect of many people hitting
#a drum. It takes a sample, and performs the folowing operations multiple times:
#-adds a randomized quantity of silence at the beginning
#-makes a randomized gain attenuation
#finally it mixes all down to the outfile and normalizes.

import sys
import os
from random import gauss

def usage():
    print "USAGE: choir-sample.py infile.wav outfile.wav number_of_copies"

def ran_vector(length, sigma):
    """Returns list with gaussian distributed values with mean 0 """
    
    ret = []
    for j in range(length):
        ret.append(gauss(0,sigma))
    return ret

def apply(args):
    n = int(args[3])
    print args
    
    #let's get some random values for gains and silence padding
    gains = ran_vector(n, 8)
    pads = ran_vector(n, 0.03)

    cmd = "ecasound "

    for i in range(n):
        cmd += "-a:{0} -i playat,{1},{2} -eadb:{3} ".format(i, abs(pads[i]), args[1] ,- abs(gains[i]))

    #now mix the files to obtain a single .wav file
#    cmd += "-a:all -f:16,1,44100 -o {0}".format(args[2])  
    cmd += "-a:all -z:mixmode,avg -f:16,1,44100 -o {0}".format(args[2])  
    print cmd
    os.system(cmd)

    #normalize file
    os.system("ecanormalize {0}".format(args[2]))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        usage()
    elif os.path.exists(sys.argv[2]):
        print "file {0} exists, exiting".format(sys.argv[2])
    else:
        apply(sys.argv)


