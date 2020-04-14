#!/bin/bash
echo "bee561333" | sudo -S service postgresql start
cd /media/ara/HDD/MyProjects/pyfin/apps/file_source && gnome-terminal -e 'bash -ic "source /media/ara/HDD/virtualenvs/pyfin3/bin/activate; python download_etf_intraday_dataset.py -d /media/hddx/datasets/pyfin/data -n 2 -st database; exec bash"'

