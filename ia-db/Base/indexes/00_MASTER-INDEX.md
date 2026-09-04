# 00 — Índice maestro

> **Propósito**: dar la visión general del repositorio —qué es, qué contiene y en qué estado está—
> para que un agente pueda situarse sin abrir el código.
> **Fuente primaria**: `README.md`, `Ejemplos.WebBlazor.E2E.Base.slnx`, `Guides/` y el árbol de `src/`.
> **Vigencia**: 2026-09-02, commit `6af2049`.

## Qué es

`Lab-E2E.WebBlazor.Base` son los **proyectos base para practicar pruebas E2E** con Playwright sobre
Blazor Web App (.NET 10, render *interactive server*). Su `README.md` lo dice en una tabla: un
proyecto muestra una superficie interactiva con sus estados y sus identificadores de prueba
declarados en el marcado; el otro, lo mismo detrás de un acceso.

Su relación con [`Lab-E2E.WebBlazor`](../../Root/README.md) es de escalón: allá el mismo enfoque se
lleva a una aplicación con servidor, base de datos, aislamiento por sesión, 22 casos y un pipeline
completo. Acá se ve **la técnica desnuda**, sin dominio ni persistencia alrededor.

Desde el 2026-09-01 los dos proyectos están construidos con el **template por defecto del Framework
SDD**: tokens del catálogo, clases `mq-`, un componente propio por patrón y ninguna librería de
componentes. Esa forma constructiva es un dominio en sí mismo y tiene su índice:
[06_Template-Y-Superficies.md](06_Template-Y-Superficies.md).

## La solución

`Ejemplos.WebBlazor.E2E.Base.slnx` — formato `.slnx`, con carpetas de solución para el workflow y
las guías (tres guías declaradas, más las tres imágenes).

| Proyecto | Ruta | Rol |
| --- | --- | --- |
| `WebBlazor.E2E.Base.HolaMundo` | `src/WebBlazor.E2E.Base.HolaMundo/` | La superficie `HolaMundo` con sus cuatro estados |
| `WebBlazor.E2E.Base.Login` | `src/WebBlazor.E2E.Base.Login/` | Lo mismo detrás de un acceso por cookies, con el guard en tres capas |
| `WebBlazor.E2E.Base.HolaMundo.E2ETests` | `tests/…HolaMundo.E2ETests/` | 1 caso E2E |
| `WebBlazor.E2E.Base.Login.E2ETests` | `tests/…Login.E2ETests/` | Sin caso propio: el archivo no compila — ver [05](05_Estado-Y-Divergencias.md) |

Los proyectos de prueba **no referencian** a los de aplicación: prueban por HTTP contra una URL, con
la aplicación levantada aparte.

## Stack

| Capa | Tecnología | Versión | Dónde se declara |
| --- | --- | --- | --- |
| Plataforma | .NET | `net10.0` | los cuatro `.csproj` |
| Interfaz | Blazor Web App, render *interactive server* | — | `Program.cs`, `Components/App.razor` |
| Estilos | Propios: `wwwroot/css/Tokens.css` + `Componentes.css` | — | `Components/App.razor` |
| Identidad | Cookies de ASP.NET Core + endpoints propios | — | `Login/Program.cs`, `Endpoints/IdentidadEndpoints.cs` |
| E2E | `Microsoft.Playwright.NUnit` | **1.52.0** | los dos `.csproj` de `tests/` |
| Runner | NUnit + `NUnit3TestAdapter` | 4.3.2 / 5.0.0 | ídem |
| Verificación de la maqueta | Playwright para Node, en contenedor | 1.62.1 | `evidencia/2026-09-01-aplicacion-template/verificar.mjs` |

No hay EF Core, ni base de datos, ni capas de dominio o aplicación. **Ya no hay Bootstrap**: la copia
vendorizada de `wwwroot/lib/` y los `app.css` / `.razor.css` del andamiaje se retiraron al aplicar el
template (commits `d32b4ab` y `eaa151a`).

## Diferencias con Lab-E2E.WebBlazor

| Aspecto | Base | Lab-E2E.WebBlazor |
| --- | --- | --- |
| Aplicaciones | Dos, con template propio | Una, con Clean Architecture en carpetas |
| Persistencia | Ninguna | EF Core sobre SQLite, aislado por sesión |
| Casos E2E | 1 que compila | 22, en 4 configuraciones |
| Servidor bajo prueba | Se levanta **a mano** | Lo levanta un `[SetUpFixture]` |
| URL | Fija en el `[SetUp]` de la prueba | `ServidorDeLaAplicacion.UrlBase`, configurable |
| Espera de interactividad | **No hay testigo** (`estado-app` no existe en el marcado) | Testigo `estado-app` + `EsperarInteractivoAsync` |
| Estilos | Tokens propios del catálogo SDD | Bootstrap 5.3.8 vendorizado |
| Playwright (pruebas) | 1.52 | 1.62 |
| Workflows | Uno, con `pull_request` y una divergencia en pie | Tres, con reutilización y protección de rama |
| Documentación | Tres guías + evidencia versionada | Cinco carpetas de guías, README extenso y changelog |

## Estado

El repositorio sigue siendo **material de práctica en construcción**, pero avanzó bastante desde el
indexado inicial: hay 15 commits, el `README.md` dejó de ser un título suelto, se aplicó el template
en las dos aplicaciones y la corrida de verificación quedó versionada como evidencia. No hay
`CHANGELOG.md`.

| Fecha | Commit | Qué trajo |
| --- | --- | --- |
| 2026-09-01 | `d32b4ab`, `eaa151a` | Template propio en `HolaMundo` y en `Login`; se quita el Bootstrap vendorizado |
| 2026-09-01 | `0b5c4c7`, `f8a2a04` | `Guides/Template-SDD-Aplicado.md` y la evidencia de la verificación, log incluido |
| 2026-09-01 | `65435e5` | El workflow se dispara en los pull requests hacia `main` |
| 2026-09-02 | `ca68245` | El workflow deja de nombrar rutas de `MovilidadUrbana` |

Lo que sigue abierto —el proyecto de pruebas del login que no compila, `pruebas.runsettings` que el
workflow pide y no existe, `Guides/GitHub-Action.md` vacío— está en
[05_Estado-Y-Divergencias.md](05_Estado-Y-Divergencias.md). **Es el índice que hay que leer antes de
tocar nada.**
