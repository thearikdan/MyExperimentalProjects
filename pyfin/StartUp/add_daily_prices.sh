#!/bin/bash
echo "bee561333" | sudo -S service postgresql start
cd /media/hdd/MyProjects/pyfin/apps/database && gnome-terminal -- bash -ic "source /media/hdd/virtualenvs/pyfin3/bin/activate; python add_last_N_daily_prices.py -n 2; exec bash"

