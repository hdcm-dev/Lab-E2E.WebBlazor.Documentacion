# 09 — Glosario

> **Propósito**: los términos propios del laboratorio —del dominio, de la sesión, de la interfaz, de las pruebas, de la CI y del vocabulario de las guías—, cada uno con el archivo donde se usa y el índice que lo desarrolla. No repite el detalle: define y remite.
>
> **Fuente primaria**: los archivos citados en la columna «Dónde se usa» (rutas relativas al repo fuente salvo las que empiezan con `/`, que son desde la raíz del workspace), `README.md`, `CHANGELOG.md` y las guías de `/LAB/Lab-Documentos/Lab-Documentos/Guides/Testing/Lab-E2E.WebBlazor-Guides/`. Ubicaciones confirmadas con `git grep` sobre `8fb4c3a`.
>
> **Vigencia**: versión 3.1, generada el 2026-10-25 sobre el commit `8fb4c3a` (2026-09-18).
>
> **Vecinos**: visión general en [00](00_MASTER-INDEX.md); el mapa de nombres viejos → nuevos del renombre está en [01](01_Arquitectura.md) §8.2 (acá solo se listan los términos vigentes).

Convención: los términos del dominio y los valores de estado van en español; los de arquitectura y piezas técnicas, en inglés ([01](01_Arquitectura.md) §8).

---

## 1. Dominio de Movilidad Urbana

| Término | Definición | Dónde se usa | Índice |
| --- | --- | --- | --- |
| **Movilidad Urbana** | La temática común de la web, la API y la app Android: ABM de localidades + encuesta de transporte | `src/MovilidadUrbana.{Web,ApiWeb,MAUI}/` | [02](02_Dominio-Y-Reglas.md) |
| **Localidad** | Entidad del ABM: `Nombre`, `Provincia`, `CodigoPostal`, `Habitantes`, con `SessionId` | `Domain/Entities/Localidad.cs` (×3 apps) | [02](02_Dominio-Y-Reglas.md) §2 |
| **ABM** | Alta, baja y modificación de localidades | `Components/Pages/Localidades.razor(.cs)`; `Controllers/LocalidadesController.cs`; `Pages/LocalidadesPage.xaml`, `LocalidadEditorPage.xaml` | [04](04_Interfaz-Y-Pantallas.md) §4 |
| **Encuesta** / `RespuestaDeEncuesta` | Asistente de tres pasos (persona, medios, distancia) y la respuesta registrada; guarda el **nombre** de la localidad, no su clave | `Domain/Entities/RespuestaDeEncuesta.cs`; `Application/Encuestas/` | [02](02_Dominio-Y-Reglas.md) §6.2 |
| **Catálogo** · clave / etiqueta | Listas fijas (`Provincias`, `Medios`, `Frecuencias`, `Motivos`); se persiste la clave (`colectivo`) y se muestra la etiqueta (`Colectivo`) | `Domain/Catalogos.cs` | [02](02_Dominio-Y-Reglas.md) §3 |
| **Medio** | Medio de transporte de la encuesta (6 en el catálogo) | `Domain/Catalogos.cs`; testid `medio-{clave}` | [02](02_Dominio-Y-Reglas.md) §3 |
| `*Rules` (regla) | Predicados y constantes del dominio (`NombreValido`, `EdadValida`, `TotalDePasos`) | `Domain/Rules/LocalidadRules.cs`, `EncuestaRules.cs` | [02](02_Dominio-Y-Reglas.md) §4 |
| `*Policy` · **requisito** | Texto para la persona derivado de las reglas, mostrado **antes** del intento («Entre 3 y 60 caracteres…») | `Application/Localidades/LocalidadPolicy.cs`, `Application/Encuestas/EncuestaPolicy.cs` | [02](02_Dominio-Y-Reglas.md) §5 |
| **Error** (de campo) | Mensaje del servicio **después** del intento, por clave de campo (`nombre`, `codigoPostal`…) | `Application/*/…Service.cs` | [02](02_Dominio-Y-Reglas.md) §7 |
| `Result` | Resultado de caso de uso: `IsSuccess`, `Message`, `Errors`; `Invalid` lleva «Revise los campos marcados en rojo.» | `Application/Result.cs` | [02](02_Dominio-Y-Reglas.md) §7.1 |
| `ValidarPaso` · `RegistrarAsync` · `AlternarMedio` | Acciones propias del caso (en español por regla) | `Application/Encuestas/EncuestaService.cs`, `EncuestaModel.cs` | [02](02_Dominio-Y-Reglas.md) §6.2 |
| **Ficha de revisión** · `ResumenDeEncuesta` / `CampoDeResumen` | Lista clave/etiqueta/valor ya formateada que se muestra al registrar | `Application/Encuestas/ResumenDeEncuesta.cs`; `Contracts/Encuestas.cs` (API) | [02](02_Dominio-Y-Reglas.md) §6.3 |
| **Siembra** · `SessionSeeder` | Corrientes y Resistencia cargadas en la primera lectura de una sesión | `Infrastructure/Persistence/SessionSeeder.cs` | [03](03_Sesiones-Y-Persistencia.md) §10 |

---

## 2. Sesión y persistencia

| Término | Definición | Dónde se usa | Índice |
| --- | --- | --- | --- |
| **Espacio de datos por sesión** | Cada fila lleva `SessionId` y todo repositorio filtra por él: aislamiento, no seguridad | `Infrastructure/Persistence/LocalidadRepository.cs`, `EncuestaRepository.cs` | [03](03_Sesiones-Y-Persistencia.md) §1 |
| `sesion-movilidad` | Cookie de sesión de la web (`SessionContext.CookieName`); la E2E repite el literal | `src/MovilidadUrbana.Web/Infrastructure/Sessions/SessionContext.cs`; `tests/MovilidadUrbana.E2ETests/Infrastructure/E2ETestBase.cs` línea 17 | [03](03_Sesiones-Y-Persistencia.md) §2 |
| `X-Sesion-Id` | Encabezado de sesión de la API; la respuesta siempre lo devuelve | `src/MovilidadUrbana.ApiWeb/Sessions/SessionHeaderMiddleware.cs` | [12](12_Api-REST.md) §5 |
| `sesion-dispositivo` · `DeviceSession` | Clave de `Preferences` y servicio que hacen del teléfono una sola sesión, con un ámbito DI para toda la vida de la app | `src/MovilidadUrbana.MAUI/Services/DeviceSession.cs` | [03](03_Sesiones-Y-Persistencia.md) §4 |
| `SessionContext` / `ISessionContext` | Contenedor scoped del id de sesión; `IsValid` = no vacío y ≤ 64 caracteres | `Infrastructure/Sessions/SessionContext.cs`; `Application/Abstractions/ISessionContext.cs` | [03](03_Sesiones-Y-Persistencia.md) §5 |
| **Identificador provisorio** | GUID que genera el constructor de `SessionContext` para que un ámbito sin sesión no escriba en un espacio compartido | `Infrastructure/Sessions/SessionContext.cs` (×3, comentario) | [03](03_Sesiones-Y-Persistencia.md) §5 |
| `SessionMiddleware` · **documento** | Middleware que emite la cookie solo al pedir un documento (`EsUnDocumento`: GET sin extensión, fuera de `/_framework` y `/_blazor`) | `src/MovilidadUrbana.Web/Sessions/SessionMiddleware.cs` | [03](03_Sesiones-Y-Persistencia.md) §2.2 |
| **Puente `App.razor` → `Routes`** | El id leído en el render estático viaja como parámetro `SessionId` al componente interactivo raíz | `src/MovilidadUrbana.Web/Components/App.razor`, `Routes.razor` | [03](03_Sesiones-Y-Persistencia.md) §2 |
| `Session` · **marca de siembra** | Fila de la tabla `Sessions` que indica que la sesión ya se sembró | `Domain/Entities/Session.cs` | [03](03_Sesiones-Y-Persistencia.md) §8 |
| `AppDbContext` | El único lugar que conoce el motor (tablas `Sessions`, `Localidades`, `Encuestas`) | `Infrastructure/Persistence/AppDbContext.cs` | [03](03_Sesiones-Y-Persistencia.md) §8 |
| `DatabaseInitializer` | `EnsureCreated` + `PRAGMA journal_mode=WAL` antes de atender | `Infrastructure/Persistence/DatabaseInitializer.cs` | [03](03_Sesiones-Y-Persistencia.md) §9 |
| `ConnectionStrings:BaseDeDatos` · `DefaultConnectionString` | Clave de configuración de la cadena SQLite y su valor por defecto `datos/movilidad.db` | `src/*/Program.cs`; `Infrastructure/DependencyInjection.cs` línea 15 | [03](03_Sesiones-Y-Persistencia.md) §7 |
| `datos/` · `datos-e2e/` | Carpetas (ignoradas) de las bases de `dotnet run` y de la app bajo prueba E2E | `.gitignore`; `TestAppServer.cs` | [03](03_Sesiones-Y-Persistencia.md) §7 |

---

## 3. Interfaz y template

| Término | Definición | Dónde se usa | Índice |
| --- | --- | --- | --- |
| **Template SDD** | Maqueta del Framework SDD aplicada sin librería: `Tokens.css` (valores) + `Componentes.css` (patrones `mq-`) | `src/*/wwwroot/css/`; `/IA/SDD/IA.SDD/Conocimiento/Knowledge-Template-*.md` | [11](11_Template-Y-Superficies.md) §1 |
| **Token** | Variable CSS del catálogo en `:root`; única fuente de color, tipografía y espaciado | `wwwroot/css/Tokens.css` | [11](11_Template-Y-Superficies.md) §3 |
| Clases `mq-` | Prefijo de las clases de patrón del template (`mq-shell`, `mq-btn`…) | `wwwroot/css/Componentes.css` | [11](11_Template-Y-Superficies.md) §2 |
| **Superficie** | Pantalla o región que la persona usa para un acto; unidad de diseño y de prueba | comentarios de `Pages/*.razor`; guías `E2E-Guide/` | [11](11_Template-Y-Superficies.md) §9, [07](07_Guias.md) |
| `SurfaceState` | Estado de una superficie, un bloque `@if` por valor: `Cargando`, `Vacio`, `FiltradoSinResultados`, `ConDatos`, `Indisponible`, `Enviando`, `ErrorDeEntrada`, `ErrorDeOperacion`, `Exito`, `Reconectando` | `src/MovilidadUrbana.Web/Components/Shared/SurfaceState.cs`; `src/WebBlazor.*/Theme/SurfaceState.cs` | [11](11_Template-Y-Superficies.md) §5 |
| `ListState` | Equivalente MAUI para la lista (`Cargando`, `ConDatos`, `Vacio`, `FiltradoSinResultados`) | `src/MovilidadUrbana.MAUI/Presentation/ListState.cs` | [13](13_App-Android.md) §4 |
| **Shell de trabajo** / **shell de acceso** · **lienzo** | Layout con barra lateral / layout sin navegación para el ingreso (`AuthLayout`, `.mq-lienzo`) | `Components/Layout/MainLayout.razor`; `src/WebBlazor.Login/Components/Layout/AuthLayout.razor` | [11](11_Template-Y-Superficies.md) §6 |
| **Banda** · `Band` / `BandTone` | Aviso persistente de resultado dentro de la superficie (no efímero); en MAUI, clave de estilo `Banda` | `Components/Shared/Band.razor`, `Tonos.cs`; `src/MovilidadUrbana.MAUI/Resources/Styles/Movilidad.xaml` | [11](11_Template-Y-Superficies.md) §4 |
| **Insignia** · `Badge` / `BadgeTone` · `Tone` | Par texto + tint (contadores); en Hola Mundo/Login un solo enum `Tone` | `Components/Shared/Badge.razor`, `Tonos.cs`; `src/WebBlazor.*/Theme/Tone.cs` | [11](11_Template-Y-Superficies.md) §4, §7 |
| `Grid` · **presentación visible** | Grilla con tabla y tarjetas apiladas siempre en el marcado; la prueba busca la fila **o** la tarjeta visible | `Components/Shared/Grid.razor`; `tests/MovilidadUrbana.E2ETests/LocalidadesTests.cs` (`PresentacionDe`) | [04](04_Interfaz-Y-Pantallas.md) §4.4 |
| `Wizard` · **paso direccionable** | Asistente; el paso se refleja en la URL (`/encuesta/{Paso}`, `replace: true`) sin poder saltearse | `Components/Shared/Wizard.razor`; `Components/Pages/Encuesta.razor.cs` | [04](04_Interfaz-Y-Pantallas.md) §5.3 |
| **Confirmación de primer / segundo grado** | Diálogo con verbo exacto / con confirmación escrita (implementada, sin uso) | `Services/IDialogService.cs` (`ConfirmationRequest`), `Components/Shared/Dialog.razor.cs`; `Localidades.razor.cs` | [04](04_Interfaz-Y-Pantallas.md) §6 |
| `DialogHost` · `IDialogService` | Host único de `<dialog>` nativo en el layout y servicio que lo abre | `Components/Shared/DialogHost.razor`, `Services/DialogService.cs` | [11](11_Template-Y-Superficies.md) §4 |
| **Sello de versión** · `VersionStamp` / `StampPlacement` | Versión resuelta en el host; «preliminar», «origen indeterminado»; ubicación `Pie`/`Lienzo` en la Base | `Components/Shared/VersionStamp.razor`, `Services/VersionIdentity.cs`; `src/WebBlazor.*/Theme/StampPlacement.cs` | [11](11_Template-Y-Superficies.md) §4 |
| `ReconnectionNotice` / `ReconnectModal` | Aviso de reconexión del circuito: banda no modal (web) / `<dialog>` conservado (Base) | `src/MovilidadUrbana.Web/Components/Shared/ReconnectionNotice.razor`; `src/WebBlazor.*/Components/Layout/ReconnectModal.razor` | [11](11_Template-Y-Superficies.md) §6 |
| **Desviación declarada** | Apartamiento explícito del template (render mode en la raíz, sin `DataAnnotationsValidator`, revisión como éxito, anchos en `ch`) | `README.md` §Desviaciones declaradas | [11](11_Template-Y-Superficies.md) §8 |
| `data-testid` | Atributo de localización de las pruebas web; no se traduce ni renombra | `src/*/Components/**/*.razor` | [04](04_Interfaz-Y-Pantallas.md) §7 |
| `AutomationId` → `resource-id` | Equivalente MAUI, que llega a Android como `ar.lab.movilidadurbana:id/<id>` | `src/MovilidadUrbana.MAUI/Pages/*.xaml`; `ScreenTestBase.cs` | [13](13_App-Android.md) §4 |
| **Testigo de hidratación** (o de interactividad) · `estado-app` / `data-interactivo` | Marca que pasa a `true` cuando el circuito está conectado; las pruebas lo esperan antes del primer click. Web: `RendererInfo.IsInteractive` en el layout; Hola Mundo/Login: `OnAfterRender` en la página | `src/MovilidadUrbana.Web/Components/Layout/MainLayout.razor`; `src/WebBlazor.*/Components/Pages/HolaMundo.razor`; `E2ETestBase.cs` | [05](05_Pruebas.md) §2.2, [10](10_Hola-Mundo-Y-Login.md) §2.3 |

---

## 4. Acceso (Login)

| Término | Definición | Dónde se usa | Índice |
| --- | --- | --- | --- |
| `auth_token` | Cookie de **autenticación** de Login (no es la de sesión de datos) | `src/WebBlazor.Login/Program.cs` | [10](10_Hola-Mundo-Y-Login.md) §3.1 |
| **Guard en tres capas** | Ruteo (`AuthorizeRouteView`), superficie (`OnInitializedAsync`) y acción (endpoint); actúa antes el middleware de cookies | `Components/Routes.razor`, `Pages/HolaMundo.razor`, `Endpoints/IdentityEndpoints.cs` (Login) | [10](10_Hola-Mundo-Y-Login.md) §4 |
| `SuperficieDeAcceso` | Constante `/login` de `LoginPath` | `src/WebBlazor.Login/Endpoints/IdentityEndpoints.cs`, `Program.cs` | [10](10_Hola-Mundo-Y-Login.md) §3.1 |
| **Catálogo de resultados** · `SignInResults` | Códigos (`credenciales-rechazadas`, `sesion-cerrada`, `sesion-requerida`, `datos-incompletos`) y sus textos | `src/WebBlazor.Login/Services/SignInResults.cs` | [10](10_Hola-Mundo-Y-Login.md) §3.3 |
| **Rechazo indiferenciado** | El mensaje de rechazo no dice qué campo falló; la prueba compara dos observaciones | `tests/WebBlazor.Login.E2ETests/LoginE2ETests.cs` | [10](10_Hola-Mundo-Y-Login.md) §5.3 |
| `DestinoSeguro` | Acepta solo `returnurl` relativas que empiezan con `/` (anti redirección abierta) | `src/WebBlazor.Login/Endpoints/IdentityEndpoints.cs` | [10](10_Hola-Mundo-Y-Login.md) §3.3 |

---

## 5. Pruebas

| Término | Definición | Dónde se usa | Índice |
| --- | --- | --- | --- |
| **Suite** | Cada uno de los siete proyectos de `tests/` | `tests/*/` | [05](05_Pruebas.md) §1 |
| **Fixture** (`[SetUpFixture]`) · `TestAppServer` | Arranque de ensamblado que instala el navegador, publica y levanta la web; debe estar en el namespace raíz | `tests/MovilidadUrbana.E2ETests/Infrastructure/TestAppServer.cs` | [05](05_Pruebas.md) §2.2 |
| **Sin fixture** | Hola Mundo y Login: la prueba apunta a una URL fija (`:5027`, `:5181`) y la app la levanta otro | `tests/WebBlazor.*.E2ETests/` | [10](10_Hola-Mundo-Y-Login.md) §5.1 |
| `E2ETestBase` | Base de las E2E web: contexto es-AR, cookie de sesión nueva, traza, espera de interactividad | `tests/MovilidadUrbana.E2ETests/Infrastructure/E2ETestBase.cs` | [05](05_Pruebas.md) §2.2 |
| `SurfaceTestBase` | Base de las pruebas de Login (`UrlBase`, `IngresarAsync`) | `tests/WebBlazor.Login.E2ETests/SurfaceTestBase.cs` | [10](10_Hola-Mundo-Y-Login.md) §5.3 |
| `ApiWebApplicationFactory` | `WebApplicationFactory<Program>` con SQLite temporal por clase | `tests/MovilidadUrbana.ApiWeb.Tests/ApiWebApplicationFactory.cs` | [12](12_Api-REST.md) §8 |
| `TestEnvironment` · `FakeNavigationService` / `FakeAlertService` | «Un dispositivo nuevo» por caso de MAUI.Tests y sus dobles | `tests/MovilidadUrbana.MAUI.Tests/TestEnvironment.cs` | [13](13_App-Android.md) §8 |
| **Archivos enlazados** · `LinkBase` | `Compile Include` de las capas MAUI en un proyecto `net10.0` (el Android no se referencia sin workload) | `tests/MovilidadUrbana.MAUI.Tests/MovilidadUrbana.MAUI.Tests.csproj` | [13](13_App-Android.md) §8 |
| `AppiumSession` · `ScreenTestBase` | Sesión UIAutomator2 única con `NoReset=true` y helpers de pantalla (`FindById`, `WaitFor`, `GoToTab`) | `tests/MovilidadUrbana.MAUI.UITests/Infrastructure/` | [13](13_App-Android.md) §9 |
| **Configuración** · `mobile-chrome` | Una entrada de la matriz E2E; `mobile-chrome` = chromium + `EMULAR_MOVIL=true` (descriptor Pixel 7) | `.github/workflows/e2e.yml`; `E2ETestBase.cs` | [06](06_CI-Y-Workflows.md) §3.2 |
| **Traza de fallidos** | `resultados/trazas/<caso>.zip`: se graba siempre y se guarda solo si falla (`TRAZAR=false` la apaga) | `E2ETestBase.cs` | [05](05_Pruebas.md) §9 |
| **Falsificación** | Corrida que se rompe a propósito para ver que la prueba se pone en rojo | `evidencia/*/…falsificacion*.log`; guías `Caso-Login-Page.md`, `Template-SDD-Aplicado.md` | [05](05_Pruebas.md) §10 |
| `REPETIR` | Variable de `scripts/pruebas.sh` para repetir la corrida y cazar intermitencias | `scripts/pruebas.sh` | [05](05_Pruebas.md) §7.2 |
| `PUBLICAR_ANTES_DE_PROBAR`, `URL_BASE`, `PUERTO`, `EMULAR_MOVIL`… | Variables que gobiernan el fixture y la base E2E | `TestAppServer.cs`, `E2ETestBase.cs`, `e2e.yml` | [05](05_Pruebas.md) §8 |
| **Evidencia** | Logs y capturas fechadas que respaldan lo afirmado | `evidencia/AAAA-MM-DD-*/` | [05](05_Pruebas.md) §10 |

---

## 6. CI, entorno y Android

| Término | Definición | Dónde se usa | Índice |
| --- | --- | --- | --- |
| **Escalera / escalón** | Hola Mundo → Login → Movilidad Urbana, en apps y en workflows | `README.md` líneas 83, 462; `.github/workflows/e2e-login.yml` línea 1 | [06](06_CI-Y-Workflows.md) §1 |
| **CI aprobada** (`ci-ok`) | Job resumen, único check pensado para la protección de rama | `.github/workflows/ci.yml` | [06](06_CI-Y-Workflows.md) §3.1 |
| **Reporte unificado** | Job que junta los TRX de la matriz en el resumen de la corrida | `.github/workflows/e2e.yml` | [06](06_CI-Y-Workflows.md) §3.2 |
| `aplicacion-publicada` | Artefacto con la web autocontenida que comparte la matriz | `.github/workflows/e2e.yml` | [06](06_CI-Y-Workflows.md) §4 |
| `i7infra-dev` / `i7infra-runner-dev` | Etiqueta y nombre del runner autoalojado (solo `publicar` de `e2e.yml`) | `.github/workflows/e2e.yml` línea 89; `README.md` §Runner | [06](06_CI-Y-Workflows.md) §5 |
| `SinMaui.slnf` | Filtro de solución sin la app Android: lo que compila CI | `Lab-E2E.WebBlazor.SinMaui.slnf` | [01](01_Arquitectura.md) §7 |
| `lab-e2e-maui-dev` · `dev.sh` · **devolver** | Contenedor Android y su script; `devolver` restituye el `adb` a `gda-core-app-dev` | `.devcontainer/dev.sh`, `devcontainer.json` | [13](13_App-Android.md) §7 |
| `DecimalEntry` | Entrada que acepta coma y punto (el teclado es-AR descartaba la coma) | `src/MovilidadUrbana.MAUI/Controls/DecimalEntry.cs` | [13](13_App-Android.md) §5 |
| `OnScreenKeyboard` · `AdjustResize` | Mantener la barra de acciones encima del teclado en la página apilada / modo de ventana | `src/MovilidadUrbana.MAUI/Services/OnScreenKeyboard.cs`; `App.xaml.cs`; `Platforms/Android/MainActivity.cs` | [13](13_App-Android.md) §5 |
| **moto e6 play** | Teléfono de la evidencia Android (Android 9, armeabi-v7a) | `evidencia/2026-09-12-maui/dispositivo.txt` | [13](13_App-Android.md) §10 |

---

## 7. Vocabulario de las guías

Términos que nacen en el corpus de `/LAB/Lab-Documentos/Lab-Documentos/Guides/Testing/Lab-E2E.WebBlazor-Guides/` y que el código cita en comentarios.

| Término | Definición | Dónde se usa | Índice |
| --- | --- | --- | --- |
| **Superficie verificable** | Marco conceptual del corpus: lo que la persona ve como unidad de prueba | `E2E-Guide/Marco-La-Superficie-Verificable.md` | [07](07_Guias.md) §2.1 |
| **Promesa** · **promesa negativa** | Lo que la superficie se compromete a hacer / a no hacer (p. ej. no revelar qué campo falló) | `E2E-Guide/Caso-Login-Page.md`, `Caso-HolaMundo-Page.md`; comentarios de `src/WebBlazor.*/Components/Pages/HolaMundo.razor`, `tests/WebBlazor.Login.E2ETests/LoginE2ETests.cs` | [07](07_Guias.md) §2.1, [10](10_Hola-Mundo-Y-Login.md) |
| **Acto divisible** | Acto que se recorre en tramos (la encuesta: tres pasos = una superficie) | `E2E-Guide/Caso-Encuesta-Page.md`, `Del-Requerimiento-Al-Caso.md` | [07](07_Guias.md) §2.1 |
| **Documento dueño** | Una corrección se hace en el documento dueño del tema; los demás enlazan | `E2E-Guide/Mapa-Del-Conjunto.md` §3.2 | [07](07_Guias.md) §2.4 |
| Marcas `[E: …]`, `[V]`, `[C]`, `[F: …]`, `[B: …]` | Citas de evidencia en las guías (la `[E:]` remite a un archivo del código) | guías de `E2E-Guide/` y `Test-Guide/` | [07](07_Guias.md) §4.2 |
| **Rastro** | Nombre previo al renombre `946d023`/`e9dea2a` que sigue en comentarios, mensajes o guías | ver inventario | [01](01_Arquitectura.md) §8.3 |
