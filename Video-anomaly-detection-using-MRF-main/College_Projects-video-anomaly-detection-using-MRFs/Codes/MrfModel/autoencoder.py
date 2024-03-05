import numpy as np
import cv2
from keras.layers import Input, Dense
from keras.models import Model
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint, EarlyStopping
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Assuming you have training frames without anomalies stored in a list called 'training_frames'
# and test frames with anomalies stored in a list called 'test_frames'

# Flatten each frame
flattened_training_frames = [frame.flatten() for frame in training_frames]
flattened_test_frames = [frame.flatten() for frame in test_frames]

# Convert the list of flattened frames to a numpy array
data_train = np.array(flattened_training_frames)
data_test = np.array(flattened_test_frames)

# Normalize the data to the range [0, 1]
data_train = data_train / 255.0
data_test = data_test / 255.0

# Split the training data into training and validation sets
X_train, X_val = train_test_split(data_train, test_size=0.1, random_state=42)

# Autoencoder architecture
input_dim = X_train.shape[1]
encoding_dim = 128
hidden_dim = 64

input_layer = Input(shape=(input_dim,))
encoded = Dense(encoding_dim, activation='relu')(input_layer)
encoded = Dense(hidden_dim, activation='relu')(encoded)
decoded = Dense(encoding_dim, activation='relu')(encoded)
decoded = Dense(input_dim, activation='sigmoid')(decoded)

autoencoder = Model(input_layer, decoded)

# Compile the model
optimizer = Adam(lr=0.001)
autoencoder.compile(optimizer=optimizer, loss='mean_squared_error')

# Model checkpoint to save the best model
checkpoint = ModelCheckpoint(
    "autoencoder_best_model.h5", save_best_only=True, verbose=1)
# Early stopping to stop training if the validation loss doesn't improve
early_stopping = EarlyStopping(
    monitor='val_loss', patience=5, restore_best_weights=True)

# Train the autoencoder
history = autoencoder.fit(
    X_train, X_train,
    epochs=50,
    batch_size=256,
    shuffle=True,
    validation_data=(X_val, X_val),
    callbacks=[checkpoint, early_stopping]
)

# Plot training history
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Mean Squared Error')
plt.legend()
plt.show()
