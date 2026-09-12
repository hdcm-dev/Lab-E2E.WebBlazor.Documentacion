# 00 — Índice maestro

> **Propósito**: dar la visión general del laboratorio —qué es, con qué está hecho y qué decisiones
> lo definen— para que un agente pueda situarse sin abrir el código.
> **Fuente primaria**: `README.md`, `CHANGELOG.md` y `Lab-E2E.WebBlazor.sln` del repositorio.
> **Vigencia**: 2026-09-12, commit `88e5caa`.

## Qué es

`Lab-E2E.WebBlazor` es un laboratorio didáctico. Su objeto de estudio no es la aplicación sino
**las pruebas de extremo a extremo que la ejercitan y el pipeline que las ejecuta**.

Desde el 2026-09-12 tiene **tres aplicaciones web de complejidad creciente**, para que la temática
se pueda estudiar de a un escalón:

| Escalón | Aplicación | Qué agrega |
| --- | --- | --- |
| 1 | `WebBlazor.HolaMundo` | Una superficie interactiva con sus estados; sin capas ni datos |
| 2 | `WebBlazor.Login` | La misma superficie detrás de un acceso por cookies |
| 3 | `MovilidadUrbana.Web` + `MovilidadUrbana.ApiWeb` | Servidor, SQLite, aislamiento por sesión, un ABM y un asistente; Clean Architecture en **proyectos por capa**, con dos cabezas —la web y una API REST— sobre las mismas capas |

Las dos primeras llegaron desde `Lab-E2E.WebBlazor.Base`, que se retiró; su detalle está en
[10_Hola-Mundo-Y-Login.md](10_Hola-Mundo-Y-Login.md).

Movilidad Urbana es la continuación de `Lab-E2E.StaticHtml`, el mismo ejemplo resuelto sin servidor:
allá el estado vivía en `localStorage`, acá vive en SQLite y cada interacción viaja por el circuito de
Blazor — ver [08_Decisiones-Y-Trampas.md](08_Decisiones-Y-Trampas.md).

## Stack

| Capa | Tecnología | Versión | Dónde se declara |
| --- | --- | --- | --- |
| Plataforma | .NET | `net10.0` | los `.csproj` |
| Interfaz | Blazor Web App, render *interactive server* | — | `Program.cs` y `Components/App.razor` de cada aplicación |
| Datos | EF Core + provider SQLite (solo Movilidad Urbana) | 10.0.11 | `MovilidadUrbana.Web.csproj` |
| Estilos | Template del Framework SDD: `Tokens.css` + `Componentes.css`, sin librería de componentes ni framework de CSS | — | `wwwroot/css/` de cada aplicación — ver [11](11_Template-Y-Superficies.md) |
| E2E | `Microsoft.Playwright.NUnit` | 1.62.0 | los tres `.csproj` E2E |
| Runner de pruebas | NUnit + `NUnit3TestAdapter` + `Microsoft.NET.Test.Sdk` | 4.3.2 / 5.0.0 / 17.14.0 | los cuatro `.csproj` de `tests/` |
| Contenedores de apoyo | `mcr.microsoft.com/dotnet/sdk:10.0`, `mcr.microsoft.com/playwright:v1.62.1-noble` | — | `scripts/dotnet.sh`, `scripts/pruebas.sh` |

**Ya no hay Bootstrap**: se retiró el 2026-09-04 al aplicar el template.

## Los doce proyectos de la solución

| Proyecto | Ruta | Rol |
| --- | --- | --- |
| `MovilidadUrbana.Dominio` | `src/MovilidadUrbana.Dominio/` | Entidades, reglas y catálogos. No depende de nada |
| `MovilidadUrbana.Aplicacion` | `src/MovilidadUrbana.Aplicacion/` | Casos de uso y abstracciones. Depende de Dominio |
| `MovilidadUrbana.Infraestructura` | `src/MovilidadUrbana.Infraestructura/` | EF Core sobre SQLite y la sesión por cookie. Depende de Aplicacion |
| `MovilidadUrbana.Web` | `src/MovilidadUrbana.Web/` | Presentación Blazor y composición |
| `MovilidadUrbana.ApiWeb` | `src/MovilidadUrbana.ApiWeb/` | Presentación REST y composición — ver [12](12_Api-REST.md) |
| `WebBlazor.HolaMundo` | `src/WebBlazor.HolaMundo/` | La superficie Hola Mundo |
| `WebBlazor.Login` | `src/WebBlazor.Login/` | Hola Mundo detrás de un acceso |
| `MovilidadUrbana.E2ETests` | `tests/MovilidadUrbana.E2ETests/` | 22 casos, con fixture que levanta la aplicación |
| `MovilidadUrbana.UnitTests` | `tests/MovilidadUrbana.UnitTests/` | 49 casos sobre las reglas de dominio; referencia solo `Dominio` |
| `MovilidadUrbana.ApiWeb.Tests` | `tests/MovilidadUrbana.ApiWeb.Tests/` | 13 casos en proceso sobre la API, con `WebApplicationFactory` |
| `WebBlazor.HolaMundo.E2ETests` | `tests/WebBlazor.HolaMundo.E2ETests/` | 1 caso, sin fixture |
| `WebBlazor.Login.E2ETests` | `tests/WebBlazor.Login.E2ETests/` | 10 casos, sin fixture |

El `.sln` los agrupa bajo las carpetas de solución `src` y `tests`, y los archivos que no pertenecen
a ningún proyecto van en otras tres: `github-workflow`, `scripts` y `Solution Items` (`README.md`,
`CHANGELOG.md`, `pruebas.runsettings`). Las guías ya no: se mudaron a
`Lab-E2E.WebBlazor.Documentacion` el 2026-09-09 — ver [07](07_Guias.md).

## Decisiones que definen el proyecto

Cada una está desarrollada en [08_Decisiones-Y-Trampas.md](08_Decisiones-Y-Trampas.md).

| Decisión | En una línea |
| --- | --- |
| **Tres aplicaciones de complejidad creciente** | La escalera es didáctica: fixture, URL y workflow difieren a propósito entre ellas |
| **Capas en proyectos, no en carpetas** (desde el 2026-09-12) | Para que la web y la API compartan reglas sin duplicarlas ni referenciar un proyecto web desde otro |
| **La API identifica la sesión por encabezado**, no por cookie | `X-Sesion-Id` es lo idiomático en REST; el aislamiento de datos es el mismo |
| Playwright con las **vinculaciones de .NET**, no el runner de JavaScript | Se gana descubrimiento y depuración desde Visual Studio; se pierden `--shard`, `merge-reports` y el reporte HTML |
| Las E2E son **proyectos de la solución** | La alternativa —carpeta `e2e/` con TypeScript, como `dotnet/eShop`— es igual de defendible; esta prioriza el IDE |
| **Un workflow E2E por aplicación**, independientes | Cada uno con la complejidad que su proyecto necesita — ver [06](06_CI-Y-Workflows.md) |
| Hola Mundo y Login **sin fixture** | La prueba apunta a una URL fija; la aplicación la levanta el script o el workflow |
| **Aislamiento por cookie de sesión** (Movilidad Urbana) | Cada prueba estrena su espacio de datos sobre una única base; es lo que habilita el paralelismo |
| **Publicar e instalar navegadores en el fixture**, no en el build | Corre siempre igual en consola, IDE y CI |
| Movilidad Urbana y Login se prueban sobre el **binario publicado** en CI | Se prueba el mismo artefacto que se despliega. Hola Mundo, el escalón simple, usa `dotnet run` |
| **`ParallelScope.Fixtures`** y nada más | Paralelizar dentro de una clase rompe el registro por worker de Playwright |
| `EnsureCreated` en lugar de **migraciones** | El laboratorio no versiona el esquema |
| **Un solo lugar** para el número de workers | Vive en `pruebas.runsettings` |

## Estado verificado

| Fecha | Comprobación | Resultado | Fuente |
| --- | --- | --- | --- |
| 2026-08-23 | `dotnet build … -warnaserror` | 0 avisos, 0 errores | `README.md` §Evidencia |
| 2026-08-23 | `scripts/pruebas.sh` chromium / firefox / webkit / móvil | 22 pasadas en cada una | ídem |
| 2026-08-24 | `dotnet test tests/MovilidadUrbana.UnitTests` | 49 pasadas | ídem |
| 2026-08-24 | Traza de un caso fallido a propósito | `.zip` de 138 KB con DOM, red y consola | ídem |
| 2026-09-01 | Hola Mundo y Login con el template aplicado: `verificar.mjs` | 10 comprobaciones en verde, 12 capturas | `evidencia/2026-09-01-aplicacion-template/` |
| 2026-09-03 | Testigo de hidratación en Hola Mundo | Cierra la intermitencia | `evidencia/2026-09-03-testigo-de-hidratacion/` |
| 2026-09-04 | Build, unitarias y las 4 configuraciones E2E tras el template | Todo en verde: 49 y 22×4 | `README.md` §Evidencia |
| 2026-09-12 | `dotnet build Lab-E2E.WebBlazor.sln -c Release -warnaserror`, siete proyectos | 0 avisos, 0 errores | `CHANGELOG.md` |
| 2026-09-12 | Hola Mundo y Login con `scripts/pruebas.sh`, 3 corridas cada uno | 3 de 3 en verde | `evidencia/2026-09-12-unificacion/*-script-3-corridas.log` |
| 2026-09-12 | Movilidad Urbana con `scripts/pruebas.sh` | 22/22 | `…/movilidad-script-por-defecto.log` |
| 2026-09-12 | Login como lo corre su workflow —binario publicado, Production— | 10/10 en chromium y firefox | `…/login-falsificacion-y-binario-publicado.log` |
| 2026-09-12 | Hola Mundo y Login sin la aplicación levantada | Fallan: no pasan en vacío | `…/*-falsificacion-*.log` |
| 2026-09-12 | GitHub Actions: `ci.yml`, `e2e-holamundo.yml` y `e2e-login.yml` sobre `f9f3ca2`; `ci.yml` sobre `06528d3` | En verde | API pública de Actions — ver [06](06_CI-Y-Workflows.md) |
| 2026-09-12 | Solución de doce proyectos en Release con `-warnaserror`; unitarias y E2E de la web tras extraer las capas | 0 avisos; 49/49 y 22/22 sin cambios | `evidencia/2026-09-12-capas-y-api/` |
| 2026-09-12 | API: pruebas en proceso; falsificación (200 en vez de 201); corrida real sobre Kestrel con OpenAPI y `curl` | 13/13; un caso en rojo; ocho rutas expuestas | ídem |

**No verificado**: la ejecución desde el Explorador de pruebas de Visual Studio —no hay Windows en esa
máquina—, incluido el paso previo que necesitan Hola Mundo y Login.

## Historia reciente

| Fecha | Cambio |
| --- | | 2026-09-12 | Capas de Movilidad Urbana en proyectos propios; `MovilidadUrbana.ApiWeb` con sus pruebas; los proyectos mudados pierden el prefijo `E2E.Base` |
--- |
| 2026-09-12 | Unificación con `Lab-E2E.WebBlazor.Base`: Hola Mundo y Login, un workflow E2E por aplicación, `scripts/pruebas.sh` con `PROYECTO` y `REPETIR`, `evidencia/` (incluida la del template, rescatada en `06528d3`) |
| 2026-09-09 | Las guías se mudan a `Lab-E2E.WebBlazor.Documentacion` |
| 2026-09-04 | Template del Framework SDD en la interfaz; se retira Bootstrap; `Caso-Encuesta-Page.md` |
| 2026-09-03 | El runner autoalojado vuelve a estar activo en `e2e.yml` —hoy, en el job `publicar`—; el `.sln` se pone al día |
| 2026-08-31 | Guía de GitHub Actions |
| 2026-08-30 | Proyecto de unitarias, traza de Playwright, guías del modelo de ramas, `CHANGELOG.md` |

Fuente: `CHANGELOG.md`, que agrupa por fecha y no por versión.
