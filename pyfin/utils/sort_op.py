def get_sorted_indices(myList):
    return [i[0] for i in sorted(enumerate(myList), key=lambda x:x[1])]

