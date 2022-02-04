import sys
from time import sleep
from threading import Thread
from datetime import date
import json

import pandas as pd

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from modules import scraping as sg

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QObject, pyqtSignal, Qt, QThread, QTimer, QEventLoop
from PyQt5.QtWidgets import (
    QMenu,
    QWidget,
    QGridLayout,
    QPushButton,
    QSizePolicy,
    QLabel,
    QProgressBar,
    QFileDialog,
    QMainWindow,
    QApplication,
    QLineEdit
)

# Icon by Flaticon (link: 'https://www.flaticon.com/free-icons/shapes-and-symbols')

# Random classes
class ThreadReturn(Thread):
    """
    Allows for a Thread to return it's data without using a Pool/Queue, so it returns just that instance
    """
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return
 
def create_menu(d, menu):
    """
    Creates a QMenu drop_list
    """
    if isinstance(d, list):
        for e in d:
            create_menu(e, menu)
    elif isinstance(d, dict):
        for k, v in d.items():
            sub_menu = QMenu(k, menu)
            menu.addMenu(sub_menu)
            create_menu(v, sub_menu)
    else:
        action = menu.addAction(d)
        action.setIconVisibleInMenu(False)

def drop_duplicates(t: list):
    new_list = []
    for k in t:
        if k not in new_list:
            new_list.append(k)
            
    return new_list

class Worker1(QObject):
    """
    QThread worker to run a Thread without crashing the main Thread
    """
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def run(self):
        for i in range(100):
            self.progress.emit(i + 1)
            sleep(0.03)
        self.finished.emit()

# PyQt classes
class FilterTab(QWidget):
    def __init__(self, parent=None):
        super(FilterTab, self).__init__(parent)
        self.parent().center(1100, 350)
        self.create_lists()
        self.startUI()
    
    def create_lists(self):
        self.url = "https://www.autoscout24.es/lst/"
        max_year = int(date.today().year)
        min_year = 1900

        self.year_str = "&fregto={year}&fregfrom={year}"
        self.year_list = [str(x) for x in range(min_year, max_year + 1)]
        self.year_list.insert(0, "Año")

        global main_dataframe
        main_dataframe = sg.create_files()

        self.marca_list = [x for x in main_dataframe['models']]
        self.marca_list.insert(0, "Marca")

        self.models_frame = main_dataframe["models"]

        self.cambio_list = ["Automático", "Manual"]
        
    def startUI(self):
        self.main_grid = QGridLayout(self)

        # Add labels
        self.lbl = QLabel("Filtrar")
        self.lbl.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.lbl.setAlignment(Qt.AlignCenter)
        self.lbl.setFont(QFont('Times', 18))

        # We create the dropdown lists
        years_menu = QMenu(self)
        marca_menu = QMenu(self)
        cambio_menu = QMenu(self)
        
        create_menu(self.year_list, years_menu)
        create_menu(self.marca_list, marca_menu)
        create_menu(self.cambio_list, cambio_menu)

        self.years_btn = QPushButton("Año")
        self.years_btn.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.years_btn.setFont(QFont('Times', 15))
        self.years_btn.setMenu(years_menu)

        self.marca_btn = QPushButton("Marca")
        self.marca_btn.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.marca_btn.setFont(QFont('Times', 15))
        self.marca_btn.setMenu(marca_menu)

        self.model_btn = QPushButton("Modelo")
        self.model_btn.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.model_btn.setFont(QFont('Times', 15))

        self.cambio_btn = QPushButton("Cambio")
        self.cambio_btn.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.cambio_btn.setFont(QFont('Times', 15))
        self.cambio_btn.setMenu(cambio_menu)

        self.km_btn = QLineEdit()
        self.km_btn.setPlaceholderText("Hasta x km")
        self.km_btn.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.km_btn.setFont(QFont('Times', 15))

        years_menu.triggered.connect(lambda action: self.years_btn.setText(action.text()))
        marca_menu.triggered.connect(lambda action: self.marca_btn.setText(action.text()))
        cambio_menu.triggered.connect(lambda action: self.cambio_btn.setText(action.text()))
        marca_menu.triggered.connect(self.model_button)

        # Final button
        self.export_btn = QPushButton("Exportar")
        self.export_btn.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.export_btn.clicked.connect(self.extract)
        self.export_btn.setFont(QFont('Times', 15))

        # Grid properties
        self.main_grid.addWidget(self.lbl, 0, 0, 1, 5)
        self.main_grid.addWidget(self.years_btn, 1, 0)
        self.main_grid.addWidget(self.marca_btn, 1, 1)
        self.main_grid.addWidget(self.model_btn, 1, 2)
        self.main_grid.addWidget(self.cambio_btn, 1,3)
        self.main_grid.addWidget(self.km_btn, 1, 4)
        self.main_grid.addWidget(self.export_btn, 2, 0, 1, 5)

        self.setLayout(self.main_grid)
        self.show()
    
    def model_button(self):
        model_menu = QMenu(self)
        marca = self.marca_btn.text()
        model_text = "Modelo"

        self.lbl.setText("Filtrar")
        self.lbl.setStyleSheet("color: black")

        try:
            models = [x for x in self.models_frame[f'{marca}']['models']]
            models.sort()
            models.insert(0, "Modelo")
            models = drop_duplicates(models)

            create_menu(models, model_menu)

            self.model_btn.setMenu(model_menu)
            model_menu.triggered.connect(lambda action: self.model_btn.setText(action.text()))

        except KeyError:
            create_menu([model_text], model_menu)
            self.model_btn.setMenu(model_menu)
            self.model_btn.setText(model_text)

    def change_text(self, n):
        """
        Makes the download text more appealing
        """
        spinners = ["\\", "-", "/", "|"]
        self.lbl.setText("Descargando datos " + spinners[n%len(spinners)])
        self.lbl.setStyleSheet("color: orange")
        if n == 100:
            self.lbl.setText("Completado!")
            self.lbl.setStyleSheet("color: black")

    def extract(self):
        global path
        path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        path = path if path != "" else os.path.dirname(os.path.abspath(__file__))
        print(path)

        year_sol = self.years_btn.text()
        marca_sol = self.marca_btn.text()
        model_sol = self.model_btn.text()
        cambio_sol = self.cambio_btn.text()
        km_sol = self.km_btn.text()
        txt = self.lbl.text()

        global url
        url = self.url
        global name
        name = "\\autoscout24"

        if marca_sol != "Marca":
            url += f'{marca_sol}/'
            name += "_" + marca_sol

        if model_sol != "Modelo":
            url += f'{model_sol}/'
            name += "_" + model_sol

        url += '?sort=age&desc=1&custtype=P&ustate=N%2CU&size=20&cy=E&atype=C&recommended_sorting_based_id=fc7fbe77-56cd-4431-920d-e075f31b45da'

        if year_sol != "Año":
            url += self.year_str.format(year=year_sol)
            name += "_" + year_sol

        if cambio_sol != "Cambio":
            url += f'&gear={cambio_sol[0]}'
            name += "_" + cambio_sol
        
        if km_sol != "":
            url += "&kmto=" + km_sol
            name += "_kmMax" + km_sol
        
        name += ".xlsx"
        
        self.close()
        self.parent().startMenuTab()

class MenuTab(QWidget):
    """
    MenuTab that holds the download button and downloads the data to scrape
    """
    def __init__(self, parent=None):
        super(MenuTab, self).__init__(parent)
        self.width = 300
        self.height = 150
        self.parent().center(self.width, self.height)
        self.startUI()

    def startUI(self):
        """
        We build the UI
        """
        self.main_grid = QGridLayout(self)

        # Add widgets
        self.lbl = QLabel("Descargando |")
        self.lbl.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.lbl.setAlignment(Qt.AlignCenter)
        self.lbl.setFont(QFont('Times', 12))

        self.bar = QProgressBar()
        self.bar.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        # We add the new Widgets
        self.main_grid.addWidget(self.lbl)
        self.main_grid.addWidget(self.bar)

        self.setLayout(self.main_grid)
        self.show()
        self.download()
    
    def download(self):
        """
        We change the UI and start all download operations (both technical and GUI wise)
        """
        # We run our worker threads
        self.change_text_thread = QThread()
        self.worker = Worker1()

        self.worker.moveToThread(self.change_text_thread)
        self.change_text_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.change_text_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(self.change_screen)
        self.change_text_thread.finished.connect(self.change_text_thread.deleteLater)
        self.worker.progress.connect(self.change_text)

        # We start the threads
        print(url)
        df = ThreadReturn(target=sg.scrape, args=(url,5,))
        th = Thread(target=self.check_frame, args=(df,))
        df.start()
        th.start()
    
    def change_text(self, n):
        """
        Makes the download text more appealing
        """
        spinners = ["\\", "-", "/", "|"]
        self.lbl.setText("Procesando datos " + spinners[n%len(spinners)])
        self.bar.setValue(n)
        if n == 100:
            self.lbl.setText("Completado!")
    
    def check_frame(self, th: Thread):
        """
        Checks when the data hasta stopped downloading to finish the process and swap windows
        """
        spinners = ["\\", "-", "/", "|"]
        text = self.lbl.text()

        while th.is_alive():
            for s in spinners:
                self.lbl.setText(text[:-1] + s)
                sleep(0.2)

        df = th.join()
        df = pd.DataFrame(df)

        print(path)
        print(name)
        print(df)
        df.to_excel(path + name, index=False)
        
        self.change_text_thread.start()

    def change_screen(self):
        """
        Swaps the window
        """
        self.close()
        self.parent().startFilterTab()

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowIcon(QIcon("car.ico"))
        self.startFilterTab()
    
    def startFilterTab(self):
        self.Window = FilterTab(self)
        self.setWindowTitle("Filtrar")
        self.setCentralWidget(self.Window)
        self.show()
    
    def startMenuTab(self):
        self.Window = MenuTab(self)
        self.setWindowTitle("Menu")
        self.setCentralWidget(self.Window)
        self.show()
    
    def center(self, app_h: int, app_w: int):
        self.setGeometry((1920 - app_h) // 2, (1080 - app_w) // 2, app_h, app_w)
        self.setFixedSize(app_h, app_w)

if __name__ == '__main__':
    sg.upload_dropbox()
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())