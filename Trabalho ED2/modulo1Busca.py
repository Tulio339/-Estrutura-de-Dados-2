# ==============================================================================
# PROJETO FORJA DE HERÓIS - DESAFIO MESTRE DOS ALGORITMOS
# MÓDULO 1 CONSOLIDADO EM UM ÚNICO ARQUIVO - VERSÃO COMENTADA
# ==============================================================================

# Importações necessárias para o script
import time     # Para medir o tempo de execução
import random   # Para embaralhar listas e escolher itens aleatórios

# ==============================================================================
# SEÇÃO 1: MÓDULO DE DADOS
# ==============================================================================

def gerar_pilha_desorganizada(tamanho=10000):
    """
    Gera uma lista de dicionários para simular uma pilha de pergaminhos sem ordem.

    Args:
        tamanho (int): O número de fragmentos a serem gerados na lista.

    Returns:
        list: Uma lista de dicionários, onde cada dicionário é um "fragmento".
    """
    pilha = []
    # Cria uma lista de fragmentos, cada um sendo um dicionário com dados ricos
    for i in range(tamanho):
        fragmento = {
            'id': f"ID_{i:06}",# O ID é formatado para ter 6 dígitos, por exemplo, ID_000001
            'titulo': f"Pergaminho Aleatório {i}",
            'raridade': random.choice(['Comum', 'Incomum', 'Raro'])
        }
        pilha.append(fragmento)
    
    # Passo crucial para o Desafio 1: embaralha a lista para simular o caos.
    random.shuffle(pilha)#
    return pilha

def gerar_catalogo_ordenado(tamanho=1000000):
    """
    Gera uma lista ORDENADA de dicionários para simular um catálogo.
    A ordem é garantida pela forma como os IDs são gerados.

    Args:
        tamanho (int): O número de fragmentos a serem gerados.

    Returns:
        list: Uma lista ORDENADA de dicionários.
    """
    catalogo = []
    # Os IDs são gerados em sequência (ID_0, ID_1, ...), então a lista já nasce ordenada.
    for i in range(tamanho):
        fragmento = {
            'id': f"ID_{i:07}",
            'titulo': f"Registro do Catálogo {i}",
            'categoria': 'História Antiga'
        }
        catalogo.append(fragmento)
    # Note a ausência de 'random.shuffle()'. Isso é intencional e necessário para a Busca Binária.
    return catalogo

def carregar_tomos_antigos():
    """
    Fornece os textos que servirão de base para o desafio Rabin-Karp.

    Returns:
        dict: Um dicionário onde as chaves são os nomes dos tomos e os valores são os textos.
    """
    tomo1 = "No início, o Vazio consumiu a luz, deixando apenas as marcas da corrupção em seu rastro. A corrupção se espalhou como uma doença, e a corrupção deve ser erradicada. A corrupção é o inimigo."
    tomo2 = "Antigas escrituras falam de um padrão místico, uma marca secreta. Mas a marca também pode ser uma corrupção. A corrupção espreita em cada sombra. O padrão se repete."
    tomo3 = "O padrão do caos se manifesta em fragmentos de texto. A corrupção é sutil, mas letal. Padrão, padrão, padrão!"
    
    # Agrupa os textos em um dicionário para fácil acesso
    tomos = {
        "Tomo do Crepúsculo": tomo1,
        "Tomo dos Segredos": tomo2,
        "Tomo da Desordem": tomo3
    }
    return tomos

# ==============================================================================
# SEÇÃO 2: MÓDULO DE ALGORITMOS DE BUSCA
# ==============================================================================

def busca_sequencial(lista_de_fragmentos, id_alvo):
    """
    Busca um fragmento pelo seu 'id' em uma lista de dicionários, um a um.

    Args:
        lista_de_fragmentos (list): A lista de dicionários onde buscar.
        id_alvo (str): O ID do fragmento que estamos procurando.

    Returns:
        tuple: Uma tupla (indice, num_comparacoes) se encontrar, ou (None, num_comparacoes) se não.
    """
    num_comparacoes = 0
    # Itera por cada item da lista, do início ao fim.
    for i, fragmento in enumerate(lista_de_fragmentos):
        num_comparacoes += 1 # Incrementa o contador a cada verificação.
        # Compara o 'id' do fragmento atual com o nosso alvo.
        if fragmento['id'] == id_alvo:
            return i, num_comparacoes # Retorna imediatamente se encontrar.
    # Se o loop terminar, o item não foi encontrado.
    return None, num_comparacoes

def busca_binaria(catalogo_ordenado, id_alvo):
    """
    Implementa a Busca Binária em uma lista de dicionários ordenada pela chave 'id'.

    Args:
        catalogo_ordenado (list): A lista ordenada onde buscar.
        id_alvo (str): O ID do fragmento que estamos procurando.

    Returns:
        tuple: (indice, num_comparacoes) se encontrar, ou (None, num_comparacoes) se não.
    """
    esquerda, direita = 0, len(catalogo_ordenado) - 1
    num_comparacoes = 0
    # Continua buscando enquanto a seção de busca for válida (esquerda não ultrapassou direita).
    while esquerda <= direita:
        # Calcula o índice do meio da seção de busca atual.
        meio = (esquerda + direita) // 2
        id_meio = catalogo_ordenado[meio]['id']
        num_comparacoes += 1
        
        # Compara o alvo com o elemento do meio.
        if id_meio == id_alvo:
            return meio, num_comparacoes # Encontrado!
        elif id_meio < id_alvo:
            # Se o alvo for maior, ele só pode estar na metade direita.
            esquerda = meio + 1
        else:
            # Se o alvo for menor, ele só pode estar na metade esquerda.
            direita = meio - 1
    # Se o loop terminar, o item não está na lista.
    return None, num_comparacoes

def rabin_karp(texto, padrao, base=256, modulo=101):
    """
    Implementa o algoritmo Rabin-Karp para encontrar um padrão em um texto usando hashing.

    Args:
        texto (str): O texto grande onde a busca será feita.
        padrao (str): A string pequena que queremos encontrar.
        base (int): O número de caracteres no alfabeto (256 para ASCII).
        modulo (int): Um número primo para ajudar a manter os hashes pequenos.

    Returns:
        tuple: (lista de ocorrências, contagem de comparações de hash, contagem de comparações de caracteres).
    """
    n, m = len(texto), len(padrao)
    ocorrencias = []
    comp_hash, comp_char = 0, 0
    if m > n:
        return [], 0, 0 # O padrão não pode ser maior que o texto.

    # Pré-cálculo de (base^(m-1)) % modulo. Usado para o "rolling hash".
    potencia_base = pow(base, m - 1, modulo)
    # Calcula o hash inicial do padrão e da primeira "janela" do texto.
    hash_padrao, hash_texto = 0, 0
    for i in range(m):
        hash_padrao = (hash_padrao * base + ord(padrao[i])) % modulo
        hash_texto = (hash_texto * base + ord(texto[i])) % modulo

    # Desliza a janela de busca pelo texto.
    for i in range(n - m + 1):
        comp_hash += 1
        # 1ª Verificação (rápida): Compara os hashes.
        if hash_padrao == hash_texto:
            # Se os hashes são iguais, pode ser uma coincidência (colisão).
            # 2ª Verificação (lenta, mas segura): Compara caractere por caractere.
            match = True
            for j in range(m):
                comp_char += 1
                if texto[i+j] != padrao[j]:
                    match = False
                    break
            if match:
                ocorrencias.append(i) # Confirmado! Adiciona a posição na lista.
        
        # Se não for a última janela, calcula o hash da próxima janela de forma eficiente.
        if i < n - m:
            # "Rolling Hash": remove o caractere da esquerda e adiciona o da direita.
            hash_texto = ((hash_texto - ord(texto[i]) * potencia_base) * base + ord(texto[i+m])) % modulo
            # Garante que o resultado do módulo seja positivo.
            if hash_texto < 0:
                hash_texto += modulo
                
    return ocorrencias, comp_hash, comp_char

# ==============================================================================
# SEÇÃO 3: MÓDULO DE DEMONSTRAÇÃO 
# ==============================================================================

def desafio_1_busca_sequencial():
    """Simula e demonstra o desafio da Busca Sequencial."""
    print("\n--- Desafio 1: A Pilha de Pergaminhos Desorganizados (Busca Sequencial) ---")
    # PREPARAÇÃO: Gera os dados caóticos.
    fragmentos = gerar_pilha_desorganizada(100000)
    pergaminho_vital_id = random.choice(fragmentos)['id'] 
    print(f"Buscando o Pergaminho Vital com ID: '{pergaminho_vital_id}' em {len(fragmentos)} fragmentos...")
    
    # EXECUÇÃO: Mede o tempo e chama o algoritmo.
    start_time = time.perf_counter()
    indice, comparacoes = busca_sequencial(fragmentos, pergaminho_vital_id)
    end_time = time.perf_counter()
    
    # APRESENTAÇÃO: Exibe os resultados de forma clara.
    tempo_execucao = (end_time - start_time) * 1000
    if indice is not None:
        print(f"SUCESSO! Pergaminho encontrado na posição {indice}.")
        print(f"Dados do Pergaminho: {fragmentos[indice]}") 
    else:
        print("FALHA! Pergaminho NÃO foi encontrado.")
    print(f"Tempo de execução: {tempo_execucao:.4f} ms")
    print(f"Número de comparações: {comparacoes}")

def desafio_2_busca_binaria():
    """Simula e demonstra o desafio da Busca Binária."""
    print("\n--- Desafio 2: Os Catálogos Ordenados (Busca Binária) ---")
    fragmentos_ordenados = gerar_catalogo_ordenado(1000000)
    fragmentos_a_encontrar = [random.choice(fragmentos_ordenados)['id'] for _ in range(5)]
    
    print(f"Buscando 5 Fragmentos Específicos em {len(fragmentos_ordenados)} registros ordenados...")
    for fragmento_id in fragmentos_a_encontrar:
        start_time = time.perf_counter()
        indice, comparacoes = busca_binaria(fragmentos_ordenados, fragmento_id)
        end_time = time.perf_counter()
        tempo_execucao = (end_time - start_time) * 1000
        if indice is not None:
            print(f"  - SUCESSO! Fragmento '{fragmento_id}' encontrado em {tempo_execucao:.6f} ms com {comparacoes} comparações.")
        else:
            print(f"  - FALHA! Fragmento '{fragmento_id}' não encontrado.")
    print("\nAnálise: Observe o número ridiculamente baixo de comparações da Busca Binária!")

def desafio_3_rabin_karp():
    """Simula e demonstra o desafio do Rabin-Karp Matcher."""
    print("\n--- Desafio 3: Decifrando os Códigos do Vazio (Rabin-Karp Matcher) ---")
    tomos = carregar_tomos_antigos()
    marcas_corrupcao = ["corrupção", "padrão", "Vazio"]
    
    for nome_tomo, texto_tomo in tomos.items():
        print(f"\nPurificando '{nome_tomo}'...")
        for marca in marcas_corrupcao:
            ocorrencias, comp_hash, comp_char = rabin_karp(texto_tomo, marca)
            if ocorrencias:
                print(f"  - Marca '{marca}' encontrada {len(ocorrencias)} vezes. Posições: {ocorrencias}")
                print(f"    Métricas: {comp_hash} comparações de hash, {comp_char} de caracteres (colisões).")
            else:
                print(f"  - Marca '{marca}' NÃO encontrada.")

# ==============================================================================
# SEÇÃO 4: PONTO DE ENTRADA PRINCIPAL
# ==============================================================================

# O bloco `if __name__ == "__main__":` garante que o código abaixo só será
# executado quando você rodar este arquivo diretamente.
if __name__ == "__main__":
    print("### INICIANDO DEMONSTRAÇÃO DO MÓDULO 1: O ARQUIVISTA DESESPERADO ###")
    
    desafio_1_busca_sequencial()
    
    print("\n" + "="*70 + "\n") # Separador para clareza
    
    desafio_2_busca_binaria()
    
    print("\n" + "="*70 + "\n") # Separador para clareza
    
    desafio_3_rabin_karp()
    
    print("\n\n### DEMONSTRAÇÃO DO MÓDULO 1 CONCLUÍDA ###")