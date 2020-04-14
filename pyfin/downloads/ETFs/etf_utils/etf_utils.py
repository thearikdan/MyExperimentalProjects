import sys
sys.path.append("../../..")

from utils import file_op
import pandas as pd
from os.path import join
import math


def replace_nan_in_list(lst, s):
    count = len(lst)
    for i in range (count):
        if type (lst[i]) != str:
            lst[i] = s
    return lst


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


def get_list_of_columns_from_directory(dir):
    df = get_full_dataframe_for_directory(dir)
    columns = list(df.columns)
    return columns



def get_all_dataframes(root_dir):
    dirs = file_op.get_only_dirs(root_dir)
    frames = []
    for d in dirs:
        path = join(root_dir, d)
        df = get_full_dataframe_for_directory(path)
        frames.append(df)

#    all_frames = pd.concat(frames, sort='False')
    all_frames = pd.concat(frames)
    return all_frames



def get_all_asset_classes(root_dir):
    all_frames = get_all_dataframes(root_dir)
    asset_list = all_frames['Asset Class'].tolist()
    lst = list(set(asset_list))
    replace_nan_in_list(lst, "n/a")
    return lst



def get_all_categories(root_dir):
    all_frames = get_all_dataframes(root_dir)
    cats = all_frames['ETFdb.com Category'].tolist()
    lst = list(set(cats))
    replace_nan_in_list(lst, "n/a")
    return lst
    return list(set(cats))


def get_all_dataframes_for_db(root_dir):
    all_frames = get_all_dataframes(root_dir)
    db_frames = all_frames[['Symbol', 'ETF Name', 'Asset Class', 'Inverse', 'Leveraged', 'ETFdb.com Category']]
    return db_frames
