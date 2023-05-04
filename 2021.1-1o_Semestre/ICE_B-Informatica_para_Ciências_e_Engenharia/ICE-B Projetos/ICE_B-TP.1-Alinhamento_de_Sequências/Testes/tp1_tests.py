"""
Módulo de testes unitários para o TP1
Instruções:
    Pôr este ficheiro na pasta do trabalho prático juntamente com o ficheiro tests.txt.
    O módulo principal do trabalho prático tem de ser um ficheiro de nome tp1.py    
    Premir F5 no Spyder (ou Run) para executar os testes
"""
from importlib import import_module
#import numpy as np

# read all tests

def readTests():
    fName = "tests.txt"
    fich = open(fName, 'r')
    P = []
    A = []
    B = []
    MC = []
    D = []
    ME = []
    M = []
    mat = 'A'
    for line in fich.readlines(): 
        l = line.strip()
        if (l!=''):            
            if (l[0]=='P'):
                if M!=[]:
                    ME.append(M)
                P.append(getPair(l))
            elif (l[0]=='A'):
                M = []
                M.append(getList(l[8:-1]))
                mat = 'A'
            elif (l[0]=='B'):
                A.append([M])
                M = []
                M.append(getList(l[8:-1]))
                mat = 'B'
            elif (l[0]=='C'):
                B.append([M])
                M = []
                M.append(getPath(l[8:-1]))
                mat = 'C'
            elif (l[0]=='D'):
                MC.append(M)
                D.append([getPair(l)])
                mat = 'D'
            elif (l[0]=='E'):
                M = []
                M.append(getTriple(l[9:-1]))
                mat = 'E'
            else:
                if mat == 'A':
                    M.append(getList(l))
                if mat == 'B':
                    M.append(getList(l))
                if mat == 'C':
                    M.append(getPath(l[1:-1]))
                if mat == 'E':
                    M.append(getTriple(l[2:-1]))
    ME.append(M)
    fich.close()
    return P, A, B, D, MC, ME

def getList(s):
    s = s.split(']')[0]
    s =s[1:]
    vs = s.split(',')
    L = []
    for x in vs:
        L.append(int(x))
    return L

def getPair(s):
    s = s[9:-2]
    s = s.split(',')
    s0 = s[0][:-1]
    s1 = s[1][2:]
    return (s0,s1)

def getTriple(s):
    s = s.split(',')
    s0 = s[0][1:-1]
    s1 = s[1][2:-2]
    s2 = int(s[2])
    return ((s0,s1),s2)

def getPath(s):
    #s = s[8:-1]
    s = s.split(')')[:-1]
    s[0] = s[0][1:]
    for i in range(1,len(s)):
        s[i] = s[i][3:]
    L = []
    for x in s:
        xx = x.split(',')
        L.append((int(xx[0]),int(xx[1])))
    return L

# execute tests

def test_function(function, tests):
    """
    run all tests on a function
    """
    results = []
    ix = 1
    for args, target in tests:
        test = function.__name__+', test '+str(ix)
        ix+=1
        try:
            res = function(*args)
            if res in target:
                results.append(test+' OK')
            else:
                results.append(test+' Incorrect result')
        except Exception as exception:
            results.append(test+' Exception raised: '+repr(exception))
    print('\n'.join(results))


def test_all(module_name,tests):
    try:
        module = import_module(module_name)
        for fn,test in tests:
            try:
                function = getattr(module,fn)
                test_function(function,test)
            except:
                print(fn+' not found')
    except:
        print(module_name+'.py not found. Aborting all tests.')


print('***** Tests *****')
P, A, B, D, MC, ME = readTests()
tests = []
La = []
Lb = []
Lc = []
LMc = []
Ld = []
Le = []
LMe = []
for i in range(len(P)):
    La.append(((P[i][0],P[i][1]), A[i]))
    Lb.append(((P[i][0],P[i][1],A[i][0]), B[i]))
    LMc.append(((P[i][0],P[i][1],B[i][0]), MC[i]))
    Ld.append(((P[i][0],P[i][1],MC[i][0]), D[i]))
    LMe.append(((P[i][0],P[i][1]), ME[i]))
tests.append(('init_matrix',La))
tests.append(('fill_matrix',Lb))
tests.append(('path_in_matrix',LMc))
tests.append(('align_by_matrix',Ld))
tests.append(('align_sequences',LMe))
test_all('tp1',tests)

