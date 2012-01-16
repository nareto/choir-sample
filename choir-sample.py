#!/usr/bin/env python2

#TODO: ecasound:
#ecasound -a:1  -i playat,0.5,a.wav -ea:100 -a:2 -i playat,1.5,a.wav -ea:80 -a:all  -f:16,1,44100 -o o.wav

#this script uses sox to try and achieve the effect of many people hitting
#a drum. It takes a sample, and performs the folowing operations multiple times:
#-adds a randomized quantity of silence at the beginning
#-makes a randomized gain attenuation
#finally it mixes all down to the outfile and normalizes to -1db.

import sys
import os
from random import uniform 

def usage():
    print "USAGE: choir-sample.py infile.wav outfile.wav number_of_copies"

def ran_vector(length, max):
    """Returns list with uniform values between 0 and max """
    
    ret = []
    for j in range(length):
        ret.append(uniform(0,max))
    return ret

def apply(args):
    n = int(args[3])
    print args
    
    #let's get some random values for gains and silence padding
    gains = ran_vector(n, 6)
    pads = ran_vector(n, 0.05)

    tmpdir = "tmp"
    os.system("mkdir {0}".format(tmpdir)) #create working directory
    files = ""
    for i in range(n):
        #here we define the actual sox command. For each iteration of the for loop, new copies
        #of the original file are made with a different gain and some silence at the beginning.
        cmd = "sox {0} {1}/{2}.wav pad {3} gain {4}".format(args[1],tmpdir,i, pads[i], -gains[i]) 
        print cmd
        os.system(cmd)
        files = files + " {0}/{1}.wav".format(tmpdir, i)
    
    #now mix the files to obtain a single .wav file
    cmd = "sox -m {0} {1} norm -1".format(files, args[2])
    os.system(cmd)

    os.system("rm -rf {0}".format(tmpdir)) #remove working directory

if __name__ == "__main__":
    if len(sys.argv) != 4:
        usage()
    else:
        apply(sys.argv)


