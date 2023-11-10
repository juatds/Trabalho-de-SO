class Pagina:
    def __init__(self, numero):
        self.numero = numero
        self.conteudo = f"Conteudo da Pagina {numero}"

class MemoriaFisica:
    def __init__(self, tamanho):
        self.tamanho = tamanho
        self.paginas = [None] * tamanho

    def alocar_pagina(self, pagina):
        for i in range(self.tamanho):
            if self.paginas[i] is None:
                self.paginas[i] = pagina
                return i
        return None

    def substituir_pagina(self, pagina, pagina_substituida):
        for i in range(self.tamanho):
            if self.paginas[i] == pagina_substituida:
                self.paginas[i] = pagina
                return i
        return None

    def desalocar_pagina(self, indice):
        self.paginas[indice] = None

    def obter_pagina(self, indice):
        return self.paginas[indice]

class GerenciadorMemoriaVirtual:
    def __init__(self, tamanho_fisico, tamanho_virtual):
        self.memoria_fisica = MemoriaFisica(tamanho_fisico)
        self.tamanho_virtual = tamanho_virtual
        self.tabela_paginas = [None] * tamanho_virtual

    def alocar_pagina(self, numero_pagina):
        if self.tabela_paginas[numero_pagina] is None:
            pagina = Pagina(numero_pagina)
            indice_memoria_fisica = self.memoria_fisica.alocar_pagina(pagina)
            if indice_memoria_fisica is not None:
                self.tabela_paginas[numero_pagina] = indice_memoria_fisica
                return True
        return False

    def acessar_pagina(self, numero_pagina):
        if self.tabela_paginas[numero_pagina] is not None:
            return self.tabela_paginas[numero_pagina]
        else:
            return None

    def imprimir_estado(self):
        print("Memória Física:")
        for i, pagina in enumerate(self.memoria_fisica.paginas):
            if pagina is not None:
                print(f"Página {i}: Conteúdo={pagina.conteudo}")
            else:
                print(f"Página {i}: Vazia")
        print("\nTabela de Páginas:")
        for i, indice in enumerate(self.tabela_paginas):
            if indice is not None:
                print(f"Página Virtual {i} -> Página Física {indice}")
            else:
                print(f"Página Virtual {i} -> Não Alocada")

# Simulação da execução de processos
def simular_execucao(processos, gerenciador_memoria):
    for processo in processos:
        print(f"\nExecutando Processo {processo}:")

        for pagina in range(5):  # Simula o acesso a 5 páginas em cada processo
            numero_pagina = processo * 5 + pagina
            if gerenciador_memoria.acessar_pagina(numero_pagina) is None:
                if not gerenciador_memoria.alocar_pagina(numero_pagina):
                    print(f"Falha de Página para Página Virtual {numero_pagina}")

        gerenciador_memoria.imprimir_estado()

# Exemplo de utilização
gerenciador_virtual = GerenciadorMemoriaVirtual(tamanho_fisico=4, tamanho_virtual=20)
processos_em_execucao = [0, 1, 2, 3, 4]

simular_execucao(processos_em_execucao, gerenciador_virtual)
