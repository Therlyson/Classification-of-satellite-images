# -*- coding: utf-8 -*-
"""classificação satélite.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15KktbuR4pI9-C7CLfBZ-_AeZo7uwosNs
"""

from google.colab import drive
drive.mount('/content/drive')

import os
import cv2
import numpy as np
from google.colab.patches import cv2_imshow
import matplotlib.pyplot as plt
import tensorflow as tf
from google.colab import files
from keras.utils import to_categorical
import sklearn
from sklearn.metrics import classification_report

from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense,Input, Dropout, GlobalAveragePooling2D
from tensorflow.keras.models import Sequential
import zipfile

path = "/content/drive/MyDrive/DATASETS/satelite.zip"
zip_object = zipfile.ZipFile(file=path, mode='r')
zip_object.extractall('./')
zip_object.close()

imagem_cloudy = "/content/data/cloudy/train_12.jpg"
img = cv2.imread(imagem_cloudy)
if img is not None:
    print("Imagem carregada com sucesso.\n")
else:
    print("Não foi possível carregar a imagem.") #problema no caminho

cv2_imshow(img)

"""# Carregando o dataset

"""

images = []
labels = []
g = []

ROOT = "/content/data/"
for root, dirs, files in os.walk(ROOT):
  for f in files:
    # Converte o nome do arquivo para minúsculas antes de verificar a extensão
    if f.lower().endswith(("jpg", "jpeg")):
      img = cv2.imread(os.path.join(root, f))
      img = cv2.resize(img, (128,128))
      img = img/255
      images.append(img)
      if "train" in f:
        labels.append(0)
      elif "desert" in f:
        labels.append(1)
      elif "Forest" in f:
        labels.append(2)
      elif "SeaLake" in f:
        labels.append(3)

print(f'Qtd de images: {len(images)}')
print(f'Qtd de labels: {len(labels)}')

n = 0
plt.imshow(images[n])
print(labels[n])

X = np.array(images)

y = to_categorical(labels, num_classes=4)
print(y)

X.shape, y.shape

n = 4500
plt.imshow(X[n])
print(y[n])

"""# DIVISÃO DE DADOS

"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle = True)  #shuffle = True: embaralha os dados
print(len(X_train))
print(len(y_train))
print(len(X_test))
print(len(y_test))

n = 0
cv2_imshow(X_train[n]*255)
print(y_train[n])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle = True) #shuffle = True: embaralha os dados novamente, para não embaralhar basta shuffle = False.

n = 0
cv2_imshow(X_train[n]*255)
print(y_train[n])

"""# CONSTRUÇÃO DO MODELO

"""

def buildModel():
  network = Sequential()
  network.add(Conv2D(32, (3,3), input_shape=(128,128,3), activation='relu', padding='same'))
  network.add(MaxPooling2D(pool_size=(2,2)))
  network.add(Conv2D(64, (3,3), activation='relu', padding = 'same'))
  network.add(MaxPooling2D(pool_size=(2,2)))
  network.add(Conv2D(128, (3,3), activation='relu', padding = 'same'))
  network.add(MaxPooling2D(pool_size=(2,2)))
  network.add(Conv2D(256, (3,3), activation='relu', padding = 'same'))
  network.add(MaxPooling2D(pool_size=(2,2)))
  network.add(Flatten())
  network.add(Dense(units=32, activation='relu'))
  network.add(Dropout(0.3)) #30% dos neurônios serão aleatoriamente desativados durante o treinamento.
  network.add(Dense(units=4, activation='softmax')) #configurando para produzir saídas com quatro unidades na última camada, números de unidades da camada de saida tem que ser igual aos números de classes do problema
  return network

model = buildModel()

model.summary()

"""# EXPERIMENTAÇÃO

"""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True, stratify=y)

X_train.shape, y_train.shape

X_test.shape, y_test.shape

model.compile(optimizer='adam', loss = 'categorical_crossentropy', metrics = ['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()])

historico = model.fit(X_train, y_train, validation_split=0.1, batch_size=32, epochs=10)

predicoes = model.predict(X_test) # predicoes é uma matriz de probabilidades, onde cada linha corresponde a uma imagem de teste e cada coluna corresponde a uma classe

predicoes = np.argmax(predicoes, axis=1);

print(y_test)

y_test = np.argmax(y_test, axis=1)

print(y_test)

print(classification_report(y_test, predicoes))

"""## Holdout

"""