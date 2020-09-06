from PyQt5 import QtCore, QtWidgets
import os
import worQt_timer
import json
import shutil

STATS_KEYS = ['Date', 'Start', 'Finish', 'Duration']


def fill_view_statistic(self):
    file = get_file_log()
    with open(file, 'r') as f:
        try:
            data = json.load(f)
            self.tableWidget.setRowCount(0)
            for i, session in enumerate(data['sessions']):
                self.tableWidget.insertRow(self.tableWidget.rowCount())
                for j, k in enumerate(STATS_KEYS):
                    it = QtWidgets.QTableWidgetItem()
                    it.setData(QtCore.Qt.DisplayRole, str(session[k]))
                    self.tableWidget.setItem(i, j, it)
            self.tableWidget.show()
        except:
            return None


def table_export(self):
    destination = QtWidgets.QFileDialog.getExistingDirectoryUrl()
    try:
        file_log = self.file_log
        fileOutput = sys.argv[2]
        inputFile = open(fileInput)
        outputFile = open(fileOutput, 'w')
        data = json.load(inputFile)
        inputFile.close()
        output = csv.writer(outputFile)
        output.writerow(data[0].keys())
        for row in data:
            output.writerow(row.values())
    except:
        pass
    pass


def set_file_error(self, file_error):
    self.file_error = file_error


def set_file_log(self, file_log):
    self.file_log = file_log


def set_check_in(self):
    session = {
        'Date': str(worQt_timer.get_today()),
        'Start': None,
        'Finish': None,
        'Duration': None,
    }
    log_write_action(session)
    i = self.tableWidget.rowCount()
    self.tableWidget.insertRow(i)
    for j, (k, v) in enumerate(session.items()):
        it = QtWidgets.QTableWidgetItem()
        it.setData(QtCore.Qt.DisplayRole, str(session[k]))
        self.tableWidget.setItem(i, j, it)
    self.tableWidget.show()


def set_session_finish(self, session):
    session['Finish'] = worQt_timer.get_today()
    session['duration'] = session['Finish'] - session['Start']


def create_file_log():
    date = worQt_timer.get_today().isoformat()
    login = os.getuid()
    file_log = 'worklog.l0g'
    with open(file_log, 'a') as out_log:
        out_log.close()
    return file_log


def create_file_error():
    date = worQt_timer.get_today().isoformat()
    login = os.getuid()
    file_error = 'error.l0g'
    with open(file_error, 'a') as out_error:
        out_error.close()
    return file_error


def get_file_log():
    file_log = 'worklog.l0g'
    return file_log if os.path.exists(file_log) else create_file_log()


def get_file_error():
    file_error = 'error.l0g'
    return file_log if os.path.exists(file_error) else create_file_error()


def save_damaged_log(path):
    shutil.copyfile(path, '{}_{}.damage'.format(worQt_timer.get_today(), path))


def log_dump_crash():
    pass


def log_write_action(session):
    file = get_file_log()
    with open(file, 'r+') as out:
        try:
            data = json.load(out)
        except:
            save_damaged_log(file)
            data = {'sessions': []}
        data['sessions'].append(session)
        out.seek(0)
        json.dump(data, out)
