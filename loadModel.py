import tensorflow as tf
import keras
import numpy as np

model = keras.models.load_model("model.keras")

"""
data_dir = "Test"
test_ds = tf.keras.utils.image_dataset_from_directory(
     data_dir,
     seed=42,
     image_size=(180, 180),
        batch_size=32,
 )
"""
data_dir = "Training Images - 258"
BATCH_SIZE=32
train_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="training",
    seed=42,
    image_size=(180, 180),
    batch_size = BATCH_SIZE,
    )
"""
val_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="validation",
    seed=42,
    image_size=(180, 180),
    batch_size = BATCH_SIZE,
    )
"""

tf_callable = tf.function(
    model.call,
    autograph=False,
    input_signature=[tf.TensorSpec((1, 180, 180, 3), tf.float32)],
    )

tf_concrete_function = tf_callable.get_concrete_function()
converter = tf.lite.TFLiteConverter.from_concrete_functions(
    [tf_concrete_function], tf_callable
    )
tflite_model = converter.convert()


# new_model = tf.keras.models.load_model('model.keras')

# # Save the model in a file
with open('model.tflite', 'wb') as f:
   f.write(tflite_model)

