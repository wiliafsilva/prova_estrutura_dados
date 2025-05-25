import streamlit as st
import graphviz

# Classe do nó da árvore
class No:
    def __init__(self, valor):
        self.valor = valor
        self.esq = None
        self.dir = None

# Classe da Árvore Binária de Busca
class ArvoreBinariaBusca:
    def __init__(self):
        self.raiz = None

    def inserir(self, valor):
        self.raiz = self._inserir_rec(self.raiz, valor)

    def _inserir_rec(self, no, valor):
        if no is None:
            return No(valor)
        if valor < no.valor:
            no.esq = self._inserir_rec(no.esq, valor)
        elif valor > no.valor:
            no.dir = self._inserir_rec(no.dir, valor)
        return no

    def buscar(self, valor):
        return self._buscar_rec(self.raiz, valor)

    def _buscar_rec(self, no, valor):
        if no is None or no.valor == valor:
            return no
        if valor < no.valor:
            return self._buscar_rec(no.esq, valor)
        return self._buscar_rec(no.dir, valor)

    def remover(self, valor):
        self.raiz = self._remover_rec(self.raiz, valor)

    def _remover_rec(self, no, valor):
        if no is None:
            return no
        if valor < no.valor:
            no.esq = self._remover_rec(no.esq, valor)
        elif valor > no.valor:
            no.dir = self._remover_rec(no.dir, valor)
        else:
            if no.esq is None:
                return no.dir
            elif no.dir is None:
                return no.esq
            temp = self._min_valor(no.dir)
            no.valor = temp.valor
            no.dir = self._remover_rec(no.dir, temp.valor)
        return no

    def _min_valor(self, no):
        atual = no
        while atual.esq is not None:
            atual = atual.esq
        return atual

    def pre_ordem(self):
        resultado = []
        self._pre_ordem(self.raiz, resultado)
        return resultado

    def _pre_ordem(self, no, resultado):
        if no:
            resultado.append(no.valor)
            self._pre_ordem(no.esq, resultado)
            self._pre_ordem(no.dir, resultado)

    def em_ordem(self):
        resultado = []
        self._em_ordem(self.raiz, resultado)
        return resultado

    def _em_ordem(self, no, resultado):
        if no:
            self._em_ordem(no.esq, resultado)
            resultado.append(no.valor)
            self._em_ordem(no.dir, resultado)

    def pos_ordem(self):
        resultado = []
        self._pos_ordem(self.raiz, resultado)
        return resultado

    def _pos_ordem(self, no, resultado):
        if no:
            self._pos_ordem(no.esq, resultado)
            self._pos_ordem(no.dir, resultado)
            resultado.append(no.valor)

    def altura(self, no):
        if no is None:
            return 0
        return 1 + max(self.altura(no.esq), self.altura(no.dir))

    def esta_balanceada(self):
        def verificar(no):
            if no is None:
                return 0, True
            alt_esq, bal_esq = verificar(no.esq)
            alt_dir, bal_dir = verificar(no.dir)
            bal = abs(alt_esq - alt_dir) <= 1
            return 1 + max(alt_esq, alt_dir), bal and bal_esq and bal_dir

        _, balanceada = verificar(self.raiz)
        return balanceada

    def gerar_grafo(self, destaque=None):
        def adicionar_nos(no):
            if no:
                cor = ' filled' if no.valor == destaque else ''
                cor_attr = ', style=filled, fillcolor=lightgreen' if no.valor == destaque else ''
                dot.node(str(no.valor), str(no.valor), **({'style': 'filled', 'fillcolor': 'lightgreen'} if no.valor == destaque else {}))
                if no.esq:
                    dot.edge(str(no.valor), str(no.esq.valor), label="esq")
                    adicionar_nos(no.esq)
                if no.dir:
                    dot.edge(str(no.valor), str(no.dir.valor), label="dir")
                    adicionar_nos(no.dir)

        dot = graphviz.Digraph()
        adicionar_nos(self.raiz)
        return dot

# Inicialização da sessão
if 'arvore' not in st.session_state:
    st.session_state.arvore = ArvoreBinariaBusca()
if 'destaque' not in st.session_state:
    st.session_state.destaque = None

st.set_page_config(page_title="Árvore Binária de Busca", layout="wide")
st.title("🌳 Árvore Binária de Busca (ABB)")

col1, col2 = st.columns([2, 3])

with col1:
    valor = st.number_input("Digite um valor:", step=1, format="%d")
    col1a, col1b, col1c = st.columns(3)
    with col1a:
        if st.button("Inserir"):
            st.session_state.arvore.inserir(valor)
            st.session_state.destaque = None
    with col1b:
        if st.button("Buscar"):
            resultado = st.session_state.arvore.buscar(valor)
            if resultado:
                st.success(f"Encontrado: {valor}")
                st.session_state.destaque = valor
            else:
                st.error(f"{valor} não encontrado na árvore")
    with col1c:
        if st.button("Remover"):
            st.session_state.arvore.remover(valor)
            st.session_state.destaque = None

    st.markdown("---")
    st.markdown("### 📏 Balanceamento:")
    if st.session_state.arvore.esta_balanceada():
        st.success("A árvore está balanceada")
    else:
        st.error("A árvore NÃO está balanceada")

    st.markdown("### 🌀 Percursos:")

    pre_ordem_str = " → ".join(map(str, st.session_state.arvore.pre_ordem()))
    em_ordem_str = " → ".join(map(str, st.session_state.arvore.em_ordem()))
    pos_ordem_str = " → ".join(map(str, st.session_state.arvore.pos_ordem()))

    st.markdown(f"**Pré-ordem:**\n\n{pre_ordem_str}")
    st.markdown(f"**Em-ordem:**\n\n{em_ordem_str}")
    st.markdown(f"**Pós-ordem:**\n\n{pos_ordem_str}")

with col2:
    st.markdown("### 🌐 Visualização da Árvore")
    grafico = st.session_state.arvore.gerar_grafo(st.session_state.destaque)
    st.graphviz_chart(grafico)
