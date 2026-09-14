# 02 — Dominio y reglas de negocio

> **Propósito**: qué entidades existen, qué valida cada regla, qué catálogos comparten las pantallas
> y cómo los casos de uso traducen esas reglas en errores por campo.
> **Fuente primaria**: `src/MovilidadUrbana.Web/Dominio/` (`Entidades/`, `Reglas/`, `Catalogos.cs`) y
> `src/MovilidadUrbana.Web/Aplicacion/` (`Localidades/`, `Encuestas/`, `Resultado.cs`, `Abstracciones/`).
> Las mismas carpetas existen en `MovilidadUrbana.ApiWeb/` y `MovilidadUrbana.MAUI/` y difieren solo
> en el `namespace` (verificado con `diff -r`, ver [01](01_Arquitectura.md)): lo que sigue vale para
> las tres copias.
> **Vigencia**: 2026-09-12, commit `10ce735`.

## Entidades (`Dominio/Entidades/`)

| Entidad | Campos | Notas |
| --- | --- | --- |
| `Localidad` | `Id`, `SesionId`, `Nombre`, `Provincia`, `CodigoPostal`, `Habitantes` | `SesionId` aísla los datos de cada visitante: es lo que en la versión estática resolvía `localStorage` |
| `RespuestaDeEncuesta` | `Id`, `SesionId`, `Nombre`, `Edad`, `Localidad` (nombre, no clave), `Medios` (`IReadOnlyList<string>`), `Frecuencia`, `Distancia`, `Minutos`, `Motivo`, `RegistradaEn` | `Medios` se persiste como texto separado por comas ([03](03_Sesiones-Y-Persistencia.md)); guarda el **nombre** de la localidad, por eso la baja de una localidad no arrastra dependientes |
| `Sesion` | `Id`, `CreadaEn` | Marca de que la sesión ya recibió su siembra: sin ella, borrar todas las localidades volvería a sembrarlas |

Las entidades son clases con setters públicos, sin comportamiento: las reglas viven aparte.

## Reglas (`Dominio/Reglas/`)

### `ReglasDeLocalidad` (clase estática parcial)

| Constante | Valor | Regla | Función |
| --- | --- | --- | --- |
| `LargoMinimoDelNombre` | 3 | Nombre recortado con al menos 3 caracteres | `NombreValido(string?)` |
| `LargoMaximoDelNombre` | 60 | Solo se usa como `maxlength` en la vista y `HasMaxLength` en EF | — |
| `DigitosDelCodigoPostal` | 4 | Exactamente 4 dígitos (`^\d{4}$`, `GeneratedRegex`), recortado antes de validar | `CodigoPostalValido(string?)` |
| `HabitantesMinimos` | 1 | Entero no nulo ≥ 1 | `HabitantesValidos(int?)` |
| — | — | Provincia no vacía ni espacios | `ProvinciaValida(string?)` |
| — | — | Misma localidad = mismo nombre (recortado, **sin** distinguir mayúsculas) **y** misma provincia (comparación **ordinal**) | `MismaLocalidad(nombreA, provA, nombreB, provB)` |

### `ReglasDeEncuesta`

| Constante | Valor | Función |
| --- | --- | --- |
| `TotalDePasos` | 3 | Regla de dominio con prueba propia; gobierna el asistente y la API |
| `LargoMinimoDelNombre` / `LargoMaximoDelNombre` | 3 / 80 | `NombreValido` (mínimo; el máximo es `maxlength` y `HasMaxLength`) |
| `EdadMinima` / `EdadMaxima` | 16 / 110 | `EdadValida(int?)` — inclusivo |
| `DistanciaMinima` / `DistanciaMaxima` | 0 / 500 | `DistanciaValida(double?)` — **cero es válido**: se puede no viajar |
| `MinutosMinimos` / `MinutosMaximos` | 1 / 600 | `MinutosValidos(int?)` — **cero no es válido**, a diferencia de la distancia |

Las 49 pruebas unitarias cubren exactamente estos bordes ([05](05_Pruebas.md)).

## Catálogos (`Dominio/Catalogos.cs`)

| Catálogo | Valores (clave → etiqueta) |
| --- | --- |
| `Provincias` (solo nombre) | Buenos Aires, Chaco, Córdoba, Corrientes, Entre Ríos, Mendoza, Santa Fe |
| `Medios` | `colectivo` Colectivo · `auto` Auto particular · `bicicleta` Bicicleta · `moto` Moto · `caminata` A pie · `tren` Tren |
| `Frecuencias` | `diaria` Todos los días · `semanal` Algunos días por semana · `ocasional` Ocasionalmente |
| `Motivos` | `trabajo` Trabajo · `estudio` Estudio · `salud` Salud · `otros` Otros |

`EtiquetaDeMedio`, `EtiquetaDeFrecuencia` y `EtiquetaDeMotivo` devuelven la etiqueta o, si la
clave no está, la clave misma. La clave es lo que se persiste; la etiqueta, lo que se muestra.

## Casos de uso (`Aplicacion/`)

### `Resultado` (`Resultado.cs`)

`record Resultado(bool EsCorrecto, string Mensaje, IReadOnlyDictionary<string,string> Errores)`.
Las claves de `Errores` son los nombres de campo que la pantalla conoce: `nombre`, `provincia`,
`codigoPostal`, `habitantes`, `edad`, `localidad`, `medios`, `frecuencia`, `distancia`, `minutos`,
`motivo`. Constructores: `Correcto(mensaje)`, `Invalido(errores)` —con el mensaje fijo «Revise los
campos marcados en rojo.»— e `Invalido(campo, mensaje)`. La API reutiliza las mismas claves en
`ValidationProblemDetails` ([12](12_Api-REST.md)).

### `ServicioDeLocalidades` (`Localidades/ServicioDeLocalidades.cs`)

| Método | Flujo | Mensajes |
| --- | --- | --- |
| `ListarAsync` | delega al repositorio | — |
| `GuardarAsync(ModeloDeLocalidad)` | 1) `Validar` campo por campo → `Invalido(errores)`; 2) duplicado por `MismaLocalidad` contra los existentes (excluyendo el propio `Id`) → `Invalido("nombre", …)`; 3) si `Id` tiene valor, actualiza (si ya no existe: «La localidad ya no existe.»); si no, agrega | «El nombre debe tener al menos 3 caracteres.» · «Seleccione una provincia.» · «El código postal debe tener 4 dígitos.» · «Ingrese una cantidad de habitantes mayor a cero.» · «Ya existe una localidad con ese nombre en la provincia.» · «Se agregó la localidad {nombre}.» · «Se actualizó la localidad {nombre}.» |
| `EliminarAsync(id)` | si no existe → `Invalido("nombre", "La localidad ya no existe.")`; si no, elimina | «Se eliminó la localidad {nombre}.» |

`ModeloDeLocalidad` es lo que edita el ABM: `Id?`, `Nombre`, `Provincia`, `CodigoPostal`,
`Habitantes` (**anulable**, para distinguir «vacío» de «cero»), `EsEdicion => Id is not null`,
`Limpiar()`.

### `ServicioDeEncuestas` (`Encuestas/ServicioDeEncuestas.cs`)

| Método | Qué hace |
| --- | --- |
| `ContarAsync` | Encuestas de la sesión |
| `ValidarPaso(paso, ModeloDeEncuesta)` | Devuelve el diccionario de errores **del paso pedido** (1: nombre, edad, localidad · 2: medios, frecuencia · 3: distancia, minutos, motivo). Un paso fuera de 1..3 devuelve vacío |
| `RegistrarAsync(modelo)` | Construye `RespuestaDeEncuesta` con `Nombre` recortado, `Medios` **en el orden del catálogo** (no en el de tipeo, para que el resumen sea estable), `RegistradaEn = UtcNow`; persiste y devuelve la entidad |

Mensajes de `ValidarPaso`: «Ingrese nombre y apellido (mínimo 3 caracteres).» · «La edad debe
estar entre 16 y 110 años.» · «Seleccione una localidad.» · «Seleccione al menos un medio de
transporte.» · «Seleccione la frecuencia de uso.» · «Ingrese una distancia entre 0 y 500 km.» ·
«Ingrese un tiempo entre 1 y 600 minutos.» · «Seleccione el motivo principal del viaje.»

`ModeloDeEncuesta` acumula los tres pasos (`Nombre`, `Edad?`, `Localidad`; `Medios` como
`HashSet<string>` + `Frecuencia`; `Distancia?`, `Minutos?`, `Motivo`) y expone
`AlternarMedio(clave, elegido)`.

### Políticas: el requisito antes del intento

`PoliticaDeLocalidades` y `PoliticaDeEncuestas` son clases estáticas con propiedades de texto
derivadas de las constantes de las reglas («Entre 3 y 60 caracteres, único por provincia.»,
«4 dígitos.», «Entre 16 y 110 años.», «Entre 0 y 500 km por día.», …). Existen para que la pantalla
**no transcriba la política**: si un límite cambia en las reglas, el requisito cambia con él. Se
muestran antes del intento; el error al fallar lo decide el servicio (comentario en
`PoliticaDeLocalidades.cs`).

### `ResumenDeEncuesta` (`Encuestas/ResumenDeEncuesta.cs`)

`De(RespuestaDeEncuesta)` devuelve siete `CampoDeResumen(Clave, Etiqueta, Valor)` **ya
formateados**: `persona` «{Nombre} ({Edad} años)», `localidad`, `medios` (etiquetas unidas por
«, »), `frecuencia`, `distancia` «{0.###} km», `minutos` «{n} min», `motivo`. La vista y la API lo
recorren en vez de escribir la ficha a mano: agregar un campo lo hace aparecer sin tocar la
superficie. Con la cultura `es-AR` fijada en los `Program.cs`, `12.5` se muestra «12,5 km» (lo
verifican una E2E y una prueba de la API).

## Abstracciones (`Aplicacion/Abstracciones/`)

| Interfaz | Métodos | Implementación |
| --- | --- | --- |
| `IRepositorioDeLocalidades` | `ListarAsync`, `ObtenerAsync(id)`, `AgregarAsync`, `ActualizarAsync`, `EliminarAsync(id)` | `Infraestructura/Persistencia/RepositorioDeLocalidades.cs` |
| `IRepositorioDeEncuestas` | `AgregarAsync`, `ContarAsync` | `Infraestructura/Persistencia/RepositorioDeEncuestas.cs` |
| `IContextoDeSesion` | `string Id` | `Infraestructura/Sesiones/ContextoDeSesion.cs` |

Todos reciben `CancellationToken` opcional. No hay abstracción para «obtener una encuesta»: la API
devuelve `Location: /api/v1/encuestas/{id}` pero **no** expone ese GET ([12](12_Api-REST.md)).

En la app Android los ViewModels consumen `ServicioDeLocalidades` y `ServicioDeEncuestas` tal
cual —mismos mensajes de error, mismas claves— ([13](13_App-Android.md)); los 18 casos de
`MovilidadUrbana.MAUI.Tests` corren contra las capas reales de esa copia.
