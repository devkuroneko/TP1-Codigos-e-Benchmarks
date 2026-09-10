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
import numpy as np

'''

função para criar valores aleatórios dinamicamente para não depender de valores fixos
params:
    vector_size:int -> define o tamanho do vetor a ser usado
    min_random_values_range:int -> define o valor minimo dos valores aleatórios
    max_random_values_range:int -> define o valor máximo dos valores aleatórios
return:
    devolve uma lista com os valores aleatórios para ordenação
    
'''


def random_number_generation(vector_size: int, min_random_values_range: int, max_random_values_range: int) -> List[int]:
    vector_base = []
    # começa em zero e vai até o (vector_size - 1)
    # se começar em 1 deverá ser acrescentado + 1 no vector_size pois o range não considera o ultimo numero
    for size in range(0, vector_size):
        vector_base.append(random.randint(min_random_values_range, max_random_values_range))
    return vector_base


def my_authorial_sort(arr: List[Any]) -> Tuple[List[Any], int, int]:
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
    vector_base = list(arr)
    comparison = 0
    steps = 0
    min_value_found = 0
    max_value_found = 0

    # =========================================================================
    # TODO: Escreva sua lógica autoral aqui.
    # Exemplo temporário (substitua pelo seu algoritmo):
    # loop inicial para percorrer para identificar o tamanho do vetor é par ou impar
    for values in range(0, len(vector_base)):
        '''
        encontrar o menor valor e maior valor do vetor
        e ir alocando a cada dois  valores
        '''
        # pega o ultimo valor do vetor
        valor_atual = vector_base[-1]

        # comparação primeiro e ultimo valor
        if vector_base[0] == vector_base[-1]:
            print(f'valores iguais\n skip')


    # =========================================================================

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
    # unittest.main(verbosity=2)
    my_authorial_sort(random_number_generation(10, 25, 75))
