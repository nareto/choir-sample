#!/usr/bin/env python2

import sys
import os
from random import gauss

def usage():
    print "USAGE: choir-sample.py number_of_copies outfile infile1 [infile2 [infile3 ...[infileN]...]]"

def ran_vector(length, sigma):
    """Returns list with gaussian distributed values with mean 0 """
    
    ret = []
    for j in range(length):
        ret.append(gauss(0,sigma))
    return ret

def stereo(file):
    """Do mono to stereo conversion if necessary - allways returns stereo file"""

    pass #for the moment we suppose all files are stereo

def apply(n,outfile,infiles):
    N = len(infiles)
    #let's get some random values for gains and silence padding
    gains = ran_vector(n*N, 8)
    pads = ran_vector(n*N, 0.04)

    #lets build the ecasound command
    cmd = "ecasound "

    #explanation of the following for line: we need an n*N matrix of indexes and a way
    #to increasingly number its elements. To convince yourself of what is going on uncomment
    #the print line and eventually the sys.exit() at the end of the for.
    for i,j,counter in [(i,j,i*(N+3) + j) for i in range(N) for j in range(n)]: 
        #for every one of the N files in infile we add n chains;
        #on each of those chains we shift in time and apply gain reduction
        cmd += "-a:{0} -f:16,i,44100 -i playat,{1},{2} -eadb:{3} ".format(counter, abs(pads[counter]), infiles[i],- abs(gains[counter]))
        #print counter, " : ", i,j
    #sys.exit()

    #now mixdown all the chains to the output file
    cmd += "-a:all -z:mixmode,avg -f:16,1,44100 -o {0}".format(outfile)  
    print "We're running this command:","\n", cmd,"\n"
    os.system(cmd)

    #finally normalize the file
    print "\n", "Normalizing file:", "\n"
    os.system("ecanormalize {0}".format(outfile))

    print "\n", "Done"

if __name__ == "__main__":
    if len(sys.argv) < 4:
        usage()
        sys.exit()
    n, outfile = sys.argv[1:3]
    infiles = sys.argv[3:]
    if os.path.exists(outfile):
        print "file {0} exists, exiting".format(outfile)
        sys.exit()
    else:
        apply(int(n),outfile,infiles)


