import sys
sys.path.append("../..")

from utils.db import db
from datetime import datetime, timedelta
from utils import time_op

conn, cur = db.connect_to_database("../../database/database_settings.txt")

date_time_list = time_op.get_last_N_days_list_from_now(3)
print (date_time_list)


ids = db.get_company_ids_from_market_and_symbol("nasdaq", "AMZN")
company_id = ids[0]
print (company_id)

for date_time in date_time_list:
    start_date_time = date_time
    end_date_time = start_date_time + timedelta(days=1)
    is_data_available, dtn, vn, on, cn, hn, ln = db.get_raw_intraday_data_from_company_id(company_id, start_date_time,
                                                                                      end_date_time)
    if is_data_available:
        print(on)

print("---------------------------------")

ids = db.get_etf_ids_from_symbol("TQQQ")
etf_id = ids[0]
print (etf_id)

for date_time in date_time_list:
    start_date_time = date_time
    end_date_time = start_date_time + timedelta(days=1)
    is_data_available, dtn, vn, on, cn, hn, ln = db.get_raw_intraday_data_from_etf_id(etf_id, start_date_time,
                                                                                      end_date_time)
    if is_data_available:
        print(on)


cur.close()
conn.close()


