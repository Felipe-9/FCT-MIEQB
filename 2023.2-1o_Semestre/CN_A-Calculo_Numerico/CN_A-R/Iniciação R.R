setwd( "~/Documents/College : Study/FCT - Mestrado Integrado em Engenharia Química e Bioquímica/FCT-MIEQB-Mestrado_Integrado_em_Engenharia_Quimica_e_Bioquimica/2024.2-1o_Semestre/CN_A-Calculo_Numerico/CN_A-R" )
#Operações
b<-289*3+456/2-11^2;b
d<-sqrt(23)/(log(exp(23)+ sin(1/2)));d

# Vetores
k<-c(0.12,0.23,0.29);k
v<-1000*(k+1);v
w<-rep(1,3);w
j<-1000*(k+w);j
u <- seq(from=1, to=5, by=1);u
v1<-exp(u);v1

#Matrizes
v<-c(1,2,3,4,5,6,7,8,9)
M<-matrix(v, nrow = 3, ncol = 3, byrow = FALSE);M

v1<-c(1,2,3)
v2<-c(4,5,6)
v3<-c(7,8,9)
M<-rbind(v1,v2,v3);M
M<-cbind(v1,v2,v3);M

#Produto matricial de A uma matrix 3x2 e B uma matrix 2x3
# v<-c(1,2,3,4,5,6)
v<-seq(from=1,to=6,by=1)
A<-matrix(v, nrow = 3, ncol = 2, byrow = TRUE);A
B<-matrix(v, nrow = 2, ncol = 3, byrow = TRUE);B
C<-A%*%B;C

#Transposta de uma matriz C
Ctrans<-t(C);Ctrans

#Inversa de uma matriz quadrada
v1<-c(1,-2,3)
v2<-c(4,5,-6)
v3<-c(7,-8,9)
M<-rbind(v1,v2,v3);M
Minv<-solve(M);Minv

#Determinante
Mdet<-det(M);Mdet

#Elemento 2,3 da matriz
C[2,3]

#Linha 3 da matriz 
C[3,]


# Tipo de objeto data frame
x1<-1:10
x2<-11:20
x3<-letters[1:10]
# cria data frame com 3 colunas x1, x2 e x3
d1<-data.frame(x1, x2, x3); d1
attributes(d1)
# soma a coluna x2
sum(d1$x2)
#acede à coluna x3
d1$x3

# Ler tabela de dados de ficheiro externo
dados<-read.table("Tabeladados", header = TRUE);dados
summary(dados)
mean(dados$fxi)

#A instrução if...else...
x<- 10
if(x<=0){  
f<-x^2+3*x+1
}else{
f<-2*x^2+5*x
}
f

#Funções
f<-function(x){log(cos(x))}
f(pi/2)

#Função por ramos
classifica<-function(nota){
  if (nota<9.5){ decisão<-"reprovado"	
  }else{ decisão<-"aprovado" }
  return(decisão)
}
classifica(5)

#Gráfico duma função (plot)
f<- function(x) x^3+2*x^2+3*x+1
x<- seq(from=-10, to=10, by=1/2)
plot(x, f(x), type="l", col="red")
plot(x, f(x), type="p", col="blue")

#Gráfico de duas ou mais funções
curve(f, col="red", xlim=c(-10,10),ylim=c(-1000,1000),ylab="p(x)")
curve(f,
  col="red",
  xlim=c(-10,10),
  ylim=c(-1000,1000),
  ylab= "p(x)",
)
lines(x, exp(x),col="green")
curve(exp(x), col="blue", add=T)
abline(v=0)
text(6, 120, "exp(x)")
text(-9, -400, "f(x)")

#Gráfico de pontos duma função
x<- c(0,2,5,6)
y<- c(-3,-1,27,51)
plot(x,y,col="blue")
f<- function(x) 1/3*x^3-2/3*x^2+x-3
curve(f, col="red",add=T)

#Gráfico duma data frame
tabela<-read.table("Tabeladados",header=T)
tabela
plot(tabela)

#Instruções repetidas: ciclo for()
n<-5
X<-c(-pi/3, -2, 0 , 3, 2*pi)
soma=0
produto=1
for (i in 1:n){
  soma<-soma+cos(X[i])
  produto<-produto*cos(X[i])
  }
resultado<-c(soma, produto)
print(resultado)
sum(cos(X))
prod(cos(X))

#Resolução de sistemas de equações lineares
v<-c(1,2,0,0,1,-1,3,1,1)
M<-matrix(v, nrow = 3, ncol = 3, byrow = TRUE);M
b<-c(1,0,1)
S2<-solve(M,b);S2
S3<-solve(M)%*%b;S3

#Obter as raizes dum polinómio 
pol<-function(x) 3*x^2-35/2*x + 49/2
p<-c(49/2,-35/2,3)
polyroot(p)

#Integração 
I<-integrate(pol,0,2);I
print(paste('Valor do integral:',I))

#Exercício 4 ficha 1
# a)
#sistema S1
y1<-function(x) 26/13-4/13*x
y2<-function(x) 20/10-3/10*x
curve(y1, col="red", xlim=c(-10,10))
curve(y2,col="green",add=T)

#b)
#sistema S2
z1<-function(x) 25.9/13-4/13*x
z2<-function(x) 20.1/10-3/10*x
curve(z1, col="red", xlim=c(-10,10))
curve(z2,col="green",add=T)

#c)
#S1
m1<-c(4,13)
m2<-c(3,10)
M1<-rbind(m1,m2);M1
b1<-c(26,20)
solve(M1,b1)

#S2
b2<-c(25.9,20.1)
solve(M1,b2)

#d)......


