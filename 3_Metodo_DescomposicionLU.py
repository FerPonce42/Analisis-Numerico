# Descomposición LU con sympy ======================================================================================== Descomposición LU
from sympy import *

# === MODIFICAR A y B ===
A = Matrix([[1, 1,  1],
            [1, 2,  1],
            [-1, 2, 0]])

B = Matrix([50, 70,25])
# =======================

# 1. Verificar solución única, determinante diferente de cero.
d = A.det()
print("det(A) =", d)
if d == 0:
    print("→ det(A) = 0: A no es invertible, no hay solución única")
else:
    print("→ det(A) ≠ 0: OK, tiene solución única")

    # 2. Descomponer A = L * U
    L, U, _ = A.LUdecomposition()
    print("\nL ="); pprint(L)
    print("\nU ="); pprint(U)

    # 3. Resolver L*Y = B
    Y = L.solve(B)
    print("\nY ="); pprint(Y)

    # 4. Resolver U*X = Y
    X = U.solve(Y)
    print("\nX ="); pprint(X)

    # 5. Verificar A*X = B
    print("\nVerificación:")
    print("A*X =", A * X)
    print("B   =", B)
    print("¿Correcto?", A * X == B)