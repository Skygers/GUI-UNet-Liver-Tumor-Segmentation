import sys
import matplotlib.pyplot as plt
from PySide6.QtWidgets import QMainWindow, QWidget, QFileDialog, QMessageBox
from PySide6.QtGui import QImage, QPixmap
import cv2
import pyqtgraph as pg
from pyqtgraph.exporters import ImageExporter
import numpy as np
from Model.modelunet import UNet
from Model.modelpartsunet import *
from Model.Unetmodel import UNetBuilder
import tensorflow as tf
from keras import backend as K
from Ui_autosegApps import Ui_MainWindow
import random
from PIL import Image, ImageOps
import tifffile as tiff

class Segtumor(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.segmentation_predict = None
        self.open_image_button.clicked.connect(self.openimage)
        self.autosegmentation_button.clicked.connect(self.autosegment)
        self.reset_button.clicked.connect(self.reset)
        self.analysis_button.clicked.connect(self.analysis)
    
    def reset(self):
        self.ctscan2_imgview.clear()
        self.ctscan_imgview.clear()
        self.segmentation_imgview.clear()
        self.overlayer_imgview.clear()
    
    def cleanimage(self):
        self.ctscan2_imgview.clear()
        self.ctscan_imgview.clear()
    
    def analysis(self):
        self.ctscan_imgview.ui.histogram.show()
        self.ctscan2_imgview.ui.histogram.show()
        self.segmentation_imgview.ui.histogram.show()
        self.overlayer_imgview.ui.histogram.show()
        self.ctscan_imgview.ui.roiBtn.show()
        self.ctscan2_imgview.ui.roiBtn.show()
        self.segmentation_imgview.ui.roiBtn.show()
        self.overlayer_imgview.ui.roiBtn.show()
    

    def openimage(self):
        options = QFileDialog.Option()
        options |= QFileDialog.ReadOnly
        filedialog = QFileDialog(self, "Select Image", "", "Image Files (*.jpg *.jpeg *.png);;All Files (*)", options=options)
        filedialog.setFileMode(QFileDialog.ExistingFile)

        if filedialog.exec_():
            selectedfile = filedialog.selectedFiles()[0]
            self.image_path = selectedfile
            self.read_image(self.image_path)

    def autosegment(self):
        if not self.image_path:
            #QMessageBox.information(self, "Error", "Segmentation Predict is None")
            return
        
        print(self.image_path)
        def dicecoef(y_true, y_pred, smooth=1):
            y_true = tf.cast(y_true, tf.float32)
            y_pred = tf.cast(y_pred, tf.float32)
            intersection = K.sum(K.abs(y_true*y_pred), axis=-1)
            return (2. * intersection+smooth)/(K.sum(K.square(y_true),-1)+K.sum(K.square(y_pred),-1)+smooth)
        
        def dicecoef_loss(y_true,y_pred):
            return 1-dicecoef(y_true, y_pred)
        
        try:
            np.random.seed(42)
            tf.random.set_seed(42)

            model = UNetBuilder.build_unet(shape=(512,512,3), num_classes=3)
            model.compile(loss=dicecoef_loss, optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
                      metrics=[dicecoef])
            model.load_weights('Model/final_model7.h5')
            image = self.convertimage(self.image_path)
            predict = model.predict(np.expand_dims(image, axis=0))[0]
            if predict is None or len(predict) == 0:
                QMessageBox.information(self, "Error", "Model prediction failed or returned an empty result")
                return
            predict = np.argmax(predict, axis=-1)
            print(np.unique(predict, return_counts=True))
            predict = np.expand_dims(predict, axis=-1)
            predict = predict.astype(np.int32)
            predict = np.squeeze(predict, axis=-1)
            img = Image.fromarray(predict.astype('uint8'), mode='L')
            img.save('output/segment.tiff')
            self.read_segmentation(self.segmentationpath)
            self.overlay(self.image_path, self.segmentationpath2)
            self.show_overlay(self.overlaypath)
        except Exception as e:
            print("An Error Occured:", str(e))
    
    def overlay(self, imagepath, segmentationpath):
        ct_image = Image.open(imagepath)
        seg_image = Image.open(segmentationpath)
        if ct_image.size != seg_image.size:
            seg_image = seg_image.resize(ct_image.size)
        ct_image = ct_image.convert('RGBA')
        seg_image = seg_image.convert('RGBA')
        ct_image = ImageOps.mirror(ct_image)
        ct_image = ct_image.rotate(90)

        alpha = 0.5
        overlay_img = Image.blend(ct_image, seg_image, alpha)
        overlay_img.save('output/overlay.png', 'PNG')

    def show_overlay(self, imagepath):
        original_img = Image.open(imagepath)
        overlay_array = np.array(original_img)
        overlay_array = overlay_array.astype(np.uint8)
        self.overlayer_imgview.setImage(overlay_array)

    def export_overlay_image(self):
        if self.overlayer_imgview is not None:
            exporter = ImageExporter(self.overlayer_imgview)
            exporter.parameters()['width'] = 800
            exporter.parameters()['height']=600
            exporter.parameters()['dpi']=100
            exporter.export(fileName='overlay_export.png')
        else:
            print('No image to export.')

    def read_image(self, imagepath):
        image = self.convertimage(imagepath)
        if image is not None:
            self.ctscan_imgview.setImage(image, autoRange=True, autoLevels=True, autoHistogramRange=True)
            self.ctscan2_imgview.setImage(image, autoRange=True, autoLevels=True, autoHistogramRange=True)
        
        else:
            self.ctscan_imgview.clear()
            self.ctscan2_imgview.clear()
            QMessageBox.information(self, "Berkas bukan termasuk citra", "Tolong masukkan citra dalam bentuk JPG, JPG, atau PNG")
    
    def read_segmentation(self, segmentationpath):
        segmentationimg = tiff.imread(segmentationpath)
        self.segmentation_imgview.setImage(segmentationimg, autoHistogramRange=True, autoLevels=True, autoRange=True)
        self.segmentation_imgview.export('output/segment.jpg')

    def convertimage(self, imagepath):
        cvimg = cv2.imread(imagepath, cv2.IMREAD_COLOR)
        cvimg = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
        cvimg = cvimg/255.0
        cvimg = cvimg.astype(np.float32)
        return cvimg
    
    def convertmask(self, imagepath):
        cvmask = cv2.imread(imagepath, cv2.IMREAD_GRAYSCALE)
        cvmask = cvmask.astype(np.int32)
        return cvmask
        
