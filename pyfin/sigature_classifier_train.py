import sys
sys.path.append("../")

from utils import db, file_op, DNN
import numpy as np
import tensorflow as tf
from os.path import join
import utils.preprocessing as prp

LEARNING_RATE=0.0001
EPOCHS = 3000
BATCH_SIZE = 20
PROJECT_NAME = "signature_classifier"
SUM_DIR = PROJECT_NAME + "_summary"
MODEL_PATH = PROJECT_NAME + "_model"
CLASSES_PATH = PROJECT_NAME + "_classes"




def get_signatures_from_ids(conn, cur, ids, algo_id):
    signatures = []
    count = len(ids)
    for i in range(count):
        sig = db.get_signature_from_design_id_and_algorithm_id(conn, cur, ids[i], algo_id)
        signatures.append(sig)
    #convert list to numpy, otherwise placeholder will complain
    size = len(signatures[0])
    np_sig = np.zeros(shape=(count, size))
    for i in range (count):
        if signatures[i] is not None:
            for j in range(size):
                np_sig[i][j] = signatures[i][j]
    return np_sig



file_op.recreate_new_dir(SUM_DIR)
file_op.recreate_new_dir(MODEL_PATH)
file_op.recreate_new_dir(CLASSES_PATH)


conn, cursor = db.connect_to_database("db_settings.txt")

train_ids, _, train_labels = db.get_verified_ids_tinkercad_design_ids_and_classes_from_usage(conn, cursor, "training")
#test_ids, _, test_labels = db.get_verified_ids_tinkercad_design_ids_and_classes_from_usage(conn, cursor, "testing")

train_labels = np.array(train_labels)
#test_labels = np.array(test_labels)

train_signatures = get_signatures_from_ids(conn, cursor, train_ids, 2)
#test_signatures = get_signatures_from_ids(conn, cursor, test_ids, 2)


train_signatures_shuffled, train_labels_shuffled = prp.unison_shuffled_copies(train_signatures, train_labels)
#test_signatures_shuffled, test_labels_shuffled = prp.unison_shuffled_copies(test_signatures, test_labels)


train_count = len(train_signatures)
#test_count = len(test_signatures)


cursor.close()
conn.close()

SIGNATURE_SIZE=len(train_signatures[0])

CLASS_COUNT, numeric_train_labels_shuffled = prp.generate_numeric_labels(train_labels_shuffled, CLASSES_PATH)
#_, numeric_test_labels_shuffled = prp.get_numeric_labels(test_labels_shuffled)


#depth = tf.constant(CLASS_COUNT)

train_one_hot_encoded_shuffled = prp.get_one_hot_encoded(train_labels_shuffled)
#test_one_hot_encoded_shuffled = prp.get_one_hot_encoded(test_labels_shuffled)


#we are using tensorflow 1.4, so no feaure columns
tf_signatures = tf.placeholder(tf.float32, shape = [None, SIGNATURE_SIZE])
tf_labels = tf.placeholder(tf.int32, shape = [None, CLASS_COUNT])


logits_train= DNN.signature_to_class_model(tf_signatures, 0.4, True, SIGNATURE_SIZE, CLASS_COUNT)
predicted_classes_train = tf.argmax(logits_train, 1)

loss_op = tf.nn.softmax_cross_entropy_with_logits(logits=logits_train, labels=tf_labels)
loss_op = tf.reduce_mean(loss_op)

loss_summary = tf.summary.scalar("loss", loss_op)

adam = tf.train.AdamOptimizer(LEARNING_RATE)
train_op = adam.minimize(loss_op, name="train_op")

merge_op = tf.summary.merge_all()
sum_writer = tf.summary.FileWriter(SUM_DIR)

saver = tf.train.Saver()

tf_sig = tf_signatures
tf_labs = tf_labels

with tf.Session(config=tf.ConfigProto(
      allow_soft_placement=True, log_device_placement=True)) as sess:
    sess.run(tf.global_variables_initializer())

    for i in range (EPOCHS + 1):
        print('-------------------------')
        print('Current iteration:%d' % (i))

        for j in xrange(0, train_count, BATCH_SIZE):
            print('Processing batch:%d' % (j / BATCH_SIZE))
            sig = train_signatures_shuffled[j:j+BATCH_SIZE]
            lab = train_one_hot_encoded_shuffled[j:j+BATCH_SIZE]
            log, pred, loss, opt, merged = sess.run([logits_train, predicted_classes_train, loss_op, train_op, merge_op], feed_dict = {tf_signatures:sig, tf_labels:lab})

        print('-------------------------')
        print('iter:%d - loss:%f' % (i, loss))
        sum_writer.add_summary(merged, i)

        BASE_NAME = PROJECT_NAME + "_" + str(i) + ".ckpt"
        save_path = join(MODEL_PATH, BASE_NAME)

        if (i % 100 == 0):
            saver.save(sess, save_path)
