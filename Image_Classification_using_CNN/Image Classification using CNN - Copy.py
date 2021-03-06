# -*- coding: utf-8 -*-
"""riris.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AidnCfUp4MrTpRcThW0stqY1hoUZoAIw

#Import Module

---
"""

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import InputLayer, Flatten, Dense, Conv2D, MaxPool2D, Dropout
from tensorflow.keras.optimizers import Adam
import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt


"""#Load Dataset"""

imagePaths = 'Dataset/'
label_list = ['Jambu Biji', 'Sirih']
data = []
labels = []

for label in label_list:
    for imagePath in glob.glob(imagePaths+label+'/*.jpg'):
        #print(imagePath)
         image = cv2.imread(imagePath)
         image = cv2.resize(image, (32, 32))
         data.append(image)
         labels.append(label)

np.array(data).shape

"""#Data Processing"""

# ubah type data dari list menjadi array
# ubah nilai dari tiap pixel menjadi range [0..1]
data = np.array(data, dtype='float') / 255.0
labels = np.array(labels)

print(labels)

# ubah nilai dari labels menjadi binary\n",
lb = LabelEncoder()
labels = lb.fit_transform(labels)
print(labels)

"""#Split Dataset"""

x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

print('Ukuran data train =', x_train.shape)
print('Ukuran data test =', x_test.shape)

"""#Build CNN Architecture"""

model = Sequential()
# Extracted Feature Layer
model.add(InputLayer(input_shape=[32,32,3]))
model.add(Conv2D(filters=32, kernel_size=2, strides=1, padding='same', activation='relu'))
model.add(MaxPool2D(pool_size=2, padding='same'))
model.add(Conv2D(filters=50, kernel_size=2, strides=1, padding='same', activation='relu'))
model.add(MaxPool2D(pool_size=2, padding='same'))
model.add(Dropout(0.25))
model.add(Flatten())
# Fully Connected Layer
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))

model.summary()

# tentukan hyperparameter
lr = 0.001
max_epochs = 100
opt_funct = Adam(learning_rate=lr)

# compile arsitektur yang telah dibuat
model.compile(loss = 'binary_crossentropy',
                  optimizer = opt_funct,
                  metrics = ['accuracy'])

"""#Train Model"""

H = model.fit(x_train, y_train, validation_data=(x_test, y_test),
         epochs=max_epochs, batch_size=32)

N = np.arange(0, max_epochs)
plt.style.use("ggplot")
plt.figure()
plt.plot(N, H.history["loss"], label="train_loss")
plt.plot(N, H.history["val_loss"], label="val_loss")
#plt.plot(N, H.history["accuracy"], label="train_acc")
#plt.plot(N, H.history["val_accuracy"], label="val_acc")
plt.xlabel("Epoch #")
plt.legend()
plt.show()

"""#Evaluate the Model"""

# menghitung nilai akurasi model terhadap data test
predictions = model.predict(x_test, batch_size=32)
target = (predictions > 0.5).astype(np.int)
print(classification_report(y_test, target, target_names=label_list))

# uji model menggunakan image lain
queryPath = imagePaths+'002.jpg'
query = cv2.imread(queryPath)
output = query.copy()
query = cv2.resize(query, (32, 32))
q = []
q.append(query)
q = np.array(q, dtype='float') / 255.0
q_pred = model.predict(q)
print(q_pred)

if q_pred<=0.5 :
    target = "Jambu Biji"
else :
    target = "Sirih"
text = "{}".format(target)
cv2.putText(output, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
# menampilkan output image
# cv2_imshow(output)

model.save('cnn.h5')