#!/bin/bash
echo "bee561333" | sudo -S service postgresql start
cd /media/hdd/MyProjects/pyfin/apps/file_source && gnome-terminal -- bash -ic "source /media/hdd/virtualenvs/pyfin3/bin/activate; python download_intraday_dataset.py -d /media/hdd/datasets/pyfin/data -n 2 -st database; exec bash"

