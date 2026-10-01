# Filas de índice para `Index-Knowledge.md`

Pegar en la §3 del `Index-Knowledge.md` de la base del fork, respetando el orden alfabético que esa base
use. Los ocho campos comunes coinciden campo por campo con la cabecera de cada documento, como exige
`Rules-Base-Conocimiento.md` §6.1.

| Documento | Alias | Naturaleza | Tema | Consumidor | Condicion-de-carga | Hereda-de | Sustituye | Compatible-con | Estado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `Knowledge-Template-HTML-SDD-Default.md` | `Template-HTML-SDD-Default` | propio | Forma constructiva de una maqueta HTML/CSS/JS sin proceso de build: layout de archivos, tokens, conmutador declarativo de estados, y los cuatro tipos de diálogo (ABM clásico, asistente de varios niveles, ventana modal y presentación de datos) | 03, AG-00031 | proyectos de código con `requiere_maqueta == true` que construyan la maqueta con HTML, CSS y JavaScript planos | — | — | 2.2 | Vigente |
| `Knowledge-Template-Blazor-Interactive-Server-SDD-Default.md` | `Template-Blazor-Interactive-Server-SDD-Default` | propio | Realización del template HTML de maqueta como proyecto .NET Blazor Web App con render mode Interactive Server y sin librería de componentes: estructura, componentes propios por patrón, formularios, diálogos, asistentes y superficies de identidad fuera del circuito | 03, 05 | proyectos de código `web-monolith` sobre stack .NET con interfaz Blazor Web App en render mode Interactive Server, sin librería de componentes de terceros | `Template-HTML-SDD-Default` | — | 2.2 | Vigente |

## Nota sobre `Sustituye`

Los dos documentos llevan `Sustituye: —`, y no por omisión.

- El de HTML **no sustituye nada**: describe el stack que `Maqueta-Rules.md` §4.1 ya elige.
- El de Blazor **contradice** el criterio de aceptación de `Design-Rules-Blazor-Mudblazor.md` §10, pero
  ese archivo no rotula ninguna de sus reglas como decisión de stack. Por `Rules-Base-Conocimiento.md`
  §0.4 eso no habilita sustitución: es conflicto, y ante conflicto manda la regla de la categoría salvo
  que el documento declare la desviación con su justificación. Está declarada en su §8.1.
