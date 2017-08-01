from __future__ import print_function
import sys,os
import json
import argparse

QUIP_DISTRO='/home/bcliffor/projects/quip_distro'
QUIP_BENCHMARK='/home/bcliffor/projects/quip_benchmark'

def loadReqTable(args):
    with open(args.iipReqs) as f:
        reqs = f.read().splitlines()
    return reqs
                
def flushUniqueReqs(args,reqs):
    with open(args.uniques,'w') as f:
        for req in reqs:
            f.write("%s\n"%req)

def is_unique(uniques,req):
    for unique in uniques:
        if req==unique:
            return False
    return True
        
#Measure performance for one parameter configuration
def find(args):
    #Load all the defined configurations
    reqs = loadReqTable(args)
    uniques = []
    found=0
    for req in reqs:
        if req not in uniques:
            uniques.append(req)
        found+=1
        if found == args.find:
            break
#    uniques.sort()
    flushUniqueReqs(args,uniques)
    exit

def parseargs():
    parser = argparse.ArgumentParser(description="Build svs image metadata table")
    parser.add_argument ( "-v", "--verbosity", action="count",default=0,help="increase output verbosity" )
    parser.add_argument ( "-i", "--iipReqs", type=str, help="iipsrv requests file", default=QUIP_BENCHMARK+'/iipReqs.parsed')
    parser.add_argument ( "-u", "--uniques", type=str, help="File of unique iip reqst", default=QUIP_BENCHMARK+'/iipReqs.unique')
    parser.add_argument ( "-f", "--find", type=int, help="Number of reqs to find", default=300)
    return(parser.parse_args())

if __name__ == '__main__':
    args=parseargs()
    find(args)
