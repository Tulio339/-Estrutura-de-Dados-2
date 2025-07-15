
# 📖 Projeto Forja de Heróis — Fase 2: Mestre dos Algoritmos

Este documento detalha a arquitetura, implementação e análise de eficiência dos algoritmos desenvolvidos para o módulo **"O Arquivista Desesperado"** do projeto **Forja de Heróis**. O objetivo é demonstrar, de forma prática e narrativa, o funcionamento e o impacto do uso de diferentes algoritmos de busca em cenários distintos.

---

## 📚 Arquitetura Geral do Projeto

O script foi estruturado de forma **modular e sequencial**, para contar uma história e facilitar a leitura. A arquitetura é dividida em **quatro seções principais**:

### 🔹 SEÇÃO 1: Módulo de Dados
Responsável por preparar o "cenário" para cada desafio:

- `gerar_pilha_desorganizada`: Cria uma lista de itens (pergaminhos) em ordem aleatória — ideal para **Busca Sequencial**.
- `gerar_catalogo_ordenado`: Gera uma lista ordenada de registros por `id` — pré-requisito para a **Busca Binária**.
- `carregar_tomos_antigos`: Carrega textos onde serão buscados padrões com **Rabin-Karp**.

---

### 🔹 SEÇÃO 2: Módulo de Algoritmos de Busca
Implementações puras e comentadas dos três algoritmos centrais:

- `busca_sequencial`
- `busca_binaria`
- `rabin_karp`

Cada função é independente e retorna resultados mensuráveis (posição, número de comparações, etc.).

---

### 🔹 SEÇÃO 3: Módulo de Demonstração
Orquestra cada simulação completa:

- Invoca os geradores de dados da Seção 1.
- Define um alvo a ser encontrado.
- Mede o tempo de execução.
- Chama o algoritmo correspondente da Seção 2.
- Apresenta os resultados de forma clara e contextualizada.

---

### 🔹 SEÇÃO 4: Ponto de Entrada Principal
Através de:

```python
if __name__ == "__main__":
```

Inicia a execução do script, organizando a saída no console para acompanhar os desafios sequencialmente.

---

## ⚙️ Implementação e Análise dos Algoritmos

### 📌 1. Busca Sequencial (`busca_sequencial`)

**Funcionamento:**  
Percorre a lista do início ao fim, comparando cada elemento com o alvo.

**Complexidade:**
- **Melhor caso:** O(1)
- **Pior caso:** O(n)
- **Média:** O(n)

**Eficiência Observada:**  
Em listas grandes, o número de comparações é proporcional ao tamanho da lista.  
💡 **Útil quando os dados estão desordenados.**

---

### 📌 2. Busca Binária (`busca_binaria`)

**Funcionamento:**  
Opera sobre listas ordenadas. Divide a busca a cada iteração, descartando metade da lista.

**Complexidade:**
- **Melhor caso:** O(1)
- **Pior caso:** O(log n)
- **Média:** O(log n)

**Eficiência Observada:**  
Muito superior à busca sequencial em listas grandes.  
💡 **Requer estrutura ordenada, mas realiza muito menos comparações.**

---

### 📌 3. Rabin-Karp Matcher (`rabin_karp`)

**Funcionamento:**  
Utiliza hashing para localizar substrings, evitando comparações caractere a caractere sempre que possível.

**Complexidade:**
- **Média:** O(n + m)
- **Pior caso:** O(n × m) (raro)

**Eficiência Observada:**  
Evita verificações desnecessárias e realiza comparações diretas só quando necessário.  
💡 **Excelente para buscas de padrão em texto.**

---

## 📊 Resumo da Eficiência

| Algoritmo       | Melhor Caso | Pior Caso | Média       | Pré-requisito     |
|:----------------|:-------------|:------------|:---------------|:------------------|
| Busca Sequencial | O(1)         | O(n)        | O(n)           | Lista qualquer     |
| Busca Binária    | O(1)         | O(log n)    | O(log n)       | Lista ordenada     |
| Rabin-Karp       | O(n + m)     | O(n × m)    | O(n + m)       | Texto + Padrão     |

---

## ✅ Conclusão

Este projeto demonstra como **a escolha do algoritmo e a estrutura dos dados** impactam diretamente o desempenho e a viabilidade de soluções computacionais. Ao modularizar a implementação, os testes e a apresentação, obtivemos um ambiente claro para comparar os algoritmos e identificar suas forças e limitações.

---

## 📎 Autor

Tulio   
Projeto fictício.
