import tensorflow as tf
from keras.layers import (Input, Reshape, Lambda, Conv2D, DepthwiseConv2D, BatchNormalization, Activation,
                          MaxPool2D, UpSampling2D, Dropout, Concatenate, Conv2DTranspose, dot, add)
from keras.models import Model
from keras.regularizers import L2
from keras import backend as K

class UNetBuilder:
    @staticmethod
    def build_unet(shape, num_classes):
        inputs = Input(shape)
        x1, p1 = UNetBuilder.res_block(inputs, 16, pool=True)
        x2, p2 = UNetBuilder.res_block(p1, 32, pool=True)
        x3, p3 = UNetBuilder.res_block(p2, 64, pool=True)
        x4, p4 = UNetBuilder.res_block(p3, 128, pool=True)
        x5, p5 = UNetBuilder.res_block(p4, 256, pool=True) 
        
        fsm_out = UNetBuilder.fsm(p5)
        
        u0 = Conv2DTranspose(256, (3,3), strides = (2,2), padding="same")(fsm_out)
        c0 = Concatenate()([u0, x5])
        x6 = UNetBuilder.res_block(c0, 256, pool=False)

        u1 = Conv2DTranspose(128, (3,3), strides = (2,2), padding="same")(x6)
        c1 = Concatenate()([u1, x4])
        x7 = UNetBuilder.res_block(c1, 128, pool=False)

        u2 = Conv2DTranspose(64, (3,3), strides = (2,2), padding="same")(x7)
        c2 = Concatenate()([u2, x3])
        x8 = UNetBuilder.res_block(c2, 64, pool=False)

        u3 = Conv2DTranspose(32, (3,3), strides = (2,2), padding="same")(x8)
        c3 = Concatenate()([u3, x2])
        x9 = UNetBuilder.res_block(c3, 32, pool=False)

        u4 = Conv2DTranspose(16, (3,3), strides = (2,2), padding="same")(x9)
        c4 = Concatenate()([u4, x1])
        x10 = UNetBuilder.res_block(c4, 16, pool=False)

        fsm_out_new = UNetBuilder.res_block(fsm_out, 64, pool=False) 
        x6_new = UNetBuilder.res_block(x6, 64, pool=False)            
        x7_new = UNetBuilder.res_block(x7, 64, pool=False)              
        x8_new = UNetBuilder.res_block(x8, 64, pool=False)            
        x9_new = UNetBuilder.res_block(x9, 64, pool=False)            
        x10_new = UNetBuilder.res_block(x10, 64, pool=False)         
    
        fsm_out_new_transposed = Conv2DTranspose(64, (3,3), strides = (32,32))(fsm_out_new)
        x6_transposed = Conv2DTranspose(64, (3,3), strides = (16,16))(x6_new)  
        x7_transposed = Conv2DTranspose(64, (3,3), strides = (8,8))(x7_new)     
        x8_transposed = Conv2DTranspose(64, (3,3), strides = (4,4))(x8_new)  
        x9_transposed = Conv2DTranspose(64, (3,3), strides = (2,2), padding='same')(x9_new)
        x10_transposed = x10_new
    
        concat_output = Concatenate()([fsm_out_new_transposed, x6_transposed, x7_transposed, x8_transposed, x9_transposed, x10_transposed])

        output = Conv2D(num_classes, 1, padding="same", activation="softmax")(concat_output)

        return Model(inputs, output)
    
    @staticmethod
    def res_block(inputs, filters, pool=True):
        x = Conv2D(filters, 3, padding="same", activation='relu')(inputs)
        x = BatchNormalization()(x)
        x = Activation("relu")(x)
        res = x
        x = Conv2D(filters, 3, padding="same")(x)
        x = BatchNormalization()(x)
        x = add([res, x])
        x = Activation("relu")(x)

        if pool == True:
            p = MaxPool2D((2, 2))(x)
            return x, p
        else:
            return x
    
    @staticmethod
    def double_conv_block(inputs, filters, pool=True):
        x = Conv2D(filters, 3, padding="same", activation='relu')(inputs)
        x = BatchNormalization()(x)
        x = Activation("relu")(x)
        x = Conv2D(filters, 3, padding="same")(x)
        x = BatchNormalization()(x)
        x = Activation("relu")(x)

        if pool == True:
            p = MaxPool2D((2, 2))(x)
            return x, p
        else:
            return x
    
    @staticmethod
    def single_conv_block(inputs, filters):
        x = Conv2D(filters, 3, padding="same", activation='relu')(inputs)
        x = BatchNormalization()(x)
        x = Activation("relu")(x)
        return x
    
    @staticmethod
    def fsm(inputs):
        channel_num = inputs.shape[-1]

        res = inputs

        inputs = UNetBuilder.single_conv_block(inputs, filters=int(channel_num // 2))
        ip = inputs
        ip_shape = K.int_shape(ip)
        batchsize, dim1, dim2, channels = ip_shape
        intermediate_dim = channels // 2
        rank = 4
        if intermediate_dim < 1:
            intermediate_dim = 1

        theta = Conv2D(intermediate_dim, (1, 1), padding='same', use_bias=False, kernel_initializer='he_normal',
                        kernel_regularizer=L2(1e-5))(ip)
        theta = Reshape((-1, intermediate_dim))(theta)

        phi = Conv2D(intermediate_dim, (1, 1), padding='same', use_bias=False, kernel_initializer='he_normal',
                    kernel_regularizer=L2(1e-5))(ip)
        phi = Reshape((-1, intermediate_dim))(phi)

        f = dot([theta, phi], axes=2)
        size = K.int_shape(f)
        f = Lambda(lambda z: (1. / float(size[-1])) * z)(f)

        g = Conv2D(intermediate_dim, (1, 1), padding='same', use_bias=False, kernel_initializer='he_normal',
                   kernel_regularizer=L2(1e-5))(ip)
        g = Reshape((-1, intermediate_dim))(g)

        y = dot([f, g], axes=[2, 1])
        y = Reshape((dim1, dim2, intermediate_dim))(y)
        y = Conv2D(channels, (1, 1), padding='same', use_bias=False, kernel_initializer='he_normal',
                    kernel_regularizer=L2(1e-5))(y)
        y = add([ip, y])

        x = y
        x = UNetBuilder.single_conv_block(x, filters=int(channel_num))
        print(x)

        x = add([x, res])
        return x