#!/bin/bash
sudo service postgresql start
cd /media/ara/HDD/MyProjects/pyfin/apps/file_source && gnome-terminal -e 'bash -ic "source /media/ara/HDD/virtualenvs/pyfin/bin/activate; python download_intraday_dataset.py -d /media/ara/Passport1_2TB/datasets/pyfin/data -n 3 -st file_system; exec bash"'

