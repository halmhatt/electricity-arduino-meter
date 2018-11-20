FROM resin/raspberry-pi-python:3.6-onbuild

# Install NFS driver
RUN apt-get update && apt-get install -y nfs-common
# && rm -rf /var/lib/apt/lists/*

ENV ELECTRICITY_MOUNTPOINT /media/electricity

RUN echo "192.168.1.83:/mnt/NAS_JACOB/electricity /media/electricity nfs nolock" >> /etc/fstab && mkdir /media/electricity

CMD ["/bin/bash", "-v", "start.sh"]