import random


class Pagina:
    def __init__(self, tamanho_pagina):
        self.infos = [None] * tamanho_pagina
        for i in range(tamanho_pagina):
            self.infos[i] = random.randint(0, 100)


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

    def verificador_info(self, numero_quadro):
        for numero_pagina, info_pagina in self.info_paginas.items():
            if info_pagina.numero_quadro == numero_quadro:
                return info_pagina, numero_pagina

    def escrever_tabela(self):
        print("--------------------")
        print("Tabela de Paginas:")
        for p, i in self.info_paginas.items():
            print(f"{p} - Presente: {i.presente} - Modificação: {i.modificada}", end=' ')
            if i.presente:
                print(f"- Quadro: {i.numero_quadro}")
            else:
                print(f"- Quadro: X")
        print("--------------------")


class MemoriaPrincipal:
    def __init__(self, tamanho_total, tamanho_quadro):
        self.tamanho_total = tamanho_total
        self.tamanho_quadro = tamanho_quadro
        self.quantidade_quadros = tamanho_total // tamanho_quadro
        self.quadros = [None] * self.quantidade_quadros

    def quadros_livres(self):
        qnt = 0
        for i in range(self.quantidade_quadros):
            if self.quadros[i] is None:
                qnt += 1
        return qnt

    def imprime_quadros(self):
        print()
        print("Memoria Principal:")
        for i in range(self.quantidade_quadros):
            if self.quadros[i] is not None:
                # vermelho:
                print("\033[F\033[1;31m[]\033[0m", end=" ")
            else:
                # verde:
                print("\033[F\033[1;32m[]\033[0m", end=" ")
        print()

    def imprime_quadro_lru(self, quadro):
        print()
        print("Memoria Principal:")
        for i in range(self.quantidade_quadros):
            if i == quadro:
                # amarelo:
                print("\033[F\033[1;33m[]\033[0m", end=" ")
            elif self.quadros[i] is not None:
                # vermelho:
                print("\033[F\033[1;31m[]\033[0m", end=" ")
            else:
                # verde:
                print("\033[F\033[1;32m[]\033[0m", end=" ")
        print()


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

    def escrever_processos(self):
        print()
        print("Memoria Secundaria:")
        for p in self.processos.keys():
            print(f"P{p}")
        print()

    def escrever_processo(self, numero_processo, numero_pagina):
        print(f"Memoria Secundaria - P{numero_processo}:")
        for i in range(len(self.processos[numero_processo])):
            if i == numero_pagina:
                # amarelo:
                print("\033[F\033[1;33m[]\033[0m", end=" ")
            else:
                # vermelho:
                print("\033[F\033[1;31m[]\033[0m", end=" ")
        print()
        print("--------------------")


class GerenciadorMemoria:
    def __init__(self, tamanho_ms, tamanho_memoria, tamanho_pagina):
        self.ms = MemoriaSecundaria(tamanho_ms, tamanho_pagina)
        self.mp = MemoriaPrincipal(tamanho_memoria, tamanho_pagina)
        self.tabelas_paginas = {}
        self.lru = []
        self.aux = []

    def atualiza_lru(self, numero_quadro, numero_processo):
        print("Atualizando LRU")
        if self.lru.count(numero_quadro) == 1:
            aux = self.lru.index(numero_quadro)
            self.aux.pop(aux)
            self.lru.remove(numero_quadro)
        self.lru.append(numero_quadro)
        self.aux.append(numero_processo)

    def criar_processo(self, numero_processo, tamanho_imagem):
        print("Crinado tabela de paginas")
        tabela_paginas = TabelaPaginas(tamanho_pagina=self.mp.tamanho_quadro, tamanho_processo=tamanho_imagem)
        tabela_paginas.escrever_tabela()
        quantidade_de_paginas = tamanho_imagem // self.mp.tamanho_quadro
        paginas = [None] * quantidade_de_paginas
        for i in range(quantidade_de_paginas):
            paginas[i] = Pagina(self.mp.tamanho_quadro)
        print("Carregando processo em Memoria Secundaria")
        self.ms.carregar_paginas(paginas, numero_processo)
        self.ms.escrever_processos()
        print("Verificando espaço livre em Memoria Principal")
        self.mp.imprime_quadros()
        quadros_livres = self.mp.quadros_livres()
        if quadros_livres != 0:
            i = 0
            if quadros_livres < quantidade_de_paginas:
                for k in range(self.mp.quantidade_quadros):
                    if self.mp.quadros[k] is None:
                        self.mp.quadros[k] = paginas[i]
                        self.atualiza_lru(k, numero_processo)
                        tabela_paginas.carregar_pagina(i, k)
                        i += 1
            else:
                k = 0
                while i < quantidade_de_paginas:
                    if self.mp.quadros[k] is None:
                        self.mp.quadros[k] = paginas[i]
                        self.atualiza_lru(k, numero_processo)
                        tabela_paginas.carregar_pagina(i, k)
                        i += 1
                    k += 1
            self.mp.imprime_quadros()
            tabela_paginas.escrever_tabela()
        self.tabelas_paginas[numero_processo] = tabela_paginas

    def busca_mp(self, numero_processo, endereco):

        # obtem a tabela de paginas associada ao processo
        tabela_paginas = self.tabelas_paginas.get(numero_processo)

        # obtem a info_pagina correspondente na tabela
        info_pagina = tabela_paginas.mapear_pagina(endereco)

        print("Verificando em qual quadro a pagina correspondente se encontra:")
        tabela_paginas.escrever_tabela()
        print(
            f"--> {endereco // tabela_paginas.tamanho_pagina} - Presente: {info_pagina.presente} - Modificação: {info_pagina.modificada} - Quadro: {info_pagina.numero_quadro}")

        # trata a falta de info_pagina, chamando o método correspondente
        if not info_pagina.presente:
            print("Tratando falta de pagina")

            # calcula o numero da pagina com base no endereço virtual
            numero_pagina = endereco // tabela_paginas.tamanho_pagina
            self.tratar_falta_pagina(numero_processo, numero_pagina)

            # obtem a tabela de paginas atualizada
            tabela_paginas = self.tabelas_paginas.get(numero_processo)

            # obtem a info_pagina correspondente na nova tabela
            info_pagina = tabela_paginas.mapear_pagina(endereco)

        self.atualiza_lru(info_pagina.numero_quadro, numero_processo)

        print("Buscando pagina do quadro em Memoria Principal")
        self.mp.imprime_quadro_lru(info_pagina.numero_quadro)

        # obtem a pagina apartir do info_pagina
        pagina = self.mp.quadros[info_pagina.numero_quadro]

        print("Informações do quadro:",end=" ")
        for i in pagina.infos:
            print(i, end=" ")
        print()

        # obtem a informação apartir do ofset
        ofset = endereco % tabela_paginas.tamanho_pagina
        return pagina.infos[ofset]

    def tratar_falta_pagina(self, numero_processo, numero_pagina):

        numero_quadro_retirado = self.lru.pop(0)
        processo_quadro_retirado = self.aux.pop(0)

        print(f"Quadro não utilizado a mais tempo:")

        self.mp.imprime_quadro_lru(numero_quadro_retirado)

        tabela_pagina_quadro_retirado = self.tabelas_paginas.get(processo_quadro_retirado)

        if tabela_pagina_quadro_retirado is not None:
            print("Verificando se o quadro sofreu modificação:")
            info, numero_pagina_retirado = tabela_pagina_quadro_retirado.verificador_info(
                numero_quadro_retirado)

            print(
                f"{numero_pagina_retirado} - Presente: {info.presente} - Modificação: {info.modificada} - Quadro: {info.numero_quadro}")

            if info.modificada:
                pagina_retirada = self.mp.quadros[numero_quadro_retirado]

                print("Atualiza a pagina na Memoria Secundaria")

                self.ms.atualiza_pagina(processo_quadro_retirado, numero_pagina_retirado, pagina_retirada)
        else:
            print("Quadro vazio")

        # Obtém a tabela de páginas associada ao processo
        tabela_paginas = self.tabelas_paginas.get(numero_processo)

        print("Buscando pagina da Memoria Secundaria")

        self.ms.escrever_processo(numero_processo, numero_pagina)

        nova_pagina = self.ms.mapear_pagina(numero_processo, numero_pagina)

        self.mp.quadros[numero_quadro_retirado] = nova_pagina

        tabela_paginas.carregar_pagina(numero_pagina, numero_quadro_retirado)

        print("Atualiza Memoria principal e tabela de paginas")
        tabela_paginas.escrever_tabela()

        self.tabelas_paginas[numero_processo] = tabela_paginas

    def escreve_mp(self, numero_processo, endereco, valor):

        # obtem a tabela de paginas associada ao processo
        tabela_paginas = self.tabelas_paginas.get(numero_processo)

        # obtem a info_pagina correspondente na tabela
        info_pagina = tabela_paginas.mapear_pagina(endereco)

        # calcula o numero da pagina com base no endereço virtual
        numero_pagina = endereco // tabela_paginas.tamanho_pagina

        print("Verificando em qual quadro a pagina correspondente se encontra:")
        tabela_paginas.escrever_tabela()
        print(
            f"--> {numero_pagina} - Presente: {info_pagina.presente} - Modificação: {info_pagina.modificada} - Quadro: {info_pagina.numero_quadro}")
        print()

        # trata a falta de info_pagina, chamando o método correspondente
        if not info_pagina.presente:
            print("Tratando falta de pagina")

            self.tratar_falta_pagina(numero_processo, numero_pagina)

            # obtem a tabela de paginas atualizada
            tabela_paginas = self.tabelas_paginas.get(numero_processo)

            # obtem a info_pagina correspondente na nova tabela
            info_pagina = tabela_paginas.mapear_pagina(endereco)

        self.atualiza_lru(info_pagina.numero_quadro, numero_processo)

        print("Buscando pagina do quadro em Memoria Principal")
        self.mp.imprime_quadro_lru(info_pagina.numero_quadro)

        # obtem a pagina apartir do info_pagina
        pagina = self.mp.quadros[info_pagina.numero_quadro]

        print("Informações do quadro:",end=" ")
        for i in pagina.infos:
            print(i, end=" ")
        print()

        # obtem a informação apartir do ofset
        ofset = endereco % tabela_paginas.tamanho_pagina
        pagina.infos[ofset] = valor

        print(f"Escrevendo valor na pagina no index {ofset}")
        print("Informações do quadro atualizadas:",end=" ")
        for i in range(len(pagina.infos)):
            if i == ofset:
                print(f"\033[F\033[1;33m{pagina.infos[i]}\033[0m", end=" ")
            else:
                print(pagina.infos[i], end=" ")
        print()

        self.mp.quadros[info_pagina.numero_quadro] = pagina
        tabela_paginas.info_paginas[numero_pagina].modificada = True
        print("Atualizando quadro em memoria principal e info na tabela de paginas para modificado")
        self.tabelas_paginas[numero_processo] = tabela_paginas

    def termina_processo(self, numero_processo):

        # Lógica para terminar o processo
        tabela_paginas = self.tabelas_paginas.get(numero_processo)

        for info_pagina in tabela_paginas.info_paginas.values():
            if info_pagina.presente:
                if self.lru.count(info_pagina.numero_quadro) == 1:
                    aux = self.lru.index(info_pagina.numero_quadro)
                    self.aux.pop(aux)
                    self.lru.remove(info_pagina.numero_quadro)
                self.lru.insert(0, info_pagina.numero_quadro)
                self.aux.insert(0, numero_processo)

                self.mp.quadros[info_pagina.numero_quadro] = None

        print("Liberando espaço em memoria principal")
        self.mp.imprime_quadros()
        # Remover a tabela de páginas do processo terminado
        del self.tabelas_paginas[numero_processo]
        # Remover o processo da ms
        del self.ms.processos[numero_processo]

        print("Deletando tabela de paginas e processo da memoria secundaria")
        self.ms.escrever_processos()

    def carregar_ms(self, numero_processo):
        # Logica verificar modicicacao e atualizar na ms

        print("Fazendo o swapping para comunicação por microprocessador dedicado")
        tabela_paginas = self.tabelas_paginas.get(numero_processo)
        print("Atualizando informações da tabela e liberando espaço em memoria principal")
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

                self.mp.quadros[info_pagina.numero_quadro] = None
        print("Atualiza Memoria Secundaria no caso de modificação")
        tabela_paginas.escrever_tabela()
        self.mp.imprime_quadros()

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
                print()
                print("##################")
                print()
                print(f"Criando processo {vet[0]} de {vet[2]} {vet[3]}")
                print()
                if tipo == 'KB':
                    GM.criar_processo(numero_processo, tamanho_processo * (2 ** 10))
                elif tipo == 'MB':
                    GM.criar_processo(numero_processo, tamanho_processo * (2 ** 20))
                elif tipo == 'GB':
                    GM.criar_processo(numero_processo, tamanho_processo * (2 ** 30))
                elif tipo == 'B':
                    GM.criar_processo(numero_processo, tamanho_processo)
            elif comando == 'P':
                endereco_logico = int(vet[2][1:-2])
                print()
                print("###################")
                print()
                print(f"Buscando instrução do processo {vet[0]} no endereço {endereco_logico}")
                print()
                info = GM.busca_mp(numero_processo, endereco_logico)
                print(f"Executando instrução {info}")
            elif comando == 'R':
                endereco_logico = int(vet[2][1:-2])
                print()
                print("###################")
                print()
                print(f"Buscando informação do processo {vet[0]} no endereço {endereco_logico}")
                print()
                info = GM.busca_mp(numero_processo, endereco_logico)
                print(f"Informação: {info}")
            elif comando == 'W':
                endereco_logico = int(vet[2][1:-2])
                valor = int(vet[3])
                print()
                print("###################")
                print()
                print(f"Escrevendo o valor {valor} no endereço {endereco_logico} do processo {vet[0]}")
                print()
                GM.escreve_mp(numero_processo, endereco_logico, valor)
            elif comando == 'I':
                dispositivo = vet[2]
                print()
                print("###################")
                print()
                print(f"Processo {vet[0]} comunicando com {dispositivo}")
                print()
                GM.carregar_ms(numero_processo)
            elif comando == 'T':
                print()
                print("###################")
                print()
                print(f"Encerrando processo {vet[0]}")
                print()
                GM.termina_processo(numero_processo)
            print()


if __name__ == "__main__":
    trabalho_so()
