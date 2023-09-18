import tensorflow as tf
from keras.regularizers import l2
from keras import backend as K
from keras.layers import (Input, Reshape, Lambda, Conv2D, DepthwiseConv2D, BatchNormalization, Activation, MaxPool2D, 
                                     UpSampling2D,Dropout, Concatenate, Conv2DTranspose, dot, add)

class ResidualBlock(tf.keras.layers.Layer):
    def __init__(self, filters, pool=False):
        super(ResidualBlock, self).__init__()
        self.filters = filters
        self.pool = pool
    
    def build(self, input_shape):
        self.conv1 = Conv2D(self.filters, 3, padding="same", activation='relu')
        self.batch_norm1 = BatchNormalization()
        self.activation1 = Activation("relu")
        self.conv2 = Conv2D(self.filters, 3, padding="same")
        self.batch_norm2 = BatchNormalization()
        
        if self.pool:
        # self.addition = add
        # self.activation2 = Activation("relu")
            self.pooling = MaxPool2D((2, 2))

    def call(self, inputs):
        x = self.conv1(inputs)
        x = self.batch_norm1(x)
        x = self.activation1(x)
        res = x
        x = self.conv2(x)
        x = self.batch_norm2(x)
        x = add([res, x])
        x = Activation("relu")(x)

        if self.pool:
            x = self.pooling(x)
        
        return x

class DoubleConvBlock(tf.keras.layers.Layer):
    def __init__(self, filters, pool=True):
        super(DoubleConvBlock, self).__init__()
        self.conv1 = Conv2D(filters, 3, padding="same", activation='relu')
        self.batch_norm1 = BatchNormalization()
        self.activation1 = Activation("relu")
        self.conv2 = Conv2D(filters, 3, padding="same")
        self.batch_norm2 = BatchNormalization()
        self.activation2 = Activation("relu")
        self.pooling = MaxPool2D((2, 2)) if pool else None

    def call(self, inputs):
        x = self.conv1(inputs)
        x = self.batch_norm1(x)
        x = self.activation1(x)
        x = self.conv2(x)
        x = self.batch_norm2(x)
        x = self.activation2(x)

        if self.pooling is not None:
            p = self.pooling(x)
            return x, p
        else:
            return x


class SingleConvBlock(tf.keras.layers.Layer):
    def __init__(self, filters):
        super(SingleConvBlock, self).__init__()
        self.conv = Conv2D(filters, 3, padding="same", activation='relu')
        self.batch_norm = BatchNormalization()
        self.activation = Activation("relu")

    def call(self, inputs):
        x = self.conv(inputs)
        x = self.batch_norm(x)
        x = self.activation(x)
        return x
    
class FSMBlock(tf.keras.layers.Layer):
    def __init__(self):
        super(FSMBlock, self).__init__()

    def build(self, input_shape):
        channel_num = input_shape[-1]

        self.single_conv_block1 = SingleConvBlock(filters=int(channel_num // 2))
        self.single_conv_block2 = SingleConvBlock(filters=int(channel_num))

    def call(self, inputs):
        channel_num = inputs.shape[-1]
        res = inputs

        x = self.single_conv_block1(inputs)

        ip = x
        ip_shape = tf.shape(ip)
        batchsize, dim1, dim2, channels = ip_shape
        intermediate_dim = channels // 2
        if intermediate_dim < 1:
            intermediate_dim = 1

        # theta path
        theta = Conv2D(intermediate_dim, (1, 1), padding='same', use_bias=False, kernel_initializer='he_normal',
                       kernel_regularizer=l2(1e-5))(ip)
        theta = Reshape((-1, intermediate_dim))(theta)

        # phi path
        phi = Conv2D(intermediate_dim, (1, 1), padding='same', use_bias=False, kernel_initializer='he_normal',
                     kernel_regularizer=l2(1e-5))(ip)
        phi = Reshape((-1, intermediate_dim))(phi)

        # dot
        f = dot([theta, phi], axes=2)
        size = tf.shape(f)
        # scale the values to make it size invariant
        f = Lambda(lambda z: (1. / float(size[-1])) * z)(f)

        # g path
        g = Conv2D(intermediate_dim, (1, 1), padding='same', use_bias=False, kernel_initializer='he_normal',
                   kernel_regularizer=l2(1e-5))(ip)
        g = Reshape((-1, intermediate_dim))(g)

        # compute output path
        y = dot([f, g], axes=[2, 1])
        y = Reshape((dim1, dim2, intermediate_dim))(y)
        y = Conv2D(channels, (1, 1), padding='same', use_bias=False, kernel_initializer='he_normal',
                   kernel_regularizer=l2(1e-5))(y)
        y = add([ip, y])

        x = y
        x = self.single_conv_block2(x)
        x = add([x, res])

        return x




# def res_block(inputs, filters, pool=True):
#     x = Conv2D(filters, 3, padding="same", activation='relu')(inputs)
#     x = BatchNormalization()(x)
#     x = Activation("relu")(x)
#     res = x
#     x = Conv2D(filters, 3, padding="same")(x)
#     x = BatchNormalization()(x)
#     x = add([res, x])
#     x = Activation("relu")(x)

#     if pool == True:
#         p = MaxPool2D((2, 2))(x)
#         return x, p
#     else:
#         return x

# def double_conv_block(inputs, filters, pool=True):
#     x = Conv2D(filters, 3, padding="same", activation='relu')(inputs)
#     x = BatchNormalization()(x)
#     x = Activation("relu")(x)
    
# #     x = add([inputs_curr, x])
#     x = Conv2D(filters, 3, padding="same")(x)
#     x = BatchNormalization()(x)
#     x = Activation("relu")(x)

#     if pool == True:
#         p = MaxPool2D((2, 2))(x)
#         return x, p
#     else:
#         return x


# def conv_block(inputs_prev,inputs_curr, filters, pool=True):
#     x = Conv2D(filters, 3, padding="same", activation='relu')(inputs_prev)
#     x = BatchNormalization()(x)
# #     x = Activation("relu")(x)
    
#     x = add([inputs_curr, x])
# #     x = Conv2D(filters, 3, padding="same")(x)
# #     x = BatchNormalization()(x)
#     x = Activation("relu")(x)

#     if pool == True:
#         p = MaxPool2D((2, 2))(x)
#         return x, p
#     else:
#         return x
    
# def single_conv_block(inputs, filters):
    # x = Conv2D(filters, 3, padding="same", activation='relu')(inputs)
    # x = BatchNormalization()(x)
    # x = Activation("relu")(x)
    # return x
    
# def fsm(inputs):
#     channel_num = inputs.shape[-1]

#     res = inputs

#     inputs = single_conv_block(inputs, filters=int(channel_num // 2))

#     # x = non_local_block(x, compression=2, mode='dot')

#     ip = inputs
#     ip_shape = K.int_shape(ip)
#     batchsize, dim1, dim2, channels = ip_shape
#     intermediate_dim = channels // 2
#     rank = 4
#     if intermediate_dim < 1:
#         intermediate_dim = 1

#     # theta path
#     theta = Conv2D(intermediate_dim, (1, 1), padding='same', use_bias=False, kernel_initializer='he_normal',
#                    kernel_regularizer=l2(1e-5))(ip)
#     theta = Reshape((-1, intermediate_dim))(theta)

#     # phi path
#     phi = Conv2D(intermediate_dim, (1, 1), padding='same', use_bias=False, kernel_initializer='he_normal',
#                    kernel_regularizer=l2(1e-5))(ip)
#     phi = Reshape((-1, intermediate_dim))(phi)

#     # dot
#     f = dot([theta, phi], axes=2)
#     size = K.int_shape(f)
#     # scale the values to make it size invariant
#     f = Lambda(lambda z: (1. / float(size[-1])) * z)(f)

#     # g path
#     g = Conv2D(intermediate_dim, (1, 1), padding='same', use_bias=False, kernel_initializer='he_normal',
#                    kernel_regularizer=l2(1e-5))(ip)
#     g = Reshape((-1, intermediate_dim))(g)

#     # compute output path
#     y = dot([f, g], axes=[2, 1])
#     y = Reshape((dim1, dim2, intermediate_dim))(y)
#     y = Conv2D(channels, (1, 1), padding='same', use_bias=False, kernel_initializer='he_normal',
#                kernel_regularizer=l2(1e-5))(y)
#     y = add([ip, y])

#     x = y
#     x = single_conv_block(x, filters=int(channel_num))
#     print(x)

#     x = add([x, res])
#     return x