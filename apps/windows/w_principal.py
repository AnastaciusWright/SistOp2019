from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow



from apps.ui.w_principal import Ui_MainWindow

from apps.windows.w_cargarProceso import W_cargarProceso

from apps.windows.w_configuracion1 import W_Configuracion1 

from Clases.Procesador import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from crearDB import session, Proceso, Presets, Particiones, Base


engine = create_engine('sqlite:///SistOp.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


class W_Main(QMainWindow):
	#---- inicio constructor ---#
	def __init__(self):
		QMainWindow.__init__(self)
		self.ventana = Ui_MainWindow()
		self.ventana.setupUi(self)
		#-- aca genera la imagen en principal
		pixmap = QtGui.QPixmap('D:\Desktop\pyqt\SistOp2019\proc8.png')
		self.ventana.label_imagen.setPixmap(pixmap)
		# -- 

		self.dialogs = list()

		self.ventana.actionCrear_procesos.triggered.connect(self.crearProceso)
		self.ventana.actionConfiguracion_2.triggered.connect(self.menuConfiguracion1)
		self.ventana.actionSalir.triggered.connect(self.salir)
		self.ventana.actionAyuda.triggered.connect(self.ayuda)
		self.ventana.actionAcerca_de.triggered.connect(self.AcercaDe)
		self.ventana.btn_comenzar.clicked.connect(self.comenzar)
		
		self.ventana.pushButton.clicked.connect(self.actualizar)

		self.ventana.spinBox_quantum.setEnabled(False)
		
		

		procesos = session.query(Proceso).all()
		presets = session.query(Presets).all()
		
		
		
		#for p in presets: #recorre presets y lista descripcion
		self.mostrarDesc(presets)
		#self.ventana.comboBox_seleccionPreConf.addItem(str(p.descripcion))
		self.mostrarProc(procesos)
		
		

		self.ventana.comboBox_seleccionAlgoritmo.addItems(["FCFS", "RR", "MVQ"])
		self.ventana.comboBox_seleccionAlgoritmo.currentTextChanged.connect(self.habilitarQuantum)

		self.ventana.comboBox_cargarProceso.currentTextChanged.connect(self.listar)
		
		self.habilitarQuantum()
		self.listar()
		#setCurrentIndex
	#----- fin constructor ----#


	def mostrarDesc(self, presets):
		for p in presets: #recorre presets y lista descripcion
			
			self.ventana.comboBox_seleccionPreConf.addItem(str(p.descripcion))
	
	def mostrarProc(self, procesos):
		listaaux=[]
		for p in procesos:
			if str(p.id_batch) not in listaaux:
				listaaux.append(str(p.id_batch))
		for x in listaaux:
			self.ventana.comboBox_cargarProceso.addItem(x)
		self.listar()

	def crearProceso(self):
		ventana = W_cargarProceso()
		self.dialogs.append(ventana)
		ventana.show()
	
	def menuConfiguracion1(self):
		ventanaConfig = W_Configuracion1()
		self.dialogs.append(ventanaConfig)
		ventanaConfig.show()
		
	def actualizar(self):
		presets = session.query(Presets).all()
		self.ventana.comboBox_seleccionPreConf.clear()
		for p in presets: #recorre presets y lista descripcion
			
			self.ventana.comboBox_seleccionPreConf.addItem(str(p.descripcion))
		self.ventana.comboBox_cargarProceso.clear()
		procesos = session.query(Proceso).all()
		
		self.mostrarProc(procesos)

	def habilitarQuantum(self):
		i=self.ventana.comboBox_seleccionAlgoritmo.currentText()
		if i == "RR":
			self.ventana.spinBox_quantum.setEnabled(True)
		else:
			self.ventana.spinBox_quantum.setEnabled(False)	
	

	def salir(self):
		self.close()

	def ayuda(self):
		pass

	def AcercaDe(self):
		pass

	def comenzar(self):
		algoritmoP = self.ventana.comboBox_seleccionAlgoritmo.currentText()
		if algoritmoP == "FCFS":
			algoritmoP=0
			quantum = 0
		elif algoritmoP =="RR":
			algoritmoP=1
			quantum = self.ventana.spinBox_quantum.value()
		
			
		
		# Realizar una busqueda en la BD para traer el preset que conincida con el ingresado
		desc_config = self.ventana.comboBox_seleccionPreConf.currentText()
		
		preset = session.query(Presets).filter(Presets.descripcion == desc_config).all()

		# Realizar busqueda en la BD para traer y armar una lista con todos los procesos correspondientes al batch
		desc_procesos = self.ventana.comboBox_cargarProceso.currentText()
		procesos = session.query(Proceso).filter(Proceso.id_batch == desc_procesos).all()
<<<<<<< HEAD
		# Realizar busqueda en BD para traer el bach de las particiones correspondientes
		# Al preset seleccionado
=======
		
		# Realizar busqueda en BD para traer el bach de las particiones
>>>>>>> master
		particiones = session.query(Particiones).filter(Particiones.batch == desc_config).all()
		
		# Pasamos al procesador
		core = Procesador()
		
		print("Algoritmo: " +str(algoritmoP), "Quantum: " +str(quantum), "Procesos: ")
		for i in particiones:
			 print("id particion " +str(i.id_part))
		core.Simular(preset[0], procesos,particiones, algoritmoP, quantum)
		'''
		print("Algoritmo: " +str(algoritmoP), "Quantum: " +str(quantum), "Procesos: ")
		for i in particiones:
			 print("id particion " +str(i.id_part))
		print("Fin")
		#print(algoritmoP)
		'''

	def listar(self):
		i = self.ventana.comboBox_cargarProceso.currentText()
		self.ventana.tableWidget.clear()
		self.ventana.tableWidget.clearContents()
		for x in range(0,self.ventana.tableWidget.rowCount()+1):
			self.ventana.tableWidget.removeRow(x)
		self.ventana.tableWidget.removeRow(0)#No sabemos porque es necesario rehacer esto
		q = session.query(Proceso).filter(Proceso.id_batch == i).all()
		for l in q:
			rowPosition = self.ventana.tableWidget.rowCount()
			self.ventana.tableWidget.insertRow(rowPosition)
			self.ventana.tableWidget.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(str(l.id_proc)))
			self.ventana.tableWidget.setItem(rowPosition , 1, QtWidgets.QTableWidgetItem(str(l.tiempo_arribo)))
			self.ventana.tableWidget.setItem(rowPosition , 2, QtWidgets.QTableWidgetItem(str(l.prioridad)))
			self.ventana.tableWidget.setItem(rowPosition , 3, QtWidgets.QTableWidgetItem(str(l.tam_proc)))
			self.ventana.tableWidget.setItem(rowPosition , 4, QtWidgets.QTableWidgetItem(str(l.rafagaCPU)))
