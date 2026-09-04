# ia-db — Lab-E2E.WebBlazor.Base

> **Instrucción para IA**: este archivo es el **punto de entrada único** a la base de conocimiento
> del repositorio `Lab-E2E.WebBlazor.Base`. Leelo entero —es una pantalla— y después cargá **solo**
> el o los índices que la tabla de navegación indique. No recorras el repositorio completo mientras
> esta base responda la pregunta; ampliá a las fuentes citadas únicamente ante insuficiencia
> comprobada.

> **Advertencia de estado**: este repositorio es un **punto de partida en construcción**, no una
> solución terminada. Avanzó bastante desde el indexado inicial —template propio, acceso por
> endpoints, evidencia versionada—, pero sigue habiendo piezas rotas: entre ellas, el proyecto de
> pruebas del login **no compila**. Todo está registrado en
> [05_Estado-Y-Divergencias.md](indexes/05_Estado-Y-Divergencias.md). Leé ese índice antes de afirmar
> que algo «funciona» o de proponer un cambio.

## Necesitás saber… → leé este índice

| Necesitás saber… | Leé |
| --- | --- |
| Qué es el repositorio, con qué stack y cómo se relaciona con el laboratorio grande | [00_MASTER-INDEX.md](indexes/00_MASTER-INDEX.md) |
| Qué hacen las dos aplicaciones, qué superficies tienen y con qué `data-testid` se las ubica | [01_Aplicaciones.md](indexes/01_Aplicaciones.md) |
| Cómo está resuelto el acceso por cookies, quién decide y cómo es el guard | [02_Autenticacion.md](indexes/02_Autenticacion.md) |
| Qué prueban los proyectos E2E, cómo se corren y qué cubre el guion de evidencia | [03_Pruebas.md](indexes/03_Pruebas.md) |
| Qué hace el workflow de GitHub Actions y qué riesgo abre el disparador nuevo | [04_CI-Y-Workflow.md](indexes/04_CI-Y-Workflow.md) |
| Qué está incompleto, qué está copiado sin adaptar y qué no funcionaría tal como está | [05_Estado-Y-Divergencias.md](indexes/05_Estado-Y-Divergencias.md) |
| Con qué forma constructiva se escriben las superficies: tokens, componentes, shells | [06_Template-Y-Superficies.md](indexes/06_Template-Y-Superficies.md) |

## Resumen ejecutivo

| Dato | Valor |
| --- | --- |
| Proyecto | `Lab-E2E.WebBlazor.Base` (`LAB/Lab-E2E.WebBlazor.Base`) |
| Tipo | Andamiaje didáctico: dos aplicaciones Blazor mínimas con su prueba E2E de ejemplo |
| Stack | .NET 10 · Blazor Web App *interactive server* · estilos propios (tokens del catálogo SDD) · `Microsoft.Playwright.NUnit` 1.52 · NUnit 4 |
| Repositorio | `https://github.com/hdcm-dev/Lab-E2E.WebBlazor.Base` · rama `main` · público |
| Solución | `Ejemplos.WebBlazor.E2E.Base.slnx` — formato `.slnx`, cuatro proyectos |
| Persistencia | Ninguna: no hay base de datos ni EF Core |
| Versión | Sin versionar; desde el 2026-09-03 tiene `CHANGELOG.md`, que arranca en esa fecha; para lo anterior la referencia temporal son los commits |

**Función principal** — mostrar el andamiaje mínimo de una prueba E2E con Playwright sobre Blazor:
cómo se crea el proyecto NUnit, cómo se marcan los elementos con `data-testid` y cómo se los ubica
desde la prueba. Es el escalón previo a `Lab-E2E.WebBlazor`, donde el mismo enfoque se lleva a una
aplicación con servidor, base de datos y pipeline completo.

**Arquitectura en una línea** — dos aplicaciones Blazor sin capas ni dominio propio (`HolaMundo` sin
autenticación y `Login` con acceso por cookies emitidas desde endpoints POST), construidas con el
template por defecto del Framework SDD, y un proyecto de pruebas E2E por cada una.

## Estructura

```
Lab-E2E.WebBlazor.Base/
├── Ejemplos.WebBlazor.E2E.Base.slnx
├── src/
│   ├── WebBlazor.E2E.Base.HolaMundo/   La superficie HolaMundo con sus cuatro estados
│   └── WebBlazor.E2E.Base.Login/       Lo mismo detrás del acceso, + Endpoints/ y Servicios/
├── tests/
│   ├── WebBlazor.E2E.Base.HolaMundo.E2ETests/   1 caso, el único que compila
│   └── WebBlazor.E2E.Base.Login.E2ETests/       No compila: dos métodos Setup en la misma clase
├── evidencia/2026-09-01-aplicacion-template/    verificar.mjs, su log y doce capturas
├── Guides/
│   ├── E2E-Guides.md              Guía de estudio (453 líneas) + Imagenes/
│   ├── Template-SDD-Aplicado.md   Qué se aplicó del template y cómo se verificó
│   ├── GitHub-Action.md           Vacío
│   └── Notas.GitHub.md            Sin versionar: runner propio y forks
└── .github/workflows/e2e.yml      Copiado del laboratorio grande, con una divergencia en pie
```

## Restricciones para IA

- **No presentar este repositorio como terminado.** Su valor es didáctico y su estado, parcial. Todo
  lo comprobado está en [05_Estado-Y-Divergencias.md](indexes/05_Estado-Y-Divergencias.md).
- **No confundirlo con `Lab-E2E.WebBlazor`**, que es un repositorio distinto y mucho más maduro, con
  su propia ia-db en [`../Root/`](../Root/README.md). Comparten técnica y difieren en alcance.
- **No suponer que las pruebas pasan**: no se ejecutaron durante este indexado —esta máquina no tiene
  SDK de .NET—, y hay divergencias verificadas por lectura entre lo que la prueba espera y lo que la
  aplicación expone.
- **No reintroducir Bootstrap ni una segunda fuente de valores visuales**: se retiraron a propósito.
  La forma constructiva vigente está en
  [06_Template-Y-Superficies.md](indexes/06_Template-Y-Superficies.md).
- **No inventar**: toda afirmación de estos índices apunta a un archivo del repositorio.
- Si una tarea cambia el código, **actualizar esta base de forma incremental** con
  `Actualizar-Indexado.md`, no reconstruirla.

## Manifiesto de generación

- Generado por : `/IA/PROMPTs/IA.Prompts/Tool-Prompts/Indexado-Documentado/Iniciar-Indexado.md`
  (invocado desde `/LAB/Lab-E2E.WebBlazor.Documentacion/PROMPTs/Indexado/Crear-Indexado.md`)
- Alcance      : `/LAB/Lab-E2E.WebBlazor.Base` — modo proyecto
- Fuentes      : `README.md`, `Ejemplos.WebBlazor.E2E.Base.slnx`, `.gitignore`, `src/`, `tests/`,
  `Guides/`, `evidencia/`, `.github/workflows/e2e.yml`
- Exclusiones  : `.git`, `bin/`, `obj/`, imágenes de `Guides/Imagenes/` y capturas de `evidencia/`
  (solo se referencian), y lo ignorado por `.gitignore`
- Estado del repositorio : rama `main`, último commit `6af2049` («.», 2026-09-02); `Guides/Notas.GitHub.md`
  sin versionar
- Generado     : 2026-09-01 · Versión: 1.0
- Actualizado  : 2026-09-02 · Versión: 1.1 — se rehicieron los índices 00 a 05 por la aplicación del
  template SDD (commits `d32b4ab`…`6af2049`) y se sumó el índice 06
- Actualizar   : `/IA/PROMPTs/IA.Prompts/Tool-Prompts/Indexado-Documentado/Actualizar-Indexado.md`
