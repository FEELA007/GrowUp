from pathlib import Path
import cv2
# ui elements 14-09-26
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (QFileDialog,QFrame,QHBoxLayout,QLabel,QLineEdit,QMessageBox,QPushButton,QSlider,QVBoxLayout,QWidget,)
# image processing 14-09-26
from processing.image_processing import process_image
from processing.upscaler import upscale_image
from ui.comparison_view import ComparisonView
from ui.drop_frame import DropFrame
from PySide6.QtCore import QSettings
#enhance page 14-09-26
class EnhancePage(QWidget):
    #for making page 
    def __init__(self, window):
        super().__init__()
        self.image_path = None
        self.original_image = None
        self.enhanced_image = None
        self.window = window
        self.settings = QSettings("GrowUp", "GrowUp")
        self.image_path = None
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 24, 30, 25)
        layout.setSpacing(18)
        subtitle = QLabel("AI Image Enhancement & Restoration")
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)
        content = QHBoxLayout()
        content.setSpacing(20)
        self.preview = DropFrame()
        self.preview.file_dropped.connect(self.load_dropped_image)
        self.preview.setAcceptDrops(True)
        self.preview.setObjectName("preview")
        preview_layout = QVBoxLayout(self.preview)
        self.comparison_view = ComparisonView()
        self.preview_label = QLabel("Drop an image here")
        preview_layout.addWidget(self.comparison_view)
        content.addWidget(self.preview, 1)
        #-----------------------------------------------------------------------------------------------------
        # for making side panal lol
        panel = QFrame()
        panel.setObjectName("panel")
        panel.setFixedWidth(300)
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(24, 24, 24, 24)
        panel_layout.setSpacing(16)
        heading = QLabel("Enhancement")
        heading.setObjectName("heading")
        panel_layout.addWidget(heading)
        #---------------------------------------------------------------------------------------------------------
        # upscale buttons 14-09-26
        upscale_label = QLabel("Upscale")
        upscale_label.setObjectName("sectionLabel")
        panel_layout.addWidget(upscale_label)
        scale_layout = QHBoxLayout()
        self.two_x = QPushButton("2×")
        self.four_x = QPushButton("4×")
        self.two_x.setCheckable(True)
        self.four_x.setCheckable(True)
        saved_scale = self.settings.value("default_scale", "2×")
        self.two_x.setChecked(saved_scale == "2×")
        self.four_x.setChecked(saved_scale == "4×")
        self.two_x.clicked.connect(lambda: self.select_scale(self.two_x, self.four_x))
        self.four_x.clicked.connect(lambda: self.select_scale(self.four_x, self.two_x))
        self.upscale_factor = 4 if saved_scale == "4×" else 2
        scale_layout.addWidget(self.two_x)
        scale_layout.addWidget(self.four_x)
        panel_layout.addLayout(scale_layout)
        #----------------------------------------------------------------------------------------------------------------------
        # denoise panel 13-09-26
        panel_layout.addWidget(QLabel("Denoise"))
        self.denoise = QSlider(Qt.Orientation.Horizontal)
        self.denoise.setRange(0, 100)
        self.denoise.setValue(50)
        self.denoise_value = QLineEdit("50")
        self.denoise_value.setFixedWidth(45)
        self.denoise_value.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        denoise_row = QHBoxLayout()
        denoise_row.addWidget(self.denoise)
        denoise_row.addWidget(self.denoise_value)
        panel_layout.addLayout(denoise_row)
        self.denoise.valueChanged.connect(lambda value: self.denoise_value.setText(str(value)))
        self.denoise_value.editingFinished.connect(lambda: self.validate_value(self.denoise_value, self.denoise, "Denoise"))
        #-----------------------------------------------------------------------------------------------------------------------
        # sharpen panel 13-09-26
        panel_layout.addWidget(QLabel("Sharpen"))
        self.sharpen = QSlider(Qt.Orientation.Horizontal)
        self.sharpen.setRange(0, 100)
        self.sharpen.setValue(40)
        self.sharpen_value = QLineEdit("40")
        self.sharpen_value.setFixedWidth(45)
        self.sharpen_value.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        sharpen_row = QHBoxLayout()
        sharpen_row.addWidget(self.sharpen)
        sharpen_row.addWidget(self.sharpen_value)
        panel_layout.addLayout(sharpen_row)
        self.sharpen.valueChanged.connect(lambda value: self.sharpen_value.setText(str(value)))
        self.sharpen_value.editingFinished.connect(lambda: self.validate_value(self.sharpen_value, self.sharpen, "Sharpen"))
        #-----------------------------------------------------------------------------------------------------------------------\
        # deblur panel 13-09-26
        panel_layout.addWidget(QLabel("Deblur"))
        self.deblur = QSlider(Qt.Orientation.Horizontal)
        self.deblur.setRange(0, 100)
        self.deblur.setValue(30)
        self.deblur_value = QLineEdit("30")
        self.deblur_value.setFixedWidth(45)
        self.deblur_value.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        deblur_row = QHBoxLayout()
        deblur_row.addWidget(self.deblur)
        deblur_row.addWidget(self.deblur_value)
        panel_layout.addLayout(deblur_row)
        self.deblur.valueChanged.connect(lambda value: self.deblur_value.setText(str(value)))
        self.deblur_value.editingFinished.connect(lambda: self.validate_value(self.deblur_value, self.deblur, "Deblur"))
        #--------------------------------------------------------------------------------------------------------------------------------
        panel_layout.addStretch()
        # enhance button 14-09-26 
        self.enhance_button = QPushButton("ENHANCE")
        self.enhance_button.setObjectName("primaryButton")
        self.enhance_button.setFixedHeight(50)
        self.enhance_button.clicked.connect(self.enhance_image)
        panel_layout.addWidget(self.enhance_button)
        content.addWidget(panel)
        layout.addLayout(content) 
        #---------------------------------------------------------------------------------------------------------------------------------
        # just info label 14-09-26
        bottom = QHBoxLayout()
        self.info = QLabel("No image selected")
        self.info.setObjectName("info")
        bottom.addWidget(self.info)
        bottom.addStretch()
        #----------------------------------------------------------------------------------------------------------------------------------
        #image choose and save buttons 14-09-26
        choose = QPushButton("Choose Image")
        choose.clicked.connect(self.choose_image)
        save = QPushButton("Save")
        save.clicked.connect(self.save_image)
        bottom.addWidget(choose)
        bottom.addWidget(save)
        layout.addLayout(bottom)
    #---------------------------------------------------------------------------------------------------------------------------------
    #end of main ui code 14-09-26


    # 2x 4x select scale function 13-09-26
    def select_scale(self, selected, other):
        selected.setChecked(True)
        other.setChecked(False)
        self.upscale_factor=4 if selected ==self.four_x else 2
        self.settings.setValue("default_scale", f"{self.upscale_factor}×")

    
    #--------------------------------------------------------------------------------------------------------------------------------------
    def load_dropped_image(self, path):
        image = cv2.imread(path)
        if image is None:
            QMessageBox.warning(self,"Invalid Image","The dropped file is not a valid image.",)
            return
        self.image_path = path
        self.original_image = image
        self.enhanced_image = None
        self.info.setText(f"{Path(path).name}  •  {image.shape[1]} × {image.shape[0]}")
        self.show_image(image)
    #-----------------------------------------------------------------------------------------------------------------------------------------------
    #find image path and load image 14-09-26
    def choose_image(self):
        path, _ = QFileDialog.getOpenFileName(self,"Choose Image","","Images (*.png *.jpg *.jpeg *.webp *.bmp)",)
        if not path:
            return
        image = cv2.imread(path)
        if image is None:
            QMessageBox.warning(self, "Invalid Image", "The selected file could not be loaded.")
            return
        self.image_path = path
        self.original_image = image
        self.info.setText(f"{Path(path).name}  •  {image.shape[1]} × {image.shape[0]}")
        self.show_image(self.original_image)
    #---------------------------------------------------------------------------------------------------------------------------------
    #to see enhanced image 14-09-26
    def update_preview(self):
        if self.original_image is None:
            return
        image = process_image(self.original_image,self.denoise.value(),self.sharpen.value(),self.deblur.value(),)
        image = upscale_image(image, getattr(self, "upscale_factor", 2))
        self.show_image(image)
    #---------------------------------------------------------------------------------------------------------------------------------

    # TO SHOW IMAGE IN PREVIEW 14-09-26
    def show_image(self, image):
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channels = rgb.shape
        bytes_per_line = channels * width
        qimage = QImage(rgb.data,width,height,bytes_per_line,QImage.Format.Format_RGB888,)
        pixmap = QPixmap.fromImage(qimage)
        if self.original_image is not  None:
            original_rgb =cv2.cvtColor(self.original_image,cv2.COLOR_BGR2RGB)
            original_height,original_width,original_channels = original_rgb.shape
            original_bytes = original_channels*original_width
            original_qimage=QImage(original_rgb.data,original_width,original_height,original_bytes,QImage.Format.Format_RGB888,)
            original_pixmap=QPixmap.fromImage(original_qimage)
            self.comparison_view.set_images(original_pixmap,pixmap,)

        available_width = max(100, self.preview.width() - 50)
        available_height = max(100, self.preview.height() - 50)
        pixmap = pixmap.scaled(available_width,available_height,Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation,)
        self.preview_label.setPixmap(pixmap)
    #---------------------------------------------------------------------------------------------------------------------------------
    # to enhance image 14-09-26
    def enhance_image(self):
        if self.original_image is None:
            QMessageBox.warning(self, "No Image", "Please choose an image to enhance.")
            return
        try:
            image =process_image(self.original_image,self.denoise.value(),self.sharpen.value(),self.deblur.value(),)
            image = upscale_image(image,self.upscale_factor,)
            self.enhanced_image = image
            self.show_image(image)
            self.info.setText("Enhanced image preview")
        except Exception as e:
            QMessageBox.critical(self, "Enhancement Error", f"An error occurred while enhancing the image: {str(e)}")
    #---------------------------------------------------------------------------------------------------------------------------------        
    # saving image 14-09-26
    def save_image(self):
        if self.enhanced_image is None:
            QMessageBox.warning(self, "No Enhanced Image", "Please enhance an image before saving.")
            return
        path,_=QFileDialog.getSaveFileName(self,"save Enhanced Image","enhanced_image.png","Png (*.png);; JPEG (*.jpg *.jpeg) ;; WebP (*.webp)",)
        if not path:
            return
        Success = cv2.imwrite(path,self.enhanced_image)
        if Success:
            self.info.setText(f"Enhanced image saved: {Path(path).name}")
        else:
            QMessageBox.critical(self, "Save Error", "Failed to save the enhanced image.")
    #---------------------------------------------------------------------------------------------------------------------------------
    #to validate the value entered 14-09-26
    def validate_value(self, field, slider, name):
        try:
            value = int(field.text())
        except ValueError:
            QMessageBox.warning(self, "Invalid Value", f"{name} value must be an integer.")
            field.setText(str(slider.value()))
            return

        if value > 100:
            QMessageBox.warning(self, "Invalid Value", f"{name} value cannot be greater than 100.")
            field.setText(str(slider.value()))
            return
        if value < 0:
            QMessageBox.warning(self, "Invalid Value", f"{name} value cannot be less than 0.")
            field.setText(str(slider.value()))
            return
        slider.setValue(value)
