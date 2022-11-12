import tensorflow as tf

INPUT_SHAPE = (300,)
INPUT_SHAPE_FIX = (226,)
INPUT_SHAPE_WITH_HEAD = (2172,)


def get_model_coord_dense_1(input_shape, num_classes):
    MODEL_COORD_DENSE = tf.keras.Sequential(
        [
            tf.keras.layers.Dense(128, activation="relu", input_shape=input_shape),
            tf.keras.layers.Dense(64, activation="relu"),
            tf.keras.layers.Dense(num_classes, activation="softmax"),
        ]
    )
    return MODEL_COORD_DENSE


def get_model_coord_dense_2(input_shape, num_classes):
    MODEL_COORD_DENSE = tf.keras.Sequential(
        [
            tf.keras.layers.Dense(128, activation="relu", input_shape=input_shape),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(64, activation="relu"),
            tf.keras.layers.Dense(num_classes, activation="softmax"),
        ]
    )
    return MODEL_COORD_DENSE


def get_model_coord_dense_3(input_shape, num_classes):
    MODEL_COORD_DENSE = tf.keras.Sequential(
        [
            tf.keras.layers.Dense(128, activation="relu", input_shape=input_shape),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(64, activation="relu", kernel_regularizer=tf.keras.regularizers.l2(0.01)),
            tf.keras.layers.Dense(num_classes, activation="softmax"),
        ]
    )
    return MODEL_COORD_DENSE


def get_model_coord_dense_4(input_shape, num_classes):
    MODEL_COORD_DENSE = tf.keras.Sequential(
        [
            tf.keras.layers.Dense(128, activation="relu", input_shape=input_shape),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(
                64, activation="relu", kernel_regularizer=tf.keras.regularizers.L1L2(l1=0.01, l2=0.01)
            ),
            tf.keras.layers.Dense(num_classes, activation="softmax"),
        ]
    )
    return MODEL_COORD_DENSE
