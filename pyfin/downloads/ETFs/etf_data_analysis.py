import sys
sys.path.append("../..")

from utils import file_op
import pandas as pd
from os.path import join

ROOT_DIR = "etf_data"

def get_etfs_from_file(f):
    df = pd.read_csv(f)
    return df

def get_full_dataframe_for_directory(dir):
    files = file_op.get_only_files(dir)
    frames = []
    for f in files:
        full_path = join(dir, f)
        df = get_etfs_from_file(full_path)
        frames.append(df)

    full_frame = pd.concat(frames)
    return full_frame


def get_etf_list_from_directory(dir):
    df = get_full_dataframe_for_directory(dir)
    etf_list = df['Symbol'].tolist()
    return etf_list


def get_etfs_in_dir_A_but_not_B(A, B):
    lst = []
    etfs_A = get_etf_list_from_directory(A)
    etfs_B = get_etf_list_from_directory(B)
    for e in etfs_A:
        if not e in etfs_B:
            lst.append(e)
    return lst


def get_all_etf_counts(root_dir):
    etf_dirs = file_op.get_only_dirs(root_dir)
    for dir in etf_dirs:
        full_path = join(ROOT_DIR, dir)
        full_frame = get_full_dataframe_for_directory(full_path)
        sh = full_frame.shape
        print("Number of ets in " + dir + " is " + str(sh[0]))


def get_list_of_columns_from_directory(dir):
    df = get_full_dataframe_for_directory(dir)
    columns = list(df.columns)
    return columns



get_all_etf_counts(ROOT_DIR)

etfs = get_etf_list_from_directory(ROOT_DIR + "/Region")
print (etfs)

etfs = get_etfs_in_dir_A_but_not_B(ROOT_DIR + "/Asset_Class", ROOT_DIR + "/Region")
print (etfs)
print (len(etfs))

etfs = get_etfs_in_dir_A_but_not_B(ROOT_DIR + "/Sector", ROOT_DIR + "/Region")
print (etfs)
print (len(etfs))

etfs = get_etfs_in_dir_A_but_not_B(ROOT_DIR + "/Volatility", ROOT_DIR + "/Region")
print (etfs)
print (len(etfs))

columns = get_list_of_columns_from_directory(ROOT_DIR + "/Region")
print (columns)

#Columns for db table ets: 'Symbol', 'ETF Name', 'Asset Class', 'Inverse', 'Leveraged', 'ETFdb.com Category', 'Inception'
