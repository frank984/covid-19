#!/usr/bin/python
# -*- encoding: utf-8 -*-

"""
@ide: PyCharm
@author: Pedro Silva
@contact: pedroh21.silva@gmail.com
@created: abr-02 of 2020
"""

# Model definition
import keras.applications as ka

# For model plot purposes
from keras import Model
from keras.layers import Dropout, Conv2D, Reshape, Activation, Dense, Flatten
from keras.utils import plot_model

from covid19.models.base_model import BaseModel


class MobileNetV2(BaseModel):
    def __init__(self, use_weights=True, custom_weights_path=None, use_regularization=False, regularizer=None):
        self._use_weights = use_weights
        self._custom_weights = custom_weights_path
        self._use_regularization = use_regularization
        self._regularizer = regularizer
        self._model_name = '/media/data/Profissional/Doc/KerasModels/mobilenetv2.h5'
        self._input_shape = (224, 224, 3)

    def create_net(self, _number_of_classes=3, _output_path=None):

        if self._use_weights:
            if self._custom_weights is None:
                weights = 'imagenet'
            else:
                weights = self._custom_weights
        else:
            weights = None

        base_model = ka.mobilenet_v2.MobileNetV2(
            input_shape=self._input_shape,
            weights=weights)

        print(base_model.summary())

        model = Model(inputs=base_model.input, outputs=base_model.get_layer('global_average_pooling2d_1').output)
        # model = Model(inputs=input_image, outputs=base_model.get_layer('pool1').output)

        x = model.output
        # x = Dropout(1e-3, name='dropout')(x)
        # x = Flatten()(x)
        x = Dense(4096, activation='relu')(x)
        x = Dense(4096, activation='relu')(x)
        x = Dense(_number_of_classes, activation='softmax')(x)

        base_model = Model(inputs=base_model.input, outputs=x)

        if self._use_regularization:
            base_model = self.add_regularization(base_model, regularizer=self._regularizer)

        print(base_model.summary())

        if _output_path is not None:
            plot_model(base_model, to_file=_output_path + '/model_base_network.png', show_shapes=True, show_layer_names=True)

        return base_model

    def get_input_size(self):
        return self._input_shape

    def get_net_name(self):
        return 'MobileNetV2'
