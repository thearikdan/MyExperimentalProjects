import tensorflow as tf
import time

sample_size = 1024
sample_count = 1000

x_input_data = tf.random_uniform([sample_size, sample_count], -10.0, 10.0)
y_output_data = tf.cast(tf.reduce_mean(x_input_data, axis = 1, keep_dims = True) > 0, tf.int32)

sample = tf.placeholder([sample_size, None], dtype = tf.float32)
res = tf.placeholder([sample_size, None], dtype = tf.int32)

#Network
fc1 = tf.random_uniform([sample_size, sample_size], -1.0, 1.0)
s11 = tf.mult(x_input_data, fc1)
b1 = tf.random_uniform([sample_size], -1.0, 1.0)
s12 = tf.sum(s11, b1)





q = tf.FIFOQueue(sample_size, dtypes = tf.float32, shapes = ())

enqueue_op = q.enqueue_many(x_input_data)

numberOfThreads = 1
qr = tf.train.QueueRunner(q, [enqueue_op] * numberOfThreads)
# Don't forget to add your "QueueRunner" to the QUEUE_RUNNERS collection
tf.train.add_queue_runner(qr)

dequeue_op = q.dequeue_many(sample_size)

y = tf.square(dequeue_op)


start = time.time()

with tf.Session() as sess:
#    print sess.run(x_input_data)
    sess.run(tf.global_variables_initializer())
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(coord=coord)
    print sess.run(y)
    
    coord.request_stop()
    coord.join(threads)

 
end = time.time()

print "Elapsed time: " + str(end - start) + " sec."
