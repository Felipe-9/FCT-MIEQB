Anotações
# Introdução
## Primeiro exp
Com o reator recebendo O2, paramos o respirometro cortando o acesso ao O2, e o declive de consumo é diretamente relacionado com o crescimento de bacterias
## Equação: Velocidade espeçifica de consumo
> "Assumindo a velocidade de consumo de O2 igual à sua velocidade de transferência e desprezando a manutenção obtém se a equação":
+ Não especificamos qual a velociade de consumo, a correta é a velocidade espeçifica V(O2)
## Resultados experimentais e discussões
### 1
####
> "E considerando também que a concentração inicial de CO2 era nula conseguimos traçar uma reta de ln(C∗ − CL) em função de *t* em que o kL a é o simétrico do declive e C∗ o exponencial da ordenada na origem."
#### C*
1.16 : mmol/L: Solubilidade do o2
20.95: %O2 no ar
32   : massa molar
#### Figura 3
> "Grafico de $ ln(C∗ − CL) × t − 19.30 $, o tempo foi defasado para alinhar com o começo do arejamento, da regressão podemos derivar $k'$ e $C^∗$"
*Derivar* no sentido de retirar de
#### Discussão
>> Integrar para mostrar o erro na ordenada na origem
- O erro de C* é esperado pois ao integrar podemos verificar que quando t0 não é zero c0 tbm n será defasando o c* do c0
### 2
> "Contudo entre os 80 e 120 minutos já existe uma *-maior-* menor velocidade de crescimento, indicando assim a proximidade de um estado estacionário, contudo, é ainda percetível um crescimento considerável. A partir dos 130 minutos pode ser considerado um estado estacionário, já que há o crescimento é praticamente inexistente."
#### Figura 6
Na tabela foi posta a unidade do X ao invés do lnX
#### Figura 11
- Para acomodar o outliner tanto foi defazado do t os 10.5 como houve uma adaptação
### 3
#### Figura 14
Unidade V(O2) falta dividir por minuto
$ X        $ => mg/L
$ r_{O2} $ => mg(O2)/L.min
$ V_{O2} $ => mg(o2)/mg(x).min
#### Figura 15
Faltou apontar a equação usada que está apensas apresentada na introdução
$V_{O2}=Y'_{O2/X} \mu + m_{O2}$
Y'(O2/X): Coeficiente de rendimento de crescimento verdadeiro
- Nossos pontos foram escolhidos tanto com base no erro quadratico como para obter um valor positivo do declive que correlaciona com um valor real de $Y'(O2/X)$, negativo n faria sentido
- Faltou as unidades no grafico
#### Discussão
> "Através do gráfico da figura 15, retirámos um valor baixo de coeficiente de rendimento de cres- cimento (m = 0.022 mg (O2)/mg (X) min). Logo concluímos que a maioria do oxigénio foi utilizado no crescimento celular. Para obtermos a melhor linearização possível selecionámos alguns pontos pois havia uma variedade de valores. Apesar de tudo, sabemos que estes valores ficam aquém do esperado."
- Coeficiente de rendimento => Coeficiente de manutenção
- Supostamente deviamos ter uma reta constante no V(O2) se houvesse uma queda devia ser maior, mas não percebemos isso
#### 4
Equação devia ter: $(C^*-C_L)\,K_{L\,a} = r_{O2}$
> "O declive da função de C∗−CL em função de rO2, como declive (m) igual ao inverso de kLa permitenos chegar ao valor do declive."
Está incorreto pois usamos kla diretamente ao invés do inverso
#### Discussão
> Esta diferença pode ser explicada pela dificuldade na transferência de oxigénio da fase gasosa para a líquida, devido à existência de microrganismos no sistema e também devido ao aumento de viscosidade do reator
provocada pela espuma, bolhas e células inoculadas
### 5
#### Discussão
> Verificamos assim que esta situação se trata de uma limitação cinética por metabolismo celular.
- Como esperado
### 6
#### Figura 17
Na legenda Devia ter CH3COOH
#### Discussão
Como o gráfico é mássico convertemos a proporção 2:1 de mols para massa (g) que resulta em 16/15=1.067:1 que condiz com o gráfico
### 7
#### Equações
$ m_{acetato} = 9.5 * 2 * 10^3/10^2 $
    - 9.5       - Conentração de acetato
    - 2 -> 3    - mililitros deviam ser 2ml
    - $10^3/10^2$ - conversão de unidades para grama/litro
$ V_{acetato} = 0.5 ∗ 0.002 ∗ 0.1 (inóculo) $
    - 0.5 -> 
    - 0.002 -> 0.003 - percebemos depois que houve alteração no protocolo desconsiderando os dados usados na realidade
    - 0.1 -> 0.025   - inoculo
ΔS (correto) = 7600000;
Y(X/S) = 315.56/7600000 = 4.152105263 E-5 < 1.66 E−4 
o que não muda nossas conclusões
#### Grafico 18
- Unidades do V(ac) devia ser mg(Ac)/mg(X).min
- mu é taxa especifica
- unidade do Y': mg(X)/mg(Ac)
# Conclusão
> "Neste trabalho foi possível aplicar e verificar diretamente os conhecimentos sobre bioreatores com culturas aeróbicas e tudo o que isso implica, incluído principalmente o arejamento e agitação e homogeneização da *cultura* consolidando-os."
> "Com a análise das necessidades de oxigénio foram identificadas algumas das fases de crescimento, mas de forma mais pronunciada a fase exponencial e a fase estacionária."
- é possível ver a fase exponencial e estacionária muito fácilmente atraves de análise do gráfico de consumo de O2 contudo tambem se existe a possibilidade de se ter visto uma fase de "lag" até os 10min e o início de uma fase de morte no ultimo ponto.