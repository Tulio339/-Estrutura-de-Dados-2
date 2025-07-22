# ⚙️ Projeto Forja de Heróis — Fase 2: Otimização de Recursos

Este documento detalha a arquitetura, implementação e análise dos algoritmos desenvolvidos para o módulo **"Otimização de Recursos"** do projeto **Forja de Heróis**. O objetivo é demonstrar, de forma prática, como otimizar o armazenamento e o acesso a dados através de técnicas de compressão e hashing.

---

## 📚 Arquitetura Geral do Projeto

O script continua a estrutura **modular e sequencial** da fase anterior, facilitando a compreensão de cada etapa da otimização.

### 🔹 SEÇÃO 1: Módulo de Dados

Prepara os cenários para os desafios de otimização:

- `carregar_mensagem_redundante`: Fornece um texto com alta repetição de caracteres, ideal para demonstrar a eficiência da **Compressão de Huffman**.
- `carregar_fragmentos_conhecimento`: Gera pares de chave-valor (conhecimentos) para testar a inserção e busca na **Tabela Hash**, incluindo chaves projetadas para colidir.

---

### 🔹 SEÇÃO 2: Módulo de Algoritmos de Otimização

Implementações puras e comentadas dos algoritmos centrais:

- `HuffmanNode`, `comprimir_huffman`, `descomprimir_huffman`: Compõem a solução de compressão.
- `CofreRapido`: A classe que implementa a Tabela Hash, com as funções `_hash_multiplicacao` e `_hash_meio_quadrado`, além do tratamento de colisões por encadeamento.

---

### 🔹 SEÇÃO 3: Módulo de Demonstração

Orquestra as simulações de otimização:

- **`desafio_pacto_compacto`**: Comprime uma mensagem, exibe a taxa de redução e a descomprime para validar a integridade dos dados.
- **`desafio_cofre_rapido`**: Insere fragmentos em uma Tabela Hash, exibe a estrutura interna (mostrando as colisões) e testa a velocidade de busca.

---

### 🔹 SEÇÃO 4: Ponto de Entrada Principal

O bloco `if __name__ == "__main__":` continua sendo o ponto de partida que executa todos os desafios em sequência, apresentando os resultados de forma organizada no console.

---

## ⚙️ Implementação e Análise dos Algoritmos

### 📌 1. Compressão de Huffman (`comprimir_huffman`)

**Funcionamento:**  
É um algoritmo de compressão sem perdas (lossless) que atribui códigos binários de tamanho variável aos caracteres. Caracteres mais frequentes recebem códigos mais curtos, enquanto os mais raros recebem códigos mais longos. O processo utiliza uma **fila de prioridade** para construir uma árvore binária ótima (a Árvore de Huffman), que serve como um dicionário para compressão e descompressão.

**Complexidade:**
- **Média:** `O(n + k log k)`, onde `n` é o número de caracteres no texto e `k` é o número de caracteres únicos.

**Eficiência Observada:**  
A eficiência é diretamente proporcional à redundância dos dados. Em textos com muitas repetições, como o do desafio, a taxa de compressão é altíssima.  
💡 **Solução poderosa para reduzir o espaço de armazenamento de dados textuais.**

---

### 📌 2. Tabela Hash (`CofreRapido`)

**Funcionamento:**  
Utiliza uma **função de hash** para mapear uma chave (ex: "FRG_ABC") a um índice numérico em uma tabela. No projeto, foram implementados e demonstrados dois métodos específicos: o **Método da Multiplicação** e o **Método do Meio-Quadrado**. Isso permite o acesso quase instantâneo aos dados. Colisões (quando duas chaves geram o mesmo índice) são tratadas com a técnica de **encadeamento separado**, onde cada posição da tabela é uma lista que armazena os elementos que colidiram.

**Complexidade (Inserção e Busca):**
- **Melhor caso:** `O(1)`
- **Pior caso:** `O(n)` (extremamente raro, ocorre se todas as chaves colidirem no mesmo índice)
- **Média:** `O(1)`

**Eficiência Observada:**  
A inserção e a busca são praticamente instantâneas, mesmo quando ocorrem colisões. O tempo de acesso não aumenta significativamente com o número de itens, demonstrando a principal vantagem da estrutura.  
💡 **Estrutura de dados ideal para acesso e recuperação de informações em tempo real.**

---

## 📊 Resumo da Eficiência

| Algoritmo             | Melhor Caso | Pior Caso | Média           | Principal Vantagem        |
|-----------------------|-------------|-----------|------------------|----------------------------|
| Compressão Huffman    | -           | -         | O(n + k log k)   | Redução de Espaço         |
| Tabela Hash (Busca)   | O(1)        | O(n)      | O(1)             | Velocidade de Acesso      |

---

## ✅ Conclusão

Esta fase do projeto ilustra duas abordagens fundamentais de otimização. Enquanto a **Compressão de Huffman** foca em reduzir a pegada de dados para armazenamento e transmissão, a **Tabela Hash** foca em minimizar o tempo de acesso. A escolha entre otimizar espaço ou tempo é um dos trade-offs mais clássicos e importantes da ciência da computação, e este módulo demonstra soluções práticas para ambos os cenários.

---

## 📎 Autor

**Tulio**  
Projeto fictício.