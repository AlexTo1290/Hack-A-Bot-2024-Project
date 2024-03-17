import tensorflow as tf
import keras
import numpy as np

EPOCHS = 10
LEARNING_RATE = 0.2
BATCH_SIZE = 32

TRAIN_SIZE = (720, 480)

# Data augmentation


#Hard coded for my computer change to be suitable to you
# data_dir = "C:\\Users\\Alex\\Documents\\Hackabot\\Spresense Hackabot\\Training Images"
data_dir = "Training Images - 258"

train_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="training",
    seed=42,
    image_size=(180, 180),
    batch_size = BATCH_SIZE,
    )

val_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="validation",
    seed=42,
    image_size=(180, 180),
    batch_size = BATCH_SIZE,
    )

test_ds = tf.keras.utils.image_dataset_from_directory(
    "Test",
    image_size=(180, 180),
    batch_size = BATCH_SIZE,
    )

def normalize(images, labels):
  images = tf.cast(images, tf.float32)
  images /= 255
  return images, labels

train_ds =  train_ds.map(normalize)
val_ds = val_ds.map(normalize)
test_ds = test_ds.map(normalize)

train_ds = train_ds.cache()
val_ds = val_ds.cache()
test_ds = val_ds.cache()


"""
model = tf.keras.Sequential([
    keras.layers.Resizing(*TRAIN_SIZE),
    keras.layers.Flatten(TRAIN_SIZE),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dropout(0.1),
    keras.layers.Dense(16, activation="softmax")
    ])
"""

num_classes = 5
L2regularizer = keras.regularizers.L2(0.005)

# Perprocessing
# model = tf.keras.Sequential([
#   #tf.keras.layers.Resizing(*TRAIN_SIZE),
#     tf.keras.layers.InputLayer(input_shape=(180, 180, 3)),
#   tf.keras.layers.Rescaling(1./255),
#   tf.keras.layers.Conv2D(16, kernel_size=(7, 7), strides=(1, 1), activation='relu', input_shape=(180, 180, 3), padding="valid"),
# #   tf.keras.layers.RandomFlip("horizontal_and_vertical"),
# #   tf.keras.layers.RandomRotation(0.2),
#     tf.keras.layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='valid'),
#     tf.keras.layers.Flatten(),
#     tf.keras.layers.Dense(150, activation='relu'),
#     # tf.keras.layers.Dense(10, activation='softmax'),
# ])

model = tf.keras.Sequential([
    #  tf.keras.layers.Rescaling(1./255),
  tf.keras.layers.InputLayer(input_shape=(180, 180, 3)),
  tf.keras.layers.Conv2D(16, kernel_size=(7, 7), strides=(1, 1), activation='relu', input_shape=(180, 180, 1), padding="valid"),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='valid'),
    tf.keras.layers.Conv2D(30, kernel_size=(3, 3), strides=(1, 1), activation='tanh', padding='valid'),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='valid'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(150, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax'),
])

model.compile(
    optimizer='adam',
    loss=tf.keras.losses.SparseCategoricalCrossentropy(),
    metrics=['accuracy']
    )

# train_ds = train_ds.cache().repeat().batch(BATCH_SIZE)

model.fit(train_ds, validation_data = val_ds, epochs=EPOCHS)
model.summary()


# # Evaluate the model on the validation dataset
val_loss, val_accuracy = model.evaluate(val_ds)

# Print the validation accuracy
print("Validation Accuracy:", val_accuracy)



# Convert the model to TensorFlow Lite



# for images, labels in train_ds.take(1):
#     numpy_images = images.numpy()
#     numpy_labels = labels.numpy()

"""
def representative_data_gen():
  for input_value in tf.data.Dataset.from_tensor_slices(numpy_images).batch(1).take(100):
    yield [input_value]


converter = tf.lite.TFLiteConverter.from_keras_model(model)

converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.representative_dataset = representative_data_gen
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.inference_input_type = tf.int8
converter.inference_output_type = tf.int8

tflite_model_quant = converter.convert()
"""
save_dir = "model.keras"
model.save(save_dir)

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
with open('model2.tflite', 'wb') as f:
   f.write(tflite_model)

# Test model
result = model.evaluate(test_ds)
print(result)
