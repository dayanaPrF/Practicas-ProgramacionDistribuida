class Archivo:
    
    def __init__(self, nombre, extension, publicar, ttl):
        self.nombre = nombre
        self.extension = extension
        self.publicar = publicar
        self.ttl = ttl

    def __str__(self):
        return f"{self.nombre}{self.extension}"