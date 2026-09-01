# 00 — Índice maestro

> **Propósito**: dar la visión general del laboratorio —qué es, con qué está hecho y qué decisiones
> lo definen— para que un agente pueda situarse sin abrir el código.
> **Fuente primaria**: `README.md` y `CHANGELOG.md` del repositorio.

## Qué es

`Lab-E2E.WebBlazor` es un laboratorio didáctico. Su objeto de estudio no es la aplicación sino
**las pruebas de extremo a extremo que la ejercitan y el pipeline que las ejecuta**. La aplicación
—*movilidad urbana*— existe para dar algo real que probar: tiene servidor, base de datos y estado
compartido, que es exactamente lo que hace interesantes a las E2E.

Es la continuación de `Lab-E2E.StaticHtml`, el mismo ejemplo resuelto sin servidor: allá el estado
vivía en `localStorage`, acá vive en SQLite y cada interacción viaja por el circuito de Blazor. La
comparación entre ambos es material de estudio en sí misma —ver
[08_Decisiones-Y-Trampas.md](08_Decisiones-Y-Trampas.md).

## Stack

| Capa | Tecnología | Versión | Dónde se declara |
| --- | --- | --- | --- |
| Plataforma | .NET | `net10.0` | `src/MovilidadUrbana.Web/MovilidadUrbana.Web.csproj` |
| Interfaz | Blazor Web App, render *interactive server* | — | `Program.cs`, `Components/App.razor` |
| Datos | EF Core + provider SQLite | 10.0.11 | `MovilidadUrbana.Web.csproj` |
| E2E | `Microsoft.Playwright.NUnit` | 1.62.0 | `tests/MovilidadUrbana.E2ETests/*.csproj` |
| Runner de pruebas | NUnit + `NUnit3TestAdapter` | 4.3.2 / 5.0.0 | ambos `.csproj` de `tests/` |
| Estilos | Bootstrap vendorizado, **sin** su bundle de JavaScript | 5.3.8 | `src/MovilidadUrbana.Web/wwwroot/vendor/bootstrap/` |
| Contenedores de apoyo | `mcr.microsoft.com/dotnet/sdk:10.0`, `mcr.microsoft.com/playwright:v1.62.1-noble` | — | `scripts/dotnet.sh`, `scripts/pruebas.sh` |

## Los tres proyectos de la solución

| Proyecto | Ruta | Rol |
| --- | --- | --- |
| `MovilidadUrbana.Web` | `src/MovilidadUrbana.Web/` | La aplicación. Un solo proyecto, capas en carpetas |
| `MovilidadUrbana.E2ETests` | `tests/MovilidadUrbana.E2ETests/` | 22 casos que ejercitan el circuito completo con navegador |
| `MovilidadUrbana.UnitTests` | `tests/MovilidadUrbana.UnitTests/` | 49 casos sobre las reglas de dominio, sin navegador ni servidor |

Las unitarias son **hermanas** de las E2E, no parte de ellas: verifican las reglas por sí solas
mientras las E2E verifican el circuito. `ci.yml` las corre en el job barato, antes de gastar un
runner con navegadores.

Los archivos que no pertenecen a ningún proyecto —`Guides/`, `scripts/`, `.github/workflows/`—
están agrupados en **carpetas de solución** que reproducen el árbol del disco, para poder abrirlos
desde el Explorador de soluciones de Visual Studio. No se compilan ni afectan el build.

## Decisiones que definen el proyecto

Cada una está desarrollada en [08_Decisiones-Y-Trampas.md](08_Decisiones-Y-Trampas.md).

| Decisión | En una línea |
| --- | --- |
| Playwright con las **vinculaciones de .NET**, no el runner de JavaScript | Se gana descubrimiento y depuración desde Visual Studio; se pierden `--shard`, `merge-reports` y el reporte HTML |
| Las E2E son **un proyecto de la solución** | La alternativa —carpeta `e2e/` con TypeScript, como `dotnet/eShop`— es igual de defendible; esta prioriza el IDE |
| **Aislamiento por cookie de sesión** | Cada prueba estrena su espacio de datos sobre una única base compartida; es lo que habilita el paralelismo |
| **Publicar e instalar navegadores en el fixture**, no en el build | Corre siempre y de la misma forma en consola, IDE y CI |
| Las pruebas ejercitan el **binario publicado**, no `dotnet run` | Se prueba el mismo artefacto que se despliega |
| **`ParallelScope.Fixtures`** y nada más | Paralelizar dentro de una clase rompe el registro por worker de Playwright |
| `EnsureCreated` en lugar de **migraciones** | El laboratorio no versiona el esquema; el binario arranca en cualquier máquina sin pasos previos |
| **Un solo lugar** para el número de workers | Vive en `pruebas.runsettings`; el *alcance* del paralelismo vive en el código |

## Estado verificado

El `README.md` registra evidencia de ejecución fechada. Lo verificado en la máquina del autor:

| Fecha | Comprobación | Resultado |
| --- | --- | --- |
| 2026-08-23 | `dotnet build … -warnaserror` | 0 avisos, 0 errores |
| 2026-08-23 | `scripts/pruebas.sh` chromium / firefox / webkit / móvil | 22 pasadas en cada una (88 en total) |
| 2026-08-24 | `dotnet test tests/MovilidadUrbana.UnitTests` | 49 pasadas en 27 ms |
| 2026-08-24 | Traza de un caso fallido a propósito | `.zip` de 138 KB con DOM, red y consola |

**No verificado** (así lo declara el propio repositorio): la ejecución desde el Explorador de
pruebas de Visual Studio —no hay Windows en esa máquina— y el comportamiento real de los workflows,
del que solo se validó la sintaxis YAML.

## Historia reciente

| Fecha | Cambio |
| --- | --- |
| 2026-08-31 | Guía de GitHub Actions en `Guides/GitHub-Action-Guide/` |
| 2026-08-30 | Proyecto de unitarias, traza de Playwright, guías del modelo de ramas, `CHANGELOG.md` |

Fuente: `CHANGELOG.md`. El registro agrupa por fecha y no por versión: lo que se publica es un
laboratorio que se lee y se corre entero, no un artefacto instalable.
