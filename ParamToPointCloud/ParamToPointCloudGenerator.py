import numpy as np
import tensorflow as tf
from os import listdir
from os.path import isfile, join
from plyfile import plyfile


#DATA_DIR = '/raid/MyProjects/python-point-cloud/data/boxes'
DATA_DIR = '/media/ara/HDD/MyProjects/python-point-cloud/data/boxes'
BATCH_SIZE = 2
PARAMS_VECTOR_SIZE = 256 #sparse vector for holding param values for different primitives
POINT_COUNT = 2048
DIMS = 3

labels = {"box":0,
          "cylinder":1,
          "sphere":2,
          "plane":3
         }


def get_primitive_params_pos_start_from_label(label):
    label_count = len(labels)
    pos = PARAMS_VECTOR_SIZE / label_count * label
    return pos



def get_primitive_file_label_params(name):
    """Returns label and parameters, derived from a file name, in a sparse vector
    First, is the label of the class (for example, box is 0)
    Next, are parameters like width, length, height, or other parameters relevant to the class
    The position of the parameters in the vector is determined by the class, and is positioned to ensure sparsity of the vector
    """
    params = name.split('_')
    count = len(params)
    p = np.zeros(PARAMS_VECTOR_SIZE)
    label = int (labels[params[0]])
    pos = get_primitive_params_pos_start_from_label(label)
    p[pos] = label
    for i in range (pos + 1, pos + count - 1): #count -1 because last param is the ".ply" extension
        p[i] = int (params[i])

    return p


def get_point_cloud_from_file(dir, name):
    filename = join(dir, name)
    plydata = plyfile.PlyData.read(filename)
    data = plydata.elements[0].data
    arr = np.fromiter(data, dtype=[('x', '<f4'), ('y', '<f4'), ('z', '<f4')])
    return arr


def get_point_clouds_labels_params(files):
    """Returns label and parameters for each file in a numpy array
    """
    count = files.size
    params = np.zeros(shape = (count, PARAMS_VECTOR_SIZE))
    for i in range(count):
        file_name = files[i]
        param = get_primitive_file_label_params(file_name)
        params[i] = param
    
    return params



def get_point_clouds_data(dir, files):
    """Returns label and parameters for each file in a numpy array
    """
    count = files.size
    data = np.zeros(shape=(count, POINT_COUNT))
    for i in range(count):
        file_name = files[i]
        file_data = get_point_cloud_from_file(dir, file_name)
        data[i] = file_data

    return data



#List all files, and shuffle them randomly into an np.array
files = [f for f in listdir(DATA_DIR) if isfile(join(DATA_DIR, f))]
data_files = np.array(files)
np.random.shuffle(data_files)
count = data_files.size

#tf_pc_params = tf.placeholder(tf.int32, shape = [None, PARAMS_VECTOR_SIZE])
tf_pc_params = tf.placeholder(tf.float32, shape = [None, PARAMS_VECTOR_SIZE])
tf_pc_data = tf.placeholder(tf.float32, shape = [None, POINT_COUNT])



#Dummy data for now
tf_params = tf_pc_params
tf_data = tf_pc_data

#Network
w = tf.get_variable('w', shape = [DIMS, PARAMS_VECTOR_SIZE, POINT_COUNT])
b = tf.get_variable('b', shape = [DIMS, POINT_COUNT])

outs = []

for i in range(DIMS):
    t1 = tf.matmul(tf_params, w[i]) + b[i]
    t2 = tf.nn.relu(t1)
    outs.append(t2)

z = tf.stack(outs)


with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    for i in xrange(0, count, BATCH_SIZE):
#        print "Batch " + str(i / BATCH_SIZE)
        print data_files[i:i+BATCH_SIZE]
        params = get_point_clouds_labels_params(data_files[i:i+BATCH_SIZE])
#        print params
        data = get_point_clouds_data(DATA_DIR, data_files[i:i+BATCH_SIZE])
#        print data
        p, d = sess.run([tf_params, tf_data], feed_dict = {tf_pc_params:params, tf_pc_data:data})
        print p, d

