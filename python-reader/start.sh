#! /bin/bash

# Mount drive
mount -a
#mount -t nfs -o nolock "$NFS_DATA_LOCATION" "$ELECTRICITY_MOUNTPOINT"

# Run script
python read.py