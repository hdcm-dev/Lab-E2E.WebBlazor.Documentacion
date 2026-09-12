# 05 — Pruebas

> **Propósito**: registrar qué cubre cada suite, cómo se ejecutan, qué hace la infraestructura de
> las E2E y qué variables de entorno la gobiernan.
> **Fuente primaria**: `tests/`, `pruebas.runsettings`, `scripts/pruebas.sh` y
> `evidencia/2026-09-12-unificacion/`.
> **Vigencia**: 2026-09-12, commit `06528d3`.

## Las cuatro suites

| Suite | Proyecto | Casos | Qué verifica | Quién levanta la aplicación |
| --- | --- | --- | --- | --- |
| Unitarias | `tests/MovilidadUrbana.UnitTests` | 49 | Las reglas de dominio de Movilidad Urbana, sin navegador ni servidor | Nadie: no hace falta |
| E2E | `tests/MovilidadUrbana.E2ETests` | 22 | El circuito completo de Movilidad Urbana | **Su fixture**, que publica y arranca la aplicación |
| E2E | `tests/WebBlazor.Login.E2ETests` | 10 | El acceso, el guard y la superficie protegida | **Quien corre la prueba**: URL fija `http://localhost:5181` |
| E2E | `tests/WebBlazor.HolaMundo.E2ETests` | 1 | La superficie Hola Mundo | **Quien corre la prueba**: URL fija `http://localhost:5027` |

Conteo verificado el 2026-09-12 contando los atributos `[Test]` y `[TestCase]` de cada proyecto;
coincide con los `--list-tests` que registra el `CHANGELOG.md`. Los tres proyectos E2E usan
`Microsoft.Playwright.NUnit` **1.62.0**, así que comparten la build de navegadores.

La diferencia en quién levanta la aplicación **es a propósito**: las tres aplicaciones escalonan la
complejidad del laboratorio — ver [00](00_MASTER-INDEX.md).

## Pruebas unitarias

`ReglasDeLocalidadTests.cs` (25 casos) y `ReglasDeEncuestaTests.cs` (24 casos), casi todos
`[TestCase]` sobre los bordes de cada validación. El proyecto referencia `MovilidadUrbana.Web.csproj`:
prueba las reglas directamente, sin dobles.

## Movilidad Urbana — el catálogo

Tres clases, cada una con su `[SetUp]` de navegación.

### NavegacionTests (4)

La portada ofrece acceso a las dos pantallas · el menú marca la página activa · desde la portada se
llega al ABM y a la encuesta · una dirección inexistente muestra la pantalla de no encontrado.

### LocalidadesTests (9) — `[SetUp] AbrirElAbmAsync` navega a `/localidades`

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

El último verifica el aislamiento por sesión de
[03_Sesiones-Y-Persistencia.md](03_Sesiones-Y-Persistencia.md): es la garantía de que el paralelismo es
correcto y no una casualidad.

### EncuestaTests (9) — `[SetUp] AbrirLaEncuestaAsync` navega a `/encuesta`

| Caso |
| --- |
| Arranca en el paso 1 con el anterior deshabilitado |
| El desplegable de localidades se alimenta del ABM |
| No avanza del paso 1 con datos inválidos |
| No avanza del paso 2 sin medios ni frecuencia |
| Permite volver atrás conservando lo cargado |
| El indicador de pasos acompaña el avance |
| No finaliza con el paso 3 incompleto |
| Recorre los tres pasos, muestra el resumen y registra la respuesta |
| «Nueva encuesta» devuelve el asistente al paso 1 |

Con el template (2026-09-04) cuatro puntos se adaptaron sin aflojar ninguna verificación:
`IrPorMenuAsync` ya no despliega un menú, el diálogo se verifica por sus identificadores propios, el
avance del asistente se verifica sobre el indicador de pasos, y las acciones de fila se buscan en la
presentación visible — detalle en [04](04_Interfaz-Y-Pantallas.md#identificadores-que-cambiaron).

**Sin caso de prueba** (registrado el 2026-09-04 en `CHANGELOG.md`): navegar directo a
`/encuesta/2` o `/encuesta/3` —el `Math.Min` que impide saltear— y el `catch` de `FinalizarAsync`
con `boton-procesando`, que exigiría un punto de inyección de fallo que la aplicación no tiene.

## Movilidad Urbana — la infraestructura

`tests/MovilidadUrbana.E2ETests/Infraestructura/`.

### ServidorDeLaAplicacion.cs — `[SetUpFixture]`

Reemplaza la sección `webServer` del runner de JavaScript:

1. **Asegura el navegador** con `Microsoft.Playwright.Program.Main(["install", <navegador>])`. Se
   apaga con `INSTALAR_NAVEGADORES=false`.
2. Si hay `URL_BASE`, la toma y **no levanta nada**.
3. Si no, fija `UrlBase = http://127.0.0.1:<PUERTO>` (por defecto **4173**).
4. **Publica** con `dotnet publish <proyecto> --configuration Release --output publicacion`
   —dependiente del framework, sin RID—, salvo `PUBLICAR_ANTES_DE_PROBAR=false`; lee las dos salidas
   del proceso en paralelo.
5. Usa el apphost nativo si existe (`MovilidadUrbana.Web.exe` en Windows, sin extensión en el resto),
   o `dotnet MovilidadUrbana.Web.dll`.
6. Lanza el proceso **desde la carpeta publicada** (`WorkingDirectory`) con `ASPNETCORE_URLS`,
   `ASPNETCORE_ENVIRONMENT=Production`, la base `datos-e2e/movilidad.db` y
   `Logging__LogLevel__Default=Warning`.
7. **Espera a que Kestrel escuche** por TCP, hasta 90 segundos.
8. `[OneTimeTearDown]` mata el árbol de procesos (`Kill(entireProcessTree: true)`).

Vive en el namespace `MovilidadUrbana.E2ETests` y no en uno anidado: un `[SetUpFixture]` cubre su
propio namespace y los que cuelgan de él, nunca el de arriba. Expone `RaizDelRepositorio`, que usan
la publicación, la base de datos y las trazas.

### PruebaE2E.cs — clase base

| Miembro | Qué hace |
| --- | --- |
| `ContextOptions()` | `BaseURL`, `Locale = es-AR`, `TimezoneId = America/Argentina/Buenos_Aires`. Con `EMULAR_MOVIL=true` parte del descriptor `Pixel 7` y **lanza `InvalidOperationException`** si Playwright no lo conoce |
| `[SetUp] EstrenarSesionAsync` | Cookie `sesion-movilidad` con un `Guid` propio, y arranca la traza |
| `[TearDown] GuardarLaTrazaSiFalloAsync` | Guarda `resultados/trazas/<caso>.zip` solo si el caso falló; si no, detiene la traza sin archivo |
| `IrAAsync(ruta)` | `GotoAsync` + espera de interactividad |
| `EsperarInteractivoAsync()` | Espera que `estado-app` tenga `data-interactivo="true"` |
| `IrPorMenuAsync(testid)` | `GetByTestId(testid).ClickAsync()`: desde el template no hay menú que desplegar |

La traza se graba **siempre** y se conserva solo en los fallos. Cuesta unos 2 segundos sobre los 22
casos de chromium y se apaga con `TRAZAR=false`.

### ParalelismoDelEnsamblado.cs

`[assembly: Parallelizable(ParallelScope.Fixtures)]`: las clases corren en paralelo entre sí; los
casos de cada clase, en secuencia. Ver [08](08_Decisiones-Y-Trampas.md).

## Hola Mundo y Login — pruebas sin fixture

Ninguno de los dos proyectos levanta la aplicación ni instala el navegador: prueban por HTTP contra
una URL escrita en el código. El detalle de las superficies está en [10](10_Hola-Mundo-Y-Login.md).

| Proyecto | Pieza | Qué hace |
| --- | --- | --- |
| HolaMundo | `HolaMundoE2ETests` : `PageTest` | `[SetUp]` navega a `http://localhost:5027/HolaMundo` y espera `estado-app`; `[Test] MostrarMensaje` llena la frase, la muestra y afirma `campo-mensaje` |
| Login | `PruebaDeSuperficie` : `PageTest` (base abstracta) | `UrlBase = http://localhost:5181`; credencial `admin`/`admin`; `IngresarAsync()` por la superficie; `EsperarCircuitoAbiertoAsync()` |
| Login | `LoginE2ETests` (9) | El acceso y el guard — lista abajo |
| Login | `HolaMundoE2ETest` (1) | Ingresa, abre `/HolaMundo`, espera el circuito y ejercita la superficie protegida |

`LoginE2ETests`:

| Caso | Método |
| --- | --- |
| Una credencial admitida abre la superficie de trabajo | `IngresoAceptadoAbreLaSuperficieDeTrabajo` |
| Aceptado el ingreso, se vuelve al destino que se había pedido | `IngresoAceptadoVuelveAlDestinoPedido` |
| Un destino externo no se honra: el ingreso no es una redirección abierta | `UnDestinoExternoNoSeHonra` |
| Una credencial rechazada devuelve al acceso con el mensaje del catálogo | `IngresoRechazadoVuelveAlAccesoConElMensajeDelCatalogo` |
| El rechazo no dice cuál de los dos campos falló | `ElRechazoNoDistingueQueCampoFallo` |
| Lo que falta no se intenta: el navegador retiene el envío incompleto | `UnEnvioIncompletoNoSale` |
| Sin sesión, la superficie protegida devuelve al acceso conservando el destino | `LaSuperficieProtegidaExigeSesion` |
| El destino sobrevive al rebote: se entra donde se quería entrar | `ElDestinoSobreviveAlRebote` |
| Cerrar la sesión devuelve al acceso y revoca el paso | `CerrarLaSesionRevocaElPaso` |

**Quien corre estas pruebas tiene que levantar la aplicación** en la URL que tienen escrita:
`scripts/pruebas.sh` con `PROYECTO`, los workflows `e2e-holamundo.yml` y `e2e-login.yml`, o a mano
con el perfil `http` de la aplicación. Cambiar la URL de un lado obliga a cambiarla del otro.

## pruebas.runsettings

Lo usan los tres proyectos E2E.

| Sección | Valor |
| --- | --- |
| `Playwright/BrowserName` | `chromium` |
| `Playwright/ExpectTimeout` | 5000 ms |
| `Playwright/LaunchOptions/Headless` | `true` |
| `NUnit/NumberOfTestWorkers` | 4 |
| `RunConfiguration/ResultsDirectory` | `resultados` |

El navegador es una **opción de la corrida**: se pisa con `-- Playwright.BrowserName=firefox`.
`NumberOfTestWorkers` es la única declaración del número de workers.

## Variables de entorno

Las lee **solo la infraestructura de Movilidad Urbana**; las pruebas de Hola Mundo y Login no leen
ninguna.

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

`Lab-E2E.WebBlazor.sln` descubre las pruebas de los cuatro proyectos: 33 casos E2E y 49 unitarios.
Movilidad Urbana **no tiene paso previo**: publicar e instalar el navegador son responsabilidad del
fixture. **Hola Mundo y Login sí**: hay que arrancar antes la aplicación con su perfil `http`, y usan
el navegador que instala la primera corrida de Movilidad Urbana. **No verificado en Windows.**

### Desde la línea de comandos

```bash
dotnet test tests/MovilidadUrbana.UnitTests
dotnet test tests/MovilidadUrbana.E2ETests --settings pruebas.runsettings
dotnet test tests/MovilidadUrbana.E2ETests --settings pruebas.runsettings -- Playwright.BrowserName=firefox
# Hola Mundo y Login, con la aplicación ya levantada en su URL:
dotnet test tests/WebBlazor.Login.E2ETests --settings pruebas.runsettings
```

### Sin nada instalado, con Docker

`scripts/pruebas.sh` corre dentro de `mcr.microsoft.com/playwright:v1.62.1-noble`
(`VERSION_PLAYWRIGHT`, `IMAGEN_E2E`) con `--ipc=host` y el usuario actual, y agrega el SDK de .NET
en `.dotnet/` la primera vez. Los navegadores quedan en `.navegadores/`.

```bash
scripts/pruebas.sh                              # Movilidad Urbana, chromium
scripts/pruebas.sh firefox
EMULAR_MOVIL=true scripts/pruebas.sh            # chromium emulando un Pixel 7
URL_BASE=https://ejemplo.test scripts/pruebas.sh chromium
PROYECTO=holamundo scripts/pruebas.sh           # levanta Hola Mundo en su URL y prueba
PROYECTO=login scripts/pruebas.sh firefox
REPETIR=8 PROYECTO=login scripts/pruebas.sh     # ocho corridas seguidas
```

Con `PROYECTO=holamundo` o `login` el script compila, levanta la aplicación con
`dotnet run --project <app> --no-build --no-launch-profile` en `Development` con `ASPNETCORE_URLS`
igual a la URL que la prueba tiene escrita, prueba `REPETIR` veces y la apaga. `REPETIR` existe
para buscar intermitencias: «una prueba que pasó una vez no probó nada».

| Script | Para qué |
| --- | --- |
| `scripts/dotnet.sh` | Ejecuta el SDK dentro de `mcr.microsoft.com/dotnet/sdk:10.0` (`IMAGEN_SDK`) |
| `scripts/publicar.sh` | Publica **autocontenido** para `linux-x64` en `publicacion/` (lo que usa CI) |
| `scripts/pruebas.sh` | Corre las E2E; con `PROYECTO` elige el proyecto y levanta la aplicación cuando hace falta |

## Evidencia

`evidencia/2026-09-12-unificacion/`, corrida en la máquina del autor:

| Archivo | Comprobación | Resultado |
| --- | --- | --- |
| `holamundo-script-3-corridas.log` | `PROYECTO=holamundo`, 3 corridas | 3 de 3 en verde |
| `login-script-3-corridas.log` | `PROYECTO=login`, 3 corridas | 3 de 3 en verde |
| `movilidad-script-por-defecto.log` | Movilidad Urbana por el camino por defecto del script | 22/22 |
| `login-falsificacion-y-binario-publicado.log` | Login como lo corre su workflow: binario publicado, Production | 10/10 en chromium y en firefox; y **falla 10/10** sin la aplicación |
| `holamundo-falsificacion-sin-aplicacion.log` | Hola Mundo **sin** la aplicación levantada | Falla: la prueba no pasa en vacío |

Las otras dos carpetas de `evidencia/` —`2026-09-01-aplicacion-template/` y
`2026-09-03-testigo-de-hidratacion/`— respaldan lo que dicen [10](10_Hola-Mundo-Y-Login.md) y
[11](11_Template-Y-Superficies.md).
