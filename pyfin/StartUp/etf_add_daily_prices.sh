#!/bin/bash
echo "bee561333" | sudo -S service postgresql start
cd /media/ssd/MyProjects/pyfin/apps/database && gnome-terminal -- bash -ic "source /media/ssd/virtualenvs/pyfin3/bin/activate; python add_etf_last_N_daily_prices.py -n 2; exec bash"

