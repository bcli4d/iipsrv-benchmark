#!/bin/bash
set  -x

if [ "$#" -ne 2 ]; then
	echo "./run_containers.sh <install folder> <path to this directory>"
	exit 1;
fi

cd $2

VERSION=latest

VIEWER_DIR=ViewerDockerContainer
if [ ! -d "$VIEWER_DIR" ]; then
	git clone https://github.com/camicroscope/ViewerDockerContainer
	# cd ViewerDockerContainer; git checkout ver-0.9; cd ..;
fi

STORAGE_FOLDER=$1;

docker network create quip_nw &> /dev/null

IMAGES_DIR=$(echo $STORAGE_FOLDER/img)
DATABASE_DIR=$(echo $STORAGE_FOLDER/data)

mkdir -p $IMAGES_DIR 
mkdir -p $DATABASE_DIR

VIEWER_PORT=80
IMAGELOADER_PORT=6002
FINDAPI_PORT=3000

data_host="http://quip-data:9099"
mongo_host="quip-data"
mongo_port=27017

# Run viewer container
INP_HTML_DIRECTORY=$(pwd)"/ViewerDockerContainer/html"
\cp -rf $INP_HTML_DIRECTORY $STORAGE_FOLDER/.
HTML_DIRECTORY="$STORAGE_FOLDER/html"
viewer_container=$(docker run --name=quip-viewer --net=quip_nw -itd \
	-p $VIEWER_PORT:80 \
	-v $HTML_DIRECTORY:/var/www/html \
	-v $IMAGES_DIR:/data/images \
	-v $2/$VIEWER_DIR:/tmp/ViewerDockerContainer \
	quip_viewer:$VERSION)
#	-v /var/log/apache2 \
echo "Started viewer container: " $viewer_container


