# 00 — Índice maestro

> **Propósito**: situar a un agente en el laboratorio —qué es, con qué está hecho, cómo se reparte
> en proyectos y qué decisiones lo definen— sin abrir el código.
> **Fuente primaria**: `README.md`, `CHANGELOG.md`, `Lab-E2E.WebBlazor.sln`,
> `Lab-E2E.WebBlazor.SinMaui.slnf` y los once `.csproj`.
> **Vigencia**: 2026-09-12, commit `10ce735`.

## Qué es

`Lab-E2E.WebBlazor` es un **laboratorio didáctico**. Su objeto de estudio no es la aplicación sino
las **pruebas de extremo a extremo** que la ejercitan con Playwright y el **pipeline** de GitHub
Actions que las ejecuta. Es la continuación de `Lab-E2E.StaticHtml` —el mismo caso de *movilidad
urbana* resuelto sin servidor— llevada a una aplicación real con servidor y base de datos
(`README.md` §intro).

Tiene **tres aplicaciones web de complejidad creciente**, para estudiar la temática de a un escalón,
y una cuarta aplicación —Android— que lleva el caso de Movilidad Urbana al teléfono:

| Escalón | Aplicación | Qué agrega | Detalle |
| --- | --- | --- | --- |
| 1 | `WebBlazor.HolaMundo` | Una superficie interactiva con sus estados; sin capas ni datos | [10](10_Hola-Mundo-Y-Login.md) |
| 2 | `WebBlazor.Login` | La misma superficie detrás de un acceso por cookies con guard en tres capas | [10](10_Hola-Mundo-Y-Login.md) |
| 3 | `MovilidadUrbana.Web` | Clean Architecture en carpetas por capa, SQLite, aislamiento por sesión, un ABM y un asistente de tres pasos | [01](01_Arquitectura.md), [04](04_Interfaz-Y-Pantallas.md) |
| 3' | `MovilidadUrbana.ApiWeb` | La misma temática como API REST, con sus propias capas | [12](12_Api-REST.md) |
| 3'' | `MovilidadUrbana.MAUI` | La misma temática como app Android nativa (XAML + MVVM), con sus propias capas y la base en el teléfono | [13](13_App-Android.md) |

Hola Mundo y Login llegaron el 2026-09-12 desde `Lab-E2E.WebBlazor.Base`, que se retiró
(`CHANGELOG.md` 2026-09-12). Los registros de `evidencia/` anteriores a esa fecha conservan el
nombre viejo `WebBlazor.E2E.Base.*`: son históricos.

## La decisión que ordena el árbol: tres aplicaciones independientes

Desde el 2026-09-12 (commit `10ce735`) la web, la API y la app Android de Movilidad Urbana **no
comparten código**: cada una trae `Dominio/`, `Aplicacion/` e `Infraestructura/` como carpetas y
espacios de nombres propios (`MovilidadUrbana.Web.*`, `MovilidadUrbana.ApiWeb.*`,
`MovilidadUrbana.MAUI.*`) y no referencia a ningún otro proyecto de la solución. El código se repite
a propósito, «porque cada aplicación tiene que poder estudiarse, compilarse y llevarse por separado»
(`README.md` §Estructura). Los proyectos `MovilidadUrbana.Dominio`, `.Aplicacion` e
`.Infraestructura` que existieron ese mismo día (commit `88e5caa`) se eliminaron.

Verificado al indexar: las tres copias de las tres capas difieren **solo** en el `namespace`, los
`using` y algún comentario (`diff -r` entre `src/MovilidadUrbana.Web/<capa>` y las otras dos). Por
eso [02](02_Dominio-Y-Reglas.md) y [03](03_Sesiones-Y-Persistencia.md) describen las capas una sola
vez, citando la copia de la web.

## Stack

| Capa | Tecnología | Versión | Dónde se declara |
| --- | --- | --- | --- |
| Plataforma | .NET | `net10.0` (`net10.0-android` en la app) | todos los `.csproj` |
| Interfaz web | Blazor Web App, render *interactive server* | — | `Program.cs` y `Components/App.razor` de cada web |
| API | ASP.NET Core con controllers, `ProblemDetails`, OpenAPI 3.1 y Scalar | `Microsoft.AspNetCore.OpenApi` 10.0.11 · `Scalar.AspNetCore` 2.17.3 | `src/MovilidadUrbana.ApiWeb/` |
| App Android | .NET MAUI, XAML nativo, MVVM | `Microsoft.Maui.Controls` `$(MauiVersion)` · `CommunityToolkit.Mvvm` 8.4.2 · `SupportedOSPlatformVersion` 23 | `src/MovilidadUrbana.MAUI/` |
| Datos | EF Core + provider SQLite (las tres aplicaciones de Movilidad Urbana) | `Microsoft.EntityFrameworkCore.Sqlite` 10.0.11 | `Infraestructura/` de cada una |
| Estilos web | Template del Framework SDD: `Tokens.css` + `Componentes.css`, sin librería de componentes ni framework CSS | — | `wwwroot/css/` de cada web — ver [11](11_Template-Y-Superficies.md) |
| Estilos Android | `Colors.xaml` + `Movilidad.xaml` con la paleta de `Tokens.css` | — | `Resources/Styles/` — ver [13](13_App-Android.md) |
| E2E | `Microsoft.Playwright.NUnit` | 1.62.0 | los tres `.csproj` E2E |
| Pruebas de la API | `Microsoft.AspNetCore.Mvc.Testing` (`WebApplicationFactory`) | 10.0.11 | `tests/MovilidadUrbana.ApiWeb.Tests/` |
| Runner | NUnit + `NUnit3TestAdapter` + `Microsoft.NET.Test.Sdk` + `NUnit.Analyzers` | 4.3.2 / 5.0.0 / 17.14.0 / 4.7.0 | los seis `.csproj` de `tests/` |
| Contenedores de apoyo | `mcr.microsoft.com/dotnet/sdk:10.0` · `mcr.microsoft.com/playwright:v1.62.1-noble` · imagen propia `lab-e2e-maui-dev:net10` | — | `scripts/dotnet.sh`, `scripts/pruebas.sh`, `.devcontainer/` |
| CI | GitHub Actions: `checkout@v7`, `setup-dotnet@v6`, `upload-artifact@v7`, `download-artifact@v8`, `cache@v6`, `github-script@v9` | — | `.github/workflows/` — ver [06](06_CI-Y-Workflows.md) |

No hay Bootstrap: se retiró el 2026-09-04 al aplicar el template (`CHANGELOG.md`).

## Los once proyectos

| Proyecto | Ruta | Rol | Referencias de proyecto |
| --- | --- | --- | --- |
| `MovilidadUrbana.Web` | `src/MovilidadUrbana.Web/` | Web Blazor con sus capas; punto de composición en `Program.cs` | ninguna |
| `MovilidadUrbana.ApiWeb` | `src/MovilidadUrbana.ApiWeb/` | API REST con sus capas; `Program.cs` compone controllers, `ProblemDetails`, OpenAPI y Scalar | ninguna |
| `MovilidadUrbana.MAUI` | `src/MovilidadUrbana.MAUI/` | App Android con sus capas y `Presentacion/`; `MauiProgram.cs` compone | ninguna |
| `WebBlazor.HolaMundo` | `src/WebBlazor.HolaMundo/` | La superficie Hola Mundo, autocontenida | ninguna |
| `WebBlazor.Login` | `src/WebBlazor.Login/` | Hola Mundo detrás de un acceso | ninguna |
| `MovilidadUrbana.E2ETests` | `tests/MovilidadUrbana.E2ETests/` | 22 casos Playwright + fixture que publica y levanta la web | ninguna (prueba por HTTP el binario publicado) |
| `MovilidadUrbana.UnitTests` | `tests/MovilidadUrbana.UnitTests/` | 49 casos sobre las reglas | `MovilidadUrbana.Web` |
| `MovilidadUrbana.ApiWeb.Tests` | `tests/MovilidadUrbana.ApiWeb.Tests/` | 13 casos en proceso sobre la API | `MovilidadUrbana.ApiWeb` |
| `MovilidadUrbana.MAUI.Tests` | `tests/MovilidadUrbana.MAUI.Tests/` | 18 casos sobre los ViewModels | ninguna: compila `Dominio/`, `Aplicacion/`, `Infraestructura/` y `Presentacion/` de la app como **archivos enlazados** |
| `WebBlazor.HolaMundo.E2ETests` | `tests/WebBlazor.HolaMundo.E2ETests/` | 1 caso, sin fixture | ninguna |
| `WebBlazor.Login.E2ETests` | `tests/WebBlazor.Login.E2ETests/` | 10 casos, sin fixture | ninguna |

El `.sln` los agrupa en las carpetas de solución `src` y `tests`, y suma tres carpetas de solución
que no compilan: `github-workflow`, `scripts` y `Solution Items` (`README.md`, `CHANGELOG.md`,
`pruebas.runsettings`). **`Lab-E2E.WebBlazor.SinMaui.slnf`** es la misma solución sin
`MovilidadUrbana.MAUI` (diez proyectos, incluidas sus pruebas): es lo que compila `ci.yml`, porque el
runner no tiene el workload de MAUI.

Los conteos (22 + 10 + 1 E2E, 49 unitarios, 13 de API, 18 de ViewModels) están verificados contra
los atributos `[Test]`/`[TestCase]` en [05_Pruebas.md](05_Pruebas.md).

## Puertos y direcciones

| Aplicación | URL | Origen |
| --- | --- | --- |
| `MovilidadUrbana.Web` en desarrollo | `http://localhost:5232` | `Properties/launchSettings.json` |
| `MovilidadUrbana.Web` bajo las E2E | `http://127.0.0.1:4173` (o `PUERTO`) | `ServidorDeLaAplicacion.cs` |
| `MovilidadUrbana.ApiWeb` | `http://localhost:5250` · OpenAPI en `/openapi/v1.json` · Scalar en `/scalar/v1` (Development) | `Properties/launchSettings.json`, `Program.cs` |
| `MovilidadUrbana.MAUI` | Sin red: paquete `ar.lab.movilidadurbana`, base en `FileSystem.AppDataDirectory/movilidad.db` | `.csproj`, `MauiProgram.cs` |
| `WebBlazor.HolaMundo` | `http://localhost:5027` (URL escrita en la prueba) | `launchSettings.json` · `HolaMundoE2ETests.cs` |
| `WebBlazor.Login` | `http://localhost:5181` (URL escrita en la prueba) | `launchSettings.json` · `PruebaDeSuperficie.cs` |

## Decisiones que definen el laboratorio

Resumen; el detalle y el porqué de cada una en [08_Decisiones-Y-Trampas.md](08_Decisiones-Y-Trampas.md).

1. **E2E como proyecto de la solución**, con el binding de .NET de Playwright, para descubrir y
   depurar desde Visual Studio; se renuncia a `--shard`, `blob`/`merge-reports` y al reporte HTML.
2. **Tres aplicaciones independientes** de Movilidad Urbana con todas sus capas repetidas; ningún
   proyecto compartido.
3. **Aislamiento por sesión**: una cookie (`sesion-movilidad`) en la web, un encabezado
   (`X-Sesion-Id`) en la API y el dispositivo entero como sesión en Android, sobre una única SQLite
   por aplicación.
4. **El fixture publica la aplicación e instala el navegador**; no el build.
5. **`ParallelScope.Fixtures`**, no `Children`: el binding de Playwright no soporta más.
6. **Tres aplicaciones web con tres workflows distintos a propósito**, en escalera de complejidad.
7. **Template SDD sin librería de componentes**: un componente Razor propio por patrón del catálogo.
8. **`EnsureCreated` y no migraciones**; **WAL** para que las sesiones paralelas convivan.
9. **La app Android no habla con ningún servidor** y se compila solo con el workload, en el
   devcontainer o en `android.yml`.

## Cómo se corre, en seis líneas

```bash
dotnet test tests/MovilidadUrbana.UnitTests                                   # reglas, sin navegador
dotnet test tests/MovilidadUrbana.ApiWeb.Tests                                # API en proceso
dotnet test tests/MovilidadUrbana.MAUI.Tests                                  # ViewModels, sin teléfono
dotnet test tests/MovilidadUrbana.E2ETests --settings pruebas.runsettings     # publica, levanta y prueba
scripts/pruebas.sh [chromium|firefox|webkit]                                  # todo por contenedor; PROYECTO=holamundo|login
.devcontainer/dev.sh run                                                      # compila, instala y abre la app en el teléfono USB
```

Hola Mundo y Login exigen la aplicación ya levantada en su URL fija (`dotnet run` con el perfil
`http`, o `scripts/pruebas.sh` con `PROYECTO`). Detalle en [05_Pruebas.md](05_Pruebas.md).

## Historia relevante (`CHANGELOG.md`)

| Fecha | Qué pasó |
| --- | --- |
| 2026-08-23 / 24 | Estado verificado con 22 E2E × 4 configuraciones; unitarias y traza de Playwright |
| 2026-08-30 | Proyecto de unitarias (49), traza en `resultados/trazas/`, guías del modelo de ramas, `CHANGELOG.md` |
| 2026-08-31 | Guía de GitHub Actions |
| 2026-09-03 | `.sln` al día con las guías consolidadas; `e2e.yml` vuelve al runner autoalojado |
| 2026-09-04 | La interfaz pasa al template SDD; se retira Bootstrap; `Caso-Encuesta-Page.md` |
| 2026-09-09 | Las guías se mudan a `Lab-E2E.WebBlazor.Documentacion` |
| 2026-09-12 | Llegan Hola Mundo y Login desde `Lab-E2E.WebBlazor.Base` (retirado); un workflow E2E por proyecto; renombre sin `E2E.Base`; capas a proyectos propios + `MovilidadUrbana.ApiWeb` y sus pruebas; Scalar; **y en el último commit** `MovilidadUrbana.MAUI` con sus pruebas, `.devcontainer/`, `android.yml`, el filtro `.slnf` y la vuelta de las capas a cada aplicación como carpetas |

El `CHANGELOG.md` agrupa por fecha y no por número de versión, a propósito: es un laboratorio que
se lee y se corre entero, no un artefacto que se instala. Las dos entradas del 2026-09-12 son un
mismo bloque «Sin publicar»; la extracción a proyectos y su vuelta a carpetas ocurrieron el mismo
día.
