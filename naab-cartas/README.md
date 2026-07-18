# NAAB — Sistema de Cartas

Contenido y generador de las cartas de nacimiento personalizadas de NAAB.

## Estructura

- `data/naab_bloques.json` — Base de datos maestra (v1.1): 80 bloques de texto + 12 frases de transición + mapeos automáticos (signo → elemento → arquetipo → cuarzo, fechas de signos). Es el archivo que consumirá la página web para armar cada carta.
- `docs/NAAB_Sistema_Bloques.md` — Versión legible del sistema completo, con reglas y tabla de correspondencias. Para revisar y editar contenido.
- `generador/` — Scripts Python (ReportLab) que generan la carta en PDF con la identidad de marca (paleta, Cormorant, torus). Incluye las fuentes.
- `muestras/` — Cartas de ejemplo: Ruta A (cuarzo de nacimiento, 3 páginas) y Ruta B (cuarzo elegido distinto, 4 páginas con doble sección de piedra).

## Lógica de la carta

1. La persona compra un dije con código único y lo registra en la web con su nombre y fecha de nacimiento.
2. El sistema calcula: número de vida (numerología, respetando 11/22/33), signo solar, elemento (según esencia masculina/femenina) y arquetipo.
3. Compara el cuarzo del dije con el que corresponde al signo:
   - Si coinciden → carta con una sección de cuarzo (correspondencia).
   - Si difieren → carta con dos secciones: la piedra de nacimiento + la piedra elegida, unidas por la frase de transición `{raiz}`.
