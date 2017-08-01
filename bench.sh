#! /bin/bash
set -x

CONFIGS=results/'configs.300.unique.2.ssd.resetviewer.noresetfuse.json'
python genConfs.py --disk='ssd' --cores=2 --configTable=$CONFIGS
for run in {1..1};
do
    python measure.py --iipReqs=iipReqs.unique --configTable=$CONFIGS -g  -vvv 
done
#mv $CONFIGS results

CONFIGS=results/'configs.300.dup.2.ssd.resetviewer.noresetfuse.json'
python genConfs.py --disk='ssd' --cores=2 --configTable=$CONFIGS
for run in {1..1};
do
    python measure.py --iipReqs=iipReqs.dup --configTable=$CONFIGS -g  -vvv 
done
#mv $CONFIGS results

CONFIGS=results/'configs.300.unique.2.ssd.noresetviewer.resetfuse.json'
python genConfs.py --disk='ssd' --cores=2 --configTable=$CONFIGS
for run in {1..1};
do
    python measure.py --iipReqs=iipReqs.unique --configTable=$CONFIGS -d  -vvv 
done
#mv $CONFIGS results

CONFIGS=results/'configs.300.dup.2.ssd.noresetviewer.resetfuse.json'
python genConfs.py --disk='ssd' --cores=2 --configTable=$CONFIGS
for run in {1..1};
do
    python measure.py --iipReqs=iipReqs.dup --configTable=$CONFIGS -d  -vvv 
done
#mv $CONFIGS results

