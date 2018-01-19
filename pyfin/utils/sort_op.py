def get_sorted_indices(myList):
    return [i[0] for i in sorted(enumerate(myList), key=lambda x:x[1])]


def get_resorted_list(orig_list, sorted_indices):
    resorted_list = []
    count = len(orig_list)
    for i in range (count):
        resorted_list.append(orig_list[sorted_indices[i]])

    return resorted_list


