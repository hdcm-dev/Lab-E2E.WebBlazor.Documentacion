# 01 — Arquitectura

> **Propósito**: cómo se reparten `Domain/`, `Application/` e `Infrastructure/` (más la presentación) dentro de cada una de las tres aplicaciones de Movilidad Urbana, cómo las compone cada `Program.cs` y `MauiProgram.cs` (y los `Program.cs` de Hola Mundo y Login), y cómo se aplica en el código la convención «arquitectura en inglés, dominio en español», con los rastros que dejó el renombre.
>
> **Fuente primaria**: `src/MovilidadUrbana.Web/`, `src/MovilidadUrbana.ApiWeb/`, `src/MovilidadUrbana.MAUI/` (carpetas de capa, `*.csproj`, `Program.cs`, `MauiProgram.cs`, `App.xaml.cs`, `AppShell.xaml.cs`), `src/WebBlazor.HolaMundo/Program.cs`, `src/WebBlazor.Login/Program.cs`, `tests/*/*.csproj`, `Lab-E2E.WebBlazor.sln`, `Lab-E2E.WebBlazor.SinMaui.slnf`, `README.md` (§Estructura, §Convención de nombres), `CHANGELOG.md` (entradas 2026-09-12 y 2026-09-18); historia: commits `0516139`, `88e5caa`, `10ce735`, `946d023`, `e9dea2a`. Guía de la regla: `/LAB/Lab-Documentos/Lab-Documentos/Guides/Testing/Lab-E2E.WebBlazor-Guides/Nomenclatura-Convensiones-Arquitecture-Dot-Net.md`.
>
> **Vigencia**: versión 3.1, generada el 2026-10-25 sobre el commit `8fb4c3a` (2026-09-18).
>
> **Vecinos**: visión general, stack y puertos en [00](00_MASTER-INDEX.md) · qué hacen las entidades, reglas y casos de uso en [02](02_Dominio-Y-Reglas.md) · sesión, base y repositorios por dentro en [03](03_Sesiones-Y-Persistencia.md) · pantallas web en [04](04_Interfaz-Y-Pantallas.md) · suites en [05](05_Pruebas.md) · por qué y trampas en [08](08_Decisiones-Y-Trampas.md) · forma constructiva de las superficies en [11](11_Template-Y-Superficies.md) · API en [12](12_Api-REST.md) · app Android en [13](13_App-Android.md) · Login y Hola Mundo en [10](10_Hola-Mundo-Y-Login.md).

---

## 1. Mapa: cinco aplicaciones, dos formas de organizarse

| Proyecto | SDK / TFM | Capas propias | Presentación | Referencia a otro proyecto |
| --- | --- | --- | --- | --- |
| `src/MovilidadUrbana.Web` | `Microsoft.NET.Sdk.Web` · `net10.0` | `Domain/`, `Application/`, `Infrastructure/` | `Components/` (Blazor Server), `Sessions/`, `Services/`, `Theme/`, `wwwroot/` | ninguna |
| `src/MovilidadUrbana.ApiWeb` | `Microsoft.NET.Sdk.Web` · `net10.0` | `Domain/`, `Application/`, `Infrastructure/` | `Controllers/`, `Contracts/`, `Sessions/` | ninguna |
| `src/MovilidadUrbana.MAUI` | `Microsoft.NET.Sdk` + `UseMaui` · `net10.0-android` | `Domain/`, `Application/`, `Infrastructure/` | `Presentation/` (ViewModels), `Pages/`, `Services/`, `Controls/`, `Converters/`, `Resources/`, `Platforms/Android/` | ninguna |
| `src/WebBlazor.HolaMundo` | `Microsoft.NET.Sdk.Web` · `net10.0` | **sin capas** | `Components/`, `Services/`, `Theme/`, `wwwroot/` | ninguna |
| `src/WebBlazor.Login` | `Microsoft.NET.Sdk.Web` · `net10.0` | **sin capas** | `Components/`, `Endpoints/`, `Services/`, `Theme/`, `wwwroot/` | ninguna |

Fuente: los cinco `*.csproj` (ninguno tiene `ProjectReference`) y `README.md` §Estructura. Los comentarios de cabecera de los tres `.csproj` de Movilidad Urbana lo declaran: «Es un proyecto independiente: trae sus propias capas … y no referencia a ningún otro proyecto de la solución».

Paquetes por aplicación (de los `.csproj`):

| Proyecto | Paquetes |
| --- | --- |
| Web | `Microsoft.EntityFrameworkCore.Sqlite` 10.0.11 |
| ApiWeb | `Microsoft.EntityFrameworkCore.Sqlite` 10.0.11, `Microsoft.AspNetCore.OpenApi` 10.0.11, `Scalar.AspNetCore` 2.17.3 · `GenerateDocumentationFile=true`, `NoWarn CS1591`, `InternalsVisibleTo MovilidadUrbana.ApiWeb.Tests` |
| MAUI | `Microsoft.Maui.Controls` `$(MauiVersion)`, `Microsoft.Extensions.Logging.Debug` 10.0.11, `Microsoft.EntityFrameworkCore.Sqlite` 10.0.11, `CommunityToolkit.Mvvm` 8.4.2 · `ApplicationId ar.lab.movilidadurbana`, `SupportedOSPlatformVersion 23.0` |
| HolaMundo, Login | ninguno (solo el framework compartido) |

Las tres webs llevan `BlazorDisableThrowNavigationException=true`.

---

## 2. Árbol de capas (idéntico en las tres apps de Movilidad Urbana)

```
<App>/                                   espacio de nombres raíz: MovilidadUrbana.<Web|ApiWeb|MAUI>
├── Domain/                              no depende de nada (solo System.Text.RegularExpressions)
│   ├── Catalogos.cs
│   ├── Entities/   Localidad, RespuestaDeEncuesta, Session
│   └── Rules/      LocalidadRules, EncuestaRules
├── Application/                         depende de Domain
│   ├── Abstractions/  ILocalidadRepository, IEncuestaRepository, ISessionContext
│   ├── Localidades/   LocalidadService, LocalidadModel, LocalidadPolicy
│   ├── Encuestas/     EncuestaService, EncuestaModel, EncuestaPolicy, ResumenDeEncuesta
│   ├── Result.cs
│   └── DependencyInjection.cs           AddApplication()
└── Infrastructure/                      depende de Application.Abstractions y Domain.Entities + EF Core
    ├── Persistence/   AppDbContext, DatabaseInitializer, SessionSeeder,
    │                  LocalidadRepository, EncuestaRepository
    ├── Sessions/      SessionContext
    └── DependencyInjection.cs           AddInfrastructure(connectionString)
```

Conteo real (`find … -name '*.cs'`): `Domain/` 6, `Application/` 12, `Infrastructure/` 7 → **25 archivos por app**. Contenido de entidades, reglas y casos de uso: ver [02](02_Dominio-Y-Reglas.md); persistencia y sesión: ver [03](03_Sesiones-Y-Persistencia.md).

### 2.1 Código repetido a propósito

Comparando las tres copias con el espacio de nombres normalizado (`diff` tras reemplazar `MovilidadUrbana.<App>`):

| Archivos | Resultado |
| --- | --- |
| 24 de los 25 | **idénticos** entre Web, ApiWeb y MAUI, comentarios incluidos |
| `Infrastructure/Sessions/SessionContext.cs` | difiere: la web tiene además `CookieName = "sesion-movilidad"`; cambian los comentarios (quién fija el valor). Detalle en [03](03_Sesiones-Y-Persistencia.md) |

Motivo declarado: «El código se repite a propósito: cada proyecto tiene que poder estudiarse, compilarse y llevarse por separado» (`README.md` §Estructura; `CHANGELOG.md` 2026-09-12 «Tres aplicaciones independientes»). Consecuencia: un cambio de regla hay que hacerlo **tres veces**; nada en la solución avisa si las copias divergen (no hay prueba ni script que compare las tres; verificado por ausencia en `tests/`, `scripts/` y `.github/workflows/`).

Por ser copias, varios comentarios hablan de otra app (ver §8.3).

---

## 3. Regla de dependencias

```
            ┌───────────────────────── presentación (por app) ─────────────────────────┐
            │ Web: Components/, Sessions/, Services/   ApiWeb: Controllers/, Sessions/ │
            │ MAUI: Presentation/, Pages/, Services/                                   │
            └───────────────┬───────────────────────────────────────┬──────────────────┘
                            │ usa servicios                          │ composición: conoce
                            ▼                                        ▼ SessionContext concreto
   Domain ◄──────── Application ◄──────────────────────────── Infrastructure
 (Entities,         (Services, Models, Policies,               (EF Core/SQLite,
  Rules,             Result, Abstractions)                      repositorios, siembra,
  Catalogos)                                                    SessionContext)
```

Verificado por los `using` de cada capa (`grep '^using'` por carpeta, las tres apps dan lo mismo):

| Capa | Importa |
| --- | --- |
| `Domain/` | `System.Text.RegularExpressions` |
| `Application/` | `Domain`, `Domain.Entities`, `Domain.Rules`, sus propios `Application.Abstractions`/`.Encuestas`/`.Localidades`, `Microsoft.Extensions.DependencyInjection` |
| `Infrastructure/` | `Application.Abstractions`, `Domain.Entities`, sus propios `Infrastructure.Persistence`/`.Sessions`, `Microsoft.EntityFrameworkCore*`, `Microsoft.Data.Sqlite`, `Microsoft.Extensions.DependencyInjection` |
| `MAUI/Presentation/` | `Application.*`, `Domain`, `Domain.Rules`, `CommunityToolkit.Mvvm.*` (no `Infrastructure`) |

Ninguna capa de `Infrastructure/` referencia ASP.NET Core: el middleware de sesión salió de ahí y vive en `Sessions/` de cada web (`src/MovilidadUrbana.Web/Sessions/SessionMiddleware.cs` líneas 5-6; `CHANGELOG.md` 2026-09-12: «la capa de infraestructura de cada aplicación ya no referencia `Microsoft.AspNetCore.App`»). Eso es lo que permite que las mismas carpetas compilen en `net10.0-android`.

### 3.1 Qué la hace cumplir y qué no

| Mecanismo | ¿Hace cumplir la regla? |
| --- | --- |
| Proyectos separados | **No**: las capas son carpetas y espacios de nombres dentro de un único ensamblado por app; el compilador permitiría que `Domain/` usara `Infrastructure/` |
| `MovilidadUrbana.MAUI.Tests` | **Sí, en parte**: compila `Domain/`, `Application/`, `Infrastructure/` y `Presentation/` de la app Android como archivos enlazados en `net10.0` (`tests/MovilidadUrbana.MAUI.Tests/MovilidadUrbana.MAUI.Tests.csproj`). Si una de esas carpetas usara una API de MAUI (`Preferences`, `FileSystem`), la prueba dejaría de compilar. La guía lo llama «la regla de dependencia haciéndose cumplir» (`/LAB/Lab-Documentos/Lab-Documentos/Guides/Testing/Lab-E2E.WebBlazor-Guides/Test-Guide/Pruebas-Unitarias-Y-Arquitectura.md` §7.2) |
| Pruebas de arquitectura (NetArchTest o similar) | no existen |

### 3.2 Excepciones observadas a «la presentación usa servicios»

| Dónde | Qué toca | Fuente |
| --- | --- | --- |
| `Components/App.razor` (web) | inyecta `Infrastructure.Sessions.SessionContext` concreto | `src/MovilidadUrbana.Web/Components/App.razor` línea 1 |
| `Components/Routes.razor` (web) | inyecta `SessionContext` concreto y llama `Set` | `src/MovilidadUrbana.Web/Components/Routes.razor` líneas 19-20 (`[Inject]`) y 23-26 (`Set`) |
| `Sessions/SessionMiddleware.cs`, `Sessions/SessionHeaderMiddleware.cs` | reciben `SessionContext` concreto por parámetro de `InvokeAsync` | ambos archivos |
| `Services/DeviceSession.cs` (MAUI) | resuelve `SessionContext` concreto | `src/MovilidadUrbana.MAUI/Services/DeviceSession.cs` línea 30 |
| `LocalidadesController` (API) | recibe `ILocalidadRepository` además de `LocalidadService` y lo usa directo para leer: `GetById` (línea 32), ubicar la creada tras el alta con `GetAllAsync` (47), comprobar que exista antes del `PUT` (60) y releer la modificada (67) | `src/MovilidadUrbana.ApiWeb/Controllers/LocalidadesController.cs` líneas 13-15 |

Las cuatro primeras son de composición (fijar la sesión). La quinta es el único lugar donde la presentación salta el caso de uso para leer: `LocalidadService` no expone un `GetByIdAsync` y `SaveAsync` devuelve un `Result` sin la entidad (`src/MovilidadUrbana.ApiWeb/Application/Localidades/LocalidadService.cs`).

---

## 4. Registro por capa

Cada capa expone una clase estática `DependencyInjection` con su método de extensión; los `Program.cs` solo componen.

| Método | Archivo | Registra | Vida |
| --- | --- | --- | --- |
| `AddApplication()` | `Application/DependencyInjection.cs` | `LocalidadService`, `EncuestaService` (clases concretas, sin interfaz) | Scoped |
| `AddInfrastructure(string connectionString)` | `Infrastructure/DependencyInjection.cs` | `AddDbContextFactory<AppDbContext>(UseSqlite)` | factory (singleton por defecto de EF) |
| | | `SessionContext` + `ISessionContext` → la misma instancia | Scoped |
| | | `SessionSeeder` | Scoped |
| | | `ILocalidadRepository → LocalidadRepository`, `IEncuestaRepository → EncuestaRepository` | Scoped |
| constante | `Infrastructure/DependencyInjection.cs` línea 15 | `DefaultConnectionString = "Data Source=datos/movilidad.db;Default Timeout=30"` | — |

Fuente: `src/MovilidadUrbana.Web/Application/DependencyInjection.cs`, `src/MovilidadUrbana.Web/Infrastructure/DependencyInjection.cs` (las otras dos apps, idénticas). Por qué factory y no `DbContext` de ámbito: ver [03](03_Sesiones-Y-Persistencia.md) §6.

Las dos capas exponen una clase llamada igual (`DependencyInjection`): por eso los `Program.cs` califican la constante con el nombre completo (`MovilidadUrbana.Web.Infrastructure.DependencyInjection.DefaultConnectionString`, `src/MovilidadUrbana.Web/Program.cs` línea 23). Era un `CS0104` del renombre (`CHANGELOG.md` 2026-09-18; guía de nomenclatura §4.4).

---

## 5. Composición de cada host

### 5.1 `src/MovilidadUrbana.Web/Program.cs` (54 líneas)

| Paso | Líneas | Qué |
| --- | --- | --- |
| Cultura | 13-15 | `es-AR` fija en `DefaultThreadCurrentCulture/UICulture` (los separadores numéricos los verifican las E2E) |
| Blazor | 17-18 | `AddRazorComponents().AddInteractiveServerComponents()` |
| Capas | 22-25 | `ConnectionStrings:BaseDeDatos` o `DefaultConnectionString` → `AddInfrastructure` → `AddApplication` |
| Presentación | 30-35 | `IVersionIdentity` singleton (`VersionIdentity.FromAssembly(Assembly.GetEntryAssembly())`); `IDialogService`, `IFocusService` **scoped** (estado del circuito) |
| Base | 39 | `DatabaseInitializer.Initialize(app.Services)` antes de atender |
| Pipeline | 41-52 | `UseExceptionHandler("/Error")` fuera de Development → `UseStatusCodePagesWithReExecute("/no-encontrado")` → `UseMiddleware<SessionMiddleware>()` → `UseAntiforgery()` → `MapStaticAssets()` → `MapRazorComponents<App>().AddInteractiveServerRenderMode()` |

Sin `UseHttpsRedirection` ni `UseHsts` (a diferencia de Hola Mundo y Login). El render mode se declara una vez en la raíz (`<Routes @rendermode="InteractiveServer" …/>`, `Components/App.razor` línea 23), desviación declarada en `README.md` §Desviaciones declaradas (1) por el puente de sesión (ver [03](03_Sesiones-Y-Persistencia.md) §2).

### 5.2 `src/MovilidadUrbana.ApiWeb/Program.cs` (50 líneas)

| Paso | Líneas | Qué |
| --- | --- | --- |
| Cultura | 11-13 | `es-AR` |
| Capas | 16-19 | igual que la web; `appsettings.json` trae `BaseDeDatos = datos/movilidad-api.db` |
| REST | 22-24 | `AddControllers()`, `AddProblemDetails()`, `AddOpenApi()` |
| Base | 28 | `DatabaseInitializer.Initialize` |
| Pipeline | 30-45 | `UseExceptionHandler()` → `UseStatusCodePages()` → en Development `MapOpenApi()` + `MapScalarApiReference(...)` → `UseMiddleware<SessionHeaderMiddleware>()` → `MapControllers()` |
| Pruebas | 50 | `public partial class Program;` para `WebApplicationFactory` |

Rutas, contratos y Scalar: ver [12](12_Api-REST.md).

### 5.3 `src/MovilidadUrbana.MAUI/MauiProgram.cs` (98 líneas)

| Paso | Líneas | Qué |
| --- | --- | --- |
| Cultura | 24-26 | `es-AR` en `Default*` **y** en `CurrentCulture` (el hilo principal ya existe) |
| Host | 28-35 | `UseMauiApp<App>()`, fuentes OpenSans |
| Ajustes Android | 37-38, 67-97 | `QuitarSubrayadoNativo()` y `AceptarComaDecimal()`: `AppendToMapping` de handlers bajo `#if ANDROID` |
| Capas | 40-42 | `AddInfrastructure($"Data Source={FileSystem.AppDataDirectory}/movilidad.db;Default Timeout=30")` → `AddApplication()` (no usa `DefaultConnectionString`) |
| Plataforma | 44-46 | `DeviceSession`, `INavigationService → ShellNavigationService`, `IAlertService → AlertService`: singletons |
| ViewModels | 49-51 | se crean con `DeviceSession.Create<T>()` (ámbito del dispositivo); `LocalidadesViewModel` y `LocalidadEditorViewModel` transient, `EncuestaViewModel` **singleton** |
| Páginas | 53-55 | `LocalidadesPage`, `LocalidadEditorPage`, `EncuestaPage` transient |
| Base | 61-62 | `DatabaseInitializer.Initialize(app.Services)` tras `Build()` |

Encadenamiento de arranque:

```
MauiProgram.CreateMauiApp ─► App(IServiceProvider)          src/MovilidadUrbana.MAUI/App.xaml.cs
                              · hereda de Microsoft.Maui.Controls.Application (nombre completo:
                                el espacio MovilidadUrbana.MAUI.Application lo tapa)
                              · UserAppTheme = Light; WindowSoftInputModeAdjust.Resize
                           ─► CreateWindow → new AppShell(services)
AppShell                     src/MovilidadUrbana.MAUI/AppShell.xaml(.cs)
   · TabBar: «Localidades» (Route localidades) y «Encuesta» (Route encuesta)
   · ContentTemplate resuelve LocalidadesPage / EncuestaPage del contenedor
   · Routing.RegisterRoute("localidad", typeof(LocalidadEditorPage))
```

La plataforma entra a los ViewModels solo por `INavigationService` e `IAlertService` (`Presentation/Abstractions/`); por eso `MovilidadUrbana.MAUI.Tests` usa dobles (`FakeNavigationService`, `FakeAlertService` en `tests/MovilidadUrbana.MAUI.Tests/TestEnvironment.cs`). Detalle de la app: [13](13_App-Android.md).

### 5.4 Hola Mundo y Login (sin capas)

| | `src/WebBlazor.HolaMundo/Program.cs` | `src/WebBlazor.Login/Program.cs` |
| --- | --- | --- |
| Servicios | Razor interactive server; `IVersionIdentity → VersionIdentity` singleton | lo mismo + `IIdentityService → IdentityService` scoped |
| Autenticación | — | cookie `auth_token`, `LoginPath = IdentityEndpoints.SuperficieDeAcceso` (`/login`), `AccessDeniedPath = /Error`, `ReturnUrlParameter = returnurl`, `HttpOnly`, `SameSite=Strict`; `AddAuthorization`, `AddCascadingAuthenticationState` |
| Pipeline | `UseExceptionHandler` + `UseHsts` fuera de Dev → `UseStatusCodePagesWithReExecute("/not-found")` → `UseHttpsRedirection` → `UseAntiforgery` → estáticos → Razor | mismo arranque, pero en otro orden: `UseHttpsRedirection` → estáticos → `UseAuthentication`/`UseAuthorization` → `UseAntiforgery` → Razor; después `app.MapearIdentidad()` publica `POST /identidad/ingreso` y `POST /identidad/salida` (`Endpoints/IdentityEndpoints.cs`) |
| Comentario rector | «Punto de composición: todo servicio se registra acá y en ningún otro archivo» (`#region services`) | ídem |

El render mode se declara por página (`@rendermode InteractiveServer` en `HolaMundo.razor`, `Home.razor`), no en la raíz. Flujo de acceso y guard: ver [10](10_Hola-Mundo-Y-Login.md).

---

## 6. Presentación de cada app, en una tabla

| App | Pieza | Archivo(s) | Vida / rol |
| --- | --- | --- | --- |
| Web | Páginas de dominio | `Components/Pages/Localidades.razor(.cs)`, `Encuesta.razor(.cs)` | consumen `LocalidadService` / `EncuestaService` |
| Web | Servicios de interfaz | `Services/DialogService.cs`, `FocusService.cs`, `VersionIdentity.cs` | dialog/focus scoped por circuito; versión singleton |
| Web | Sesión HTTP | `Sessions/SessionMiddleware.cs` | middleware |
| Web | Componentes técnicos | `Components/Shared/*` | ver [11](11_Template-Y-Superficies.md) |
| ApiWeb | Controllers | `Controllers/LocalidadesController.cs`, `EncuestasController.cs`, `ValidationProblems.cs` | ver [12](12_Api-REST.md) |
| ApiWeb | DTO | `Contracts/Localidades.cs`, `Contracts/Encuestas.cs` | |
| ApiWeb | Sesión HTTP | `Sessions/SessionHeaderMiddleware.cs` | middleware |
| MAUI | ViewModels | `Presentation/Localidades/*`, `Presentation/Encuestas/*`, `Presentation/ListState.cs` | CommunityToolkit.Mvvm |
| MAUI | Vistas | `Pages/*.xaml(.cs)` | `BindingContext` = VM inyectado |
| MAUI | Plataforma | `Services/DeviceSession.cs`, `ShellNavigationService.cs`, `AlertService.cs`, `OnScreenKeyboard.cs` | singletons (salvo `OnScreenKeyboard`, estático) |

---

## 7. Proyectos de prueba frente a las capas

| Proyecto de prueba | Cómo llega al código | Fuente |
| --- | --- | --- |
| `MovilidadUrbana.UnitTests` | `ProjectReference` a **`MovilidadUrbana.Web`** (prueba `Domain/Rules` de la web) | su `.csproj` |
| `MovilidadUrbana.ApiWeb.Tests` | `ProjectReference` a `MovilidadUrbana.ApiWeb`; `WebApplicationFactory<Program>` | su `.csproj`, `ApiWebApplicationFactory.cs` |
| `MovilidadUrbana.MAUI.Tests` | `Compile Include` enlazado de las 4 carpetas de la app Android | su `.csproj` |
| `MovilidadUrbana.E2ETests` | **sin referencia**: publica y lanza el binario de la web desde el fixture (o, con `URL_BASE`, prueba contra un entorno ya desplegado) | su `.csproj`, `Infrastructure/TestAppServer.cs` |
| `MovilidadUrbana.MAUI.UITests` | sin referencia: Appium contra la app instalada | su `.csproj` |
| `WebBlazor.*.E2ETests` | sin referencia: URL fija | sus `.csproj` |

Las reglas de ApiWeb y de MAUI no tienen pruebas unitarias propias: las 49 de `UnitTests` ejercitan la copia de la web; que las otras dos copias sean iguales se apoya solo en §2.1. Suites y conteos: [05](05_Pruebas.md).

Solución: `Lab-E2E.WebBlazor.sln` tiene 12 proyectos `.csproj` (conteo de entradas `Project(...)` con `.csproj`). `Lab-E2E.WebBlazor.SinMaui.slnf` lista 11: todos menos `src/MovilidadUrbana.MAUI` (CI no tiene el workload; ver [06](06_CI-Y-Workflows.md)).

---

## 8. Convención inglés/español aplicada al código

### 8.1 La regla

«Lo que viene del estándar va en inglés; lo que viene del problema va en español» (guía de nomenclatura §1; `README.md` §Convención de nombres; aplicada en `946d023` y `e9dea2a`, 2026-09-18).

| Inglés (arquitectura) | Español (dominio) | No se tocó |
| --- | --- | --- |
| Carpetas/espacios: `Domain`, `Application`, `Infrastructure`, `Presentation`, `Services`, `Pages`, `Controls`, `Converters`, `Components/Shared`, `Contracts`, `Sessions`, `Persistence`, `Entities`, `Rules`, `Abstractions` | Agrupación por dominio dentro de una capa: `Application/Localidades/`, `Application/Encuestas/`, `Presentation/Encuestas/` | Nombres de proyecto y solución |
| Sufijo de rol: `…Controller`, `…Service`, `…Repository`, `…Policy`, `…Rules`, `…Model`, `…ViewModel`, `…Request`, `…Dto`, `…Page`, `…Tests`, `…TestBase` | Raíz: `Localidad`, `Encuesta`, `RespuestaDeEncuesta`, `Catalogos` | Texto visible, URL (`/localidades`, `/encuesta/{Paso}`), contrato JSON |
| Operaciones de patrón: `GetAllAsync`, `GetByIdAsync`, `AddAsync`, `UpdateAsync`, `DeleteAsync`, `CountAsync`, `SaveAsync`, `Set`, `IsValid` | Acciones propias: `RegistrarAsync`, `ValidarPaso`, `AlternarMedio` | `data-testid`, `AutomationId` |
| Piezas técnicas: `Result`, `AppDbContext`, `SessionContext`, `SessionMiddleware`, `SessionHeaderMiddleware`, `DatabaseInitializer`, `SessionSeeder`, `DependencyInjection`, `DeviceSession`, `ShellNavigationService` | Reglas: `LocalidadRules.NombreValido`, `EncuestaRules.TotalDePasos`; atributos `CodigoPostal`, `Habitantes` | Comentarios y XML doc (salvo `cref`) |
| Tipos de estado: `SurfaceState`, `ListState`, `Tone` | **Valores** de estado: `ConDatos`, `Vacio`, `FiltradoSinResultados`, `Indisponible` | Clases CSS |
| Helpers de prueba: `E2ETestBase`, `TestAppServer`, `ApiWebApplicationFactory`, `AppiumSession` | Nombres de métodos de prueba | Tablas/columnas existentes (se borran las bases) |

Ejemplos de la regla en una sola palabra: `EncuestasController`, `LocalidadService`, `ILocalidadRepository`, `LocalidadRules`, `EncuestaViewModel`.

Los literales de sesión quedaron en español: cookie `sesion-movilidad` (`SessionContext.CookieName`), encabezado `X-Sesion-Id` (`SessionHeaderMiddleware.HeaderName`) y clave de `Preferences` `sesion-dispositivo` (`DeviceSession.Clave`). Que se conserven por ser contrato observable (las pruebas los repiten, [03](03_Sesiones-Y-Persistencia.md) §2.3) es lectura de este índice: el README no los menciona en §Convención de nombres.

### 8.2 Glosario del renombre (nombres viejos → nuevos)

Reconstruido de `git show 946d023^` (árbol previo) y del árbol actual. Los pares de archivos que `git` detecta como renombres cruzan de app porque las tres copias son idénticas; la tabla empareja por nombre, no por ruta.

| Antes (≤ `3e119b8`) | Ahora | Antes | Ahora |
| --- | --- | --- | --- |
| `Dominio/` · `Entidades/` · `Reglas/` | `Domain/` · `Entities/` · `Rules/` | `Aplicacion/` · `Abstracciones/` | `Application/` · `Abstractions/` |
| `Infraestructura/` · `Persistencia/` · `Sesiones/` | `Infrastructure/` · `Persistence/` · `Sessions/` | `Presentacion/` · `Servicios/` · `Paginas/` · `Controles/` · `Convertidores/` · `Contratos/` | `Presentation/` · `Services/` · `Pages/` · `Controls/` · `Converters/` · `Contracts/` |
| `Sesion` (entidad), `SesionId` | `Session`, `SessionId` | `ReglasDeLocalidad`, `ReglasDeEncuesta` | `LocalidadRules`, `EncuestaRules` |
| `ContextoDeDatos` | `AppDbContext` | `PreparadorDeBaseDeDatos` | `DatabaseInitializer` |
| `SembradorDeSesion` | `SessionSeeder` | `ContextoDeSesion`, `IContextoDeSesion` | `SessionContext`, `ISessionContext` |
| `RepositorioDeLocalidades`, `IRepositorioDeLocalidades` | `LocalidadRepository`, `ILocalidadRepository` | `ListarAsync`, `ObtenerAsync`, `AgregarAsync`, `ActualizarAsync`, `EliminarAsync` | `GetAllAsync`, `GetByIdAsync`, `AddAsync`, `UpdateAsync`, `DeleteAsync` |
| `ServicioDeLocalidades`, `ServicioDeEncuestas` | `LocalidadService`, `EncuestaService` | `ModeloDeLocalidad`, `PoliticaDeLocalidades` | `LocalidadModel`, `LocalidadPolicy` |
| `Resultado` | `Result` | `ServiciosDeAplicacion` / `AgregarAplicacion()` | `DependencyInjection` / `AddApplication()` |
| `ServiciosDeInfraestructura` / `AgregarInfraestructura(cadena)` | `DependencyInjection` / `AddInfrastructure(...)` | `MiddlewareDeSesion` | `SessionMiddleware` |
| `MiddlewareDeSesionPorEncabezado` | `SessionHeaderMiddleware` | `SesionDelDispositivo` | `DeviceSession` |
| `INavegador`, `IAvisos`, `AvisosDelSistema` | `INavigationService`, `IAlertService`, `AlertService` | `TecladoEnPantalla`, `EstadoDeLista` | `OnScreenKeyboard`, `ListState` |
| `ProblemasDeValidacion` | `ValidationProblems` | `Components/Componentes/` (`Grilla`, `ColumnaDeGrilla`, `Asistente`, `Insignia`, `Banda`, `Esqueleto`, `Icono`, `EstadoDeSuperficie`…) | `Components/Shared/` (`Grid`, `GridColumn`, `Wizard`, `Badge`, `Band`, `Skeleton`, `Icon`, `SurfaceState`…) |
| `PruebaE2E`, `ServidorDeLaAplicacion`, `ParalelismoDelEnsamblado` | `E2ETestBase`, `TestAppServer`, `AssemblyParallelism` | `SesionDeAppium`, `PruebaDePantalla`, `PruebaDeSuperficie`, `FabricaDeApi` | `AppiumSession`, `ScreenTestBase`, `SurfaceTestBase`, `ApiWebApplicationFactory` |
| `Theme/Iconos.cs`, `Theme/RolesDeIcono.cs` (las tres webs) | `Theme/Icons.cs`, `Theme/IconRoles.cs` | `Theme/Tono.cs` (Hola Mundo, Login) | `Theme/Tone.cs` (el `Tonos.cs` de la web **no** se renombró, §8.3) |

`946d023` toca 284 archivos (139 renombres detectados por `git show -M --name-status`). `e9dea2a` corrige 21 archivos: los `<see cref>` que la herramienta de renombre había protegido y que hicieron fallar la CI con `CS1574` (mensaje del commit; `CHANGELOG.md` 2026-09-18).

Consecuencias que el renombre obligó a resolver (`CHANGELOG.md` 2026-09-18; guía §4.4):

| Síntoma | Resolución en el código |
| --- | --- |
| `CS0104` ambiguo `DependencyInjection` | nombre calificado en `Program.cs` (§4) |
| `Application` no es una clase en MAUI | `App : Microsoft.Maui.Controls.Application` (`src/MovilidadUrbana.MAUI/App.xaml.cs` línea 5) |
| Tabla `Sesiones` → `Sessions`, columna `SesionId` → `SessionId` | borrar bases viejas: `EnsureCreated` no migra ([03](03_Sesiones-Y-Persistencia.md) §7) |
| Nombres generados por `[ObservableProperty]`/`[RelayCommand]` y bindings anidados | renombrados junto con su origen |

### 8.3 Rastros: nombres viejos que siguen en el árbol

La regla deja los comentarios sin traducir (guía §3), así que la mayoría de estos rastros son **esperables**, pero nombran piezas que ya no existen con ese nombre. Inventario por `git grep` sobre `8fb4c3a` (excluidos `CHANGELOG.md` y `evidencia/`, que son históricos por definición):

| Rastro | Dónde | Hoy se llama |
| --- | --- | --- |
| `MiddlewareDeSesionPorEncabezado` | `src/MovilidadUrbana.ApiWeb/Infrastructure/Sessions/SessionContext.cs` línea 8 | `SessionHeaderMiddleware` |
| `SesionDelDispositivo` | `src/MovilidadUrbana.MAUI/Infrastructure/Sessions/SessionContext.cs` línea 8 | `DeviceSession` |
| `ObtenerAsync` | `Infrastructure/Persistence/LocalidadRepository.cs` línea 52 (×3 apps) | `GetByIdAsync` |
| `SesionId` | `Domain/Entities/Localidad.cs` línea 4 (×3 apps) | `SessionId` |
| `ParalelismoDelEnsamblado.cs` | comentario de `pruebas.runsettings` línea 22 | `AssemblyParallelism.cs` |
| tabla `Sesiones` | `Infrastructure/Persistence/SessionSeeder.cs` línea 9 (×3 apps) | tabla `Sessions` |
| «Dominio, Aplicacion, Infraestructura[, Presentacion]» | cabeceras de `MovilidadUrbana.Web.csproj`, `MovilidadUrbana.ApiWeb.csproj`, `MovilidadUrbana.MAUI.csproj` | `Domain`, `Application`, `Infrastructure`, `Presentation` |
| «Aplicacion e Infraestructura» | `src/MovilidadUrbana.MAUI/MauiProgram.cs` línea 15; `Services/DeviceSession.cs` línea 11 | ídem |
| `Paginas/, Servicios/, Controles/` | comentario de `tests/MovilidadUrbana.MAUI.Tests/MovilidadUrbana.MAUI.Tests.csproj` | `Pages/`, `Services/`, `Controls/` |
| `PruebaDeSuperficie.UrlBase` | `scripts/pruebas.sh` línea 50; `.github/workflows/e2e-login.yml` línea 11 | `SurfaceTestBase.UrlBase` |
| `Domain/Reglas` | `README.md` línea 224 | `Domain/Rules` |
| `MovilidadUrbana.E2ETests.Infraestructura` | `README.md` línea 455 (ejemplo de la trampa del `[SetUpFixture]`) | `…E2ETests.Infrastructure` |
| Texto de enlace `Inicio`, `Grilla`, `Campo`, `Asistente`, `Insignia`, `Esqueleto`, `Banda`, `Dialogo`, `Icono`, `Iconos` | `README.md` líneas 184-191 (los destinos sí apuntan a `Home.razor`, `Grid.razor`, `FormField.razor`, `Wizard.razor`, …) | `Home`, `Grid`, `FormField`, `Wizard`, `Badge`, `Skeleton`, `Band`, `Dialog`, `Icon`, `Icons` |
| `Icono.razor` | comentario XML de `src/MovilidadUrbana.Web/Theme/Icons.cs` línea 5 | `Icon.razor` |
| `Icono` / `Iconos` | `src/WebBlazor.HolaMundo/Theme/Icons.cs` y `src/WebBlazor.Login/Theme/Icons.cs` línea 5; `Components/Shared/Icon.razor` línea 1 de ambas | `Icon` / `Icons` |
| «ColumnaDeGrilla solo se puede usar dentro del bloque <Columnas> de una Grilla.» | **cadena de una excepción**, `src/MovilidadUrbana.Web/Components/Shared/GridColumn.cs` línea 38 | `GridColumn`, parámetro `Columns` de `Grid` |

Comentarios **copiados de otra app** (efecto de §2.1, no del renombre):

| Comentario | Dónde | Por qué no aplica |
| --- | --- | --- |
| «Lo invoca cada punto de composición: la web y la API» | `Application/DependencyInjection.cs` línea 7, en las 3 apps | en MAUI lo invoca `MauiProgram`; en la web, solo la web |
| «La cadena de conexión la decide quien compone —web o API—» | `Infrastructure/DependencyInjection.cs` líneas 10-11, en las 3 apps | MAUI también compone |
| «Factory y no contexto de ámbito: un circuito de Blazor vive más que una petición» | ídem línea 19, en ApiWeb y MAUI | no hay circuito en la API ni en Android |
| «La implementación vive en Infraestructura porque depende de cookies y de HTTP» | `Application/Abstractions/ISessionContext.cs` líneas 4-5, en las 3 apps | `SessionContext` ya no depende de HTTP en ninguna (el middleware se fue a `Sessions/`); MAUI no tiene cookies |
| WAL «con las pruebas E2E en paralelo, varias sesiones tocan el mismo archivo» | `Infrastructure/Persistence/DatabaseInitializer.cs` líneas 27-28, en las 3 apps | en ApiWeb las pruebas usan una base por clase; en el teléfono no hay E2E en paralelo |

Los rastros propios de cada zona están en su índice y no se repiten acá: los de la vista web en [11](11_Template-Y-Superficies.md) §10, los de Hola Mundo y Login en [10](10_Hola-Mundo-Y-Login.md) §7, los de las pruebas en [05](05_Pruebas.md) §13, el mapa de nombres de la API en [12](12_Api-REST.md) §13 y el de Android en [13](13_App-Android.md) §12.

Mezclas que la regla no resolvió (observadas, sin que el repositorio las declare):

| Identificador | Dónde | Observación |
| --- | --- | --- |
| `Grid.Agregar(...)`, parámetro `Clave` | `src/MovilidadUrbana.Web/Components/Shared/Grid.razor.cs` líneas 38 y 69 (llamado desde `GridColumn.cs` línea 41) | operación técnica en español dentro de un componente técnico en inglés |
| `Tonos.cs` (web) frente a `Tone.cs` (Hola Mundo y Login) | `src/MovilidadUrbana.Web/Components/Shared/Tonos.cs`; `src/WebBlazor.*/Theme/Tone.cs` | la misma pieza técnica con nombre en idioma distinto; la guía pone `Tone` como inglés |

---

## 9. Historia de la arquitectura

| Fecha | Commit | Estado |
| --- | --- | --- |
| 2026-08-23 | `0516139` | la web nace con capas como **carpetas en español** dentro de `MovilidadUrbana.Web` (`Dominio/`, `Aplicacion/`, `Infraestructura/`); `MiddlewareDeSesion` dentro de `Infraestructura/Sesiones/` |
| 2026-09-12 | `88e5caa` | las capas pasan a **tres proyectos** `MovilidadUrbana.Dominio`, `.Aplicacion`, `.Infraestructura`; nace `MovilidadUrbana.ApiWeb` sobre ellos; aparecen `AgregarAplicacion()` / `AgregarInfraestructura(cadena)` |
| 2026-09-12 | `10ce735` | se eliminan los proyectos de capa: **cada app lleva sus carpetas** (código repetido a propósito); nace `MovilidadUrbana.MAUI`; `UnitTests` pasa a referenciar la web; el middleware sale de `Infraestructura/` |
| 2026-09-13 | `3e119b8` | `MovilidadUrbana.MAUI.UITests`: la solución llega a 12 proyectos |
| 2026-09-18 | `946d023`, `e9dea2a` | convención inglés/español (§8) |
| 2026-09-18 | `8fb4c3a` | README y CHANGELOG enlazan la guía de nomenclatura |

Lo que sobrevivió del paso por proyectos separados: «la separación en capas con registro propio … y los `Program.cs` que solo componen» (`CHANGELOG.md` 2026-09-12).

---

## 10. Desfasajes y huecos

| Tema | Estado | Fuente |
| --- | --- | --- |
| `CHANGELOG.md` 2026-09-12 dice «La solución queda en once proyectos» | cierto en `10ce735`; con `3e119b8` son 12, como dice el `README.md` | `CHANGELOG.md`, `Lab-E2E.WebBlazor.sln` |
| Enlace a la guía de nomenclatura | el README apunta a `github.com/hdcm-dev/Lab-E2E.WebBlazor.Documentacion/.../Guides/Nomenclatura-…`; la guía vive hoy en `/LAB/Lab-Documentos/Lab-Documentos/Guides/Testing/Lab-E2E.WebBlazor-Guides/` | `README.md` líneas 102-104; ver [07](07_Guias.md) |
| Evidencia del renombre de `946d023` | no hay carpeta de evidencia propia; `evidencia/2026-09-12-renombre/` es del renombre anterior (quitar el prefijo `E2E.Base`) | `ls evidencia/`, `CHANGELOG.md` 2026-09-12 |
| `cref` de `SessionContext` (web) | `<see cref="SessionMiddleware"/>` en `MovilidadUrbana.Web.Infrastructure.Sessions` no importa `MovilidadUrbana.Web.Sessions` | `src/MovilidadUrbana.Web/Infrastructure/Sessions/SessionContext.cs` línea 8. **No verificado** que resuelva; la web no activa `GenerateDocumentationFile` |
