# ia-db — Lab-E2E.WebBlazor.Base

> **Instrucción para IA**: este archivo es el **punto de entrada único** a la base de conocimiento
> del repositorio `Lab-E2E.WebBlazor.Base`. Leelo entero —es una pantalla— y después cargá **solo**
> el o los índices que la tabla de navegación indique. No recorras el repositorio completo mientras
> esta base responda la pregunta; ampliá a las fuentes citadas únicamente ante insuficiencia
> comprobada.

> **Advertencia de estado**: este repositorio es un **punto de partida en construcción**, no una
> solución terminada. Varias piezas están incompletas o copiadas sin adaptar; están todas
> registradas en [05_Estado-Y-Divergencias.md](indexes/05_Estado-Y-Divergencias.md). Leé ese índice
> antes de afirmar que algo «funciona» o de proponer un cambio.

## Necesitás saber… → leé este índice

| Necesitás saber… | Leé |
| --- | --- |
| Qué es el repositorio, con qué stack y cómo se relaciona con el laboratorio grande | [00_MASTER-INDEX.md](indexes/00_MASTER-INDEX.md) |
| Qué hacen las dos aplicaciones y qué pantallas tienen | [01_Aplicaciones.md](indexes/01_Aplicaciones.md) |
| Cómo está resuelto el login por cookies y por qué así | [02_Autenticacion.md](indexes/02_Autenticacion.md) |
| Qué prueban los proyectos E2E y cómo se corren | [03_Pruebas.md](indexes/03_Pruebas.md) |
| Qué hace el workflow de GitHub Actions | [04_CI-Y-Workflow.md](indexes/04_CI-Y-Workflow.md) |
| Qué está incompleto, qué está copiado sin adaptar y qué no funcionaría tal como está | [05_Estado-Y-Divergencias.md](indexes/05_Estado-Y-Divergencias.md) |

## Resumen ejecutivo

| Dato | Valor |
| --- | --- |
| Proyecto | `Lab-E2E.WebBlazor.Base` (`LAB/Lab-E2E.WebBlazor.Base`) |
| Tipo | Andamiaje didáctico: dos aplicaciones Blazor mínimas con su prueba E2E de ejemplo |
| Stack | .NET 10 · Blazor Web App *interactive server* · `Microsoft.Playwright.NUnit` 1.52 · NUnit 4 · Bootstrap (plantilla estándar) |
| Repositorio | `https://github.com/hdcm-dev/Lab-E2E.WebBlazor.Base` · rama `main` |
| Solución | `Ejemplos.WebBlazor.E2E.Base.slnx` — formato `.slnx`, cuatro proyectos |
| Persistencia | Ninguna: no hay base de datos ni EF Core |

**Función principal** — mostrar el andamiaje mínimo de una prueba E2E con Playwright sobre Blazor:
cómo se crea el proyecto NUnit, cómo se marcan los elementos con `data-testid` y cómo se los ubica
desde la prueba. Es el escalón previo a `Lab-E2E.WebBlazor`, donde el mismo enfoque se lleva a una
aplicación con servidor, base de datos y pipeline completo.

**Arquitectura en una línea** — dos aplicaciones Blazor de plantilla, sin capas ni dominio propio
(`HolaMundo` sin autenticación y `Login` con autenticación por cookies), y un proyecto de pruebas
E2E por cada una.

## Estructura

```
Lab-E2E.WebBlazor.Base/
├── Ejemplos.WebBlazor.E2E.Base.slnx
├── src/
│   ├── WebBlazor.E2E.Base.HolaMundo/   Blazor de plantilla + la página HolaMundo
│   └── WebBlazor.E2E.Base.Login/       Lo mismo + login/logout por cookies y [Authorize]
├── tests/
│   ├── WebBlazor.E2E.Base.HolaMundo.E2ETests/   1 caso, funcional
│   └── WebBlazor.E2E.Base.Login.E2ETests/       1 caso, con el cuerpo vacío
├── Guides/
│   ├── E2E-Guides.md          Guía de estudio (453 líneas) + Imagenes/
│   └── GitHub-Action.md       Vacío
└── .github/workflows/e2e.yml  Copiado del laboratorio grande, sin adaptar del todo
```

## Restricciones para IA

- **No presentar este repositorio como terminado.** Su valor es didáctico y su estado, parcial. Todo
  lo comprobado está en [05_Estado-Y-Divergencias.md](indexes/05_Estado-Y-Divergencias.md).
- **No confundirlo con `Lab-E2E.WebBlazor`**, que es un repositorio distinto y mucho más maduro, con
  su propia ia-db en [`../Root/`](../Root/README.md). Comparten técnica y difieren en alcance.
- **No suponer que las pruebas pasan**: no se ejecutaron durante este indexado, y hay divergencias
  verificadas entre lo que la prueba espera y lo que la aplicación expone.
- **No inventar**: toda afirmación de estos índices apunta a un archivo del repositorio.
- Si una tarea cambia el código, **actualizar esta base de forma incremental** con
  `Actualizar-Indexado.md`, no reconstruirla.

## Manifiesto de generación

- Generado por : `/IA/PROMPTs/IA.Prompts/Tool-Prompts/Indexado-Documentado/Iniciar-Indexado.md`
  (invocado desde `/LAB/Lab-E2E.WebBlazor.Documentacion/PROMPTs/Indexado/Crear-Indexado.md`)
- Alcance      : `/LAB/Lab-E2E.WebBlazor.Base` — modo proyecto
- Fuentes      : `README.md`, `Ejemplos.WebBlazor.E2E.Base.slnx`, `src/`, `tests/`, `Guides/`,
  `.github/workflows/e2e.yml`
- Exclusiones  : `.git`, `bin/`, `obj/`, `wwwroot/lib/` (Bootstrap de plantilla), imágenes de
  `Guides/Imagenes/` (solo se referencian), y lo ignorado por `.gitignore`
- Estado del repositorio : rama `main`, último commit `f4ee8df` («login fix», 2026-09-01)
- Generado     : 2026-09-01 · Versión: 1.0
- Actualizar   : `/IA/PROMPTs/IA.Prompts/Tool-Prompts/Indexado-Documentado/Actualizar-Indexado.md`
