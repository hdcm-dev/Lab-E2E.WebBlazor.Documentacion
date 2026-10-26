# 05 — Pruebas

> **Propósito**: mapa de las siete suites de prueba del laboratorio —qué verifica cada una, cuántos casos tiene (contados), cómo se corre en cada entorno, qué infraestructura levanta, qué variables de entorno la gobiernan, qué evidencia la respalda y qué queda sin cubrir—.
>
> **Fuente primaria**: `tests/*/` (los siete proyectos), `pruebas.runsettings`, `scripts/pruebas.sh`, `scripts/dotnet.sh`, `scripts/publicar.sh`, `.devcontainer/dev.sh` (`cmd_uitests`), `.github/workflows/*.yml` (solo los pasos de prueba), `evidencia/`, `README.md` («Cómo se corren», «Lo que cambia respecto del ejemplo estático», «Evidencia»), `CHANGELOG.md`.
>
> **Vigencia**: versión 3.1, generada el 2026-10-25 sobre el commit `8fb4c3a` (2026-09-18).
>
> **Vecinos**: el detalle de Hola Mundo y Login —superficie, guard, sus 11 casos— está en [10](10_Hola-Mundo-Y-Login.md); el arnés de la API y su contrato en [12](12_Api-REST.md); la app Android, su compilación y Appium en [13](13_App-Android.md); los `data-testid` de cada pantalla (incluidos los que ninguna prueba usa) en [04](04_Interfaz-Y-Pantallas.md); el aislamiento por sesión del lado de la app en [03](03_Sesiones-Y-Persistencia.md); los workflows enteros en [06](06_CI-Y-Workflows.md); las reglas que verifican las unitarias en [02](02_Dominio-Y-Reglas.md); el porqué de las trampas en [08](08_Decisiones-Y-Trampas.md).

---

## 1. Las siete suites, de un vistazo

Casos contados con `grep` de `[Test]` / `[TestCase]` sobre `tests/` en `8fb4c3a` (118 atributos: 72 `[Test]` + 46 `[TestCase]`; los 46 `[TestCase]` son todos de las unitarias, que suman 3 `[Test]` para llegar a 49).

| Suite (`tests/…`) | Casos | Qué ejercita | Herramienta | Contra qué | ¿En CI? |
| --- | ---: | --- | --- | --- | --- |
| `MovilidadUrbana.E2ETests` | **22** | Web de Movilidad Urbana por navegador | Playwright .NET 1.62.0 + NUnit | Binario **publicado** que levanta el propio fixture (`TestAppServer`) | Sí: `e2e.yml` (llamado por `ci.yml`; además `workflow_dispatch` y `schedule` propios); `ci.yml` además lista (`--list-tests`) |
| `MovilidadUrbana.UnitTests` | **49** | `LocalidadRules` y `EncuestaRules` de la web | NUnit | Referencia de proyecto a `src/MovilidadUrbana.Web` | Sí: job `compilacion` de `ci.yml` |
| `MovilidadUrbana.ApiWeb.Tests` | **13** | API REST en proceso | `Microsoft.AspNetCore.Mvc.Testing` 10.0.11 | `WebApplicationFactory<Program>` + SQLite temporal | Sí: `ci.yml` |
| `MovilidadUrbana.MAUI.Tests` | **18** | ViewModels de Android con capas reales | NUnit + EF Core SQLite + CommunityToolkit.Mvvm | Archivos **enlazados** de `src/MovilidadUrbana.MAUI/{Domain,Application,Infrastructure,Presentation}` | Sí: `ci.yml` y `android.yml` |
| `MovilidadUrbana.MAUI.UITests` | **5** | App Android instalada | Appium.WebDriver 8.0.0 (UIAutomator2) | Dispositivo o emulador visible por `adb` + servidor Appium (comentario del `.csproj`); la evidencia es un teléfono por USB | **No** (necesita dispositivo) |
| `WebBlazor.HolaMundo.E2ETests` | **1** | Superficie Hola Mundo | Playwright .NET 1.62.0 | URL fija `http://localhost:5027`, **sin fixture** | Sí: `e2e-holamundo.yml` |
| `WebBlazor.Login.E2ETests` | **10** | Acceso por cookies + guard + Hola Mundo protegido | Playwright .NET 1.62.0 | URL fija `http://localhost:5181`, **sin fixture** | Sí: `e2e-login.yml` |
| **Total** | **118** | | | | |

Todas: `net10.0`, `Microsoft.NET.Test.Sdk` 17.14.0, NUnit 4.3.2, NUnit.Analyzers 4.7.0, NUnit3TestAdapter 5.0.0 (los `.csproj`). Las tres E2E web suman `coverlet.collector` 6.0.4 (`tests/*E2ETests*.csproj`), que ningún workflow ni script invoca (no verificado que se use).

```
             por navegador / dispositivo           en proceso          sin host
  web        E2ETests(22) HolaMundo(1) Login(10)                       UnitTests(49)
  api                                              ApiWeb.Tests(13)
  android    UITests(5) (Appium + teléfono)                            MAUI.Tests(18)
```

---

## 2. `MovilidadUrbana.E2ETests` — 22 casos

### 2.1 Casos por clase

| Clase | # | Casos (método) |
| --- | ---: | --- |
| `NavigationTests` | 4 | `LaPortadaOfreceAccesoALasDosPantallas`, `ElMenuMarcaLaPaginaActiva`, `DesdeLaPortadaSeLlegaAlAbmYALaEncuesta`, `UnaDireccionInexistenteMuestraLaPantallaDeNoEncontrado` |
| `LocalidadesTests` | 9 | `MuestraElListadoSembrado`, `RechazaElAltaConCamposInvalidos`, `DaDeAltaUnaLocalidadYLaPersisteTrasRecargar`, `NoPermiteDuplicarNombreDentroDeLaMismaProvincia`, `ModificaUnaLocalidadExistente`, `CancelarLaBajaDejaLaTablaIntacta`, `ConfirmarLaBajaEliminaLaFila`, `AlBorrarTodasLasLocalidadesAvisaQueNoHayDatos`, `CadaPruebaTrabajaSobreSuPropioConjuntoDeDatos` |
| `EncuestaTests` | 9 | `ArrancaEnElPaso1ConElAnteriorDeshabilitado`, `ElDesplegableDeLocalidadesSeAlimentaDelAbm`, `NoAvanzaDelPaso1ConDatosInvalidos`, `NoAvanzaDelPaso2SinMediosNiFrecuencia`, `PermiteVolverAtrasConservandoLoCargado`, `ElIndicadorDePasosAcompanaElAvance`, `NoFinalizaConElPaso3Incompleto`, `RecorreLosTresPasosMuestraElResumenYRegistraLaRespuesta`, `NuevaEncuestaDevuelveElAsistenteAlPaso1` |

Rasgos que se repiten (leídos en los `.cs`):

- Localización solo por `GetByTestId` (más `[data-paso]`, `option` y `Filter(HasText/Visible)`).
- `LocalidadesTests.PresentacionDe(nombre)` busca la fila **o** la tarjeta visible (`[data-testid=fila], [data-testid=tarjeta]` + `Visible = true`): el mismo caso corre en escritorio y en móvil.
- Tres casos **recargan** la página (`ReloadAsync`) para distinguir lo persistido de lo que vive en el circuito.
- Formatos de `es-AR` afirmados: `89.000`, `300.000`, `12,5 km` (la prueba escribe `12.5`).
- Datos sembrados que asumen: 2 localidades, `Corrientes` y `Resistencia` (siembra en [03](03_Sesiones-Y-Persistencia.md)).

### 2.2 Infraestructura (`tests/MovilidadUrbana.E2ETests/Infrastructure/`)

| Archivo | Rol | Qué resuelve |
| --- | --- | --- |
| `TestAppServer.cs` | `[SetUpFixture]` de ensamblado | Instala el navegador, publica la app, la arranca, espera el puerto, la baja |
| `E2ETestBase.cs` | Base de toda clase (hereda `PageTest`) | Opciones de contexto, cookie de sesión por prueba, traza de fallidos, espera de interactividad |
| `AssemblyParallelism.cs` | `[assembly: Parallelizable(ParallelScope.Fixtures)]` | Clases en paralelo, casos de una clase en serie |

Los tres archivos viven en la carpeta `Infrastructure/` pero en el namespace raíz `MovilidadUrbana.E2ETests`: un `[SetUpFixture]` solo cubre su namespace y los de abajo (comentario de `TestAppServer.cs`; README §6).

**Ciclo de vida de una corrida**

```
OneTimeSetUp  TestAppServer.StartAsync
  ├─ AsegurarElNavegador        Microsoft.Playwright.Program.Main(["install", <BrowserName>])   (salvo INSTALAR_NAVEGADORES=false)
  ├─ URL_BASE definida? ── sí ─▶ UrlBase = URL_BASE; no se levanta nada
  ├─ UrlBase = http://127.0.0.1:<PUERTO|4173>
  ├─ HayQuePublicar? ─ sí ─▶ dotnet publish src/MovilidadUrbana.Web -c Release -o <publicacion/>   (dependiente del framework, sin RID)
  ├─ ResolverElArranque         apphost (MovilidadUrbana.Web[.exe]) o, si no, `dotnet MovilidadUrbana.Web.dll`
  ├─ Process.Start              WorkingDirectory = carpeta publicada (si no, wwwroot sale vacío)
  │     ASPNETCORE_URLS=UrlBase · ASPNETCORE_ENVIRONMENT=Production
  │     ConnectionStrings__BaseDeDatos="Data Source=<datos-e2e/movilidad.db>;Default Timeout=30"
  │     Logging__LogLevel__Default=Warning
  └─ EsperarAQueEscucheAsync    TCP a 127.0.0.1:<puerto>, cada 500 ms, hasta 90 s; si el proceso sale antes → excepción con su código
por caso   [SetUp] PageTest (contexto nuevo) → E2ETestBase.StartFreshSessionAsync
             ├─ cookie `sesion-movilidad` = Guid nuevo (aislamiento de datos)
             └─ Tracing.StartAsync (Screenshots, Snapshots, Sources)   (salvo TRAZAR=false)
           [SetUp] de la clase → IrAAsync("/localidades" | "/encuesta") → WaitForInteractiveAsync
                                 (NavigationTests no tiene [SetUp]: cada caso llama a IrAAsync)
           [TearDown] SaveTraceOnFailureAsync: si falló → <resultados>/trazas/<caso>.zip ; si pasó → se descarta
OneTimeTearDown  TestAppServer.TearDownFactory   Kill(entireProcessTree) + WaitForExit(10 s)
```

**Opciones de contexto** (`E2ETestBase.ContextOptions`): `BaseURL = TestAppServer.UrlBase`, `Locale = "es-AR"`, `TimezoneId = "America/Argentina/Buenos_Aires"`; con `EMULAR_MOVIL=true` parte del descriptor `Playwright.Devices["Pixel 7"]` y, si no existe, **lanza** en vez de caer en silencio a escritorio.

**Espera de interactividad**: `WaitForInteractiveAsync` espera `data-testid="estado-app"` con `data-interactivo="true"`; el testigo lo publica `MainLayout.razor` con `RendererInfo.IsInteractive` (`src/MovilidadUrbana.Web/Components/Layout/MainLayout.razor:22-23`). Hola Mundo y Login usan otra realización del testigo: ver [10](10_Hola-Mundo-Y-Login.md).

**Navegación por menú**: `IrPorMenuAsync(testid)` es un click directo sobre el enlace; ya no despliega `navbar-toggler` (README «Lo que cambió en las pruebas»).

---

## 3. `MovilidadUrbana.UnitTests` — 49 casos

| Clase | Método | Casos | Bordes notables |
| --- | --- | ---: | --- |
| `EncuestaRulesTests` | `NombreValido` | 5 | `"Ana"` válido (mínimo 3), `"An"` no |
| | `EdadValida` | 6 | 16 y 110 admitidos; 15 y 111 no |
| | `DistanciaValida` | 6 | `0` válido («se puede no viajar»); `-0.1`, `500.1` no |
| | `MinutosValidos` | 6 | `0` **no** válido; 1–600 |
| | `TotalDePasos` (`[Test]`) | 1 | `== 3` |
| `LocalidadRulesTests` | `NombreValido` | 6 | se recorta; `"  A  "` no |
| | `ProvinciaValida` | 4 | blancos y `null` no |
| | `CodigoPostalValido` | 8 | exactamente 4 dígitos; `34O0`, `W3400` no |
| | `HabitantesValidos` | 5 | mínimo 1 |
| | `MismaLocalidadCompara` (`[Test]`) | 1 | ignora mayúsculas y espacios del nombre; no cruza provincias |
| | `LaProvinciaSeComparaDeFormaOrdinal` (`[Test]`) | 1 | la provincia distingue mayúsculas |
| **Total** | | **49** | 24 + 25 |

Usa `[TestCase(..., ExpectedResult = ...)]` sobre métodos que devuelven `bool`. Referencia solo la web (`MovilidadUrbana.UnitTests.csproj` → `src/MovilidadUrbana.Web`); las reglas duplicadas en ApiWeb y MAUI no tienen unitarias propias (ver §11).

---

## 4. `MovilidadUrbana.ApiWeb.Tests` — 13 casos (detalle en [12](12_Api-REST.md))

| Clase | # | Casos |
| --- | ---: | --- |
| `LocalidadesTests` | 7 | `UnaSesionNuevaArrancaConLasSembradas`, `SinEncabezadoLaRespuestaDevuelveUno`, `DaDeAltaUnaLocalidad`, `RechazaElAltaConCamposInvalidos`, `NoPermiteDuplicar`, `ModificaYDaDeBaja`, `CadaSesionTieneSusDatos` |
| `EncuestasTests` | 4 | `RegistraUnaEncuestaCompleta`, `RechazaUnaEncuestaIncompleta`, `ValidaUnPasoPorSeparado`, `UnPasoInexistenteEs404` |
| `DocumentationTests` | 2 | `ElContratoOpenApiDeclaraLasRutas`, `ScalarSeSirveYApuntaAlContrato` |

Arnés: `ApiWebApplicationFactory` (`UseEnvironment("Development")`, base `movilidad-api-<guid>.db` en el temporal; al disponer borra el archivo y sus `-wal`/`-shm`). Cada clase la crea en `[OneTimeSetUp] SetUpFactory` y la dispone en `[OneTimeTearDown] TearDownFactory`.

---

## 5. `MovilidadUrbana.MAUI.Tests` — 18 casos (detalle en [13](13_App-Android.md))

| Clase | # | Casos |
| --- | ---: | --- |
| `LocalidadesViewModelTests` | 5 | `CargaLasSembradasOrdenadas`, `FiltrarSinCoincidenciasYLimpiar`, `FiltraPorProvinciaYPorCodigoPostal`, `SinLocalidadesEsVacio`, `AbreElEditor` |
| `LocalidadEditorViewModelTests` | 6 | `GuardarInvalidoMuestraErrores`, `CorregirUnCampoBorraSuError`, `GuardarNuevaAvisaYVuelve`, `ModificarActualiza`, `EliminarCanceladoNoBorra`, `EliminarConfirmadoBorra` |
| `EncuestaViewModelTests` | 7 | `CargaLasLocalidadesDelAbm`, `NoAvanzaDelPaso1ConDatosInvalidos`, `CorregirElPaso2BorraSusErrores`, `VolverAtrasConservaLoCargado`, `RecorreYRegistra`, `NoRegistraConElPaso3Incompleto`, `NuevaEncuestaReinicia` |

Arnés: `TestEnvironment` (un «dispositivo nuevo» por caso: fija cultura `es-AR`, compone `AddInfrastructure` + `AddApplication` sobre `movilidad-maui-<guid>.db`, corre `DatabaseInitializer.Initialize`), con dobles `FakeNavigationService` y `FakeAlertService`. El `.csproj` compila como `<Compile Include … LinkBase>` las cuatro carpetas de capa porque el proyecto `net10.0-android` no se puede referenciar sin el workload.

---

## 6. `MovilidadUrbana.MAUI.UITests` — 5 casos (detalle en [13](13_App-Android.md))

| Clase | # | Casos |
| --- | ---: | --- |
| `LocalidadesTests` | 3 | `FiltrarSinCoincidenciasYLimpiar`, `AltaInvalidaMuestraErrores`, `AltaEdicionYBaja` |
| `EncuestaTests` | 2 | `NoAvanzaConElPaso1Vacio`, `RecorreRegistraYMuestraElResumen` |

| Pieza | Qué hace |
| --- | --- |
| `Infrastructure/AppiumSession.cs` (`[SetUpFixture]`, namespace raíz) | Una sesión `AndroidDriver` por corrida: `APPIUM_URL` (def. `http://127.0.0.1:4723`), `NoReset=true`, paquete `ar.lab.movilidadurbana`, `ActivateApp` y reintento hasta 120 s de la primera pantalla |
| `Infrastructure/ScreenTestBase.cs` | `FindById` (`MobileBy.Id` = `AutomationId`), esperas por condición de 60 s cada 500 ms, `TypeText` que cierra el teclado, `Pick`, `ScrollIntoView` con `UiScrollable`, `GoToTab` que vuelve atrás si quedó una página apilada, `Capture` de evidencia |
| `Infrastructure/AssemblyParallelism.cs` | `[assembly: NonParallelizable]`: un dispositivo es una sola pantalla |

La vía prevista (comentario del `.csproj`: «se corren desde el devcontainer (`dev.sh uitests`), no en CI») es `.devcontainer/dev.sh uitests`: levanta `appium` desprendido dentro del contenedor si `:4723/status` no responde (espera 30 s) y ejecuta `dotnet test tests/MovilidadUrbana.MAUI.UITests -c Release --logger 'trx;LogFileName=uitests.trx' --results-directory tests/MovilidadUrbana.MAUI.UITests/resultados` (`.devcontainer/dev.sh:84-94`).

---

## 7. Cómo se corren

### 7.1 Por entorno

| Entorno | Movilidad E2E | HolaMundo / Login | Unit / API / MAUI.Tests | UITests |
| --- | --- | --- | --- | --- |
| **Visual Studio** (Explorador de pruebas) | Directo: el fixture publica e instala | Antes arrancar la web con su perfil `http` (5027 / 5181) | Directo | No |
| **CLI con SDK** | `dotnet test tests/MovilidadUrbana.E2ETests --settings pruebas.runsettings [-- Playwright.BrowserName=firefox]` | Ídem, con la app ya escuchando | `dotnet test tests/<suite>` | No |
| **Docker, sin nada instalado** | `scripts/pruebas.sh [chromium\|firefox\|webkit]` | `PROYECTO=holamundo\|login scripts/pruebas.sh` (el script levanta la app) | `scripts/dotnet.sh dotnet test tests/<suite>` | No |
| **Devcontainer Android** | — | — | — | `.devcontainer/dev.sh uitests` |
| **CI** | `e2e.yml` (matriz de configuraciones) | `e2e-holamundo.yml`, `e2e-login.yml` | `ci.yml` (y `android.yml` para MAUI.Tests) | — |

Fuentes: README «Cómo se corren»; `scripts/pruebas.sh`; `.github/workflows/*.yml`. La ejecución desde Visual Studio **no está verificada**: el README declara que no hay Windows ni Visual Studio en la máquina de evidencia.

### 7.2 `scripts/pruebas.sh`

Imagen `mcr.microsoft.com/playwright:v<VERSION_PLAYWRIGHT|1.62.1>-noble` (o `IMAGEN_E2E`), `--ipc=host`, repo montado en `/trabajo`, SDK 10.0 instalado la primera vez en `.dotnet/` y navegadores en `.navegadores/` (ambos ignorados por git).

```
PROYECTO=movilidad (def.) → build tests Debug → dotnet test --no-build --settings pruebas.runsettings -- Playwright.BrowserName=$NAVEGADOR
PROYECTO=holamundo|login  → build tests Debug → instalar navegador con el CLI del paquete (.playwright/node + cli.js install)
                          → build app Debug → dotnet run --no-build --no-launch-profile en URL_APP (ASPNETCORE_ENVIRONMENT=Development)
                          → curl a URL_APP/ hasta 60 s → dotnet test …  ×REPETIR → «Resumen: N de M corridas en rojo»
```

| `PROYECTO` | Pruebas | App que levanta | `URL_APP` |
| --- | --- | --- | --- |
| `movilidad` | `tests/MovilidadUrbana.E2ETests` | ninguna (la levanta el fixture) | — |
| `holamundo` | `tests/WebBlazor.HolaMundo.E2ETests` | `src/WebBlazor.HolaMundo` | `http://localhost:5027` |
| `login` | `tests/WebBlazor.Login.E2ETests` | `src/WebBlazor.Login` | `http://localhost:5181` |

### 7.3 `pruebas.runsettings` (raíz)

| Clave | Valor | Nota |
| --- | --- | --- |
| `Playwright/BrowserName` | `chromium` | Se pisa con `-- Playwright.BrowserName=<x>` |
| `Playwright/ExpectTimeout` | `5000` | ms |
| `Playwright/LaunchOptions/Headless` | `true` | |
| `NUnit/NumberOfTestWorkers` | `4` | Única fuente del número de workers (el alcance va en código) |
| `RunConfiguration/ResultsDirectory` | `resultados` | Misma carpeta que usan las trazas |

Lo usan las tres suites Playwright cuando se pasa `--settings` (script y los tres workflows E2E). Las otras cuatro suites no lo reciben.

### 7.4 Paralelismo

| Suite | Declaración | Efecto |
| --- | --- | --- |
| `MovilidadUrbana.E2ETests` | `[assembly: Parallelizable(ParallelScope.Fixtures)]` | 3 clases en paralelo; `ParallelScope.Children` rompe Playwright (`The given key 'Browser' was not present in the dictionary`) |
| `WebBlazor.HolaMundo.E2ETests` | `[Parallelizable(ParallelScope.Self)]` en la clase | Una sola clase |
| `WebBlazor.Login.E2ETests` | `[Parallelizable(ParallelScope.Self)]` en cada clase | Sus 2 clases pueden correr a la vez |
| `MovilidadUrbana.MAUI.UITests` | `[assembly: NonParallelizable]` | En serie |
| Unit / API / MAUI.Tests | sin declaración | Por defecto de NUnit, sin paralelismo (no se pidió) |

---

## 8. Variables de entorno

| Variable | Quién la lee | Defecto | Efecto |
| --- | --- | --- | --- |
| `URL_BASE` | `TestAppServer` | vacío | Prueba contra un entorno desplegado; no publica ni levanta nada. Solo Movilidad (HolaMundo/Login tienen la URL escrita) |
| `PUERTO` | `TestAppServer` | `4173` | Puerto local de la app bajo prueba (`http://127.0.0.1:<puerto>`) |
| `PUBLICAR_ANTES_DE_PROBAR` | `TestAppServer` | publica | `false` = usar lo que haya en la carpeta (CI lo fija en `e2e.yml`) |
| `CARPETA_APLICACION` | `TestAppServer` | `<raíz>/publicacion` | Carpeta de la publicación |
| `INSTALAR_NAVEGADORES` | `TestAppServer` | instala | `false` = no llamar al instalador |
| `BASE_DE_DATOS` | `TestAppServer` | `<raíz>/datos-e2e/movilidad.db` | Archivo SQLite de la app bajo prueba |
| `TRAZAR` | `E2ETestBase` | graba | `false` = sin traza |
| `CARPETA_RESULTADOS` | `E2ETestBase` | `<raíz>/resultados` | Raíz de `trazas/` |
| `EMULAR_MOVIL` | `E2ETestBase` | `false` | `true` = descriptor Pixel 7 (`mobile-chrome` en CI) |
| `APPIUM_URL` | `AppiumSession` | `http://127.0.0.1:4723` | Servidor Appium |
| `PROYECTO`, `NAVEGADOR` (o `$1`), `REPETIR` | `scripts/pruebas.sh` | `movilidad`, `chromium`, `1` | Suite, navegador, repeticiones |
| `VERSION_PLAYWRIGHT`, `IMAGEN_E2E` | `scripts/pruebas.sh` | `1.62.1`, imagen noble | Imagen del contenedor |
| `DOTNET_USE_POLLING_FILE_WATCHER` | `scripts/pruebas.sh` (pasa al contenedor) | vacío | `1` esquiva el agotamiento de `inotify` (app sale con código 134) |
| `IMAGEN_SDK` | `scripts/dotnet.sh` | `mcr.microsoft.com/dotnet/sdk:10.0` | Imagen del SDK |

`<raíz>` = primer directorio hacia arriba desde `AppContext.BaseDirectory` que contiene un `*.sln` (`TestAppServer.UbicarLaRaizDelRepositorio`).

**Hueco del script** (leído en `scripts/pruebas.sh`): el `docker run` pasa al contenedor `EMULAR_MOVIL`, `URL_BASE`, `CARPETA_APLICACION`, `PUBLICAR_ANTES_DE_PROBAR` y `DOTNET_USE_POLLING_FILE_WATCHER`, pero **no** `TRAZAR`, `PUERTO`, `BASE_DE_DATOS`, `INSTALAR_NAVEGADORES` ni `CARPETA_RESULTADOS`: definidas en el host, no llegan a la prueba.

---

## 9. Salidas de una corrida

| Salida | Dónde | Quién la produce |
| --- | --- | --- |
| Publicación de la web | `publicacion/` (ignorada) | Fixture (dependiente del framework) o `scripts/publicar.sh` (autocontenida `linux-x64`) |
| Base de la app bajo prueba | `datos-e2e/movilidad.db` (ignorada) | App levantada por el fixture |
| TRX | `resultados/` (o `--results-directory`) | `dotnet test --logger trx` en CI |
| Trazas de fallidos | `resultados/trazas/<caso>.zip` | `E2ETestBase`; se abren con `playwright show-trace` o trace.playwright.dev |
| Capturas Appium | `<WorkDirectory>/capturas/<nombre>.png` + adjunto del TestContext | `ScreenTestBase.Capture` |
| TRX Appium | `tests/MovilidadUrbana.MAUI.UITests/resultados/uitests.trx` (ignorada) | `dev.sh uitests` |

---

## 10. Evidencia de corridas (`evidencia/`)

| Carpeta | Suite | Qué registra |
| --- | --- | --- |
| `2026-09-01-aplicacion-template/` | HolaMundo, Login | `verificar.mjs` (Playwright JS ad hoc, no es una suite): 10 comprobaciones OK y 12 capturas — detalle en [10](10_Hola-Mundo-Y-Login.md) §5.5 |
| `2026-09-03-testigo-de-hidratacion/` | HolaMundo, Login | Corridas repetidas en verde tras el testigo de hidratación — detalle en [10](10_Hola-Mundo-Y-Login.md) §5.5 |
| `2026-09-12-capas-y-api/` | E2E, API | `movilidad-e2e-tras-extraer-capas.log` 22/22; `api-tests.log` 13/13; `api-falsificacion-201.log` 1 rojo de 11 |
| `2026-09-12-unificacion/` | las tres E2E | HolaMundo 3/3 y Login 3/3 con `REPETIR=3`; Movilidad 22/22; **falsificación**: sin app, HolaMundo 1 rojo (`ERR_CONNECTION_REFUSED`) y Login 10 rojos; Login como `e2e-login.yml` (autocontenido, Production) 10/10 en chromium y firefox |
| `2026-09-12-renombre/` | HolaMundo, Login | Tras quitar `E2E.Base`: 1/1 y 10/10 |
| `2026-09-12-maui/` | — (manual) | Recorrido a mano en el moto e6 play, capturas e índice (ver [13](13_App-Android.md)) |
| `2026-09-13-uitests/` | UITests | 5/5 en 3 min 21 s y 5/5 en 3 min 5 s; falsificación 1 rojo de 5 |

Corridas que solo figuran en texto (README «Evidencia», CHANGELOG), sin log en `evidencia/`: 22 × 4 configuraciones (2026-08-23 y 2026-09-04), 49 unitarias (2026-08-24/09-04/09-12), 18 de MAUI.Tests (2026-09-12) y el verde completo tras el renombre (CHANGELOG 2026-09-18). **No verificables** desde el repositorio.

Los logs de 2026-09-03 y de `2026-09-12-unificacion/` nombran los ensamblados viejos `WebBlazor.E2E.Base.*`: son anteriores a `e0f3e9d` y el CHANGELOG los declara históricos. `falsificacion.log` de UITests muestra el helper `Texto(...)`, nombre anterior a `GetText` (946d023).

---

## 11. Deuda de cobertura

| Hueco | Evidencia del hueco | Estado |
| --- | --- | --- |
| Ninguna E2E navega a `/encuesta/2` ni `/encuesta/3`: el `Math.Min(pedido, _pasoMaximoAlcanzado)` que impide saltear pasos no está cubierto | CHANGELOG 2026-09-04 «Encontrado, no resuelto»; `grep '"/encuesta' tests/` solo da `/encuesta` | Abierto |
| El `catch` de `FinishAsync` (`Encuesta.razor.cs:118`) y `boton-procesando` (`Wizard.razor:56`) nunca se ejercitan; falta un punto de inyección de fallos | CHANGELOG 2026-09-04; `grep boton-procesando tests/` vacío | Abierto, con motivo declarado |
| La barra de filtros del ABM web (`campo-buscar`, `filtro-provincia`) y el estado `FiltradoSinResultados` de la web no tienen caso E2E (sí lo tienen MAUI.Tests y UITests) | `grep -i 'buscar\|filtro' tests/MovilidadUrbana.E2ETests` vacío | Abierto (no declarado en README/CHANGELOG) |
| `boton-cancelar` (cancelar edición del ABM, `Localidades.razor:97`) sin caso | `grep boton-cancelar tests/` solo da `boton-cancelar-dialogo` (`LocalidadesTests.cs:117`), que es otro control | Abierto (no declarado) |
| Las reglas de `MovilidadUrbana.ApiWeb` y `MovilidadUrbana.MAUI` (copias propias) no tienen unitarias; solo las de la web | `UnitTests.csproj` referencia solo la web | Implícito en el diseño de apps independientes |
| Hola Mundo: solo el estado `ConDatos`; `ErrorDeEntrada`, `Enviando` y vacío no tienen caso en la suite | `HolaMundoE2ETests.cs` (1 caso); vacío y error de entrada se miraron una vez con `verificar.mjs` (2026-09-01); `Enviando`, ni eso | Ver [10](10_Hola-Mundo-Y-Login.md) |
| Login: `SesionRequerida`, `DatosIncompletos`, `/Error` y `/not-found` sin caso | Ver [10](10_Hola-Mundo-Y-Login.md) | |
| UITests fuera de CI | `.csproj` y README: necesitan dispositivo | Por diseño |
| Ejecución desde Visual Studio y comportamiento real de los workflows | README «Evidencia»: «no se verificó» | Las corridas observadas de GitHub Actions están en [06](06_CI-Y-Workflows.md) |

Inventario completo de `data-testid` declarados y no usados: [04](04_Interfaz-Y-Pantallas.md).

---

## 12. Trampas de prueba ya pagadas (resumen; el porqué en [08](08_Decisiones-Y-Trampas.md))

| Síntoma | Causa | Dónde quedó resuelto |
| --- | --- | --- |
| Click perdido, intermitencia en máquinas cargadas | HTML prerenderizado antes del circuito | Testigo `estado-app` + `WaitForInteractiveAsync` |
| URL base vacía, Playwright se queja de la cookie | `[SetUpFixture]` en namespace hijo | Fixture en el namespace raíz (también en UITests) |
| `blazor.web.js` llega con `200` y `Content-Length: 0` | Directorio actual distinto de la publicación | `WorkingDirectory = carpeta` |
| Descubrimiento falla en Windows | Apphost sin `.exe` | `NombreDelApphost` según SO |
| Todas mueren en `OneTimeSetUp` en VS | Publicar atado al build | Publicar en el fixture |
| Formulario «completo» que la validación rechaza | `FillAsync` dispara `input`, `@bind` escucha `change` | `@bind:event="oninput"` |
| App termina con código 134 antes de escuchar | `inotify` agotado en la máquina | `DOTNET_USE_POLLING_FILE_WATCHER=1` |
| Sesión Appium falla al arrancar | Hilo principal ocupado ~21 s tras instalar en Debug | Reintento de la primera pantalla (CHANGELOG 2026-09-18) |

---

## 13. Rastros de nombres viejos en el dominio de pruebas

Previos al renombre `946d023` / `e9dea2a`, todavía en el árbol de `8fb4c3a`. Los que nombran archivos o clases de prueba fuera de `tests/` (`ParalelismoDelEnsamblado.cs` en `pruebas.runsettings`, `PruebaDeSuperficie.UrlBase` en `scripts/pruebas.sh` y `e2e-login.yml`, `…E2ETests.Infraestructura` en el `README.md`, `Paginas/, Servicios/, Controles/` en el `.csproj` de MAUI.Tests) están en [01](01_Arquitectura.md) §8.3. Los de adentro de las suites:

| Dónde | Rastro | Nombre vigente |
| --- | --- | --- |
| `TestAppServer.PublicarLaAplicacionAsync(string navTarget)` | parámetro `destino` traducido como `navTarget` (no es navegación: es la carpeta de salida) | — (deriva semántica del renombre) |
| `TestAppServer.TearDownFactory` | antes `Bajar`, igual que en las clases de la API (que también pasaron a `TearDownFactory`, `git show 946d023`); acá no hay fábrica, se mata un proceso | — (deriva del renombre) |
| `TestEnvironment.Navegador`, `.Avisos`; campo `_entorno` | propiedades en español sobre dobles en inglés | mezcla tolerada |
| `EncuestaRulesTests.TotalDePasos` `[Description]` | «barra de progreso», retirada el 2026-09-04 | indicador de pasos |
| `CHANGELOG.md` 2026-08-30 | `PruebaE2E`, `ServidorDeLaAplicacion` | `E2ETestBase`, `TestAppServer` (histórico) |

---

## 14. Desfasajes documentales del dominio

| Afirmación | Dónde | Lo que hay |
| --- | --- | --- |
| «descubre las pruebas de los cinco proyectos —33 E2E…, 49 unitarios y 13 de la API—» | README «Desde Visual Studio» | La solución tiene **siete** proyectos de prueba; faltan MAUI.Tests (18) y UITests (5) |
| «la API 11/11» en `evidencia/2026-09-12-capas-y-api/` | CHANGELOG 2026-09-12 | `api-tests.log` muestra 13/13 (la falsificación sí es sobre 11) |
| `corrida-b-5-de-5.trx` listado como evidencia | `evidencia/2026-09-13-uitests/README.md` | Existe en disco pero `*.trx` está en `.gitignore` (línea 67): **no versionado**; la guía `Test-Guide/Pruebas-De-Interfaz-Por-Pantalla.md` §5.5 también lo da por versionado |
| Hola Mundo y Login «usan el mismo [navegador] que instala la primera corrida de Movilidad» | README «Desde Visual Studio» | Habla de VS (no verificado: no hay VS en la máquina de evidencia); `pruebas.sh` y los workflows los instalan con el CLI del paquete |
| Movilidad Urbana «levanta la aplicación desde su propio fixture, en un puerto libre» | comentario de `scripts/pruebas.sh:18-19` | `TestAppServer` usa `PUERTO` o, por defecto, `4173` fijo; no busca puerto libre |
