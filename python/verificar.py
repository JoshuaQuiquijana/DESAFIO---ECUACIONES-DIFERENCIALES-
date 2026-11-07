"""Inti Q'uñi - verificación independiente (Python puro, sin dependencias).

EDO:  dT/dt = -k (T - Ta) + N*g ,  T(0) = T0
Exacta: T(t) = Tinf + (T0 - Tinf) e^{-k t},  Tinf = Ta + N g / k
"""
import math

# Parámetros HIPOTÉTICOS (caso base)
P = dict(T0=6.0, Ta=10.0, k=0.20, g=2.0, N=6, Tm=40.0, tm=4.0, tmax=8.0, V=300.0)

def Tinf(p): return p["Ta"] + p["N"] * p["g"] / p["k"]
def exacta(t, p): return Tinf(p) + (p["T0"] - Tinf(p)) * math.exp(-p["k"] * t)
def f(T, p): return -p["k"] * (T - p["Ta"]) + p["N"] * p["g"]

def heun(p, n):
    h = p["tmax"] / n; T = p["T0"]; out = [T]
    for _ in range(n):
        k1 = f(T, p); k2 = f(T + h * k1, p)
        T += h / 2 * (k1 + k2); out.append(T)
    return out

def rk4(p, n):
    h = p["tmax"] / n; T = p["T0"]; out = [T]
    for _ in range(n):
        k1 = f(T, p); k2 = f(T + h / 2 * k1, p)
        k3 = f(T + h / 2 * k2, p); k4 = f(T + h * k3, p)
        T += h / 6 * (k1 + 2 * k2 + 2 * k3 + k4); out.append(T)
    return out

def errores(p, n):
    h = p["tmax"] / n
    H, R = heun(p, n), rk4(p, n)
    filas = []
    for j in range(n + 1):
        t = j * h; ex = exacta(t, p)
        eH, eR = abs(ex - H[j]), abs(ex - R[j])
        filas.append((t, ex, H[j], R[j], eH, eR,
                      eH / abs(ex) * 100 if ex else None,
                      eR / abs(ex) * 100 if ex else None))
    return filas

if __name__ == "__main__":
    p = P
    ti = Tinf(p)
    print(f"T_inf = {ti:.4f} C")
    tstar = math.log((ti - p['T0']) / (ti - p['Tm'])) / p["k"]
    print(f"t* (T={p['Tm']} C) = {tstar:.4f} h")
    g_min = p["k"] * ((p["Tm"] - p["Ta"]) - (p["T0"] - p["Ta"]) * math.exp(-p["k"] * p["tm"])) / (1 - math.exp(-p["k"] * p["tm"]))
    print(f"g_total minimo = {g_min:.4f} C/h  -> N_min = {math.ceil(g_min / p['g'])}")
    # comprobación por sustitución en t = 3
    t = 3.0; d = (p["T0"] - ti) * (-p["k"]) * math.exp(-p["k"] * t)
    print("residuo EDO en t=3:", abs(d - f(exacta(t, p), p)), " | T(0)-T0:", exacta(0, p) - p["T0"])
    for n in (8, 16):
        print(f"\n--- h = {p['tmax']/n} h  (n={n}) ---")
        print("   t        exacta     Heun      RK4     |e|Heun    |e|RK4   %Heun    %RK4")
        for r in errores(p, n):
            print(f"{r[0]:5.2f} {r[1]:10.5f} {r[2]:9.5f} {r[3]:9.5f} {r[4]:10.2e} {r[5]:10.2e} {r[6]:7.4f} {r[7]:8.5f}")
    print("\n--- convergencia (error máximo) ---")
    prev = None
    for n in (8, 16, 32, 64, 128):
        F = errores(p, n); mH = max(r[4] for r in F); mR = max(r[5] for r in F)
        if prev:
            print(f"h={p['tmax']/n:7.4f}  Heun={mH:.3e} (p={math.log2(prev[0]/mH):.2f})  RK4={mR:.3e} (p={math.log2(prev[1]/mR):.2f})")
        else:
            print(f"h={p['tmax']/n:7.4f}  Heun={mH:.3e}  RK4={mR:.3e}")
        prev = (mH, mR)
    E = p["V"] * 4.186 * (p["Tm"] - p["T0"]) / 1000
    print(f"\nEnergía a Tm: {E:.2f} MJ = {E/3.6:.2f} kWh ; garrafas/mes = {30*E/(10*46.1*0.7):.2f}")
