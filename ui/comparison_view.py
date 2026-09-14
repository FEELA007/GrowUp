from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPixmap , QPen ,QBrush
from PySide6.QtWidgets import QWidget

class ComparisonView(QWidget):


    def __init__(self,parent=None):
        super().__init__(parent)
        self.before=QPixmap()
        self.after=QPixmap()
        self.position=0.5
        self.setMinimumSize(400,300)
        self.setMouseTracking(True)
        self.setCursor(Qt.OpenHandCursor)

    def set_images(self,before,after):
        self.before=before
        self.after=after
        self.update()

    def mousePressEvent(self,event):
        if event.button()==Qt.LeftButton:
            self.update_position(event.position().x())
            self.setCursor(Qt.ClosedHandCursor)

    
    def mouseReleaseEvent(self,event):
        if event.button()==Qt.LeftButton:
            self.setCursor(Qt.OpenHandCursor)


    def mouseMoveEvent(self,event):
        if event.buttons() & Qt.LeftButton:
            self.update_position(event.position().x())

    def update_position(self,x):
        self.position=max(0.0,min(1.0,x/self.width()))
        self.update()
    # before after main pannel 14-09-26
    def paintEvent(self,event):
        if self.before.isNull() or self.after.isNull():
            return
        painter=QPainter(self)
        painter.fillRect(self.rect(), Qt.black)
        rect=self.rect()
        painter.setRenderHint(QPainter.Antialiasing)
        after=self.after.scaled(rect.size(),Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
        x=(self.width()-after.width())//2
        y=(self.height()-after.height())//2
        painter.drawPixmap(x,y,after)
        split_x=int(self.width()*self.position)
        painter.save()
        painter.setClipRect(0,0,split_x,self.height())
        before=self.before.scaled(rect.size(),Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
        painter.drawPixmap(x,y,before)
        painter.restore()
        painter.setPen(QPen(Qt.white, 1))
        painter.drawLine(split_x,y,split_x,y+after.height())
        painter.setBrush(QBrush(Qt.black))
        painter.setPen(QPen(Qt.white,1))
        painter.drawRoundedRect(split_x-16,self.height()//2-20,32,40,9,9)
        painter.setPen(QPen(Qt.white,2))
        center_y=self.height()//2
        painter.drawLine(split_x-8,center_y,split_x-3,center_y-5)
        painter.drawLine(split_x-8,center_y,split_x-3,center_y+5)
        painter.drawLine(split_x+8,center_y,split_x+3,center_y-5)
        painter.drawLine(split_x+8,center_y,split_x+3,center_y+5)
        painter.setPen(QPen(Qt.lightGray, 1))
        painter.drawText(16,28,"BEFORE")
        painter.drawText(self.width() - 55,28,"AFTER")
        #-------------------------------------------------------------------------------------------------------

