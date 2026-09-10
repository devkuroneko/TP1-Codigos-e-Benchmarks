# Análise, Correção e Ajuste de Pivô — `student_template.py`

Documento de apoio ao TP1 de APA. Cobre três fases: o diagnóstico do código original, as
correções aplicadas e a troca do pivô fixo por um pivô dinâmico. Todos os números aqui foram
**medidos executando o código**, não estimados.

---

## Parte I — Diagnóstico do código original (histórico)

> Esta seção descreve o estado **anterior** às correções. Os números de linha citados são os do
> arquivo original e não correspondem mais ao arquivo atual. Ela é mantida porque o "antes" é
> material direto para a seção de dificuldades do relatório.

### As duas causas-raiz

| # | Causa | Efeito observado |
|---|-------|------------------|
| **1** | O laço iterava sobre **índices** (`range(0, lenght_vector)`), mas `values_to_compare` era comparado contra **valores** (`last_index_value`). Índice e valor são grandezas diferentes. | Com índices `0..9` e valores `25..125`, a condição `last_index_value > values_to_compare` era **sempre verdadeira** → 100% dos elementos caíam em `vetor_menor_que_mediador`, e os outros dois ramos eram código morto. |
| **2** | O critério `ultimo_valor_adicionado_*` não era um algoritmo de ordenação, e sim um filtro de sequência crescente, com o ramo corretivo quebrado. | Mesmo corrigindo a causa 1, o vetor **não saía ordenado** e **perdia elementos**. |

### Evidência da execução original

```
valor definido como mediador: 99: 9 -- vetor OG: [66, 44, 75, 108, 31, 34, 93, 37, 71, 99]
vetor menor:[44, 75, 108, 31, 34, 93, 37, 71, 99]
vetor igual[]
vetor maior[]
```

Três defeitos numa só saída: os outros dois baldes vazios; `108` e `99` classificados como
"menores" que o mediador `99`; e o elemento `66` (índice 0) desaparecido.

### Inventário dos defeitos

1. **Índice tratado como valor** — causa-raiz, descrita acima.
2. **Primeiro elemento sempre descartado** — com `ultimo_valor_adicionado_* = 0`, a primeira
   iteração testava `0 > 0` (falso) e `0 < 0` (falso). Sem `else`, o elemento sumia. O mesmo
   buraco engolia **toda duplicata**.
3. **Sentinela `0` incompatível com negativos** — assumia dados positivos; `test_random` usa
   `randint(-1000, 1000)`.
4. **Ramo de inserção com quatro defeitos independentes** — `insert()` durante a iteração sobre
   a própria lista (reinserção descontrolada: inserir `5` em `[2,4,6,8]` gerou 50+ cópias antes
   da trava de segurança); ausência de `break`; ordem invertida (`if v > x: insert(pos_de_x, v)`
   coloca o maior antes do menor); e `.index()`, que devolve a *primeira* ocorrência do valor.
   Além disso, quando nenhum elemento satisfazia a condição, o valor não era inserido em lugar
   nenhum — simulando a correção mínima de índice→valor, `[5,3,8,2,9,7,6]` produzia
   `menor=[5] igual=[6] maior=[8,9]`, perdendo 3 dos 7 elementos.
5. **Dados heterogêneos no mesmo balde** — um ramo gravava o valor
   (`append(vector_base[values_to_compare])`), o outro gravava o índice
   (`insert(index_add, values_to_compare)`).
6. **`IndexError` em lista vazia** — `vector_base[-1]` executava *antes* da guarda
   `if lenght_vector >= 2`. E `n == 1` retornava três baldes vazios, perdendo o único elemento.
7. **Não havia concatenação nem recursão** — mesmo perfeita, a função produzia um agrupamento,
   não uma ordenação.
8. **Contrato quebrado** — `find_max_value` devolvia uma string formatada, impossível de
   encadear; `my_authorial_sort` era esboço, devolvendo a entrada intacta com
   `comparison = steps = 0`. Os 6 testes falhavam e a suíte estava comentada.
9. **Complexidade** — os laços de inserção com `.index()` interno e `insert()` deslocando a
   cauda davam O(n³) no pior caso, pior que o Bubble Sort que se pretendia superar.

---

## Parte II — O que foi corrigido

| Onde (linha atual) | Correção |
|---|---|
| `:180` | Laço passou a percorrer **valores** (`for valor_atual in vector_base`), não índices. Elimina a causa-raiz. |
| `:182-198` | Três ramos exaustivos (`<`, `>`, `else`). Invariante garantida: `len(menor)+len(igual)+len(maior) == len(entrada)`. |
| removido | Sentinelas `ultimo_valor_adicionado_*`, que descartavam o 1º elemento e as duplicatas e quebravam com negativos. |
| removido | O bloco `for ... insert(index_add, ...)`; reparticionar cada metade faz o trabalho corretamente. |
| `:150` | Guarda de tamanho virou a condição do `while`, antes de qualquer acesso a `[-1]`. Fim do `IndexError`. |
| `:242` | **A concatenação que faltava**: `vetor_menor_final + vector_base + vetor_maior_final`. |
| `:248-256` | `my_authorial_sort` passou a delegar e repassar `(lista, comparações, movimentações)`. |
| `:107` | **Pivô dinâmico** por mediana de três posições sorteadas (Parte III). |
| `:22` | Gerador aleatório próprio do módulo, isolado do `random` global. |

### A recursão pela metade menor

Com pivô fixo em `[-1]` e recursão pura nos dois lados, entrada ordenada ou invertida joga tudo
para um lado só e a profundidade vira N — **`RecursionError` confirmado em N=1000**, e o
`benchmark.py` usa exatamente N=1000 com `sorted` e `reverse`.

A correção foi descer por recursão apenas na **menor** das duas metades e manter a maior no
`while` (`:214`). Cada chamada passa a ter no máximo N/2 elementos, e a profundidade cai para
O(log N). É a *eliminação de recursão de cauda* de Sedgewick (1978).

Medição da profundidade máxima na versão recursiva pura (limite padrão do Python = 1000):

| N | distribuição | pivô `[-1]` | pivô mediana-3 |
|---|---|---:|---:|
| 1000 | sorted | 999 | 9 |
| 4000 | sorted | 3999 | 11 |
| 4000 | reverse | 3999 | 11 |

O laço foi **mantido** mesmo após a troca do pivô: custa quase nada e garante o limite de
profundidade mesmo numa sequência infeliz de sorteios.

---

## Parte III — Pivô fixo vs. pivô dinâmico

### O problema do pivô `[-1]`

Um pivô fixo na última posição mantém o algoritmo em O(n²) justamente nas distribuições que o
`benchmark.py` mede.

### Comparação das estratégias (N=1000, comparações contadas pelo próprio algoritmo)

| caso | `[-1]` fixo | mediana-3 fixa | aleatório | **mediana-3 aleatória** |
|---|---:|---:|---:|---:|
| random | 16.584 | 16.236 | 17.423 | 16.634 |
| sorted | 501.498 | 14.480 | 18.376 | 16.774 |
| reverse | 1.000.998 | 14.591 | 18.028 | 17.190 |
| duplicates | 3.585 | 4.078 | 3.849 | 3.851 |
| almost_sorted | 45.933 | 15.409 | 17.824 | 16.970 |
| organ_pipe | 499.999 | **501.496** | 16.204 | 15.567 |
| serrote | 26.500 | **51.150** | 9.488 | 8.942 |
| **PIOR CASO** | **1.000.998** | **501.496** | 18.376 | **17.190** |

### Por que a mediana de três *fixa* foi descartada

É o padrão clássico e é o que o próprio `classical.py:153` usa em `_median_of_three`. Mas ela
tem um buraco adversarial real: no padrão **organ pipe** (`[0,1,…,499,500,499,…,1]`) ela pega
primeiro=`0`, meio=`500`, último=`1`; a mediana é `1`, que gera partição degenerada —
**501.496 comparações, pior que o pivô `[-1]` original**. O padrão *serrote* (`i % 50`) também
a deixa 2× pior que o pivô fixo.

Sortear as três posições fecha esse buraco: nenhum padrão fixo de entrada consegue induzir o
pior caso, porque o adversário teria de acertar os sorteios.

### Resultado medido no código final

| caso | antes (`[-1]`) | agora | ganho |
|---|---:|---:|---:|
| random | 16.584 | 16.585 | 1,0× |
| sorted | 501.498 | 16.379 | **30,6×** |
| reverse | 1.000.998 | 18.065 | **55,4×** |
| duplicates | 3.585 | 3.599 | 1,0× |
| almost_sorted | 45.933 | 16.739 | 2,7× |
| organ_pipe | 499.999 | 14.933 | 33,5× |
| serrote | 26.500 | 9.030 | 2,9× |
| **PIOR CASO** | **1.000.998** | **18.065** | **55,4×** |

O ponto central: em `random` e `duplicates` o ganho é 1,0× — **o pivô dinâmico não cobra nada
onde o algoritmo já ia bem**. Ele só remove os casos catastróficos.

### Escalabilidade (tempo de parede, código final)

| N | sorted | reverse |
|---|---:|---:|
| 1000 | 1,71 ms | 1,69 ms |
| 2000 | 3,56 ms | 3,63 ms |
| 4000 | 8,02 ms | 7,33 ms |

O tempo dobra quando N dobra — comportamento linearítmico. Com o pivô fixo os mesmos casos
iam de 20,62 ms (N=1000) a 314,38 ms (N=4000) em `sorted`, e 505,59 ms em `reverse`: o fator de
perda **crescia** com N (32× → 110×), assinatura de O(n²).

### O que mudou no código

Pouca coisa, e há uma razão estrutural: como a partição é **out-of-place**, o pivô é usado
apenas como **valor de comparação** — não precisa ocupar posição alguma. Num quicksort in-place
seria necessário trocá-lo de lugar e manter índices; aqui bastou trocar de onde vem o valor.

1. `SEMENTE_PIVOT` / `sorteador_pivot` (`:21-22`) — instância `random.Random` própria.
2. `escolher_pivot()` (`:107`) — devolve `(valor, comparações_gastas)`; abaixo de 3 elementos
   mantém `[-1]` com custo 0.
3. `:159` — a linha `valor_pivot = vector_base[-1]` virou a chamada ao auxiliar, somando o custo.

**Detalhe não-óbvio — o gerador aleatório precisa ser próprio.** O `benchmark.py:172` faz
`random.seed(42)` e usa o stream global para gerar os datasets (`benchmark.py:67`). Se a
ordenação sorteasse pivôs desse mesmo stream, cada chamada deslocaria a sequência e os datasets
dos blocos seguintes mudariam, destruindo a reprodutibilidade da comparação entre algoritmos.
Com instância própria os dois streams ficam isolados — verificado: dois processos independentes
produzem contagens de comparações idênticas para **todos** os algoritmos.

**Outro detalhe de correção:** a escolha devolve sempre um elemento **que existe no vetor**.
Isso garante que o balde dos iguais nunca fica vazio e que o `while` sempre encurta
`vector_base`. Um pivô "inventado" (a média dos valores, por exemplo) poderia deixar todos os
elementos de um lado só e **travar o laço**.

---

## Parte IV — Identificação na literatura

O algoritmo é um **Quicksort com particionamento ternário, na variante não-in-place**:

| Componente | Nome na literatura |
|---|---|
| Partição por pivô + recursão + concatenação | **Quicksort** — C.A.R. Hoare, *Quicksort*, The Computer Journal, 1961 |
| Terceiro balde para os iguais | **Particionamento ternário / Dutch National Flag** — Dijkstra, 1976; aplicado a quicksort em **Bentley & McIlroy, _Engineering a Sort Function_, 1993** |
| Pivô no último elemento (versão original) | esquema de **Lomuto** (via Bentley, *Programming Pearls*) |
| Baldes novos em vez de trocas in-place | quicksort *out-of-place* / "quicksort de listas" |
| Recursão só na metade menor | **eliminação de recursão de cauda** — Sedgewick, *Implementing Quicksort Programs*, CACM, 1978 |
| Mediana de três para o pivô | Sedgewick, 1978; a variante **aleatorizada** remove o pior caso adversarial |

### Propriedades

**É estável.** Verificado com chaves marcadas: `[3a,1b,3c,2d,1e,3f]` → `[1b,1e,2d,3a,3c,3f]`.
O quicksort in-place clássico **não é estável**; a estabilidade aqui vem de construir os baldes
preservando a ordem de origem e concatenar. A troca de pivô não afeta essa propriedade.

**Duplicatas em O(n).** O balde dos iguais absorve todas as repetições numa passada. É a
motivação original de Bentley–McIlroy, e aparece nos números: em `duplicates` o algoritmo faz
**3.599** comparações, contra 11.571 do Quick Sort com mediana-3 fixa e 7.653 do DPES.

**Custo: O(n) de memória extra** por nível, contra O(1) do in-place, mais a alocação de listas
novas a cada partição. É o preço da estabilidade e da simplicidade.

### Posição frente aos demais algoritmos do projeto (comparações, N=1000)

| algoritmo | random | sorted | reverse | duplicates |
|---|---:|---:|---:|---:|
| Insertion Sort | 238.487 | 999 | 499.500 | 197.427 |
| Merge Sort | 8.704 | 4.932 | 5.044 | 8.146 |
| Quick Sort (mediana-3 fixa) | 13.807 | 10.542 | 10.549 | 11.571 |
| Authorial DPES (referência) | 18.047 | 14.191 | 15.218 | 7.653 |
| **Autoral (Aluno)** | **16.585** | 16.379 | 18.065 | **3.599** |

Leitura honesta: o Merge Sort ganha em comparações na maioria das colunas (também ao custo de
O(n) de memória), e o Quick Sort in-place fica à frente em `sorted`/`reverse`. O algoritmo
autoral **vence todos em `duplicates`**, por uma margem de 2× sobre o segundo colocado, e supera
o DPES de referência em `random`. O contraste com o Insertion Sort mostra a diferença entre
O(n log n) e O(n²).

### Complexidade final

| | |
|---|---|
| Tempo, caso médio/esperado | **O(n log n)** |
| Tempo, pior caso teórico | O(n²) — inerente a qualquer quicksort sem *introsort*; com pivô aleatorizado a probabilidade é desprezível e nenhuma entrada fixa o induz |
| Tempo, poucos valores distintos | **O(n)** pelo particionamento ternário |
| Memória | O(n) extra |
| Profundidade de recursão | O(log n) garantida pela descida na metade menor |
| Estabilidade | **Estável** |

---

## Parte V — Como validar

Do diretório `codigo/python/`:

```bash
python3 -m unittest student_template -v    # 6 testes de corretude
python3 student_template.py                # demonstração + suíte
python3 benchmark.py --trials 1            # benchmark completo, com o autoral registrado
```

Validações executadas na correção, todas aprovadas:

1. **Corretude** — 6/6 testes (`test_empty`, `test_single`, `test_sorted`, `test_reverse`,
   `test_identical`, `test_random`).
2. **Propriedade** — 3.000 vetores aleatórios (tamanhos 0–60, com negativos e duplicatas):
   0 incorretos, entrada nunca mutada, contadores nunca zerados.
3. **Estabilidade** — preservada, verificada com chaves marcadas.
4. **Ganho do pivô** — 7 distribuições em N=1000; pior caso 18.065 contra 1.000.998.
5. **Sem estouro de pilha** — N até 4000 nas 5 distribuições, nenhum `RecursionError`.
6. **Integração** — `benchmark.py --trials 1` completa sem disparar o `assert` de sanidade, com
   "Autoral (Aluno)" na tabela Markdown e no gráfico PNG.
7. **Reprodutibilidade** — dois processos independentes produzem contagens de comparações
   idênticas para todos os algoritmos (MD5 igual), provando que o RNG próprio não contamina o
   stream global usado na geração dos datasets.

Invariante barata e eficaz para depurar particionamento, caso o código seja alterado de novo:
`len(menor) + len(igual) + len(maior) == len(entrada)`. Na versão original ela falhava já na
primeira execução (9 ≠ 10).
