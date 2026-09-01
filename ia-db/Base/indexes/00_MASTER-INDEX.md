# 00 — Índice maestro

> **Propósito**: dar la visión general del repositorio —qué es, qué contiene y en qué estado está—
> para que un agente pueda situarse sin abrir el código.
> **Fuente primaria**: `Ejemplos.WebBlazor.E2E.Base.slnx`, `Guides/E2E-Guides.md` y el árbol de `src/`.

## Qué es

`Lab-E2E.WebBlazor.Base` es el **andamiaje mínimo** de una prueba de extremo a extremo con
Playwright sobre Blazor. Muestra lo esencial y nada más: una página con dos controles y un `div`,
los tres marcados con `data-testid`, y una prueba que los llena, hace clic y afirma sobre el
resultado.

Su relación con [`Lab-E2E.WebBlazor`](../../Root/README.md) es de escalón: allá el mismo enfoque se
lleva a una aplicación con servidor, base de datos, aislamiento por sesión, 22 casos y un pipeline
completo. Acá se ve **la técnica desnuda**, sin nada alrededor.

El `README.md` del repositorio contiene únicamente su título: la documentación de estudio está en
`Guides/E2E-Guides.md`.

## La solución

`Ejemplos.WebBlazor.E2E.Base.slnx` — formato `.slnx`, con carpetas de solución para el workflow y
las guías.

| Proyecto | Ruta | Rol |
| --- | --- | --- |
| `WebBlazor.E2E.Base.HolaMundo` | `src/WebBlazor.E2E.Base.HolaMundo/` | Blazor de plantilla + la página `HolaMundo` |
| `WebBlazor.E2E.Base.Login` | `src/WebBlazor.E2E.Base.Login/` | Lo mismo, más autenticación por cookies y `[Authorize]` |
| `WebBlazor.E2E.Base.HolaMundo.E2ETests` | `tests/…HolaMundo.E2ETests/` | 1 caso E2E funcional |
| `WebBlazor.E2E.Base.Login.E2ETests` | `tests/…Login.E2ETests/` | 1 caso E2E con el cuerpo vacío |

Los proyectos de prueba **no referencian** a los de aplicación: prueban por HTTP contra una URL, con
la aplicación levantada aparte.

## Stack

| Capa | Tecnología | Versión | Dónde se declara |
| --- | --- | --- | --- |
| Plataforma | .NET | `net10.0` | los cuatro `.csproj` |
| Interfaz | Blazor Web App, render *interactive server* | — | `Program.cs`, `Components/App.razor` |
| E2E | `Microsoft.Playwright.NUnit` | **1.52.0** | los dos `.csproj` de `tests/` |
| Runner | NUnit + `NUnit3TestAdapter` | 4.3.2 / 5.0.0 | ídem |
| Estilos | Bootstrap de la plantilla, en `wwwroot/lib/bootstrap/` | — | `Components/App.razor` |

No hay EF Core, ni base de datos, ni capas de dominio o aplicación: los dos proyectos web son la
plantilla estándar de Blazor con una o dos páginas agregadas. Ambos declaran
`BlazorDisableThrowNavigationException` en `true`.

## Diferencias con Lab-E2E.WebBlazor

| Aspecto | Base | Lab-E2E.WebBlazor |
| --- | --- | --- |
| Aplicaciones | Dos, de plantilla | Una, con Clean Architecture en carpetas |
| Persistencia | Ninguna | EF Core sobre SQLite, aislado por sesión |
| Casos E2E | 2 declarados (1 con cuerpo) | 22, en 4 configuraciones |
| Servidor bajo prueba | Se levanta **a mano** | Lo levanta un `[SetUpFixture]` |
| URL | Fija en el `[SetUp]` de la prueba | `ServidorDeLaAplicacion.UrlBase`, configurable |
| Espera de interactividad | **No hay** | Testigo `estado-app` + `EsperarInteractivoAsync` |
| Aislamiento entre pruebas | Una cookie propia sin uso en el servidor | Cookie de sesión que filtra todos los repositorios |
| Playwright | 1.52 | 1.62 |
| Workflows | Uno, sin adaptar del todo | Tres, con reutilización y protección de rama |
| Documentación | Una guía + un archivo vacío | Cuatro familias de guías, README extenso y changelog |

## Estado

El repositorio está **en construcción**. No hay changelog; los tres commits del historial son
«iniciando repo», «agregando login» y «login fix» (último: 2026-09-01).

Las divergencias verificadas —URL de la prueba que no coincide con ningún perfil de arranque,
workflow que todavía nombra al laboratorio grande, guía vacía— están todas en
[05_Estado-Y-Divergencias.md](05_Estado-Y-Divergencias.md). **Es el índice que hay que leer antes de
tocar nada.**
