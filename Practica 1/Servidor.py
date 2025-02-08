import os
import json
from Archivo import Archivo

class Servidor:
    def __init__(self, pathCarpeta):
        self.pathCarpeta = pathCarpeta
        self.lista_archivos = []
        self.lista_nombres = []
        self.configurationFile = "config.json"

    #Para obtener la lista de archivos en la carpeta especificada
    def obtenerNombresArchivos(self):
        self.lista_nombres = []
        try:
            for arch in os.listdir(self.pathCarpeta): #Obtiene los nombrre de los archivos de la ruta
                if os.path.isfile(os.path.join(self.pathCarpeta, arch)): #Verifica si existe el archivo en la ruta dada
                    #nombre, extension = os.path.splitext(arch) #Separa el nombre y la extension
                    self.lista_nombres.append(arch) #Añadimos a la lista de nombres
        except Exception as e:
            print(f"Error al obtener archivos: {e}")
    
    #Cargar JSON
    def cargarConfiguracionJSON(self):
        try:
            with open(self.configurationFile, "r") as f:
                config = json.load(f)  #Cargar el JSON en un diccionario
            return config
        except Exception as e:
            print(f"Error al cargar la configuración: {e}")
            return None
    
    #Compara las listas de archivos del json y de la obtenida actual
    def estadoActualArchivos(self):
        #Para implementar este metodo ya deben estar cargados los archivos del JSON a la lista de archivos
        if not self.lista_archivos:
            print("Configuracion vacia. Aun no hay archivos")
            return
        #Recorre cada archivo en la lista de la carpeta
        for archivo_carpeta in self.lista_nombres:
            if archivo_carpeta not in self.lista_archivos: 
                #Si el archivo de la carpeta NO esta en la lista del JSON
                #preguntamos al usuario si se podrá publicar, para ello, si el usuario contesta se asigna ese 
                # valor, si no, después de un tiempo establecido, se le asignará un valor predeterminado a 
                # cada archivo.
                nombre, extension = os.path.splitext(archivo_carpeta)
                resp = input(f"¿Desea publicar el archivo {archivo_carpeta}? (y/n)")
                if resp == "y" or resp == "Y":
                    #Hacemos una funcion para cargar a JSON con publico True
                    public = True
                elif resp == "n" or resp == "N":
                    #Hacemos una funcion para cargar a JSON con publico False
                    public = False
                else:
                    print("Opcion no disponible")
                ttl = input(f"Ingrese el TTL para {archivo_carpeta}")
                self.agregarArchivoAlJson(nombre, extension, public, ttl)
                break
        #Recorre cada archivo en la lista del JSON
        for archivo_json in self.lista_archivos:
            nombre_completo = archivo_json.nombre+"."+archivo_json.extension
            if nombre_completo not in self.lista_nombres:
                #Si el archivo del JSON ya no esta en la carpeta
                #Borramos el arch_Json del JSON
                self.eliminarArchivoDelJson(nombre_completo)
                break

    #Se carga el Json a la lista de archivos
    def cargarJsonAListaArchivos(self):
        config = self.cargarConfiguracionJSON()
        if config is None:
            print("Aun no hay archivos cargados")
            return
        for arch_Json in config["archivos"]:
            nombre, extension = os.path.splitext(arch_Json["nombre"])
            self.lista_archivos.append(Archivo(nombre, extension, arch_Json["publicar"], arch_Json["ttl"]))

    #Agregar 1 solo archivo a el json
    def agregarArchivoAlJson(self, nombre, extension, publicar, ttl):
        config = self.cargarConfiguracionJSON()
        if config is None:
            return
        nuevo_archivo = {
            "nombre": f"{nombre}{extension}",
            "publicar": publicar,
            "ttl": ttl
        }
        #Añadir el nuevo archivo a la lista de archivos
        config["archivos"].append(nuevo_archivo)
        # Guardar el archivo JSON con el nuevo archivo añadido
        try:
            with open(self.configurationFile, "w") as f:
                json.dump(config, f, indent=4)  # Guardar el JSON con formato legible
            print(f"El archivo {nombre}{extension} ha sido añadido al JSON.")
        except Exception as e:
            print(f"Error al guardar el archivo JSON: {e}")

    #Eliminar 1 solo archivo del json
    def eliminarArchivoDelJson(self, nombre_archivo):
        config = self.cargarConfiguracion() 
        if config is None:
            return
        #Filtrar la lista de archivos eliminando el archivo que coincide con el nombre
        archivos_actualizados = [archivo for archivo in config["archivos"] if archivo["nombre"] != nombre_archivo]

        if len(archivos_actualizados) == len(config["archivos"]):
            print(f"El archivo '{nombre_archivo}' no se encontró en el JSON")
            return
        #Actualizar la lista de archivos con la lista filtrada
        config["archivos"] = archivos_actualizados
        #Guardar el archivo JSON con el archivo eliminado
        try:
            with open(self.configurationFile, "w") as f:
                json.dump(config, f, indent=4)
            print(f"El archivo '{nombre_archivo}' ha sido eliminado del JSON")
        except Exception as e:
            print(f"Error al guardar el archivo JSON: {e}")

    
    def imprimirLista(self, lista):
        for l in lista:
            print(l)

def main():
    path = r"C:\Users\dayan\OneDrive\Documentos\Practica1"
    #print(f"Contenido del directorio {path}:")
    #print(os.listdir(path))
    s = Servidor(path)
    s.obtenerNombresArchivos()
    #s.subirConfiguracionJson()
    s.imprimirLista(s.lista_nombres)

if __name__ == "__main__":
    main()
