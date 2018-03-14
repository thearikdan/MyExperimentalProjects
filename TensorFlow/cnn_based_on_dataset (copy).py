#Based on https://kratzert.github.io/2017/06/15/example-of-tensorflows-new-input-pipeline.html

import tensorflow as tf
from tensorflow.contrib.data import Dataset, Iterator

import os
from glob import glob
from os.path import dirname

#TRAIN_DIR = "/raid/data/cnn/m40/train"
#TEST_DIR = "/raid/data/cnn/m40/test" 

TRAIN_DIR = "/media/ara/HDD/data/cnn/m40/train"
TEST_DIR = "/media/ara/HDD/data/cnn/m40/test"


BATCH_SIZE = 20
SHAPE = [128, 128]

def get_labels_from_files(files):
    labels = []
    for f in files:
        directory = dirname(f)
        dirs = directory.split('/')
        dirs_len = len(dirs)
        labels.append(dirs[dirs_len - 1])
    return labels


def convert_labels_to_numbers(labels, classes):
    label_numbers = []
    label_count = len(labels)
    class_count = len(classes)
    for i in range (label_count):
        for j in range (class_count):
            if labels[i] == classes[j]:
                label_numbers.append(j)
    return label_numbers


def input_parser(img_path, label):
    one_hot = tf.one_hot(label, CLASS_COUNT)

    img_file = tf.read_file(img_path)
    img_decoded = tf.image.decode_image(img_file, channels=1)
    return img_decoded, one_hot


train_files = [y for x in os.walk(TRAIN_DIR) for y in glob(os.path.join(x[0], '*.png'))]
train_labels = get_labels_from_files(train_files)

classes = list(set(train_labels))
CLASS_COUNT = len(classes)

train_classes = convert_labels_to_numbers(train_labels, classes)

tf_train_files = tf.constant(train_files)
tf_train_classes = tf.constant(train_classes)


test_files = [y for x in os.walk(TEST_DIR) for y in glob(os.path.join(x[0], '*.png'))]
test_labels = get_labels_from_files(test_files)
test_classes = convert_labels_to_numbers(test_labels, classes)

tf_test_files = tf.constant(test_files)
tf_test_classes = tf.constant(test_classes)



def get_dataset(image_files, labels, shuffle, batch_size, repeat_count):
    data = Dataset.from_tensor_slices((image_files, labels))
    data = data.map(input_parser)
    data = dataset.repeat(repeat_count)
    if (shuffle):
        data = data.shuffle(buffer_size = 10000)
    data = data.batch(batch_size)
    return data


def input_fn(dir, classes, batch_size, shuffle=False, repeat_count=1):
    files = [y for x in os.walk(dir) for y in glob(os.path.join(x[0], '*.png'))]
    labels = get_labels_from_files(files)
    num_labels = convert_labels_to_numbers(labels, classes)

    tf_files = tf.constant(test_files)
    tf_labels = tf.constant(num_labels)

    data = get_dataset(tf_files, tf_labels, shuffle, batch_size, repeat_count)

    iterator = data.make_one_shot_iterator()
    batch_images, batch_labels = iterator.get_next()
    return batch_images, batch_labels



def cnn_model_fn(images, labels, mode):
    #Input layer
    input_layer = tf.reshape(images[x], [-1, 128, 128, 1])

    #Convolutional layer
    conv1 = tf.layers.conv2d(input = input_layer,
                             filters=32,
                             kernel_size=[5,5],
                             padding="same",
                             activation=tf.nn.relu)

    #Pooling Layer #1
    pool1 = tf.layers.max_pooling2D(inputs=conv1,
                                    pool_size=[2,2],
                                    strides=2)

    #Convolutional Layer#2 and Poling #2
    conv2 = tf.layers.conv2d(input = pool1,
                             filters=64,
                             kernel_size=[5,5],
                             padding="same",
                             activation=tf.nn.relu)
    pool2 = tf.layers.max_pooling2D(inputs=conv2,
                                    pool_size=[2,2],
                                    strides=2)

    #Dense Layer
    pool2_flat = tf.reshape(pool2, [-1, 7 * 7 * 64])
    dense = tf.layers.dense(inputs=pool2_flat,
                            units=1024,
                            activation=tf.nn.relu)
    dropout = tf.layers.dropout(inputs=dense,
                                rate=0.4,
                                training=mode == tf.estimator.ModeKeys.TRAIN)

    #Logits layer
    logits = tf.layers.dense(inputs=dropout, units = CLASS_COUNT)

    predictions = {
      # Generate predictions (for PREDICT and EVAL mode)
      "classes": tf.argmax(input=logits, axis=1),
      # Add `softmax_tensor` to the graph. It is used for PREDICT and by the
      # `logging_hook`.
      "probabilities": tf.nn.softmax(logits, name="softmax_tensor")
     }

    if mode == tf.estimator.ModeKeys.PREDICT:
        return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions)

    # Calculate Loss (for both TRAIN and EVAL modes)
    loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)

    # Configure the Training Op (for TRAIN mode)
    if mode == tf.estimator.ModeKeys.TRAIN:
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001)
        train_op = optimizer.minimize(
            loss=loss,
            global_step=tf.train.get_global_step())
        return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)

    # Add evaluation metrics (for EVAL mode)
    eval_metric_ops = {
          "accuracy": tf.metrics.accuracy(
              labels=labels, predictions=predictions["classes"])}
    return tf.estimator.EstimatorSpec(
          mode=mode, loss=loss, eval_metric_ops=eval_metric_ops)



#Create Dataset objects
train_data = get_dataset(tf_train_files, tf_train_classes, BATCH_SIZE)
test_data = get_dataset(tf_test_files, tf_test_classes, BATCH_SIZE)


#Create Iterator object
iterator = Iterator.from_structure(train_data.output_types, train_data.output_shapes)
next_element = iterator.get_next()

#Create two initializations to switch between datasets
train_init_op = iterator.make_initializer(train_data)
test_init_op = iterator.make_initializer(test_data)

feature_columns = [
    tf.feature_column.numeric_column(key="Image", dtype=tf.float64, shape = SHAPE)
    tf.feature_column.numeric_column(key="Label", dtype=tf.int32)
    ]

classifier = tf.estimator.Estimator(cnn_model_fn, model_dir="CNN_Model")


'''
with tf.Session() as sess:
    sess.run(train_init_op)

    while(True):
        try:
#            elem = sess.run(next_element)
#            print elem
            images, labels = sess.run(next_element)
            print images, labels
            cnn_model_fn(images, labels, tf.estimator.ModeKeys.TRAIN)

            print "------------------------"
        except tf.errors.OutOfRangeError:
            print ("End of training dataset")
            break


    sess.run(test_init_op)

    while(True):
        try:
            elem = sess.run(next_element)
            print elem
            print "------------------------"
        except tf.errors.OutOfRangeError:
            print ("End of testing dataset")
            break
            
'''