import numpy as np

#Función declarada en la tarea
def f(x): 
    return 0.1*x - 2*np.exp(-0.5*x)

#Tabular hasta encontrar un cambio de signo
for i in np.arange(0, 10, 0.5):
    print(f"f({i:.1f}) = {f(i):.5f}")


#Tomamos los valores conseguidos como base, de la tabulación anterior
xl = 3.0
xu = 3.5

for i in range(5):
    #aplico la tabulacion para xl, xu respectivamente
    y_xl = f(xl)
    y_xu = f(xu)

    #aplico la formula para hallar xr 
    xr = xu - (((y_xu) * (xl - xu))/(y_xl - y_xu))
    
    print("----------------------------------------")
    print(f"==Nro Iteracion: {i+1} ==")
    print(f"xl = {round(xl,5)}    xu = {round(xu,5)}    xr = {round(xr,5)}")
    
    print(f"f(xl) * f(xr) = {f(xl) * f(xr):.5f}")
    #ver si se cumple la condición, para reasignar los valores de xu o xl
    if f(xl) * f(xr) < 0:
        xu = xr
    else: 
        xl = xr

