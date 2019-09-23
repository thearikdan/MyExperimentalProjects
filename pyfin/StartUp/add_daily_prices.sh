#!/bin/bash
sudo service postgresql start
cd /media/ara/HDD/MyProjects/pyfin/apps/database && gnome-terminal -e 'bash -ic "source /media/ara/HDD/virtualenvs/pyfin/bin/activate; python add_last_N_daily_prices.py -n 4; exec bash"'

