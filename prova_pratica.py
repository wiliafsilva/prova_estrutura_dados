from graphviz import Digraph

#Representa um nó da árvore
class No:
    def __init__(self, valor):
        self.valor = valor
        self.esq = None
        self.dir = None

#Construtor da árvore
class Arvore:
    def __init__(self):
        self.raiz = None

#Método de inserção
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
#Método de busca
    def buscar(self, valor):
        return self._buscar_recursivo(self.raiz, valor)

    def _buscar_recursivo(self, no, valor):
        if no is None or no.valor == valor:
            return no
        elif valor < no.valor:
            return self._buscar_recursivo(no.esq, valor)
        else:
            return self._buscar_recursivo(no.dir, valor)
#Método de remoção
    def remover(self, valor):
        self.raiz = self._remover_recursivo(self.raiz, valor)

    def _remover_recursivo(self, no, valor):
        if no is None:
            return None
        if valor < no.valor:
            no.esq = self._remover_recursivo(no.esq, valor)
        elif valor > no.valor:
            no.dir = self._remover_recursivo(no.dir, valor)
        else:
            # Caso 1: nó sem filhos
            if no.esq is None and no.dir is None:
                return None
            # Caso 2: um filho
            elif no.esq is None:
                return no.dir
            elif no.dir is None:
                return no.esq
            # Caso 3: dois filhos
            sucessor = self._minimo(no.dir)
            no.valor = sucessor.valor
            no.dir = self._remover_recursivo(no.dir, sucessor.valor)
        return no
    
#Localiza o sucessor em-ordem (o menor valor da subárvore direita)
    def _minimo(self, no):
        atual = no
        while atual.esq is not None:
            atual = atual.esq
        return atual

#Métodos de percurso (pre-ordem, em-ordem e pos-ordem)
    def pre_ordem(self):
        return self._pre_ordem(self.raiz)

    def _pre_ordem(self, no):
        return ([no.valor] + self._pre_ordem(no.esq) + self._pre_ordem(no.dir)) if no else []

    def em_ordem(self):
        return self._em_ordem(self.raiz)

    def _em_ordem(self, no):
        return (self._em_ordem(no.esq) + [no.valor] + self._em_ordem(no.dir)) if no else []

    def pos_ordem(self):
        return self._pos_ordem(self.raiz)

    def _pos_ordem(self, no):
        return (self._pos_ordem(no.esq) + self._pos_ordem(no.dir) + [no.valor]) if no else []

#Função para desenhar a árvore
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

# Opções do menu usuário
arv = Arvore()

print("Menu Árvore Binária de Busca:")
while True:
    print("\n1 - Inserir valor")
    print("2 - Buscar valor")
    print("3 - Remover valor")
    print("4 - Mostrar percursos")
    print("5 - Mostrar árvore (salva como PNG)")
    print("6 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == '1':
        while True:
            valor = input("Digite um valor inteiro ou 'parar' para voltar ao menu: ")
            if valor.lower() == 'parar':
                break
            try:
                arv.inserir(int(valor))
            except ValueError:
                print("Valor inválido. Digite um número inteiro ou 'parar'.")
    elif opcao == '2':
        valor = input("Digite o valor a buscar: ")
        no = arv.buscar(int(valor))
        if no:
            print(f"Valor {valor} encontrado na árvore.")
        else:
            print(f"Valor {valor} não está na árvore.")
    elif opcao == '3':
        valor = input("Digite o valor a remover: ")
        arv.remover(int(valor))
        print(f"Valor {valor} removido (se existia).")
    elif opcao == '4':
        print("Pré-ordem:", arv.pre_ordem())
        print("Em-ordem:", arv.em_ordem())
        print("Pós-ordem:", arv.pos_ordem())
    elif opcao == '5':
        print("Gerando visualização da árvore...")
        dot = desenhar_arvore(arv.raiz)
        dot.render('arvore_binaria', format='png', cleanup=True)
        print("Árvore salva como 'arvore_binaria.png'")
    elif opcao == '6':
        break
    else:
        print("Opção inválida.")
