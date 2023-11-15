class Pagina:
    def _init_(self, tamanho_pagina):
        self.infos = [None] * tamanho_pagina
        for i in range(tamanho_pagina):
            self.infos[i] = i


class InfoTabela:
    def _init_(self, numero_quadro=None, presente=False, modificada=False):
        self.numero_quadro = numero_quadro
        self.presente = presente
        self.modificada = modificada


class TabelaPaginas:
    def _init_(self, tamanho_pagina):
        self.tamanho_pagina = tamanho_pagina
        self.paginas = {}

    def mapear_pagina(self, endereco_virtual):
        numero_pagina = endereco_virtual // self.tamanho_pagina
        return self.paginas.get(numero_pagina)

    def carregar_pagina(self, numero_pagina, numero_quadro):
        self.paginas[numero_pagina] = InfoTabela(numero_quadro=numero_quadro, presente=True, modificada=False)


class MemoriaPrincipal:
    def _init_(self, tamanho_total, tamanho_quadro):
        self.tamanho_total = tamanho_total
        self.tamanho_quadro = tamanho_quadro
        self.quantidade_quadros = tamanho_total // tamanho_quadro
        self.quadros = [None] * self.quantidade_quadros

    def quadros_livres(self):
        if self.quadros[-1] is not None:
            return 0
        for i in range(self.quantidade_quadros):
            if self.quadros[i] is None:
                return self.quantidade_quadros - i


class MemoriaSecundaria:
    def _init_(self, tamanho_total, tamanho_pagina):
        self.tamanho_total = tamanho_total
        self.quantidade_paginas = tamanho_total // tamanho_pagina
        self.processos = {}

    def mapear_pagina(self, numero_processo, numero_pagina):
        paginas = self.processos.get(numero_processo)
        return paginas[numero_pagina]

    def carregar_paginas(self, paginas, numero_processo):
        self.processos[numero_processo] = paginas


class GerenciadorMemoria:
    def _init_(self, tamanho_ms, tamanho_memoria, tamanho_pagina):
        self.ms = MemoriaSecundaria(tamanho_ms, tamanho_pagina)
        self.mp = MemoriaPrincipal(tamanho_memoria, tamanho_pagina)
        self.tabelas_paginas = {}
        self.lru = []

    def criar_processo(self, numero_processo, tamanho_imagem):
        tabela_paginas = TabelaPaginas(tamanho_pagina=self.mp.tamanho_quadro)
        quantidade_de_paginas = tamanho_imagem // self.mp.tamanho_quadro
        paginas = [None] * quantidade_de_paginas
        for i in range(quantidade_de_paginas):
            paginas[i] = Pagina(self.mp.tamanho_quadro)
        quadros_livres = self.mp.quadros_livres()
        if quadros_livres != 0:
            if quadros_livres < quantidade_de_paginas:
                for i, k in enumerate(range(self.mp.quantidade_quadros - quadros_livres - 1, self.mp.quantidade_quadros)):
                    self.mp.quadros[k] = paginas[i]
                    tabela_paginas.carregar_pagina(i, k)
            else:
                for i, k in enumerate(range(self.mp.quantidade_quadros - quadros_livres - 1, self.mp.quantidade_quadros)):
                    self.mp.quadros[k] = paginas[i]
                    tabela_paginas.carregar_pagina(i, k)
        self.tabelas_paginas[numero_processo] = tabela_paginas

    def busca_mp(self, numero_processo, endereco):
        
        #obtem a tabela de paginas associada ao processo
        tabela_paginas = self.tabela_paginas.get(numero_processo)

        if tabela_paginas is None:
            print(f"Processo {numero_processo} não existe.")
            return None
            
        #calcula o numero da pagina com base no endereço virtual
        numero_pagina = endereco // tabela_paginas.tamanho_pagina
        
        #obtem a pagina correspondente na tabela
        pagina = tabela_paginas.mapear_pagina(endereco)

        if pagina is None or not pagina.presente:
            
            #trata a falta de pagina, chamando o método correspondente
            self.tratar_falta_pagina(numero_processo, numero_pagina)
            
        #obtem o numero do quadro e o endereço fisico
        numero_quadro = pagina.numero_quadro
        endereco_fisico = numero_quadro * tabela_paginas.tamanho_pagina + (endereco % tabela_paginas.tamanho_pagina)

        return endereco_fisico

    def tratar_falta_pagina(self, numero_processo, numero_pagina):

        # Lógica para trazer a página da memória secundária para a memória principal
        # ...

    def busca_ms(self,numero_processo, endereco):

        # Lógica para execução de operações de leitura na mp
        # ...


def trabalho_so():
    GM = GerenciadorMemoria(32768, 1024, 16)

    # Leitura do arquivo com lista de execução e chamada das funções do GM segundo a instrução solicitada
    # ...


if __name__ == "__main__":
    trabalho_so()
