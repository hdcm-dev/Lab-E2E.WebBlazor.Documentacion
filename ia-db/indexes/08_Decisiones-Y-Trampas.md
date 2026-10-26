# 08 — Decisiones y trampas

> **Propósito**: por qué el laboratorio está hecho como está, qué no hay que revertir y qué trampas ya se pagaron (web, arnés E2E, CI, renombre, Android, Appium), cada una con su síntoma, su arreglo y la evidencia o el commit que la respalda. Es lo primero que conviene leer antes de «simplificar» algo.
> **Fuente primaria**: `README.md` (§ «Por qué las pruebas E2E son un proyecto de la solución», § «Lo que cambia respecto del ejemplo estático», § «Diseño», § «Runner», § «Evidencia»), `CHANGELOG.md`, comentarios de `tests/MovilidadUrbana.E2ETests/Infrastructure/`, `tests/MovilidadUrbana.MAUI.UITests/Infrastructure/`, `src/MovilidadUrbana.MAUI/{App.xaml.cs,Platforms/Android/MainActivity.cs,Controls/DecimalEntry.cs,Services/OnScreenKeyboard.cs}`, `pruebas.runsettings`, `.gitignore`, `evidencia/`, `git log` (de `0516139` a `8fb4c3a`).
> **Vigencia**: versión 3.1, generada el 2026-10-25 sobre el commit `8fb4c3a` (2026-09-18).
> **Vecinos**: la forma del template y sus desviaciones en detalle en [11](11_Template-Y-Superficies.md); cómo se corren las suites y sus variables en [05](05_Pruebas.md); workflows y corridas observadas en [06](06_CI-Y-Workflows.md); sesión por cookie/encabezado/dispositivo y la base en [03](03_Sesiones-Y-Persistencia.md); acceso y guard de Login en [10](10_Hola-Mundo-Y-Login.md); la API en [12](12_Api-REST.md); la app Android y su devcontainer en [13](13_App-Android.md); la convención inglés/español y el inventario de rastros en [01](01_Arquitectura.md).

---

## 0. Cómo leer este índice

| Marca | Significa |
| --- | --- |
| **No revertir** | Decisión vigente con un costo ya medido: deshacerla reabre una falla conocida |
| **Pagada** | Trampa que ocurrió, con síntoma y arreglo registrados |
| **Abierto** | Encontrado y no resuelto, o no verificado |

Cada fila cita dónde está escrito. Las fechas son las del commit o de la entrada del `CHANGELOG.md`.

---

## 1. Estructura de la solución

| Decisión | Por qué | Marca | Fuente |
| --- | --- | --- | --- |
| Tres aplicaciones de Movilidad Urbana (Web, ApiWeb, MAUI) **independientes**, cada una con sus capas como carpetas; el código se repite a propósito | «cada proyecto tiene que poder estudiarse, compilarse y llevarse por separado» | No revertir | `README.md` § Estructura; `10ce735` |
| Las capas fueron proyectos propios (`MovilidadUrbana.Dominio/.Aplicacion/.Infraestructura`) y el mismo día volvieron a carpetas | Hicieron falta para que la API compartiera reglas; luego se priorizó la independencia. Quedó el registro por capa (entonces `AgregarAplicacion`/`AgregarInfraestructura(cadena)`, hoy `AddApplication`/`AddInfrastructure`) y `Program.cs` que solo compone | Historia | `88e5caa` → `10ce735` (ambos 2026-09-12); `CHANGELOG.md` 2026-09-12 |
| Tres webs de complejidad creciente: Hola Mundo → Login → Movilidad Urbana | Estudiar la temática «de a un escalón» | No revertir | `README.md` § Estructura (l. 83); `CHANGELOG.md` 2026-09-12; `11620e9` |
| Hola Mundo y Login llegaron **byte a byte** desde `Lab-E2E.WebBlazor.Base` | «los números de línea que citan las guías siguen valiendo» | No revertir | `11620e9` |
| `Lab-E2E.WebBlazor.SinMaui.slnf` para CI | El runner no tiene el workload de MAUI | No revertir | `CHANGELOG.md` 2026-09-12; `.github/workflows/ci.yml` l. 56–59 |
| Las E2E son **proyecto C# de la solución** (`Microsoft.Playwright.NUnit`) y no specs de TypeScript | Descubrir, correr y **depurar** desde Visual Studio: el Explorador de pruebas no soporta Playwright JS (solo Mocha, Jasmine, Tape, Jest, Vitest). Costo: se pierden `--shard`, `blob`/`merge-reports` y el reporte HTML; queda TRX | No revertir | `README.md`; `90ad8fe` (reemplazó `e2e/`, `playwright.config.js`, `package.json`) |
| Alternativa conocida: `e2e/` fuera de la solución, como `dotnet/eShop` | «Las dos son defendibles; esta prioriza el IDE» | — | `README.md` |
| Las guías viven en otro repo (una sola copia) | Una sola copia en vez de «dos que pueden divergir en silencio» | No revertir | `98fde5f`; ver [07](07_Guias.md) |
| Nombres: arquitectura en inglés, dominio en español; no se tocan texto visible, URL, contrato JSON, `data-testid`, `AutomationId` ni comentarios | Regla de la guía de nomenclatura; las pruebas y las guías citan esos literales | No revertir | `946d023`; `README.md` § Convención de nombres |

---

## 2. Arnés E2E de Movilidad Urbana (web)

| Decisión / trampa | Síntoma si se revierte o se ignora | Arreglo vigente | Marca | Fuente |
| --- | --- | --- | --- | --- |
| Se prueba el binario **publicado**, no `dotnet run` | Se ejercita otra cosa que lo desplegado | `TestAppServer` lanza `publicacion/` | No revertir | `TestAppServer.cs` l. 189–192 |
| Publicar **en el fixture**, no en el build | Con un target de MSBuild (`31c379d`) Visual Studio decide por su cuenta si compila y «todas las pruebas mueren en `OneTimeSetUp`» | `dotnet publish` incremental antes de la primera prueba; opt-out `PUBLICAR_ANTES_DE_PROBAR=false` (CI lo usa) | Pagada | `6ef117c`; `TestAppServer.cs` l. 124–136; `e2e.yml` l. 229 |
| Instalar el navegador **en el fixture** | `pwsh playwright.ps1 install` exige PowerShell 7, producto aparte del de Windows | API del paquete `Microsoft.Playwright`, solo el navegador de la corrida; `INSTALAR_NAVEGADORES=false` | Pagada | `097692d`; `TestAppServer.cs` l. 89–122 |
| Nombre del apphost según SO | En Windows `FileNotFoundException` en `OneTimeSetUp` (buscaba el nombre de Linux) | `.exe` en Windows; si falta, `dotnet MovilidadUrbana.Web.dll` | Pagada | `bf8b83d`; `TestAppServer.cs` l. 24–30, 201–222 |
| `WorkingDirectory` = carpeta de la publicación | Lanzado desde otra carpeta, `wwwroot` no se encuentra: estáticos con `200` y `Content-Length: 0`, `blazor.web.js` en blanco, el circuito nunca arranca | El fixture lo fija | No revertir | `README.md` § 3; `TestAppServer.cs` l. 62–64 |
| Leer stdout y stderr del `dotnet publish` **en paralelo** | «esperar a uno con el búfer del otro lleno traba el proceso» | Lectura simultánea | No revertir | `TestAppServer.cs` l. 172 |
| `[SetUpFixture]` en el namespace **raíz** de las pruebas | En un namespace hijo no corre para las de arriba: URL base vacía y Playwright «se queja de la cookie» | `namespace MovilidadUrbana.E2ETests;` | Pagada | `README.md` § 6; `TestAppServer.cs` l. 16–17 |
| Paralelismo `ParallelScope.Fixtures`, nunca `Children` | `The given key 'Browser' was not present in the dictionary` / `Collection was modified` | `[assembly: Parallelizable(ParallelScope.Fixtures)]` | No revertir | `90ad8fe`; `Infrastructure/AssemblyParallelism.cs` |
| Cantidad de workers **solo** en `pruebas.runsettings` (`NumberOfTestWorkers` = 4) | Con `[assembly: LevelOfParallelism(3)]` además, «dos números que pueden divergir» | Se quitó el atributo | No revertir | `6f5947e`; `pruebas.runsettings` |
| Traza de Playwright manejada a mano en `[TearDown]` | El binding .NET no tiene `trace: 'on-first-retry'`; una traza que empieza al fallar «llega tarde» | Se graba siempre, se guarda solo lo fallido en `resultados/trazas/<caso>.zip`; `TRAZAR=false`; costo ≈ 2 s sobre 22 casos | No revertir | `6f5947e`; `E2ETestBase.cs` l. 23–29, 87–114; `README.md` § Evidencia (costo) |
| Móvil = chromium con descriptor «Pixel 7», que **falla fuerte** si Playwright no lo conoce | Degradarse en silencio a escritorio | `EMULAR_MOVIL=true` | No revertir | `90ad8fe`; `E2ETestBase.cs` l. 19, 33, 44 |
| Esperar el **testigo de interactividad** antes del primer click | El HTML prerenderizado se ve pero no responde: clicks perdidos, intermitencia en máquinas cargadas | `estado-app[data-interactivo]` + `WaitForInteractiveAsync` | No revertir | `README.md` § 1; `src/MovilidadUrbana.Web/Components/Layout/MainLayout.razor`. La evidencia `evidencia/2026-09-03-testigo-de-hidratacion/` es de **Hola Mundo y Login** (testigo en su página), no de Movilidad Urbana: 8/8 corridas por proyecto, 0 en rojo (`corrida.log`) |
| `@bind:event="oninput"` en los campos | `FillAsync` dispara `input`, no `change`: con `@bind` por defecto el valor llega recién al perder foco y la validación rechaza un formulario que se ve completo | 4 campos con `@bind:event="oninput"` (3 en `Encuesta.razor`, 1 en `Localidades.razor`); los de texto usan `@oninput` a mano (4) | No revertir | `README.md` § 5; `grep` en `Components/Pages` |
| Aislamiento por **sesión** sobre una única SQLite | Las pruebas en paralelo se pisan los datos | Cookie propia por prueba y siembra por sesión | No revertir | `README.md` § 2; detalle en [03](03_Sesiones-Y-Persistencia.md) |
| La cookie se lee en `App.razor` y viaja como parámetro de `Routes` | Un circuito no tiene la petición HTTP: la página no puede leer la cookie | Render mode en la raíz (desviación 1) | No revertir | `README.md` § 2; `Routes.razor` |
| Cultura fija `es-AR` | Los separadores de miles y decimales son parte de lo verificado | `CultureInfo.DefaultThreadCurrentCulture`/`UICulture` en la app; `Locale = "es-AR"` en el contexto de Playwright | No revertir | `src/MovilidadUrbana.Web/Program.cs` l. 13–15; `E2ETestBase.cs` l. 56–57 |
| Hola Mundo y Login **sin fixture**, URL fija | Es a propósito (escalón más simple); la falsificación prueba que sin la app levantada fallan (1/1 y 10/10 en rojo) | Levantar el perfil `http` antes; `scripts/pruebas.sh` con `PROYECTO` lo hace | No revertir | `README.md`; `evidencia/2026-09-12-unificacion/*falsificacion*.log` |
| Hola Mundo y Login de **https a http** (`:5027`, `:5181`) | Con https no corren en CI sin confiar un certificado; se verificó que escuchando solo http no redirigen | perfiles http de `launchSettings` | Pagada | `f9f3ca2`; `CHANGELOG.md` 2026-09-12 |

---

## 3. Interfaz (template SDD)

| Decisión | Por qué | Marca | Fuente |
| --- | --- | --- | --- |
| Template propio con tokens; sin Bootstrap ni librería | Una sola fuente de valor visual y trazabilidad catálogo ↔ código | No revertir | `b0c828e`; [11](11_Template-Y-Superficies.md) |
| Diálogo = `<dialog>` nativo + host único + `IDialogService` | En la versión estática hubo dos defectos con el modal de Bootstrap (click durante la animación y orden de `data-bs-dismiss`); el nativo trae foco confinado y Escape, sin animación que esperar | No revertir | `README.md` § 4; `mq-dialogo.js` |
| `EditForm` sin `DataAnnotationsValidator` en Web | Anotar el modelo sería «transcribir la política de validación en la vista»; la política vive en `Domain/Rules` con pruebas propias | No revertir | `README.md` desviación 2 |
| Revisión del asistente como estado de éxito | `TotalDePasos` es regla de dominio | No revertir | desviación 3 |
| Resultados como **banda**, sin avisos efímeros | Un aviso que se autodescarta haría depender la evidencia E2E de un temporizador | No revertir | `README.md` § Lo que no aplica |
| Ids de `EmptyState`/`UnavailableState` derivados del título (Web) | «tiene que ser el mismo en el prerenderizado y en el circuito». Hola Mundo y Login siguen con `Guid.NewGuid()`: el riesgo de desajuste allí **no está verificado** | No revertir (Web) / Abierto (Base) | `src/MovilidadUrbana.Web/Components/Shared/EmptyState.razor`; `src/WebBlazor.HolaMundo/Components/Shared/EmptyState.razor` l. 40 |
| Reconexión como banda no modal en Web | «cortar la interacción con un velo mientras el circuito vuelve no agrega nada» | No revertir | `ReconnectionNotice.razor` |
| En Hola Mundo/Login se conserva `<dialog id="components-reconnect-modal">` | El módulo del circuito llama `showModal()` y conmuta clases sobre ese elemento: un `div` dejaría la reconexión muda | No revertir | `Template-SDD-Aplicado.md` §2 |
| Login: ingreso en **SSR estático** y POST a endpoint | La cookie se emite en el ciclo de request; con circuito ya no hay dónde escribir la cabecera | No revertir | `Pages/Account/Login.razor`; ver [10](10_Hola-Mundo-Y-Login.md) |
| Cuatro adaptaciones de la suite al template sin aflojar nada (sigue en 22) | Menú, ids del diálogo, indicador de pasos, acciones en la presentación visible (`Filter(Visible = true)`) | No revertir | `README.md` § Lo que cambió en las pruebas |

---

## 4. CI y runner (resumen; detalle en [06](06_CI-Y-Workflows.md))

| Decisión / trampa | Síntoma / motivo | Marca | Fuente |
| --- | --- | --- | --- |
| Ningún job con `container:` | El runner `i7infra-dev` es un contenedor sin socket de Docker: falla en *Initialize containers* con `failed to connect to the docker API at unix:///var/run/docker.sock` | Pagada | `6cb167d`; `README.md` § Runner |
| `publicar` de `e2e.yml` en `[self-hosted, i7infra-dev]`; el resto en `ubuntu-latest` | «esa combinación es la que acumula 23 corridas en verde»: se corrigió el README, no el workflow | No revertir | `7262395`; `e2e.yml` l. 89 |
| `actions/setup-dotnet` explícito y caché de navegadores | La imagen de GitHub no garantiza .NET 10; los runners arrancan sin caché (clave: hash del csproj de pruebas, `e2e.yml` l. 200) | No revertir | `db775c5`; `README.md` § Runner |
| `/dev/shm` de 64 MB | `6cb167d` agregó `--disable-dev-shm-usage` en `playwright.config.js` (no en los workflows); `90ad8fe` borró ese archivo y el README pasó a «a esta escala no hace falta» (`git log -S`). Medido: las 22 de chromium pasan igual. Si aparece la intermitencia: ese argumento o `--shm-size` | Abierto (vigilar) | `README.md` § Runner; `6cb167d`; `90ad8fe` |
| `ci-ok` como único check a exigir | No actualizar la regla de protección cada vez que cambia la matriz | No revertir | `README.md` § ci.yml |
| Se retiró `e2e_2.yml` (el workflow de Base; nunca estuvo en la historia de este repo: `git log --all` vacío) | 0 corridas exitosas de 4 en aquel repo, no levantaba la app, compartía `name` y artefacto con `e2e.yml` | Pagada | `f9f3ca2`; `CHANGELOG.md` 2026-09-12 |
| `-warnaserror --no-incremental` para validar renombres | El build incremental local no mostró `CS1574`; la CI, que compila desde cero, sí (sobre `946d023`) | Pagada | `e9dea2a`; `CHANGELOG.md` 2026-09-18 |

---

## 5. Trampas del renombre (`946d023`, `e9dea2a`, 2026-09-18)

| Trampa | Qué pasó | Arreglo | Fuente |
| --- | --- | --- | --- |
| `<see cref>` con nombres viejos | La herramienta de renombre protege los comentarios; la CI falló con `CS1574` | Segundo commit que renombra las `cref` | `e9dea2a`; `CHANGELOG.md` |
| `Sesion` → `Session` cambia la **tabla** | Las bases SQLite de corridas anteriores quedan con el esquema viejo: `EnsureCreated` no migra | Borrar las bases (`datos-e2e/`, etc.) | `CHANGELOG.md` 2026-09-18; ver [03](03_Sesiones-Y-Persistencia.md) |
| Dos `DependencyInjection` (Application e Infrastructure) | Ambigüedad en `Program.cs` | `Program.cs` califica (`MovilidadUrbana.Web.Infrastructure.DependencyInjection.DefaultConnectionString`) | `CHANGELOG.md`; `src/MovilidadUrbana.Web/Program.cs` |
| Namespace `MovilidadUrbana.MAUI.Application` tapa la clase `Application` de MAUI | No compila `App : Application` | `App : Microsoft.Maui.Controls.Application` | `CHANGELOG.md`; `src/MovilidadUrbana.MAUI/App.xaml.cs` |
| Nombres generados por `[ObservableProperty]`/`[RelayCommand]`, prefijos XAML y bindings con `RelativeSource` | Renombrar solo el origen rompe los bindings en silencio | Se renombraron junto con su origen | `CHANGELOG.md` 2026-09-18 |
| Renombre que miente | Una traducción automática cambia el sentido (p. ej. `AlRechazarLaEntrada` → `OnSignInRejected` en una superficie sin ingreso) | Sin corregir (rastro) | casos en [10](10_Hola-Mundo-Y-Login.md) §7 y [05](05_Pruebas.md) §13 |
| Rastros en texto (README, comentarios, mensajes) | p. ej. `README.md` dice `MovilidadUrbana.E2ETests.Infraestructura`; `pruebas.runsettings` cita `ParalelismoDelEnsamblado.cs` | Sin corregir | inventario en [01](01_Arquitectura.md); los de la vista en [11](11_Template-Y-Superficies.md) § 10 |
| Renombre previo: prefijo `E2E.Base` (2026-09-12) | Los registros de `evidencia/` anteriores conservan `WebBlazor.E2E.Base.*`: son históricos, no se tocan | — | `e0f3e9d` (su verificación, 1/1 y 10/10, está en `evidencia/2026-09-12-renombre/`); p. ej. `evidencia/2026-09-12-unificacion/*.log` |

Verificación del renombre: Release `-warnaserror --no-incremental`; 49 + 13 + 18 unitarias/API/ViewModels, 22 + 1 + 10 E2E, APK compila, Appium 5/5 (`CHANGELOG.md` 2026-09-18). No hay carpeta de evidencia propia: `evidencia/2026-09-12-renombre/` es del renombre de prefijo (`e0f3e9d`), no de `946d023`.

---

## 6. Trampas de Android (`MovilidadUrbana.MAUI`)

Probado en un Motorola moto e6 play (Android 9, armeabi-v7a, 720×1440: `evidencia/2026-09-12-maui/dispositivo.txt`).

| Trampa | Síntoma | Arreglo | Fuente / evidencia |
| --- | --- | --- | --- |
| MAUI pisa el `AdjustResize` del manifiesto con su modo **Pan** | Enfocar un campo bajo corre toda la pantalla y corta el encabezado | `UseWindowSoftInputModeAdjust(…Resize)` en `App` + `WindowSoftInputMode = SoftInput.AdjustResize` en `MainActivity` | `App.xaml.cs`; `MainActivity.cs` |
| En la página **apilada** por Shell la ventana no se achica | La barra con «Guardar» queda tapada por el teclado; `SafeAreaEdges` deja un hueco que no se cierra; los insets del IME no llegan | `OnScreenKeyboard.KeepAboveKeyboard`: mide en cada `GlobalLayout` cuánto quedó tapado y corrige el margen hasta converger | `Services/OnScreenKeyboard.cs`; capturas `36`–`38` |
| Teclado numérico descarta la coma | «12,5» llegaba como «125» y se registraba **sin error** | `DecimalEntry` acepta coma y punto; el ViewModel interpreta los dos | `Controls/DecimalEntry.cs`; capturas `24` → `35` |
| Errores que no se borraban, sin borde rojo, error de grupo debajo de la tarjeta | Iteraciones de la UI | Corregidos en orden | `evidencia/2026-09-12-maui/README.md` (`07`→`18`, `05`→`29`, `21`→`32`) |
| El Toast dura menos que una captura | No hay imagen que lo pruebe | La evidencia es la línea de `logcat` con `producer=(…:ar.lab.movilidadurbana)` | `evidencia/2026-09-12-maui/toast-logcat.txt` |
| Nombre de la activity | Sin `[Register]` el nombre es un hash y Appium no puede lanzarla | `[Register("ar.lab.movilidadurbana.MainActivity")]` | `MainActivity.cs`; `3e119b8` |
| El proyecto Android no se referencia sin el workload | Las pruebas de ViewModels no compilarían en CI | `MovilidadUrbana.MAUI.Tests` compila `Domain/`, `Application/`, `Infrastructure/`, `Presentation/` como archivos enlazados | `tests/MovilidadUrbana.MAUI.Tests/MovilidadUrbana.MAUI.Tests.csproj` l. 27–30 |
| El teléfono es un recurso único para adb | «dos servidores de adb se lo disputan y el síntoma aparece en el otro» | `dev.sh up` apaga el adb del otro contenedor y `devolver` lo restituye | `.devcontainer/dev.sh` l. 15–18, 40–41 |
| Tema oscuro | — | `UserAppTheme = AppTheme.Light`: «no se deriva un tema oscuro que nadie diseñó» | `App.xaml.cs` |

---

## 7. Trampas de Appium (`MovilidadUrbana.MAUI.UITests`)

Suite: `Appium.WebDriver` 8.0.0, servidor Appium 3.7.0, `uiautomator2@8.6.4` (`evidencia/2026-09-13-uitests/README.md`). Las trampas 1–3 son las corridas en rojo que ese README no guardó («la causa era de la suite, no de la app»); la 4 sale del `CHANGELOG.md` 2026-09-18; la 5 y la 6 son decisiones de la suite:

| # | Trampa | Síntoma | Arreglo | Fuente |
| --- | --- | --- | --- | --- |
| 1 | `[SetUpFixture]` en namespace hijo (la misma de la web) | «La sesión de Appium no está abierta» | `AppiumSession` en `namespace MovilidadUrbana.MAUI.UITests;` | README de evidencia; `AppiumSession.cs` l. 5–6 |
| 2 | Esperas de 30 s y «Eliminar» debajo del pliegue | Timeouts | Esperas de 60 s (`ScreenTestBase.Timeout`) y `UiScrollable` | README de evidencia; `ScreenTestBase.cs` l. 16, 56–70 |
| 3 | `NoReset` con el proceso vivo en segundo plano | «already running and noReset is enabled»: no trae la app al frente | `ActivateApp(AppPackage)` y espera de la primera pantalla | `AppiumSession.cs` |
| 4 | Arranque en frío tras instalar en Debug | Hilo principal ocupado ~21 s (`Skipped 1272 frames`); UIAutomator2 no consigue el árbol y la sesión fallaba antes de empezar | Reintento hasta 120 s buscando `lista-localidades` o `etiqueta-paso` | `CHANGELOG.md` 2026-09-18; `946d023`; `AppiumSession.cs` |
| 5 | Un dispositivo es una sola pantalla | — | `[assembly: NonParallelizable]` | `UITests/Infrastructure/AssemblyParallelism.cs` |
| 6 | Prueba anterior que dejó una página apilada | La siguiente arranca en otra pantalla | El `[SetUp]` de cada clase llama `GoToTab`, que vuelve atrás (`Navigate().Back()`, hasta 4 intentos) | `ScreenTestBase.cs` l. 76–91; `LocalidadesTests.cs` l. 12–15; `EncuestaTests.cs` l. 9–12; `CHANGELOG.md` 2026-09-12 |

No corren en CI (necesitan el dispositivo). Evidencia: dos corridas 5/5 (3 min 21 s y 3 min 5 s) y una falsificación (`NoAvanzaConElPaso1Vacio` esperando «Paso 2 de 3» → 1 en rojo, 4 en verde) en `evidencia/2026-09-13-uitests/`.

---

## 8. Trampas del entorno y del repositorio

| Trampa | Síntoma | Arreglo | Fuente |
| --- | --- | --- | --- |
| `fs.inotify.max_user_instances = 128` agotado en la máquina | La app muere con código 134 al construir su configuración («terminó sola con código 134 antes de escuchar») | `DOTNET_USE_POLLING_FILE_WATCHER=1` (`scripts/pruebas.sh` l. 64 lo reenvía al contenedor si está definido; vacío por defecto). Es del entorno, no del laboratorio | `README.md` § Evidencia |
| `git add -A` con carpetas de `evidencia/` ausentes del disco | El commit las registró como borradas | Restauradas desde `HEAD~1` | `910b42b` |
| `*.log` ignorado por la plantilla de `.gitignore` | La evidencia no se versionaría | Excepción `!evidencia/**/*.log` (l. 122–123); los `.trx` siguen ignorados (consecuencia para la evidencia de UITests en [05](05_Pruebas.md) §14) | `.gitignore`; `git ls-files evidencia` |
| Carpetas de solución del `.sln` apuntando a archivos que no existen | Explorador de soluciones lleno de enlaces rotos, «sobrevive meses porque no rompe el build» (llegaron a ser 37 archivos) | Se retiraron los nodos; los archivos sueltos se declaran uno por uno | `7a069b3`, `98fde5f`, `bd69d1e` |
| Enlaces relativos `../../IA/...` y `../Lab-E2E.StaticHtml` del `README.md` | No resuelven desde la ubicación del clon (verificado) | Sin corregir | `README.md` l. 7, 17–19, 172–176; ver [11](11_Template-Y-Superficies.md) §1 |

---

## 9. Abierto / no verificado

| Tema | Estado | Fuente |
| --- | --- | --- |
| Paso direccionable sin caso (`/encuesta/2`, `/encuesta/3`) y `catch` de `FinishAsync` / `boton-procesando` sin ejercitar; el paso se hizo direccionable «para que se pueda verificar de a uno» | Abierto; detalle y evidencia del hueco en [05](05_Pruebas.md) §11 | `CHANGELOG.md` 2026-09-04 «Encontrado, no resuelto» |
| Cierre del `<dialog>` por **Escape** | `Dialog.razor` no maneja `cancel`/`close` y ninguna prueba usa Escape (`git grep`). Por lectura del código, `DialogService.Current` quedaría sin resolver; la consecuencia **no está verificada** en ejecución | `Dialog.razor`, `DialogService.cs` |
| Confirmación de segundo grado (escrita) | Implementada y sin uso | `README.md` § Lo que no aplica |
| Explorador de pruebas de Visual Studio | **No verificado** («no hay Windows ni Visual Studio en esta máquina») | `README.md` § Evidencia |
| Comportamiento real de los workflows | El README dice que solo se validó la sintaxis; las corridas observadas están en [06](06_CI-Y-Workflows.md) | `README.md` § Evidencia |

---

## 10. Lista corta de «no revertir»

1. Publicar e instalar el navegador en el fixture, no en el build.
2. `ParallelScope.Fixtures` y los workers solo en `pruebas.runsettings`.
3. `[SetUpFixture]` en el namespace raíz (web y Appium).
4. `WorkingDirectory` del proceso = carpeta publicada.
5. Testigo `estado-app` antes del primer click y `@bind:event="oninput"`.
6. Render mode en la raíz de Movilidad Urbana (puente de la cookie).
7. `<dialog>` nativo con host único; nada de avisos efímeros.
8. Tres aplicaciones independientes con código repetido; CI sobre `SinMaui.slnf`.
9. Jobs sin `container:`; `publicar` en el runner propio.
10. `AdjustResize` + `OnScreenKeyboard` + `DecimalEntry` en Android; `[Register]` en `MainActivity`.
11. No renombrar `data-testid`, `AutomationId`, URL, contrato JSON ni texto visible; validar renombres con `--no-incremental`.
