import matplotlib.pyplot as plt
import numpy as np
import PIL
import tensorflow as tf
import pathlib

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential


data_dir = pathlib.Path("data/real_items").with_suffix("")
model_path = "data/models/item_classifier.keras"

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

model = Sequential([
  layers.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
  layers.Conv2D(16, (3, 3), activation='relu', padding='same'),
  layers.BatchNormalization(),
  layers.MaxPooling2D((2, 2)),
  # layers.Dropout(0.25),

  layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
  layers.BatchNormalization(),
  layers.MaxPooling2D((2, 2)),
  # layers.Dropout(0.25),

  layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
  layers.BatchNormalization(),
  layers.MaxPooling2D((2, 2)),
  # layers.Dropout(0.25),

  layers.Flatten(),
  
  layers.Dense(256, activation='relu'),
  layers.Dropout(0.5),
  layers.Dense(num_classes)
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.summary()

# Train
epochs=25
history = model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=epochs,
  verbose=1
)

print('Saving file to ' + model_path)
model.save(model_path)
np.save("data/models/class_names.npy", np.array(class_names))

# Model results summary
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(epochs)

# plt.figure(figsize=(8, 8))
# plt.subplot(1, 2, 1)
# plt.plot(epochs_range, acc, label='Training Accuracy')
# plt.plot(epochs_range, val_acc, label='Validation Accuracy')
# plt.legend(loc='lower right')
# plt.title('Training and Validation Accuracy')

# plt.subplot(1, 2, 2)
# plt.plot(epochs_range, loss, label='Training Loss')
# plt.plot(epochs_range, val_loss, label='Validation Loss')
# plt.legend(loc='upper right')
# plt.title('Training and Validation Loss')
# plt.show()

val_images = []
val_labels = []

# Iterate through the dataset to collect images and labels
for images, labels in val_ds:
    val_images.append(images.numpy())  # Convert to NumPy array
    val_labels.append(labels.numpy())  # Convert to NumPy array

# Concatenate the batch results to get the full validation set
val_images = np.concatenate(val_images)
val_labels = np.concatenate(val_labels)

# Run predictions on the validation images
val_predictions = model.predict(val_images)

# Convert predictions from probabilities to class indices (if using softmax output)
predicted_classes = np.argmax(val_predictions, axis=1)

# Convert true labels to class indices if they are one-hot encoded
# Otherwise, `val_labels` are likely already in integer format
true_classes = val_labels  # Use directly if they are in integer form

# Find where the predictions don't match the true labels
misclassified_indices = np.where(predicted_classes != true_classes)[0]

# Optionally, you can count misclassified instances per class
from collections import Counter
misclassified_classes = true_classes[misclassified_indices]
misclassified_count = Counter(misclassified_classes)
print("Misclassified classes and their counts:", misclassified_count)

for mis in misclassified_classes:
    print(class_names[mis])

import matplotlib.pyplot as plt

# Display some of the misclassified images
num_display = 5  # Number of misclassified images to display
for i in range(min(num_display, len(misclassified_indices))):
    idx = misclassified_indices[i]
    plt.imshow(val_images[idx].astype("uint8"))  # Ensure images are in uint8 format for display
    plt.title(f"True: {class_names[true_classes[idx]]}, Predicted: {class_names[predicted_classes[idx]]}")
    plt.show(block=True)
