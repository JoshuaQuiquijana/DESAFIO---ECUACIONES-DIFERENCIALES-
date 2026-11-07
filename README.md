# Inti Q'uñi — Termotanque solar comunitario

**Estudiante:** Quiquijana Calle Joshua Ivan · **Materia:** Metodos Numericos · **Desafío:** modelar un problema real con una EDO de primer orden (Heun, RK4 y solución analítica)

**Aplicación web:** https://joshuaquiquijana.github.io/DESAFIO---ECUACIONES-DIFERENCIALES-/

Caso hipotético. Los parámetros son supuestos declarados, no mediciones, y los resultados son simulaciones, no predicciones comprobadas.

## 1. Problema y contexto
Un internado rural del altiplano necesita agua tibia para higiene y duchas. Calentarla con GLP cuesta y la garrafa no siempre llega. Un tanque con colectores solares gana calor pero también lo pierde hacia el aire frío.

**Pregunta:** ¿cuántos colectores necesita para que el agua llegue a 40 °C antes de las 12:00 (4 h después de las 08:00)?
**Beneficiarios:** estudiantes y personal del internado.

## 2. Modelo matemático
- Variable dependiente: T(t), temperatura del agua (°C). Variable independiente: t, tiempo (h), con t = 0 a las 08:00.
- Parámetros: Tₐ ambiente (°C), k pérdida de calor (1/h), g aporte de un colector (°C/h), N número de colectores.

```
dT/dt = -k (T - Tₐ) + N g ,     T(0) = T₀
```
Justificación: la pérdida es proporcional a la diferencia con el aire (ley de enfriamiento de Newton) y el aporte solar se supone constante.
Supuestos: agua bien mezclada, Tₐ y radiación constantes (promedios), un solo tanque. Intervalo: 0 ≤ t ≤ 8 h.

Valores base (hipotéticos): T₀ = 6 °C, Tₐ = 10 °C, k = 0,20 1/h, g = 2 °C/h por colector, N = 6, V = 300 L.

## 3. Solución analítica
Con u = T − T∞, donde T∞ = Tₐ + N g / k, la EDO queda u' = −k u, cuya solución es u = u₀ e^(−kt):

```
T(t) = T∞ + (T₀ − T∞) e^(−k t)
```
**Comprobación por sustitución.** T'(t) = −k (T₀ − T∞) e^(−kt). Por otro lado −k(T − Tₐ) + N g = −k (T∞ − Tₐ) − k (T₀ − T∞) e^(−kt) + N g, y como k (T∞ − Tₐ) = N g, queda −k (T₀ − T∞) e^(−kt). Ambos lados coinciden. Además T(0) = T∞ + T₀ − T∞ = T₀.

**Resultados derivados.** Tiempo a la meta T_m: t* = (1/k) ln[(T∞ − T₀)/(T∞ − T_m)] = 3,788 h (11:47) con 6 colectores.
Colectores mínimos para llegar a T_m en t_m: N·g ≥ k[(T_m − Tₐ) − (T₀ − Tₐ) e^(−k t_m)] / (1 − e^(−k t_m)) = 11,55 °C/h, o sea **N = 6** (con 4 colectores llegaría a las 15:24).

## 4. Métodos numéricos
Con f(T) = −k(T − Tₐ) + N g, paso h:
- **Heun (RK2):** k₁ = f(Tᵢ), k₂ = f(Tᵢ + h k₁), Tᵢ₊₁ = Tᵢ + (h/2)(k₁ + k₂).
- **RK4:** k₁ = f(Tᵢ), k₂ = f(Tᵢ + h k₁/2), k₃ = f(Tᵢ + h k₂/2), k₄ = f(Tᵢ + h k₃), Tᵢ₊₁ = Tᵢ + (h/6)(k₁ + 2k₂ + 2k₃ + k₄).

## 5. Resultados (valores base, 0–8 h)
| h (h) | Método | Evaluaciones de f | Error abs. máx (°C) | Error abs. final (°C) | Error rel. máx (%) |
|---|---|---|---|---|---|
| 1 | Heun | 16 | 1,83e-1 | 1,61e-1 | 0,4912 |
| 1 | RK4 | 32 | 3,71e-4 | 3,26e-4 | 9,98e-4 |
| 0,5 | Heun | 32 | 4,23e-2 | 3,72e-2 | 0,1138 |
| 0,5 | RK4 | 64 | 2,13e-5 | 1,87e-5 | 5,74e-5 |

Tabla de los primeros pasos con h = 1 (completa en la app y con `python/verificar.py`):

| t (h) | Analítica | Heun | RK4 | \|e\| Heun | \|e\| RK4 |
|---|---|---|---|---|---|
| 0 | 6,00000 | 6,00000 | 6,00000 | 0 | 0 |
| 1 | 17,60123 | 17,52000 | 17,60107 | 8,12e-2 | 1,65e-4 |
| 2 | 27,09952 | 26,96640 | 27,09925 | 1,33e-1 | 2,70e-4 |
| 4 | 41,24295 | 41,06421 | 41,24258 | 1,79e-1 | 3,63e-4 |
| 8 | 57,07862 | 56,91750 | 57,07830 | 1,61e-1 | 3,26e-4 |

**Orden observado** (error máximo al dividir h a la mitad): Heun ≈ 2,0–2,1 y RK4 ≈ 4,0–4,1, como indica la teoría.

## 6. Interpretación y conclusiones
- Con 6 colectores el agua llega a 40 °C a las 11:47, antes del límite. Con 4 no llega a tiempo. El mínimo es 6.
- RK4 tuvo menor error en todos los ensayos (unas 500 veces menos con h = 1). Ni Heun con h = 0,0625 (256 evaluaciones) iguala el error de RK4 con h = 1 (32 evaluaciones).
- Calentar 300 L de 6 a 40 °C requiere unos 42,7 MJ (11,9 kWh), equivalente a unas 4 garrafas de GLP de 10 kg al mes (70 % de eficiencia).
- Limitaciones: radiación y temperatura ambiente reales varían durante el día; parámetros hipotéticos que habría que medir antes de decidir una compra.

## Cómo ejecutar
- **App:** abrir `index.html` en el navegador (no requiere instalación). Para publicarla: GitHub → Settings → Pages → rama `main`, carpeta `/ (root)`.
- **Verificación independiente:** `python3 python/verificar.py`
- `src/app.html` es la fuente; `python3 build.py` regenera `index.html`.

## Estructura
```
index.html           app web completa
src/app.html         fuente de la app
python/verificar.py  verificación en Python puro
build.py             genera index.html
docs/guion_video.md  guion del video de 1 minuto
```
