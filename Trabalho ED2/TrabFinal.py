# ==============================================================================
# PROJETO FORJA DE HERÓIS - DESAFIO MESTRE DOS ALGORITMOS
# ==============================================================================

# Importações necessárias para todos os módulos
import time      # Usado para medir o tempo de execução e comparar a eficiência dos algoritmos.
import random    # Usado para embaralhar listas (busca sequencial) e escolher itens aleatórios para busca.
import heapq     # Essencial para a fila de prioridade (min-heap) usada na construção da árvore de Huffman.
import math      # Necessário para as operações matemáticas nas funções de hash (raiz quadrada e parte fracionária).
import sys       # Usado no Módulo 2 para medir o tamanho de objetos em memória (embora a medição final tenha sido em bits).

# ==============================================================================
# SEÇÃO DE DADOS 
# ==============================================================================

# --- Dados para o Módulo 1: Busca ---

def gerar_pilha_desorganizada(tamanho=10000):
    """
    Gera uma lista de dicionários para simular uma pilha de pergaminhos sem ordem.
    O objetivo é criar o pior cenário para busca, onde não há nenhuma ordem prévia.
    """
    pilha = []
    for i in range(tamanho):
        fragmento = {
            'id': f"ID_{i:06}",
            'titulo': f"Pergaminho Aleatório {i}",
            'raridade': random.choice(['Comum', 'Incomum', 'Raro'])
        }
        pilha.append(fragmento)
    # A chamada a random.shuffle() é o passo crucial que garante a desordem,
    # forçando a necessidade de uma busca sequencial.
    random.shuffle(pilha)
    return pilha

def gerar_catalogo_ordenado(tamanho=1000000):
    """
    Gera uma lista ORDENADA de dicionários para simular um catálogo.
    A lista já é gerada em ordem, representando um conjunto de dados organizado,
    que é o pré-requisito para algoritmos eficientes como a Busca Binária.
    """
    catalogo = []
    for i in range(tamanho):
        fragmento = {
            'id': f"ID_{i:07}",
            'titulo': f"Registro do Catálogo {i}",
            'categoria': 'História Antiga'
        }
        catalogo.append(fragmento)
    # Note a ausência de 'random.shuffle()'. Isso é intencional.
    return catalogo

def carregar_tomos_antigos():
    """
    Fornece os textos (o "palheiro") onde o algoritmo Rabin-Karp procurará
    por padrões específicos (as "agulhas").
    """
    tomo1 = "No início, o Vazio consumiu a luz, deixando apenas as marcas da corrupção em seu rastro. A corrupção se espalhou como uma doença, e a corrupção deve ser erradicada. A corrupção é o inimigo."
    tomo2 = "Antigas escrituras falam de um padrão místico, uma marca secreta. Mas a marca também pode ser uma corrupção. A corrupção espreita em cada sombra. O padrão se repete."
    tomo3 = "O padrão do caos se manifesta em fragmentos de texto. A corrupção é sutil, mas letal. Padrão, padrão, padrão!"
    return {
        "Tomo do Crepúsculo": tomo1,
        "Tomo dos Segredos": tomo2,
        "Tomo da Desordem": tomo3
    }

# --- Dados para o Módulo 2: Otimização ---

def carregar_mensagem_redundante():
    """
    Fornece um texto com muitas repetições. A alta redundância é o cenário
    ideal para a compressão de Huffman, pois permite alcançar uma alta taxa de compressão.
    """
    return "AAAAABBBCCCCCCDEEEEEEFFFFFFFFGGGGGGGGHHHHHHHHIIIIIIIIJJJJJJJJJKKKKKKKKKLLLLLLLLMMMMMMMM"

def carregar_fragmentos_conhecimento():
    """
    Gera uma lista de pares (chave, valor) para serem inseridos na tabela hash.
    Algumas chaves são intencionalmente similares ("ABC", "BCA", "CAB") para
    testar o tratamento de colisões da tabela hash.
    """
    return [
        ("FRG_001", "O segredo do fogo está na centelha."),
        ("FRG_010", "A água sempre encontra seu caminho."),
        ("FRG_100", "O ar é invisível, mas sustenta a vida."),
        ("FRG_111", "A terra é a base de toda a criação."),
        ("FRG_234", "A entropia é a seta do tempo."),
        ("FRG_456", "A gravidade une todas as coisas."),
        ("FRG_ABC", "A luz viaja mais rápido que o som."),
        ("FRG_BCA", "A sombra é a ausência de luz."),
        ("FRG_CAB", "O eco é a memória do som."),
    ]

# ==============================================================================
# SEÇÃO DE ALGORITMOS
# ==============================================================================

# --- Algoritmos do Módulo 1: Busca ---

def busca_sequencial(lista_de_fragmentos, id_alvo):
    """
    Busca um item percorrendo a lista do início ao fim.
    É o método mais simples, mas ineficiente para grandes volumes de dados (Complexidade O(n)).
    """
    num_comparacoes = 0
    # Itera por cada item da lista, mantendo o controle do índice (i) e do item (fragmento).
    for i, fragmento in enumerate(lista_de_fragmentos):
        num_comparacoes += 1 # Conta cada comparação feita.
        if fragmento['id'] == id_alvo:
            return i, num_comparacoes # Retorna imediatamente ao encontrar o alvo.
    # Se o loop terminar, o item não foi encontrado.
    return None, num_comparacoes

def busca_binaria(catalogo_ordenado, id_alvo):
    """
    Implementa a Busca Binária, um algoritmo de "dividir para conquistar".
    A cada passo, ele descarta metade do espaço de busca, tornando-o extremamente
    rápido para dados ORDENADOS (Complexidade O(log n)).
    """
    esquerda, direita = 0, len(catalogo_ordenado) - 1
    num_comparacoes = 0
    # O loop continua enquanto a seção de busca for válida (ponteiro da esquerda não ultrapassou o da direita).
    while esquerda <= direita:
        # Calcula o índice do meio para dividir a lista.
        meio = (esquerda + direita) // 2
        id_meio = catalogo_ordenado[meio]['id']
        num_comparacoes += 1
        
        # Compara o alvo com o elemento do meio.
        if id_meio == id_alvo:
            return meio, num_comparacoes # Encontrado!
        elif id_meio < id_alvo:
            # Se o alvo for maior, ele só pode estar na metade direita. Ajusta o ponteiro da esquerda.
            esquerda = meio + 1
        else:
            # Se o alvo for menor, ele só pode estar na metade esquerda. Ajusta o ponteiro da direita.
            direita = meio - 1
    return None, num_comparacoes

def rabin_karp(texto, padrao, base=256, modulo=103):
    """
    Implementa o algoritmo Rabin-Karp, que usa hashing para encontrar um padrão em um texto.
    Ele evita comparações caras de strings, comparando primeiro os valores de hash.
    """
    n, m = len(texto), len(padrao)
    ocorrencias, comp_hash, comp_char = [], 0, 0
    if m > n: return [], 0, 0 # Impossível encontrar um padrão maior que o texto.

    # Pré-cálculo de (base^(m-1)) % modulo. Usado para o "rolling hash".
    potencia_base = pow(base, m - 1, modulo)
    # Calcula o hash inicial do padrão e da primeira "janela" do texto.
    hash_padrao, hash_texto = 0, 0
    for i in range(m):
        hash_padrao = (hash_padrao * base + ord(padrao[i])) % modulo
        hash_texto = (hash_texto * base + ord(texto[i])) % modulo

    # Desliza a janela de busca pelo texto, uma posição de cada vez.
    for i in range(n - m + 1):
        comp_hash += 1
        # 1ª Verificação (rápida): Compara os hashes.
        if hash_padrao == hash_texto:
            # 2ª Verificação (lenta, mas segura): Se os hashes batem, verifica caractere por caractere
            # para garantir que não é uma "colisão de hash" (dois textos diferentes com o mesmo hash).
            match = True
            for j in range(m):
                comp_char += 1
                if texto[i+j] != padrao[j]:
                    match = False
                    break
            if match:
                ocorrencias.append(i) # Confirmado! Adiciona a posição na lista.
        
        # Se não for a última janela, calcula o hash da próxima de forma eficiente.
        if i < n - m:
            # "Rolling Hash": remove o caractere da esquerda e adiciona o da direita
            # sem ter que recalcular o hash da janela inteira.
            hash_texto = ((hash_texto - ord(texto[i]) * potencia_base) * base + ord(texto[i+m])) % modulo
            if hash_texto < 0: # Garante que o resultado do módulo seja positivo.
                hash_texto += modulo
    return ocorrencias, comp_hash, comp_char

# --- Algoritmos do Módulo 2: Otimização e Hashing ---

class HuffmanNode:
    """
    Representa um nó na árvore de Huffman. Contém o caractere, sua frequência e os filhos.
    (ANTERIORMENTE NoHuffman)
    """
    def __init__(self, char, freq):
        self.char, self.freq, self.left, self.right = char, freq, None, None
    # O método __lt__ (less than) é crucial para que a heapq (fila de prioridade)
    # saiba como ordenar os nós: o nó com menor frequência é considerado "menor".
    def __lt__(self, other):
        return self.freq < other.freq

def _generate_huffman_codes(node, current_code, codes):
    """Função auxiliar recursiva para gerar os códigos binários a partir da árvore."""
    if node is None: return # Caso base: nó nulo.
    # Caso base: se o nó é uma folha (tem um caractere), armazena o código gerado.
    if node.char is not None:
        codes[node.char] = current_code
        return
    # Passo recursivo: continua para a esquerda (adiciona '0') e para a direita (adiciona '1').
    _generate_huffman_codes(node.left, current_code + "0", codes)
    _generate_huffman_codes(node.right, current_code + "1", codes)

def comprimir_huffman(text):
    """Comprime um texto usando o algoritmo de Huffman."""
    # Passo 1: Calcular a frequência de cada caractere no texto.
    frequencies = {char: text.count(char) for char in set(text)}
    # Passo 2: Criar a fila de prioridade com os nós folha.
    priority_queue = [HuffmanNode(char, freq) for char, freq in frequencies.items()]
    heapq.heapify(priority_queue) # Transforma a lista em uma min-heap.
    
    # Passo 3: Construir a árvore de Huffman fundindo os nós de menor frequência.
    while len(priority_queue) > 1:
        left_node = heapq.heappop(priority_queue)  # Pega o nó de menor frequência.
        right_node = heapq.heappop(priority_queue) # Pega o segundo de menor frequência.
        
        # Cria um nó pai com a soma das frequências dos filhos.
        parent_node = HuffmanNode(None, left_node.freq + right_node.freq)
        parent_node.left, parent_node.right = left_node, right_node
        
        # Adiciona o novo nó pai de volta na fila.
        heapq.heappush(priority_queue, parent_node)
        
    # A árvore está pronta. O único nó que restou na fila é a raiz.
    tree_root = priority_queue[0]
    
    # Passo 4: Gerar o mapa de códigos a partir da árvore.
    huffman_codes = {}
    _generate_huffman_codes(tree_root, "", huffman_codes)
    
    # Passo 5: Codificar o texto original usando o mapa de códigos.
    compressed_text = "".join([huffman_codes[char] for char in text])
    return compressed_text, tree_root

def descomprimir_huffman(compressed_text, tree_root):
    """Descomprime um texto usando a árvore de Huffman."""
    decompressed_text = ""
    current_node = tree_root
    # Itera bit a bit pela string comprimida.
    for bit in compressed_text:
        # Navega na árvore de acordo com o bit.
        current_node = current_node.left if bit == '0' else current_node.right
        # Se chegou a uma folha, encontrou um caractere.
        if current_node.char is not None:
            decompressed_text += current_node.char
            current_node = tree_root # Volta para a raiz para decodificar o próximo caractere.
    return decompressed_text

class CofreRapido:
    """Implementa uma Tabela Hash com tratamento de colisão por encadeamento."""
    def __init__(self, tamanho, funcao_hash_nome):
        self.tamanho, self.funcao_hash_nome = tamanho, funcao_hash_nome
        # A tabela é uma lista de listas. Cada lista interna representa uma "corrente"
        # para armazenar múltiplos itens que colidem no mesmo índice.
        self.tabela = [[] for _ in range(tamanho)]
        # A constante A (conjugado da razão áurea) é uma boa escolha para o método
        # da multiplicação, pois ajuda a espalhar bem as chaves.
        self.A = (math.sqrt(5) - 1) / 2

    def _str_para_int(self, chave):
        """Converte uma string em um inteiro para que possamos aplicar cálculos matemáticos."""
        return sum(ord(c) for c in chave)

    def _hash_multiplicacao(self, chave):
        """Função de hash pelo método da multiplicação."""
        k = self._str_para_int(chave)
        # A fórmula multiplica a chave por A, pega a parte fracionária, e escala pelo tamanho da tabela.
        return math.floor(self.tamanho * ((k * self.A) % 1))

    def _hash_meio_quadrado(self, chave):
        """Função de hash pelo método do meio-quadrado."""
        k = self._str_para_int(chave)
        quadrado = str(k * k)
        # Determina quantos dígitos pegar do meio do quadrado.
        num_digitos = len(str(self.tamanho - 1))
        meio_pos = len(quadrado) // 2
        inicio = max(0, meio_pos - (num_digitos // 2))
        meio = int(quadrado[inicio:inicio + num_digitos]) if len(quadrado) >= num_digitos else int(quadrado)
        # O módulo final garante que o índice esteja dentro dos limites da tabela.
        return meio % self.tamanho

    def _hash(self, chave):
        """Chama a função de hash escolhida durante a inicialização do cofre."""
        return self._hash_multiplicacao(chave) if self.funcao_hash_nome == 'multiplicacao' else self._hash_meio_quadrado(chave)

    def inserir(self, chave, valor):
        """Insere um par (chave, valor) no cofre (tabela hash)."""
        indice = self._hash(chave)
        # Antes de inserir, verifica se a chave já existe na corrente para apenas atualizar o valor.
        for par in self.tabela[indice]:
            if par[0] == chave:
                par[1] = valor # Atualiza o valor existente.
                print(f"  > Chave '{chave}' atualizada no índice {indice}.")
                return
        # Se a chave não existe, adiciona o novo par à corrente (lista) do índice.
        self.tabela[indice].append([chave, valor])
        print(f"  > Chave '{chave}' inserida no índice {indice}.")

    def buscar(self, chave):
        """Busca um valor no cofre pela sua chave."""
        indice = self._hash(chave)
        # Percorre a pequena lista (corrente) no índice calculado.
        for par in self.tabela[indice]:
            if par[0] == chave:
                return par[1] # Encontrou a chave, retorna o valor.
        return None # Se percorreu a corrente e não encontrou, retorna None.

    def exibir_cofre(self):
        """Mostra a estrutura interna do cofre para visualizar a distribuição e as colisões."""
        print("\n--- Estrutura do Cofre Rápido ---")
        for i, lista in enumerate(self.tabela):
            if lista: # Só imprime os índices que contêm dados.
                print(f"Índice {i:02d}: {lista}")
        print("----------------------------------\n")

# ==============================================================================
# SEÇÃO DE DEMONSTRAÇÃO 
# ==============================================================================

# --- Demonstrações do Módulo 1 ---

def desafio_1_busca_sequencial():
    """Simula e demonstra o desafio da Busca Sequencial."""
    print("\n--- Desafio 1: A Pilha de Pergaminhos Desorganizados (Busca Sequencial) ---")
    # PREPARAÇÃO
    fragmentos = gerar_pilha_desorganizada(100000)
    pergaminho_vital_id = random.choice(fragmentos)['id']
    print(f"Buscando o Pergaminho Vital com ID: '{pergaminho_vital_id}' em {len(fragmentos)} fragmentos...")
    
    # EXECUÇÃO
    start_time = time.perf_counter()
    indice, comparacoes = busca_sequencial(fragmentos, pergaminho_vital_id)
    end_time = time.perf_counter()
    
    # APRESENTAÇÃO DOS RESULTADOS
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
    # PREPARAÇÃO
    fragmentos_ordenados = gerar_catalogo_ordenado(1000000)
    fragmentos_a_encontrar = [random.choice(fragmentos_ordenados)['id'] for _ in range(5)]
    print(f"Buscando 5 Fragmentos Específicos em {len(fragmentos_ordenados)} registros ordenados...")
    
    # EXECUÇÃO E APRESENTAÇÃO (dentro do loop)
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
    # PREPARAÇÃO
    tomos, marcas_corrupcao = carregar_tomos_antigos(), ["corrupção", "padrão", "Vazio"]
    
    # EXECUÇÃO E APRESENTAÇÃO
    for nome_tomo, texto_tomo in tomos.items():
        print(f"\nPurificando '{nome_tomo}'...")
        for marca in marcas_corrupcao:
            ocorrencias, comp_hash, comp_char = rabin_karp(texto_tomo, marca)
            if ocorrencias:
                print(f"  - Marca '{marca}' encontrada {len(ocorrencias)} vezes. Posições: {ocorrencias}")
                print(f"    Métricas: {comp_hash} comparações de hash, {comp_char} de caracteres (colisões).")
            else:
                print(f"  - Marca '{marca}' NÃO encontrada.")

# --- Demonstrações do Módulo 2 ---

def desafio_pacto_compacto():
    """Simula e demonstra a compressão e descompressão de Huffman."""
    print("\n--- Desafio 4: O Pacto Compacto (Compressão Huffman) ---")
    # PREPARAÇÃO
    mensagem = carregar_mensagem_redundante()
    print(f"Mensagem Original: '{mensagem}'")
    tamanho_original_bits = len(mensagem) * 8
    print(f"\nTamanho Original: {tamanho_original_bits} bits")
    
    # EXECUÇÃO
    comprimido, arvore = comprimir_huffman(mensagem)
    tamanho_comprimido_bits = len(comprimido)
    
    # APRESENTAÇÃO
    print(f"Tamanho Comprimido: {tamanho_comprimido_bits} bits")
    # Calcula a taxa de compressão para mostrar a eficiência.
    reducao = ((tamanho_original_bits - tamanho_comprimido_bits) / tamanho_original_bits) * 100
    print(f"\nTexto Comprimido (bits): {comprimido}")
    print(f"Taxa de compressão: {reducao:.2f}%")
    
    # VERIFICAÇÃO DE INTEGRIDADE
    descomprimido = descomprimir_huffman(comprimido, arvore)
    print(f"\nTexto Descomprimido: '{descomprimido}'")
    if mensagem == descomprimido:
        print("\nSUCESSO! A mensagem foi restaurada com integridade total.")
    else:
        print("\nFALHA! A mensagem foi corrompida no processo.")

def desafio_cofre_rapido():
    """Simula e demonstra a inserção e busca na Tabela Hash."""
    print("\n--- Desafio 5: O Cofre Rápido (Tabela Hash) ---")
    # PREPARAÇÃO
    fragmentos = carregar_fragmentos_conhecimento()
    
    # EXECUÇÃO E APRESENTAÇÃO (um teste para cada função de hash)
    for nome_funcao in ['multiplicacao', 'meio_quadrado']:
        print(f"\n=== Testando Cofre com Função de Hash: '{nome_funcao.upper()}' ===")
        cofre = CofreRapido(tamanho=10, funcao_hash_nome=nome_funcao)
        
        print("\n1. Inserindo Fragmentos no Cofre...")
        for chave, valor in fragmentos:
            cofre.inserir(chave, valor)
        
        cofre.exibir_cofre() # Mostra a estrutura final da tabela.
        
        print("2. Buscando Fragmentos Específicos...")
        for chave in ["FRG_100", "FRG_ABC", "FRG_NAO_EXISTE"]: # Testa casos de sucesso e falha.
            resultado = cofre.buscar(chave)
            if resultado:
                print(f"  - Busca por '{chave}': SUCESSO! Segredo: '{resultado}'")
            else:
                print(f"  - Busca por '{chave}': FALHA! Fragmento não encontrado.")

# ==============================================================================
# SEÇÃO 4: PONTO DE ENTRADA PRINCIPAL
# ==============================================================================

# O bloco `if __name__ == "__main__":` garante que o código abaixo só será
# executado quando você rodar este arquivo diretamente. É o ponto de partida do programa.
if __name__ == "__main__":
    print("######################################################################")
    print("###      PROJETO FORJA DE HERÓIS - MESTRE DOS ALGORITMOS           ###")
    print("######################################################################")

    # Execução dos desafios do Módulo 1
    print("\n\n=============== MÓDULO 1: O ARQUIVISTA DESESPERADO ===============")
    desafio_1_busca_sequencial()
    print("\n" + "-"*70)
    desafio_2_busca_binaria()
    print("\n" + "-"*70)
    desafio_3_rabin_karp()

    # Execução dos desafios do Módulo 2
    print("\n\n=============== MÓDULO 2: OTIMIZAÇÃO DE RECURSOS ===============")
    desafio_pacto_compacto()
    print("\n" + "-"*70)
    desafio_cofre_rapido()

    print("\n\n###   DEMONSTRAÇÃO COMPLETA DOS MÓDULOS 1 E 2 CONCLUÍDA    ###")