# Informatica para Ciências e Engenharias - B:
# Trabalho Prático 1 - Alinhamento de Sequencias
# 2021.1
#
# Felipe Pinto

# import sys  # Receive arguments: argv[]
# import argparse
# import os  # system()
# import os.path  # isfile ()


# Main
def main():
    '''
    Recebe duas sequencias de arquivos, compara e salva novos strings
    '''

    # TODO: argv
    # TODO: Comparar sequencias
    # TODO: Salvar novas Sequencias
    # TODO: Multithread

    # TODO: Modify to receive multiple strings strings
    #   Output list:
    #       object 0: List of string names and string content;
    #       rest of objects: Sorted from the greatest comparision value to the least
    #           the comp value, strings
    #           strings = list of (string name, parsed string)
    #       note on names of strings: make default "str" n as the index of the string

    StringsName = []
    StringsComp = []


    return StringsName, StringsComp


if __name__ == '__main__': main()

def strcompare(Strings1, Strings2 = []):
    '''
    Compara um ou dois grupos de strings aos pares
    :param Strings1 e Strings2: ((strindex, value), ...) tuple de strings a serem comparadas
        strindex = index do nome da string
        value = conteudo da string
    :return: Strcompare = ((v, (str1), (str2)), ...)
        v: valor de semelhança entre strings
        str1, str2 = (strindex, value)
            strindex = mesmo que no parametro
            value = strings modificadas para maior semelhança
    '''

    Strcompare = []
    Strings2_isEmpty = len(Strings2) == 0

    if Strings2_isEmpty: Strings2 = Strings1

    for indexStr1 in range(len(Strings1) - int(Strings2_isEmpty)):
        for indexStr2 in range((indexStr1 + 1) * int(Strings2_isEmpty), len(Strings2)):

            str1 = Strings1[indexStr1][1]
            str2 = Strings2[indexStr2][1]

            # Inicializa matrix semelhança

            MatrixSemelhanca = [
                [0 for c in range(len(str1) + 1)] for r in range(len(str2) + 1)
            ]

            for index1 in range(len(MatrixSemelhanca   )): MatrixSemelhanca[index1][0] = - index1
            for index1 in range(len(MatrixSemelhanca[0])): MatrixSemelhanca[0][index1] = - index1

            # Preenche matrix semelhanca

            for r in range(1, len(MatrixSemelhanca)):
                for c in range(1, len(MatrixSemelhanca[r])):
                    MatrixSemelhanca[r][c] = max(
                        MatrixSemelhanca[r - 1][c] - 1,
                        MatrixSemelhanca[r][c - 1] - 1,
                        MatrixSemelhanca[r - 1][c - 1] + int(str1[r - 1] == str2[c - 1]) * 2 - 1
                    )

            # Cria Sequencia de caminhos percorridos na matrix para maior semelhança

            r = len(MatrixSemelhanca   ) - 1
            c = len(MatrixSemelhanca[0]) - 1

            TransformParam = []
            TransformParam.append((r, c))

            while r > 0 or c > 0:
                sequence = [
                    PrecessorCheck_TopLeft(MatrixSemelhanca[r][c], MatrixSemelhanca[r-1][c-1]),
                    PrecessorCheck_Top(    MatrixSemelhanca[r][c], MatrixSemelhanca[r-1][c]),
                    PrecessorCheck_Left(   MatrixSemelhanca[r][c], MatrixSemelhanca[r][c-1])
                ]
                sequence.sort(key=lambda x: -x[0])

                for seq in sequence:
                    r -= seq[2]
                    c -= seq[3]
                    if seq[1]: break

                TransformParam.append((r, c))
            TransformParam.reverse()

            # Gera strings optimizadas

            str1_, str2_ = Parse_optimalstring(str1, str2, TransformParam)

            # Calcula semelhança entre strings

            Semelhanca = 0
            for index1 in range(len(str1_)): Semelhanca += int(str1_[index1] == str2_[index1]) * 2 - 1

            # Salva comparação

            Strcompare.append(
                (
                    Semelhanca,
                    (Strings1[indexStr1][0], str1_),
                    (Strings2[indexStr2][0], str2_)
                )
            )

    return Strcompare

    # # Inicializa matrix semelhança
    #
    # MatrixSemelhanca = [[0 for c in range(len(str1) + 1)] for r in range(len(str2) + 1)]
    #
    # for index1 in range(len(MatrixSemelhanca)): MatrixSemelhanca[index1][0] = - index1
    # for index1 in range(len(MatrixSemelhanca[0])): MatrixSemelhanca[0][index1] = - index1
    #
    # # Preenche matrix semelhanca
    #
    # for r in range(1, len(MatrixSemelhanca)):
    #     for c in range(1, len(MatrixSemelhanca[r])):
    #         MatrixSemelhanca[r][c] = max(
    #             MatrixSemelhanca[r - 1][c] - 1,
    #             MatrixSemelhanca[r][c - 1] - 1,
    #             MatrixSemelhanca[r - 1][c - 1] + int(str1[r - 1] == str2[c - 1]) * 2 - 1
    #         )
    #
    # # Cria Sequencia de caminhos percorridos na matrix para maior semelhança
    #
    # r = len(MatrixSemelhanca) - 1
    # c = len(MatrixSemelhanca[0]) - 1
    #
    # TransformParam = []
    # TransformParam.append([(r, c)])
    #
    # while r > 0 or c > 0:
    #     sequence = [
    #         (1, MatrixSemelhanca[r - 1][c - 1]),
    #         (2, MatrixSemelhanca[r - 1][c]),
    #         (3, MatrixSemelhanca[r][c - 1])
    #     ]
    #     sequence.sort(key=lambda x: -x[1])
    #
    #     for seq in sequence:
    #         if seq[0] == 1 and abs(MatrixSemelhanca[r][c] - seq[1]) == 1:
    #             r -= 1; c -= 1; break
    #         elif MatrixSemelhanca[r][c] == seq[1] - 1:
    #             if seq[0] == 2:
    #                 r -= 1; break
    #             else:
    #                 c -= 1; break
    #
    #     TransformParam.append((r, c))
    # TransformParam.reverse()
    #
    # # Gera strings optimizadas
    #
    # str1_ = Parse_optimalstring(str1, TransformParam[0])
    # str2_ = Parse_optimalstring(str2, TransformParam[1])
    #
    # # Calcula semelhança entre strings
    #
    # Semelhanca = 0
    # for index1 in range(len(str1_)): Semelhanca += int(str1_[index1] == str2_[index1]) * 2 - 1
    #
    # # Compara strings optimizadas
    #
    # return Semelhanca, (str1_, str2_)


def Parse_optimalstring(str1, str2, TransformParam):
    '''
    :param str1, str2: Strings a serem optimizadas
    :param TransformParam: Parametros de optimização
    :return: Strings optimizada
    '''

    Strings = (
        str1 + "-" * (len(TransformParam) - len(str1)),
        str2 + "-" * (len(TransformParam) - len(str2))
    )

    Strings_ = ["", ""]

    for index1 in (0, 1):
        for index2 in range(len(TransformParam) - 1):
            Strings_[index1] += chr(
                45
                +
                int(TransformParam[index2][index1] != TransformParam[index2 + 1][index1])
                * (ord(Strings[index1][TransformParam[index2][index1]]) - 45)
            )

    return Strings_

def PrecessorCheck_Top(cvalue, precessor):
    valuecompare = cvalue == precessor - 1
    return precessor, valuecompare, int(valuecompare), 0


def PrecessorCheck_Left(cvalue, precessor):
    valuecompare = cvalue == precessor - 1
    return precessor, valuecompare, 0, int(valuecompare)


def PrecessorCheck_TopLeft(cvalue, precessor):
    valuecompare = abs(cvalue - precessor) == 1
    return precessor, valuecompare, int(valuecompare), int(valuecompare)

