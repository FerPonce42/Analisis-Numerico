import numpy as np

#Definir xl y xu
xl=4
xu=6

#Definir la función
def f(x): return 2*x**2-8*x-9

for i in range(30):

  #Encontramos el punto medio xr
  xr= (xl + xu) /2
  print(f"iteracion {i}:")
  print(f"En [{xl},{xu}] tenemos" )
  print(f"xr={xr}" )
  print(f"")
  
  #Evaluamos en el punto medio xr
  f(xr)

  if f(xl)*f(xr)<0 :
     xu=xr
  else:
     xl=xr