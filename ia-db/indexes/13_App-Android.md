# 13 — App Android (MAUI)

> **Propósito**: qué es `MovilidadUrbana.MAUI`, cómo se compone y navega, qué hace cada pantalla y cada ViewModel, qué resuelve para la plataforma Android, cómo se compila e instala desde el devcontainer, y cómo se prueban los ViewModels (sin teléfono) y la interfaz (con Appium en el teléfono).
> **Fuente primaria**: `src/MovilidadUrbana.MAUI/` (`MovilidadUrbana.MAUI.csproj`, `MauiProgram.cs`, `App.xaml(.cs)`, `AppShell.xaml(.cs)`, `Pages/`, `Presentation/`, `Services/`, `Controls/`, `Converters/`, `Platforms/Android/`, `Resources/Styles/`), `tests/MovilidadUrbana.MAUI.Tests/`, `tests/MovilidadUrbana.MAUI.UITests/`, `.devcontainer/` (`Dockerfile`, `devcontainer.json`, `dev.sh`), `.github/workflows/android.yml`, `Lab-E2E.WebBlazor.SinMaui.slnf`, `README.md` («La aplicación Android», «Evidencia»), `CHANGELOG.md`, `evidencia/2026-09-12-maui/`, `evidencia/2026-09-13-uitests/`.
> **Vigencia**: versión 3.1, generada el 2026-10-25 sobre el commit `8fb4c3a` (2026-09-18).
> **Vecinos**: reglas, catálogos y mensajes en [02](02_Dominio-Y-Reglas.md); la sesión del dispositivo comparada con cookie y encabezado, y la base SQLite, en [03](03_Sesiones-Y-Persistencia.md); el reparto de capas y la composición de `MauiProgram.cs` frente a los `Program.cs`, en [01](01_Arquitectura.md); el inventario de suites y cómo se corren todas, en [05](05_Pruebas.md); `android.yml` y sus corridas, en [06](06_CI-Y-Workflows.md); las guías de `Test-Guide/`, en [07](07_Guias.md); las trampas de Android y Appium con su porqué, en [08](08_Decisiones-Y-Trampas.md); la API, en [12](12_Api-REST.md).

---

## 1. Identidad de la app

| Aspecto | Valor | Fuente |
| --- | --- | --- |
| Target | `net10.0-android` únicamente («el laboratorio se construye en Linux, donde iOS y Mac Catalyst no compilan») | `MovilidadUrbana.MAUI.csproj:7,9` |
| Tipo | `OutputType Exe`, `UseMaui`, `SingleProject` | `:10-13` |
| Título / id | «Movilidad Urbana» / `ar.lab.movilidadurbana` | `:17-18` |
| Versión | `ApplicationDisplayVersion 1.0`, `ApplicationVersion 1` | `:19-20` |
| API mínima | 23 («AndroidX de .NET 10 exige API 23 como mínimo») | `:22-23` |
| Paquetes | `Microsoft.Maui.Controls` `$(MauiVersion)` (la fija el workload instalado), `Microsoft.Extensions.Logging.Debug` 10.0.11, `Microsoft.EntityFrameworkCore.Sqlite` 10.0.11, `CommunityToolkit.Mvvm` 8.4.2 | `:34-37` |
| Ícono y splash | SVG con color `#0F6E56` | `:27-28` |
| Permisos | ninguno declarado; «en Debug el SDK agrega INTERNET por su cuenta para el depurador» | `Platforms/Android/AndroidManifest.xml:2-5` |
| Servidor | no habla con ninguno: base SQLite en el almacenamiento privado | `csproj:3-6`, `MauiProgram.cs:14-16` |

```
src/MovilidadUrbana.MAUI/
├── MauiProgram.cs            raíz de composición
├── App.xaml(.cs)             recursos, tema claro, AdjustResize
├── AppShell.xaml(.cs)        TabBar: Localidades | Encuesta; ruta "localidad" (editor apilado)
├── Domain/ Application/ Infrastructure/   capas propias, idénticas a web y API (ver 01, 02, 03)
├── Presentation/             ViewModels + INavigationService, IAlertService, ListState
├── Pages/                    LocalidadesPage, LocalidadEditorPage, EncuestaPage (.xaml + .xaml.cs)
├── Services/                 DeviceSession, ShellNavigationService, AlertService, OnScreenKeyboard
├── Controls/DecimalEntry.cs  Converters/Converters.cs
├── Platforms/Android/        MainActivity, MainApplication, AndroidManifest, colors.xml
└── Resources/                AppIcon, Splash, Images (agregar, tab_*), Fonts (OpenSans), Styles
```

---

## 2. Composición (`MauiProgram.cs`)

| Registro | Vida | Nota | Línea |
| --- | --- | --- | --- |
| Cultura `es-AR` | — | `DefaultThread*` y también `CurrentCulture` del hilo principal, que ya existe | `:24-26` |
| `AddInfrastructure("Data Source=<AppDataDirectory>/movilidad.db;Default Timeout=30")` | scoped (repos, `SessionContext`, `SessionSeeder`) + factory | misma capa que web y API | `:40-41` |
| `AddApplication()` | scoped | `LocalidadService`, `EncuestaService` | `:42` |
| `DeviceSession` | singleton | abre **un** ámbito que vive lo que la app y fija ahí la sesión | `:44` |
| `INavigationService` → `ShellNavigationService` | singleton | | `:45` |
| `IAlertService` → `AlertService` | singleton | | `:46` |
| `LocalidadesViewModel`, `LocalidadEditorViewModel` | transient | creados con `DeviceSession.Create<T>()` (`ActivatorUtilities` sobre el ámbito del dispositivo) | `:49-50` |
| `EncuestaViewModel` | **singleton** | el asistente conserva lo cargado al alternar pestañas | `:51` |
| Páginas | transient | | `:53-55` |
| Handlers Android | — | `QuitarSubrayadoNativo()` y `AceptarComaDecimal()` (§5) | `:37-38` |
| Arranque | — | `DatabaseInitializer.Initialize` (EnsureCreated + WAL) | `:62` |

- `App` hereda de `Microsoft.Maui.Controls.Application` con nombre completo: el espacio `MovilidadUrbana.MAUI.Application` tapa la clase de MAUI (`App.xaml.cs:5`; `CHANGELOG.md` 2026-09-18).
- `App` fuerza `UserAppTheme = AppTheme.Light` («no se deriva un tema oscuro que nadie diseñó») y `WindowSoftInputModeAdjust.Resize`, porque MAUI aplica Pan por defecto y pisa el manifiesto (`App.xaml.cs:13-19`).
- `AppShell`: `FlyoutBehavior=Disabled`, `TabBar` con `Tab` «Localidades» (ruta `localidades`) y «Encuesta» (ruta `encuesta`); las páginas se resuelven del contenedor con `DataTemplate`; registra la ruta `localidad` para `LocalidadEditorPage` (`AppShell.xaml:5,14-21`, `AppShell.xaml.cs:11-13`).

### Navegación

| Desde | Acción | Implementación | Fuente |
| --- | --- | --- | --- |
| Lista | Agregar / tocar fila | `GoToAsync("localidad", { localidad: item ?? "" })`: siempre se pasa el parámetro, así el editor distingue alta de edición | `Services/ShellNavigationService.cs:9-17` |
| Editor | recibe | `IQueryAttributable.ApplyQueryAttributes` → `vm.Initialize(valor as LocalidadItem)` | `Pages/LocalidadEditorPage.xaml.cs:17-21` |
| Editor | guardar / eliminar con éxito | `GoToAsync("..")` | `ShellNavigationService.cs:19` |
| Lista y Encuesta | aparecer | `OnAppearing` ejecuta `LoadCommand` (la lista refleja el editor; la encuesta, cambios de la otra pestaña) | `Pages/LocalidadesPage.xaml.cs:16-20`, `Pages/EncuestaPage.xaml.cs:18-22` |

El editor oculta la barra de pestañas (`Shell.TabBarIsVisible="False"`, `LocalidadEditorPage.xaml`).

---

## 3. Sesión y base en el teléfono

| Aspecto | Cómo | Fuente |
| --- | --- | --- |
| Sesión | el dispositivo entero es **una** sesión; id `Guid "n"` generado la primera vez y guardado en `Preferences` con la clave `sesion-dispositivo` | `Services/DeviceSession.cs:16,22-27` |
| Fijación | `DeviceSession` crea un `IServiceScope` y llama `SessionContext.Set(id)` en él | `DeviceSession.cs:29-31` |
| Base | `movilidad.db` en `FileSystem.AppDataDirectory` | `MauiProgram.cs:40` |
| Persistencia | los datos sobreviven a cerrar la app | `README.md` «La aplicación Android» |
| Siembra | Corrientes y Resistencia en la primera lectura (misma `SessionSeeder` que web y API) | ver [03](03_Sesiones-Y-Persistencia.md) |

`DeviceSession` vive en `Services/` y no en `Infrastructure/` porque usa `Preferences`, que no existe en `net10.0`: si se moviera, `MAUI.Tests` dejaría de compilar (`/LAB/Lab-Documentos/Lab-Documentos/Guides/Testing/Lab-E2E.WebBlazor-Guides/Test-Guide/Pruebas-Unitarias-Y-Arquitectura.md` §7.2).

---

## 4. Pantallas, ViewModels y `AutomationId`

### Localidades (`LocalidadesPage` + `LocalidadesViewModel`)

| Elemento | Comportamiento | Fuente |
| --- | --- | --- |
| Búsqueda | `SearchText` filtra por nombre (sin distinguir mayúsculas, cultura actual) o por código postal (ordinal), sobre lo ya traído | `Presentation/Localidades/LocalidadesViewModel.cs:81-88` |
| Filtro | `Provincia` con «Todas las provincias» + las siete del catálogo | `:16,22` |
| Estados | `ListState`: `Cargando`, `ConDatos`, `Vacio`, `FiltradoSinResultados` (vocabulario de la web) | `Presentation/ListState.cs`, `:93-95` |
| Resumen | «N localidades» o «N de M localidades» | `:43-45` |
| Orden | por nombre, `StringComparer.CurrentCulture` | `:57-59` |
| Fila | `LocalidadItem` con `Detalle` «Provincia · CP 3400» y `HabitantesTexto` `N0` «hab.» | `Presentation/Localidades/LocalidadItem.cs` |
| Recargar | `RefreshView` → `LoadCommand` | `Pages/LocalidadesPage.xaml:30` |
| Agregar | botón flotante de 56 dp abajo a la derecha | `LocalidadesPage.xaml:80-89` |

### Editor (`LocalidadEditorPage` + `LocalidadEditorViewModel`)

| Elemento | Comportamiento | Fuente |
| --- | --- | --- |
| Título | «Nueva localidad» / «Editar localidad» según `Id` | `LocalidadEditorViewModel.cs:39-41` |
| Validación | la del servicio de aplicación; los errores se ubican por clave junto a cada campo | `:74-88,137-143` |
| Corregir borra el error | `partial void On<Campo>Changed` → `<Campo>Error = null` | `:61-64` |
| Habitantes | `ParseInt` ignora separadores de miles | `:131-135` |
| Guardar ok | Toast con el mensaje del servicio y vuelve | `:90-91` |
| Eliminar | confirmación «¿Eliminar {Nombre}? Esta acción no se puede deshacer.»; si se cancela, no pasa nada | `:104-109` |
| Foco | en un alta, el cursor va al nombre tras 250 ms | `LocalidadEditorPage.xaml.cs:24-28` |
| Error visible | `DataTrigger` pone el borde del campo en `TextoError`, grosor 2 | `LocalidadEditorPage.xaml:20` |

### Encuesta (`EncuestaPage` + `EncuestaViewModel`, singleton)

| Elemento | Comportamiento | Fuente |
| --- | --- | --- |
| Pasos | 1 «Datos de la persona», 2 «Medios que utiliza para viajar», 3 «Distancia recorrida»; etiqueta «Paso N de 3»; barra `Progress` | `Presentation/Encuestas/EncuestaViewModel.cs:80-89` |
| Avanzar | `Next` valida solo el paso vigente con `EncuestaService.ValidarPaso`; con errores, aviso «Complete los datos del paso antes de continuar.» | `:134-138,186-201`, `:19` |
| Volver | `Previous` limpia errores y conserva lo cargado | `:140-146` |
| Registrar | valida el paso 3, registra, llena `Resumen` (`ResumenDeEncuesta.De`), actualiza el contador y pasa a «Encuesta completada» / «¡Gracias por participar!» | `:150-172` |
| Falla al registrar | aviso «No pudimos registrar la encuesta. Volvé a intentar en unos segundos.» | `:164-167` |
| Nueva encuesta | vacía todo, vuelve al paso 1, conserva el contador | `:174-184` |
| Localidades | los nombres del ABM, ordenados; si la elegida desapareció, se deselecciona | `:118-132` |
| Medios | `SelectableOption` por medio del catálogo; toda la fila alterna la casilla; marcar borra el error | `Presentation/Encuestas/Opciones.cs:10-22`, `EncuestaViewModel.cs:62-70` |
| Frecuencia y motivo | `RadioButtonGroup` ligado a la clave | `Pages/EncuestaPage.xaml:95-104,136-145` |
| Números | `Edad`, `Minutos` con `InvariantCulture`; `Distancia` acepta coma o punto (`Replace(',', '.')`) | `EncuestaViewModel.cs:215-230` |
| Desplazamiento | al cambiar `Paso`, `Completada` o `Notice`, `ScrollToAsync(0,0)` | `EncuestaPage.xaml.cs:25-29` |

### `AutomationId` declarados (contados con `grep`)

| Página | `AutomationId` | Usados por UITests |
| --- | --- | --- |
| `LocalidadesPage.xaml` (6) | `buscar`, `filtro-provincia`, `lista-localidades`, `estado-vacio`, `estado-sin-resultados`, `agregar` | todos salvo `filtro-provincia` y `estado-vacio` |
| `LocalidadEditorPage.xaml` (7) | `aviso`, `nombre`, `provincia`, `codigo-postal`, `habitantes`, `eliminar`, `guardar` | todos |
| `EncuestaPage.xaml` (14) | `etiqueta-paso`, `contador`, `aviso`, `nombre`, `edad`, `localidad`, `{Binding Clave}` (una fila por medio: `colectivo`, `auto`, …), `distancia`, `minutos`, `encuesta-completada`, `nueva-encuesta`, `anterior`, `siguiente`, `registrar` | todos salvo `contador` y `anterior`; de los medios, solo `colectivo` |

Los botones de radio de frecuencia y motivo no tienen `AutomationId`: los UITests los tocan por texto («Todos los días», «Trabajo») (`tests/MovilidadUrbana.MAUI.UITests/EncuestaTests.cs:41,47`). El `AutomationId` llega a Android como `resource-id` `ar.lab.movilidadurbana:id/<id>` (`ScreenTestBase.cs:18,62`). Los `data-testid` de la web son de [04](04_Interfaz-Y-Pantallas.md).

---

## 5. Lo que resuelve para Android

| Problema | Solución | Fuente | Evidencia |
| --- | --- | --- | --- |
| El teclado numérico en es-AR descartaba la coma: «12,5» llegaba como «125» y se registraba sin error | `DecimalEntry` + mapper que fija `InputType ClassNumber|NumberFlagDecimal` y `DigitsKeyListener("0123456789,.")`; el VM acepta coma y punto | `Controls/DecimalEntry.cs`, `MauiProgram.cs:67-77` | capturas `24` → `35` |
| Subrayado nativo dentro de la caja del campo | mapper `SinSubrayado` en `Entry`, `Picker` y `SearchBar` (placa `search_plate` resuelta por nombre) | `MauiProgram.cs:83-97` | captura `01` |
| La barra fija («Guardar», «Siguiente») tapada por el teclado | `MainActivity` con `SoftInput.AdjustResize` + `App` con `WindowSoftInputModeAdjust.Resize` | `Platforms/Android/MainActivity.cs:10-13`, `App.xaml.cs:15-19` | `33` |
| En la página apilada del editor la ventana no se achica; `SafeAreaEdges` deja hueco | `OnScreenKeyboard.KeepAboveKeyboard`: en cada `GlobalLayout` mide la barra contra `GetWindowVisibleDisplayFrame` y corrige su margen hasta converger | `Services/OnScreenKeyboard.cs:3-47`, `LocalidadEditorPage.xaml.cs:14` | `36`–`38` |
| Appium no puede lanzar la activity: sin nombre fijo, su nombre Java es un hash | `[Register("ar.lab.movilidadurbana.MainActivity")]`; la misma activity declara `MainLauncher`, `LaunchMode.SingleTop` y el tema `Maui.SplashTheme` | `MainActivity.cs:8,11-12` | — |
| Aviso breve | `AlertService.ShowAsync` = Toast corto; `ConfirmAsync` = `Shell.Current.DisplayAlertAsync` | `Services/AlertService.cs` | `toast-logcat.txt` |

El porqué de cada una y lo que no hay que revertir está en [08](08_Decisiones-Y-Trampas.md).

---

## 6. Diseño

- Paleta propia en `Resources/Styles/Colors.xaml:46-58`: `Marca #0F6E56`, `MarcaOscura #04342C`, `MarcaTinte #E1F5EE`, `Superficie #FFFFFF`, `Lienzo #F7F6F4`, `TextoPrimario #1A1A18`, `TextoSecundario #5C5C57`, `Borde #D9D9D4`, `SuperficieInerte #F1F1EF`, `TextoError #A03030`, `FondoError #FBEAF0`, `FondoInfo #E7F0F9`, `TextoInfo #185FA5` (el comentario de `Colors.xaml:45` y el README la presentan como los valores de `Tokens.css` de la web). Las claves de las líneas 8-43 (`Primary`, `Gray100`, sus `…Brush`) son las de la plantilla de MAUI; `Primary`/`PrimaryDark`/`Secondary`/`Tertiary` llevan valores de la marca.
- Colores nativos de Android (`Platforms/Android/Resources/values/colors.xml:3-5`): `colorPrimary` `#0F6E56`, `colorPrimaryDark` y `colorAccent` `#04342C`, los mismos valores de marca.
- Estilos con clave en `Resources/Styles/Movilidad.xaml`: `Titulo`, `Rotulo`, `Ayuda`, `Error`, `Campo`, `Desplegable`, `Tarjeta`, `BotonPrimario`, `BotonSecundario`, `BotonPeligro`, `Banda`; `MinimumHeightRequest` 48 en cinco setters (objetivo táctil de 48 dp). `Styles.xaml` (434 líneas) es el diccionario base.
- Convertidores: `IsNotNullOrEmptyConverter` (clave `TextoPresente`) e `InvertedBoolConverter` (`Negar`) (`App.xaml:13-14`).
- Las superficies web son de [11](11_Template-Y-Superficies.md).

---

## 7. Compilación: devcontainer y `dev.sh`

### Imagen (`.devcontainer/Dockerfile`)

| Capa | Contenido | Líneas |
| --- | --- | --- |
| Base | `mcr.microsoft.com/dotnet/sdk:10.0` | `:9` |
| Sistema | `openjdk-17-jdk-headless`, `usbutils`, `udev`, `sudo`, `libicu-dev`, `locales` (es_AR y en_US generados) | `:17-27` |
| Android SDK | cmdline-tools `13114758`; `platform-tools`, `platforms;android-36`, `android-35`, `build-tools;36.0.0` y `35.0.0` | `:37-53` |
| Workload | `dotnet workload install maui-android --skip-sign-check` | `:58-59` |
| Appium | Node.js 22 (nodesource), `npm install -g appium` **sin versión fija**, `appium driver install uiautomator2`, `APPIUM_HOME=/opt/appium` | `:61-69` |
| Usuario | `dev` con UID/GID 1000 del host; `sudo` sin contraseña (el servidor `adb` necesita root para el nodo USB) | `:71-90` |
| Entorno | `LANG=es_AR.UTF-8`, telemetría apagada, `WORKDIR /workspace` | `:92-97` |

### Contenedor

| Aspecto | `devcontainer.json` (VS Code) | `dev.sh` (consola) |
| --- | --- | --- |
| Nombre | `lab-e2e-maui-dev` (`runArgs`) | `NAME=lab-e2e-maui-dev`, imagen `lab-e2e-maui-dev:net10` |
| Montaje del repo | `/work` (`workspaceFolder`) | `/work` (`-v` y `-w`, `dev.sh:46,50`) |
| Privilegios | `--privileged`, `/dev/bus/usb` | ídem |
| Volúmenes | `lab-maui-nuget` → `~/.nuget`; `gda-app-adbkeys` → `~/.android` (clave adb ya autorizada por el teléfono, compartida con GDA.Core.APP); `lab-maui-keystore` → `~/.local/share/Xamarin` (keystore Debug persistente: si cambia, el APK nuevo no se instala sobre el anterior) | ídem |
| Arranque | `postCreateCommand` chown; `postStartCommand` `sudo -E HOME=/home/dev adb start-server` | `chown` como root + `adb start-server` como root |

Los dos usan el mismo nombre de contenedor: no pueden estar levantados a la vez (deducido de `devcontainer.json:6` y `dev.sh:23,43`).

### Subcomandos de `dev.sh`

| Subcomando | Qué hace | Líneas |
| --- | --- | --- |
| `up` | construye la imagen si falta; si `gda-core-app-dev` está corriendo, le apaga el `adb`; levanta el contenedor y lista dispositivos | `:37-55` |
| `devices` | `adb devices -l` | `:57` |
| `build` | `dotnet build … -c Debug -f net10.0-android -p:AndroidPackageFormat=apk -p:RuntimeIdentifier=$ABI -p:EmbedAssembliesIntoApk=true` | `:59-63` |
| `install` | build + `adb install -r` del `*-Signed.apk` | `:67-72` |
| `run` | install + `adb shell monkey -p ar.lab.movilidadurbana … 1` | `:74-78` |
| `logs` | `logcat -d --pid=…` (últimas 200 líneas) | `:80` |
| `uitests` | levanta Appium desprendido (`docker exec -d`) si `:4723/status` no responde, espera hasta 30 s y corre `dotnet test tests/MovilidadUrbana.MAUI.UITests -c Release` con TRX `uitests.trx` en `tests/MovilidadUrbana.MAUI.UITests/resultados/` | `:84-94` |
| `down` | mata `adb` y borra el contenedor | `:96-99` |
| `devolver` | `down` + `adb start-server` en `gda-core-app-dev` | `:101-107` |

- ABI por defecto `android-arm` (armeabi-v7a, la del teléfono de prueba); `ABI=android-arm64` para 64 bits (`dev.sh:29-30`).
- Regla: **un solo servidor `adb` por vez**; mientras este contenedor es el dueño, los medios de observación se usan con `MEDIOS_ADB_OWNER=lab-e2e-maui-dev` (`dev.sh:15-18`).
- La solución completa incluye el proyecto Android; `Lab-E2E.WebBlazor.SinMaui.slnf` lista los otros once proyectos (incluidos `MAUI.Tests` y `MAUI.UITests`) y es lo que compila `ci.yml` (`README.md` «La aplicación Android»; [06](06_CI-Y-Workflows.md)).

### En CI (`android.yml`, detalle en [06](06_CI-Y-Workflows.md))

`ubuntu-latest`, 45 min: `dotnet test tests/MovilidadUrbana.MAUI.Tests` → Java 17 Temurin → `dotnet workload install maui-android` → `-t:InstallAndroidDependencies` → `dotnet publish -c Release -f net10.0-android -p:AndroidPackageFormat=apk` → artefacto `movilidad-urbana-apk` (`apk/*-Signed.apk`, 14 días). Firmado con la clave de depuración del runner: «sirve para instalarlo en un teléfono de prueba, no para publicarlo en una tienda». Filtro de rutas: `src/MovilidadUrbana.MAUI/**`, `tests/MovilidadUrbana.MAUI.Tests/**` y el propio workflow; los UITests no lo disparan (`.github/workflows/android.yml:1-78`).

---

## 8. Pruebas de los ViewModels (`tests/MovilidadUrbana.MAUI.Tests`)

| Pieza | Qué hace | Fuente |
| --- | --- | --- |
| Proyecto | `net10.0`, NUnit 4.3.2; EF Core Sqlite 10.0.11 y CommunityToolkit.Mvvm 8.4.2 propios | `MovilidadUrbana.MAUI.Tests.csproj:8,14-24` |
| Archivos enlazados | `<Compile Include="..\..\src\MovilidadUrbana.MAUI\{Domain,Application,Infrastructure,Presentation}\**\*.cs" LinkBase="MAUI\…" />`: el proyecto Android no se puede referenciar sin el workload | `:27-30` |
| Lo que queda afuera | el comentario dice «Paginas/, Servicios/, Controles/ y MauiProgram» (nombres previos al renombre, [01](01_Arquitectura.md) §8.3); por los `Compile Include` también quedan afuera `Converters/`, `App`, `AppShell` y `Platforms/` | `:3-6`, `:27-30` |
| `TestEnvironment` | compone `AddInfrastructure` + `AddApplication` sobre `%TEMP%/movilidad-maui-<guid>.db`, inicializa la base, abre un ámbito («cada instancia es un dispositivo nuevo»), fija es-AR; al `Dispose` limpia pools y borra `.db/-wal/-shm` | `TestEnvironment.cs:17-53` |
| Dobles | `FakeNavigationService` (registra editores abiertos y `GoBackCount`) y `FakeAlertService` (registra avisos; `ConfirmResult` configurable) | `TestEnvironment.cs:55-71` |

### Los 18 casos (`grep -c '\[Test\]'`: 5 + 6 + 7)

| Clase | Casos |
| --- | --- |
| `LocalidadesViewModelTests` (5) | `CargaLasSembradasOrdenadas`, `FiltrarSinCoincidenciasYLimpiar`, `FiltraPorProvinciaYPorCodigoPostal`, `SinLocalidadesEsVacio`, `AbreElEditor` |
| `LocalidadEditorViewModelTests` (6) | `GuardarInvalidoMuestraErrores`, `CorregirUnCampoBorraSuError`, `GuardarNuevaAvisaYVuelve`, `ModificarActualiza`, `EliminarCanceladoNoBorra`, `EliminarConfirmadoBorra` |
| `EncuestaViewModelTests` (7) | `CargaLasLocalidadesDelAbm`, `NoAvanzaDelPaso1ConDatosInvalidos`, `CorregirElPaso2BorraSusErrores`, `VolverAtrasConservaLoCargado`, `RecorreYRegistra`, `NoRegistraConElPaso3Incompleto`, `NuevaEncuestaReinicia` |

Se corren con `dotnet test tests/MovilidadUrbana.MAUI.Tests`, sin teléfono; en CI, en `ci.yml` (job `compilacion`, TRX `maui-viewmodels.trx`) y en `android.yml` antes del APK.

Límite que la evidencia mostró: el defecto de la coma decimal pasó las 18, porque para el ViewModel «125» es una distancia válida; solo se vio tocando el teléfono (`/LAB/Lab-Documentos/Lab-Documentos/Guides/Testing/Lab-E2E.WebBlazor-Guides/Test-Guide/Pruebas-De-Interfaz-Por-Pantalla.md` §5.4).

---

## 9. Pruebas de interfaz con Appium (`tests/MovilidadUrbana.MAUI.UITests`)

| Pieza | Qué hace | Fuente |
| --- | --- | --- |
| Proyecto | `net10.0`, `Appium.WebDriver` 8.0.0, NUnit 4.3.2; **sin** referencia a la app | `MovilidadUrbana.MAUI.UITests.csproj:14-18` |
| `AppiumSession` (`[SetUpFixture]` en el namespace raíz) | una sesión `AndroidDriver` por corrida: `UIAutomator2`, `NoReset=true`, `appPackage`/`appActivity` `ar.lab.movilidadurbana.MainActivity`, `appWaitActivity *`, `appWaitDuration 60000`, `newCommandTimeout 300`; URL `APPIUM_URL` o `http://127.0.0.1:4723` | `Infrastructure/AppiumSession.cs:13-35` |
| Primera pantalla | `ActivateApp` (con `NoReset` el driver no trae al frente un proceso vivo) y reintento hasta 120 s mientras UIAutomator2 no consigue el árbol | `AppiumSession.cs:37-54` |
| Serie | `[assembly: NonParallelizable]` («un dispositivo es una sola pantalla») | `Infrastructure/AssemblyParallelism.cs` |
| `ScreenTestBase` | `FindById` (`MobileBy.Id`), `FindByText`, `Exists`, `WaitUntilGone`, `Tap`, `TypeText` (escribe y cierra teclado), `HideKeyboard` (espera que se cierre), `Pick` (Picker por texto), `ScrollIntoView`/`ScrollToText` (`UiScrollable`), `GetText`, `GoToTab` (vuelve atrás hasta 4 veces si quedó una página apilada), `WaitFor` (cada 500 ms, `Timeout` 60 s), `Capture` (PNG en `capturas/` adjunto al resultado) | `Infrastructure/ScreenTestBase.cs` |

### Los 5 casos (`grep -c '\[Test\]'`: 3 + 2)

| Clase | Caso | Recorrido |
| --- | --- | --- |
| `LocalidadesTests` | `FiltrarSinCoincidenciasYLimpiar` | escribe «zzz» → `estado-sin-resultados` → «Limpiar filtro» → desaparece |
| | `AltaInvalidaMuestraErrores` | agregar → guardar vacío → `aviso` y sigue en el editor → atrás |
| | `AltaEdicionYBaja` | alta «Prueba HHmmss» (Corrientes, 3450, 90000) → edita a «… B» → elimina y confirma → ya no está |
| `EncuestaTests` | `NoAvanzaConElPaso1Vacio` | `Assume` «Paso 1 de 3» → siguiente → `aviso`, sigue en paso 1 |
| | `RecorreRegistraYMuestraElResumen` | Ana Perez, 34, Corrientes → colectivo, «Todos los días» → 12,5, 45, «Trabajo» → registrar → «Encuesta completada» y «12,5 km» → nueva encuesta |

- No corren en CI: necesitan app instalada, servidor de Appium y `adb` viendo el dispositivo (`MovilidadUrbana.MAUI.UITests.csproj:3-5`). Se corren con `.devcontainer/dev.sh uitests`.
- Aislamiento: «cada prueba deja la lista como la encontró» (`LocalidadesTests.cs:5-8`). `RecorreRegistraYMuestraElResumen` registra una encuesta y no la borra: el contador de la sesión del dispositivo crece en cada corrida (deducido del código; la app no tiene baja de encuestas).

---

## 10. Evidencia

| Carpeta | Qué contiene | Datos clave |
| --- | --- | --- |
| `evidencia/2026-09-12-maui/` | 33 capturas `adb screencap` (numeradas 01–38 con huecos: faltan 04, 08, 14, 28, 30), `README.md` índice, `dispositivo.txt`, `toast-logcat.txt` | Motorola moto e6 play, Android 9, armeabi-v7a, 720×1440, densidad 320 (`dispositivo.txt`); el README enumera lo corregido a partir de las capturas |
| `evidencia/2026-09-13-uitests/` | `README.md`, `corrida-a-5-de-5.log` (5/5, 3 min 21 s), `corrida-b-5-de-5.log` (5/5, 3 min 5 s), `falsificacion.log` (1 rojo, 4 verdes), 7 capturas | Appium 3.7.0, `uiautomator2@8.6.4`, `Appium.WebDriver` 8.0.0; API 28; tres corridas previas en rojo por defectos de la suite |

`README.md` «Evidencia» (2026-09-12): build de la imagen `lab-e2e-maui-dev:net10` con APK Debug `android-arm` sin errores, y 18/18 de los ViewModels. `CHANGELOG.md` 2026-09-18: tras el renombre el APK compila y la suite Appium pasó 5/5.

---

## 11. Historia

| Commit | Fecha | Qué pasó |
| --- | --- | --- |
| `10ce735` | 2026-09-12 | Nace `MovilidadUrbana.MAUI`, `MAUI.Tests`, `.devcontainer/`, `android.yml` y `SinMaui.slnf`; las tres apps se vuelven independientes |
| `3e119b8` | 2026-09-13 | `MAUI.UITests` con Appium; `dev.sh uitests`; Node 22 + Appium 3 en la imagen; `[Register]` en `MainActivity` |
| `946d023` | 2026-09-18 | Renombre inglés/español (carpetas, clases, propiedades generadas por `[ObservableProperty]`/`[RelayCommand]`, bindings anidados); reintento de la primera pantalla de Appium |
| `e9dea2a` | 2026-09-18 | `cref` renombrados |

---

## 12. Rastros y desfasajes

Mapa de nombres anteriores (de `git ls-tree 3e119b8` y `git show -M 946d023`):

| Antes | Ahora |
| --- | --- |
| `Dominio/`, `Aplicacion/`, `Infraestructura/`, `Presentacion/`, `Paginas/`, `Servicios/`, `Controles/`, `Convertidores/` | `Domain/`, `Application/`, `Infrastructure/`, `Presentation/`, `Pages/`, `Services/`, `Controls/`, `Converters/` |
| `INavegador`, `IAvisos`, `NavegadorDeShell`, `AvisosDelSistema` | `INavigationService`, `IAlertService`, `ShellNavigationService`, `AlertService` |
| `SesionDelDispositivo`, `TecladoEnPantalla`, `EntradaDecimal`, `EstadoDeLista` | `DeviceSession`, `OnScreenKeyboard`, `DecimalEntry`, `ListState` |
| `Entorno` (MAUI.Tests) | `TestEnvironment` |
| `Infraestructura/` (UITests), `SesionDeAppium`, `PruebaDePantalla`, `ParalelismoDelEnsamblado` | `Infrastructure/`, `AppiumSession`, `ScreenTestBase`, `AssemblyParallelism` |
| `Abrir`, `Cerrar`, `Esperar`, `Elemento`, `PorTexto`, `Tocar`, `Escribir`, `Texto`, `IrAPestaña`, `Capturar` | `Open`, `Close`, `WaitFor`, `FindById`, `FindByText`, `Tap`, `TypeText`, `GetText`, `GoToTab`, `Capture` |

Los rastros en el código vigente de la app y de `MAUI.Tests` (`SesionDelDispositivo` en `SessionContext.cs:8`, «Dominio, Aplicacion, Infraestructura y Presentacion» en el `.csproj`, «Aplicacion e Infraestructura» en `MauiProgram.cs:15` y `DeviceSession.cs:11`, «`Paginas/`, `Servicios/`, `Controles/`» en el `.csproj` de pruebas, y los comentarios copiados de la web sobre «web o API», el circuito y WAL) están en [01](01_Arquitectura.md) §8.3. Los de evidencia y guías:

| Dónde | Rastro |
| --- | --- |
| `evidencia/2026-09-12-maui/README.md:28` | `EntradaDecimal` |
| `evidencia/2026-09-13-uitests/falsificacion.log` | `Texto("etiqueta-paso")`: registro de antes del renombre |
| `CHANGELOG.md` 2026-09-12 | `Dominio/`, `INavegador`, `IAvisos`: registro histórico |
| `/LAB/Lab-Documentos/Lab-Documentos/Guides/Testing/Lab-E2E.WebBlazor-Guides/Test-Guide/Pruebas-De-Interfaz-Por-Pantalla.md` §5.5 | `ScreenTestBase.Esperar`, `AppiumSession.Abrir`, `…Infraestructura` |
| `…/Test-Guide/Pruebas-Unitarias-Y-Arquitectura.md` §7.1 | cita `LinkBase="MAUI\Dominio"` en líneas 24-27; hoy es `MAUI\Domain` en las líneas 27-30 |

Desfasajes de otro tipo:

| Afirmación | Realidad | Fuente |
| --- | --- | --- |
| El Dockerfile se presenta como «Entorno de build/depuracion de GDA.Core.APP» | la receta es la de GDA.Core.APP («comparten caché de Docker y la clave de adb»); el encabezado no se adaptó | `Dockerfile:2`, `devcontainer.json:2-3` |
| «El .csproj pone InvariantGlobalization=false» / «el .csproj ya lo condiciona a macOS» | `MovilidadUrbana.MAUI.csproj` no tiene ni lo uno ni lo otro: es solo Android | `Dockerfile:24,56-57` |
| «Cada prueba deja los datos como los encontró» (README) | vale para localidades; la encuesta registrada no se deshace | `README.md` «La aplicación Android», `EncuestaTests.cs` |
| `WORKDIR /workspace` en la imagen | los dos caminos montan el repo en `/work` y trabajan ahí (`workspaceFolder`, `-w /work`) | `Dockerfile:97`, `devcontainer.json:7-8`, `dev.sh:46,50` |

Otros desfasajes que tocan a la app y tienen dueño en otro índice: `corrida-b-5-de-5.trx` no versionado y «Desde Visual Studio … cinco proyectos» → [05](05_Pruebas.md) §14; `MaxLength="80"` del nombre de localidad en el editor frente al máximo 60 → [02](02_Dominio-Y-Reglas.md) §8 (H2).

---

## No verificado

- Qué versión de `Microsoft.Maui.Controls` resuelve `$(MauiVersion)`: depende del workload instalado (sin versión fija en la imagen ni en `android.yml`).
- Qué ABI produce `android.yml` (no pasa `RuntimeIdentifier`).
- Las corridas reales de `android.yml` en GitHub: no se consultaron en este índice (ver [06](06_CI-Y-Workflows.md)).
- Que la imagen se siga construyendo igual hoy: Appium y Node 22 se instalan sin versión fija; las versiones 3.7.0 y 8.6.4 son las del 2026-09-13.
- Que `devcontainer.json` (VS Code) funcione igual que `dev.sh`: la evidencia registra solo corridas por `dev.sh`.
- El efecto del `WORKDIR /workspace` de la imagen: los dos caminos lo pisan con `/work`; no se probó otro uso.
