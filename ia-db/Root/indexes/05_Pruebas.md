# 05 — Pruebas

> **Propósito**: registrar qué cubre cada suite, cómo se ejecutan, qué hace la infraestructura de
> las E2E y qué variables de entorno la gobiernan.
> **Fuente primaria**: `tests/`, `pruebas.runsettings`, `scripts/pruebas.sh`.

## Las dos suites

| Suite | Proyecto | Casos | Qué verifica | Duración |
| --- | --- | --- | --- | --- |
| Unitarias | `tests/MovilidadUrbana.UnitTests` | 49 | Las reglas de dominio por sí solas, sin navegador ni servidor | ~27 ms |
| E2E | `tests/MovilidadUrbana.E2ETests` | 22 | El circuito completo con navegador real | 6–15 s según navegador |

Las E2E corren en **4 configuraciones** —chromium, firefox, webkit y `mobile-chrome` (chromium con
el descriptor de un Pixel 7)—: 88 ejecuciones en total.

## Pruebas unitarias

`ReglasDeLocalidadTests.cs` (25 casos) y `ReglasDeEncuestaTests.cs` (24 casos), casi todos
`[TestCase]` sobre los bordes de cada validación. Dos casos con nombre propio en localidades
—`MismaLocalidadCompara` y `LaProvinciaSeComparaDeFormaOrdinal`— y uno en encuesta —`TotalDePasos`—.

El proyecto referencia `MovilidadUrbana.Web.csproj`: prueba las reglas directamente, sin dobles.

```bash
dotnet test tests/MovilidadUrbana.UnitTests
```

## Pruebas E2E — el catálogo

Tres clases, cada una con su `[SetUp]` de navegación.

### NavegacionTests (4 casos)

| Caso |
| --- |
| La portada ofrece acceso a las dos pantallas |
| El menú marca la página activa |
| Desde la portada se llega al ABM y a la encuesta |
| Una dirección inexistente muestra la pantalla de no encontrado |

### LocalidadesTests (9 casos) — `[SetUp]` navega a `/localidades`

| Caso |
| --- |
| Muestra el listado sembrado |
| Rechaza el alta con campos inválidos |
| Da de alta una localidad y la persiste tras recargar |
| No permite duplicar nombre dentro de la misma provincia |
| Modifica una localidad existente |
| Cancelar la baja deja la tabla intacta |
| Confirmar la baja elimina la fila |
| Al borrar todas las localidades avisa que no hay datos |
| **Cada prueba trabaja sobre su propio conjunto de datos** |

El último es el que verifica el aislamiento por sesión descrito en
[03_Sesiones-Y-Persistencia.md](03_Sesiones-Y-Persistencia.md); es la garantía de que el paralelismo
es correcto y no una casualidad.

### EncuestaTests (9 casos) — `[SetUp]` navega a `/encuesta`

| Caso |
| --- |
| Arranca en el paso 1 con el anterior deshabilitado |
| El desplegable de localidades se alimenta del ABM |
| No avanza del paso 1 con datos inválidos |
| No avanza del paso 2 sin medios ni frecuencia |
| Permite volver atrás conservando lo cargado |
| La barra de progreso acompaña el avance |
| No finaliza con el paso 3 incompleto |
| Recorre los tres pasos, muestra el resumen y registra la respuesta |
| «Nueva encuesta» devuelve el asistente al paso 1 |

## La infraestructura de las E2E

`tests/MovilidadUrbana.E2ETests/Infraestructura/` — tres archivos que resuelven lo que el binding de
.NET no trae de fábrica.

### ServidorDeLaAplicacion.cs — `[SetUpFixture]`

Reemplaza la sección `webServer` que ofrece el runner de JavaScript. Ciclo:

1. **Asegura el navegador** llamando a `Microsoft.Playwright.Program.Main(["install", <navegador>])`
   —la vía documentada, `pwsh playwright.ps1 install`, exige PowerShell 7—. Instala solo el
   navegador de la corrida. Se apaga con `INSTALAR_NAVEGADORES=false`.
2. Si hay `URL_BASE`, la toma y **no levanta nada**.
3. Si no, fija `UrlBase = http://127.0.0.1:<PUERTO>` (por defecto **4173**).
4. **Publica** la aplicación con `dotnet publish -c Release -o publicacion` (salvo
   `PUBLICAR_ANTES_DE_PROBAR=false`). Lee las dos salidas del proceso en paralelo, porque esperar a
   una con el búfer de la otra lleno traba el proceso.
5. **Resuelve el arranque**: usa el apphost nativo si existe —`MovilidadUrbana.Web.exe` en Windows,
   sin extensión en Linux y macOS— y si no `dotnet MovilidadUrbana.Web.dll`.
6. Lanza el proceso con `WorkingDirectory` en la carpeta de publicación, `ASPNETCORE_URLS`,
   `ASPNETCORE_ENVIRONMENT=Production`, la cadena de conexión a `datos-e2e/movilidad.db` y
   `Logging__LogLevel__Default=Warning`.
7. **Espera a que Kestrel escuche** por TCP, hasta 90 segundos, abortando si el proceso murió solo.
8. `[OneTimeTearDown]` mata el árbol de procesos.

`RaizDelRepositorio` se ubica subiendo directorios hasta encontrar un `*.sln`; la usan la
publicación, la base de datos y las trazas.

El fixture vive en el namespace `MovilidadUrbana.E2ETests` **y no en uno anidado**: un
`[SetUpFixture]` cubre su propio namespace y los que cuelgan de él, nunca el de arriba.

### PruebaE2E.cs — clase base

Hereda de `PageTest`, que da a cada prueba una página nueva en su propio `BrowserContext`. Aporta:

| Miembro | Qué hace |
| --- | --- |
| `ContextOptions()` | Fija `BaseURL`, `Locale = es-AR` y `TimezoneId = America/Argentina/Buenos_Aires`. Con `EMULAR_MOVIL=true` parte del descriptor `Pixel 7`, y **falla explícitamente** si Playwright no lo conoce —para que la emulación no caiga en silencio a escritorio— |
| `[SetUp] EstrenarSesionAsync` | Agrega la cookie `sesion-movilidad` con un `Guid` propio y arranca la traza |
| `[TearDown] GuardarLaTrazaSiFalloAsync` | Guarda `resultados/trazas/<caso>.zip` solo si el caso falló; si pasó, la descarta |
| `IrAAsync(ruta)` | `GotoAsync` + espera de interactividad |
| `EsperarInteractivoAsync()` | Espera que `estado-app` tenga `data-interactivo="true"` |
| `IrPorMenuAsync(testid)` | Despliega el menú si el alternador es visible y después hace clic |

La traza se graba **siempre** y se conserva solo en los fallos: sin reintentos no existe el
`trace: 'on-first-retry'` del runner de JavaScript, y una traza que empieza cuando el caso ya falló
llega tarde. Cuesta unos 2 segundos sobre los 22 casos de chromium y se apaga con `TRAZAR=false`.
El `.zip` trae DOM paso a paso, red y consola; se abre con `playwright show-trace <archivo>` o en
[trace.playwright.dev](https://trace.playwright.dev).

### ParalelismoDelEnsamblado.cs

Una sola línea: `[assembly: Parallelizable(ParallelScope.Fixtures)]`. Las clases corren en paralelo
entre sí; los casos de cada clase, en secuencia. El motivo de no subir a `Children` está en
[08_Decisiones-Y-Trampas.md](08_Decisiones-Y-Trampas.md).

## pruebas.runsettings

| Sección | Valor |
| --- | --- |
| `Playwright/BrowserName` | `chromium` |
| `Playwright/ExpectTimeout` | 5000 ms |
| `Playwright/LaunchOptions/Headless` | `true` |
| `NUnit/NumberOfTestWorkers` | 4 |
| `RunConfiguration/ResultsDirectory` | `resultados` |

Es el reemplazo del bloque `projects` de un `playwright.config.js`: en el binding de .NET el
navegador es una **opción de la corrida**, no un proyecto del archivo de configuración. Se pisa
desde la línea de comandos con `-- Playwright.BrowserName=firefox`.

`NumberOfTestWorkers` es la **única** declaración del número de workers: el alcance vive en el
código y el número acá, para que no puedan divergir.

## Variables de entorno

| Variable | Efecto | Por defecto |
| --- | --- | --- |
| `URL_BASE` | Probar contra un entorno ya desplegado; no se levanta nada local | vacío |
| `PUERTO` | Puerto del servidor local | `4173` |
| `PUBLICAR_ANTES_DE_PROBAR` | `false` salta el `dotnet publish` del fixture (CI lo usa) | publicar |
| `INSTALAR_NAVEGADORES` | `false` salta la instalación del navegador | instalar |
| `CARPETA_APLICACION` | Dónde está la publicación | `<raíz>/publicacion` |
| `BASE_DE_DATOS` | Ruta del archivo SQLite | `<raíz>/datos-e2e/movilidad.db` |
| `CARPETA_RESULTADOS` | Dónde caen TRX y trazas | `<raíz>/resultados` |
| `EMULAR_MOVIL` | `true` activa el descriptor Pixel 7 | escritorio |
| `TRAZAR` | `false` apaga la grabación de traza | grabar |

## Cómo se corren

### Desde Visual Studio

Se abre `Lab-E2E.WebBlazor.sln` y el Explorador de pruebas descubre los 22 casos; se ejecutan o
depuran de a uno, con puntos de interrupción en el C# de la prueba. **No hay ningún paso previo**:
publicar la aplicación e instalar el navegador son responsabilidad del fixture. La primera corrida
tarda minutos porque baja el navegador. El navegador se elige en *Test > Configurar archivo de
configuración de ejecución* apuntando a `pruebas.runsettings`.

### Desde la línea de comandos

```bash
dotnet test tests/MovilidadUrbana.UnitTests
dotnet test tests/MovilidadUrbana.E2ETests --settings pruebas.runsettings
dotnet test tests/MovilidadUrbana.E2ETests --settings pruebas.runsettings -- Playwright.BrowserName=firefox
```

### Sin nada instalado, con Docker

`scripts/pruebas.sh` corre todo dentro de `mcr.microsoft.com/playwright:v1.62.1-noble` —que ya trae
las librerías de sistema— y le agrega el SDK de .NET en `.dotnet/` la primera vez. Los navegadores
quedan en `.navegadores/` y los paquetes en `.nuget/`; las tres carpetas están ignoradas por git.

```bash
scripts/pruebas.sh                     # chromium
scripts/pruebas.sh firefox
scripts/pruebas.sh webkit
EMULAR_MOVIL=true scripts/pruebas.sh   # chromium emulando un Pixel 7
URL_BASE=https://ejemplo.test scripts/pruebas.sh chromium
```

| Script | Para qué |
| --- | --- |
| `scripts/dotnet.sh` | Ejecuta el SDK dentro de `mcr.microsoft.com/dotnet/sdk:10.0` |
| `scripts/publicar.sh` | Publica **autocontenido** para `linux-x64` en `publicacion/`; es el artefacto que usa CI |
| `scripts/pruebas.sh` | Corre las E2E en la imagen de Playwright |

Los tres montan la raíz del repositorio en `/trabajo` y corren con el UID de quien invoca, para no
dejar archivos de root.
