#!/bin/bash
sudo service postgresql start
cd /media/ara/HDD/MyProjects/pyfin/apps/file_source && gnome-terminal -e 'bash -ic "source /media/ara/HDD/virtualenvs/pyfin/bin/activate; python download_intraday_dataset.py -d /media/ara/Passport2_4TB1/datasets/pyfin/data -n 3 -st file_system; exec bash"'
