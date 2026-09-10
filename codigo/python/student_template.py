"""
TEMPLATE PARA O ALUNO — TRABALHO PRÁTICO 1 (TP1)
Disciplina: Análise e Projetos de Algoritmos (APA)

Instruções:
1. Implemente seu método de ordenação autoral na função `my_authorial_sort`.
2. O retorno deve ser obrigatoriamente a tupla: (lista_ordenada, total_comparacoes, total_movimentacoes).
3. Execute este arquivo diretamente para rodar a suíte de testes de corretude e o benchmark rápido.
"""

from typing import Any, List, Tuple
import unittest
import random

# CLAUDE: [gerador aleatório PRÓPRIO do módulo, separado do 'random' global]
# [o benchmark.py chama random.seed(42) e usa o stream global para gerar os datasets; se a
# ordenação sorteasse pivôs desse mesmo stream, cada chamada deslocaria a sequência e os
# datasets dos blocos seguintes mudariam, quebrando a reprodutibilidade da comparação entre
# algoritmos. Com instância própria e semente fixa os dois streams ficam isolados e as
# execuções do algoritmo continuam determinísticas de uma rodada para outra]
SEMENTE_PIVOT = 42
sorteador_pivot = random.Random(SEMENTE_PIVOT)


def random_number_generation(vector_size: int, min_random_values_range: int, max_random_values_range: int) -> List[int]:
    '''

    função para criar valores aleatórios dinamicamente para não depender de valores fixos

    params:
        vector_size:int -> define o tamanho do vetor a ser usado
        min_random_values_range:int -> define o valor minimo dos valores aleatórios
        max_random_values_range:int -> define o valor máximo dos valores aleatórios

    return:
        devolve uma lista com os valores aleatórios para ordenação

    '''

    # checagem simples de tipagem
    # caso não seja float e nem inteiro, o usuário é notificado e encerra a função
    if not isinstance(vector_size, int) and not isinstance(vector_size, float):
        print('valor inserido não é inteiro. Encerrando o loop de criação de dados')
        exit(0)

    elif vector_size == 0:
        print('tamanho de vetor insuficiente')
        exit(0)

    vector_base = []
    # abs() retira o valor negativo do valor inserido, que ocorre após a conversão de float para int
    for size in range(0, abs(int(vector_size))):
        # TODO: melhorar a randomização para que os valores gerados sejam mais 'aleatórios'
        vector_base.append(random.randint(min_random_values_range, max_random_values_range))
    return vector_base


"""
    IMPLEMENTE AQUI SEU ALGORITMO AUTORAL.

    Parâmetros:
        arr (List[Any]): Lista de entrada a ser ordenada.

    Retorno:
        Tuple[List[Any], int, int]:
            - Lista ordenada
            - Total de comparações realizadas
            - Total de movimentações/trocas realizadas
"""

'''
esta função particiona o vetor em torno de um pivô (o elemento da posição [-1]) e se chama
recursivamente até que tudo esteja ordenado.

param:
    recebe o vetor gerado pela função "random_number_generation" (ou qualquer sublista vinda da recursão)

return
    retorna a tupla (lista_ordenada, comparacoes, movimentacoes) para ser utilizada pela
    função "my_authorial_sort"
'''

'''
escolhe dinamicamente o valor que servirá de pivô (mediador) para uma partição

param:
    recebe o vetor (ou sublista) que está prestes a ser particionado

return
    retorna a tupla (valor_do_pivot, comparacoes_gastas_na_escolha)
'''

def escolher_pivot(vector_base: List[Any]) -> Tuple[Any, int]:
    # vetores com menos de 3 elementos mantêm o pivô em [-1]
    if len(vector_base) < 3:
        return vector_base[-1], 0

    primeira_posicao = sorteador_pivot.randrange(len(vector_base))
    segunda_posicao = sorteador_pivot.randrange(len(vector_base))
    terceira_posicao = sorteador_pivot.randrange(len(vector_base))

    candidatos = [
        vector_base[primeira_posicao],
        vector_base[segunda_posicao],
        vector_base[terceira_posicao],
    ]

    candidatos.sort()

    return candidatos[1], 3



def find_max_value(array_generated: List[Any]) -> Tuple[List[Any], int, int]:
    vector_base = list(array_generated)

    comparison = 0
    steps = 0

    # vetor_maior_final tudo que é maior; a invariante mantida do começo ao fim é
    # vetor_menor_final <= vector_base <= vetor_maior_final, então a concatenação final sai ordenada
    vetor_menor_final = []
    vetor_maior_final = []

    # CLAUDE: [a guarda de tamanho ficava DEPOIS de vector_base[-1], estourando IndexError em lista vazia]
    # [virou a condição do while: um vetor vazio ou de 1 elemento já está ordenado por definição, então
    # o laço nem começa e o caso base encerra o processamento — antes o único elemento era perdido]
    while len(vector_base) > 1:

        # o pivô é usado apenas como VALOR de comparação, não precisa estar em posição nenhuma do vetor
        valor_pivot, comparison_escolha_pivot = escolher_pivot(vector_base)
        comparison += comparison_escolha_pivot

        vetor_menor_que_mediador = []
        vetor_maior_que_mediador = []
        vetor_igual_mediador = []

        # =========================================================================
        # loop de particionamento: cada valor vai para exatamente um dos três vetores
        for valor_atual in vector_base:

            # aqui é len(menor) + len(igual) + len(maior) == len(entrada)
            comparison += 1
            if valor_atual < valor_pivot:
                vetor_menor_que_mediador.append(valor_atual)

            elif valor_atual > valor_pivot:
                comparison += 1
                vetor_maior_que_mediador.append(valor_atual)

            else:
                # modo easy, só adiciona pois são valores iguais ao pivô
                comparison += 1
                vetor_igual_mediador.append(valor_atual)

            steps += 1

        # =========================================================================


        # CLAUDE: [só o MENOR dos dois vetores desce por recursão; o maior continua no while]
        # [com o pivô fixo na posição [-1], um vetor já ordenado ou invertido joga todos os elementos
        # para um lado só e a recursão pura chegava a N níveis — o benchmark.py usa N=1000 com as
        # distribuições 'sorted' e 'reverse' e estourava RecursionError.
        if len(vetor_menor_que_mediador) <= len(vetor_maior_que_mediador):
            menor_ordenado, comparison_recursao, steps_recursao = find_max_value(vetor_menor_que_mediador)

            # os menores já ordenados e os iguais ao pivô ficam definitivamente à esquerda
            vetor_menor_final = vetor_menor_final + menor_ordenado + vetor_igual_mediador
            steps += len(menor_ordenado) + len(vetor_igual_mediador)

            # sobra o vetor dos maiores para ser particionado na próxima volta do while
            vector_base = vetor_maior_que_mediador

        else:
            maior_ordenado, comparison_recursao, steps_recursao = find_max_value(vetor_maior_que_mediador)

            # os iguais ao pivô e os maiores já ordenados ficam definitivamente à direita
            vetor_maior_final = vetor_igual_mediador + maior_ordenado + vetor_maior_final
            steps += len(maior_ordenado) + len(vetor_igual_mediador)

            # sobra o vetor dos menores para ser particionado na próxima volta do while
            vector_base = vetor_menor_que_mediador

        comparison += comparison_recursao
        steps += steps_recursao

    # =========================================================================
    # algoritmo: pela invariante mantida no while, tudo à esquerda é menor e tudo à direita é maior
    # que o que sobrou em vector_base (0 ou 1 elemento), então a junção já está ordenada]
    vetor_ordenado = vetor_menor_final + vector_base + vetor_maior_final
    steps += len(vetor_ordenado)

    return vetor_ordenado, comparison, steps


def my_authorial_sort(arr: List[Any]) -> Tuple[List[Any], int, int]:
    # CLAUDE: [a função era um esboço que devolvia a entrada intacta com comparison = steps = 0]
    # [agora delega para find_max_value, que é o algoritmo de fato, e apenas repassa a tupla no
    # contrato exigido pelo enunciado: (lista_ordenada, total_comparacoes, total_movimentacoes)]
    vector_base, comparison, steps = find_max_value(arr)

    return vector_base, comparison, steps


# =============================================================================
# SUÍTE DE TESTES AUTOMÁTICA DE VALIDAÇÃO
# =============================================================================
class TestStudentAuthorialSort(unittest.TestCase):
    def assert_sorted(self, original: List, result: List):
        self.assertEqual(len(result), len(original), "Tamanho divergente!")
        self.assertEqual(sorted(original), result, "A lista não foi ordenada corretamente!")

    def test_empty(self):
        res, _, _ = my_authorial_sort([])
        self.assert_sorted([], res)

    def test_single(self):
        res, _, _ = my_authorial_sort([99])
        self.assert_sorted([99], res)

    def test_sorted(self):
        data = list(range(100))
        res, _, _ = my_authorial_sort(data)
        self.assert_sorted(data, res)

    def test_reverse(self):
        data = list(range(100, 0, -1))
        res, _, _ = my_authorial_sort(data)
        self.assert_sorted(data, res)

    def test_identical(self):
        data = [5] * 50
        res, _, _ = my_authorial_sort(data)
        self.assert_sorted(data, res)

    def test_random(self):
        import random
        random.seed(42)
        data = [random.randint(-1000, 1000) for _ in range(200)]
        res, _, _ = my_authorial_sort(data)
        self.assert_sorted(data, res)


if __name__ == "__main__":
    print("🧪 Executando testes unitários no seu algoritmo autoral...")

    vetor_demonstracao = random_number_generation(100, 25, 125)
    print(f'vetor original: {vetor_demonstracao}')
    print(f'valor definido como pivô (posição [-1]): {vetor_demonstracao[-1]}')
    resultado, total_comparacoes, total_movimentacoes = my_authorial_sort(vetor_demonstracao)
    print(f'vetor ordenado: {resultado}')
    print(f'comparações: {total_comparacoes} | movimentações: {total_movimentacoes}\n')
    unittest.main(verbosity=2)
