# 02 — Dominio y reglas de negocio

> **Propósito**: registrar qué se modela, qué valida cada regla y con qué límites, para poder
> razonar sobre el comportamiento esperado sin abrir el código.
> **Fuente primaria**: `src/MovilidadUrbana.Dominio/` y `src/MovilidadUrbana.Aplicacion/`.
> **Vigencia**: 2026-09-12, commit `88e5caa`.

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
| `Medios` | `colectivo` (Colectivo), `auto` (Auto particular), `bicicleta`, `moto`, `caminata` (A pie), `tren` |
| `Frecuencias` | `diaria` (Todos los días), `semanal` (Algunos días por semana), `ocasional` (Ocasionalmente) |
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
`HabitantesMinimos = 1` y `DigitosDelCodigoPostal = 4` —el patrón `^\d{4}$` la espeja—. El largo
máximo lo aplica el mapeo de EF y el `maxlength` del campo.

La asimetría de `MismaLocalidad` es deliberada y está cubierta por una prueba unitaria propia
(«La provincia se compara de forma ordinal»): el nombre lo escribe la persona, la provincia sale de
un catálogo cerrado.

## ReglasDeEncuesta

`Dominio/Reglas/ReglasDeEncuesta.cs` — solo rangos; el orden de los pasos lo gobierna el servicio.

| Constante | Valor |
| --- | --- |
| `TotalDePasos` | 3 |
| `LargoMinimoDelNombre` / `LargoMaximoDelNombre` | 3 / 80 |
| `EdadMinima` / `EdadMaxima` | 16 / 110 |
| `DistanciaMinima` / `DistanciaMaxima` | 0 / 500 (km, `double`) |
| `MinutosMinimos` / `MinutosMaximos` | 1 / 600 |

`NombreValido` pide `LargoMinimoDelNombre` (3) caracteres recortados, igual que en localidades.

## Casos de uso

### ServicioDeLocalidades

`Aplicacion/Localidades/ServicioDeLocalidades.cs`. Recibe `IRepositorioDeLocalidades` por
constructor primario.

| Operación | Comportamiento |
| --- | --- |
| `ListarAsync` | Delega en el repositorio |
| `GuardarAsync` | 1) valida campo por campo; 2) si hay errores, corta; 3) busca duplicada con `MismaLocalidad` excluyendo el propio `Id` («Ya existe una localidad con ese nombre en la provincia.», en `nombre`); 4) actualiza si `Id` tiene valor, si no da de alta |
| `EliminarAsync` | Si la localidad ya no existe devuelve «La localidad ya no existe.» en el campo `nombre` |

`GuardarAsync` recorta el nombre y el código postal antes de persistir. Los mensajes de alta,
modificación y baja nombran la localidad («Se agregó / Se actualizó / Se eliminó la localidad X.»),
lo que las E2E aprovechan para distinguir una operación de la otra.

Mensajes de error por campo: `nombre` («El nombre debe tener al menos 3 caracteres.»), `provincia`
(«Seleccione una provincia.»), `codigoPostal` («El código postal debe tener 4 dígitos.»),
`habitantes` («Ingrese una cantidad de habitantes mayor a cero.»). Los números se interpolan desde
las constantes de la regla.

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

`ModeloDeEncuesta` acumula los tres pasos; `Medios` es un `HashSet<string>` con `AlternarMedio`;
`Edad` y `Minutos` son `int?`.

## Políticas: el requisito antes del intento

Desde el 2026-09-04, `Aplicacion/Localidades/PoliticaDeLocalidades.cs` y
`Aplicacion/Encuestas/PoliticaDeEncuestas.cs` derivan de las constantes de `Dominio/Reglas/` el texto
de requisito que cada campo muestra **antes** del intento. Los límites que estaban escritos a mano en
la vista y en los mensajes —60 caracteres, 4 dígitos, 3 caracteres— pasaron a constantes de las
reglas. Los errores los sigue decidiendo el servicio de aplicación.

`Aplicacion/Encuestas/ResumenDeEncuesta.cs` arma las filas clave/valor que la superficie recorre al
registrar una respuesta, en vez de escribirlas a mano en la vista.

Fuente: `CHANGELOG.md` (2026-09-04) y la sección «Diseño» de `README.md`.

## Cobertura de estas reglas

Las 49 pruebas de `tests/MovilidadUrbana.UnitTests/` verifican **solo** este índice: bordes de cada
validación del ABM (`ReglasDeLocalidadTests`, 25 casos: 23 `[TestCase]` + 2 `[Test]`) y rangos de la
encuesta paso por paso (`ReglasDeEncuestaTests`, 24 casos: 23 + 1), sin navegador ni servidor. Ver
[05_Pruebas.md](05_Pruebas.md).
