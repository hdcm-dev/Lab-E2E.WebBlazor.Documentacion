# 08 — Decisiones y trampas ya pagadas

> **Propósito**: reunir el porqué de las decisiones no obvias y los errores que ya se encontraron y
> se resolvieron, para no revertirlos por «prolijidad» ni volver a pisarlos.
> **Fuente primaria**: `README.md` (secciones «Por qué las pruebas E2E son un proyecto de la
> solución», «Lo que cambia respecto del ejemplo estático», «Los workflows» y «Evidencia»),
> `CHANGELOG.md`, las cabeceras de `.devcontainer/dev.sh` y `Dockerfile`, y los comentarios del
> código citado.
> **Vigencia**: 2026-09-12, commit `10ce735`.

## Decisiones de fondo

### Playwright con el binding de .NET, no el runner de JavaScript

Se usan las vinculaciones oficiales `Microsoft.Playwright.NUnit` con un objetivo concreto: que las
pruebas se **descubran, ejecuten y depuren desde Visual Studio**, sin salir del IDE ni del lenguaje
de la aplicación.

Es una decisión con costo, y conviene tenerlo a la vista. El Explorador de pruebas de Visual Studio
soporta pruebas de JavaScript, pero solo de Mocha, Jasmine, Tape, Jest y Vitest: Playwright no está
en esa lista. A cambio de ganar el IDE se pierden funciones que solo existen en `@playwright/test`:
`--shard`, el reporter `blob` con `merge-reports` y el reporte HTML. Acá el reporte de cada
configuración es un TRX y el paralelismo lo maneja NUnit.

La alternativa —dejar las E2E fuera de la solución, en una carpeta `e2e/` con specs de TypeScript—
es la que eligió `dotnet/eShop`. **Las dos son defendibles**; esta prioriza el IDE.

### Tres aplicaciones independientes de Movilidad Urbana, con el código repetido

La web, la API y la app Android **no comparten proyectos**: cada una lleva `Dominio/`,
`Aplicacion/` e `Infraestructura/` como carpetas propias, y las tres copias son idénticas salvo el
`namespace`. El `README.md` lo declara: «el código se repite a propósito: cada proyecto tiene que
poder estudiarse, compilarse y llevarse por separado». Los proyectos por capa existieron unas horas
(`88e5caa`) y volvieron a carpetas el mismo día (`10ce735`, `CHANGELOG.md`). Lo que quedó de ese
paso es la separación en capas con registro propio (`AgregarAplicacion()`,
`AgregarInfraestructura(cadena)`) y los puntos de composición que solo componen.

El costo, a la vista: un cambio de regla se replica a mano en tres lugares y las unitarias cubren
solo la copia de la web ([05](05_Pruebas.md)). **No proponer «extraer lo común»**: es exactamente lo
que se deshizo. Un beneficio concreto: la `Infraestructura/` de la app Android se compila enlazada
en su proyecto de pruebas, cosa que un proyecto compartido con `FrameworkReference` a ASP.NET Core
no permitía — por eso `MiddlewareDeSesion` se mudó a `Web/Sesiones/`.

### Tres aplicaciones web de complejidad creciente, cada una con su forma

Hola Mundo y Login no tienen fixture, prueban contra una URL fija y tienen cada una su workflow, con
menos piezas que el de Movilidad Urbana. **No es una deuda**: es la escalera didáctica que declara
el `README.md` («para que la temática se pueda estudiar de a un escalón»). Uniformarlas destruiría
el escalón.

### Publicar e instalar navegadores en el fixture, no en el build

Atado al build, el paso queda a merced de que el entorno decida compilar: Visual Studio evalúa por
su cuenta si el proyecto está al día y cómo invocar targets de otro proyecto, y cuando esa decisión
no sale como se espera **no hay publicación y todas las pruebas mueren en `OneTimeSetUp`**. En el
fixture corre siempre y de la misma forma en consola, IDE y CI.

`dotnet publish` es incremental: cuando no cambió nada tarda un par de segundos. Se paga ese costo
una vez por corrida a cambio de no ejercitar nunca un binario viejo.

Lo mismo con el navegador: la vía documentada (`pwsh playwright.ps1 install`) exige PowerShell 7
—un producto aparte del PowerShell que trae Windows— y acordarse de correrlo. El paquete expone el
mismo instalador como API, y se instala solo el navegador de la corrida.

### `EnsureCreated` en lugar de migraciones

El laboratorio no versiona el esquema, y así el binario publicado arranca en cualquier máquina sin
pasos previos. No es una omisión: es lo apropiado para el alcance.

### La política de validación vive en el dominio, no en la vista

`EditForm` sin `DataAnnotationsValidator` en Movilidad Urbana: anotar el modelo de pantalla sería
«transcribir la política de validación en la vista». Lo que la regla del template protege —error por
campo asociado por `aria-describedby` y requisito visible antes del intento— se conserva por otra
vía (`Politica*.cs`). Hola Mundo, que no tiene dominio, sí usa anotaciones. Ver
[11](11_Template-Y-Superficies.md).

## Las seis diferencias con el ejemplo estático

Lo que sigue es lo que **aparece recién cuando la aplicación tiene servidor**. Las decisiones de
fondo —selectores por `data-testid`, nada de esperas fijas, cuatro configuraciones de navegador con
una móvil— se mantienen del laboratorio estático.

### 1. Hay que esperar a que la página sea interactiva

Una aplicación *interactive server* se entrega primero como HTML prerenderizado y recién después se
establece el circuito por WebSocket. En el medio los botones **se ven pero no responden**: un clic
que llegue antes de la conexión se pierde sin dejar rastro, y el síntoma es una prueba que falla de
manera intermitente y solo en las máquinas cargadas.

`MainLayout.razor` publica un testigo con `RendererInfo.IsInteractive`; `EsperarInteractivoAsync` de
`PruebaE2E.cs` lo espera antes de tocar nada. En Hola Mundo el mismo testigo cerró una intermitencia
de 1 en 8 — evidencia en `evidencia/2026-09-03-testigo-de-hidratacion/`.

### 2. El estado es del servidor, así que hay que aislarlo

Detalle propio de Blazor Server: **un circuito no tiene acceso a la petición HTTP** que lo originó,
así que la cookie no se puede leer desde una página. El identificador se lee en `App.razor` —que sí
se renderiza dentro de la petición— y se pasa como parámetro al componente raíz `Routes`, puente
entre el render estático y el interactivo. Mecanismo completo en
[03_Sesiones-Y-Persistencia.md](03_Sesiones-Y-Persistencia.md).

### 3. La aplicación hay que compilarla antes de probarla

En CI se publica **autocontenida** para `linux-x64`, así el binario no depende del runtime del
ejecutor, y **una sola vez** para que todas las configuraciones la reutilicen. En la máquina de
quien desarrolla alcanza con una publicación dependiente del framework.

El fixture admite las dos formas: usa el apphost nativo si está —`MovilidadUrbana.Web.exe` en
Windows, sin extensión en Linux y macOS— y si no arranca con `dotnet MovilidadUrbana.Web.dll`.
**El nombre fijo de Linux era justamente lo que hacía fallar el descubrimiento en Windows.**

Trampa que cuesta un rato encontrar: **ASP.NET Core toma el directorio actual como raíz de
contenido**. Si se lanza el binario desde otra carpeta, `wwwroot` no se encuentra, los recursos
estáticos se sirven **vacíos —con `200` y `Content-Length: 0`, no con `404`—** y el circuito nunca
arranca porque `blazor.web.js` llega en blanco. Por eso el fixture fija `WorkingDirectory` en la
carpeta de la publicación.

### 4. Menos JavaScript, menos intermitencia

En la versión estática hubo que corregir dos defectos alrededor del modal de Bootstrap: el clic que
llegaba durante la animación de apertura y el orden del manejador de `data-bs-dismiss`. Acá el
diálogo es el `<dialog>` nativo, abierto y cerrado por `ServicioDeDialogos` con la interoperabilidad
mínima de `mq-dialogo.js`: el confinamiento de foco y el cierre por Escape los trae el navegador, no
hay animación de apertura que esperar y esa clase de carrera no existe.

### 5. El enlace de datos tiene que escuchar el evento correcto

`FillAsync` dispara `input`, no `change`. Con el `@bind` por defecto —que escucha `onchange`— el
valor no llega al servidor hasta que el campo pierde el foco, y la validación rechaza un formulario
que en pantalla se ve completo. Los campos usan `@bind:event="oninput"` o `@oninput` directo — la
tabla exacta está en [04](04_Interfaz-Y-Pantallas.md).

### 6. Con el binding de .NET, el paralelismo llega hasta la clase

NUnit no paraleliza por defecto. Pero subirlo a `ParallelScope.Children` —casos en paralelo dentro
de una misma clase— rompe la integración de Playwright, que lleva un registro de servicios por
worker: la corrida falla con `The given key 'Browser' was not present in the dictionary` y
`Collection was modified; enumeration operation may not execute`.

El límite práctico es **`ParallelScope.Fixtures`**. Es una diferencia real con `fullyParallel: true`
del runner de JavaScript, que reparte caso por caso.

Otra trampa: un `[SetUpFixture]` cubre **su** namespace y los que cuelgan de él, nunca el de arriba.
Puesto en `MovilidadUrbana.E2ETests.Infraestructura` no se ejecuta para las pruebas de
`MovilidadUrbana.E2ETests`, y el síntoma es desconcertante —la URL base llega vacía y Playwright se
queja de la cookie—.

## Trampas de la app Android, ya pagadas

Todas están registradas en comentarios del código o en `evidencia/2026-09-12-maui/README.md`; el
detalle de cada pieza está en [13](13_App-Android.md).

| Trampa | Dónde se ve | Solución |
| --- | --- | --- |
| El teclado numérico de Android filtra caracteres según el idioma y puede descartar la coma: «12,5» llegaba como «125» y se registraba sin error | Captura `24-encuesta-paso3-completo.png` | `Controles/EntradaDecimal` + un mapeo de `EntryHandler` que fija `InputType` decimal y un `DigitsKeyListener` con `0123456789,.`; el ViewModel acepta coma o punto (`LeerDecimal`) |
| MAUI aplica su propio modo de teclado a la ventana (`Pan`) y pisa el `AdjustResize` del manifiesto: enfocar un campo bajo corre toda la pantalla y corta el encabezado | `App.xaml.cs` | `UseWindowSoftInputModeAdjust(Resize)` en el constructor de `App`, además del atributo de `MainActivity` |
| En una página **apilada** por Shell la ventana no se achica con el teclado; `SafeAreaEdges` deja un hueco que no se cierra y los insets del IME no llegan a la vista | `Servicios/TecladoEnPantalla.cs` | Medir en cada `GlobalLayout` cuánto del borde inferior de la barra quedó bajo la zona visible y corregir su margen por esa diferencia hasta converger; al desaparecer la página, margen cero |
| Android dibuja un subrayado propio bajo `Entry`, `Picker` y `SearchBar`, que dentro de la caja con borde del estilo «Campo» queda como una segunda línea | `MauiProgram.QuitarSubrayadoNativo` | `BackgroundTintList` transparente por handler; el `search_plate` del `SearchView` se resuelve por nombre porque el binding no expone su id |
| El teclado numérico deja tipear separadores de miles en «Habitantes» | `LocalidadEditorViewModel.LeerEntero` | Se conservan solo los dígitos |
| `CultureInfo.DefaultThreadCurrent*` no alcanza al hilo principal, que ya existe al arrancar | `MauiProgram.cs` | Se fija además `CultureInfo.CurrentCulture` / `CurrentUICulture` |
| El proyecto `net10.0-android` no se puede referenciar desde un proyecto de pruebas `net10.0` sin el workload | `MovilidadUrbana.MAUI.Tests.csproj` | Las carpetas `Dominio/`, `Aplicacion/`, `Infraestructura/` y `Presentacion/` se compilan como `<Compile Include=... LinkBase=...>`; queda fuera solo lo que toca la plataforma |
| El runner de `ci.yml` no tiene el workload de MAUI y la solución completa no compila allí | `Lab-E2E.WebBlazor.SinMaui.slnf` | CI compila el filtro; `android.yml` instala el workload y construye el APK aparte |
| Dos servidores de `adb` se disputan el mismo teléfono y el síntoma aparece en el otro contenedor | `.devcontainer/dev.sh` | `up` apaga el adb de `gda-core-app-dev` antes de levantar el propio; `devolver` lo restituye |
| Si el keystore de Debug se regenera, el APK nuevo no se instala sobre el anterior | `devcontainer.json` | Volumen nombrado `lab-maui-keystore` para `~/.local/share/Xamarin` |
| El nodo USB del teléfono no es escribible para el usuario normal del contenedor | `Dockerfile`, `dev.sh` | El servidor de adb corre como root (`docker exec -u 0`), con `sudo` sin contraseña para el arranque desde VS Code |
| Sin locales reales, el runtime de build y la app se quedan sin ICU útil | `Dockerfile` | `locale-gen` de `es_AR.UTF-8` y `en_US.UTF-8`; `LANG=es_AR.UTF-8` |
| Un Toast dura menos que un ciclo de captura y no se puede evidenciar por pantalla | `evidencia/2026-09-12-maui/toast-logcat.txt` | La prueba es la línea de `logcat` con `Toast#0 … producer=(…:ar.lab.movilidadurbana)` |

## Trampas menores, ya resueltas

| Trampa | Solución en el repositorio |
| --- | --- |
| La cookie de sesión se emitía también en css y js, que el navegador pide en paralelo, y la primera visita generaba varios identificadores | `MiddlewareDeSesion.EsUnDocumento` filtra por GET, sin extensión y fuera de `/_framework` y `/_blazor` |
| Borrar todas las localidades volvía a sembrarlas | Marca en la tabla `Sesiones` |
| Dos peticiones de la misma sesión sembraban a la vez | `try/catch (DbUpdateException)` en `SembradorDeSesion` |
| Con `EMULAR_MOVIL=true` la emulación podía caer en silencio a escritorio | `ContextOptions()` lanza si Playwright no conoce el descriptor `Pixel 7` |
| El número de workers estaba declarado en dos lados y podía divergir | Se quitó `[assembly: LevelOfParallelism(3)]`; vive solo en `NumberOfTestWorkers` |
| Las carpetas de solución de `Guides` apuntaban a rutas inexistentes | Se reordenaron el 2026-08-30, se pusieron al día el 2026-09-03 y se retiraron el 2026-09-09, cuando las guías se mudaron a `Lab-E2E.WebBlazor.Documentacion` |
| Los artefactos de Actions pierden el bit de ejecución | `chmod +x` antes de arrancar |
| El resumen de la encuesta variaba con el orden de tipeo | Los medios se guardan en el orden del catálogo |
| Leer una salida del proceso con el búfer de la otra llena trababa el `dotnet publish` | Se leen ambas en paralelo |
| `/dev/shm` a 64 MB mata Chromium a media corrida | **Medido**: a esta escala no ocurre. Si apareciera: `--disable-dev-shm-usage` o más `--shm-size` |
| `fs.inotify.max_user_instances` agotado en la máquina del autor: la aplicación moría con código 134 al construir su configuración | No es del laboratorio: correr con `DOTNET_USE_POLLING_FILE_WATCHER=1` (`README.md` §Evidencia) |
| Hola Mundo y Login probaban por https con un puerto fijo y ningún paso levantaba la aplicación: en su repositorio de origen su workflow tuvo 0 corridas verdes de 4 | URL `http` en los puertos de sus `launchSettings` y un workflow por proyecto que levanta la aplicación antes de probar (2026-09-12) |
| Dos workflows se llamaban `E2E` y compartían nombre de artefacto | Se retiró el copiado (`e2e_2.yml`); los nuevos tienen nombre y artefacto propios |
| La sección *Runner* del README decía que todo corría en `ubuntu-latest` | Corregido el texto (2026-09-12): `publicar` de `e2e.yml` usa el runner propio, y esa combinación es la que acumula las corridas en verde |

## Límites conocidos

- La ejecución desde el Explorador de pruebas de Visual Studio **no se verificó** (no hay Windows en
  la máquina del autor), incluido el paso previo que necesitan Hola Mundo y Login: arrancar la
  aplicación con su perfil `http`.
- Los workflows **sí se observaron corriendo** en GitHub Actions — ver
  [06_CI-Y-Workflows.md](06_CI-Y-Workflows.md).
- El runner autoalojado no admite jobs con `container:`: es él mismo un contenedor y no tiene montado
  el socket de Docker.
- Dos promesas de la Encuesta no tienen caso de prueba (paso direccionable y fallo al registrar) —
  ver [05](05_Pruebas.md).
- La app Android se recorrió en **un solo teléfono** (Motorola moto e6 play, Android 9,
  armeabi-v7a); `TecladoEnPantalla` está calibrado contra lo observado ahí. No hay pruebas de
  interfaz sobre Android: solo los 18 casos de ViewModels y las capturas de `evidencia/2026-09-12-maui/`.
- Las unitarias cubren la copia de las reglas de la web; las de la API y de Android se verifican
  indirectamente ([05](05_Pruebas.md)).
