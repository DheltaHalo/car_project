import sys
from time import sleep
from threading import Thread
from datetime import date
import json
from numpy import min_scalar_type

import pandas as pd

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from modules import segundamano as sg

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
        self.parent().center(1200, 350)
        self.create_lists()
        self.startUI()
    
    def create_lists(self):
        self.url = "https://www.coches.net/segunda-mano/"
        max_year = int(date.today().year)
        min_year = 1971

        global main_dataframe
        main_dataframe = sg.create_files()
        self.models_frame = main_dataframe["models"]

        self.year_str = "&MaxYear={year_max}&MinYear={year_min}"
        self.year_list = [str(x) for x in range(min_year, max_year + 1)]
        self.year_list.insert(0, "Año")

        self.marca_list = [x.replace("_models", "") for x in self.models_frame]
        self.marca_list.insert(0, "Marca")

        self.cambio_list = ["Automático", "Manual"]
        
    def startUI(self):
        self.main_grid = QGridLayout(self)

        # Add labels
        self.lbl = QLabel("Filtrar")
        self.lbl.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.lbl.setAlignment(Qt.AlignCenter)
        self.lbl.setFont(QFont('Times', 18))

        # We create the dropdown lists
        min_year_menu = QMenu(self)
        marca_menu = QMenu(self)
        cambio_menu = QMenu(self)
        
        create_menu(self.year_list, min_year_menu)
        create_menu(self.marca_list, marca_menu)
        create_menu(self.cambio_list, cambio_menu)

        self.min_years_btn = QPushButton("Año")
        self.min_years_btn.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.min_years_btn.setFont(QFont('Times', 15))
        self.min_years_btn.setMenu(min_year_menu)

        self.max_years_btn = QPushButton("Hasta")
        self.max_years_btn.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.max_years_btn.setFont(QFont('Times', 15))      

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

        min_year_menu.triggered.connect(lambda action: self.min_years_btn.setText(action.text()))
        marca_menu.triggered.connect(lambda action: self.marca_btn.setText(action.text()))
        cambio_menu.triggered.connect(lambda action: self.cambio_btn.setText(action.text()))
        marca_menu.triggered.connect(self.model_button)
        min_year_menu.triggered.connect(self.max_year_button)

        # Final button
        self.export_btn = QPushButton("Exportar")
        self.export_btn.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.export_btn.clicked.connect(self.extract)
        self.export_btn.setFont(QFont('Times', 15))

        # Grid properties
        self.main_grid.addWidget(self.lbl, 0, 0, 1, 6)
        self.main_grid.addWidget(self.min_years_btn, 1, 0)
        self.main_grid.addWidget(self.max_years_btn, 1, 1)
        self.main_grid.addWidget(self.marca_btn, 1, 2)
        self.main_grid.addWidget(self.model_btn, 1, 3)
        self.main_grid.addWidget(self.cambio_btn, 1,4)
        self.main_grid.addWidget(self.km_btn, 1, 5)
        self.main_grid.addWidget(self.export_btn, 2, 0, 1, 6)

        self.setLayout(self.main_grid)
        self.show()
    
    def model_button(self):
        model_menu = QMenu(self)
        marca = self.marca_btn.text()
        model_text = "Modelo"
        
        models = self.models_frame[f'{marca}']
        models.sort()
        models.insert(0, "Modelo")
        models = drop_duplicates(models)

        create_menu(models, model_menu)

        self.model_btn.setMenu(model_menu)
        model_menu.triggered.connect(lambda action: self.model_btn.setText(action.text()))

    def max_year_button(self):
        max_year_menu = QMenu(self)
        min_year = self.min_years_btn.text()

        max_year_list = self.year_list[self.year_list.index(min_year):]
        max_year_list.insert(0, "Hasta")
        create_menu(max_year_list, max_year_menu)
        self.max_years_btn.setMenu(max_year_menu)
        max_year_menu.triggered.connect(lambda action: self.max_years_btn.setText(action.text()))

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

        min_year_sol = self.min_years_btn.text()
        max_year_sol = self.max_years_btn.text()
        marca_sol = self.marca_btn.text()
        model_sol = self.model_btn.text()
        cambio_sol = self.cambio_btn.text()
        km_sol = self.km_btn.text()
        txt = self.lbl.text()

        global url
        url = self.url
        global name
        name = "car_data"

        if marca_sol != "Marca":
            url += marca_sol.replace(" ", "_") + "/"
            name += "_" + marca_sol

        if model_sol != "Modelo":
            url += model_sol.replace(" ", "_") + "/"
            name += "_" + model_sol 

        url += "?st=2"

        if min_year_sol != "Año":
            if max_year_sol != "Hasta":
                url += self.year_str.format(year_max=max_year_sol, year_min=min_year_sol)
                name += f'_{min_year_sol}-{max_year_sol}'
            
            else:
                url += self.year_str.format(year_max=min_year_sol, year_min=min_year_sol)
                name += f'_{min_year_sol}'

        if cambio_sol != "Cambio":
            indx = self.cambio_list.index(cambio_sol)
            url += f'&TransmissionTypeId={indx+1}'
            name += "_" + cambio_sol
        
        if km_sol != "":
            url += "&MaxKms=" + km_sol
            name += "_kmMax" + km_sol
        
        
        print(url)

        name += ".csv"

        global button_window_epic
        button_window_epic = self.parent().ButtonWindow
        
        self.parent().startMenuTab()
        self.hide()

class MenuTab(QWidget):
    """
    MenuTab that holds the download button and downloads the data to scrape
    """
    def __init__(self, parent=None):
        super(MenuTab, self).__init__(parent)
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
        df = ThreadReturn(target=sg.get_url, args=("", url, 1, True,))
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
        # df["phone"] = df["phone"].apply(pd.to_numeric)
        # df = pd.concat([df, df2])
        df = sg.clean(df)
        print(path)
        print(name)
        full_path = os.path.join(path, name)
        print(full_path)
        df.to_csv(full_path, index=False)
        
        self.change_text_thread.start()

    def change_screen(self):
        """
        Swaps the window
        """
        self.parent().startFilterTab()
        self.close()

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowIcon(QIcon("car.ico"))
        self.startFilterTab()
    
    def startFilterTab(self):
        if hasattr(self, 'ButtonWindow'):
            self.ButtonWindow.show()
            self.center(1200, 350)
        else:
            self.ButtonWindow = FilterTab(self)
            self.setWindowTitle("Filtrar")
            self.setCentralWidget(self.ButtonWindow)
            self.show()
        
    def startMenuTab(self):
        self.Window = MenuTab(self)
        self.center(300, 150)
        self.setWindowTitle("Menu")
        self.show()
    
    def center(self, app_h: int, app_w: int):
        self.setGeometry((1920 - app_h) // 2, (1080 - app_w) // 2, app_h, app_w)
        self.setFixedSize(app_h, app_w)

if __name__ == '__main__':
    sg.upload_dropbox()
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())