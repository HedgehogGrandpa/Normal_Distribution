from PyQt4 import QtGui
import pyqtgraph as pg
import math
import numpy
import xlsxwriter


def gaussian(x, mu, sigma):
    return math.exp(-0.5*((x-mu)/sigma)**2) / sigma / math.sqrt(2*math.pi)


def main():
    def write_to_xls(ss, avs, asd):
        fn, fl = QtGui.QFileDialog.getSaveFileNameAndFilter(filter='Excel Files (*.xlsx *.xls)')
        if len(fn) > 0:
            workbook = xlsxwriter.Workbook(fn)
            worktable = workbook.add_worksheet()
            worktable.set_column('A:B', 20)
            l = len(ss)
            format1 = workbook.add_format({'bold': True, 'align': 'right'})

            worktable.write('A1', '#', format1)
            worktable.write('B1', 'Size', format1)
            for i in range(l):
                worktable.write('A{}'.format(i+2), i+1)
                worktable.write('B{}'.format(i+2), ss[i])
            worktable.write('A{}'.format(l+4), 'average size', format1)
            worktable.write('B{}'.format(l+4), avs)
            worktable.write('A{}'.format(l+5), 'standart deviation', format1)
            worktable.write('B{}'.format(l+5), asd)
            workbook.close()

    def read_arguments():
        try:
            _lb = left_border.text()
            lb = float(_lb.strip().replace(',', '.'))
        except:
            lb = 100
            sizes_list.append('used default left border: 100')
        try:
            _rb = right_border.text()
            rb = float(_rb.strip().replace(',', '.'))
        except:
            rb = 200
            sizes_list.append('used default right border: 200')
        if rb < lb:
            rb, lb = lb, rb
        try:
            accur = int(accuracy.text())
        except:
            accur = 0
            sizes_list.append('used default accuracy: 0')
        try:
            c = int(count.text())
        except:
            c = 100
            sizes_list.append('used default quantity: 100')
        return lb, rb, accur, c

    def draw():
        try:
            lb, rb, accur, c = read_arguments()
            mu = 0.5*(lb + rb)
            sigma = (rb-lb)/6
            sizes_list.clear()
            sizes = []
            sum_size = 0

            for i in range(c):
                size = round(numpy.random.normal(mu, sigma), accur)
                while not (lb <= size <= rb):
                    size = round(numpy.random.normal(mu, sigma), accur)
                sizes_list.append('{}: {}'.format(i+1, size))
                sizes.append(size)
                sum_size += size

            average_size = sum_size/c
            asd_sum = 0
            for size in sizes:
                asd_sum += (size-average_size)**2
            asd = math.sqrt(asd_sum/c)
            sizes_list.append('average size = {:f}\nstandart deviantion = {:f}'.format(average_size, asd))
            plot_widget.clear()
            plot_widget.plot(range(1, c+1), sizes)
            write_to_xls(sizes, average_size, asd)

            '''
            sizes_count = []
            for size in sorted(set(sizes)):
                size_count = sizes.count(size)
                sizes_list.append('{}: {} things'.format(size, size_count))
                sizes_count.append(size_count)
            plot2 = pg.plot(sorted(set(sizes)), sizes_count)
            '''
        except Exception as e:
            sizes_list.append(str(e))

    app = QtGui.QApplication([])
    w = QtGui.QWidget()
    w.resize(500, 400)
    w.move(0, 0)
    left_border_lbl = QtGui.QLabel()
    left_border_lbl.setText('Left Border:')
    left_border = QtGui.QLineEdit()
    left_border.setText('100')
    right_border_lbl = QtGui.QLabel()
    right_border_lbl.setText('Right Border:')
    right_border = QtGui.QLineEdit()
    right_border.setText('200')
    accuracy_lbl = QtGui.QLabel()
    accuracy_lbl.setText('Accuracy:')
    accuracy = QtGui.QLineEdit()
    accuracy.setText('0')
    count_lbl = QtGui.QLabel()
    count_lbl.setText('quantity')
    count = QtGui.QLineEdit()
    count.setText('100')
    calc_btn = QtGui.QPushButton('Calculate\n Normal Distribution')
    calc_btn.clicked.connect(draw)
    sizes_list = QtGui.QTextEdit()
    sizes_list.setMinimumWidth(150)
    #filename_lbl = QtGui.QLabel()
    #filename_lbl.setText('XLS file name')
    #save_to_btn = QtGui.QPushButton('Save results to')
    #save_to_btn.clicked.connect(write_to_xls)
    plot_widget = pg.PlotWidget()
    plot_widget.setMinimumSize(400, 300)
    layout = QtGui.QGridLayout()
    w.setLayout(layout)

    layout.addWidget(left_border_lbl, 0, 0)
    layout.addWidget(left_border, 0, 1)
    layout.addWidget(right_border_lbl, 1, 0)
    layout.addWidget(right_border, 1, 1)
    layout.addWidget(accuracy_lbl, 2, 0)
    layout.addWidget(accuracy, 2, 1)
    layout.addWidget(count_lbl, 3, 0)
    layout.addWidget(count, 3, 1)
    layout.addWidget(calc_btn, 4, 0, 1, 2)
    layout.addWidget(sizes_list, 5, 0, 1, 2)
    #layout.addWidget(save_to_btn, 6, 0, 1, 2)
    layout.addWidget(plot_widget, 0, 2, 7, 1)

    w.show()

    # Start the Qt event loop
    app.exec_()

if __name__ == '__main__':
    main()
