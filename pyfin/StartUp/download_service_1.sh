#!/bin/bash
echo "bee561333" | sudo -S service postgresql start
cd /media/ssd/MyProjects/pyfin/apps/file_source && gnome-terminal -- bash -ic "source /media/ssd/virtualenvs/pyfin3/bin/activate; python download_intraday_dataset.py -d /media/ssd/datasets/pyfin/data -n 2 -st database; exec bash"

