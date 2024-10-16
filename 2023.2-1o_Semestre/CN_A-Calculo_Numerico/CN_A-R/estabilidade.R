f<-function(x) (1-cos(x))/x^2
g<-function(x) (2*sin(x/2)^2)/x^2

#f<-function(x) tan(x)^2/x^2
#g<-function(x) (1-cos(2*x))/(x^2*(1+cos(2*x)))

x<- seq(from=0, to=0.0000001, by=0.000001/1000)

plot(x, y=f(x), type="l", col="red")
lines(x, y=g(x), col="blue")