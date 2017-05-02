#! /bin/bash
set -x

CONFIGS='configs.300.unique.2.ssd.json'
python genConfs.py --disk='ssd' --cores=2 --configTable=$CONFIGS
for run in {1..1};
do
    python measure.py --iipReqs=iipReqs.301-600.unique --configTable=$CONFIGS -vvv 
done
#mv $CONFIGS results

CONFIGS='configs.300.dup.2.ssd.json'
python genConfs.py --disk='ssd' --cores=2 --configTable=$CONFIGS
for run in {1..1};
do
    python measure.py --iipReqs=iipReqs.301-600.dup --configTable=$CONFIGS  -vvv
done
#mv $CONFIGS results
