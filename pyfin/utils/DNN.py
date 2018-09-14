import tensorflow as tf

def signature_to_class_model(signatures, dropout_rate, is_training, signature_size, class_count):
    with tf.name_scope('fc1'):
        layer1 = tf.layers.dense(inputs=signatures, units=signature_size, activation=tf.nn.relu, name = "fc1")
        fc1_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, 'fc1')
        tf.summary.histogram('kernel', fc1_vars[0])
        tf.summary.histogram('bias', fc1_vars[1])
        tf.summary.histogram('act', layer1)

        dropout1 = tf.layers.dropout(inputs=layer1, rate=dropout_rate, training=is_training)

    l2_units = (class_count + signature_size) * 2 / 3

    with tf.name_scope('fc2'):
        layer2 = tf.layers.dense(inputs=dropout1, units=l2_units, activation=tf.nn.relu, name="fc2")
        fc2_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, 'fc2')
        tf.summary.histogram('kernel2', fc2_vars[0])
        tf.summary.histogram('bias2', fc2_vars[1])
        tf.summary.histogram('act2', layer2)

        dropout2 = tf.layers.dropout(inputs=layer2, rate=dropout_rate, training=is_training)

    l3_units = (class_count + signature_size) / 3

    with tf.name_scope('fc3'):
        layer3 = tf.layers.dense(inputs=dropout2, units=l3_units, activation=tf.nn.relu, name="fc3")
        fc3_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, 'fc3')
        tf.summary.histogram('kernel3', fc3_vars[0])
        tf.summary.histogram('bias3', fc3_vars[1])
        tf.summary.histogram('act3', layer3)

        dropout3 = tf.layers.dropout(inputs=layer3, rate=dropout_rate, training=is_training)


    with tf.name_scope('fc4'):
        out = tf.layers.dense(inputs=dropout3, units=class_count, activation=tf.nn.relu, name="fc4")
        fc3_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, 'fc4')
        tf.summary.histogram('kernel4', fc3_vars[0])
        tf.summary.histogram('bias4', fc3_vars[1])
        tf.summary.histogram('act4', out)

    return out

