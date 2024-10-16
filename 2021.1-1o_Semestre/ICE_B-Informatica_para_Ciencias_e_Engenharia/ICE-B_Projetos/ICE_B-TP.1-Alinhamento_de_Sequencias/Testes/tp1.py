# Informatica para Ciências e Engenharias - B:
# Trabalho Prático 1 - Alinhamento de Sequencias
# 2021.1
#
# Felipe Pinto - 61387 e Juliana Guimares - 61382

def align_sequences(M, N):
    '''
    :param M e N: strings a ser comparadas
    :return ((M', N'), v):
        (M',N') - Strings optimizadas para maior semelhanca
        v       - valor de alinhamento
    '''

    C = init_matrix(M, N)
    C = fill_matrix(M, N, C)
    P = path_in_matrix(M, N, C)
    M_, N_ = align_by_matrix(M, N, P)

    # Recebe o ultimo valor da matrix de semelhança
    v = C[len(C)-1][len(C[0])-1]

    # for i in range(len(M_)): v += int(M_[i] == N_[i]) * 2 - 1

    return (M_, N_), v

def init_matrix(M, N):
    '''
    Inicializa matrix de comparação com os valores padrões
    :param M e N: strings a serem comparadas
    :return C: Matrix matrix de comparação com os valores padrões
        C[M + 1 linhas][N + 1 Colunas]
    '''

    # Inicializa matrix com tamanhos definidos e C[0] com valores padrões
    C = [[-i for i in range(len(N) + 1)]] \
        + [[0 for c in range(len(N) + 1)] for r in range(1, len(M) + 1)]

    # Preenche matrix com valores padrões
    for i in range(len(C   )): C[i][0] = - i
    # for i in range(len(C[0])): C[0][i] = - i

    return C


def fill_matrix(M, N, C):
    '''
    Preenche matrix de comparação
    :param M e N: strings a serem comparadas
    :param C: Matrix comparação inicializada
    :return: Matrix comparação completa
    '''

    for r in range(1, len(C)):
        for c in range(1, len(C[r])):
            # Recebe maior valor comparando com as celulas anteriores
            C[r][c] = max(
                C[r - 1][c] - 1,
                C[r][c - 1] - 1,
                C[r - 1][c - 1] + int(M[r - 1] == N[c - 1]) * 2 - 1
            )

    return C

def path_in_matrix(M, N, C):
    '''
    Cria um parametro de transformação que pode modificar M e N para maior semelhança
    com base na matrix de comparação
    :param M e N: strings a serem comparadas (inutil presença)
    :param C: Matrix Comparação completa
    :return: parametro de transformação que pode modificar M e N para maior semelhança
    '''

    # r e c recebem os valores da ultima posição em C
    r = len(C) - 1
    c = len(C[0]) - 1

    # Inicializa P com o primeiro termo igual ao ultimo valor de C
    P = [(r, c)]

    def PrecessorCheck_Top(cvalue, precessor):
        '''
        Checa se o valor atual pode ter vindo do precessor
        :param cvalue: Valor atual
        :param precessor: Valor anterior
        :return (precessor, valuecompare, r, c):
            precessor: precessor
            valuecompare: resultado da verificação
            r: valor que deve ser alterado em r
            c: valor que deve ser alterado em c
        '''
        valuecompare = cvalue == precessor - 1
        return precessor, valuecompare, int(valuecompare), 0

    def PrecessorCheck_Left(cvalue, precessor):
        '''
        Checa se o valor atual pode ter vindo do precessor
        :param cvalue: Valor atual
        :param precessor: Valor anterior
        :return (precessor, valuecompare, r, c):
            precessor: precessor
            valuecompare: resultado da verificação
            r: valor que deve ser alterado em r
            c: valor que deve ser alterado em c
        '''
        valuecompare = cvalue == precessor - 1
        return precessor, valuecompare, 0, int(valuecompare)

    def PrecessorCheck_TopLeft(cvalue, precessor):
        '''
        Checa se o valor atual pode ter vindo do precessor
        :param cvalue: Valor atual
        :param precessor: Valor anterior
        :return (precessor, valuecompare, r, c):
            precessor: precessor
            valuecompare: resultado da verificação
            r: valor que deve ser alterado em r
            c: valor que deve ser alterado em c
        '''
        valuecompare = abs(cvalue - precessor) == 1
        return precessor, valuecompare, int(valuecompare), int(valuecompare)

    # Enquanto não chegar na celula C[0][0]
    while r > 0 or c > 0:
        # Cria sequencia de valores a testar com base na serie de funções PrecessorCheck
        sequence = [
            PrecessorCheck_TopLeft(C[r][c], C[r - 1][c - 1]),
            PrecessorCheck_Top(    C[r][c], C[r - 1][c]),
            PrecessorCheck_Left(   C[r][c], C[r][c - 1])
        ]

        # Ordena sequencia em ordem do maior precessor para o menor
        sequence.sort(key=lambda x: -x[0])

        for i in sequence:
            # Modifica r e c com base na comparação dos precessores
            r -= i[2]
            c -= i[3]
            # break quando o precessor for válido
            if i[1]: break

        # Adiciona novo endereço a P
        P.append((r, c))

    # Reverte P para que ele contenha sequencia direta
    P.reverse()

    return P


def align_by_matrix(M, N, P):
    '''
    Optimiza M e N para maior semelhança com base na lista P
    :param M e N: Strings a serem comparadas
    :param P: Lista de parametros que servem para optimizar M e N para maior Semelhança
    :return: (M',N') strings optimizadas para maior semelhança
    '''

    # Junta parametros em uma unica lista para poder fazer o for duplo

    # Expande M e N com "-" pela differença entre seu tamanho e o tamanho de P
    string_i = (M + "-" * (len(P) - len(M)), N + "-" * (len(P) - len(N)))
    string_o = ["", ""]

    # Nota: chr(45) = "-"

    for j in (0, 1):
        for i in range(len(P) - 1):
            # string_o[j] += Adiciona a string de saida
            # chr( Cria caractere do valor interno
            # int(P[i][j] != P[i + 1][j])
            #   compara o ponto com o posterior,
            #   se for igual: iguala a segunda parte da comparação a zero
            #       tornando chr(45) que é igual a "-"
            #   se for differente: Anula o 45 e retorna chr(ord(string_i[j][P[i][j]]))
            #       onde string_i[j][P[i][j]] é o caractere da string parametro de entrada
            #
            # P[i][j] != P[i + 1][j] Compara o valor com seu posterior
            # Se for differente anula 45 e adiciona o caractere
            # Se for igual adiciona chr(45) mais conhecido por "-"
            string_o[j] += chr(45 + int(P[i][j] != P[i + 1][j]) * (ord(string_i[j][P[i][j]]) - 45))

    return string_o[0], string_o[1]