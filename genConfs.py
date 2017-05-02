from __future__ import print_function
import json
import sys,os
import argparse

def flushResults(param_table,param_file):
    #Output results of scanning files of caType
    try:
        with open(param_file,'w') as f:
            json.dump(param_table,f)
    except IOError:
        print("Can't open results file {} for write".format(param_file),file=sys.stderr)
        exit()
def genTable(args):
    param_table = []
    for threads in (32,64):
        #    for tile_size in (256,512,1024):
        for cores in (args.cores,):
            for disk in (args.disk,):
                for jpeg_qual in (75,):
                    for tile_size in (256,):
                        for max_image_cache in (128,256,512,1024,2048):
                            for max_tile_cache in (64,128,256,512):
                                param_set={}
                                param_set['cores']=cores
                                param_set['disk']=disk
                                param_set['jpeg_qual']=jpeg_qual
                                param_set['threads']=threads
                                param_set['tile_size']=tile_size
                                param_set['max_image_cache']=max_image_cache
                                param_set['max_tile_cache']=max_tile_cache
                                param_set['avgTime']=[]
                                param_set['tiles']=[]
                                #print(param_set)
                                param_table.append(param_set)
                                flushResults(param_table,args.configTable)
                                
def parseargs():
    parser = argparse.ArgumentParser(description="Build svs image metadata table")
    parser.add_argument ( "-v", "--verbosity", action="count",default=0,help="increase output verbosity" )
    parser.add_argument ( "-t", "--configTable", type=str, help="Configuration table", default='./configs.json')
    parser.add_argument ( "-c", "--cores", type=int, help="Number of cores", default=2)
    parser.add_argument ( "-d", "--disk", type=str, help="Type of disk", default='hdd')
    return(parser.parse_args())

if __name__ == '__main__':
    args=parseargs()
    genTable(args)
                                
