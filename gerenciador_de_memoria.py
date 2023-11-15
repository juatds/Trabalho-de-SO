class Pagina:
    def __init__(self, tamanho_pagina):
        self.infos = [None] * tamanho_pagina
        for i in range(tamanho_pagina):
            self.infos[i] = i


class InfoTabela:
    def __init__(self, numero_quadro=None, presente=False, modificada=False):
        self.numero_quadro = numero_quadro
        self.presente = presente
        self.modificada = modificada


class TabelaPaginas:
    def __init__(self, tamanho_pagina):
        self.tamanho_pagina = tamanho_pagina
        self.paginas = {}

    def mapear_pagina(self, endereco_virtual):
        numero_pagina = endereco_virtual // self.tamanho_pagina
        return self.paginas.get(numero_pagina)

    def carregar_pagina(self, numero_pagina, numero_quadro):
        self.paginas[numero_pagina] = InfoTabela(numero_quadro=numero_quadro, presente=True, modificada=False)


class MemoriaPrincipal:
    def __init__(self, tamanho_total, tamanho_quadro):
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
    def __init__(self, tamanho_total, tamanho_pagina):
        self.tamanho_total = tamanho_total
        self.quantidade_paginas = tamanho_total // tamanho_pagina
        self.processos = {}

    def mapear_pagina(self, numero_processo, numero_pagina):
        paginas = self.processos.get(numero_processo)
        return paginas[numero_pagina]

    def carregar_paginas(self, paginas, numero_processo):
        self.processos[numero_processo] = paginas


class GerenciadorMemoria:
    def __init__(self, tamanho_ms, tamanho_memoria, tamanho_pagina):
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
        self.ms.carregar_paginas(paginas, numero_processo)
        quadros_livres = self.mp.quadros_livres()
        if quadros_livres != 0:
            if quadros_livres < quantidade_de_paginas:
                for i, k in enumerate(range(self.mp.quantidade_quadros - quadros_livres, self.mp.quantidade_quadros)):
                    self.mp.quadros[k] = paginas[i]
                    tabela_paginas.carregar_pagina(i, k)
            else:
                for i, k in enumerate(range(self.mp.quantidade_quadros - quadros_livres, self.mp.quantidade_quadros - quadros_livres + quantidade_de_paginas)):
                    self.mp.quadros[k] = paginas[i]
                    tabela_paginas.carregar_pagina(i, k)
        self.tabelas_paginas[numero_processo] = tabela_paginas

    def busca_mp(self, numero_processo, endereco):

        # obtem a tabela de paginas associada ao processo
        tabela_paginas = self.tabelas_paginas.get(numero_processo)

        # obtem a endereco_quadro correspondente na tabela
        endereco_quadro = tabela_paginas.mapear_pagina(endereco)

        # trata a falta de endereco_quadro, chamando o método correspondente
        if endereco_quadro is None:
            # calcula o numero da pagina com base no endereço virtual
            numero_pagina = endereco // tabela_paginas.tamanho_pagina
            self.tratar_falta_pagina(numero_processo, numero_pagina)

            # obtem a tabela de paginas atualizada
            tabela_paginas = self.tabelas_paginas.get(numero_processo)

            # obtem a endereco_quadro correspondente na nova tabela
            endereco_quadro = tabela_paginas.mapear_pagina(endereco)

        # obtem a pagina apartir do endereco_quadro
        pagina = self.mp.quadros[endereco_quadro.numero_quadro]

        # obtem a informação apartir do ofset
        ofset = endereco % tabela_paginas.tamanho_pagina
        return pagina.infos[ofset]

    def tratar_falta_pagina(self, numero_processo, numero_pagina):
        # Obtém a tabela de páginas associada ao processo
        tabela_paginas = self.tabela_paginas.get(numero_processo)

        if tabela_paginas is None:
            print(f"Processo {numero_processo} não possui tabela de páginas.")
            return

        # Lógica para escolher um quadro livre na memória principal
        # (Essa parte pode variar dependendo do algoritmo de substituição utilizado)
        quadro_livre = self.encontrar_quadro_livre()

        if quadro_livre is not None:
            # Carrega a página da memória secundária para o quadro livre na memória principal
            tabela_paginas.carregar_pagina(numero_pagina, quadro_livre)
            print(f"Página {numero_pagina} do Processo {numero_processo} carregada no Quadro {quadro_livre}.")

            # Lógica adicional, se necessário (por exemplo, gravação da página de volta ao disco se ela foi modificada)
            # ...

        else:
            print("Não há quadros livres na memória principal. Aplicar algoritmo de substituição de página.")
            # Lógica para aplicar o algoritmo de substituição de página (por exemplo, LRU)
            # ...

    def encontrar_quadro_livre(self):
        # Encontrar o primeiro quadro livre na memória principal
        for i, quadro in enumerate(self.memoria_principal.quadros):
            if quadro is None:
                return i  # Retorna o índice do quadro livre
        return None  # Retorna None se não houver quadros livres


    def busca_ms(self, numero_processo, endereco):
        # Obtém a tabela de páginas associada ao processo
        tabela_paginas = self.tabela_paginas.get(numero_processo)
    
        if tabela_paginas is None:
            print(f"Processo {numero_processo} não possui tabela de páginas.")
            return None
    
        # Calcula o número da página com base no endereço virtual
        numero_pagina = endereco // tabela_paginas.tamanho_pagina
        # Obtém a página correspondente na tabela
        pagina = tabela_paginas.mapear_pagina(endereco)
    
        if pagina is None:
            print(f"Página {numero_pagina} não está mapeada para o processo {numero_processo}.")
            return None
    
        if not pagina.presente:
            print(f"Página {numero_pagina} não está na memória principal. Realizando busca na memória secundária.")
    
            # Lógica para buscar a página na memória secundária (por exemplo, carregar do disco)
            # ...
    
            # Atualiza a tabela de páginas indicando que a página está presente
            tabela_paginas.carregar_pagina(numero_pagina, numero_quadro)
            print(f"Página {numero_pagina} do Processo {numero_processo} carregada na memória principal.")
        
        # Obtém o número do quadro e o endereço físico
        numero_quadro = pagina.numero_quadro
        endereco_fisico = numero_quadro * tabela_paginas.tamanho_pagina + (endereco % tabela_paginas.tamanho_pagina)
    
        return endereco_fisico
        


def trabalho_so():
    GM = GerenciadorMemoria(32768, 1024, 16)
    
    # Leitura do arquivo com lista de execução e chamada das funções do GM segundo a instrução solicitada
    # ...


if __name__ == "__main__":
    trabalho_so()
