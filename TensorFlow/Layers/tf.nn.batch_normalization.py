#requires tensorflow 1.3

import tensorflow as tf

unif_10 = tf.constant([-9.0, -8.0, -7.0, -6.0, -5.0, -4.0, -3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])
mean, variance = tf.nn.moments(unif_10, axes=[0])
offset_0 = tf.constant(0.0)
scale_0 = tf.constant(1.0)
variance_epsilon = tf.constant(0.001)
out1 = tf.nn.batch_normalization(unif_10, mean, variance, offset_0, scale_0, variance_epsilon)
#out1 = tf.nn.batch_normalization(unif_10, mean, variance, None, None, variance_epsilon)

with tf.Session() as sess:
    print (sess.run(unif_10))
    print (sess.run(mean))
    print (sess.run(variance))
    print (sess.run(offset_0))
    print (sess.run(scale_0))
    print (sess.run(variance_epsilon))

    print (sess.run(out1))



