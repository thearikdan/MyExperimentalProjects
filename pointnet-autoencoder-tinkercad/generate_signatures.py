import tensorflow as tf
import numpy as np
import argparse
import socket
import importlib
import time
import os
import scipy.misc
import sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = BASE_DIR
sys.path.append(BASE_DIR) # model
sys.path.append(ROOT_DIR) # provider
sys.path.append(os.path.join(ROOT_DIR, 'models'))
sys.path.append(os.path.join(ROOT_DIR, 'utils'))
#import show3d_balls
import part_dataset

parser = argparse.ArgumentParser()
parser.add_argument('--gpu', type=int, default=0, help='GPU to use [default: GPU 0]')
parser.add_argument('--num_point', type=int, default=2048, help='Point Number [default: 2048]')
parser.add_argument('--category', default=None, help='Which single class to train on [default: None]')
parser.add_argument('--model', default='model', help='Model name [default: model]')
parser.add_argument('--model_path', default='log/model.ckpt', help='model checkpoint file path [default: log/model.ckpt]')
parser.add_argument('--num_group', type=int, default=1, help='Number of groups of generated points -- used for hierarchical FC decoder. [default: 1]')
FLAGS = parser.parse_args()


MODEL_PATH = FLAGS.model_path
GPU_INDEX = FLAGS.gpu
NUM_POINT = FLAGS.num_point
MODEL = importlib.import_module(FLAGS.model) # import network module
DATA_PATH = os.path.join(BASE_DIR, 'data/numpy_mean_0_normalized')
TEST_DATASET = part_dataset.PartDataset(root=DATA_PATH, npoints=NUM_POINT, classification=False, class_choice=FLAGS.category, split='test',normalize=True)
print(len(TEST_DATASET))

def get_model(batch_size, num_point):
    with tf.Graph().as_default():
        with tf.device('/gpu:'+str(GPU_INDEX)):
            pointclouds_pl, labels_pl = MODEL.placeholder_inputs(batch_size, num_point)
            is_training_pl = tf.placeholder(tf.bool, shape=())
            pred, end_points = MODEL.get_model(pointclouds_pl, is_training_pl)
            loss = MODEL.get_loss(pred, labels_pl, end_points)
            saver = tf.train.Saver()
        # Create a session
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        config.allow_soft_placement = True
        sess = tf.Session(config=config)
        # Restore variables from disk.
        saver.restore(sess, MODEL_PATH)
        ops = {'pointclouds_pl': pointclouds_pl,
               'labels_pl': labels_pl,
               'is_training_pl': is_training_pl,
               'pred': pred,
               'loss': loss,
               'signature': end_points['embedding']}
        return sess, ops

def inference(sess, ops, pc, batch_size):
    ''' pc: BxNx3 array, return BxN pred '''
    assert pc.shape[0]%batch_size == 0
    num_batches = pc.shape[0]/batch_size
#    logits = np.zeros((pc.shape[0], pc.shape[1], 3))
    signatures = np.zeros((batch_size, 1024))
    for i in range(num_batches):
        feed_dict = {ops['pointclouds_pl']: pc[i*batch_size:(i+1)*batch_size,...],
                     ops['is_training_pl']: False}
#        feed_dict = {ops['pointclouds_pl']: pc[i*batch_size:(i+1)*batch_size,...]}

        batch_logits, batch_signatures = sess.run([ops['pred'], ops['signature']], feed_dict=feed_dict)
#        batch_logits = sess.run(ops['pred'], feed_dict=feed_dict)
        batch_signatures = sess.run(ops['signature'], feed_dict=feed_dict)
#        logits[i*batch_size:(i+1)*batch_size,...] = batch_logits
        signatures[i*batch_size:(i+1)*batch_size,...] = batch_signatures
#    return logits, signatures
    return signatures


def get_design_name_from_file(name_tuple):
    suffix = "-ascii.txt"
    suffix_length = len(suffix)
    name = name_tuple[1]
    base_name = os.path.basename(name)
    base_name_length = len(base_name)
    design_name = base_name[:(base_name_length - suffix_length)]
    return design_name



if __name__=='__main__':

    num_group = FLAGS.num_group
    color_list = []
    for i in range(num_group):
        color_list.append(np.random.random((3,)))

    sess, ops = get_model(batch_size=1, num_point=NUM_POINT)
    indices = np.arange(len(TEST_DATASET))
    np.random.shuffle(indices)
    for i in range(len(TEST_DATASET)):
        ps, seg, fn = TEST_DATASET[indices[i]]
        design_name = get_design_name_from_file(fn)
#        pred, signature = inference(sess, ops, np.expand_dims(ps,0), batch_size=1)
#        pred = pred.squeeze()
        signature = inference(sess, ops, np.expand_dims(ps,0), batch_size=1)

