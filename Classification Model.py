import tensorflow as tf
import keras
import numpy as np

EPOCHS = 5
LEARNING_RATE = 0.2
BATCH_SIZE = 32

TRAIN_SIZE = (252, 189)

#Hard coded for my computer change to be suitable to you
data_dir = "C:\\Users\\Alex\\Documents\\Hackabot\\Spresense Hackabot\\Training Images"
data_dir = "Training Images - 258"

train_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="training",
    seed=42,
    image_size=(252, 189),
    batch_size = BATCH_SIZE,
    )

val_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="validation",
    seed=42,
    image_size=(252, 189),
    batch_size = BATCH_SIZE,
    )

train_ds = train_ds.cache().prefetch(buffer_size=tf.data.AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=tf.data.AUTOTUNE)

"""
model = tf.keras.Sequential([
    keras.layers.Resizing(*TRAIN_SIZE),
    keras.layers.Flatten(TRAIN_SIZE),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dropout(0.1),
    keras.layers.Dense(16, activation="softmax")
    ])
"""

num_classes = 2

L2regularizer = keras.regularizers.L2(0.005)

model = tf.keras.Sequential([
  #tf.keras.layers.Resizing(*TRAIN_SIZE),
  tf.keras.layers.Rescaling(1./255),
  tf.keras.layers.Conv2D(32, 3, activation='relu', activity_regularizer=L2regularizer),
  tf.keras.layers.MaxPooling2D(),
  tf.keras.layers.Conv2D(32, 3, activation='relu', activity_regularizer=L2regularizer),
  tf.keras.layers.MaxPooling2D(),
  tf.keras.layers.Conv2D(32, 3, activation='relu', activity_regularizer=L2regularizer),
  tf.keras.layers.MaxPooling2D(),
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dense(num_classes)
])

model.compile(
    optimizer='adam',
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy']
    )


model.fit(train_ds, validation_data = val_ds, epochs=EPOCHS)
    

