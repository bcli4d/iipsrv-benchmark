from __future__ import print_function
import subprocess
import sys,os
import json
import argparse
import time
from operator import attrgetter

QUIP_DISTRO='/home/bcliffor/projects/quip_distro'
QUIP_BENCHMARK='/home/bcliffor/projects/quip_benchmark'

def getRow(args):
    if os.path.exists(args.testRow):
        with open(args.testRow) as f:
            return int(f.read())
    else:
        print("Failed to open {}".format(args.table))
        exit

def setRow(args,row):
    if os.path.exists(args.testRow):
        with open(args.testRow,'w') as f:
            f.write(str(row))
    else:
        print("Failed to open {}".format(args.table))
        exit
    
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

#Modify a line in args.iipsrvConf (defaults to apache-iipsrv-fcgid.conf)
def mod_apache_iipsrv(args, phrase, value):
    saved_input=[]
    input = file(args.iipsrvConf,'r')
    if args.verbosity>=4:
        print("Find {}".format(phrase))
    for line in input:
        if line.find(phrase)>=0:
            if args.verbosity>=4:
                print("Found in {}".format(line))
            saved_input.append(phrase+'"'+str(value)+'"\n')
        else:
            if args.verbosity>=4:
                print("Not in {}".format(line))
            saved_input.append(line)
    input.close()

    if args.verbosity>=4:
            print("Now {}".format(saved_input))

    output = file(args.iipsrvConf,'w')
    for line in saved_input:
        output.write(line)
    output.close()
    
def configureThisSet(args,config):
    mod_apache_iipsrv(args, 'FcgidInitialEnv MAX_IMAGE_CACHE_SIZE ', config["max_image_cache"])
    mod_apache_iipsrv(args, 'FcgidInitialEnv MAX_TILE_CACHE_SIZE ', config["max_tile_cache"])
    mod_apache_iipsrv(args, 'FcgidInitialEnv JPEG_QUALITY ', config["jpeg_qual"])
    mod_apache_iipsrv(args, 'FcgidMaxProcessesPerClass ', config["threads"])

#Remove all containers (assume the only containers are for quip
def stopQuip():
    containers = subprocess.check_output(['docker','ps','-aq']).split('\n')[0:-1]
    for container in containers:
        subprocess.check_output(['docker','rm', '-f', container])
#     subprocess.check_output(['docker','rm', '-f', 'quip-viewer'])

def startQuip():
#    subprocess.check_output([QUIP_DISTRO+'/vrun_containers.sh', QUIP_DISTRO+'/data', QUIP_DISTRO])
    subprocess.check_output([QUIP_DISTRO+'/vrun_viewer.sh', QUIP_DISTRO+'/data', QUIP_DISTRO])

def remount_gcsfuse(args):
    script=QUIP_BENCHMARK+'/remount_gcsfuse.sh'
    subprocess.check_output([script,args.bucket])
    
#Measure performance for one parameter configuration
def one_config(args, row, config):
    #Stop quip. By stopping and restarting we flush any quip maintained caches.
    stopQuip()

    #Implement the configuration for this test
    configureThisSet(args,config)

    #Need to ensure that gcsfuse caches are flushed. This doesn't work if done while quip is running
    remount_gcsfuse(args)

    #Now start quip again
    startQuip()

    if args.verbosity >=1:
        print("Config {}: {}".format(row,config))

    #Run the benchmark on this config and capture result
    t0 = time.time()
    subprocess.check_output([args.test,args.iipReqs,args.ip])
    t1 = time.time()
    tiles = int(subprocess.check_output(['wc','-l',args.iipReqs]).partition(' ')[0])
    totalTime = t1-t0
    if args.verbosity >=1:
        print("Avg time for {} tiles: {} seconds".format(tiles,totalTime/tiles))
    #Record average per-tile time in config table
    config['avgTime'].append(totalTime/tiles)
    config['tiles'].append(tiles)
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
        one_config(args, row, configs[row])

    flushConfigTable(args,configs)

    print("Testing complete".format())
    sorted_configs= (sorted( configs, key=lambda config:config['avgTime']))
    print("max_image_size\tmax_tile_size\tthreads\t\ttile_size\tavgTime".format())
    for i,r in zip(range(len(configs)),sorted_configs):
        print("{}\t\t{}\t\t{}\t\t{}\t\t{}".format(
            sorted_configs[i]['max_image_cache'],
            sorted_configs[i]['max_tile_cache'],
            sorted_configs[i]['threads'],
            sorted_configs[i]['tile_size'],
            sorted_configs[i]['avgTime']))
        
def parseargs():
    parser = argparse.ArgumentParser(description="Build svs image metadata table")
    parser.add_argument ( "-v", "--verbosity", action="count",default=0,help="increase output verbosity" )
    parser.add_argument ( "-t", "--test", type=str, help="Benchmark script", default=QUIP_BENCHMARK+'/run.sh')
    parser.add_argument ( "-i", "--iipReqs", type=str, help="iipsrv requests file", default=QUIP_BENCHMARK+'/iipReqs.parsed')
    parser.add_argument ( "-r", "--testRow", type=str, help="Config table row to test", default=QUIP_BENCHMARK+'/test_row.txt')
    parser.add_argument ( "-c", "--configTable", type=str, help="Configuration table", default=QUIP_BENCHMARK+'/configs.json')
    parser.add_argument ( "-s", "--iipsrvConf", type=str, help="iipsrv config file", default=QUIP_DISTRO+'/ViewerDockerContainer/apache2-iipsrv-fcgid.conf')
    parser.add_argument ( "-p", "--ip", type=str, help="IP address of the apache2 server", default='104.199.116.255')
    parser.add_argument ( "-b", "--bucket", type=str, help="GCS bucket on which to mount gcsfuse", default='svs_images')
    return(parser.parse_args())

if __name__ == '__main__':
    args=parseargs()
    all_configs(args)
