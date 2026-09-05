import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pickle


def get_dist(p1, p2):
    return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)


def main():

    '''

    '''

  #matriz = np.array(pickle.load(open("MATRIZ_B.pickle", "rb")))
  #matriz = np.array(pickle.load(open("MATRIZ_C.pickle", "rb")))
  #matriz = np.array(pickle.load(open("MATRIZx9.pickle", "rb")))
  #print(matriz)
  #matriz = matriz-1

  # 0 = Círculo, 1 = Quadrado, 2 = Triângulo
    matriz = np.array([
      [1, 2, 0, 2, 0, 1],
      [2, 2, 1, 0, 1, 2],
      [0, 1, 2, 1, 2, 0],
      [2, 0, 1, 1, 2, 2],
      [0, 1, 2, 1, 2, 0],
      [1, 2, 0, 0, 1, 2]
  ])

    graph = nx.DiGraph()

    rows = len(matriz)
    cols = len(matriz[0])


    mapa_formas = {
      0: ('o', 'green'),
      1: ('s', 'black'),
      2: ('^', 'blue')
  }

    for row in range(rows):
      for column in range(cols):
          value = matriz[row, column]
          if value in mapa_formas:
              shape = mapa_formas[value][0]
              color = mapa_formas[value][1]
              graph.add_node((row, column), shape=shape, color=color, type=value)

    quadrados = [n for n, attr in graph.nodes(data=True) if attr['type'] == 1]
    triangulos = [n for n, attr in graph.nodes(data=True) if attr['type'] == 2]
    circulos = [n for n, attr in graph.nodes(data=True) if attr['type'] == 0]

    quadrados_estrela = []

    for circ in circulos:

      menor_dist = min([get_dist(circ, q) for q in quadrados])
      quadrados_vizinhos = [q for q in quadrados if get_dist(circ, q) == menor_dist]

      for prox_q in quadrados_vizinhos:
          graph.add_edge(circ, prox_q)

          #Quadrado -> Triângulo
          tri_validos = [t for t in triangulos if (t[0] >= prox_q[0] and t[1] == prox_q[1])
                        or (t[1] >= prox_q[1] and t[0] == prox_q[0])]

          if tri_validos:
              prox_t = min(tri_validos, key=lambda t: (get_dist(prox_q, t), -t[1], -t[0]))
              graph.add_edge(prox_q, prox_t)

              #Triângulo -> Quadrado Diagonal
              quad_diagonais = [q for q in quadrados if abs(q[0] - prox_t[0]) == abs(q[1] - prox_t[1]) and q != prox_t]

              if quad_diagonais:
                  prox_q_diag = min(quad_diagonais, key=lambda q: get_dist(prox_t, q))
                  graph.add_edge(prox_t, prox_q_diag)
                  quadrados_estrela.append(prox_q_diag)


    #O último plot deve ser em (18, 18)
    plt.figure(figsize=(18, 18))
    pos = {(row, column): (column, -row) for row, column in graph.nodes()}

    # Desenha Formas Base
    for tipo, (marker, cor) in mapa_formas.items():
      nodos_grupo = [n for n, attr in graph.nodes(data=True) if attr['type'] == tipo]
      nx.draw_networkx_nodes(graph, pos, nodelist=nodos_grupo, node_shape=marker,
                            node_color=cor, node_size=800, edgecolors='white', linewidths=1.5)

    # Desenha as Estrelas
    if quadrados_estrela:
      nx.draw_networkx_nodes(graph, pos,
                            nodelist=list(set(quadrados_estrela)),
                            node_shape='*',
                            node_color='yellow',
                            node_size=1000)

    # Desenha Arestas
    arestas_curvas = [(u, v) for u, v in graph.edges() if graph.nodes[u]['type'] == 2]
    arestas_retas = [(u, v) for u, v in graph.edges() if graph.nodes[u]['type'] != 2]


    if menor_dist > 1.0:
        nx.draw_networkx_edges(graph, pos, edgelist=arestas_retas, edge_color='black', arrows=True, arrowsize=20, width=1.2, connectionstyle="arc3,rad=0.2")
    else:
        nx.draw_networkx_edges(graph, pos, edgelist=arestas_retas, edge_color='black', arrows=True, arrowsize=20, width=1.2)

    nx.draw_networkx_edges(graph, pos, edgelist=arestas_curvas, edge_color='blue', arrows=True, arrowsize=20, width=1.2, connectionstyle="arc3,rad=0.2")

    plt.title("Conhecendo NetworkX", pad=20, fontsize=14)
    #plt.axis('off')
    plt.show()

if __name__ == "__main__":
  main()