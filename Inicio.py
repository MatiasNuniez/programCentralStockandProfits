import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QTableWidgetItem
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from random import randint
import tda_archivos
from datetime import date
from datetime import datetime

class Producto():
    def __init__(self, id, nombre, tipo, precio, fechaventa, descripcion):
        self.id = id
        self.nombre = nombre
        self.tipo = tipo
        self.precio = precio                                #OBJETO Y ATRIBUTOS DEL OBJETO
        self.fechaventa = fechaventa
        self.descripcion = descripcion


#-------------------------------------CLASEPRINCIPAL--------------------------------------------------------#
class MainWindow (QMainWindow):#CLASE PRINCIPAL DEL PROGRAMA
    def __init__(self):
        super().__init__()
        uic.loadUi("Inicio.ui", self)
        pixmap = QPixmap('Inicio.jpg')
        self.inicio.setPixmap(pixmap)
        self.agregar = Agregar()
        self.listar = Listar()
        self.ingresos = Ingresos()
        self.btnagregar.clicked.connect(self.agregarprod)
        self.btnlistar.clicked.connect(self.listarprod)
        self.btncalcular.clicked.connect(self.calcingresos)
#-------------------------------------FUNCIONES--------------------------------------------------------#
    def agregarprod(self):
        self.agregar.exec_()

    def listarprod(self):
        self.listar.exec_()
    
    def calcingresos(self):
        self.ingresos.exec_()
#-------------------------------------SUBCLASE--------------------------------------------------------#
class Agregar (QDialog):#CLASE AGREGAR, DONDE VAMOS A AGREGAR PRODUCTOS Y GUARDARLOS EN UN ARCHIVO LLAMADO "PRODUTOS"
    def __init__(self):
        self.productos = []
        QDialog.__init__(self)
        uic.loadUi("Agregar.ui", self)
        self.Agrebtnagregar.clicked.connect(self.getdataagr)
        self.Agrebtnagregar.clicked.connect(self.agrvacio)
#-------------------------------------FUNCIONES--------------------------------------------------------#
    def getdataagr(self):#OBTENEMOS LOS DATOS DE LOS LINETEXT, LOS GUARDAMOS Y LOS ESCRIBIMOS EN UN ARCHIVO COMO UN OBJETO PRODUCTO
        idd = randint(0,1000000)
        id = str(idd)
        nombre = self.Agrenom.text()
        tipo = self.Agretipo.currentText()
        precio = self.Agreprecio.text()
        descripcion = self.Agredesc.text()
        fechaventa = date.today()
        producto = Producto(id, nombre, tipo, precio, fechaventa, descripcion)
        archproductos = tda_archivos.abrir("productos")
        tda_archivos.escribir(archproductos, producto)
        tda_archivos.cerrar(archproductos)

    def agrvacio(self):#PONEMOS EN VACIO LOS LINETEXT PARA QUE NO SE QUEDE GUARDADO EL ATRIBUTO ANTERIOR
        self.Agrenom.setText("")
        self.Agreprecio.setText("")
        self.Agredesc.setText("")
        
#-------------------------------------SUBCLASE--------------------------------------------------------#
class Ingresos (QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("Ingresos.ui", self)
        self.btncalcular.clicked.connect(self.getdataing)
        self.btncalcular.clicked.connect(self.ingvacio)
#-------------------------------------FUNCIONES--------------------------------------------------------#
    def getdataing(self): #OBTENEMOS LOS DATOS DE LA CLASE INGRESO EXACTAMEENTE DE SUS LINETEXT Y HACEME LA COMPARACION
        total = 0 
        format = '%Y-%m-%d'
        fechainicios = self.Fechainicio.toPlainText()
        fechafins = self.Fechafin.toPlainText()
        fechainicio = datetime.strptime(fechainicios, format).date()
        fechafin = datetime.strptime(fechafins, format).date()
        productos = tda_archivos.abrir("productos")
        for i in range (len(productos)):
            producto = tda_archivos.leer(productos, i)
            if (((producto.fechaventa)) >= (fechainicio)) and ((producto.fechaventa)<= (fechafin)):
                total = total + int(producto.precio)
        self.Recaudado.setText(str(total))
    
    def ingvacio(self):#PONEMOS EN VACIO LOS LINETEXT PARA QUE NO SE QUEDE GUARDADO EL ATRIBUTO ANTERIOR
        self.Fechainicio.setText("")
        self.Fechafin.setText("")
#-------------------------------------SUBCLASE--------------------------------------------------------#
class Listar (QDialog):#DEFINIMOS LAS COLUMNAS Y FILAS CON SUS RESPECTIVOS NOMBRE 
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("Listar.ui", self)
        self.tabla.setRowCount(10)
        self.tabla.setColumnCount(6)
        itemscolumnas = ("ID", "Nombre", "Tipo", "Precio","Fecha Venta", "Descripcion")
        self.tabla.setHorizontalHeaderLabels(itemscolumnas)
        self.btnlistar.clicked.connect(self.listar)

#-------------------------------------FUNCIONES--------------------------------------------------------#
    def listar(self):#OBTENEMOS LOS DATOS DEL ARCHIVO Y LO LISTAMOS ASI SABEMOS LAS VENTAS QUE HICIMOS
        datoarchivo = tda_archivos.abrir("productos")
        for i in range (len(datoarchivo)):
            producto = tda_archivos.leer(datoarchivo, i)
            self.tabla.setItem(i,0, QTableWidgetItem(producto.id))
            self.tabla.setItem(i,1, QTableWidgetItem(producto.nombre))
            self.tabla.setItem(i,2, QTableWidgetItem(producto.tipo))
            self.tabla.setItem(i,3, QTableWidgetItem(producto.precio))
            self.tabla.setItem(i,4, QTableWidgetItem(str(producto.fechaventa)))
            self.tabla.setItem(i,5, QTableWidgetItem(producto.descripcion))
        tda_archivos.cerrar(datoarchivo)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

# with shelve.open('producto') as db:
#     db['nombre'] = producto.nombre
#     for producto in db:
#         print(producto.id)