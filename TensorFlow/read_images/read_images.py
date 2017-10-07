from os import listdir
from os.path import isfile, join, isdir

ROOT = "data"

def get_files(mypath):
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles


def get_directories(root):
    onlydirs = [f for f in listdir(root) if isdir(join(root, f))]
    return onlydirs


def get_label_dict(root):
    dic = {}
    dirs = get_directories(root)
    for i, d in enumerate(dirs):
        dic[d] = i
    return dic


label_dic = get_label_dict(ROOT)
#print label_dic

files = []
labels = []

dirs = get_directories(ROOT)
#print dirs


for d in dirs:
    l = label_dic[d]
    dr = join(ROOT, d)
    fl = get_files(dr)
    for f in fl:
        labels.append(l)
        files.append(join (dr, f))

print files
print labels
