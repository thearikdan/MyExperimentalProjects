import tensorflow as tf

def _parser(record):
    features={
        'label': tf.FixedLenFeature([], tf.int64),
        'image': tf.FixedLenFeature([], tf.string)
    }
    parsed_record = tf.parse_single_example(record, features)
    image = tf.decode_raw(parsed_record['image'], tf.float32)

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

training_filenames = ["train_tfrecords"]
sess.run(iterator.initializer, feed_dict={filenames: training_filenames})

for i in range (100):
    value = sess.run(next_element)
    print value


#validation_filenames = ["test.tfrecords"]
#sess.run(iterator.initializer, feed_dict={filenames: validation_filenames})
