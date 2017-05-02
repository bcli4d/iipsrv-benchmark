#! /bin/bash
set -x

MOUNT_AT=/home/bcliffor/projects/quip_distro/data/img/isb-cgc-open
if grep -q $MOUNT_AT /etc/mtab; then
   fusermount -u $MOUNT_AT
fi
gcsfuse -o allow_other --stat-cache-ttl 0 --type-cache-ttl 0 $1  $MOUNT_AT &> /dev/null
exit 0
