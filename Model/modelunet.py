from modelpartsunet import *
from keras.models import Model
import tensorflow as tf
from keras.layers import (Input, Reshape, Lambda, Conv2D, DepthwiseConv2D, BatchNormalization, Activation, MaxPool2D, 
                                     UpSampling2D,Dropout, Concatenate, Conv2DTranspose, dot, add)


class UNet(Model):
    def __init__(self, shape=(512,512,3), num_classes=3):
        super(UNet, self).__init__()
        self.num_classes = num_classes
        self.inputs = Input(shape)
        
        # Encoder
        self.x1, self.p1 = ResidualBlock(16)(self.inputs, pool=True)
        self.x2, self.p2 = ResidualBlock(32)(self.p1, pool=True)
        self.x3, self.p3 = ResidualBlock(64)(self.p2, pool=True)
        #drop3 = Dropout(0.1)(x3)
        self.x4, self.p4 = ResidualBlock(128)(self.p3, pool=True)
        #drop4 = Dropout(0.1)(x4)
        self.x5, self.p5 = ResidualBlock(256)(self.p4, pool=True)
        
        # Bridge
        self.fsm_out = FSMBlock()(self.p5)
        
        # Decoder
        self.u0 = Conv2DTranspose(256, (3,3), strides=(2,2), padding="same")(self.fsm_out)
        self.c0 = Concatenate()([self.u0, self.x5])
        self.x6 = ResidualBlock(256)(self.c0, pool=False)

        self.u1 = Conv2DTranspose(128, (3,3), strides=(2,2), padding="same")(self.x6)
        self.c1 = Concatenate()([self.u1, self.x4])
        self.x7 = ResidualBlock(128)(self.c1, pool=False)

        self.u2 = Conv2DTranspose(64, (3,3), strides=(2,2), padding="same")(self.x7)
        self.c2 = Concatenate()([self.u2, self.x3])
        self.x8 = ResidualBlock(64)(self.c2, pool=False)

        self.u3 = Conv2DTranspose(32, (3,3), strides=(2,2), padding="same")(self.x8)
        self.c3 = Concatenate()([self.u3, self.x2])
        self.x9 = ResidualBlock(32)(self.c3, pool=False)

        self.u4 = Conv2DTranspose(16, (3,3), strides=(2,2), padding="same")(self.x9)
        self.c4 = Concatenate()([self.u4, self.x1])
        self.x10 = ResidualBlock(16)(self.c4, pool=False)

        # Additional Layers
        self.fsm_out_new = ResidualBlock(64)(self.fsm_out, pool=False)
        self.x6_new = ResidualBlock(64)(self.x6, pool=False)
        self.x7_new = ResidualBlock(64)(self.x7, pool=False)
        self.x8_new = ResidualBlock(64)(self.x8, pool=False)
        self.x9_new = ResidualBlock(64)(self.x9, pool=False)
        self.x10_new = ResidualBlock(64)(self.x10, pool=False)

        self.fsm_out_new_transposed = Conv2DTranspose(64, (3,3), strides=(32,32))(self.fsm_out_new)
        self.x6_transposed = Conv2DTranspose(64, (3,3), strides=(16,16))(self.x6_new)  
        self.x7_transposed = Conv2DTranspose(64, (3,3), strides=(8,8))(self.x7_new)     
        self.x8_transposed = Conv2DTranspose(64, (3,3), strides=(4,4))(self.x8_new)  
        self.x9_transposed = Conv2DTranspose(64, (3,3), strides=(2,2), padding='same')(self.x9_new)
        self.x10_transposed = self.x10_new
    
        self.concat_output = Concatenate()([self.fsm_out_new_transposed, self.x6_transposed, 
                                             self.x7_transposed, self.x8_transposed, 
                                             self.x9_transposed, self.x10_transposed])
        
        # Output layer
        self.output = Conv2D(self.num_classes, 1, padding="same", activation="softmax")(self.concat_output)
