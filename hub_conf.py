import json

def importarDatos(self, file):
	# self.schema = 
	fichero_datos = open(file)
	datos = json.load(fichero_datos)
	print(file)
	print(datos)


importarDatos("prueba_hub.txt")