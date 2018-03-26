import tensorflow as tf

DATA_DIR = "data/cnn/"
OUTPUT_DIR = "output/images/cnn/"


def _parser(record):
    features={
        'label': tf.FixedLenFeature([], tf.int64),
        'image': tf.FixedLenFeature([], tf.string)
    }
    parsed_record = tf.parse_single_example(record, features)
    image_decoded = tf.decode_raw(parsed_record['image'], tf.float32)
    image = tf.reshape(image_decoded, [128, 128])

    label = tf.cast(parsed_record['label'], tf.int32)

    return image, label

filenames = tf.placeholder(tf.string, shape=[None])
dataset = tf.data.TFRecordDataset(filenames)

dataset = dataset.map(_parser)
dataset = dataset.repeat()
dataset = dataset.batch(32)

iterator = dataset.make_initializable_iterator()
next_element = iterator.get_next()


sess = tf.Session()

#Run tfRecord_write.py to get tfrecord files

training_filenames = [DATA_DIR + "train_tfrecords"]
sess.run(iterator.initializer, feed_dict={filenames: training_filenames})

for i in range (100):
    value = sess.run(next_element)
    images = value[0]
    labels = value[1]
    print images


#validation_filenames = ["test.tfrecords"]
#sess.run(iterator.initializer, feed_dict={filenames: validation_filenames})
