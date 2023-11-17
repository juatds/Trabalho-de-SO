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
    def __init__(self, tamanho_pagina, tamanho_processo):
        self.tamanho_pagina = tamanho_pagina
        self.tamanho_processo = tamanho_processo
        self.quantidade_paginas = tamanho_processo // tamanho_pagina
        self.info_paginas = {}
        for i in range(self.quantidade_paginas):
            self.info_paginas[i] = InfoTabela()

    def mapear_pagina(self, endereco_virtual):
        numero_pagina = endereco_virtual // self.tamanho_pagina
        return self.info_paginas.get(numero_pagina)

    def carregar_pagina(self, numero_pagina, numero_quadro):
        self.info_paginas[numero_pagina].modificada = False
        self.info_paginas[numero_pagina].presente = True
        self.info_paginas[numero_pagina].numero_quadro = numero_quadro

    def verificador_modificacao(self, numero_quadro):
        for numero_pagina, info_pagina in self.info_paginas.items():
            if info_pagina.numero_quadro == numero_quadro:
                return info_pagina.modificada, numero_pagina


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

    def atualiza_pagina(self, numero_processo, numero_pagina, pagina):
        paginas = self.processos[numero_processo]
        paginas[numero_pagina] = pagina
        self.carregar_paginas(paginas, numero_processo)


class GerenciadorMemoria:
    def __init__(self, tamanho_ms, tamanho_memoria, tamanho_pagina):
        self.ms = MemoriaSecundaria(tamanho_ms, tamanho_pagina)
        self.mp = MemoriaPrincipal(tamanho_memoria, tamanho_pagina)
        self.tabelas_paginas = {}
        self.lru = []
        self.aux = []

    def atualiza_lru(self, numero_quadro, numero_processo):
        if self.lru.count(numero_quadro) == 1:
            aux = self.lru.index(numero_quadro)
            self.aux.pop(aux)
            self.lru.remove(numero_quadro)
        self.lru.append(numero_quadro)
        self.aux.append(numero_processo)

    def criar_processo(self, numero_processo, tamanho_imagem):
        tabela_paginas = TabelaPaginas(tamanho_pagina=self.mp.tamanho_quadro, tamanho_processo=tamanho_imagem)
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
                    self.atualiza_lru(k, numero_processo)
                    tabela_paginas.carregar_pagina(i, k)
            else:
                for i, k in enumerate(range(self.mp.quantidade_quadros - quadros_livres,
                                            self.mp.quantidade_quadros - quadros_livres + quantidade_de_paginas)):
                    self.mp.quadros[k] = paginas[i]
                    self.atualiza_lru(k, numero_processo)
                    tabela_paginas.carregar_pagina(i, k)
        self.tabelas_paginas[numero_processo] = tabela_paginas

    def busca_mp(self, numero_processo, endereco):

        # obtem a tabela de paginas associada ao processo
        tabela_paginas = self.tabelas_paginas.get(numero_processo)

        # obtem a info_pagina correspondente na tabela
        info_pagina = tabela_paginas.mapear_pagina(endereco)

        # trata a falta de info_pagina, chamando o método correspondente
        if not info_pagina.presente:
            # calcula o numero da pagina com base no endereço virtual
            numero_pagina = endereco // tabela_paginas.tamanho_pagina
            self.tratar_falta_pagina(numero_processo, numero_pagina)

            # obtem a tabela de paginas atualizada
            tabela_paginas = self.tabelas_paginas.get(numero_processo)

            # obtem a info_pagina correspondente na nova tabela
            info_pagina = tabela_paginas.mapear_pagina(endereco)

        self.atualiza_lru(info_pagina.numero_quadro, numero_processo)

        # obtem a pagina apartir do info_pagina
        pagina = self.mp.quadros[info_pagina.numero_quadro]

        # obtem a informação apartir do ofset
        ofset = endereco % tabela_paginas.tamanho_pagina
        return pagina.infos[ofset]

    def tratar_falta_pagina(self, numero_processo, numero_pagina):

        numero_quadro_retirado = self.lru.pop(0)
        processo_quadro_retirado = self.aux.pop(0)

        tabela_pagina_quadro_retirado = self.tabelas_paginas.get(processo_quadro_retirado)

        if tabela_pagina_quadro_retirado is not None:
            verificador_modificacao, numero_pagina_retirado = tabela_pagina_quadro_retirado.verificador_modificacao(
                numero_quadro_retirado)

            if verificador_modificacao:
                pagina_retirada = self.mp.quadros[numero_quadro_retirado]

                self.ms.atualiza_pagina(processo_quadro_retirado, numero_pagina_retirado, pagina_retirada)

        # Obtém a tabela de páginas associada ao processo
        tabela_paginas = self.tabelas_paginas.get(numero_processo)

        nova_pagina = self.ms.mapear_pagina(numero_processo, numero_pagina)

        self.mp.quadros[numero_quadro_retirado] = nova_pagina

        tabela_paginas.carregar_pagina(numero_pagina, numero_quadro_retirado)

        self.tabelas_paginas[numero_processo] = tabela_paginas


    def escreve_mp(self, numero_processo, endereco, valor):

        # obtem a tabela de paginas associada ao processo
        tabela_paginas = self.tabelas_paginas.get(numero_processo)

        # obtem a info_pagina correspondente na tabela
        info_pagina = tabela_paginas.mapear_pagina(endereco)

        # calcula o numero da pagina com base no endereço virtual
        numero_pagina = endereco // tabela_paginas.tamanho_pagina

        # trata a falta de info_pagina, chamando o método correspondente
        if not info_pagina.presente:
            self.tratar_falta_pagina(numero_processo, numero_pagina)

            # obtem a tabela de paginas atualizada
            tabela_paginas = self.tabelas_paginas.get(numero_processo)

            # obtem a info_pagina correspondente na nova tabela
            info_pagina = tabela_paginas.mapear_pagina(endereco)

        self.atualiza_lru(info_pagina.numero_quadro, numero_processo)

        # obtem a pagina apartir do info_pagina
        pagina = self.mp.quadros[info_pagina.numero_quadro]

        # obtem a informação apartir do ofset
        ofset = endereco % tabela_paginas.tamanho_pagina
        pagina.infos[ofset] = valor
        self.mp.quadros[info_pagina.numero_quadro] = pagina
        tabela_paginas.info_paginas[numero_pagina].modificada = True
        self.tabelas_paginas[numero_processo] = tabela_paginas

    def termina_processo(self, numero_processo):

        # Lógica para terminar o processo
        tabela_paginas = self.tabelas_paginas.get(numero_processo)

        for numero_pagina, info_pagina in tabela_paginas.info_paginas.items():
            if info_pagina.presente:
                if self.lru.count(info_pagina.numero_quadro) == 1:
                    aux = self.lru.index(info_pagina.numero_quadro)
                    self.aux.pop(aux)
                    self.lru.remove(info_pagina.numero_quadro)
                self.lru.insert(0, info_pagina.numero_quadro)
                self.aux.insert(0, numero_processo)

        # Remover a tabela de páginas do processo terminado
        del self.tabelas_paginas[numero_processo]
        # Remover o processo da ms
        del self.ms.processos[numero_processo]

    def carregar_ms(self, numero_processo):
        # Logica verificar modicicacao e atualizar na ms
        tabela_paginas = self.tabelas_paginas.get(numero_processo)

        for numero_pagina, info_pagina in tabela_paginas.info_paginas.items():
            if info_pagina.presente:
                if info_pagina.modificada:
                    pagina = self.mp.quadros[info_pagina.numero_quadro]
                    self.ms.atualiza_pagina(numero_processo, numero_pagina, pagina)
                if self.lru.count(info_pagina.numero_quadro) == 1:
                    aux = self.lru.index(info_pagina.numero_quadro)
                    self.aux.pop(aux)
                    self.lru.remove(info_pagina.numero_quadro)
                self.lru.insert(0, info_pagina.numero_quadro)
                self.aux.insert(0, numero_processo)
                info_pagina.presente = False

        self.tabelas_paginas[numero_processo] = tabela_paginas


def trabalho_so():
    # Leitura do arquivo com a lista de execução
    GM = GerenciadorMemoria(32768, 1024, 16)
    with open('arquivo_de_entrada.txt', 'r') as arquivo:
        for linha in arquivo:
            # Split da linha
            vet = linha.split()
            numero_processo = int(vet[0][1:])
            comando = vet[1]

            # Executar a ação com base no comando
            if comando == 'C':
                tamanho_processo = int(vet[2])
                tipo = vet[3]
                if tipo == 'KB':
                    GM.criar_processo(numero_processo, tamanho_processo * (2 ** 10))
                elif tipo == 'MB':
                    GM.criar_processo(numero_processo, tamanho_processo * (2 ** 20))
                elif tipo == 'GB':
                    GM.criar_processo(numero_processo, tamanho_processo * (2 ** 30))
            elif comando == 'P':
                endereco_logico = int(vet[2][1:-2])
                info = GM.busca_mp(numero_processo, endereco_logico)
                print(f"Instrução sob a informação {info}")
            elif comando == 'R':
                endereco_logico = int(vet[2][1:-2])
                info = GM.busca_mp(numero_processo, endereco_logico)
                print(f"Leitura da informação do endereço lógico {endereco_logico}: {info}")
            elif comando == 'W':
                endereco_logico = int(vet[2][1:-2])
                valor = int(vet[3])
                GM.escreve_mp(numero_processo, endereco_logico, valor)
            elif comando == 'I':
                dispositivo = vet[2]
                GM.carregar_ms(numero_processo)
            elif comando == 'T':
                GM.termina_processo(numero_processo)


if __name__ == "__main__":
    trabalho_so()
