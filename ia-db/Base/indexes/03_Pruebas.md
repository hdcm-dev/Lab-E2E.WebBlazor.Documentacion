# 03 — Pruebas E2E

> **Propósito**: registrar qué prueba cada proyecto, cómo está montado y qué hace falta para
> correrlo.
> **Fuente primaria**: `tests/` y `Guides/E2E-Guides.md`.

## Los dos proyectos

Ambos `.csproj` son idénticos salvo el nombre: `net10.0`, `Nullable` y `ImplicitUsings` activos,
`IsPackable` en `false`.

| Paquete | Versión |
| --- | --- |
| `Microsoft.Playwright.NUnit` | 1.52.0 |
| `Microsoft.NET.Test.Sdk` | 17.14.0 |
| `NUnit` | 4.3.2 |
| `NUnit.Analyzers` | 4.7.0 |
| `NUnit3TestAdapter` | 5.0.0 |
| `coverlet.collector` | 6.0.4 |

Los `Using` globales están declarados en el `.csproj`: `Microsoft.Playwright.NUnit`,
`NUnit.Framework`, `System.Text.RegularExpressions` y `System.Threading.Tasks`. Por eso los archivos
de prueba no tienen ningún `using` visible.

**Ninguno referencia al proyecto de aplicación**: prueban por HTTP contra una URL, con la aplicación
levantada aparte.

## HolaMundoE2ETests

`tests/WebBlazor.E2E.Base.HolaMundo.E2ETests/HolaMundoE2ETests.cs`. Es el ejemplo completo del
repositorio.

```csharp
[Parallelizable(ParallelScope.Self)]
[TestFixture]
public class HolaMundoE2ETests : PageTest
```

| Miembro | Qué hace |
| --- | --- |
| `[SetUp] Setup` | `Page.GotoAsync("https://localhost:7071/HolaMundo")` — URL **fija en el código** |
| `[Test] MostrarMensaje` | Llena `campo-frase`, hace clic en `boton-mostrar-frase` y afirma que `campo-mensaje` tiene ese texto |

Hereda de `PageTest`, que da a cada caso una página nueva en su propio `BrowserContext`.

El caso deja a la vista una distinción útil, en una línea comentada: para un `input` se afirma con
`ToHaveValueAsync`, para un `div` con `ToHaveTextAsync`.

`ParallelScope.Self` habilita que este fixture corra en paralelo con otros, no sus casos entre sí.

## LoginE2ETests

`tests/WebBlazor.E2E.Base.Login.E2ETests/LoginE2ETests.cs`.

```csharp
[Parallelizable(ParallelScope.Self)]
[TestFixture]
internal class LoginE2ETests : PageTest
```

| Miembro | Qué hace |
| --- | --- |
| `[SetUp] Setup` | Agrega una cookie llamada `MiCookie` con un `Guid` como valor |
| `[Test] TestLogin` | **Vacío**: dos comentarios en inglés sobre qué habría que implementar |

Ni el `[SetUp]` navega a ninguna página, ni la cookie `MiCookie` corresponde a nada del servidor
—la de autenticación se llama `auth_token`, ver [02_Autenticacion.md](02_Autenticacion.md)—. El
proyecto es un esqueleto reservado, no una prueba. Está registrado en
[05_Estado-Y-Divergencias.md](05_Estado-Y-Divergencias.md).

## Qué falta respecto del laboratorio grande

No hay `pruebas.runsettings`, ni `[SetUpFixture]` que levante la aplicación, ni espera de
interactividad, ni scripts de contenedor. En concreto:

| Pieza | Base | `Lab-E2E.WebBlazor` |
| --- | --- | --- |
| Levantar el servidor | **A mano**, antes de correr las pruebas | `ServidorDeLaAplicacion` (`[SetUpFixture]`) |
| URL bajo prueba | Literal en el `[SetUp]` | `ServidorDeLaAplicacion.UrlBase`, con `URL_BASE` opcional |
| Esperar el circuito | **No se espera** | Testigo `estado-app` + `EsperarInteractivoAsync` |
| Navegador y timeouts | Los de por defecto | `pruebas.runsettings` |
| Traza de los fallos | No hay | `.zip` por caso fallido |
| Aislamiento de datos | No aplica (no hay datos) | Cookie de sesión que filtra los repositorios |

Sin espera de interactividad, el clic sobre `boton-mostrar-frase` puede llegar antes de que el
circuito esté conectado y perderse sin dejar rastro. Es el problema que el laboratorio grande
documenta como la primera de las seis diferencias con el ejemplo estático.

## Cómo se corren

Según `Guides/E2E-Guides.md`: **desde el Explorador de pruebas de Visual Studio**, con clic derecho
sobre el proyecto de pruebas (la guía ilustra el menú y el resultado con capturas en
`Guides/Imagenes/`).

La aplicación bajo prueba tiene que estar corriendo por separado —nada en el repositorio la levanta—.

### Instalación de los navegadores

La guía la resuelve a mano, con el script que genera el build:

```bash
cd WebBlazor.E2E.Base.HolaMundo.E2ETests\
./bin/Debug/net10.0/playwright.ps1 install
```

Es la vía documentada por Playwright, y exige PowerShell 7. (El laboratorio grande la reemplaza por
una llamada al mismo instalador desde el propio fixture.)

El anexo de la guía explica el síntoma que lleva hasta acá: heredar de `PageTest` hace que
`BrowserTest.BrowserSetup()` intente lanzar el navegador con `BrowserType.LaunchAsync()`, y si los
binarios no están descargados el ejecutable no existe y se lanza la excepción.

## La guía de estudio

`Guides/E2E-Guides.md` (453 líneas). Estructura:

| Sección | Contenido |
| --- | --- |
| Definiciones iniciales | Qué es una prueba E2E y qué aporta Playwright: espera a que el elemento exista, aserciones con reintento, contexto de navegador propio por prueba |
| 1. Creación del proyecto | `dotnet new nunit`, `dotnet add package Microsoft.Playwright.NUnit`, `dotnet sln add`; y la alternativa desde el asistente de Visual Studio |
| 2. Ejemplo: Hola Mundo | Estructura del repositorio, el `.razor` completo, la prueba, cómo correrla desde el Explorador y el workflow de GitHub Actions transcripto |
| 3. Anexos | Por qué falla el caso de plantilla de Playwright y cómo instalar los navegadores |

`Guides/GitHub-Action.md` está **vacío** (0 líneas), aunque figura en la solución.
