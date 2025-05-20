from graphviz import Digraph

class No:
    def __init__(self, valor):
        self.valor = valor
        self.esq = None
        self.dir = None

class Arvore:
    def __init__(self):
        self.raiz = None

    def inserir(self, valor):
        self.raiz = self._inserir_recursivo(self.raiz, valor)

    def _inserir_recursivo(self, no, valor):
        if no is None:
            return No(valor)
        elif valor < no.valor:
            no.esq = self._inserir_recursivo(no.esq, valor)
        elif valor > no.valor:
            no.dir = self._inserir_recursivo(no.dir, valor)
        return no

def desenhar_arvore(no, dot=None):
    if dot is None:
        dot = Digraph()
        dot.graph_attr['rankdir'] = 'TB'
        dot.attr('node', shape='circle')

    if no:
        dot.node(str(no.valor))
        if no.esq:
            dot.edge(str(no.valor), str(no.esq.valor), label='esq')
            desenhar_arvore(no.esq, dot)
        if no.dir:
            dot.edge(str(no.valor), str(no.dir.valor), label='dir')
            desenhar_arvore(no.dir, dot)
    return dot

# Programa principal
arv = Arvore()
print("Inserção em Árvore Binária de Busca")

while True:
    valor = input("Digite um valor inteiro ou 'sair' para encerrar: ")
    if valor.lower() == 'sair':
        break
    try:
        arv.inserir(int(valor))
    except ValueError:
        print("Por favor, insira um número inteiro válido.")

print("Inserção finalizada.")

print("Gerando visualização da árvore...")
dot = desenhar_arvore(arv.raiz)
dot.render('arvore_binaria', format='png', cleanup=True)
print("Árvore salva como 'arvore_binaria.png'")
