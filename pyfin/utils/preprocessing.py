import numpy as np
from os.path import join


def unison_shuffled_copies(a, b):
    assert len(a) == len(b)
    p = np.random.permutation(len(a))
    return a[p], b[p]


def generate_numeric_labels(labels, classes_path):
    label_count = len(labels)
    numeric_labels = np.zeros(label_count)
    classes = list(set(labels))
    #store classes in file for persistency between sessions
    filename = join(classes_path, 'tinkercad_classes.txt')
    with open(filename, 'w') as f:
        for item in classes:
            f.write("%s\n" % item)
    class_count = len(classes)
    for i in range (label_count):
        for j in range(class_count):
            if (labels[i]==classes[j]):
                numeric_labels[i] = j
    return class_count, numeric_labels


def get_numeric_labels(labels, classes_path):
    classes = []
    filename = join(classes_path, 'tinkercad_classes.txt')
    with open(filename, 'r') as f:
        classes = f.read().splitlines()

    label_count = len(labels)
    numeric_labels = np.zeros(label_count)
    #store classes in file for persistency between sessions
    class_count = len(classes)
    for i in range (label_count):
        for j in range(class_count):
            if (labels[i]==classes[j]):
                numeric_labels[i] = j
    return class_count, numeric_labels



def get_one_hot_encoded(labels):
    label_count = len(labels)
    classes = list(set(labels))
    class_count = len(classes)
    one_hot = np.zeros(shape=(label_count, class_count), dtype=int)
    for i in range (label_count):
        for j in range(class_count):
            if (labels[i]==classes[j]):
                one_hot[i, j] = 1
                break
    return one_hot

