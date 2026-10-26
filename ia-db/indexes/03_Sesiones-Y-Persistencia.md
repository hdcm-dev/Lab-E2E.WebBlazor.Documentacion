# 03 — Sesiones y persistencia

> **Propósito**: cómo cada aplicación de Movilidad Urbana reparte un **espacio de datos por sesión** (cookie en la web, encabezado `X-Sesion-Id` en la API, el dispositivo en Android), qué archivo SQLite usa cada una y cada suite, y cómo funcionan `AppDbContext`, `DatabaseInitializer` (con `EnsureCreated` y WAL), la siembra por sesión y los repositorios.
>
> **Fuente primaria**: `src/MovilidadUrbana.Web/Sessions/SessionMiddleware.cs`, `src/MovilidadUrbana.Web/Components/App.razor`, `src/MovilidadUrbana.Web/Components/Routes.razor`, `src/MovilidadUrbana.ApiWeb/Sessions/SessionHeaderMiddleware.cs`, `src/MovilidadUrbana.MAUI/Services/DeviceSession.cs`, `src/*/Infrastructure/Sessions/SessionContext.cs`, `src/*/Infrastructure/Persistence/*.cs`, `src/*/Infrastructure/DependencyInjection.cs`, `src/*/Domain/Entities/*.cs`, `src/*/Application/Abstractions/*.cs`, `src/*/appsettings.json`, `src/MovilidadUrbana.MAUI/MauiProgram.cs`, `tests/MovilidadUrbana.E2ETests/Infrastructure/{E2ETestBase,TestAppServer}.cs`, `tests/MovilidadUrbana.ApiWeb.Tests/ApiWebApplicationFactory.cs`, `tests/MovilidadUrbana.MAUI.Tests/TestEnvironment.cs`, `tests/MovilidadUrbana.MAUI.UITests/Infrastructure/AppiumSession.cs`, `.gitignore`, `README.md` (§«El estado es del servidor», §La API, §La aplicación Android), `CHANGELOG.md` 2026-09-18; historia: `0516139`, `88e5caa`, `10ce735`, `946d023`.
>
> **Vigencia**: versión 3.1, generada el 2026-10-25 sobre el commit `8fb4c3a` (2026-09-18).
>
> **Vecinos**: dónde vive cada pieza y cómo se compone en [01](01_Arquitectura.md) · entidades y reglas en [02](02_Dominio-Y-Reglas.md) · cómo las suites aprovechan el aislamiento en [05](05_Pruebas.md) · el `X-Sesion-Id` como contrato REST en [12](12_Api-REST.md) · la app Android en [13](13_App-Android.md) · la cookie de **autenticación** de Login (`auth_token`), que no es esta, en [10](10_Hola-Mundo-Y-Login.md) · por qué y trampas en [08](08_Decisiones-Y-Trampas.md).

---

## 1. El modelo: un espacio de datos por sesión

Toda fila de `Localidades` y `Encuestas` lleva un `SessionId`, y todo repositorio filtra por el `ISessionContext.Id` del ámbito actual. Así varias pruebas en paralelo comparten **un servidor y un archivo SQLite** sin verse entre sí (`README.md` §«2. El estado es del servidor, así que hay que aislarlo»).

| App | Portador del identificador | Quién lo fija en `SessionContext` | Si no viene | Vida |
| --- | --- | --- | --- | --- |
| Web | cookie `sesion-movilidad` | `SessionMiddleware` (petición) y `Routes.OnParametersSet` (circuito) | se emite cookie con un GUID nuevo, **solo** al pedir un documento | `MaxAge` 1 día |
| ApiWeb | encabezado `X-Sesion-Id` | `SessionHeaderMiddleware` | la petición usa un GUID nuevo y lo devuelve en el mismo encabezado | lo que el cliente lo repita |
| MAUI | `Preferences` clave `sesion-dispositivo` | `DeviceSession` (una vez, al crearse) | se genera y se guarda la primera vez | sobrevive a cerrar la app |
| Hola Mundo, Login | — (no tienen base ni sesión de datos) | — | — | — |

No es seguridad: cualquier cadena no vacía de hasta 64 caracteres se acepta como identificador (`SessionContext.IsValid`), sin firma ni verificación. Quien conoce un id ve esos datos. El laboratorio lo declara como mecanismo de aislamiento, no de identidad: «Este laboratorio no tiene credenciales: la sesión la reparte un middleware por cookie para aislar los datos entre pruebas» (`README.md` §Lo que no aplica, declarado).

---

## 2. Web: cookie y puente al circuito

```
GET /localidades (documento)
   │
   ▼  SessionMiddleware                         src/MovilidadUrbana.Web/Sessions/SessionMiddleware.cs
   │   id = Request.Cookies[SessionContext.CookieName]        (línea 19)
   │   si id inválido Y es documento → id = session.Id (GUID provisorio del ámbito)
   │                                  → Set-Cookie sesion-movilidad=<id>   (líneas 24-38)
   │   session.Set(id ?? "")                                   (línea 40)
   ▼
App.razor  (render estático, dentro de la petición HTTP)   src/MovilidadUrbana.Web/Components/App.razor
   │   @inject SessionContext Session                          (línea 1)
   │   <Routes @rendermode="InteractiveServer" SessionId="@Session.Id" />   (línea 23)
   ▼  el parámetro viaja serializado al circuito
Routes.razor  (componente interactivo raíz, ámbito del CIRCUITO)  src/MovilidadUrbana.Web/Components/Routes.razor
       [Parameter] string? SessionId                           (líneas 16-17)
       OnParametersSet → Contexto.Set(SessionId)              (líneas 23-26)
       ⇒ los servicios scoped del circuito (repositorios, siembra) ya ven la sesión correcta
```

Por qué así: «un circuito de Blazor Server no tiene acceso a la petición HTTP original, así que este parámetro es el puente entre el render estático y el interactivo. Debe ser serializable: por eso es un `string`» (comentario en `Routes.razor` líneas 11-15). Es también la causa de la desviación «el render mode se declara en la raíz y no por página» (`README.md` §Desviaciones declaradas, 1).

### 2.1 La cookie

| Atributo | Valor | Fuente |
| --- | --- | --- |
| Nombre | `sesion-movilidad` (`SessionContext.CookieName`) | `src/MovilidadUrbana.Web/Infrastructure/Sessions/SessionContext.cs` línea 15 |
| Valor | GUID `"n"` (32 hex) generado por el constructor de `SessionContext` | ídem línea 19 |
| `HttpOnly` / `IsEssential` | `true` / `true` | `SessionMiddleware.cs` líneas 32-33 |
| `SameSite` | `Lax` | línea 34 |
| `Path` / `MaxAge` | `/` / 1 día | líneas 35-36 |
| `Secure` | no se fija | (ausente en el código) |

### 2.2 «Documento» y por qué importa

`EsUnDocumento` = `GET` que no empieza con `/_framework` ni `/_blazor` y cuya ruta no tiene extensión (`SessionMiddleware.cs` líneas 49-53). Si la cookie se emitiera también para css y js —pedidos en paralelo— la primera visita generaría varios identificadores y el navegador se quedaría con el último en llegar (comentario, líneas 21-23).

### 2.3 Nombre duplicado en las pruebas

La E2E no importa la constante: repite el literal `private const string CookieDeSesion = "sesion-movilidad";` (`tests/MovilidadUrbana.E2ETests/Infrastructure/E2ETestBase.cs` línea 17). Cambiar uno sin el otro deja de aislar las pruebas.

---

## 3. ApiWeb: encabezado `X-Sesion-Id`

`src/MovilidadUrbana.ApiWeb/Sessions/SessionHeaderMiddleware.cs`:

| Paso | Líneas | Qué |
| --- | --- | --- |
| Constante | 12 | `HeaderName = "X-Sesion-Id"` |
| Lectura | 16-17 | si el encabezado es válido → `session.Set(id)`; si no, queda el GUID provisorio |
| Respuesta | 19-23 | `Response.OnStarting` escribe `X-Sesion-Id: <session.Id>` en **toda** respuesta |

Se registra en `Program.cs` después de `MapOpenApi`/Scalar y antes de `MapControllers` (`src/MovilidadUrbana.ApiWeb/Program.cs` líneas 44-45). Evidencia de una corrida real sobre Kestrel con «sesión asignada: 854410443f…» y el flujo por `curl`: `evidencia/2026-09-12-capas-y-api/api-kestrel-openapi-y-curl.log` (de la época de `88e5caa`, con capas en proyectos separados; el log tiene además dos `python3: command not found`). Contrato REST: [12](12_Api-REST.md).

---

## 4. MAUI: el dispositivo es una sesión

`src/MovilidadUrbana.MAUI/Services/DeviceSession.cs` (singleton registrado en `MauiProgram.cs` línea 44):

```
DeviceSession(IServiceProvider)
  id = Preferences.Default.Get<string?>(Clave, null)   Clave = "sesion-dispositivo"   (líneas 16, 22)
  si !SessionContext.IsValid(id) → id = GUID nuevo; Preferences.Default.Set(Clave, id)   (líneas 23-27)
  _alcance = services.CreateScope()      ← UN ámbito que vive lo que la app   (línea 29)
  _alcance.ServiceProvider.GetRequiredService<SessionContext>().Set(id!)   (línea 30)
  Create<T>() = ActivatorUtilities.CreateInstance<T>(_alcance.ServiceProvider)   (línea 36)
```

Los ViewModels se crean con `DeviceSession.Create<T>()` (`MauiProgram.cs` líneas 49-51), así sus `LocalidadService`/`EncuestaService` y repositorios son los del ámbito único que ya tiene la sesión. `DeviceSession` vive en `Services/` y no en `Infrastructure/` porque usa `Preferences` (API de MAUI); por eso `MovilidadUrbana.MAUI.Tests` puede enlazar `Infrastructure/` sin el workload ([01](01_Arquitectura.md) §3.1).

---

## 5. `SessionContext` en las tres apps

Mismo contrato (`Application/Abstractions/ISessionContext.cs`: solo `string Id { get; }`) y misma implementación base:

| Miembro | Web | ApiWeb | MAUI |
| --- | --- | --- | --- |
| `Id` inicial | `Guid.NewGuid().ToString("n")` — «identificador provisorio» para que un ámbito sin sesión no escriba en un espacio compartido | ídem | ídem |
| `Set(string id)` | solo si `IsValid(id)` | ídem | ídem |
| `IsValid` | no vacío ni blanco y `Length ≤ 64` (`MaxLength`) | ídem | ídem |
| `CookieName` | `"sesion-movilidad"` | — | — |
| Comentario: quién lo fija | `SessionMiddleware` + `Routes` | `MiddlewareDeSesionPorEncabezado` (rastro, hoy `SessionHeaderMiddleware`) | `SesionDelDispositivo` (rastro, hoy `DeviceSession`) |

Registro: `SessionContext` scoped y `ISessionContext` resuelto a **la misma instancia** (`Infrastructure/DependencyInjection.cs` líneas 23-24). El largo 64 coincide con `HasMaxLength(64)` de `SessionId` en el modelo (§7).

---

## 6. Ámbitos: qué vive cuánto

| Host | Un ámbito DI es… | Consecuencia | Fuente |
| --- | --- | --- | --- |
| Web, render estático | una petición HTTP | `SessionMiddleware` y `App.razor` comparten `SessionContext` | `SessionMiddleware.cs`, `App.razor` |
| Web, interactivo | un **circuito** (minutos u horas) | por eso `AddDbContextFactory` y un `DbContext` por operación: «un `DbContext` con alcance de ámbito viviría lo que dura el circuito» | `Infrastructure/DependencyInjection.cs` línea 19; `LocalidadRepository.cs` líneas 11-13 |
| ApiWeb | una petición | la sesión se fija en cada pedido | `SessionHeaderMiddleware.cs` |
| MAUI | **uno solo** para toda la vida de la app | `SessionSeeder._alreadySeeded` se evalúa una vez por ejecución | `DeviceSession.cs` líneas 11-12, 29 |
| `MAUI.Tests` | un ámbito por `TestEnvironment` (= «un dispositivo nuevo») | | `tests/MovilidadUrbana.MAUI.Tests/TestEnvironment.cs` líneas 15, 35-36 |

`AddDbContextFactory` es el mismo en las tres apps (archivo idéntico), aunque el motivo escrito —el circuito— solo aplica a la web ([01](01_Arquitectura.md) §8.3).

---

## 7. Qué base usa cada app y cada suite

| Quién | Cadena de conexión | De dónde sale | Fuente |
| --- | --- | --- | --- |
| Web (`dotnet run` / publicado) | `Data Source=datos/movilidad.db;Default Timeout=30` | `DefaultConnectionString`: ni `appsettings.json` ni `appsettings.Development.json` de la web definen `ConnectionStrings` | `src/MovilidadUrbana.Web/Infrastructure/DependencyInjection.cs` línea 15; `src/MovilidadUrbana.Web/appsettings.json` |
| ApiWeb | `Data Source=datos/movilidad-api.db;Default Timeout=30` | `ConnectionStrings:BaseDeDatos` | `src/MovilidadUrbana.ApiWeb/appsettings.json` |
| MAUI | `Data Source=<FileSystem.AppDataDirectory>/movilidad.db;Default Timeout=30` | armada en `MauiProgram` (no usa `DefaultConnectionString`, que existe en la copia pero queda sin uso) | `src/MovilidadUrbana.MAUI/MauiProgram.cs` líneas 40-41 |
| `MovilidadUrbana.E2ETests` | `Data Source=<BASE_DE_DATOS>;Default Timeout=30`, y si la variable falta `<raíz del repo>/datos-e2e/movilidad.db` (`BASE_DE_DATOS` es la ruta completa del archivo) | variable de entorno `ConnectionStrings__BaseDeDatos` al lanzar el binario publicado (en `Production`) | `tests/MovilidadUrbana.E2ETests/Infrastructure/TestAppServer.cs` líneas 70-71, 185-187 |
| `MovilidadUrbana.ApiWeb.Tests` | `Data Source=<tmp>/movilidad-api-<guid>.db;Default Timeout=30` | `UseSetting("ConnectionStrings:BaseDeDatos", …)`; borra `.db`, `-wal`, `-shm` al terminar | `tests/MovilidadUrbana.ApiWeb.Tests/ApiWebApplicationFactory.cs` líneas 12-24 |
| `MovilidadUrbana.MAUI.Tests` | `Data Source=<tmp>/movilidad-maui-<guid>.db` (sin `Default Timeout`) | un archivo por `TestEnvironment`; `SqliteConnection.ClearAllPools()` y borra los tres archivos | `tests/MovilidadUrbana.MAUI.Tests/TestEnvironment.cs` líneas 19, 32, 50-51 |
| `MovilidadUrbana.MAUI.UITests` | la base real del teléfono | Appium con `NoReset=true`: «conserva los datos entre pruebas; cada prueba deja lo que encontró» | `tests/MovilidadUrbana.MAUI.UITests/Infrastructure/AppiumSession.cs` líneas 11, 27 |
| `MovilidadUrbana.UnitTests` | ninguna (reglas puras) | | ver [05](05_Pruebas.md) |

La clave de configuración es **`ConnectionStrings:BaseDeDatos`** (en español), leída por `GetConnectionString("BaseDeDatos")` en los dos `Program.cs` web (`src/MovilidadUrbana.Web/Program.cs` línea 22; `src/MovilidadUrbana.ApiWeb/Program.cs` línea 16).

Las rutas `datos/…` son relativas: `DatabaseInitializer` las resuelve con `Path.GetFullPath` (directorio actual del proceso) y crea la carpeta si falta. **No verificado** en qué carpeta exacta queda `datos/` con `dotnet run` (depende del directorio desde el que se lance).

Ignorado por git (`.gitignore`, sección «Laboratorio E2E»): `datos/`, `*.db`, `*.db-wal`, `*.db-shm`, `/datos-e2e/`.

---

## 8. `AppDbContext` (esquema)

`src/*/Infrastructure/Persistence/AppDbContext.cs` (idéntico en las tres apps; «el único lugar que conoce el motor de base de datos»):

| `DbSet` (= tabla) | Entidad | Clave | Restricciones | Índice |
| --- | --- | --- | --- | --- |
| `Sessions` | `Session { Id, CreatedAt }` | `Id` string, máx. 64 | — | PK |
| `Localidades` | `Localidad { Id, SessionId, Nombre, Provincia, CodigoPostal, Habitantes }` | `Id` int | `SessionId` 64 req · `Nombre` 60 req · `Provincia` 60 req · `CodigoPostal` 4 req | `SessionId` |
| `Encuestas` | `RespuestaDeEncuesta { Id, SessionId, Nombre, Edad, Localidad, Medios, Frecuencia, Distancia, Minutos, Motivo, RegistradaEn }` | `Id` int | `SessionId` 64 req · `Nombre` 80 req | `SessionId` |

- `Medios` (`IReadOnlyList<string>`) se guarda como **texto separado por comas** con `ValueConverter` + `ValueComparer` («SQLite no tiene tipo lista», líneas 41-52).
- `RespuestaDeEncuesta.Localidad` es un **string** (el nombre), no una clave foránea: no hay relaciones entre tablas. Por eso dar de baja una localidad «no arrastra dependientes» (`README.md` §Lo que no aplica, declarado).
- `Session` no se relaciona con las otras tablas: es solo la **marca de siembra** (`Domain/Entities/Session.cs`, comentario líneas 3-6).
- Detalle semántico de cada campo y sus reglas: [02](02_Dominio-Y-Reglas.md).

---

## 9. `DatabaseInitializer`

`src/*/Infrastructure/Persistence/DatabaseInitializer.cs`, invocado por cada host antes de atender (web `Program.cs` línea 39, API línea 28, `MauiProgram.cs` línea 62, `TestEnvironment` línea 35):

```
CreateScope → IDbContextFactory<AppDbContext>.CreateDbContext()
  origen  = SqliteConnectionStringBuilder(cadena).DataSource          (línea 21)
  carpeta = Path.GetDirectoryName(Path.GetFullPath(origen)) → CreateDirectory   (líneas 22-23)
  Database.EnsureCreated()                                             (línea 25)
  ExecuteSqlRaw("PRAGMA journal_mode=WAL;")                           (línea 29)
```

| Decisión | Motivo escrito | Consecuencia |
| --- | --- | --- |
| `EnsureCreated`, **no migraciones** | «el laboratorio no versiona el esquema, y así el binario publicado arranca en cualquier máquina sin pasos previos» (líneas 10-11) | si el esquema cambia, una base existente **no se actualiza**: hay que borrarla |
| WAL | «permite leer mientras otra conexión escribe. Con las pruebas E2E en paralelo, varias sesiones tocan el mismo archivo al mismo tiempo» (líneas 27-28) | aparecen los archivos `-wal` y `-shm`, que las pruebas borran y git ignora |
| `Default Timeout=30` en las cadenas | **no hay comentario** que lo explique en el código | **No verificado** el motivo; plausiblemente esperar al bloqueo de escritura de SQLite bajo concurrencia |

Trampa ya pagada: con `946d023` la entidad `Sesion` pasó a `Session` (tabla `Sesiones` → `Sessions`, columna `SesionId` → `SessionId`). «las bases SQLite de corridas anteriores hay que borrarlas (`EnsureCreated` no migra)» (`CHANGELOG.md` 2026-09-18; guía `/LAB/Lab-Documentos/Lab-Documentos/Guides/Testing/Lab-E2E.WebBlazor-Guides/Nomenclatura-Convensiones-Arquitecture-Dot-Net.md` §4.4: «borrar las bases SQLite de corridas anteriores (`datos-e2e/`)»). Aplica igual a `datos/` y a la base del teléfono; para esta última el repositorio no documenta cómo borrarla (**no verificado**: desinstalar o borrar datos de la app).

---

## 10. Siembra por sesión (`SessionSeeder`)

`src/*/Infrastructure/Persistence/SessionSeeder.cs` (scoped):

| Paso | Líneas | Qué |
| --- | --- | --- |
| Datos iniciales | 13-17 | `Corrientes` (Corrientes, `3400`, 346334 hab.) y `Resistencia` (Chaco, `3500`, 291720 hab.) |
| Atajo | 19, 23 | `_alreadySeeded` por instancia (= por ámbito): una sola consulta por petición/circuito/ejecución |
| ¿Ya sembrada? | 27 | `Sessions.AnyAsync(s => s.Id == session.Id)` |
| Siembra | 28-41 | inserta la marca `Session { Id, CreatedAt = UtcNow }` **y** las dos localidades en un mismo `SaveChangesAsync` |
| Carrera | 39-46 | `catch (DbUpdateException)`: «Otra petición de la misma sesión ganó la carrera insertando la marca: los datos ya están» |
| Fin | 49 | `_alreadySeeded = true` |

Las pruebas dependen de este juego: «Muestra el listado sembrado» espera 2 filas y el desplegable de la encuesta, 3 opciones (marcador + 2) (`tests/MovilidadUrbana.E2ETests/LocalidadesTests.cs`, `EncuestaTests.cs`); la API y los ViewModels también esperan Corrientes y Resistencia ([12](12_Api-REST.md) §8, [13](13_App-Android.md) §8). No hay siembra de encuestas: el contador arranca en 0.

Por qué la marca: sin ella, borrar todas las localidades «volvería a sembrarlas en la siguiente lectura» (`Domain/Entities/Session.cs`). Lo verifica la E2E `AlBorrarTodasLasLocalidadesAvisaQueNoHayDatos`: tras recargar, la tabla sigue con 0 filas (`tests/MovilidadUrbana.E2ETests/LocalidadesTests.cs` líneas 136-155).

Qué dispara la siembra (de `LocalidadRepository.cs`):

| Operación | ¿Siembra antes? |
| --- | --- |
| `GetAllAsync`, `GetByIdAsync`, `AddAsync` (localidades) | **sí** (`EnsureSeededAsync`, líneas 22, 33, 42) |
| `UpdateAsync`, `DeleteAsync` (localidades) | no |
| `EncuestaRepository.AddAsync`, `CountAsync` | **no**: una sesión que solo registra encuestas no tiene fila en `Sessions` hasta que lee localidades |

---

## 11. Repositorios

Interfaces en `Application/Abstractions/` (nombres de patrón en inglés); implementaciones en `Infrastructure/Persistence/`. Todas abren **un `DbContext` por operación** desde la factory (`await using var context = await factory.CreateDbContextAsync(...)`).

| Método | Filtro de sesión | Notas | Fuente |
| --- | --- | --- | --- |
| `ILocalidadRepository.GetAllAsync` | `Where(SessionId == session.Id)` | `AsNoTracking`, `OrderBy(Id)` | `LocalidadRepository.cs` 20-29 |
| `GetByIdAsync(id)` | `Id == id && SessionId == session.Id` | `AsNoTracking`; un id de otra sesión devuelve `null` | 31-38 |
| `AddAsync(localidad)` | **escribe** `localidad.SessionId = session.Id` | devuelve el `Id` generado | 40-48 |
| `UpdateAsync(localidad)` | si `localidad.SessionId != session.Id` → sale sin hacer nada | `context.Update` de la entidad desconectada | 50-59 |
| `DeleteAsync(id)` | `Id == id && SessionId == session.Id` | `ExecuteDeleteAsync` (sin cargar) | 61-67 |
| `IEncuestaRepository.AddAsync(respuesta)` | escribe `SessionId` | devuelve el `Id` | `EncuestaRepository.cs` 11-18 |
| `CountAsync()` | `CountAsync(SessionId == session.Id)` | | 20-24 |

Garantía declarada: «ninguna consulta sale del espacio de datos del visitante, ni siquiera si le llega el identificador de otra sesión» (`LocalidadRepository.cs` líneas 7-9). La comprobación de `UpdateAsync` «deja igual la garantía escrita en el código y no en la memoria de quien lo lea» (líneas 52-53; el comentario nombra `ObtenerAsync`, rastro de `GetByIdAsync`).

Quién los consume: `LocalidadService` y `EncuestaService` ([02](02_Dominio-Y-Reglas.md)); además `LocalidadesController` usa `ILocalidadRepository` directo para leer ([01](01_Arquitectura.md) §3.2).

---

## 12. Cómo lo aprovechan las pruebas (resumen; detalle en [05](05_Pruebas.md))

| Suite | Aislamiento | Fuente |
| --- | --- | --- |
| `MovilidadUrbana.E2ETests` | `[SetUp] StartFreshSessionAsync` agrega la cookie `sesion-movilidad` con un GUID nuevo antes de navegar → cada caso recibe su juego recién sembrado sobre **una** instancia y **una** base | `E2ETestBase.cs` líneas 62-79 |
| | caso `CadaPruebaTrabajaSobreSuPropioConjuntoDeDatos`: alta en una sesión, `ClearCookiesAsync`, otra página ve 2 filas y no «Mercedes» | `LocalidadesTests.cs` líneas 157-174 |
| `MovilidadUrbana.ApiWeb.Tests` | cada cliente agrega `X-Sesion-Id` con un GUID nuevo; casos `UnaSesionNuevaArrancaConLasSembradas`, `SinEncabezadoLaRespuestaDevuelveUno`, `CadaSesionTieneSusDatos` | `tests/MovilidadUrbana.ApiWeb.Tests/LocalidadesTests.cs` líneas 16-22, 24-41, 97-107 |
| `MovilidadUrbana.MAUI.Tests` | un archivo SQLite y un ámbito por caso | `TestEnvironment.cs` |
| `MovilidadUrbana.MAUI.UITests` | **sin** aislamiento: una sola sesión del dispositivo; las pruebas van en serie y, según el README, cada una deja los datos como los encontró (vale para localidades; la encuesta registrada no se deshace, [13](13_App-Android.md) §9) | `AppiumSession.cs` línea 11; `README.md` §La aplicación Android |

---

## 13. Historia

| Fecha | Commit | Cambio |
| --- | --- | --- |
| 2026-08-23 | `0516139` | nacen `MiddlewareDeSesion` (en `Infraestructura/Sesiones/`), `ContextoDeSesion`, `SembradorDeSesion`, `PreparadorDeBaseDeDatos` con `EnsureCreated` + WAL, `IDbContextFactory` |
| 2026-09-12 | `88e5caa` | la API suma `MiddlewareDeSesionPorEncabezado` (`X-Sesion-Id`) sobre los mismos repositorios y base (capas en proyectos propios) |
| 2026-09-12 | `10ce735` | cada app con su copia; el middleware web se muda a `MovilidadUrbana.Web/Sesiones/`; nace `SesionDelDispositivo` (MAUI) con `Preferences` |
| 2026-09-18 | `946d023` | renombre: `Sesion`→`Session`, `SesionId`→`SessionId`, tabla `Sesiones`→`Sessions`; las clases pasan a `SessionMiddleware`, `SessionHeaderMiddleware`, `SessionContext`, `SessionSeeder`, `DatabaseInitializer`, `AppDbContext`, `DeviceSession` |

---

## 14. Lo que no hay (verificado por ausencia en `src/`)

| Ausencia | Efecto |
| --- | --- |
| Limpieza de sesiones viejas | `Sessions`, `Localidades` y `Encuestas` crecen con cada sesión nueva (cada caso E2E estrena una sesión con un GUID nuevo); nada borra filas por antigüedad. La cookie vence al día, los datos no |
| Migraciones EF | ver §9 |
| Relaciones / claves foráneas | ver §8 |
| Firma o validación del identificador | ver §1 |
| Transacción explícita | se apoya en la atomicidad de cada `SaveChangesAsync` (la siembra inserta marca y localidades juntas) |
