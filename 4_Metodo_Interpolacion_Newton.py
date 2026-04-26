import numpy as np
import matplotlib.pyplot as plt
from fractions import Fraction

# =============================================
#   Puntos a probar
puntos = [(0, -4), (1, -4), (2, 10), (3, 56)]
# =============================================

def ordinal(n):
    nombres = ["Primero","Segundo","Tercero","Cuarto","Quinto",
               "Sexto","Séptimo","Octavo","Noveno","Décimo"]
    return nombres[n] if n < len(nombres) else f"Punto {n+1}"

def fmt(val):
    try:
        f = Fraction(val).limit_denominator(1000)
        if f.denominator == 1:
            return str(f.numerator)
        return f"{f.numerator}/{f.denominator}"
    except:
        return str(round(val, 6))

def factor_str(xs, hasta):
    return "".join([f"(x - {fmt(xs[j])})" if xs[j] != 0 else "(x)" for j in range(hasta)])

def fmt_coef(coef, grado, primero=False):
    f = Fraction(coef).limit_denominator(1000)
    num, den = f.numerator, f.denominator
    negativo = num < 0
    abs_num = abs(num)
    val_str = str(abs_num) if den == 1 else f"{abs_num}/{den}"
    if grado == 0:
        termino = val_str
    elif grado == 1:
        termino = f"{val_str}x" if abs_num != 1 else "x"
    else:
        termino = f"{val_str}x^{grado}" if abs_num != 1 else f"x^{grado}"
    if primero:
        return f"-{termino}" if negativo else termino
    else:
        return f" - {termino}" if negativo else f" + {termino}"

def newton_termino(k, xs, i):
    f = Fraction(k).limit_denominator(1000)
    negativo = f.numerator < 0
    abs_f = Fraction(abs(f.numerator), f.denominator)
    k_str = str(abs_f.numerator) if abs_f.denominator == 1 else f"{abs_f.numerator}/{abs_f.denominator}"
    factores = factor_str(xs, i+1)
    return (negativo, f"{k_str} · {factores}")

def newton_interpolacion(puntos):
    xs = [p[0] for p in puntos]
    ys = [p[1] for p in puntos]

    if len(set(xs)) != len(xs):
        raise ValueError("Error: hay valores de x repetidos. Todos deben ser distintos.")

    n = len(puntos)
    polinomio = np.array([float(ys[0])])
    ks = []

    print("=" * 50)
    print("  Interpolación — Método de Newton")
    print("=" * 50)
    print()

    print(f"● {ordinal(0)}: ({fmt(xs[0])}, {fmt(ys[0])})")
    print(f"   P0(x) = {fmt(ys[0])}")
    print()

    for i in range(1, n):
        coords = " ".join([f"({fmt(xs[j])}, {fmt(ys[j])})" for j in range(i+1)])
        print(f"● {ordinal(i)}: {coords}")
        print(f"   P{i}(x) = P{i-1}(x) + k{i} · {factor_str(xs, i)}")

        p_en_xi = np.polyval(polinomio[::-1], xs[i])
        factor_eval = 1.0
        factor_parts = []
        for j in range(i):
            factor_eval *= xs[i] - xs[j]
            factor_parts.append(f"{fmt(xs[i])}" if xs[j] == 0 else f"({fmt(xs[i])} - {fmt(xs[j])})")

        print(f"   P{i}({fmt(xs[i])}) = {fmt(p_en_xi)} + k{i} · {' · '.join(factor_parts)} = {fmt(ys[i])}")
        print(f"          {fmt(p_en_xi)} + {fmt(factor_eval)}·k{i} = {fmt(ys[i])}")

        k = (ys[i] - p_en_xi) / factor_eval
        ks.append(k)

        print(f"          {fmt(factor_eval)}·k{i} = {fmt(ys[i] - p_en_xi)}")
        print(f"          k{i} = {fmt(k)}")
        print()

        factor_poly = np.array([1.0])
        for j in range(i):
            factor_poly = np.polymul(factor_poly, [1, -xs[j]])
        factor_poly = factor_poly[::-1] * k
        if len(factor_poly) > len(polinomio):
            polinomio = np.append(polinomio, [0.0] * (len(factor_poly) - len(polinomio)))
        polinomio[:len(factor_poly)] += factor_poly

        # Pi sin expandir con signos limpios
        partes = [fmt(ys[0])]
        for m in range(len(ks)):
            if abs(ks[m]) < 1e-10:
                continue
            neg, txt = newton_termino(ks[m], xs, m)
            partes.append(("- " if neg else "+ ") + txt)
        print(f"   P{i}(x) = " + " ".join(partes))
        print()

    # Coeficientes
    print("=" * 50)
    print("Coeficientes K:")
    print(f"  K0 = {fmt(ys[0])}")
    for i, k in enumerate(ks):
        print(f"  K{i+1} = {fmt(k)}")
    print()

    # Forma Newton sin expandir
    print("=" * 50)
    print("P(x) en forma de Newton (sin expandir):")
    partes = [fmt(ys[0])]
    for i, k in enumerate(ks):
        if abs(k) < 1e-10:
            continue
        neg, txt = newton_termino(k, xs, i)
        partes.append(("- " if neg else "+ ") + txt)
    print("P(x) = " + " ".join(partes))
    print()

    # Expandido
    print("=" * 50)
    print("p(x) expandido:")
    resultado = ""
    primero = True
    for grado, coef in list(enumerate(polinomio))[::-1]:
        if abs(coef) < 1e-10:
            continue
        resultado += fmt_coef(coef, grado, primero)
        primero = False
    print(f"p(x) = {resultado}")
    print()

    # Verificacion
    print("=" * 50)
    print("Verificación:")
    for p in puntos:
        r = round(np.polyval(polinomio[::-1], p[0]), 6)
        print(f"   p({fmt(p[0])}) = {r}  (esperado: {fmt(p[1])})")

    # Grafica
    margen = (max(xs) - min(xs)) * 0.8
    x_plot = np.linspace(min(xs) - margen, max(xs) + margen, 500)
    y_plot = np.polyval(polinomio[::-1], x_plot)
    y_min = min(min(y_plot), min(ys))
    y_max = max(max(y_plot), max(ys))
    padding = (y_max - y_min) * 0.1

    print()
    print("=" * 50)
    print("  Gráfico")
    print("=" * 50)
    print()
    plt.figure(figsize=(8, 5))
    plt.plot(x_plot, y_plot, color='royalblue', linewidth=2, label='P(x)')
    plt.scatter(xs, ys, color='crimson', zorder=5, s=80, label='Puntos dados')
    for x, y in zip(xs, ys):
        plt.annotate(f"({fmt(x)}, {fmt(y)})", (x, y),
                     textcoords="offset points", xytext=(8, 6), fontsize=10)
    plt.axhline(0, color='gray', linewidth=0.8)
    plt.axvline(0, color='gray', linewidth=0.8)
    plt.ylim(y_min - padding, y_max + padding)
    plt.title("Interpolación — Método de Newton", fontsize=13)
    plt.xlabel("x")
    plt.ylabel("P(x)")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

newton_interpolacion(puntos)