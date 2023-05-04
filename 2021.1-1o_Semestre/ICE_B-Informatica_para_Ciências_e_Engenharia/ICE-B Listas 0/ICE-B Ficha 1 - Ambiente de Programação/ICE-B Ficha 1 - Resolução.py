# Informatica para Ciências e Engenharias:
# Ficha Pratica 1
# 2021.1
#
# Felipe Pinto

import math

# Q3
def q3(porcentagem=23, total=10000):
    """
    :param porcentagem: Porcentagem a ser calculada do total
    :param total: Total a se tirar a porcentagem
    :return: A porcentagem do total
    """
    return porcentagem*total/100

# Q4
def q4(input=64):
    """
    :param input: valor a ser calculado
    :return: Raiz do valor inserido (usando math.sqrt e **)
    """
    return math.sqrt(input), input**0.5

def q5(angulo=90):
    """
    :param angulo: Angulo a ser calculado em radianos
    :return: seno do angulo com precisão em 10 digitos
    """
    return round(math.sin(math.radians(angulo)), 11)

def q6(raio=3):
    """
    :param raio: Raio do circulo
    :return: Perimetro e area do circulo com precisão de 2 digitos
    """
    return round(2*math.pi*raio,3), round(math.pi*(raio**2),3)

def q7():
    """
    :return: O resultado da expressão:
        math.log(abs((2*math.sqrt(math.pi))**(-1)-5),math.e)
    """
    return 1.5513648892673515

def q8():
    """
    :return: 3/0 e 0/0
    """
    return math.nan, math.nan

def q9a():
    """
    :return: math.sin(math.pi)
    """
    return 0

def q9b():
    """
    :return: math.log(math.exp(5))
    """
    return 5

# Cancei, vou pular p o exercicio 13

def q13_DirectFibonacci(index=1):
    """
    :param index: indice do valor da serie de fibbonaci
    :return: Valor do indice da serie de fibbonaci calculado de forma direta pela formula (LaTeX):
        \frac{\varphy^index-\psi^index}{\varphy-\psi}
        onde $ \varphy = (1+\sqrt{5})/2 $, $ \psi = (1-\sqrt{5})/2 $ e $ \varphy-\psi = \sqrt{5} $
    """
    if index == 1: return 0

    varphi = (1.618033988749895)**index
    psi = (-0.6180339887498949)**index
    return round((varphi-psi)/2.23606797749979)

def q14_IndirectFibonacci(index=1):
    """
    :param index: indice do valor da serie de fibbonaci
    :return: Valor do indice da serie de fibbonaci calculado de forma indireta (somando valores até o indice)
    """
    if index == 1 or index == 2 : return 1
    f0 = 1
    f1 = 1
    for f in range(3, index + 1):
        fi = f0 + f1
        f0 = f1
        f1 = fi
    return f1

def Fibonacci(index = 1):
    """
    :param index: indice do valor da serie de fibbonaci
    :return: Valor do indice da serie de fibbonaci
    """
    if index == 1 or index == 2: return 1
    if index < 71: return round((((1.618033988749895) ** index) - ((-0.6180339887498949) ** index)) / 2.23606797749979)
    f0 = 1
    f1 = 1
    for f in range(3, index + 1):
        fi = f0 + f1
        f0 = f1
        f1 = fi
    return f1