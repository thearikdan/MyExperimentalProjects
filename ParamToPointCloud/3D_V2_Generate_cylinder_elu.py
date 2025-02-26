import numpy as np
import tensorflow as tf
from os import listdir
from os.path import isfile, join
from plyfile import plyfile
import os
import shutil
import tf_nndistance
import tflearn

#use write_box.py, write_phere.py utils from experiments/mintools/point_cloud/primitives_to_point_clouds
#to generate datasets and point to them in the following line

BATCH_SIZE = 32
PARAMS_VECTOR_SIZE = 20 #sparse vector for holding param values for different primitives
POINT_COUNT = 1024
DIMS = 3
EPOCHS = 3000

LEARNING_RATE=0.001


PROJECT_NAME = "PPC2_V2_3D_CYLINDER_1500_1024_ELU"

DATA_DIR = '/raid/Github/experiments/mintools/point_cloud/primitives_to_point_clouds/data/cylinder/1500_1024'



GENERATED_DIR = "generated/"+ PROJECT_NAME
SUM_DIR = "summary/" + PROJECT_NAME
MODEL_PATH = "saved_sessions/" + PROJECT_NAME
BASE_NAME = PROJECT_NAME + ".ckpt"
EXCLUDE_SUFFIX = 'meta'
GENERATED_DEBUG_DIR = "generated_debug/" + PROJECT_NAME

labels = {"box":0,
          "cylinder":1,
          "sphere":2,
          "cone":3
         }



##########################
def get_latest_file(path, no_suffix):

	files = []

	for f in os.listdir(path):
	    if ((f.find('.') != -1) and (f.find(no_suffix) == -1)): 
		files.append(os.path.join(path, f))

	if not files:
		return ''

	latest = min(files, key=os.path.getctime)
	return latest


##########################
def get_latest_checkpoint(fname):
	pos = fname.rfind('-')
	if (pos == -1):
		return -1
	else:
		chkp_str = fname[pos+1:]
		return int(chkp_str)



##########################
def recreate_new_dir(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)



##########################
def ensure_dir_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)



##########################
def identity_initializer():
    def _initializer(shape, dtype=tf.float32):
        if len(shape) == 1:
            return tf.constant_op.constant(0., dtype=dtype, shape=shape)
        elif len(shape) == 2 and shape[0] == shape[1]:
            return tf.constant_op.constant(np.identity(shape[0], dtype))
        elif len(shape) == 4 and shape[2] == shape[3]:
            array = np.zeros(shape, dtype=float)
            cx, cy = shape[0]/2, shape[1]/2
            for i in range(shape[2]):
                array[cx, cy, i, i] = 1
            return tf.constant_op.constant(array, dtype=dtype)
        else:
            raise
    return _initializer


##########################
def get_primitive_params_pos_start_from_label(label):
    label_count = len(labels)
    pos = PARAMS_VECTOR_SIZE / label_count * label
    return pos


##########################
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
        p[i] = int (params[i-pos])

    return p


##########################
def write_point_cloud_to_file(dir, name, cloud):
    filename = join(dir, name)
    point_count = cloud.shape[0]

    vertex = np.zeros((point_count,),
                      dtype=[('x', 'f4'), ('y', 'f4'),
                             ('z', 'f4')])

    for i in range (point_count):
        x = cloud[i][0]
        y = cloud[i][1]
        z = cloud[i][2]
        print "x = " + str(x) + "; y = " + str(y) + "; z = " + str(z)
        vertex[i] = (x, y, z)

    el = plyfile.PlyElement.describe(vertex, 'vertex')
    plyfile.PlyData([el]).write(filename)



##########################
def write_color_point_cloud_to_file(dir, name, cloud, r, g, b):
    filename = join(dir, name)
    point_count = cloud.shape[0]

    vertex = np.zeros((point_count,),
                      dtype=[('x', 'f4'), ('y', 'f4'),
                             ('z', 'f4')])

    vertex_color = np.zeros((point_count, ),
                               dtype=[('red', 'u1'), ('green', 'u1'), ('blue', 'u1')])

    for i in range (point_count):
        x = cloud[i][0]
        y = cloud[i][1]
        z = cloud[i][2]
        vertex[i] = (x, y, z)
        vertex_color[i] = (r, g, b)

    vertex_all = np.empty(point_count, vertex.dtype.descr + vertex_color.dtype.descr)

    for prop in vertex.dtype.names:
        vertex_all[prop] = vertex[prop]

    for prop in vertex_color.dtype.names:
        vertex_all[prop] = vertex_color[prop]

    el = plyfile.PlyElement.describe(vertex_all, 'vertex')
    plyfile.PlyData([el]).write(filename)


##########################
def write_multiple_point_clouds_to_file(dir, name, clouds):
    filename = join(dir, name)
    cloud_count = clouds.shape[0]
    point_count = clouds.shape[1]
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
    colors_count = len(colors)

    vertex = np.zeros((point_count * cloud_count,),
                      dtype=[('x', 'f4'), ('y', 'f4'),
                             ('z', 'f4')])

    vertex_color = np.zeros((point_count * cloud_count, ),
                               dtype=[('red', 'u1'), ('green', 'u1'), ('blue', 'u1')])

    for k in range(cloud_count):
        for i in range (point_count):
            x = clouds[k][i][0]
            y = clouds[k][i][1]
            z = clouds[k][i][2]
            vertex[i + k * point_count] = (x, y, z)
            vertex_color[i + k * point_count] = colors[k % colors_count]

    vertex_all = np.empty(point_count * cloud_count, vertex.dtype.descr + vertex_color.dtype.descr)

    for prop in vertex.dtype.names:
        vertex_all[prop] = vertex[prop]

    for prop in vertex_color.dtype.names:
        vertex_all[prop] = vertex_color[prop]

    el = plyfile.PlyElement.describe(vertex_all, 'vertex')
    plyfile.PlyData([el]).write(filename)


##########################
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


##########################
def get_point_clouds_data(dir, files):
    """Returns point cloud data in shape(BATCH_SIZE, POINT_COUNT, DIMS)
    """
    batch_size = files.size
    data = np.zeros(shape=(batch_size, POINT_COUNT, DIMS))
    point_data = np.zeros(shape=(POINT_COUNT, DIMS))
    point = np.zeros(shape=(DIMS))
    for i in range(batch_size):
        file_name = files[i]
        file_data = get_point_cloud_from_file(dir, file_name)
        for j in range(POINT_COUNT):
            for k in range(DIMS):
                t = file_data[j]
                point[k] = t[k]
            point_data[j] = point
        data[i] = point_data
    return data


##########################
def batch_distance_matrix_general(A, B):
    r_A = tf.reduce_sum(A * A, axis=2, keep_dims=True)
    r_B = tf.reduce_sum(B * B, axis=2, keep_dims=True)
    m = tf.matmul(A, tf.transpose(B, perm=(0, 2, 1)))
    D = r_A - 2 * m + tf.transpose(r_B, perm=(0, 2, 1))
    return D


##########################
def knn_indices_general(queries, points, k, sorted=True):
    queries_shape = tf.shape(queries)
    batch_size = queries_shape[0]
    point_num = queries_shape[1]
    D = batch_distance_matrix_general(queries, points)
    distances, point_indices = tf.nn.top_k(-D, k=k, sorted=sorted)
    batch_indices = tf.tile(tf.reshape(tf.range(batch_size), (-1, 1, 1, 1)), (1, point_num, k, 1))
    indices = tf.concat([batch_indices, tf.expand_dims(point_indices, axis=3)], axis=3)
    return -distances, indices


##########################
# A shape is (batch_size, point_count, dims), B shape is (batch_size, point_count, dims)
def chamfer_distance_loss(A, B):
    distances, _ = knn_indices_general(A, B, 1, False)
    return tf.reduce_mean(distances)


############################
############################

############################
############################
def point_set_generation_loss(A, B):
    #https: // github.com / fanhqme / PointSetGeneration
    #https: // arxiv.org / abs / 1612.00603
    dists_forward, _, dists_backward, _ = tf_nndistance.nn_distance(A, B)
    mindist = dists_forward
    dist0 = mindist[0, :]
    dists_forward = tf.reduce_mean(dists_forward)
    dists_backward = tf.reduce_mean(dists_backward)
    loss_nodecay = (dists_forward + dists_backward / 2.0) * 10000
    loss = loss_nodecay + tf.add_n(tf.get_collection(tf.GraphKeys.REGULARIZATION_LOSSES)) * 0.1
#    loss = loss_nodecay
    return loss

############################
############################

recreate_new_dir(GENERATED_DIR)
recreate_new_dir(GENERATED_DEBUG_DIR)


save_path = join(MODEL_PATH, BASE_NAME)

#tf_pc_params = tf.placeholder(tf.int32, shape = [None, PARAMS_VECTOR_SIZE])
tf_pc_params = tf.placeholder(tf.float32, shape = [None, PARAMS_VECTOR_SIZE])
tf_pc_data = tf.placeholder(tf.float32, shape = [None, POINT_COUNT, DIMS])


#Network
with tf.device('/gpu:1'):
	with tf.name_scope('fc1'):
	#    layer1 = tf.layers.dense(inputs=tf_pc_params, units=PARAMS_VECTOR_SIZE, activation=tf.nn.relu, name = "fc1")
	    layer1 = tflearn.layers.core.fully_connected(tf_pc_params, PARAMS_VECTOR_SIZE, activation=tf.nn.elu, weight_decay=1e-4,
		                                           regularizer='L2', name = "fc1")
	    fc1_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, 'fc1')
	    tf.summary.histogram('kernel', fc1_vars[0])
	    tf.summary.histogram('bias', fc1_vars[1])
	    tf.summary.histogram('act', layer1)

	    dropout1 = tf.layers.dropout(inputs=layer1, rate=0.4, training=True)

	out_name = "out"
	out_k = "out_kernel"
	out_b = "out_bias"
	out_a = "out_act"


	with tf.name_scope(out_name):
	    dim_layer = tflearn.layers.core.fully_connected(dropout1, POINT_COUNT * DIMS, activation=tf.nn.elu, weight_decay=1e-4,
		                                     regularizer='L2', name=out_name)

	    out_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, out_name)
	    tf.summary.histogram(out_k, out_vars[0])
	    tf.summary.histogram(out_b, out_vars[1])
	    tf.summary.histogram(out_a, dim_layer)

	z = tf.reshape(dim_layer, [-1, POINT_COUNT, DIMS])

	loss_op = point_set_generation_loss(z, tf_pc_data)

	loss_summary = tf.summary.scalar("loss", loss_op)

	adam = tf.train.AdamOptimizer(LEARNING_RATE)
	train_op = adam.minimize(loss_op, name = "train_op")

	merge_op = tf.summary.merge_all()
	sum_writer = tf.summary.FileWriter(SUM_DIR)

	saver = tf.train.Saver()


with tf.Session(config=tf.ConfigProto(
      allow_soft_placement=True, log_device_placement=True)) as sess:
    sess.run(tf.global_variables_initializer())

    #fname = get_latest_file(MODEL_PATH, EXCLUDE_SUFFIX)
    fname = "saved_sessions/PPC2_V2_3D_CYLINDER_1500_1024_ELU/PPC2_V2_3D_CYLINDER_1500_1024_ELU_6000.ckpt"

    if (len(fname) == 0):
        print ("Could not find model")
        exit(-1)

    saver.restore(sess, fname)

    cylinders = ["cylinder_40_20_", "cylinder_80_40_"] #array of cylinders to generate
    count = len(cylinders)

    file_names = []
    data_files = []
    for i in range (count):
        file_names.append(cylinders[i] + ".ply")
        data_files.append(GENERATED_DEBUG_DIR + '/' + cylinders[i] + ".csv")

    params = np.zeros(shape = (count, PARAMS_VECTOR_SIZE))
    for i in range(count):
        params[i] = get_primitive_file_label_params(file_names[i])

    out_clouds = sess.run(z, feed_dict = {tf_pc_params:params})
    print('Writing out point cloud files')

    write_multiple_point_clouds_to_file(GENERATED_DIR, "compare_cylinders.ply", out_clouds)




