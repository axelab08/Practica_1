from datetime import datetime, timedelta

class Material:
    def __init__(self, titulo, estado='disponible'):
        self.titulo = titulo
        self.estado = estado

class Libro(Material):
    def __init__(self, titulo, autor, genero, estado='disponible'):
        super().__init__(titulo, estado)
        self.autor = autor
        self.genero = genero

class Revista(Material):
    def __init__(self, titulo, edicion, periodicidad, estado='disponible'):
        super().__init__(titulo, estado)
        self.edicion = edicion
        self.periodicidad = periodicidad

class MaterialDigital(Material):
    def __init__(self, titulo, tipo_archivo, enlace):
        super().__init__(titulo, 'disponible')
        self.tipo_archivo = tipo_archivo
        self.enlace = enlace

class Persona:
    def __init__(self, nombre):
        self.nombre = nombre

class Usuario(Persona):
    def __init__(self, nombre):
        super().__init__(nombre)
        self.prestamos = []
        self.multas = 0
    
    def consultar_catalogo(self, catalogo):
        return catalogo.listar_materiales()
    
    def devolver_material(self, prestamo):
        if datetime.now() > prestamo.fecha_devolucion:
            self.multas += 10
        prestamo.material.estado = 'disponible'
        self.prestamos.remove(prestamo)
        print(f"{self.nombre} ha devuelto '{prestamo.material.titulo}'")

class Bibliotecario(Persona):
    def agregar_material(self, sucursal, material):
        sucursal.catalogo.append(material)
    
    def gestionar_prestamo(self, usuario, material):
        if material.estado == 'disponible':
            material.estado = 'prestado'
            prestamo = Prestamo(usuario, material)
            usuario.prestamos.append(prestamo)
            print(f"{material.titulo} ha sido prestado a {usuario.nombre}")
        else:
            print("Material no disponible")
    
    def transferir_material(self, material, sucursal_origen, sucursal_destino):
        if material in sucursal_origen.catalogo:
            sucursal_origen.catalogo.remove(material)
            sucursal_destino.catalogo.append(material)
            print(f"{material.titulo} transferido a {sucursal_destino.nombre}")

class Sucursal:
    def __init__(self, nombre):
        self.nombre = nombre
        self.catalogo = []
    
    def listar_materiales(self):
        return [material.titulo for material in self.catalogo]

class Prestamo:
    def __init__(self, usuario, material):
        self.usuario = usuario
        self.material = material
        self.fecha_prestamo = datetime.now()
        self.fecha_devolucion = self.fecha_prestamo + timedelta(days=14)

class Catalogo:
    def __init__(self, sucursales):
        self.sucursales = sucursales
    
    def listar_materiales(self):
        materiales = []
        for sucursal in self.sucursales:
            materiales.extend(sucursal.listar_materiales())
        return materiales


sucursal_central = Sucursal("Biblioteca Central")
sucursal_norte = Sucursal("Biblioteca Norte")

catalogo = Catalogo([sucursal_central, sucursal_norte])
bibliotecario = Bibliotecario("Ana Gómez")
libro1 = Libro("Cien años de soledad", "Gabriel García Márquez", "Novela")
revista1 = Revista("National Geographic", "Enero 2024", "Mensual")
bibliotecario.agregar_material(sucursal_central, libro1)
bibliotecario.agregar_material(sucursal_norte, revista1)

usuario = Usuario("Carlos Ramírez")
print("Materiales en todas las sucursales:", usuario.consultar_catalogo(catalogo))
bibliotecario.gestionar_prestamo(usuario, libro1)

bibliotecario.gestionar_prestamo(usuario, libro1)
usuario.devolver_material(usuario.prestamos[0])
print(f"Multa acumulada por {usuario.nombre}: {usuario.multas} créditos")
bibliotecario.transferir_material(revista1, sucursal_norte, sucursal_central)
print("Materiales en todas las sucursales después de la transferencia:", catalogo.listar_materiales())
