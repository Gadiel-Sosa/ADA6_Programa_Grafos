import networkx as nx
import matplotlib.pyplot as plt

class Estado:
    def __init__(self, nombre):
        self.nombre = nombre
        self.conexiones = [] 
    def agregar_conexion(self, otro_estado, costo):
        self.conexiones.append((otro_estado, costo))
class Grafo:
    def __init__(self):
        self.estados = {}  
    def agregar_estado(self, nombre_estado):
        if nombre_estado not in self.estados:
            self.estados[nombre_estado] = Estado(nombre_estado)
    def agregar_conexion(self, estado1, estado2, costo):
        if estado1 not in self.estados:
            self.agregar_estado(estado1)
        if estado2 not in self.estados:
            self.agregar_estado(estado2)
        self.estados[estado1].agregar_conexion(self.estados[estado2], costo)
        self.estados[estado2].agregar_conexion(self.estados[estado1], costo)
    def mostrar_estados_y_conexiones(self):
        print("Estados y sus conexiones:")
        for estado in self.estados.values():
            conexiones = ", ".join([f"{vecino.nombre} (costo: {costo})" for vecino, costo in estado.conexiones])
            print(f"{estado.nombre}: {conexiones}")
    def recorrer_sin_repetir(self, actual, visitados, costo):
        if len(visitados) == len(self.estados):  
            return costo
        costo_minimo = float('inf')
        for vecino, costo_traslado in actual.conexiones:
            if vecino not in visitados:
                nuevo_costo = self.recorrer_sin_repetir(vecino, visitados + [vecino], costo + costo_traslado)
                costo_minimo = min(costo_minimo, nuevo_costo)
        return costo_minimo
    def recorrer_con_repeticion(self, actual, visitados, costo):
        if len(visitados) >= len(self.estados):  
            return costo
        costo_minimo = float('inf')
        for vecino, costo_traslado in actual.conexiones:
            nuevo_costo = self.recorrer_con_repeticion(vecino, visitados + [vecino], costo + costo_traslado)
            costo_minimo = min(costo_minimo, nuevo_costo)
        return costo_minimo
    def dibujar_grafo(self):
        G = nx.Graph()
        for estado in self.estados.values():
            for vecino, costo in estado.conexiones:
                G.add_edge(estado.nombre, vecino.nombre, weight=costo)
        pos = nx.spring_layout(G) 
        nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=10, font_weight="bold")
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        plt.title("Grafo de Estados con Costos de Traslado")
        plt.show()
grafo = Grafo()
grafo.agregar_conexion("Mérida", "Zacatecas", 11)
grafo.agregar_conexion("Mérida", "San Luis Potosi", 20)
grafo.agregar_conexion("Mérida", "Jalisco", 15)
grafo.agregar_conexion("Zacatecas", "Durango", 25)
grafo.agregar_conexion("Zacatecas", "San Luis Potosi", 30)
grafo.agregar_conexion("San Luis Potosi", "Jalisco", 35)
grafo.agregar_conexion("Jalisco", "Michoacan", 40)
grafo.agregar_conexion("Durango", "Chihuahua", 50)
grafo.agregar_conexion("Michoacan", "Guerrero", 55)
grafo.agregar_conexion("Guerrero", "Chihuahua", 45)

grafo.mostrar_estados_y_conexiones()

estado_inicial = grafo.estados["Mérida"]
costo_sin_repetir = grafo.recorrer_sin_repetir(estado_inicial, [estado_inicial], 0)
costo_con_repeticion = grafo.recorrer_con_repeticion(estado_inicial, [estado_inicial], 0)

print("\nCosto total sin repetir estados:", costo_sin_repetir)
print("Costo total con al menos una repetición:", costo_con_repeticion)

grafo.dibujar_grafo()