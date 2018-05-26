#!/usr/bin/python
'''
Author: SARBAJIT MUKHERJEE
Email: sarbajit.mukherjee@aggiemail.usu.edu

$python ConvNet3.py > saved_model/ConvNet3.txt
This code generates the audio classifcation model without the custom layer and replaces it with 
two hidden layers, a batch normalization layer, a FC layer with 256 neurons and a dropout of 0.5.
Also replace the 'n' in the first layer with your choice of filter size. 
In this paper we used 3,10,30,80,100
'''

from tflearn.layers.estimator import regression
import pydub
pydub.AudioSegment.ffmpeg = '/usr/bin/ffmpeg'
import pickle
import tflearn
from tflearn.layers.core import input_data,fully_connected,dropout
from tflearn.layers.normalization import batch_normalization
import utility


pickle_path = 'pickle/'
############Loading from pickle#############################
f = open(pickle_path + 'train_data.pickle')
X = pickle.load(f)
f.close()

f = open(pickle_path + 'train_labels.pickle')
Y = pickle.load(f)
f.close()

###########################################################

AUDIO_LENGTH = 20000

network1 = input_data(shape=[None,AUDIO_LENGTH,1])
#replace filter_size 'n' with your choice of size
network2 = tflearn.layers.conv.conv_1d (network1,
                             nb_filter=256,
                             filter_size='n',
                             strides=4,
                             padding='same',
                             activation='relu',
                             bias=True,
                             weights_init='xavier',
                             bias_init='zeros',
                             regularizer='L2',
                             weight_decay=0.0001,
                             trainable=True,
                             restore=True,
                             reuse=False,
                             scope=None,
                             name='Conv1D_1')
network3 = batch_normalization(network2)
network4 = tflearn.layers.conv.max_pool_1d(network3,kernel_size=4,strides=None)
network5 = tflearn.layers.conv.conv_1d (network4,
                             nb_filter=256,
                             filter_size=3,
                             strides=1,
                             padding='same',
                             activation='relu',
                             bias=True,
                             weights_init='xavier',
                             bias_init='zeros',
                             regularizer='L2',
                             weight_decay=0.0001,
                             trainable=True,
                             restore=True,
                             reuse=False,
                             scope=None,
                             name='Conv1D_2')
network6 = batch_normalization(network5)
network7 = tflearn.layers.conv.max_pool_1d(network6,kernel_size=4,strides=None)

########
network8 = tflearn.layers.conv.conv_1d (network7,
                             nb_filter=256,
                             filter_size=3,
                             strides=1,
                             padding='same',
                             activation='relu',
                             bias=True,
                             weights_init='xavier',
                             bias_init='zeros',
                             regularizer='L2',
                             weight_decay=0.0001,
                             trainable=True,
                             restore=True,
                             reuse=False,
                             scope=None,
                             name='Conv1D_3')
network9 = tflearn.layers.conv.conv_1d (network8,
                             nb_filter=256,
                             filter_size=3,
                             strides=1,
                             padding='same',
                             activation='relu',
                             bias=True,
                             weights_init='xavier',
                             bias_init='zeros',
                             regularizer='L2',
                             weight_decay=0.0001,
                             trainable=True,
                             restore=True,
                             reuse=False,
                             scope=None,
                             name='Conv1D_4')
network10 = batch_normalization(network9)
########

network11 = fully_connected(network10,256,activation='softmax')
network12 = dropout(network11,0.5)
network13 = fully_connected(network12,3,activation='softmax')
network14 = regression(network13, optimizer='adam',
                       loss='categorical_crossentropy',learning_rate=0.0001)

model = tflearn.DNN(network14, tensorboard_verbose=2)
model.fit(X, Y, n_epoch=100, validation_set=0.3, snapshot_step=400, shuffle= True,
          show_metric=True, batch_size=128,run_id='ConvNet3')

model.save('saved_model/ConvNet3')