import matplotlib.pyplot as plt
import networkx as nx
import numpy as np



etiquetas_nodos = {
    0: "Centro",
    1: "Norte",
    2: "Este",
    3: "Sur",
    4: "Oeste",
}

matriz_adyacencia = np.array(
    [
        [0, 1, 1, 1, 1],  # Centro conectado con todos
        [1, 0, 1, 0, 1],  # Norte conectado con Centro, Este, Oeste
        [1, 1, 0, 1, 0],  # Este conectado con Centro, Norte, Sur
        [1, 0, 1, 0, 1],  # Sur conectado con Centro, Este, Oeste
        [1, 1, 0, 1, 0],  # Oeste conectado con Centro, Norte, Sur
    ]
)

print("--- MATRIZ DE ADYACENCIA ---")
print(matriz_adyacencia)
print("-" * 30)


G = nx.from_numpy_array(matriz_adyacencia)
G = nx.relabel_nodes(G, etiquetas_nodos)



def validar_euler(graph):
    if not nx.is_connected(graph):
        return False, "El grafo no es conexo."

    grados_impares = [node for node, deg in graph.degree() if deg % 2 != 0]
    num_impares = len(grados_impares)

    if num_impares == 0:
        return (
            True,
            "Existe un CIRCUITO de Euler (recorrido cerrado pasando por todas las calles).",
        )
    elif num_impares == 2:
        return (
            True,
            f"Existe un CAMINO de Euler abierto. Empieza/termina en: {grados_impares}.",
        )
    else:
        return (
            False,
            f"No tiene camino de Euler (tiene {num_impares} nodos de grado impar).",
        )


def validar_hamilton(graph):
    n = len(graph.nodes())
    nodos = list(graph.nodes())

    def backtrack(v, visited, path):
        if len(path) == n:
            return True, path
        for neighbor in graph.neighbors(v):
            if neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)
                res, final_path = backtrack(neighbor, visited, path)
                if res:
                    return True, final_path
                visited.remove(neighbor)
                path.pop()
        return False, []

    for start_node in nodos:
        cumple, camino = backtrack(
            start_node, {start_node}, [start_node]
        )
        if cumple:
            return (
                True,
                f"Existe Camino de Hamilton. Ruta sugerida: {' -> '.join(camino)}",
            )

    return False, "No existe camino de Hamilton."



cumple_euler, msg_euler = validar_euler(G)
cumple_hamilton, msg_hamilton = validar_hamilton(G)

print(f"Camino de Euler: {msg_euler}")
print(f"Camino de Hamilton: {msg_hamilton}")
print("-" * 30)


plt.figure(figsize=(8, 6))
pos = nx.spring_layout(G, seed=42)  


nx.draw_networkx_nodes(
    G, pos, node_color="#1f77b4", node_size=1200, alpha=0.9
)
nx.draw_networkx_edges(G, pos, width=2, edge_color="#888888")
nx.draw_networkx_labels(
    G,
    pos,
    font_color="white",
    font_weight="bold",
    font_size=10,
)

plt.title(
    "Grafo del Problema: Optimización de Ruta de Recolección Urbana",
    fontsize=12,
)
plt.axis("off")
plt.tight_layout()
plt.show()
