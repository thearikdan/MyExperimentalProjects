#!/bin/bash
sudo service postgresql start
cd /media/ara/HDD/MyProjects/pyfin/apps/file_source && gnome-terminal -e 'bash -ic "source /media/ara/HDD/virtualenvs/pyfin3/bin/activate; python download_intraday_dataset.py -d /media/ara/Passport1_2TB1/datasets/pyfin/data -n 2 -st file_system; exec bash"'

