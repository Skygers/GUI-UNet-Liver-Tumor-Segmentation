# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'autosegApps.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QGroupBox,
    QLabel, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QWidget)

from pyqtgraph import ImageView, GraphicsLayoutWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.ApplicationModal)
        MainWindow.resize(1020, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.maintoolbar_widget = QWidget(self.centralwidget)
        self.maintoolbar_widget.setObjectName(u"maintoolbar_widget")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.maintoolbar_widget.sizePolicy().hasHeightForWidth())
        self.maintoolbar_widget.setSizePolicy(sizePolicy)
        self.gridLayout_6 = QGridLayout(self.maintoolbar_widget)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.groupBox = QGroupBox(self.maintoolbar_widget)
        self.groupBox.setObjectName(u"groupBox")
        font = QFont()
        font.setBold(True)
        self.groupBox.setFont(font)
        self.groupBox.setFlat(False)
        self.groupBox.setCheckable(False)
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.open_image_button = QPushButton(self.groupBox)
        self.open_image_button.setObjectName(u"open_image_button")

        self.gridLayout_2.addWidget(self.open_image_button, 1, 0, 1, 1)

        self.reset_button = QPushButton(self.groupBox)
        self.reset_button.setObjectName(u"reset_button")

        self.gridLayout_2.addWidget(self.reset_button, 6, 0, 1, 1)

        self.autosegmentation_button = QPushButton(self.groupBox)
        self.autosegmentation_button.setObjectName(u"autosegmentation_button")

        self.gridLayout_2.addWidget(self.autosegmentation_button, 4, 0, 1, 1)

        self.analysis_button = QPushButton(self.groupBox)
        self.analysis_button.setObjectName(u"analysis_button")

        self.gridLayout_2.addWidget(self.analysis_button, 8, 0, 1, 1)

        self.open_image_label = QLabel(self.groupBox)
        self.open_image_label.setObjectName(u"open_image_label")
        self.open_image_label.setFont(font)
        self.open_image_label.setFrameShape(QFrame.Panel)
        self.open_image_label.setFrameShadow(QFrame.Sunken)
        self.open_image_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.open_image_label, 0, 0, 1, 1)

        self.autosegmentation_label = QLabel(self.groupBox)
        self.autosegmentation_label.setObjectName(u"autosegmentation_label")
        self.autosegmentation_label.setFrameShape(QFrame.Panel)
        self.autosegmentation_label.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.autosegmentation_label, 3, 0, 1, 1)

        self.clear_image_button = QPushButton(self.groupBox)
        self.clear_image_button.setObjectName(u"clear_image_button")

        self.gridLayout_2.addWidget(self.clear_image_button, 7, 0, 1, 1)

        self.line = QFrame(self.groupBox)
        self.line.setObjectName(u"line")
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setLineWidth(2)
        self.line.setFrameShape(QFrame.HLine)

        self.gridLayout_2.addWidget(self.line, 5, 0, 1, 1)


        self.gridLayout_6.addWidget(self.groupBox, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.maintoolbar_widget, 1, 0, 3, 1)

        self.ctscan_imgview = ImageView(self.centralwidget)
        self.ctscan_imgview.setObjectName(u"ctscan_imgview")
        self.ctscan_imgview.ui.histogram.hide()
        self.ctscan_imgview.ui.roiBtn.hide()

        self.gridLayout.addWidget(self.ctscan_imgview, 1, 1, 1, 1)

        self.overlayer_imgview = ImageView(self.centralwidget)
        self.overlayer_imgview.setObjectName(u"overlayer_imgview")
        #self.overlayer_imgview.addViewBox()
        #self.overlayer_imgview.setAspectLocked()
        
        self.overlayer_imgview.ui.histogram.hide()
        self.overlayer_imgview.ui.roiBtn.hide()

        self.overlayer_imgview_v = self.overlayer_imgview.getView()

        self.gridLayout.addWidget(self.overlayer_imgview, 3, 2, 1, 1)

        self.segmentation_imgview = ImageView(self.centralwidget)
        self.segmentation_imgview.setObjectName(u"segmentation_imgview")
        self.segmentation_imgview.ui.histogram.hide()
        self.segmentation_imgview.ui.roiBtn.hide()

        self.gridLayout.addWidget(self.segmentation_imgview, 3, 1, 1, 1)

        self.ctscan2_imgview_label = QLabel(self.centralwidget)
        self.ctscan2_imgview_label.setObjectName(u"ctscan2_imgview_label")
        self.ctscan2_imgview_label.setFont(font)

        self.gridLayout.addWidget(self.ctscan2_imgview_label, 0, 2, 1, 1)

        self.ctscan_imgview_label = QLabel(self.centralwidget)
        self.ctscan_imgview_label.setObjectName(u"ctscan_imgview_label")
        self.ctscan_imgview_label.setFont(font)

        self.gridLayout.addWidget(self.ctscan_imgview_label, 0, 1, 1, 1)

        self.ctscan2_imgview = ImageView(self.centralwidget)
        self.ctscan2_imgview.setObjectName(u"ctscan2_imgview")
        self.ctscan2_imgview.ui.histogram.hide()
        self.ctscan2_imgview.ui.roiBtn.hide()

        self.gridLayout.addWidget(self.ctscan2_imgview, 1, 2, 1, 1)

        self.segmentation_imgview_label = QLabel(self.centralwidget)
        self.segmentation_imgview_label.setObjectName(u"segmentation_imgview_label")
        self.segmentation_imgview_label.setFont(font)

        self.gridLayout.addWidget(self.segmentation_imgview_label, 2, 1, 1, 1)

        self.overlay_imgview_label = QLabel(self.centralwidget)
        self.overlay_imgview_label.setObjectName(u"overlay_imgview_label")
        self.overlay_imgview_label.setFont(font)

        self.gridLayout.addWidget(self.overlay_imgview_label, 2, 2, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.image_path = ''
        self.segmentationpath = 'output/segment.tiff'
        self.segmentationpath2 = 'output/segment.jpg'
        self.overlaypath = 'output/overlay.png'

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"AutoSegApps", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"MAIN TOOLBAR", None))
        self.open_image_button.setText(QCoreApplication.translate("MainWindow", u"Open Image", None))
        self.reset_button.setText(QCoreApplication.translate("MainWindow", u"RESET", None))
        self.autosegmentation_button.setText(QCoreApplication.translate("MainWindow", u"Auto Segmentation", None))
        self.analysis_button.setText(QCoreApplication.translate("MainWindow", u"ANALYSIS", None))
        self.open_image_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Citra CT-Scan dalam bentuk<br/>JPG, JPEG, dan PNG</p></body></html>", None))
        self.autosegmentation_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>CATATAN PENTING:</p><p><span style=\" font-weight:400;\">Hanya digunakan sebagai identifikasi.</span></p><p><span style=\" font-weight:400;\">Tidak dipergunakan sebagai diagnosa medis.</span></p></body></html>", None))
        self.clear_image_button.setText(QCoreApplication.translate("MainWindow", u"CLEAR IMAGE", None))
        self.ctscan2_imgview_label.setText(QCoreApplication.translate("MainWindow", u"CT-SCAN", None))
        self.ctscan_imgview_label.setText(QCoreApplication.translate("MainWindow", u"CT-SCAN", None))
        self.segmentation_imgview_label.setText(QCoreApplication.translate("MainWindow", u"SEGMENTATION", None))
        self.overlay_imgview_label.setText(QCoreApplication.translate("MainWindow", u"OVERLAY", None))
    # retranslateUi

