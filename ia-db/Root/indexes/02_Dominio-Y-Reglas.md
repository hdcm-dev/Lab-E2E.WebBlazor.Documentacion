# 02 — Dominio y reglas de negocio

> **Propósito**: registrar qué se modela, qué valida cada regla y con qué límites, para poder
> razonar sobre el comportamiento esperado sin abrir el código.
> **Fuente primaria**: `src/MovilidadUrbana.Web/Dominio/` y `src/MovilidadUrbana.Web/Aplicacion/`.

## Entidades

`Dominio/Entidades/`. Las tres llevan `SesionId` o son la sesión misma: el aislamiento por sesión es
parte del modelo, no un agregado de infraestructura.

| Entidad | Campos | Nota |
| --- | --- | --- |
| `Localidad` | `Id`, `SesionId`, `Nombre`, `Provincia`, `CodigoPostal`, `Habitantes` | `SesionId` es lo que en la versión estática del laboratorio resolvía `localStorage` |
| `RespuestaDeEncuesta` | `Id`, `SesionId`, `Nombre`, `Edad`, `Localidad`, `Medios` (lista), `Frecuencia`, `Distancia`, `Minutos`, `Motivo`, `RegistradaEn` | `Medios` se persiste como texto separado por comas — ver [03](03_Sesiones-Y-Persistencia.md) |
| `Sesion` | `Id`, `CreadaEn` | Marca de que la sesión **ya recibió** su juego de datos inicial. Sin ella, borrar todas las localidades volvería a sembrarlas |

## Catálogos

`Dominio/Catalogos.cs` — valores fijos que comparten pantallas y reglas.

| Catálogo | Valores |
| --- | --- |
| `Provincias` | Buenos Aires, Chaco, Córdoba, Corrientes, Entre Ríos, Mendoza, Santa Fe |
| `Medios` | `colectivo`, `auto`, `bicicleta`, `moto`, `caminata`, `tren` (clave → etiqueta) |
| `Frecuencias` | `diaria`, `semanal`, `ocasional` |
| `Motivos` | `trabajo`, `estudio`, `salud`, `otros` |

Los tres últimos son pares **(clave persistida, etiqueta mostrada)**, con `EtiquetaDeMedio`,
`EtiquetaDeFrecuencia` y `EtiquetaDeMotivo` para traducir. Lo que se guarda es la clave; lo que se
verifica en pantalla es la etiqueta.

## ReglasDeLocalidad

`Dominio/Reglas/ReglasDeLocalidad.cs` — clase `static partial`, con el código postal como
`[GeneratedRegex]`.

| Regla | Criterio |
| --- | --- |
| `NombreValido` | Al menos 3 caracteres **una vez recortado** (`LargoMinimoDelNombre`) |
| `ProvinciaValida` | No vacía ni solo espacios |
| `CodigoPostalValido` | Exactamente 4 dígitos: `^\d{4}$`, sobre el valor recortado |
| `HabitantesValidos` | No nulo y ≥ 1 (`HabitantesMinimos`) |
| `MismaLocalidad` | Mismo nombre **sin distinguir mayúsculas** y misma provincia **de forma ordinal** |

Constantes públicas: `LargoMinimoDelNombre = 3`, `LargoMaximoDelNombre = 60`,
`HabitantesMinimos = 1`. El largo máximo lo aplica el mapeo de EF y el `maxlength` del campo.

La asimetría de `MismaLocalidad` es deliberada y está cubierta por una prueba unitaria propia
(«La provincia se compara de forma ordinal»): el nombre lo escribe la persona, la provincia sale de
un catálogo cerrado.

## ReglasDeEncuesta

`Dominio/Reglas/ReglasDeEncuesta.cs` — solo rangos; el orden de los pasos lo gobierna el servicio.

| Constante | Valor |
| --- | --- |
| `TotalDePasos` | 3 |
| `EdadMinima` / `EdadMaxima` | 16 / 110 |
| `DistanciaMinima` / `DistanciaMaxima` | 0 / 500 (km) |
| `MinutosMinimos` / `MinutosMaximos` | 1 / 600 |

`NombreValido` pide 3 caracteres recortados, igual que en localidades.

## Casos de uso

### ServicioDeLocalidades

`Aplicacion/Localidades/ServicioDeLocalidades.cs`. Recibe `IRepositorioDeLocalidades` por
constructor primario.

| Operación | Comportamiento |
| --- | --- |
| `ListarAsync` | Delega en el repositorio |
| `GuardarAsync` | 1) valida campo por campo; 2) si hay errores, corta; 3) busca duplicada con `MismaLocalidad` excluyendo el propio `Id`; 4) actualiza si `Id` tiene valor, si no da de alta |
| `EliminarAsync` | Si la localidad ya no existe devuelve «La localidad ya no existe.» en el campo `nombre` |

`GuardarAsync` recorta el nombre y el código postal antes de persistir. Los mensajes de alta y
modificación nombran la localidad («Se agregó la localidad X.»), lo que las E2E aprovechan para
distinguir una operación de la otra.

`ModeloDeLocalidad` lleva `Habitantes` como `int?` **a propósito**: «vacío» y «cero» son dos errores
distintos. `EsEdicion` es `Id is not null` y `Limpiar()` devuelve el formulario al estado de alta.

### ServicioDeEncuestas

`Aplicacion/Encuestas/ServicioDeEncuestas.cs`. Validación **por paso**: el asistente no deja avanzar
mientras el paso actual tenga errores.

| Paso | Campos validados | Claves de error |
| --- | --- | --- |
| 1 | Nombre (≥3), edad (16–110), localidad elegida | `nombre`, `edad`, `localidad` |
| 2 | Al menos un medio, frecuencia elegida | `medios`, `frecuencia` |
| 3 | Distancia (0–500), minutos (1–600), motivo elegido | `distancia`, `minutos`, `motivo` |

`RegistrarAsync` persiste la respuesta y la devuelve ya construida. Detalle con consecuencia
verificable: los medios se guardan **en el orden del catálogo y no en el de tipeo**, para que el
resumen sea estable y la prueba pueda compararlo con un texto fijo.

`ModeloDeEncuesta` acumula los tres pasos; `Medios` es un `HashSet<string>` con `AlternarMedio`.

## Cobertura de estas reglas

Las 49 pruebas de `tests/MovilidadUrbana.UnitTests/` verifican **solo** este índice: bordes de cada
validación del ABM (25 casos) y rangos de la encuesta paso por paso (24 casos), sin navegador ni
servidor. Ver [05_Pruebas.md](05_Pruebas.md).
