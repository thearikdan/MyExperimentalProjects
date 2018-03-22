import tensorflow as tf
from utils import file_op
from os.path import join

def _parser(record):
    features={
        'label': tf.FixedLenFeature([], tf.int64),
        'view_count': tf.FixedLenFeature([], tf.int64)
    }
    count = 80  #need to determine view_count dynamically
    for i in range(count):
        desc_key = "description_" + str(i)
        features[desc_key] = tf.FixedLenFeature([], tf.string)
        view_key = "view_" + str(i)
        features[view_key] = tf.FixedLenFeature([], tf.string)

    parsed_record = tf.parse_single_example(record, features)
    descriptions = []
    images = []
   
    for i in range (count):
        desc_key = "description_" + str(i)
        descriptions.append(parsed_record[desc_key])
        view_key = "view_" + str(i)
        images.append(tf.decode_raw(parsed_record[view_key], tf.float32))

    label = tf.cast(parsed_record['label'], tf.int32)
    view_count = tf.cast(parsed_record['view_count'], tf.int32)

    return label, view_count, descriptions, images

TRAIN_TFRECORD_DIR = "/media/ara/HDD/MyProjects/TensorFlow/data/mvcnn/train"


filenames = tf.placeholder(tf.string, shape=[None])
dataset = tf.data.TFRecordDataset(filenames)


dataset = dataset.map(_parser)
'''
dataset = dataset.repeat()
dataset = dataset.batch(32)

iterator = dataset.make_initializable_iterator()
next_element = iterator.get_next()


sess = tf.Session()

fs = file_op.get_only_files(TRAIN_TFRECORD_DIR)

file_count = len(fs)
training_filenames = []

for i in range (file_count):
    training_filenames.append(join(TRAIN_TFRECORD_DIR, fs[i]))

sess.run(iterator.initializer, feed_dict={filenames: training_filenames})

for i in range (20):
    value = sess.run(next_element)
    print value


#validation_filenames = ["test.tfrecords"]
#sess.run(iterator.initializer, feed_dict={filenames: validation_filenames})
'''
