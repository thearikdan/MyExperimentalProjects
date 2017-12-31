from utils import file_op
from os.path import join
import pickle

def put_intraday_data_to_file(dir_name, file_name, date_time, volume, opn, close, high, low):
    file_op.ensure_dir_exists(dir_name)
    full_path = join(dir_name, file_name)
    with open(full_path, "wb") as f:
        pickle.dump((date_time, volume, opn, close, high, low), f)



