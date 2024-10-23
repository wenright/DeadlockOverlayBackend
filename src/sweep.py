# Trains the model using Weights & Biases. Usefull for sweeps

import train

from tensorflow import keras
import wandb

class WandbMetricsLogger(keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs=None):
    wandb.log(logs)

if __name__ == '__main__':
  wandb.init(
    # set the wandb project where this run will be logged
    project="my-awesome-project",
  )

  train.train(wandb.config, WandbMetricsLogger())

  wandb.finish()
