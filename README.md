# 🕸️ Visualizador de Grafos de Formas (em Python) - NetworkX

Projeto desenvolvido em **linguagem Python** para implementação e estudo de **Teoria dos Grafos aplicados ao mapeamento de matrizes**.

O sistema permite transformar uma matriz bidimensional em um grafo direcionado, conectando formas geométricas com base em regras de distância e posição.

---

## 📌 Sobre o Projeto

O **Problema de Roteamento de Formas** é um exercício lógico onde uma matriz contém diferentes valores, representando formas:

* `0` = Círculo (Verde)
* `1` = Quadrado (Preto)
* `2` = Triângulo (Azul)

O objetivo é conectar essas formas obedecendo a regras estritas de distância e alinhamento cartesiano:

```text
[1, 2, 0, 2, 0, 1]
[2, 2, 1, 0, 1, 2]
[0, 1, 2, 1, 2, 0]
[2, 0, 1, 1, 2, 2]
[0, 1, 2, 1, 2, 0]
[1, 2, 0, 0, 1, 2]
```

Neste projeto, o sistema:

* 📍 Mapeia coordenadas matriciais para posições num plano cartesiano;
* 📏 Calcula Distâncias Euclidianas entre os nós;
* 🔗 Estabelece arestas direcionadas baseadas em vizinhos mais próximos;
* ⭐ Destaca o destino final dos caminhos (Nós Estrela);
* 📊 Plota visualmente o grafo complexo gerado.

---

## 🚀 Funcionalidades

### 🗺️ Mapeamento Espacial

O script converte linhas e colunas em coordenadas `(x, y)` invertendo o eixo Y para exibição correta no gráfico:

| Matriz (Linha, Coluna) | Plano Cartesiano (x, y) |
| ---------------------- | ----------------------- |
| `(0, 0)`               | `(0, 0)`                |
| `(1, 0)`               | `(0, -1)`               |
| `(0, 5)`               | `(5, 0)`                |

---

### 📏 Cálculo de Distâncias e Conexões

O projeto implementa o cálculo de **Distância Euclidiana** para encontrar a proximidade entre os nós.

A distância é calculada através da fórmula:

```python
def get_dist(p1, p2):
    return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
```

Onde:
* `p1` e `p2` são as coordenadas dos nós avaliados.

---

### 🎯 Regras de Roteamento (Caminhos)

O algoritmo principal cria as conexões seguindo esta ordem rigorosa:

1. **Círculo → Quadrado:** O círculo se conecta ao quadrado que possui a menor distância euclidiana.
2. **Quadrado → Triângulo:** O quadrado busca triângulos à sua direita (mesma linha, coluna maior) ou abaixo (mesma coluna, linha maior), escolhendo o mais próximo.
3. **Triângulo → Quadrado Diagonal:** O triângulo procura quadrados perfeitamente em sua diagonal (`abs(dx) == abs(dy)`). O mais próximo recebe a conexão final.

---

## 🏗️ Estrutura do Projeto

O programa possui diferentes estruturas responsáveis pelo processamento.

### Matriz de Formas

O tabuleiro inicial é representado por um Numpy Array:

```python
matriz = np.array([
    [1, 2, 0, 2, 0, 1],
    [2, 2, 1, 0, 1, 2],
    [0, 1, 2, 1, 2, 0],
    [2, 0, 1, 1, 2, 2],
    [0, 1, 2, 1, 2, 0],
    [1, 2, 0, 0, 1, 2]
])
```

---

### Estrutura de um Nó

Cada nó no grafo do `NetworkX` é instanciado armazenando atributos visuais e lógicos:

```python
graph.add_node((row, column), shape=shape, color=color, type=value)
```

Ele armazena informações como:
* Coordenada `(row, column)` (que age como ID do nó);
* Formato (marker do matplotlib);
* Cor;
* Tipo original (0, 1 ou 2).

---

### Listas de Coordenadas

O projeto filtra os nós em listas usando List Comprehension para facilitar a busca:

```python
quadrados = [n for n, attr in graph.nodes(data=True) if attr['type'] == 1]
triangulos = [n for n, attr in graph.nodes(data=True) if attr['type'] == 2]
circulos = [n for n, attr in graph.nodes(data=True) if attr['type'] == 0]
```

---

## 🎨 Renderização e Plotagem

Antes de finalizar, o grafo é desenhado usando o `matplotlib.pyplot`. 
As formas base são plotadas primeiro:

```python
nx.draw_networkx_nodes(graph, pos, nodelist=nodos_grupo, node_shape=marker, node_color=cor, node_size=800)
```

O gráfico finalizado tem tamanho `18x18`.

---

## ⭐ Identificação de Nodos Finais (Estrelas)

Para evidenciar onde as cadeias de conexões terminam, o algoritmo identifica os quadrados que foram alvos de um triângulo na etapa final do roteamento.

Eles recebem um destaque visual sobreposto:

```python
node_shape='*',
node_color='yellow',
node_size=1000
```

---

## 🏁 Exibição do Grafo

Quando a lógica finaliza, o programa renderiza a visualização final, dividindo as conexões (arestas) em dois estilos visuais:

* **Arestas Retas (Pretas):** Conexões normais (Círculo → Quadrado).
* **Arestas Curvas (Azuis):** Conexões saindo de triângulos, utilizando `connectionstyle="arc3,rad=0.2"`.

---

## 🖥️ Entrada de Dados (Pickle/Matriz)

O script permite duas formas de leitura da matriz inicial:

1. 📝 **Matriz hardcoded:** Direta no código em `np.array`.
2. 📂 **Arquivos Pickle:** Suporte comentado para carregar matrizes grandes salvos como `MATRIZ_B.pickle`.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* Criação de Grafos Direcionados (`DiGraph`)
* List Comprehensions e Lambdas
* Cálculo de vetores/distâncias

Bibliotecas utilizadas:

```python
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pickle
```

---

## ▶️ Como Executar

### 1. Instale as dependências

```bash
pip install networkx matplotlib numpy
```

### 2. Salve o arquivo

Salve o código Python em um arquivo local, por exemplo, `main.py`.

### 3. Execute o programa

No Linux/macOS:

```bash
python3 main.py
```

No Windows:

```bash
python main.py
```

---

## 📚 Conceitos de Teoria dos Grafos

Este projeto permite aplicar conceitos importantes de **Teoria dos Grafos e Geometria**, incluindo:

* Grafos Direcionados (Dígrafos);
* Nós (Vértices) com múltiplos atributos;
* Arestas condicionais;
* Distância Euclidiana em malhas;
* Algoritmos de busca de vizinhos mais próximos;
* Renderização e topologia visual.

---

## 📈 Tipos de Arestas Geradas

| Característica               | Arestas Retas (Pretas)      | Arestas Curvas (Azuis) |
| ---------------------------- | --------------------------- | ---------------------- |
| Nó de Origem                 | Círculos e Quadrados        | Triângulos             |
| Nó de Destino                | Quadrados e Triângulos      | Quadrados (Diagonais)  |
| Distância limite             | Flexível (qualquer dist)    | Condicionada           |
| Estilo de Plotagem           | Reta padrão (`arc3,rad=0`)  | Curva (`arc3,rad=0.2`) |

---

## 🎯 Objetivos Acadêmicos

O projeto foi desenvolvido com o objetivo de aplicar, na prática, conceitos de **análise de matrizes e grafos matemáticos**, utilizando regras condicionais estritas.

Entre os principais objetivos estão:

* Compreender a transição de matrizes (arrays) para redes (grafos);
* Trabalhar com a biblioteca NetworkX;
* Aplicar condições lógicas envolvendo coordenadas geométricas;
* Customizar visualizações de dados com Matplotlib.

---

## 👨‍💻 Autor

**Arthur Bergamasco Constantino**

Estudante de **Ciência de Dados e Inteligência Artificial**.

---

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para obter detalhes.
