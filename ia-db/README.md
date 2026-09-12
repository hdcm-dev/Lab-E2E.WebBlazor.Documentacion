# ia-db — Lab-E2E.WebBlazor

> **Instrucción para IA**: este archivo es el **punto de entrada único** a la base de conocimiento
> del repositorio `Lab-E2E.WebBlazor`. Leelo entero —es una pantalla— y después cargá **solo** el o
> los índices que la tabla de navegación indique para tu tarea. No recorras el repositorio completo
> ni cargues toda la documentación mientras esta base responda la pregunta; ampliá a las fuentes
> citadas únicamente ante insuficiencia comprobada.

## Necesitás saber… → leé este índice

| Necesitás saber… | Leé |
| --- | --- |
| De qué trata el laboratorio, cuáles son sus tres aplicaciones y qué decisiones lo definen | [00_MASTER-INDEX.md](indexes/00_MASTER-INDEX.md) |
| Cómo se reparten las capas de Movilidad Urbana, qué depende de qué y dónde se compone todo | [01_Arquitectura.md](indexes/01_Arquitectura.md) |
| Qué entidades y reglas de negocio existen, y qué valida cada una | [02_Dominio-Y-Reglas.md](indexes/02_Dominio-Y-Reglas.md) |
| Cómo se aísla el estado por sesión y cómo se persiste en SQLite | [03_Sesiones-Y-Persistencia.md](indexes/03_Sesiones-Y-Persistencia.md) |
| Qué pantallas tiene Movilidad Urbana, qué hace cada una y con qué `data-testid` se la ubica | [04_Interfaz-Y-Pantallas.md](indexes/04_Interfaz-Y-Pantallas.md) |
| Cómo se corren las pruebas de las tres aplicaciones, qué cubre cada suite y qué variables las gobiernan | [05_Pruebas.md](indexes/05_Pruebas.md) |
| Qué hace cada workflow —uno por aplicación—, cuándo se dispara y qué se observó corriendo | [06_CI-Y-Workflows.md](indexes/06_CI-Y-Workflows.md) |
| Dónde están las guías de estudio y cuál responde qué pregunta | [07_Guias.md](indexes/07_Guias.md) |
| Por qué el proyecto está hecho así y qué trampas ya se pagaron | [08_Decisiones-Y-Trampas.md](indexes/08_Decisiones-Y-Trampas.md) |
| Qué significa un término del proyecto | [09_Glosario.md](indexes/09_Glosario.md) |
| Qué hacen Hola Mundo y Login, cómo es el acceso por cookies y cómo se prueban sin fixture | [10_Hola-Mundo-Y-Login.md](indexes/10_Hola-Mundo-Y-Login.md) |
| Con qué forma constructiva se escriben las superficies de las tres aplicaciones | [11_Template-Y-Superficies.md](indexes/11_Template-Y-Superficies.md) |
| Qué expone la API REST de Movilidad Urbana, cómo identifica la sesión y cómo se prueba | [12_Api-REST.md](indexes/12_Api-REST.md) |

## Resumen ejecutivo

| Dato | Valor |
| --- | --- |
| Proyecto | `Lab-E2E.WebBlazor` (`LAB/Lab-E2E.WebBlazor`) |
| Tipo | Laboratorio didáctico: tres aplicaciones web de complejidad creciente, sus pruebas E2E y su pipeline |
| Stack | .NET 10 · Blazor Web App *interactive server* y ASP.NET Core Web API con controllers · EF Core 10 sobre SQLite (Movilidad Urbana) · Playwright 1.62 + NUnit 4 · `WebApplicationFactory` para la API · template del Framework SDD, sin librería de componentes |
| Repositorio | `https://github.com/hdcm-dev/Lab-E2E.WebBlazor` · rama `main` |
| Versión | Sin versionar: el `CHANGELOG.md` agrupa por fecha, no por número (última entrada: 2026-09-12) |
| Documentación asociada | `Lab-E2E.WebBlazor.Documentacion` (este repositorio), donde viven también las guías |

**Función principal** — enseñar a escribir, estabilizar y automatizar pruebas de extremo a extremo
con Playwright sobre Blazor, y a atarlas a las puertas de un pipeline de GitHub Actions. Las tres
aplicaciones escalonan la dificultad: una superficie sola, la misma detrás de un acceso, y un caso de
negocio de juguete —*movilidad urbana*: un ABM y una encuesta en tres pasos— con servidor y base.

**Arquitectura en una línea** — tres aplicaciones web —Hola Mundo y Login sin capas, Movilidad
Urbana con Clean Architecture en **proyectos por capa** y dos cabezas, la web Blazor y una API
REST—, cada web con su proyecto E2E y su workflow, más las pruebas unitarias y las de la API de
Movilidad Urbana.

## Estructura

```
Lab-E2E.WebBlazor/
├── Lab-E2E.WebBlazor.sln         Doce proyectos + carpetas de solución (src, tests, github-workflow, scripts, Solution Items)
├── src/
│   ├── MovilidadUrbana.Dominio/      Entidades, reglas y catálogos
│   ├── MovilidadUrbana.Aplicacion/   Casos de uso y abstracciones
│   ├── MovilidadUrbana.Infraestructura/  EF Core sobre SQLite y la sesión por cookie
│   ├── MovilidadUrbana.Web/          Presentación Blazor
│   ├── MovilidadUrbana.ApiWeb/       Presentación REST: dos controllers sobre las mismas capas
│   ├── WebBlazor.HolaMundo/ La superficie más simple
│   └── WebBlazor.Login/     La misma superficie detrás de un acceso
├── tests/
│   ├── MovilidadUrbana.E2ETests/                22 casos + fixture que levanta la aplicación
│   ├── MovilidadUrbana.UnitTests/               49 casos sobre las reglas de dominio
│   ├── MovilidadUrbana.ApiWeb.Tests/            13 casos sobre la API, en proceso
│   ├── WebBlazor.HolaMundo.E2ETests/   1 caso, sin fixture
│   └── WebBlazor.Login.E2ETests/       10 casos, sin fixture
├── scripts/                      dotnet.sh, publicar.sh, pruebas.sh (todo por contenedor)
├── .github/workflows/            ci.yml, e2e.yml, e2e-holamundo.yml, e2e-login.yml, verificacion-entorno.yml
├── evidencia/                    Registros de corridas que respaldan lo que afirman las guías (tres carpetas)
├── pruebas.runsettings           Navegador, timeouts y workers de las E2E
├── README.md                     Documento de referencia del repositorio (extenso)
└── CHANGELOG.md                  Registro por fecha
```

## Restricciones para IA

- **No inventar**: toda afirmación de estos índices apunta a un archivo del repositorio. Si algo no
  figura acá, verificalo en la fuente antes de afirmarlo.
- **No uniformar las tres aplicaciones**: que Hola Mundo y Login no tengan fixture, que prueben contra
  una URL fija y que cada una tenga un workflow distinto es **deliberado** — ver
  [10](indexes/10_Hola-Mundo-Y-Login.md) y [06](indexes/06_CI-Y-Workflows.md).
- **No proponer cambios de estructura** por «prolijidad»: las decisiones no obvias —publicar en el
  fixture, `ParallelScope.Fixtures`, la cookie de sesión, `EnsureCreated`— están justificadas en
  [08_Decisiones-Y-Trampas.md](indexes/08_Decisiones-Y-Trampas.md).
- **No dar por verificado lo que no lo está**: la ejecución desde el Explorador de pruebas de Visual
  Studio nunca se probó desde esta máquina. Los workflows, en cambio, sí se observaron corriendo — ver
  [06](indexes/06_CI-Y-Workflows.md).
- **`Lab-E2E.WebBlazor.Base` ya no existe como repositorio aparte**: se unificó en este el
  2026-09-12. Su conocimiento vigente está en [10](indexes/10_Hola-Mundo-Y-Login.md) y
  [11](indexes/11_Template-Y-Superficies.md); no hay una ia-db separada que consultar.
- **No modificar el repositorio indexado desde esta base**: la ia-db vive en
  `Lab-E2E.WebBlazor.Documentacion`, no en `Lab-E2E.WebBlazor`.
- Si una tarea cambia el código o la documentación, **actualizar esta base de forma incremental** con
  `Actualizar-Indexado.md`, no reconstruirla.

## Manifiesto de generación

- Generado por : `/IA/PROMPTs/IA.Prompts/Tool-Prompts/Indexado-Documentado/Iniciar-Indexado.md`
  (invocado desde `/LAB/Lab-E2E.WebBlazor.Documentacion/PROMPTs/Indexado/Crear-Indexado.md`)
- Alcance      : `/LAB/Lab-E2E.WebBlazor` — modo proyecto, un solo repositorio (doce proyectos:
  tres capas y dos cabezas de Movilidad Urbana, dos webs simples, tres suites E2E, una unitaria y
  una de la API)
- Destino      : `/LAB/Lab-E2E.WebBlazor.Documentacion/ia-db` (estructura canónica plana). Sucede al
  workspace `ia-db/Root/` (versión 1.2, del 2026-09-12, commit `7262395`), retirado junto con
  `ia-db/Base/` al quedar un solo repositorio de código
- Fuentes      : `README.md`, `CHANGELOG.md`, `Lab-E2E.WebBlazor.sln`, `pruebas.runsettings`,
  `.gitignore`, `src/` (siete proyectos), `tests/` (cinco), `scripts/`, `.github/workflows/`,
  `evidencia/` (`.log` y `.mjs`; las capturas solo se referencian). Para el índice 07, el árbol
  `Guides/` de `Lab-E2E.WebBlazor.Documentacion`. Para las corridas observadas del índice 06, la API
  pública de GitHub Actions consultada el 2026-09-12
- Exclusiones  : `.git`, `.nuget/`, `.dotnet/`, `.navegadores/`, `publicacion/`, `datos-e2e/`,
  `resultados/`, `bin/`, `obj/`, las capturas `.png` de `evidencia/` y lo ignorado por `.gitignore`
- Estado del repositorio : rama `main`, último commit `88e5caa` (2026-09-12, «Extraer las capas de
  Movilidad Urbana a proyectos y sumar una API REST»)
- Generado     : 2026-09-12 · Versión: 1.0
- Actualizado  : 2026-09-12 · Versión: 1.1 — capas de Movilidad Urbana en proyectos propios y
  `MovilidadUrbana.ApiWeb` con sus pruebas: índice nuevo `12_Api-REST.md`; `00`, `01`, `05` y `06`
  corregidos; `02` y `03` solo en las rutas de sus fuentes; el resto sin cambios
- Actualizar   : `/IA/PROMPTs/IA.Prompts/Tool-Prompts/Indexado-Documentado/Actualizar-Indexado.md`
  (invocado desde `/LAB/Lab-E2E.WebBlazor.Documentacion/PROMPTs/Indexado/Actualizar-Indexado.md`)
