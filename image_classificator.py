from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Flatten, Dense, Dropout
from keras.preprocessing.image import ImageDataGenerator

import time
import json

IMG_SIZE = 75
NB_CHANNELS = 3
BATCH_SIZE = 32
NB_TRAIN_IMG = 1800
NB_VALID_IMG = 600

train_datagen = ImageDataGenerator(
    rotation_range = 40,
    width_shift_range = 0.2,
    height_shift_range = 0.2,
    rescale = 1./255,
    shear_range = 0.2,
    zoom_range = 0.2,   
    horizontal_flip = True)

validation_datagen = ImageDataGenerator(rescale = 1./255)

train_generator = train_datagen.flow_from_directory(
    'data/train',
    target_size=(IMG_SIZE,IMG_SIZE),
    class_mode='binary',
    batch_size = BATCH_SIZE)

validation_generator = validation_datagen.flow_from_directory(
    'data/test',
    target_size=(IMG_SIZE,IMG_SIZE),
    class_mode='binary',
    batch_size = BATCH_SIZE)

cnn = Sequential()

cnn.add(Conv2D(filters=32, 
               kernel_size=(2,2), 
               strides=(1,1),
               padding='same',
               input_shape=(IMG_SIZE,IMG_SIZE,NB_CHANNELS),
               data_format='channels_last'))
cnn.add(Activation('relu'))
cnn.add(MaxPooling2D(pool_size=(2,2),
   strides=2))

cnn.add(Dropout(0.4))

cnn.add(Conv2D(filters=64,
               kernel_size=(2,2),
               strides=(1,1),
               padding='valid'))
cnn.add(Activation('relu'))
cnn.add(MaxPooling2D(pool_size=(2,2),
   strides=2))

cnn.add(Flatten())        
cnn.add(Dense(64))
cnn.add(Activation('relu'))

cnn.add(Dropout(0.4))

cnn.add(Dense(1))
cnn.add(Activation('sigmoid'))

cnn.compile(loss = 'binary_crossentropy', 
            optimizer = 'rmsprop', metrics = ['accuracy'])

start = time.time()
cnn.fit_generator(
    train_generator,
    steps_per_epoch=NB_TRAIN_IMG//BATCH_SIZE,
    epochs=50,
    validation_data=validation_generator,
    validation_steps=NB_VALID_IMG//BATCH_SIZE)
end = time.time()
print('Processing time:', (end - start)/60)

cnnjson = cnn.to_json()
with open("cnn.json", "w") as json_file:
    json.dump(cnnjson, json_file)

cnn.save_weights('cnn.h5')