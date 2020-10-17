import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize
from os import listdir
from os.path import isfile, join
import collections

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.inverted_index = {}
        self.namefile_idx = {}
        self.dict_vec_pr = {}

        self.load_page_rank_and_inverted_index()

        self.setMinimumSize(QSize(320, 140))    
        self.setWindowTitle("Search Engine") 

        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Name:')
        self.line = QLineEdit(self)

        self.line.move(80, 20)
        self.line.resize(200, 32)
        self.nameLabel.move(20, 20)

        pybutton = QPushButton('OK', self)
        pybutton.clicked.connect(self.clickMethod)
        pybutton.resize(200,32)
        pybutton.move(80, 60)

    def load_page_rank_and_inverted_index(self):
        mypath = "./output_inverted_index"
        onlyfiles = [join(mypath, f) for f in listdir(mypath)]
        for filepath in onlyfiles:
            file_inv_idx = open(filepath, "r")
            lines_file_inv_idx = file_inv_idx.readlines()
            file_inv_idx.close()
            lines_file_inv_idx = [x.strip() for x in lines_file_inv_idx]
            for line in lines_file_inv_idx:
                word, namefile = line.split()
                value_obt = self.inverted_index.get(word)
                if value_obt == None:
                    self.inverted_index[word] = [namefile]
                else:
                    self.inverted_index[word].append(namefile)

        file_namefiles = open("name_files.txt", "r")
        lines_file_nf = file_namefiles.readlines()
        file_namefiles.close()
        lines_file_nf = [x.strip() for x in lines_file_nf]
        count = 0
        for line in lines_file_nf:
            self.namefile_idx[line] = count
            count += 1

        file_pr = open("vector_page_rank_final.txt", "r")
        lines_file_pr = file_pr.readlines()
        file_pr.close()
        lines_file_pr = [x.strip() for x in lines_file_pr]
        for line in lines_file_pr:
            numbers = line.split()
            idx = int(numbers[0])
            value_vec = float(numbers[1])
            self.dict_vec_pr[idx] = value_vec

    def clickMethod(self):
        num_max_results = 15
        count = 0
        input_line = self.line.text()
        input_words = input_line.split()
        result = []
        for word in input_words:
            res_inv_idx = self.inverted_index.get(word)
            if res_inv_idx != None:
                list_sorted_pr_namefile = []
                for namefile in res_inv_idx:
                    idx_namefile = self.namefile_idx[namefile]
                    list_sorted_pr_namefile.append((self.dict_vec_pr[idx_namefile], namefile))
                list_sorted_pr_namefile.sort(key=lambda tup: tup[0], reverse=True)
                i = 0
                while count < num_max_results:
                    print(list_sorted_pr_namefile[i][1], list_sorted_pr_namefile[i][0])
                    i += 1
                    count += 1
                if count >= num_max_results:
                    break
        print()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit( app.exec_() )