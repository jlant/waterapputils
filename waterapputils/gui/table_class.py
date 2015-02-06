from PyQt4 import QtGui, QtCore

class Table(QtGui.QTableWidget):
	""" Table class """
	
	def __init__(self, data, *args):
		
		super(Table, self).__init__(self, *args)
		self.data = data
		self.setmydata()
		self.resizeColumnsToContents()
		self.resizeRowsToContents()

	def setmydata(self):
		""" Set the data in the table """
		header = []
		for n, key in enumerate(sorted(self.data.keys())):
			header.append(key)
			for m, item in enumerate(self.data[key]):
				newitem = QtGui.QTableWidgetItem(item)
				self.setItem(m, n, newitem)
		self.setHorizonalHeaderLabels(header)