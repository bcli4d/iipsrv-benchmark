from __future__ import print_function
import subprocess
import sys,os
import json
import argparse
import time
from operator import attrgetter

QUIP_DISTRO='/home/bcliffor/projects/quip_distro'
QUIP_BENCHMARK='/home/bcliffor/projects/quip_benchmark'

def loadConfigTable(args):
    if os.path.exists(args.configTable):
        with open(args.configTable) as f:
            return json.load(f)
    else:
        print("Failed to open {}".format(args.configTable))
        exit
        
def flushConfigTable(args,configs):
    if os.path.exists(args.configTable):
        with open(args.configTable,'w') as f:
            json.dump(configs,f)
    else:
        print("Failed to open {}".format(args.table))
        exit

def all_configs(args):
    #Load all the defined configurations
    configs = loadConfigTable(args)
    #Get which row in configs to use to configure the system
#    row = getRow(args)

    for row in range(len(configs)):
        if args.verbosity>=3:
            for i,r in zip(range(len(configs)),configs):
                print(i,r)
        sum = times = 0
        for time in configs[row]["avgTime"]:
            if time <> max(configs[row]["avgTime"]) :
                if time  <> min(configs[row]["avgTime"]) :
                    sum += time
                    times +=1
        configs[row]['avgAvgTime'] = sum/times

    flushConfigTable(args,configs)

    sorted_configs= (sorted( configs, key=lambda config:config['avgAvgTime']))
    if args.verbosity >=1 :
        print("max_image_cache\tmax_tile_cache\tthreads\t\ttile_size\tavgAvgTime\tAvgTime".format())
        for i,r in zip(range(len(configs)),sorted_configs):
            print("{}\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}".format(
                sorted_configs[i]['max_image_cache'],
                sorted_configs[i]['max_tile_cache'],
                sorted_configs[i]['threads'],
                sorted_configs[i]['tile_size'],
                sorted_configs[i]['avgAvgTime'],
                sorted_configs[i]['avgTime']))
    else:
        print("max_image_cache\tmax_tile_cache\tthreads\t\ttile_size\tavgAvgTime".format())
        for i,r in zip(range(len(configs)),sorted_configs):
            print("{}\t\t{}\t\t{}\t\t{}\t\t{}".format(
                sorted_configs[i]['max_image_cache'],
                sorted_configs[i]['max_tile_cache'],
                sorted_configs[i]['threads'],
                sorted_configs[i]['tile_size'],
                sorted_configs[i]['avgAvgTime']))
        
def parseargs():
    parser = argparse.ArgumentParser(description="Build svs image metadata table")
    parser.add_argument ( "-v", "--verbosity", action="count",default=0,help="increase output verbosity" )
    parser.add_argument ( "-c", "--configTable", type=str, help="Configuration table", default=QUIP_BENCHMARK+'/configs.json')
    return(parser.parse_args())

if __name__ == '__main__':
    args=parseargs()
    all_configs(args)
