# ICE-B - Informatica para Ciências e Engenharias - B:
# Trabalho Prático 2 - Porosoidade de Materiais
# 2021.1
#
# Felipe Pinto

import sqlite3              # SQLite3
import math                 # math
import os                   # os
import sys                  # sys
import errno                # errno
import time                 # time
import concurrent.futures   # futures


def main():
    porosidade("test.db", "ordens.txt")



# Porosidade
def porosidade(MateriaisBD, FichComandos, FichResultados="Resultados.txt"):
    '''
    :param MateriaisBD: Nome do arquivo da base de dados em SQL a ser consultada/editada
        irá criar a variavel MateriaisBD_ como base de dados SQLite

    :param FichComandos: Nome do ficheiro contendo comandos a serem executados
        Possui um comando por linha

        Comandos:
        - "CRIAR_TABELAS":              Chama criar_tabelas(MateriaisBD_)
            Cria duas tabelas no banco de dados: Ensaios e Resultados

        - "CARREGAR_ENSAIO $ficheiro":  Chama carregar_ensaio($ficheiro, MateriaisBD_)
            $ficheiro: ficheiro com a medição a ser adicionada ao banco de dados

            Adiciona ao banco de dados os dados do ficheiro de nome $ficheiro

        - "RESUMO $inicio;$fim;$pais":  Chama resumo($inicio, $fim, $pais, MateriaisBD_, FicheiroResultados)
            Escreve no FicheiroResultados uma lista de material_id dos
            experimentos enquadrados por:
                - Periodo delimitados por $inicio e $fim em anos
                - País

        - "GRAFICO $codigo":            Chama grafico($codigo, MateriaisBD_)
            $codigo: material_id

            Gera e salva um grafico das medidas do material de código $codigo

    :param FichResultados: Nome do ficheiro onde os resultados seram escritos

    :return:
        0: Sucesso
     else: Erro
    '''

    # RECEBER PARAMETROS

    # Comandos= {
    #   "CRIAR_TABELAS"= False,
    #   "CARREGAR_ENSAIO"= [],
    #   "RESUMO"= [],
    #   "GRAFICO"= []
    #   }

    try: Comandos = Ler_FichComandos(FichComandos)
    except Exception as error:  print(error); raise

    # CRIAR_TABELAS

    if Comandos["CRIAR_TABELAS"]:

        try: criar_tabelas(MateriaisBD)
        except Exception as error:  print(error); raise

    # CARREGAR_ENSAIO

    if len(Comandos["CARREGAR_ENSAIO"]):

        with concurrent.futures.ThreadPoolExecutor() as executor:
            ensaios = list(executor.map(carregar_ensaio, Comandos["CARREGAR_ENSAIO"]))

        sqlconnection = None
        for i in range(3):
            try:
                sqlconnection = sqlite3.connect(MateriaisBD)
            except sqlite3.Error as error:
                print(error)
                if i == 2: raise
        sqlcursor = sqlconnection

        sqlcursor.execute("BEGIN TRANSACTION")

        try:
            sqlcursor.executemany(
                "INSERT INTO ensaios (id, pais, ano, material_id, concentracao) VALUES(?, ?, ?, ?, ?);",
                [ensaio[0:-1] for ensaio in ensaios]
            )
            for resultado in [ensaio[-1] for ensaio in ensaios]:
                sqlcursor.executemany(
                    "INSERT INTO resultados (id, Ensaios_id, tempo, concentracao) VALUES(?, ?, ?, ?);", resultado)

        except sqlite3.Error as error:
            print(error);
            sqlcursor.execute("ROLLBACK;")
            sqlconnection.close()
            raise

        sqlcursor.execute("COMMIT;")
        sqlconnection.close()

    # RESUME

    if len(Comandos["RESUMO"]):

        with concurrent.futures.ThreadPoolExecutor() as executor:
            resumos = list(executor.map(resumo, [res + [MateriaisBD] for res in Comandos["RESUMO"]]))

        # check if file FichResultados Exists
        if os.path.isfile(FichResultados):
            print(FileExistsError(errno.EEXIST, os.strerror(errno.EEXIST), f"./{FichResultados}"))
            print("Deleting file in: ", end="")

            for i in range(3, 0, -1):
                for _ in range(3): print(".", end=""); time.sleep(.4)
                print(i, end="")

            for _ in range(3): print(".", end=""); time.sleep(.4)
            print("")

            try:
                os.remove(f"./{FichResultados}")
            except PermissionError as error:
                print(error, "Ok, so i dont have permission to delete this file, and probably shouldn't have\
                              Run script again in sudo mode if you are really, REALLY sure about it.", sep="\n")
                raise
            except FileNotFoundError as error:
                print("Huh? thanks for deleting it for me", sep="\n"); pass
            except OSError as error:
                print(error, "Unexpected error occurred", sep="\n"); raise

            print("File successfully removed, resuming operation...")

        try:
            with open(FichResultados, "w") as FichResultados_:
                for resumo_ in resumos: FichResultados_.write(resumo_)

        except:
            FichResultados_.close()
            raise

        FichResultados_.close()

    # GRAFICO




    # Recriar/Atualizar index

    # LER E INTERPRETAR

    if len(Comandos["RESUMO"]):
        pass



    sys.exit(0) # Sucesso


def Ler_FichComandos(FichComandos):
    '''
    Ler Fichcomandos e os organiza em uma biblioteca de comandos
    :param Fichcimandos: Nome do arquivo para ser lido
    :return Comandos: Biblioteca com os comandos listados por seus argumentos
    '''

    if not os.path.isfile(FichComandos):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), f"{os.getcwd()}/{FichComandos}")

    Comandos = {
        "CRIAR_TABELAS": False,
        "CARREGAR_ENSAIO": [],
        "RESUMO": [],
        "GRAFICO": []
    }

    with open(FichComandos, "r") as FichComandos_:

        def FichComandos_readline():
            try:
                return FichComandos_.readline().rstrip().split(" ", 1)
            except EOFError as error: raise error

        line_argvs = FichComandos_readline()

        # CRIAR_TABELAS
        if line_argvs[0].upper() == "CRIAR_TABELAS":
            Comandos["CRIAR_TABELAS"] = True
            line_argvs = FichComandos_readline()

        while True:
            try:
                # CARREGAR_ENSAIO
                while line_argvs[0].upper() == "CARREGAR_ENSAIO":
                    Comandos["CARREGAR_ENSAIO"].append(line_argvs[1])
                    line_argvs = FichComandos_readline()

                # RESUMO
                while line_argvs[0].upper() == "RESUMO":
                    Comandos["RESUMO"].append(line_argvs[1].split(";", 3))
                    line_argvs = FichComandos_readline()

                # GRAFICO
                while line_argvs[0].upper() == "GRAFICO":
                    Comandos["GRAFICO"].append(line_argvs[1])
                    line_argvs = FichComandos_readline()

                if line_argvs[0] != "CARREGAR_ENSAIO" \
                        and line_argvs[0] != "RESUMO" \
                        and line_argvs[0] != "GRAFICO": raise EOFError

            except EOFError: break

    return Comandos


def criar_tabelas(MateriaisBD):
    '''
    Cria duas tabelas na base de dados MateriaisBD

    schema:
        - CREATE TABLE Ensaios(
                id INTEGER,
                ano INTEGER NOT NULL,
                material_id VARCHAR(6) NOT NULL,
                concentracao REAL NOT NULL,
                pais TEXT NOT NULL,
                PRIMARY KEY(id)
            );
        - CREATE TABLE Resultados(
                id INTEGER,
                Ensaios_id INTEGER NOT NULL,
                duracao INTEGER NOT NULL,
                concentracao REAL NOT NULL,
                PRIMARY KEY(id),
                FOREIGN KEY(Ensaios_id) REFERENCES Ensaios(id)
            );
    :return:
    '''

    # Check for database

    if os.path.isfile(MateriaisBD):
        print(FileExistsError(errno.EEXIST, os.strerror(errno.EEXIST),f"./{MateriaisBD}"))
        print("Deleting database in: ", end="")

        for i in range(3, 0, -1):
            for _ in range(3): print(".", end=""); time.sleep(.4)
            print(i, end="")

        for _ in range(3): print(".", end=""); time.sleep(.4)
        print("")

        try: os.remove(f"./{MateriaisBD}")
        except PermissionError as error:
            print(error, "Ok, so i dont have permission to delete this file, and probably shouldn't have\
                          Run script again in sudo mode if you are really, REALLY sure about it.", sep="\n")
            raise
        except FileNotFoundError as error:  print("Huh? thanks for deleting it for me", sep="\n"); pass
        except OSError as error:            print(error, "Unexpected error occurred", sep="\n"); raise

        print("File successfully removed, resuming operation...")

    open(MateriaisBD, "w").close()

    # Connecting to database

    print("Connecting to database")
    sqlconnection = None
    for i in range(3):
        try: sqlconnection = sqlite3.connect(MateriaisBD)
        except sqlite3.Error as error:
            print(error)
            if i == 2: raise
            print(f"Trying again ({i+1} of 2)")

    print(f"Database connected: {sqlite3.version}")

    sqlcursor = sqlconnection.cursor()

    # Create Table: Ensaios e Resumo
    # schema:
    #     - CREATE TABLE Ensaios(
    #             id INTEGER,
    #             ano INTEGER NOT NULL,
    #             material_id VARCHAR(6) NOT NULL,
    #             concentracao REAL NOT NULL,
    #             pais TEXT NOT NULL,
    #             PRIMARY KEY(id)
    #         );
    #     - CREATE TABLE Resultados(
    #             id INTEGER,
    #             Ensaios_id INTEGER NOT NULL,
    #             tempo INTEGER NOT NULL,
    #             concentracao REAL NOT NULL,
    #             PRIMARY KEY(id),
    #             FOREIGN KEY(Ensaios_id) REFERENCES Ensaios(id)
    #         );

    sqlcommands=["""CREATE TABLE Ensaios (
                    id INTEGER,
                    ano INTEGER NOT NULL,
                    material_id VARCHAR(6) NOT NULL,
                    concentracao REAL NOT NULL,
                    pais TEXT NOT NULL,
                    PRIMARY KEY(id)
                );""",
                """CREATE TABLE Resultados (
                    id INTEGER,
                    Ensaios_id INTEGER NOT NULL,
                    tempo INTEGER NOT NULL,
                    concentracao REAL NOT NULL,
                    PRIMARY KEY(id),
                    FOREIGN KEY(Ensaios_id) REFERENCES Ensaios(id)
                );"""]
    
    sqlcursor.execute("BEGIN TRANSACTION;")
    
    try:
        for sqlcommand in sqlcommands:
            sqlcursor.execute(sqlcommand)
    except error:
        sqlcursor.execute("ROLLBACK;")
        sqlconnection.close()
        print(error, "Something went wrong when creating tables: Ensaios e Resultados, aborting process", sep="\n")
        raise

    sqlcursor.execute("COMMIT")
    sqlconnection.close()

    print(f"Tables \"Ensaio\" e \"Resumo\" Created in {MateriaisBD}")

    return
    
def carregar_ensaio(ficheiro):
    '''
    Ler e faz o UPLOAD dos dados contidos no $ficheiro para a base de dados
        - Linha 1 a 5 é feito o upload para a tabela Ensaios
        - Linha 6 em diante é feito o upload para a tabela Resultados

    modelo de ficheiro
        - linha 1: ID do ensáio
        - Linha 2: País que pertence o laboratório
        - Linha 3: Ano do ensáio
        - Linha 4: Id do material
        - Linha 5: Concentração do do soluto no meio exterior
        - Linha 6 em diante: tabela
            medId-tempo:medida
                - medId INTEGER: Id da medida
                - tempo INTEGER: tempo em minutos da medição
                - medida REAL: Concentração medida

    :param ficheiro: nome do ficheiro a ser lido
    :param MateriaisBD: nome da base de dados a ser atualizada
    :return: id do ensaio na tabela Ensaios
    '''

    # Ler ficheiro

    ensaio = []
    medicoes = []

    try:

        # Dados iniciais

        with open(ficheiro, "r") as ficheiro_:

            try:
                ensaio.append(int(ficheiro_.readline().rstrip()))       # id
                ensaio.append(ficheiro_.readline().rstrip())            # pais
                ensaio.append(int(ficheiro_.readline().rstrip()))       # ano
                ensaio.append(ficheiro_.readline().rstrip())            # material_id
                ensaio.append(float(ficheiro_.readline().rstrip()))     # concentracao

                next(ficheiro_)

                medicoes = ficheiro_.readlines()                        # medicoes

            except EOFError as error: print(error, f"File incomplete, ignoring \"{ficheiro}\"", step="\n"); raise

        # tabela de medicoes

        i = -1
        for medicao in medicoes:
            try:
                i += 1

                medicao = medicao.split("-", 1)
                medicao = [medicao[0]] +  medicao[1].split(":", 1)

                for j in range(2): medicao[j] = int(medicao[j])
                medicao[2] = float(medicao[2].rstrip())
                medicao.insert(1, ensaio[0])

                medicoes[i] = medicao

            except TypeError as error:
                print(error, f"do ficheiro: \"{ficheiro}\" a linha {i + 6} não pode ser lida, essa será ignorada")
                del medicoes[i]
                i -= 1

        ensaio += [medicoes]

    except FileNotFoundError as error: print(error, f"file: {ficheiro} cant be added to database"); pass

    return ensaio

def resumo(argvs):
    '''
    Prepara um block de string que será inserido no FicheiroResultados uma lista de material_id dos
    experimentos enquadrados por:
        - Periodo delimitados por inicio e fim em anos
        - País

    Cada lista possui um header com o seguinte formato:
        $n materiais entre $inicio e $fim do país $pais:
            - $n:        Numero de itens da lista
            - $inicio:   inicio inserido como parametro
            - $fim:      fim inserido como parametro
            - $pais:     pais inserido como parametro

    NOTA: Aceita "*" como wildcard para qualquer parametro

    :param inicio:  delimitador de menor ano
    :param fim:     delimitados de maior ano
    :param pais:    filtro por pais
    :param MateriaisBD_: Base de dados a ser consultada
    :return: bloco string
    '''

    inicio = argvs[0]
    fim     = argvs[1]
    pais    = argvs[2]

    MateriaisBD = argvs[3]

    sqlconnection = None
    for i in range(3):
        try:
            sqlconnection = sqlite3.connect(f"file:{MateriaisBD}?mode=ro", uri=True)
        except sqlite3.Error as error:
            print(error)
            if i == 2: raise

    sqlcursor = sqlconnection.cursor()

    query_string = "( "
    query = []

    if inicio != "*":
        query.append(int(inicio))
        query_string += "ano > ? AND "

    if fim != "*":
        query.append(int(fim))
        query_string += "ano < ? AND "

    if pais != "*":
        query.append(pais)
        query_string += "pais = ? AND "

    query_string += "1);"

    try:
        sqlcursor.execute("SELECT material_id FROM Ensaios WHERE " + query_string, query)
    except sqlite3.Error as error:
        print("sqlite3 error", error)
        raise

    resultados = sqlcursor.fetchall()

    sqlconnection.close()

    resume_box = [f"{len(resultados)} materiais entre {inicio} e {fim} do país {pais}"]
    resume_box.extend([res[0] for res in resultados])

    return "\n".join(resume_box) + "\n"

def grafico(material_id, MateriaisBD_):
    '''
    Cria e salva um grafico em PGN com o nome material_id inserido como parametro.

    O grafico deve crusar o Tempo em minutos de cada medida e a Concentração relatvia
    (concentração medida * 100% / Cocentracao inicial), agrupando valores pelo id da medida

    O grafico deve apresentar uma curva teorica em tracejado obtida pela seguinte expressão (tex):

    $$  C = C_0 * (1 - e^{t/k})  $$
        - C     = Concentração teórica
        - C_0   = Concentração Inicial
        - t     = Tempo em minutos
        - k     = Constante de porosidade calculada da seguinte forma (tex)

            $$  k = -(1/k) \sum\limits_{i=1}^{n} t_i / ( \ln(1-C_i/C_o) ) $$

    Parametros do grafico
        - Titulo= Ensáios com o material $codigo
        - legend: ids das medidas
        - x label= Tempo (minutos)
        - y label= Concentrações Relativas (%)
        - x min= 0, y min= 0
        - y max= 3*k
            k: Constante de porosidade calculada

    :param material_id:     id do material na base de dados
    :param MateriaisBD_:    Base de dados a ser consultada
    :return:
    '''

def constante_porosidade(medidas):
    '''
    Constante de porosidade (k) calculada da seguinte forma (tex):

        $$  k = -(1/n) \sum\limits_{i=1}^{n} t_i / ( \ln(1-C_i/C_0) ) $$
            - c_0 = medidas[0]["concentracao"]
            - C_i = medidas[*]["concentracao"]
            - t_i = medidas[*]["tempo"]

    :param medidas: Medidas a serem usadas no calculo
    :return: Constante de Porosidade
    '''

    k = 0
    for medida in range(1, len(medidas)):
        k += medidas[medida]["tempo"] / (math.log(1-(medidas[medida]["concentracao"] / medidas[0]["concentracao"])))

    return k * (-1/len(medidas))

# def concentracao_teorica():




if __name__ == '__main__': main()