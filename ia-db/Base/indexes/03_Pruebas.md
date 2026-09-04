# 03 — Pruebas E2E

> **Propósito**: registrar qué prueba cada proyecto, cómo está montado y qué hace falta para
> correrlo.
> **Fuente primaria**: `tests/`, `Guides/E2E-Guides.md` y `evidencia/2026-09-01-aplicacion-template/`.
> **Vigencia**: 2026-09-02, commit `6af2049`. Nada de esto se ejecutó durante el indexado.

## Los dos proyectos

Ambos `.csproj` son idénticos salvo el nombre: `net10.0`, `Nullable` y `ImplicitUsings` activos,
`IsPackable` en `false`. No cambiaron desde el indexado inicial.

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
de prueba casi no tienen `using` visibles.

**Ninguno referencia al proyecto de aplicación**: prueban por HTTP contra una URL, con la aplicación
levantada aparte.

## HolaMundoE2ETests — el único caso que compila

`tests/WebBlazor.E2E.Base.HolaMundo.E2ETests/HolaMundoE2ETests.cs`, sin cambios desde el indexado
inicial.

```csharp
[Parallelizable(ParallelScope.Self)]
[TestFixture]
public class HolaMundoE2ETests : PageTest
```

| Miembro | Qué hace |
| --- | --- |
| `[SetUp] Setup` | `Page.GotoAsync("https://localhost:7071/HolaMundo")` (línea 10) — URL **fija en el código**, y el puerto no es el de ningún perfil |
| `[Test] MostrarMensaje` | Llena `campo-frase`, hace clic en `boton-mostrar-frase` y afirma que `campo-mensaje` tiene ese texto |

Hereda de `PageTest`, que da a cada caso una página nueva en su propio `BrowserContext`. El caso deja
a la vista una distinción útil, en una línea comentada: para un `input` se afirma con
`ToHaveValueAsync`, para un elemento de texto con `ToHaveTextAsync`. `ParallelScope.Self` habilita
que este fixture corra en paralelo con otros, no sus casos entre sí.

La aserción sigue siendo válida con la superficie nueva: `campo-mensaje` aparece recién cuando el
envío se resuelve, y `Expect(...)` reintenta hasta que exista.

## El proyecto de pruebas del login no compila

`tests/WebBlazor.E2E.Base.Login.E2ETests/HolaMundoE2ETest.cs` (renombrado desde `LoginE2ETests.cs` en
el commit `6af2049`, «.»). El archivo declara **dos métodos `Setup` en la misma clase**:

```csharp
internal class HolaMundoE2ETest : PageTest
{
    [SetUp] async public Task Setup() { /* agrega la cookie MiCookie */ }
    [SetUp] public async Task Setup() { /* navega y espera estado-app */ }
    …
}
```

Es un error de compilación —dos miembros con el mismo nombre y la misma firma—, así que **el proyecto
no compila y el módulo entero queda fuera de la corrida**, incluido el `[Test] MostrarMensaje` que el
archivo trae copiado del otro proyecto. Sobre eso, el segundo `Setup` arrastra tres problemas
propios: navega primero a `https://localhost:7071/HolaMundo` y enseguida a `/HolaMundo` relativo —sin
`BaseURL` configurada—, y espera un testigo `estado-app` que **no existe en el marcado de este
repositorio**. Todo está detallado en [05_Estado-Y-Divergencias.md](05_Estado-Y-Divergencias.md).

Conclusión práctica: **el flujo de identidad no tiene ninguna cobertura en la batería**. Lo que sí lo
cubre es el guion de evidencia, abajo.

## El guion de verificación de la evidencia

`evidencia/2026-09-01-aplicacion-template/verificar.mjs` — Playwright **para Node**, versión 1.62.1,
corrido en contenedor contra las dos aplicaciones. No es parte de la batería de NUnit y no lo dispara
el workflow: es la evidencia de la aplicación del template.

Su log del 2026-09-01 (`verificacion.log`, versionado a propósito con una excepción en el
`.gitignore`) registra diez comprobaciones, todas en verde:

| Comprobación | Sobre |
| --- | --- |
| `holamundo inicio` · `estado vacio visible` · `campo-mensaje == frase` · `error de entrada exhibido` | La superficie `HolaMundo` y sus estados |
| `sin scroll horizontal a 320px` | La maqueta |
| `guard lleva al ingreso` · `rechazo indiferenciado` · `ingreso aceptado` · `superficie protegida operable` · `cierre de sesión por POST` | El acceso |

Lo acompañan doce capturas `.png` en el mismo directorio. El comando exacto de la corrida está en
`Guides/Template-SDD-Aplicado.md` §4.

## Qué falta respecto del laboratorio grande

No hay `pruebas.runsettings` —aunque el workflow lo pasa—, ni `[SetUpFixture]` que levante la
aplicación, ni espera de interactividad, ni scripts de contenedor para la batería. En concreto:

| Pieza | Base | `Lab-E2E.WebBlazor` |
| --- | --- | --- |
| Levantar el servidor | **A mano**, antes de correr las pruebas | `ServidorDeLaAplicacion` (`[SetUpFixture]`) |
| URL bajo prueba | Literal en el `[SetUp]` | `ServidorDeLaAplicacion.UrlBase`, con `URL_BASE` opcional |
| Esperar el circuito | **No se espera**: no hay testigo `estado-app` en el marcado | Testigo `estado-app` + `EsperarInteractivoAsync` |
| Navegador y timeouts | Los de por defecto | `pruebas.runsettings` |
| Traza de los fallos | No hay | `.zip` por caso fallido |
| Aislamiento de datos | No aplica (no hay datos) | Cookie de sesión que filtra los repositorios |

Sin espera de interactividad, el clic sobre `boton-mostrar-frase` puede llegar antes de que el
circuito esté conectado y perderse sin dejar rastro. Es el problema que el laboratorio grande
documenta como la primera de las seis diferencias con el ejemplo estático.

## Cómo se corren

Según `Guides/E2E-Guides.md`: **desde el Explorador de pruebas de Visual Studio**, con clic derecho
sobre el proyecto de pruebas (la guía ilustra el menú y el resultado con capturas en
`Guides/Imagenes/`). La aplicación bajo prueba tiene que estar corriendo por separado —nada en el
repositorio la levanta—.

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

## Las guías

| Documento | Líneas | Contenido |
| --- | --- | --- |
| `Guides/E2E-Guides.md` | 453 | Definiciones, creación del proyecto (`dotnet new nunit`, `dotnet add package`, `dotnet sln add`), el ejemplo Hola Mundo completo, cómo correrlo y el workflow transcripto; anexos sobre el caso de plantilla que falla y la instalación de navegadores |
| `Guides/Template-SDD-Aplicado.md` | 151 | Qué se aplicó del template, qué se decidió al aplicarlo y cómo se verificó — ver [06](06_Template-Y-Superficies.md) |
| `Guides/GitHub-Action.md` | 0 | **Vacío**, aunque figura en la solución y el `README.md` lo enlaza |
| `Guides/Notas.GitHub.md` | 14 | Sin versionar. Cómo evitar que un PR desde un fork ejecute el runner propio — ver [04](04_CI-Y-Workflow.md) |

`E2E-Guides.md` describe la superficie `HolaMundo` **anterior** a la aplicación del template: su
transcripción del `.razor` todavía muestra `class="form-control"` de Bootstrap y un `@onclick`
(líneas 90 y 101), donde hoy hay un `EditForm` con clases `mq-`. Los tres `data-testid` sí se
conservaron, así que la prueba que la guía enseña sigue siendo la vigente.
