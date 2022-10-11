import tensorflow as tf


def get_resnet50_adapted_model(num_classes):
    model = tf.keras.applications.ResNet50(weights="imagenet", include_top=False)
    x = model.output
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    predictions = tf.keras.layers.Dense(num_classes, activation="softmax")(x)
    model = tf.keras.Model(inputs=model.input, outputs=predictions)
    return model
