class Persona:
    def __init__(self, nombre, correo):
        self.nombre = nombre
        self.correo = correo

class Cliente(Persona):
    def __init__(self, nombre, correo):
        super().__init__(nombre, correo)
        self.frecuente = False

class Empleado(Persona):
    def __init__(self, nombre, correo, rol, inventario):
        super().__init__(nombre, correo)
        self.rol = rol
        self.inventario = inventario

    def reabastecer_ingrediente(self, ingrediente, cantidad):
        self.inventario.reabastecer(ingrediente, cantidad)
        print(f"{self.nombre} ha reabastecido {cantidad} de {ingrediente}.")

class ProductoBase:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

class Bebida(ProductoBase):
    def __init__(self, nombre, precio, tamaño, tipo, opciones=None):
        super().__init__(nombre, precio)
        self.tamaño = tamaño  
        self.tipo = tipo 
        self.opciones = opciones if opciones else {}

    def personalizar(self, opcion, valor):
        self.opciones[opcion] = valor

class Postre(ProductoBase):
    def __init__(self, nombre, precio, vegano=False, sin_gluten=False):
        super().__init__(nombre, precio)
        self.vegano = vegano
        self.sin_gluten = sin_gluten

class Inventario:
    def __init__(self):
        self.ingredientes = {
            "café": 10,
            "leche": 10,
            "azúcar": 10,
            "harina": 10,
            "chocolate": 10,
            "almendra": 5
        }

    def verificar_disponibilidad(self, ingredientes_necesarios):
        for ingrediente, cantidad in ingredientes_necesarios.items():
            if self.ingredientes.get(ingrediente, 0) < cantidad:
                return False
        return True

    def actualizar_inventario(self, ingredientes_necesarios):
        if self.verificar_disponibilidad(ingredientes_necesarios):
            for ingrediente, cantidad in ingredientes_necesarios.items():
                self.ingredientes[ingrediente] -= cantidad
            return True
        return False

    def reabastecer(self, ingrediente, cantidad):
        self.ingredientes[ingrediente] = self.ingredientes.get(ingrediente, 0) + cantidad

class Promocion:
    def __init__(self, descripcion, descuento, min_productos=0, cliente_frecuente=False):
        self.descripcion = descripcion
        self.descuento = descuento
        self.min_productos = min_productos
        self.cliente_frecuente = cliente_frecuente

    def validar(self, pedido):
        cumple_productos = len(pedido.productos) >= self.min_productos
        cumple_cliente = pedido.cliente.frecuente if self.cliente_frecuente else True
        return cumple_productos and cumple_cliente
    
class Pedido:
    ESTADOS = ["pendiente", "en preparación", "entregado"]

    def __init__(self, cliente, inventario):
        self.cliente = cliente
        self.inventario = inventario
        self.productos = []
        self.estado = "pendiente"
        self.total = 0.0

    def agregar_producto(self, producto, ingredientes_necesarios={}):
        if self.inventario.actualizar_inventario(ingredientes_necesarios):
            self.productos.append(producto)
            self.calcular_total()
            print(f"{producto.nombre} agregado al pedido.")
        else:
            print(f"No hay suficiente stock para {producto.nombre}.")

    def calcular_total(self):
        self.total = sum(producto.precio for producto in self.productos)

    def cambiar_estado(self, nuevo_estado):
        if nuevo_estado in self.ESTADOS:
            self.estado = nuevo_estado
        else:
            print("Estado no válido.")

    def aplicar_promocion(self, promocion):
        if promocion.validar(self):
            self.total -= promocion.descuento

#Ejemplo de uso
inventario = Inventario()

cliente1 = Cliente("Carlos", "carlos@email.com")
cliente1.frecuente = True

empleado1 = Empleado("Ana", "ana@email.com", "Barista", inventario)

cafe = Bebida("Café", 5, "Mediano", "Caliente")
cafe.personalizar("leche", "almendra")
cafe.personalizar("azúcar", "sin azúcar")

postre = Postre("Brownie", 8, sin_gluten=True)

pedido1 = Pedido(cliente1, inventario)

pedido1.agregar_producto(cafe, {"café": 2, "leche": 1})
pedido1.agregar_producto(postre, {"harina": 2, "chocolate": 1})

print(f"Total antes de promoción: ${pedido1.total}")

promo = Promocion("Descuento cliente frecuente", 3, min_productos=2, cliente_frecuente=True)
pedido1.aplicar_promocion(promo)

print(f"Total después de promoción: ${pedido1.total}")

pedido1.cambiar_estado("en preparación")
print(f"Estado del pedido: {pedido1.estado}")

empleado1.reabastecer_ingrediente("café", 10)
