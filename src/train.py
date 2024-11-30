import matplotlib.pyplot as plt
import numpy as np
import PIL
import tensorflow as tf
import pathlib
import json

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
import tensorflowjs

def train(config, callbacks, saveModel=False):
  data_dir = pathlib.Path("data/training_data").with_suffix("")
  model_path = "data/models/item_classifier_model"
  class_names_path = "data/models/class_names.json"

  print("Number of images in data set: " + str(len(list(data_dir.glob("*/*.png")))))

  batch_size = 32
  img_width = 30
  img_height = 30

  train_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size)

  val_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size)

  class_names = train_ds.class_names

  train_ds = (train_ds
              .cache()
              .shuffle(1000)
              .prefetch(buffer_size=tf.data.AUTOTUNE))
  val_ds = (val_ds
            .cache()
            .prefetch(buffer_size=tf.data.AUTOTUNE))

  num_classes = len(class_names)

  kernal_size = (config['kernal_size'], config['kernal_size'])

  architecture = []
  architecture.append(layers.Input(shape=(img_height, img_width, 3)))
  architecture.append(layers.Rescaling(1./255))
  architecture.append(layers.Conv2D(config['filter_sizes'][0], kernal_size, activation=config['cnn_activation_function'], padding='same'))
  if config['pooling_strategy'] == 'max':
    architecture.append(layers.BatchNormalization())
    architecture.append(layers.MaxPooling2D((2, 2)))
  else:
    architecture.append(layers.AveragePooling2D())
  architecture.append(layers.Conv2D(config['filter_sizes'][1], kernal_size, activation=config['cnn_activation_function'], padding='same'))
  if config['pooling_strategy'] == 'max':
    architecture.append(layers.BatchNormalization())
    architecture.append(layers.MaxPooling2D((2, 2)))
  else:
    architecture.append(layers.AveragePooling2D())
  architecture.append(layers.Flatten())
  for _ in range(config['num_dense_layers']):
    architecture.append(layers.Dense(config['fc_layer_size'], activation=config['dense_activation_function']))
  architecture.append(layers.Dropout(config['dropout']))
  architecture.append(layers.Dense(num_classes, activation='softmax'))

  model = Sequential(architecture)

  optimizer = None
  if config['optimizer_name'] == 'adam':
    optimizer = tf.keras.optimizers.Adam(learning_rate=config['learning_rate'])
  else:
    optimizer = tf.keras.optimizers.SGD(learning_rate=config['learning_rate'])

  model.compile(optimizer=optimizer,
                loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                metrics=['accuracy'])

  model.summary()

  # Train
  history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=50,
    verbose=1,
    callbacks=callbacks
  )

  if saveModel:
    model.save('model.h5')
    
    print('Saving file to ' + model_path)
    tensorflowjs.converters.save_keras_model(model, model_path)
    with open(class_names_path, 'w', encoding='utf-8') as f:
        json.dump(class_names, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
   train({
    'learning_rate': 0.03660573315077385,
    'dropout': 0.5,
    'fc_layer_size': 256,
    'optimizer_name': 'SGD',
    'cnn_activation_function': 'softmax',
    'dense_activation_function': 'relu',
    'num_conv_layers': 2,
    'filter_sizes': [6, 16],
    'kernal_size': 3,
    'num_dense_layers': 1,
    'pooling_strategy': 'max',
   }, None, True)
