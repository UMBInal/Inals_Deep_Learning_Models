import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import numpy as np

# Load the MNIST dataset
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# Normalize the data to the range [0, 1]
x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0

# Reshape the data to include the channel dimension
x_train = np.expand_dims(x_train, axis=-1)
x_test = np.expand_dims(x_test, axis=-1)

# Define the Encoder
input_img = keras.Input(shape=(28, 28, 1))
x = keras.layers.Flatten()(input_img)
x = keras.layers.Dense(128, activation='relu')(x)
latent_space = keras.layers.Dense(64, activation='relu')(x)

# Define the Decoder
x = keras.layers.Dense(128, activation='relu')(latent_space)
x = keras.layers.Dense(28 * 28, activation='sigmoid')(x)
output_img = keras.layers.Reshape((28, 28, 1))(x)

# Combine Encoder and Decoder into an Autoencoder model
autoencoder = keras.Model(input_img, output_img)

# Compile the Autoencoder model
autoencoder.compile(optimizer='adam', loss='mse')

# Show the model architecture
autoencoder.summary()

# Train the Autoencoder
history = autoencoder.fit(
    x_train, x_train,
    epochs=10,
    batch_size=128,
    validation_split=0.1
)

# Select a test image
test_img = x_test[0]

# Reshape the test image for the model input
test_img_input = np.expand_dims(test_img, axis=0)

# Get the Autoencoder's output
reconstructed_img = autoencoder.predict(test_img_input)

# Display the original image
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.title("Original Image")
plt.imshow(test_img.squeeze(), cmap='gray')

# Display the reconstructed image
plt.subplot(1, 2, 2)
plt.title("Reconstructed Image")
plt.imshow(reconstructed_img.squeeze(), cmap='gray')
plt.show()
