# 03 — Sesiones y persistencia

> **Propósito**: cómo se aísla el estado por visitante —cookie en la web, encabezado en la API,
> el dispositivo entero en Android— y cómo se persiste en SQLite con EF Core: esquema, siembra, WAL
> y el ciclo de vida del `DbContext`.
> **Fuente primaria**: `src/MovilidadUrbana.Web/Infraestructura/` (`Sesiones/`, `Persistencia/`,
> `ServiciosDeInfraestructura.cs`; idéntico salvo el `namespace` en `ApiWeb/` y `MAUI/`),
> `src/MovilidadUrbana.Web/Sesiones/MiddlewareDeSesion.cs`,
> `src/MovilidadUrbana.ApiWeb/Sesiones/MiddlewareDeSesionPorEncabezado.cs`,
> `src/MovilidadUrbana.MAUI/Servicios/SesionDelDispositivo.cs`, `App.razor`, `Routes.razor`.
> **Vigencia**: 2026-09-12, commit `10ce735`.

## El problema

En `Lab-E2E.StaticHtml` cada prueba tenía su `localStorage`. Acá hay **una sola base SQLite** y
todas las pruebas —incluidas las paralelas— la comparten. La solución es que la aplicación reparta
un **espacio de datos por sesión** y que todo repositorio filtre por él (`README.md` §2).

## `ContextoDeSesion` (`Infraestructura/Sesiones/ContextoDeSesion.cs`)

| Miembro | Valor / comportamiento |
| --- | --- |
| `NombreDeCookie` | `sesion-movilidad` |
| `LargoMaximo` | 64 |
| `Id` | Arranca en `Guid.NewGuid().ToString("n")`: un ámbito sin cookie nunca lee un espacio compartido |
| `Establecer(id)` | Solo reemplaza si `EsValido(id)` |
| `EsValido(id)` | No vacío ni espacios y largo ≤ 64 |

Es *scoped* —una petición HTTP, un circuito o, en Android, el único ámbito de la aplicación— y la
**misma instancia** sirve a `ContextoDeSesion` y a `IContextoDeSesion`
(`ServiciosDeInfraestructura.cs`).

## Tres formas de identificar la sesión

| | Web (`MiddlewareDeSesion`) | API (`MiddlewareDeSesionPorEncabezado`) |
| --- | --- | --- |
| Portador | Cookie `sesion-movilidad` | Encabezado `X-Sesion-Id` |
| Si no llega | Emite una cookie **solo al pedir un documento** (GET, sin extensión, fuera de `/_framework` y `/_blazor`) | Toma el `Id` provisorio y lo devuelve en el **mismo encabezado** de la respuesta (`Response.OnStarting`) para que el cliente lo repita |
| Opciones | `HttpOnly`, `IsEssential`, `SameSite=Lax`, `Path=/`, `MaxAge=1 día` | — |
| Por qué así | Si se emitiera también en css/js —que el navegador pide en paralelo— la primera visita generaría varios identificadores y se quedaría con el último | Es la forma idiomática en una API; equivale a la cookie |
| Prueba que lo verifica | «Cada prueba trabaja sobre su propio conjunto de datos» (`LocalidadesTests`) | «Sin encabezado de sesión, la respuesta devuelve uno» y «Cada sesión trabaja sobre su propio conjunto de datos» (`LocalidadesTests` de la API) |

Cada prueba E2E escribe la cookie con un GUID propio antes de navegar (`PruebaE2E.EstrenarSesionAsync`);
cada prueba de la API agrega el encabezado con un GUID propio (`Cliente()`).

**En Android el dispositivo es una sola sesión** (`Servicios/SesionDelDispositivo.cs`): el
identificador se genera la primera vez, queda en `Preferences` bajo la clave `sesion-dispositivo`, y
un único `IServiceScope` —abierto en el constructor y vivo lo que vive la aplicación— recibe
`ContextoDeSesion.Establecer(id)`. Los ViewModels se crean desde ese ámbito con
`ActivatorUtilities`, así los repositorios ya ven la sesión puesta. Los datos sobreviven a cerrar la
aplicación. En las pruebas de ViewModels cada `Entorno` es «un dispositivo nuevo»: base propia y
sesión provisoria ([13](13_App-Android.md)).

## El puente al circuito de Blazor

Un circuito **no tiene acceso a la petición HTTP** que lo originó. La cookie se lee en
`App.razor` (`@inject ContextoDeSesion Sesion` → `<Routes SesionId="@Sesion.Id" />`) y `Routes`
la establece en el `ContextoDeSesion` del ámbito del circuito en `OnParametersSet`, antes de que se
renderice cualquier página. El parámetro es `string` porque debe ser serializable. Diagrama en
[01](01_Arquitectura.md).

## Persistencia

### `ContextoDeDatos` (`Persistencia/ContextoDeDatos.cs`)

Único lugar que conoce el motor. Tres `DbSet`: `Localidades`, `Encuestas`, `Sesiones`.

| Entidad | Configuración |
| --- | --- |
| `Sesion` | clave `Id` (`HasMaxLength(64)`) |
| `Localidad` | `SesionId` ≤ 64 requerido, `Nombre` ≤ 60, `Provincia` ≤ 60, `CodigoPostal` ≤ 4, todos requeridos; **índice en `SesionId`** porque toda consulta del ABM filtra por sesión |
| `RespuestaDeEncuesta` | `SesionId` ≤ 64, `Nombre` ≤ 80, índice en `SesionId`; `Medios` con `ValueConverter` lista ↔ texto separado por comas y `ValueComparer` por secuencia (SQLite no tiene tipo lista) |

### `PreparadorDeBaseDeDatos.Preparar(IServiceProvider)`

1. Crea la carpeta del `DataSource` si no existe.
2. `EnsureCreated()` — **no migraciones**, a propósito: el laboratorio no versiona el esquema y así
   el binario publicado arranca en cualquier máquina sin pasos previos.
3. `PRAGMA journal_mode=WAL` — permite leer mientras otra conexión escribe; con las E2E en paralelo
   varias sesiones tocan el mismo archivo a la vez.

Lo invocan los dos `Program.cs`, `MauiProgram.cs` y el `Entorno` de las pruebas de ViewModels justo
después de `Build()`. En el teléfono crea `movilidad.db` en `FileSystem.AppDataDirectory`.

### Cadenas de conexión

| Contexto | Cadena | Origen |
| --- | --- | --- |
| Por defecto (web en desarrollo) | `Data Source=datos/movilidad.db;Default Timeout=30` | `ServiciosDeInfraestructura.CadenaDeConexionPorDefecto` |
| API | `Data Source=datos/movilidad-api.db;Default Timeout=30` | `ApiWeb/appsettings.json` |
| Web bajo las E2E | `datos-e2e/movilidad.db` en la raíz del repositorio (o `BASE_DE_DATOS`) | `ServidorDeLaAplicacion.cs` vía `ConnectionStrings__BaseDeDatos` |
| API bajo sus pruebas | `%TEMP%/movilidad-api-{guid}.db`, borrado (con `-wal` y `-shm`) al terminar | `FabricaDeApi.cs` |
| Android | `{FileSystem.AppDataDirectory}/movilidad.db;Default Timeout=30` — almacenamiento privado de la app, sin permisos de red | `MauiProgram.cs` |
| ViewModels bajo sus pruebas | `%TEMP%/movilidad-maui-{guid}.db` (sin `Default Timeout`), borrado con `ClearAllPools()` previo | `tests/MovilidadUrbana.MAUI.Tests/Entorno.cs` |

`datos/`, `*.db`, `*.db-wal`, `*.db-shm` y `/datos-e2e/` están en `.gitignore`.

### Repositorios (`Persistencia/`)

Ambos usan `IDbContextFactory<ContextoDeDatos>` y **abren un contexto por operación**: en Blazor
Server un `DbContext` de ámbito viviría lo que dura el circuito —minutos u horas— y no está pensado
para eso (comentario en `RepositorioDeLocalidades.cs`).

| `RepositorioDeLocalidades` | Comportamiento |
| --- | --- |
| `ListarAsync` | `AsegurarAsync` del sembrador → `AsNoTracking`, filtra `SesionId`, ordena por `Id` |
| `ObtenerAsync(id)` | Siembra → busca por `Id` **y** `SesionId`: un id de otra sesión devuelve `null` |
| `AgregarAsync` | Siembra → fija `SesionId` y guarda |
| `ActualizarAsync` | Si `SesionId` no coincide, **no hace nada** (la garantía escrita en el código) |
| `EliminarAsync(id)` | `ExecuteDeleteAsync` filtrando por `Id` y `SesionId` |

`RepositorioDeEncuestas`: `AgregarAsync` fija `SesionId` y devuelve el `Id`; `ContarAsync` cuenta
por sesión. No pasa por el sembrador.

### `SembradorDeSesion.AsegurarAsync`

La primera vez que se toca una sesión inserta la marca `Sesion` y dos localidades:

| Nombre | Provincia | CP | Habitantes |
| --- | --- | --- | --- |
| Corrientes | Corrientes | 3400 | 346334 |
| Resistencia | Chaco | 3500 | 291720 |

Un `bool _yaVerificada` por instancia (*scoped*) evita repetir la consulta dentro del mismo
ámbito. Si otra petición de la misma sesión gana la carrera, el `DbUpdateException` se traga: los
datos ya están. Como la marca `Sesion` persiste, **borrar las dos localidades no vuelve a
sembrarlas** al recargar (lo verifica «Al borrar todas las localidades avisa que no hay datos»).

## Observaciones

- **Hecho**: la web y la API en desarrollo usan archivos SQLite distintos (`movilidad.db` y
  `movilidad-api.db`), así que una sesión creada por la API no es visible desde la web ni al revés.
  Ningún documento del repositorio afirma lo contrario.
- **Hecho**: ninguna `Infraestructura/` depende de ASP.NET Core. `MiddlewareDeSesion` vive en
  `MovilidadUrbana.Web/Sesiones/` justamente para eso: cuando estaba en la capa, la capa arrastraba
  `Microsoft.AspNetCore.App` y no podía usarse desde la app Android (comentario del archivo y
  `CHANGELOG.md` 2026-09-12).
- **Hecho**: las tres aplicaciones tienen **tres bases distintas** y ninguna comparte datos con otra:
  la app Android no habla con ningún servidor (`AndroidManifest.xml`: sin permiso `INTERNET` salvo el
  que agrega el SDK en Debug para el depurador).
