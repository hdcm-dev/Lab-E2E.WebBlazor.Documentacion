# 13 — La aplicación Android (MovilidadUrbana.MAUI)

> **Propósito**: registrar qué es la app Android de Movilidad Urbana, cómo se compone, cómo maneja
> la sesión y el teclado, cómo se compila sin SDKs en el host y cómo se prueban sus ViewModels, para
> que un agente pueda tocarla sin abrir los `.xaml` ni improvisar un entorno de build.
> **Fuente primaria**: `src/MovilidadUrbana.MAUI/`, `tests/MovilidadUrbana.MAUI.Tests/`,
> `.devcontainer/` (`Dockerfile`, `devcontainer.json`, `dev.sh`), `.github/workflows/android.yml`,
> la sección «La aplicación Android» de `README.md` y `evidencia/2026-09-12-maui/`.
> **Vigencia**: 2026-09-12, commit `10ce735`.

## Qué es

La tercera aplicación de Movilidad Urbana: la misma temática —un ABM de localidades y una encuesta en
tres pasos— en **.NET MAUI 10 para Android, con XAML nativo y MVVM**. Dos módulos, uno por pestaña
—**Localidades** y **Encuesta**—, que hacen el papel de los dos controllers de la API. Es
**totalmente independiente**: trae sus propias capas, la base SQLite vive en el almacenamiento
privado de la app y **no habla con ningún servidor** (`AndroidManifest.xml` sin permiso `INTERNET`;
en Debug el SDK lo agrega por su cuenta para el depurador).

| Dato | Valor | Origen |
| --- | --- | --- |
| Target | `net10.0-android` solo («el laboratorio se construye en Linux, donde iOS y Mac Catalyst no compilan») | `.csproj` |
| Paquete | `ar.lab.movilidadurbana`, versión `1.0` (`ApplicationVersion` 1), título «Movilidad Urbana» | `.csproj` |
| API mínima | 23 («AndroidX de .NET 10 exige API 23 como mínimo») | `.csproj` |
| Paquetes | `Microsoft.Maui.Controls`, `CommunityToolkit.Mvvm` 8.4.2, `Microsoft.EntityFrameworkCore.Sqlite` 10.0.11, `Microsoft.Extensions.Logging.Debug` 10.0.11 | `.csproj` |
| Base | `movilidad.db` en `FileSystem.AppDataDirectory`, creada con el mismo `PreparadorDeBaseDeDatos` | `MauiProgram.cs` |
| Tema | Claro forzado (`UserAppTheme = Light`): «no se deriva un tema oscuro que nadie diseñó» | `App.xaml.cs` |
| Teclado | `WindowSoftInputMode = AdjustResize` en `MainActivity` **y** `UseWindowSoftInputModeAdjust(Resize)` en `App`, porque MAUI pisa el del manifiesto con `Pan` | `MainActivity.cs`, `App.xaml.cs` |

```
src/MovilidadUrbana.MAUI/
├── Dominio/, Aplicacion/, Infraestructura/   Las mismas tres capas de la web, en MovilidadUrbana.MAUI.* — ver 01, 02, 03
├── Presentacion/
│   ├── Abstracciones/     INavegador, IAvisos: la plataforma vista desde el ViewModel
│   ├── Localidades/       LocalidadesViewModel, LocalidadEditorViewModel, LocalidadItem
│   ├── Encuestas/         EncuestaViewModel, Opcion, OpcionElegible
│   └── EstadoDeLista.cs   Cargando · ConDatos · Vacio · FiltradoSinResultados
├── Paginas/               LocalidadesPage, LocalidadEditorPage, EncuestaPage (.xaml + .xaml.cs)
├── Servicios/             SesionDelDispositivo, NavegadorDeShell, AvisosDelSistema, TecladoEnPantalla
├── Controles/             EntradaDecimal
├── Convertidores/         TextoPresenteConverter, NegarConverter
├── Resources/             AppIcon, Splash, Images (svg de pestañas y «agregar»), Fonts (OpenSans), Styles/
├── Platforms/Android/     AndroidManifest.xml, MainActivity, MainApplication, colors.xml
├── App.xaml(.cs), AppShell.xaml(.cs), MauiProgram.cs
```

## Composición (`MauiProgram.CreateMauiApp`)

| Paso | Qué hace | Por qué |
| --- | --- | --- |
| Cultura `es-AR` en `DefaultThreadCurrent*` **y** en `CurrentCulture` | Los formatos del resumen y la lista son los de Argentina | El hilo principal ya existe: `Default*` solo alcanza a los nuevos |
| `ConfigureFonts` OpenSans Regular y Semibold | — | — |
| `QuitarSubrayadoNativo()` | `BackgroundTintList` transparente en `Entry`, `Picker` y `SearchBar` (la placa del `SearchView` se ubica por nombre `search_plate`) | Los campos van en una caja con borde («Campo»); el subrayado de Android quedaría como segunda línea |
| `AceptarComaDecimal()` | Para `EntradaDecimal`, `InputType` numérico decimal y `DigitsKeyListener("0123456789,.")`, enganchado a la clave `Keyboard` para correr después de ella | El teclado numérico puede descartar la coma según el idioma del sistema |
| `AgregarInfraestructura(cadena)` + `AgregarAplicacion()` | Las mismas dos extensiones que la web y la API | [01](01_Arquitectura.md) |
| `SesionDelDispositivo` singleton; `INavegador` → `NavegadorDeShell`; `IAvisos` → `AvisosDelSistema` | La plataforma detrás de dos interfaces | Así los ViewModels se prueban sin teléfono |
| ViewModels creados con `SesionDelDispositivo.Crear<T>()` | `LocalidadesViewModel` y `LocalidadEditorViewModel` transitorios; **`EncuestaViewModel` singleton** | Los servicios son de ámbito y el único ámbito ya tiene la sesión puesta; la encuesta a medio cargar sobrevive al cambio de pestaña |
| Tres páginas transitorias; `AddDebug()` en `DEBUG`; `PreparadorDeBaseDeDatos.Preparar` | — | — |

`AppShell` es un `TabBar` con dos `Tab` (rutas `localidades` y `encuesta`, `FlyoutBehavior=Disabled`,
chrome en el color de marca); su code-behind resuelve las páginas desde el `IServiceProvider` y
registra la ruta apilada `localidad` → `LocalidadEditorPage`.

## La sesión: el dispositivo entero

`Servicios/SesionDelDispositivo.cs`: el identificador se genera la primera vez, se guarda en
`Preferences` bajo `sesion-dispositivo` y se establece en el `ContextoDeSesion` de **un único
`IServiceScope`** que vive lo que vive la aplicación. Los datos sobreviven a cerrar la app. Es el
equivalente de la cookie de la web y del encabezado de la API ([03](03_Sesiones-Y-Persistencia.md)):
la siembra (Corrientes y Resistencia) aparece la primera vez que se toca la lista.

## Los tres ViewModels (`Presentacion/`)

Todos con CommunityToolkit.Mvvm (`ObservableObject`, `[ObservableProperty]`, `[RelayCommand]`).
**La validación es la del servicio de aplicación**: los mensajes de error y las claves son los mismos
que en la web y la API; el ViewModel solo reparte `errores["nombre"]` etc. en propiedades `Error*`.
**Corregir un campo borra su error** (`On<Campo>Changed` → `Error<Campo> = null`), en los dos
editores.

| ViewModel | Estado y comandos | Detalles |
| --- | --- | --- |
| `LocalidadesViewModel` (lista) | `Visibles`, `Provincias` (con «Todas las provincias» primero), `Texto`, `Provincia`, `Estado` (`EstadoDeLista`), `Refrescando`, `Resumen` («N localidades» / «N de M localidades»); `CargarAsync`, `AgregarAsync`, `EditarAsync(item)`, `LimpiarFiltro` | Busca por nombre (sin distinguir mayúsculas) o código postal (ordinal) y filtra por provincia **sobre lo ya traído**; ordena por nombre con la cultura actual; `Vacio` y `FiltradoSinResultados` distintos. Alta y edición se delegan al editor por `INavegador` |
| `LocalidadEditorViewModel` | `Id?`, `Nombre`, `Provincia?`, `CodigoPostal`, `Habitantes` (texto), cuatro `Error*`, `Aviso`, `Procesando`; `Titulo` («Nueva localidad» / «Editar localidad»); los cuatro `Requisito*` de `PoliticaDeLocalidades`; `GuardarAsync`, `EliminarAsync` (con `CanExecute = !Procesando`) | `Preparar(item?)` lo deja para alta o edición. `LeerEntero` conserva solo dígitos (el teclado deja tipear separadores de miles). Guardar bien → `IAvisos.MostrarAsync` (Toast) + `VolverAsync`; eliminar pide `ConfirmarAsync` primero |
| `EncuestaViewModel` | `Paso`, `Completada`, los campos como texto o `string?`, ocho `Error*`, `Aviso`, `Registradas`, `Procesando`; `Medios` (`OpcionElegible` con `Alternar`: **toda la fila** es el área táctil), `Frecuencias`, `Motivos`, `Localidades`, `Resumen`; derivados `EtiquetaDelPaso`, `TituloDelPaso`, `Progreso`, `Mostrar*`; `CargarAsync`, `Siguiente`, `Anterior`, `RegistrarAsync`, `NuevaEncuesta` | Hacia adelante valida el paso vigente (`AvisoDePasoIncompleto` = «Complete los datos del paso antes de continuar.»); hacia atrás nunca y conserva lo cargado; marcar un medio borra el error de «al menos uno»; `LeerDecimal` acepta coma o punto; registrada, pasa al estado de éxito con el resumen de `ResumenDeEncuesta` y el contador; `NuevaEncuesta` vuelve al paso 1 vacío. `CargarAsync` trae los nombres del ABM y descarta la localidad elegida si ya no existe |

Las páginas (`Paginas/*.xaml.cs`) son delgadas: `LocalidadesPage` recarga en `OnAppearing`
(refleja alta, edición o baja al volver del editor); `LocalidadEditorPage` implementa
`IQueryAttributable` para recibir el `LocalidadItem` (o `string.Empty` en un alta), llama a
`TecladoEnPantalla.MantenerVisible(this, BarraInferior)` y enfoca el nombre a los 250 ms en un alta;
`EncuestaPage` recarga en `OnAppearing` (las localidades pudieron cambiar en la otra pestaña) y hace
`ScrollToAsync(0,0)` al cambiar `Paso`, `Completada` o `Aviso`.

`AutomationId` presentes en el XAML (no hay pruebas de interfaz que los usen todavía): `buscar`,
`filtro-provincia`, `contador`, `lista-localidades`, `estado-vacio`, `estado-sin-resultados`,
`agregar`; `nombre`, `provincia`, `codigo-postal`, `habitantes`, `guardar`, `eliminar`, `aviso`;
`etiqueta-paso`, `edad`, `localidad`, `distancia`, `minutos`, `{Binding Clave}` por medio,
`anterior`, `siguiente`, `registrar`, `encuesta-completada`, `nueva-encuesta`.

## Diseño

Paleta de `Tokens.css` en `Resources/Styles/Colors.xaml` (`Marca #0F6E56`, `MarcaOscura #04342C`,
`MarcaTinte #E1F5EE`, `Superficie #FFFFFF`, `TextoSecundario`, más las claves `Primary*` del
andamiaje con los mismos valores) y estilos por rol en `Movilidad.xaml` (`Titulo`, `Rotulo`,
`Ayuda`, `Error`, `Campo`, `Desplegable`, `Tarjeta`, `BotonPrimario`, `BotonSecundario`,
`BotonPeligro`, `Banda`). Objetivos táctiles de 48 dp, acción principal fija abajo (`BarraInferior`
en el editor; «Anterior/Siguiente/Registrar» en la encuesta), borde del campo en rojo cuando tiene
error, `ProgressBar` de avance en la encuesta (`README.md` §La aplicación Android). La lista es un
`CollectionView` dentro de un `RefreshView`, con `EmptyView` que alterna indicador de carga, estado
vacío y estado sin resultados; el editor es una página apilada con `Shell.TabBarIsVisible=False`.

## El teclado en la página apilada (`Servicios/TecladoEnPantalla.cs`)

En las páginas raíz de las pestañas alcanza con `AdjustResize`. En una página apilada por Shell la
ventana **no se achica** (verificado en el moto e6 play), `SafeAreaEdges` deja un hueco que no se
cierra al ocultar el teclado y los insets del IME no llegan a la vista. Lo estable es **medir**: en
cada `GlobalLayout` del `DecorView` se compara el borde inferior de la barra con
`GetWindowVisibleDisplayFrame` y se corrige `Margin.Bottom` por la diferencia (convertida por
densidad) hasta converger; al desaparecer la página, el margen vuelve a cero. Capturas `36`, `37` y
`38` de `evidencia/2026-09-12-maui/`.

## Pruebas: 18 casos sin teléfono (`tests/MovilidadUrbana.MAUI.Tests`)

El proyecto Android es `net10.0-android` y no se puede referenciar desde `net10.0` sin el workload,
así que el `.csproj` compila `Dominio/`, `Aplicacion/`, `Infraestructura/` y `Presentacion/` de la
app como **archivos enlazados** (`<Compile Include="..\..\src\MovilidadUrbana.MAUI\<capa>\**\*.cs"
LinkBase="MAUI\<capa>">`). Queda fuera solo lo que toca la plataforma: `Paginas/`, `Servicios/`,
`Controles/` y `MauiProgram`. Paquetes: NUnit 4.3.2 y adaptador 5.0.0, EF Core SQLite 10.0.11,
CommunityToolkit.Mvvm 8.4.2.

`Entorno.cs` compone las capas reales como la app —`AgregarInfraestructura` + `AgregarAplicacion` +
`PreparadorDeBaseDeDatos`— sobre un SQLite propio en `%TEMP%/movilidad-maui-{guid}.db`, fija `es-AR`
y abre un ámbito: «cada instancia es un dispositivo nuevo». Dobles: `NavegadorFalso` (registra
`EditoresAbiertos` y cuenta `Vueltas`) y `AvisosFalsos` (registra `Mostrados`; `RespuestaAConfirmar`
configurable). `Dispose` limpia pools y borra el archivo con `-wal` y `-shm`.

| Clase | Casos |
| --- | --- |
| `LocalidadesViewModelTests` (5) | Carga las sembradas ordenadas · filtrar sin coincidencias y limpiar · filtra por provincia y por código postal · sin localidades es `Vacio` · abre el editor |
| `LocalidadEditorViewModelTests` (6) | Guardar inválido muestra errores · corregir un campo borra su error · guardar nueva avisa y vuelve · modificar actualiza · eliminar cancelado no borra · eliminar confirmado borra |
| `EncuestaViewModelTests` (7) | Carga las localidades del ABM · no avanza del paso 1 con datos inválidos · corregir el paso 2 borra sus errores · volver atrás conserva lo cargado · recorre y registra · no registra con el paso 3 incompleto · nueva encuesta reinicia |

Las corren `ci.yml` (job `compilacion`, después de las de la API) y `android.yml` (antes de instalar
el workload). Verificado el 2026-09-12: 18/18 en la máquina del autor (`README.md` §Evidencia) y
en las dos corridas de GitHub Actions sobre `10ce735` ([06](06_CI-Y-Workflows.md)).

## Cómo se compila: el devcontainer

Compilar pide el workload `maui-android`, JDK 17 y el SDK de Android. Para no instalar nada en el
host está `.devcontainer/`:

| Pieza | Qué es |
| --- | --- |
| `Dockerfile` | `mcr.microsoft.com/dotnet/sdk:10.0` + OpenJDK 17 headless + cmdline-tools de Android con `platforms;android-36` y `-35`, `build-tools;36.0.0` y `35.0.0` + `dotnet workload install maui-android`; locales `es_AR`/`en_US`; usuario `dev` con el UID/GID del host y `sudo` sin contraseña (el servidor de `adb` necesita root para el nodo USB). La receta es la de `GDA.Core.APP`: comparten caché de Docker y la clave de `adb` |
| `devcontainer.json` | Contenedor `lab-e2e-maui-dev`, privilegiado, con `/dev/bus/usb` montado y tres volúmenes nombrados: `lab-maui-nuget`, `gda-app-adbkeys` (la clave RSA que el teléfono ya autorizó) y `lab-maui-keystore` (el keystore de Debug: si se regenera, el APK nuevo no se instala sobre el anterior). Extensiones `dotnet-maui` y `csdevkit`; se abre con **Dev Containers: Reopen in Container** |
| `dev.sh` | Orquesta desde el host: `up` (construye la imagen `lab-e2e-maui-dev:net10` si falta, apaga el `adb` de `gda-core-app-dev` si lo tenía, levanta el contenedor y arranca `adb` como root), `devices`, `build` (`dotnet build -c Debug -f net10.0-android -p:AndroidPackageFormat=apk -p:RuntimeIdentifier=$ABI -p:EmbedAssembliesIntoApk=true`), `install` (`adb install -r` del `*-Signed.apk`), `run` (instala y abre con `monkey`), `logs` (`logcat` del proceso), `down`, `devolver` (apaga y le devuelve el `adb` al otro contenedor) |

`ABI` es `android-arm` (armeabi-v7a, la del teléfono de prueba) por defecto; `ABI=android-arm64
.devcontainer/dev.sh run` compila para 64 bits. «El teléfono es un recurso único: dos servidores de
adb se lo disputan y el síntoma aparece en el otro» (cabecera de `dev.sh`); mientras este contenedor
es el dueño, los medios de observación del workspace se usan con `MEDIOS_ADB_OWNER=lab-e2e-maui-dev`.

En CI, `android.yml` instala el workload en `ubuntu-latest` y publica el APK de Release como
artefacto `movilidad-urbana-apk` (14 días), firmado con la clave de depuración del runner
([06](06_CI-Y-Workflows.md)). La solución completa incluye el proyecto; `ci.yml` compila
`Lab-E2E.WebBlazor.SinMaui.slnf`, que lo excluye.

## Evidencia

`evidencia/2026-09-12-maui/`: 33 capturas por `adb screencap` en un **Motorola moto e6 play**
(Android 9, armeabi-v7a, 720×1440, densidad 320 — `dispositivo.txt`), con el APK Debug del
devcontainer instalado por USB, y su `README.md` con lo que muestra cada una: lista sembrada,
filtrado sin resultados y filtro limpio, editor con errores (con y sin borde rojo, iteración previa
y final), selector de provincia, alta de Goya, edición, confirmación y cancelación de baja, los
tres pasos de la encuesta con sus errores, el selector de localidad, el resumen con «12,5 km», nueva
encuesta, y el teclado con «Guardar» encima en la página apilada. `24-encuesta-paso3-completo.png`
documenta el defecto de la coma («125») que corrige `EntradaDecimal`; `33` y `35`, la versión final.
`toast-logcat.txt` prueba el Toast del alta por la línea de `logcat`.

## Lo que no tiene

- Sincronización con la web o la API: los datos viven solo en el teléfono.
- Pruebas de interfaz (Appium, MAUI UITest o similares): los `AutomationId` están, sin consumidor.
- iOS, Mac Catalyst ni Windows: el `.csproj` declara solo `net10.0-android`.
- Tema oscuro.
- Firma de tienda: el APK de `android.yml` va con la clave de depuración del runner.

## Cómo verificar todo esto

| Afirmación | Comprobación |
| --- | --- |
| Las capas son copia de las de la web | `diff -r src/MovilidadUrbana.Web/Dominio src/MovilidadUrbana.MAUI/Dominio` (solo `namespace`) |
| Los 18 casos | `dotnet test tests/MovilidadUrbana.MAUI.Tests` (sin workload ni teléfono) |
| Las capas van enlazadas | `grep -n Compile tests/MovilidadUrbana.MAUI.Tests/MovilidadUrbana.MAUI.Tests.csproj` |
| Sin permisos de red | `cat src/MovilidadUrbana.MAUI/Platforms/Android/AndroidManifest.xml` |
| El APK se construye | `.devcontainer/dev.sh build` (imagen `lab-e2e-maui-dev:net10`) |
| Qué teléfono se usó | `cat evidencia/2026-09-12-maui/dispositivo.txt` |
