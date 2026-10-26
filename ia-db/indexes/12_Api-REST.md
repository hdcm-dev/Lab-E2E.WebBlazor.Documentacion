# 12 — API REST de Movilidad Urbana

> **Propósito**: qué expone `MovilidadUrbana.ApiWeb` (rutas, contratos, códigos), cómo identifica la sesión por encabezado, cómo responde los errores, dónde se sirven OpenAPI y Scalar, y cómo se prueba en proceso.
> **Fuente primaria**: `src/MovilidadUrbana.ApiWeb/` (`Program.cs`, `Controllers/`, `Contracts/`, `Sessions/SessionHeaderMiddleware.cs`, `Infrastructure/Sessions/SessionContext.cs`, `MovilidadUrbana.ApiWeb.csproj`, `Properties/launchSettings.json`, `appsettings*.json`), `tests/MovilidadUrbana.ApiWeb.Tests/`, `.github/workflows/ci.yml`, `README.md` («La API»), `CHANGELOG.md` (2026-09-12 y 2026-09-18), `evidencia/2026-09-12-capas-y-api/`.
> **Vigencia**: versión 3.1, generada el 2026-10-25 sobre el commit `8fb4c3a` (2026-09-18).
> **Vecinos**: las reglas y mensajes que la API devuelve son de [02](02_Dominio-Y-Reglas.md); la base, la siembra y el aislamiento por sesión en las tres apps, de [03](03_Sesiones-Y-Persistencia.md); el reparto de capas y la composición en general, de [01](01_Arquitectura.md); el inventario de las siete suites, de [05](05_Pruebas.md); el job de CI que corre estas pruebas, de [06](06_CI-Y-Workflows.md); la guía que trata la API como superficie, de [07](07_Guias.md); la app Android, de [13](13_App-Android.md).

---

## 1. Qué es, en una tabla

| Aspecto | Valor | Fuente |
| --- | --- | --- |
| Proyecto | `MovilidadUrbana.ApiWeb`, SDK `Microsoft.NET.Sdk.Web`, `net10.0` | `MovilidadUrbana.ApiWeb.csproj:1,7` |
| Independencia | No referencia a ningún otro proyecto: trae `Domain/`, `Application/`, `Infrastructure/` propias (el comentario del csproj las nombra todavía «Dominio, Aplicacion, Infraestructura», ver §13) | `MovilidadUrbana.ApiWeb.csproj:3-5`, `README.md` «La API» |
| Paquetes | `Microsoft.EntityFrameworkCore.Sqlite` 10.0.11, `Microsoft.AspNetCore.OpenApi` 10.0.11, `Scalar.AspNetCore` 2.17.3 | `MovilidadUrbana.ApiWeb.csproj:15-17` |
| Documentación XML | `GenerateDocumentationFile=true`, `NoWarn CS1591` (los `<summary>` alimentan el contrato) | `MovilidadUrbana.ApiWeb.csproj:10-11` |
| Pruebas con acceso interno | `InternalsVisibleTo MovilidadUrbana.ApiWeb.Tests` | `MovilidadUrbana.ApiWeb.csproj:21` |
| Puerto local | `http://localhost:5250`, perfil `http`, `ASPNETCORE_ENVIRONMENT=Development`, sin abrir navegador | `Properties/launchSettings.json:7-9` |
| Base | `Data Source=datos/movilidad-api.db;Default Timeout=30` (cadena `BaseDeDatos`) | `appsettings.json:2` |
| Cultura | `es-AR` para hilos nuevos (formatos del resumen, p. ej. «12,5 km») | `Program.cs:11-13` |
| Presentación | Dos controllers MVC: `LocalidadesController`, `EncuestasController` | `Controllers/` |

Las capas `Domain/`, `Application/` e `Infrastructure/Persistence/` son **idénticas** a las de la web y la app Android salvo el espacio de nombres (verificado el 2026-10-25: mismo hash MD5 de su concatenación tras reemplazar `MovilidadUrbana.<App>`). Su contenido está en [02](02_Dominio-Y-Reglas.md) y [03](03_Sesiones-Y-Persistencia.md).

```
src/MovilidadUrbana.ApiWeb/
├── Program.cs                         composición + pipeline
├── Controllers/
│   ├── LocalidadesController.cs       ABM  /api/v1/localidades
│   ├── EncuestasController.cs         /api/v1/encuestas
│   └── ValidationProblems.cs          errores por campo → ValidationProblemDetails
├── Contracts/
│   ├── Localidades.cs                 LocalidadDto, LocalidadRequest
│   └── Encuestas.cs                   EncuestaRequest, EncuestaRegistradaDto, CampoDeResumenDto,
│                                      ValidacionDePasoDto, ContadorDeEncuestasDto
├── Sessions/SessionHeaderMiddleware.cs   X-Sesion-Id
├── Domain/  Application/  Infrastructure/  (copias propias; ver 02 y 03)
├── Properties/launchSettings.json     :5250
└── appsettings.json / appsettings.Development.json
```

---

## 2. Composición y pipeline (`Program.cs`)

```
CreateBuilder
 ├─ CultureInfo es-AR (DefaultThread*)                                    :11-13
 ├─ cadena = ConnectionStrings:BaseDeDatos ?? Infrastructure.DependencyInjection.DefaultConnectionString  :16-17
 ├─ AddInfrastructure(cadena)  → DbContextFactory, SessionContext (scoped), SessionSeeder, repositorios   :18
 ├─ AddApplication()           → LocalidadService, EncuestaService (scoped)                               :19
 ├─ AddControllers · AddProblemDetails · AddOpenApi                                                       :22-24
Build
 ├─ DatabaseInitializer.Initialize  (EnsureCreated + PRAGMA journal_mode=WAL)                             :28
 ├─ UseExceptionHandler · UseStatusCodePages                                                              :30-31
 ├─ [Development] MapOpenApi · MapScalarApiReference(título, cliente Shell/Curl)                          :33-42
 ├─ UseMiddleware<SessionHeaderMiddleware>                                                                :44
 └─ MapControllers                                                                                        :45
public partial class Program;   ← visible para WebApplicationFactory                                     :50
```

- `Program.cs` califica `MovilidadUrbana.ApiWeb.Infrastructure.DependencyInjection.DefaultConnectionString` porque las dos capas exponen una clase `DependencyInjection` (consecuencia del renombre, `CHANGELOG.md` 2026-09-18).
- `DefaultConnectionString` de la capa es `datos/movilidad.db`, pero la API siempre lo pisa con `movilidad-api.db` desde `appsettings.json` (`Infrastructure/DependencyInjection.cs:15`, `appsettings.json:2`).
- La ruta `datos/…` es relativa al directorio de trabajo del proceso: ver [03](03_Sesiones-Y-Persistencia.md) §7.

---

## 3. Rutas

Ocho operaciones, todas con `[ApiController]` y `[Produces("application/json")]`.

| Verbo y ruta | Acción | Cuerpo de entrada | Éxito | Otros códigos declarados | Fuente |
| --- | --- | --- | --- | --- | --- |
| `GET /api/v1/localidades` | `GetAll` | — | 200 `LocalidadDto[]` | — | `LocalidadesController.cs:18-24` |
| `GET /api/v1/localidades/{id:int}` | `GetById` | — | 200 `LocalidadDto` | 404 | `:27-34` |
| `POST /api/v1/localidades` | `Create` | `LocalidadRequest` | 201 + `Location` (vía `CreatedAtAction(GetById)`) | 400 `ValidationProblemDetails` | `:37-51` |
| `PUT /api/v1/localidades/{id:int}` | `Update` | `LocalidadRequest` | 200 `LocalidadDto` | 400, 404 | `:54-68` |
| `DELETE /api/v1/localidades/{id:int}` | `Delete` | — | 204 | 404 | `:71-78` |
| `GET /api/v1/encuestas/contador` | `GetCount` | — | 200 `ContadorDeEncuestasDto` | — | `EncuestasController.cs:18-21` |
| `POST /api/v1/encuestas/pasos/{paso:int}/validacion` | `ValidarPaso` | `EncuestaRequest` | 200 `ValidacionDePasoDto` (también cuando el paso es inválido) | 404 si `paso` ∉ 1..3 | `:24-33` |
| `POST /api/v1/encuestas` | `Registrar` | `EncuestaRequest` | 201 `EncuestaRegistradaDto` + `Location: /api/v1/encuestas/{id}` | 400 `ValidationProblemDetails` | `:36-55` |

Detalles de comportamiento, leídos del código:

| Caso | Qué hace | Fuente |
| --- | --- | --- |
| Alta de localidad | El servicio no devuelve la entidad: el controller relee la lista y la ubica por `Nombre.Trim()` + `Provincia` (únicos por sesión) | `LocalidadesController.cs:45-48` |
| Modificación | Primero 404 si el id no es de la sesión; después `SaveAsync` con `model.Id = id` | `:60-65` |
| Baja | `DeleteAsync` devuelve inválido si no existe → 404 | `:76-77` |
| Registrar encuesta | Valida los **tres** pasos y junta los errores en un solo diccionario antes de guardar | `EncuestasController.cs:43-46` |
| Medios | `ToModel` marca cada medio recibido con `AlternarMedio(medio, elegido: true)`; al registrar se guardan en el orden del catálogo | `EncuestasController.cs:69`, `Application/Encuestas/EncuestaService.cs:77-78` |
| Nulos en la entrada | Todo campo del request es anulable; `ToModel` convierte `null` de texto en `""` para que la validación lo rechace con su mensaje | `LocalidadesController.cs:82-88`, `EncuestasController.cs:57-71` |

---

## 4. Contratos (`Contracts/`)

| Registro | Campos (C#) | Uso |
| --- | --- | --- |
| `LocalidadDto` | `Id`, `Nombre`, `Provincia`, `CodigoPostal`, `Habitantes` | salida del ABM |
| `LocalidadRequest` | `Nombre?`, `Provincia?`, `CodigoPostal?`, `Habitantes?` | alta y modificación |
| `EncuestaRequest` | `Nombre?`, `Edad?`, `Localidad?`, `Medios?` (lista), `Frecuencia?`, `Distancia?` (double), `Minutos?`, `Motivo?` | los tres pasos en un envío |
| `EncuestaRegistradaDto` | `Id`, `RegistradaEn` (`DateTimeOffset`), `Resumen` (`CampoDeResumenDto[]`) | 201 de registrar |
| `CampoDeResumenDto` | `Clave`, `Etiqueta`, `Valor` (ya formateado en es-AR) | ficha de revisión |
| `ValidacionDePasoDto` | `Paso`, `Valido`, `Errors` (diccionario campo → mensaje) | validación de un paso |
| `ContadorDeEncuestasDto` | `Cantidad` | contador de la sesión |

- Serialización: no hay `JsonPropertyName` ni opciones de serializador en el proyecto (búsqueda sin resultados en `src/MovilidadUrbana.ApiWeb`), así que rige la política por defecto de ASP.NET Core, camelCase. La corrida del 2026-09-12 lo muestra: `{"id":1,"registradaEn":…,"resumen":[{"clave":"persona","etiqueta":"Persona","valor":"Ana Pérez (34 años)"},…]}` y `{"cantidad":1}` (`evidencia/2026-09-12-capas-y-api/api-kestrel-openapi-y-curl.log`).
- Claves de `resumen`: `persona`, `localidad`, `medios`, `frecuencia`, `distancia`, `minutos`, `motivo` (`Application/Encuestas/ResumenDeEncuesta.cs:21-27`).
- Claves de error por campo, las mismas que la web: `nombre`, `provincia`, `codigoPostal`, `habitantes` (localidad); `nombre`, `edad`, `localidad`, `medios`, `frecuencia`, `distancia`, `minutos`, `motivo` (encuesta) (`Application/Localidades/LocalidadService.cs:76-92`, `Application/Encuestas/EncuestaService.cs:23-63`). Los textos de cada mensaje están en [02](02_Dominio-Y-Reglas.md).

Ejemplo mínimo (de `README.md` «La API»):

```bash
dotnet run --project src/MovilidadUrbana.ApiWeb          # http://localhost:5250 — la documentación, en /scalar/v1
curl -i http://localhost:5250/api/v1/localidades          # devuelve X-Sesion-Id
curl -H "X-Sesion-Id: <el que vino>" http://localhost:5250/api/v1/encuestas/contador
```

---

## 5. Sesión por encabezado `X-Sesion-Id`

```
cliente ──GET /api/v1/localidades (sin encabezado)──▶ SessionHeaderMiddleware
                                                      │ header vacío → SessionContext conserva su Guid "n" provisorio
                                                      │ Response.OnStarting: X-Sesion-Id = session.Id
        ◀──200 + X-Sesion-Id: 8544…cd────────────────┘
cliente ──GET … X-Sesion-Id: 8544…cd──▶ middleware: IsValid → session.Set(id)
                                        repositorio filtra por SessionId; primera lectura siembra Corrientes y Resistencia
```

| Regla | Valor | Fuente |
| --- | --- | --- |
| Nombre del encabezado | `X-Sesion-Id` (`SessionHeaderMiddleware.HeaderName`) | `Sessions/SessionHeaderMiddleware.cs:12` |
| Validez | no vacío ni blanco, largo ≤ 64 (`SessionContext.MaxLength`); no se exige formato | `Infrastructure/Sessions/SessionContext.cs:13,22-23` |
| Encabezado inválido o ausente | se ignora y la petición usa un Guid nuevo (`ToString("n")`), que vuelve en la respuesta | `SessionContext.cs:15`, `SessionHeaderMiddleware.cs:16-23` |
| Eco | siempre: la respuesta lleva el id efectivo, también cuando el cliente mandó uno válido | `SessionHeaderMiddleware.cs:19-23` |
| Alcance | `SessionContext` es scoped: una petición HTTP | `Infrastructure/DependencyInjection.cs:23-24` |
| Equivalente | la cookie en la web (`SessionHeaderMiddleware.cs:6-8`); el dispositivo en Android, ver [03](03_Sesiones-Y-Persistencia.md) | `SessionHeaderMiddleware.cs:6-8` |

- El identificador no autentica: quien conozca el id de otra sesión ve sus datos. Es un aislamiento de laboratorio para que las pruebas en paralelo no se pisen, no un control de acceso (deducido del código; ningún documento del repo lo trata como seguridad).
- Las encuestas no siembran nada: `EncuestaRepository` no usa `SessionSeeder`; la siembra ocurre en la primera operación sobre localidades (`Infrastructure/Persistence/EncuestaRepository.cs`, `LocalidadRepository.cs:22,33,42`).

---

## 6. Errores

| Situación | Respuesta | Quién la arma | Fuente |
| --- | --- | --- | --- |
| Validación de negocio (campos) | 400 `ValidationProblemDetails`, `title` «La solicitud tiene datos inválidos.», `errors: { campo: [mensaje] }` (RFC 9457) | `ValidationProblems.De` | `Controllers/ValidationProblems.cs:11-19` |
| Duplicado nombre + provincia | 400 con `errors.nombre` = «Ya existe una localidad con ese nombre en la provincia.» | `LocalidadService.SaveAsync` | `Application/Localidades/LocalidadService.cs:23-26` |
| Id inexistente o de otra sesión | 404 | controller | `LocalidadesController.cs:33,60,77` |
| Paso fuera de 1..3 | 404 | controller | `EncuestasController.cs:29` |
| Código de estado sin cuerpo | cuerpo ProblemDetails | `AddProblemDetails` + `UseStatusCodePages` | `Program.cs:23,31` |
| Excepción no controlada | ProblemDetails | `UseExceptionHandler` | `Program.cs:30` |
| JSON mal formado o tipo incorrecto | 400 automático de `[ApiController]` | framework | **no verificado**: ningún caso lo ejercita |

`ValidationProblems` traduce el `IReadOnlyDictionary<string,string>` de la capa de aplicación sin que esta sepa de HTTP (`ValidationProblems.cs:5-8`). La forma del cuerpo de 400 la fijan dos pruebas (§9).

---

## 7. OpenAPI y Scalar

| Qué | Dónde | Entorno | Evidencia |
| --- | --- | --- | --- |
| Contrato OpenAPI | `/openapi/v1.json` (`MapOpenApi`) | solo Development (`Program.cs:33-38`) | la corrida sobre Kestrel lista `MovilidadUrbana.ApiWeb \| v1 3.1.1` y las ocho operaciones (`evidencia/2026-09-12-capas-y-api/api-kestrel-openapi-y-curl.log`) |
| Documentación navegable | `/scalar/v1` (`MapScalarApiReference`), título «Movilidad Urbana — API», ejemplos en `curl` (`ScalarTarget.Shell`, `ScalarClient.Curl`) | solo Development (`Program.cs:39-41`) | `GET /scalar/v1 -> 200 text/html` en Development y `404` en Production (`evidencia/2026-09-12-capas-y-api/scalar-development-y-production.log`) |

- El README y el CHANGELOG dicen «OpenAPI 3.1»; la evidencia muestra la versión `3.1.1`.
- Scalar se sumó en `3b53d14` (2026-09-12): «verificado 200 en Development y 404 en Production».
- **Desfasaje comentario/código**: `Program.cs:35-37` dice que el encabezado de sesión «se declara ahí mismo» en la documentación, pero `AddOpenApi()` se llama sin opciones ni transformadores (`Program.cs:24`) y no hay otra mención de `X-Sesion-Id` en la configuración OpenAPI. Lo que sí hay es la indicación manual del README: «repetí el `X-Sesion-Id` en el encabezado de cada pedido». Que el contrato publicado no lo declare se deduce del código; no se volvió a inspeccionar el JSON generado.
- La corrida de la evidencia no pudo listar con `python3` («command not found»); el listado de rutas que sí aparece salió de otra herramienta que el log no identifica.

---

## 8. Arnés de pruebas (`tests/MovilidadUrbana.ApiWeb.Tests`)

| Pieza | Qué hace | Fuente |
| --- | --- | --- |
| Proyecto | `net10.0`, NUnit 4.3.2, `Microsoft.AspNetCore.Mvc.Testing` 10.0.11, `Microsoft.NET.Test.Sdk` 17.14.0, `NUnit3TestAdapter` 5.0.0, `NUnit.Analyzers` 4.7.0; `ProjectReference` a la API | `MovilidadUrbana.ApiWeb.Tests.csproj` |
| `ApiWebApplicationFactory` | `WebApplicationFactory<Program>` en Development; pisa `ConnectionStrings:BaseDeDatos` con `%TEMP%/movilidad-api-<guid>.db`; al `Dispose` borra `.db`, `-wal`, `-shm` | `ApiWebApplicationFactory.cs:10-24` |
| Una fábrica por clase | `[OneTimeSetUp]` / `[OneTimeTearDown]` en cada fixture | `LocalidadesTests.cs:13-14`, `EncuestasTests.cs:13-14`, `DocumentationTests.cs:10-11` |
| Sesión por caso | `CreateClient()` agrega `X-Sesion-Id: <Guid nuevo>` («cada caso estrena su sesión, igual que las E2E de la web estrenan su cookie») | `LocalidadesTests.cs:16-22`, `EncuestasTests.cs:16-21` |
| Lectura del 400 | record privado `ProblemaDeValidacion(Title, Status, Errors)` | `LocalidadesTests.cs:110`, `EncuestasTests.cs:77` |

Sin Kestrel ni navegador (`MovilidadUrbana.ApiWeb.Tests.csproj:3`).

### Los 13 casos (contados con `grep -c '\[Test\]'`: 7 + 4 + 2)

| Clase | Caso | Afirma |
| --- | --- | --- |
| `LocalidadesTests` | `UnaSesionNuevaArrancaConLasSembradas` | GET devuelve exactamente Corrientes y Resistencia |
| | `SinEncabezadoLaRespuestaDevuelveUno` | sin `X-Sesion-Id` la respuesta trae uno no vacío |
| | `DaDeAltaUnaLocalidad` | 201, `Location` termina en `/api/v1/localidades/{id}`, la misma sesión la lista |
| | `RechazaElAltaConCamposInvalidos` | 400 con claves `nombre`, `provincia`, `codigoPostal`, `habitantes` |
| | `NoPermiteDuplicar` | 400 al repetir Corrientes/Corrientes |
| | `ModificaYDaDeBaja` | PUT 200 con el nombre nuevo, DELETE 204, GET 404 |
| | `CadaSesionTieneSusDatos` | lo que da de alta una sesión no aparece en otra |
| `EncuestasTests` | `RegistraUnaEncuestaCompleta` | 201; `medios` = «Colectivo, Bicicleta»; `distancia` = «12,5 km»; contador = 1 |
| | `RechazaUnaEncuestaIncompleta` | 400 con las ocho claves de los tres pasos |
| | `ValidaUnPasoPorSeparado` | paso 2 vacío → `Valido=false`, claves `medios` y `frecuencia`; contador sigue en 0 |
| | `UnPasoInexistenteEs404` | paso 4 → 404 |
| `DocumentationTests` | `ElContratoOpenApiDeclaraLasRutas` | el JSON contiene `/api/v1/localidades`, `/api/v1/encuestas`, `…/pasos/{paso}/validacion`, `…/contador` |
| | `ScalarSeSirveYApuntaAlContrato` | `/scalar/v1` 200 `text/html` con el título y `openapi/v1.json` |

- La descripción de `ElContratoOpenApiDeclaraLasRutas` dice «declara las ocho rutas», pero comprueba cuatro rutas de nivel `paths`; `/api/v1/localidades/{id}` no se busca (`DocumentationTests.cs:14-20`).
- Cómo se corre: `dotnet test tests/MovilidadUrbana.ApiWeb.Tests` (`README.md` «Desde la línea de comandos»); en CI, paso «Pruebas de la API» del job `compilacion` de `ci.yml:69-75`, con TRX `api.trx` en `resultados/` ([06](06_CI-Y-Workflows.md)).

### Huecos de cobertura, leídos del código

| Comportamiento | ¿Hay caso? |
| --- | --- |
| PUT/GET/DELETE con id de otra sesión → 404 | no (solo se prueba que la lista no se mezcla) |
| PUT con datos inválidos → 400 | no |
| Encabezado `X-Sesion-Id` de más de 64 caracteres | no |
| `Location` de la encuesta registrada | no |
| Medio fuera del catálogo | no |
| JSON mal formado | no |

---

## 9. Observaciones del código (sin caso que las fije)

| Observación | Detalle | Fuente |
| --- | --- | --- |
| `Location` de encuesta sin destino | `Registrar` responde `Created("/api/v1/encuestas/{id}")`, pero no existe `GET /api/v1/encuestas/{id}`: esa URL daría 404 | `EncuestasController.cs:54`; rutas del §3 |

Los huecos de validación que por la API quedan expuestos sin el freno de un `<select>` o un `maxlength` —provincia y localidad fuera de catálogo, medio desconocido registrado como lista vacía, largo máximo del nombre no aplicado— son de las reglas compartidas: [02](02_Dominio-Y-Reglas.md) §8 (H1–H4).

---

## 10. El contrato JSON cambió con el renombre

El README («Convención de nombres»), el CHANGELOG (2026-09-18) y el mensaje de `946d023` («Proyectos, URL, contrato JSON, data-testid, AutomationId y textos visibles no cambian») afirman que el renombre **no cambió el contrato JSON de la API**; la guía de nomenclatura dice que «si un DTO se renombra por dentro, se conserva el nombre en el JSON» (`/LAB/Lab-Documentos/Lab-Documentos/Guides/Testing/Lab-E2E.WebBlazor-Guides/Nomenclatura-Convensiones-Arquitecture-Dot-Net.md:76`). El historial muestra una excepción:

| Antes (`3e119b8`) | Después (`8fb4c3a`) | Efecto en el JSON |
| --- | --- | --- |
| `ValidacionDePasoDto(int Paso, bool Valido, … Errores)` | `ValidacionDePasoDto(int Paso, bool Valido, … Errors)` | la propiedad pasa de `errores` a `errors` (camelCase por defecto, sin `JsonPropertyName`) |
| `SolicitudDeLocalidad`, `SolicitudDeEncuesta` | `LocalidadRequest`, `EncuestaRequest` | los nombres de propiedad no cambian; que cambien los nombres de esquema del documento OpenAPI se deduce (los genera el tipo), no se comparó el JSON |

Verificado con `git show 3e119b8:src/MovilidadUrbana.ApiWeb/Contratos/Encuestas.cs`. El efecto en el cable se deduce del código; no hay corrida posterior al renombre que muestre el JSON de `/pasos/{paso}/validacion`. La prueba `ValidaUnPasoPorSeparado` no lo detecta porque deserializa con el mismo DTO renombrado. Las rutas no cambiaron.

---

## 11. Evidencia (`evidencia/2026-09-12-capas-y-api/`)

| Archivo | Qué registra |
| --- | --- |
| `api-tests.log` | `Passed! 13/13` (2 s) |
| `api-falsificacion-201.log` | `Failed 1, Passed 10, Total 11`: la falsificación 200 en vez de 201 pone un caso en rojo; es de antes de sumar los dos casos de documentación (`CHANGELOG.md` 2026-09-12: «la API 11/11, una falsificación») |
| `api-kestrel-openapi-y-curl.log` | corrida real: sesión asignada, POST inválido 400, registro con resumen, `{"cantidad":1}`, OpenAPI `v1 3.1.1` con las ocho operaciones, GET con las dos sembradas |
| `scalar-development-y-production.log` | `/scalar/v1` 200 en Development, 404 en Production |
| `movilidad-e2e-tras-extraer-capas.log` | 22/22 E2E de la web tras extraer las capas (contexto: [05](05_Pruebas.md)) |

---

## 12. Historia

| Commit | Fecha | Qué pasó con la API |
| --- | --- | --- |
| `88e5caa` | 2026-09-12 | Nace la API REST; las capas se extraen a proyectos `MovilidadUrbana.Dominio/.Aplicacion/.Infraestructura` |
| `3b53d14` | 2026-09-12 | Scalar en `/scalar/v1`; dos casos de documentación; 13/13 |
| `10ce735` | 2026-09-12 | Las tres apps vuelven a ser independientes: la API trae sus capas como carpetas (`Dominio/`, `Aplicacion/`, `Infraestructura/`) |
| `946d023` | 2026-09-18 | Convención inglés/español: carpetas, clases y miembros renombrados (ver §13) |
| `e9dea2a` | 2026-09-18 | Se renombran las referencias `cref` que el primer paso dejó viejas (la CI falló con `CS1574`) |

---

## 13. Rastros de nombres previos al renombre

Mapa de nombres de la API (de `git ls-tree 3e119b8` y `git show -M 946d023`):

| Antes | Ahora |
| --- | --- |
| `Sesiones/MiddlewareDeSesionPorEncabezado` | `Sessions/SessionHeaderMiddleware` |
| `Infraestructura/Sesiones/ContextoDeSesion` | `Infrastructure/Sessions/SessionContext` |
| `ServicioDeLocalidades` / `ServicioDeEncuestas` | `LocalidadService` / `EncuestaService` |
| `IRepositorioDeLocalidades` / `IRepositorioDeEncuestas` | `ILocalidadRepository` / `IEncuestaRepository` |
| `Contratos/`, `SolicitudDeLocalidad`, `SolicitudDeEncuesta` | `Contracts/`, `LocalidadRequest`, `EncuestaRequest` |
| `ProblemasDeValidacion` | `ValidationProblems` |
| `Resultado`, `ServiciosDeAplicacion`, `ServiciosDeInfraestructura` | `Result`, `Application/DependencyInjection`, `Infrastructure/DependencyInjection` |
| acciones `Listar`, `Obtener`, `Crear`, `Modificar`, `Eliminar`, `Contar`; `ADto`, `AModelo`; parámetro `cancelacion` | `GetAll`, `GetById`, `Create`, `Update`, `Delete`, `GetCount`; `ToDto`, `ToModel`; `cancellationToken` |
| `FabricaDeApi`, `DocumentacionTests` | `ApiWebApplicationFactory`, `DocumentationTests` |

Los rastros que quedaron en la prosa del código vigente de la API (`MiddlewareDeSesionPorEncabezado` en `SessionContext.cs:8`, `ObtenerAsync` en `LocalidadRepository.cs:52`, «Dominio, Aplicacion, Infraestructura» en el `.csproj`, y los comentarios copiados de la web sobre cookies, circuito, WAL y «la web y la API») están en el inventario de [01](01_Arquitectura.md) §8.3. El `CHANGELOG.md` 2026-09-12 conserva `AgregarAplicacion()`, `AgregarInfraestructura(cadena)` y `MiddlewareDeSesion` como registro histórico.

---

## No verificado

- El 400 automático de `[ApiController]` ante JSON mal formado: ningún caso ni evidencia lo muestra.
- Que el documento OpenAPI generado no declare `X-Sesion-Id`: se deduce del código, no se inspeccionó el JSON en esta versión.
- El cambio `errores` → `errors` en el cuerpo de `/pasos/{paso}/validacion`: se deduce del código, sin corrida posterior al renombre.
- Con qué herramienta salió el listado de rutas de `api-kestrel-openapi-y-curl.log`: el log no lo dice.
- La ubicación real de `datos/movilidad-api.db` al correr con `dotnet run --project`: depende del directorio de trabajo; no se corrió en esta regeneración.
