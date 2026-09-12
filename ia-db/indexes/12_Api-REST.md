# 12 — La API REST de Movilidad Urbana

> **Propósito**: registrar qué expone `MovilidadUrbana.ApiWeb`, cómo identifica la sesión, cómo
> devuelve los errores y cómo se prueba, para que un agente pueda consumirla o extenderla sin abrir
> los controllers.
> **Fuente primaria**: `src/MovilidadUrbana.ApiWeb/`, `tests/MovilidadUrbana.ApiWeb.Tests/`,
> `evidencia/2026-09-12-capas-y-api/`.
> **Vigencia**: 2026-09-12, commit `3b53d14`.

## Qué es

La misma aplicación de Movilidad Urbana **sin interfaz**: una segunda cabeza sobre las mismas capas
que la web —`MovilidadUrbana.Aplicacion` e `Infraestructura`—, con dos controllers. Existe desde el
2026-09-12, y para que existiera sin duplicar las reglas las capas se extrajeron a proyectos propios
— ver [01](01_Arquitectura.md). Escucha en `http://localhost:5250` (`launchSettings.json`).

```
src/MovilidadUrbana.ApiWeb/
├── Controllers/   LocalidadesController, EncuestasController, ProblemasDeValidacion
├── Contratos/     DTOs de entrada (Solicitud*) y de salida (*Dto)
├── Sesiones/      MiddlewareDeSesionPorEncabezado
└── Program.cs     Compone las capas, AddControllers, AddProblemDetails, AddOpenApi y Scalar
```

## Rutas

| Método | Ruta | Devuelve |
| --- | --- | --- |
| GET | `/api/v1/localidades` | `200` lista de `LocalidadDto` |
| GET | `/api/v1/localidades/{id}` | `200` o `404` |
| POST | `/api/v1/localidades` | `201` con `Location` y la localidad creada; `400` con errores por campo |
| PUT | `/api/v1/localidades/{id}` | `200` con la localidad; `400`; `404` |
| DELETE | `/api/v1/localidades/{id}` | `204`; `404` |
| POST | `/api/v1/encuestas` | `201` con `EncuestaRegistradaDto` —id, fecha y el resumen de `ResumenDeEncuesta`—; `400` con los errores de los tres pasos |
| POST | `/api/v1/encuestas/pasos/{paso}/validacion` | `200` con `ValidacionDePasoDto` (`valido`, `errores`); `404` si el paso no es 1–3 |
| GET | `/api/v1/encuestas/contador` | `200` `{ cantidad }` de la sesión |

El contrato OpenAPI 3.1 se sirve en `/openapi/v1.json` en Development (`Microsoft.AspNetCore.OpenApi`
10.0.11). Las ocho rutas se verificaron en él sobre Kestrel el 2026-09-12.

## Documentación navegable: Scalar

`Scalar.AspNetCore` 2.17.3 sirve en **`/scalar/v1`**, solo en Development, la documentación del
contrato: cada ruta con su esquema, y probable desde el navegador con ejemplos en `curl` (cliente
por defecto configurado en `Program.cs`). Para ver datos propios hay que repetir el `X-Sesion-Id` en
cada pedido. Verificado el 2026-09-12: `200 text/html` en Development y `404` en Production.

## La sesión: encabezado `X-Sesion-Id`

La web aísla los datos de cada visitante con una cookie; en una API eso no es idiomático.
`MiddlewareDeSesionPorEncabezado` lee `X-Sesion-Id` y lo establece en el mismo `ContextoDeSesion` de
Infraestructura. **Si el cliente no lo manda, la respuesta lo devuelve** —un identificador nuevo—
para que lo repita en las siguientes. Sin repetirlo, cada petición es una sesión distinta: la
siembra vuelve a aparecer y lo creado no.

Es el mismo aislamiento que habilita el paralelismo de las E2E de la web: cada prueba de la API
estrena un `X-Sesion-Id`, igual que cada E2E estrena su cookie.

## Errores

- **Validación**: `400` con `ValidationProblemDetails` (RFC 9457). `ProblemasDeValidacion.De`
  traduce el `Resultado.Errores` de Aplicación, así que las claves son **las mismas que en la web**:
  `nombre`, `provincia`, `codigoPostal`, `habitantes`, `edad`, `medios`, … La API no valida por su
  cuenta: reutiliza `ServicioDeLocalidades.GuardarAsync` y `ServicioDeEncuestas.ValidarPaso`.
- **No encontrado**: `404` sin cuerpo (`NotFound()`).
- **Excepciones**: `AddProblemDetails` + `UseExceptionHandler`, respuesta `application/problem+json`.

Detalle de `Crear`: el servicio no devuelve la entidad creada, así que el controller la ubica por
nombre y provincia —que el propio servicio garantiza únicos dentro de la sesión— para armar el
`Location`.

## Pruebas

`tests/MovilidadUrbana.ApiWeb.Tests`, 13 casos NUnit en proceso con `WebApplicationFactory<Program>`
(`Microsoft.AspNetCore.Mvc.Testing` 10.0.11). `FabricaDeApi` arranca la API en Development sobre una
base SQLite **propia de la corrida** en la carpeta temporal, y la borra al terminar: no toca `datos/`.

| Clase | Casos |
| --- | --- |
| `LocalidadesTests` (7) | Sesión nueva con las sembradas · sin encabezado la respuesta devuelve uno · alta con `201` y `Location` · `400` por campo con las cuatro claves · no duplica · modifica y da de baja (`200`, `204`, `404`) · cada sesión tiene sus datos |
| `EncuestasTests` (4) | Registra una completa (`201`, resumen `"Colectivo, Bicicleta"` y `"12,5 km"`, contador 1) · incompleta (`400` con las ocho claves) · valida un paso sin registrar · paso 4 es `404` |
| `DocumentacionTests` (2) | El contrato declara las rutas · Scalar se sirve y apunta al contrato |

`ci.yml` las corre en el job `compilacion`, después de las unitarias.

**Verificado el 2026-09-12** (`evidencia/2026-09-12-capas-y-api/`): 13/13; una falsificación
—responder `200` en vez de `201` en el alta— pone un caso en rojo; y sobre Kestrel, el OpenAPI con
las ocho rutas y un flujo por `curl`: `X-Sesion-Id` asignado, listado sembrado, `400` a un alta
inválida, `201` a una encuesta y contador en 1.

## Lo que no tiene

- Autenticación: la sesión identifica un espacio de datos, no a una persona. Igual que la web.
- `GET /api/v1/encuestas/{id}`: el `Location` del `201` apunta ahí, pero la ruta no existe todavía
  — `IRepositorioDeEncuestas` solo agrega y cuenta.
- Catálogos (provincias, medios, frecuencias, motivos) como recurso: un cliente hoy tiene que
  conocer las claves.
- Versionado más allá del prefijo `v1` de la ruta.

## Cómo verificar todo esto

| Afirmación | Comprobación |
| --- | --- |
| Las rutas | `dotnet run --project src/MovilidadUrbana.ApiWeb` y `curl http://localhost:5250/openapi/v1.json` |
| La sesión por encabezado | `curl -i http://localhost:5250/api/v1/localidades` devuelve `X-Sesion-Id` |
| Las pruebas | `dotnet test tests/MovilidadUrbana.ApiWeb.Tests` |
