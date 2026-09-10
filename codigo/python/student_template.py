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
esta função tem como objetivo percorrer o vetor original e identificar o valor máximo para realizar
a ordenação

param:
    recebe o vetor gerado pela função "random_number_generation"

return
    retorna o valor máximo do vetor para ser utilizado pela função "my_authorial_sort"
'''


def find_max_value(array_generated: List[Any]):
    vector_base = list(array_generated)
    lenght_vector = len(vector_base)
    last_index_value = vector_base[-1]
    vetor_menor_que_mediador = []
    vetor_maior_que_mediador = []
    vetor_igual_mediador = []
    ultimo_valor_adicionado_vetor_maior= 0
    ultimo_valor_adicionado_vetor_menor = 0
    # =========================================================================
    # loop inicial para percorrer para identificar o maior valor do vetor, caso seja maior que 1_000_000 será usado uma
    # constante para minimizar re atribuições para dados muito longos

    if lenght_vector >= 2:
        print(f'valor definido como mediador: {last_index_value}: {vector_base.index(last_index_value)} -- vetor OG: {vector_base}')
        for values_to_compare in range(0, lenght_vector):

            # o valor [-1] é maior que o valor que estou comparando?
            if last_index_value > values_to_compare:

                if values_to_compare > ultimo_valor_adicionado_vetor_menor:
                    ultimo_valor_adicionado_vetor_menor = values_to_compare  # atualizo somente o ultimo valor máximo
                    vetor_menor_que_mediador.append(vector_base[values_to_compare])


                elif values_to_compare < ultimo_valor_adicionado_vetor_menor:
                    for index_values_vetor_menor in vetor_menor_que_mediador:
                        if values_to_compare > index_values_vetor_menor:
                            index_add = vetor_menor_que_mediador.index(index_values_vetor_menor)
                            vetor_menor_que_mediador.insert(index_add, values_to_compare)

    # ==================================================================================================
            # modo easy, só adiciona pois são valores iguais
            elif last_index_value == values_to_compare:
                vetor_igual_mediador.append(vector_base[values_to_compare])

    # ==================================================================================================

            # o valor [-1] é menor que o valor que estou comparando?
            elif values_to_compare > last_index_value:

                if values_to_compare > ultimo_valor_adicionado_vetor_maior:
                    ultimo_valor_adicionado_vetor_maior = values_to_compare  # atualizo somente o ultimo valor máximo
                    vetor_maior_que_mediador.append(vector_base[values_to_compare])


                elif values_to_compare < ultimo_valor_adicionado_vetor_maior:
                    for index_values_vetor_maior in vetor_maior_que_mediador:
                        if values_to_compare > index_values_vetor_maior:
                            index_add = vetor_maior_que_mediador.index(index_values_vetor_maior)
                            vetor_maior_que_mediador.insert(index_add, values_to_compare)


    return f'vetor menor:{vetor_menor_que_mediador}\n\nvetor igual{vetor_igual_mediador}\n\nvetor maior{vetor_maior_que_mediador}\n\n'


def my_authorial_sort(arr: List[Any]) -> Tuple[List[Any], int, int]:
    vector_base = list(arr)
    lenght_vector = len(vector_base)
    comparison = 0
    steps = 0
    # usar dicionário?
    score_vector = []
    # =========================================================================
    # TODO: Escreva sua lógica autoral aqui.
    # Exemplo temporário (substitua pelo seu algoritmo):

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
    # my_authorial_sort(random_number_generation(10, 25, 75))
    print(find_max_value(random_number_generation(10, 25, 125)))
