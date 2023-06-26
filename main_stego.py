import sys  
from PyQt5 import QtWidgets
import design_stego 
from PyQt5.QtGui import QPixmap
import Insert_Data
import Extract_Data
import os


class ExampleApp(QtWidgets.QMainWindow, design_stego.Ui_MainWindow):
    def __init__(self):
   
        super().__init__()
        self.setupUi(self) 


        self.outputFormat.addItems(["png", "bmp", "jp2", "jpg"])
        self.N_levels.addItems(["1", "2", "3", "4", "5"])

        self.getFileNameInsert.clicked.connect(self.GFNI)
        self.getFileNameExtract.clicked.connect(self.GFNE)
        self.getKeyPathInsert.clicked.connect(self.GKFNI)
        self.getKeyPathExtract.clicked.connect(self.GKFNE)

        self.Insert.clicked.connect(self.Insert_f)
        self.Extract.clicked.connect(self.Extract_f)

      


    def GFNI(self):
        filename = self.getFileName()
        self.PathToInsertFile.setText(filename)
        pixmap = QPixmap(filename)
        self.ImageInsert.setPixmap(pixmap)

    def GFNE(self):
        filename = self.getFileName()
        self.PathToExtractFile.setText(filename)
        pixmap = QPixmap(filename)
        self.ImageExtract.setPixmap(pixmap)

    def GKFNI(self):
        filename = self.getFileName()
        self.PathToKeyFileInsert.setText(filename)

    def GKFNE(self):
        filename = self.getFileName()
        self.PathToKeyFileExtract.setText(filename)


    def Insert_f(self):
        secret_message = self.TextInsert.text()
        filename = self.PathToInsertFile.text()
        file_key = self.PathToKeyFileInsert.text()
        output_format = self.outputFormat.currentText()
        n_levels = int(self.N_levels.currentText())
        print("output_format = |" + output_format+"|")
        result = Insert_Data.paste_data_to_image(filename, output_format, file_key, secret_message, n_levels)
        if result != 0:
            self.label.setText("Tidak Berhasil")
            self.label.setStyleSheet("QLabel {color:rgba(255, 0, 0, 255)}")
        else:
            self.label.setText("Berhasil")
            self.label.setStyleSheet("QLabel {color:rgba(0, 255, 0, 255)}")


    def Extract_f(self):
        #Extract
        filename = self.PathToExtractFile.text()
        file_key = self.PathToKeyFileExtract.text()
        n_levels = int(self.N_levels.currentText())
        exctract_message = Extract_Data.extract_data(filename, file_key, n_levels)
        self.TextExtract.setText(exctract_message)

    def getFileName(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, "Pilih File")

        return filename[0]



def main():
    app = QtWidgets.QApplication(sys.argv)  
    window = ExampleApp()
    window.show()  
    app.exec_() 


if __name__ == '__main__': 
    main()  