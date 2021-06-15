import shelve

def abrir(ruta):
    return shelve.open(ruta)

def cerrar(archivo):
    archivo.close()

def leer(archivo, pos):
    return archivo[str(pos)]

def escribir(archivo, reg):
    """para guardar un nuevo registro"""
    archivo[str(len(archivo))] = reg

def modificar(archivo, pos, reg):
    """modifica un registro existente"""
    archivo[str(pos)] = reg