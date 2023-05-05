# Informatica para Ciências e Engenharias:
# Ficha Pratica 4
# 2021.1
#
# Felipe Pinto

import math


# Q1
def obtemConcentrPb():
    """Retorna uma matriz com a concentração de chumbo no solo em vários
    pontos e, para cada ponto, a várias profundidades. A matriz tem:
        • na primeira linha, o ponto de amostragem;
        • na segunda linha, a profundidade da amostra, em centimetros;
        • na terceira linha, a concentracao de chumbo da amostra,
          em partes por milhao.
    """
    mat = \
        [
            [
                2, 1, 2, 16, 1, 14, 10, 13, 9, 2, 17, 18, 18, 11, 15, 20, 6, 1,
                8, 15, 20, 14, 7, 3, 6, 16, 10, 13, 2, 4, 3, 14, 13, 10, 14,
                20, 18, 17, 12, 8, 10, 14, 1, 9, 4, 16, 5, 15, 14, 7, 11, 19,
                20, 15, 13, 5, 1, 12, 18, 3, 6, 17, 16, 4, 8, 10, 16, 13, 9,
                6, 16, 8, 12, 5, 8, 15, 19, 19, 16, 19, 12, 11, 2, 14, 7, 12,
                3, 12, 13, 14, 11, 14, 13, 18, 5, 2, 20, 3, 16, 11
            ], [
            62, 102, 82, 190, 117, 39, 156, 49, 153, 130, 69, 104, 122, 28,
            139, 200, 154, 178, 49, 103, 176, 171, 105, 35, 193, 31, 169,
            80, 127, 181, 112, 91, 58, 154, 130, 174, 141, 50, 87, 73, 83,
            185, 65, 151, 72, 130, 157, 71, 74, 142, 187, 21, 178, 154, 115,
            77, 102, 48, 128, 62, 36, 166, 161, 55, 150, 152, 100, 191,
            172, 52, 132, 26, 150, 80, 147, 78, 103, 35, 139, 191, 162, 92,
            72, 77, 100, 48, 128, 171, 182, 84, 62, 120, 164, 50, 167, 101,
            191, 140, 65, 92
        ], [
            13, 14, 6, 28, 16, 22, 10, 14, 22, 25, 8, 4, 27, 22, 14, 7, 24,
            8, 2, 3, 6, 19, 21, 7, 9, 20, 27, 22, 4, 11, 10, 5, 31, 9, 26,
            20, 13, 27, 22, 11, 8, 8, 24, 24, 24, 25, 25, 21, 15, 9, 7, 16,
            12, 18, 19, 17, 9, 21, 7, 27, 17, 7, 3, 23, 6, 15, 25, 13, 11,
            5, 21, 23, 20, 23, 18, 9, 12, 15, 25, 10, 24, 6, 0, 21, 16, 18,
            18, 23, 26, 18, 25, 24, 23, 2, 28, 8, 16, 27, 21, 18
        ]
        ]
    return mat


# Q1 - a) Amostras no ponto 1
def q1a(ponto=1):
    """
    :param ponto: Ponto de coleta
    :return: Soma de coletas no ponto indicado
    """
    Pontos = obtemConcentrPb()[0]
    occurenceCounter = 0

    for p in Pontos:
        occurenceCounter += int(p == ponto)

    return occurenceCounter


# Q1 - b) Amostras com profundidade pelomenos 90
def q1b(profundidade=90):
    """
    :param profundidade: Profundidade minima das amostras
    :return: quantidade de amostras tiradas na profundidade minima
    """
    profundidades = obtemConcentrPb()[1]
    occurrenceCounter = 0

    for p in profundidades:
        occurrenceCounter += int(p >= profundidade)

    return occurrenceCounter


# Q1 - c) Concentração média a mais de 1m de profundidade
def q1c(profundidade=1):
    """
    :param profundidade: Profundidade minima das amostras
    :return: Concentração média das amostras Consideradas
    """
    profundidade *= 100

    amostras = obtemConcentrPb()

    sumConcentracao = 0
    sumAmostras = 0

    for i in range(len(amostras[0])):
        if amostras[1][i] > profundidade:
            sumConcentracao += amostras[2][i]
            sumAmostras += 1

    return round(sumConcentracao / sumAmostras, 3)


# Q1 - e)

# Q4

# Q4 - a)

D = [
    [1, 0.1],
    [2, 0.9],
    [3, 0.4],
    [4, 0.2],
    [5, 0.7]
]


def comprPercurso(Posicoes):
    distancia = 0
    for i in range(len(Posicoes) - 1):
        somaquadratica = 0
        for j in range(len(Posicoes[i])): somaquadratica += (Posicoes[i][j] - Posicoes[i + 1][j]) ** 2
        distancia += math.sqrt(somaquadratica)
    return distancia
