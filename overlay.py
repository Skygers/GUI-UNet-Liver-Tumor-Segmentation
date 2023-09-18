import sys
import numpy as np
import cv2
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QImage


def load_image(image_path, target_size=None):
    img = cv2.imread(image_path)
    if target_size:
        img = cv2.resize(img, target_size)
    return img

def load_tiff_image(image_path, target_size=None):
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if target_size:
        img = cv2.resize(img, target_size)
    return img

def convert_cvimage_to_qimage(cv_image):
    height, width, channel = cv_image.shape
    bytes_per_line = 3 * width
    q_image = QImage(cv_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
    return q_image

def overlay_images(ct_image, seg_image):
    overlay = cv2.addWeighted(ct_image, 0.7, seg_image, 0.3, 0)
    return overlay

class ImageViewer(QMainWindow):
    def __init__(self, overlay_image):
        super().__init__()

        self.initUI(overlay_image)

    def initUI(self, overlay_image):
        view = QGraphicsView(self)
        scene = QGraphicsScene(self)
        view.setScene(scene)
        pixmap = QPixmap.fromImage(overlay_image)
        item = QGraphicsPixmapItem(pixmap)
        scene.addItem(item)
        view.setSceneRect(item.sceneBoundingRect())

        self.setCentralWidget(view)

def main():
    app = QApplication(sys.argv)

    ct_image_path = 'img/volume-0_slice_60.jpg'
    seg_image_path = 'img/volume-0_slice_60.tiff'

    common_size = (512, 512)  # Set the common size for resizing

    ct_image = load_image(ct_image_path, common_size)
    seg_image = load_tiff_image(seg_image_path, common_size)

    overlay = overlay_images(ct_image, seg_image)

    q_image = convert_cvimage_to_qimage(overlay)

    print(f"CT scan image dimensions: {ct_image.shape}")
    print(f"Segmentation image dimensions: {seg_image.shape}")


    viewer = ImageViewer(q_image)
    viewer.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
