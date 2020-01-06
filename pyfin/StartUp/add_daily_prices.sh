#!/bin/bash
echo "bee561333" | sudo -S service postgresql start
cd /media/ara/HDD/MyProjects/pyfin/apps/database && gnome-terminal -e 'bash -ic "source /media/ara/HDD/virtualenvs/pyfin3/bin/activate; python add_last_N_daily_prices.py -n 4; exec bash"'

