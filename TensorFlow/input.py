import random
import tensorflow as tf

def func(x1, x2, x3, x4):
    return (2*x1 + 3*x2 + 4 *x3 +5 * x4)


def get_parameters(low, high):
    a = [random.randint(low, high), random.randint(low, high), random.randint(low, high), random.randint(low, high)]
    return a


def create_record(low, high):
    a = get_parameters(low, high)
    b = func(a[0], a[1], a[2], a[3])
    el = (a[0] , a[1], a[2], a[3], b)
    s = ','.join(str(s) for s in el)
    return s

def create_array(count, low, high):
    arr = []
    for i in range(count):
        a = create_record(low, high)
        arr.append(a)
    print arr
    return arr


def create_file(name, count):
    low = 1
    high = 10
    arr = create_array(count, low, high)
    count = len(arr)
    with open(name, 'wb')  as myfile:
        for item in arr:
            myfile.write("%s\n" % item)


create_file("file0.csv", 5)
create_file("file1.csv", 5)

filename_queue = tf.train.string_input_producer(["file0.csv", "file1.csv"])
reader = tf.TextLineReader()
key, value = reader.read(filename_queue)

record_defaults = [[1], [1], [1], [1], [1]]
col1, col2, col3, col4, col5 = tf.decode_csv(value, record_defaults=record_defaults)
features = tf.stack([col1, col2, col3, col4])


with tf.Session() as sess:
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(coord=coord)

    for i in range(10):
        example, label = sess.run([features, col5])
        print "example:"
        print example
        print "label:"
        print label

coord.request_stop()
coord.join.threads()
