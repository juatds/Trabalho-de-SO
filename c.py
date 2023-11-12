class Pagina:
    def init(self, tamanho_pagina):
        self.infos = [None] * tamanho_pagina


class InfoTabela:
    def init(self, numero_quadro=None, presente=False, modificada=False):
        self.numero_quadro = numero_quadro
        self.presente = presente
        self.modificada = modificada


class TabelaPaginas:
    def init(self, tamanho_pagina):
        self.tamanho_pagina = tamanho_pagina
        self.paginas = {}

    def mapear_pagina(self, endereco_virtual):
        numero_pagina = endereco_virtual // self.tamanho_pagina
        return self.paginas.get(numero_pagina)

    def carregar_pagina(self, numero_pagina, numero_quadro):
        self.paginas[numero_pagina] = InfoTabela(numero_quadro=numero_quadro, presente=True, modificada=False)


class MemoriaPrincipal:
    def init(self, tamanho_total, tamanho_quadro):
        self.tamanho_total = tamanho_total
        self.tamanho_quadro = tamanho_quadro
        self.quantidade_quadros = tamanho_total // tamanho_quadro
        self.quadros = [None] * self.quantidade_quadros


class MS:
    def init(self, tamanho_total, tamanho_pagina):
        self.tamanho_total = tamanho_total
        self.quantidade_paginas = tamanho_total // tamanho_pagina
        self.paginas = [None] * self.quantidade_paginas

class GerenciadorMemoria:
    def init(self, tamanho_ms, tamanho_memoria, tamanho_pagina):
        self.disco = MS(tamanho_ms, tamanho_pagina)
        self.memoria_principal = MemoriaPrincipal(tamanho_memoria, tamanho_pagina)
        self.tabela_paginas = {}
        self.lru = []

    def criar_processo(self, numero_processo, tamanho_imagem):
        tabela_paginas = TabelaPaginas(tamanho_pagina=self.memoria_principal.tamanho_quadro)
        self.tabela_paginas[numero_processo] = tabela_paginas

        # Lógica para alocar quadros iniciais para o processo
        # ...

    def busca_mp(self, numero_processo, endereco):
        
        # Lógica para execução de operações de leitura na mp
        # ...

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


if _name_ == "_main_":
    trabalho_so()
