# 02 — Dominio y reglas de Movilidad Urbana

> **Propósito**: destilar el dominio de Movilidad Urbana —entidades, catálogos, reglas, políticas
> (requisitos que ve la persona), mensajes de error y casos de uso— tal como lo comparten las tres
> aplicaciones (web, API y Android), con los huecos de validación que el código deja abiertos.
>
> **Fuente primaria**: `src/MovilidadUrbana.Web/Domain/` (`Catalogos.cs`, `Entities/*.cs`,
> `Rules/*.cs`), `src/MovilidadUrbana.Web/Application/` (`Result.cs`, `Encuestas/*.cs`,
> `Localidades/*.cs`, `Abstractions/*.cs`), sus copias en `src/MovilidadUrbana.ApiWeb/` y
> `src/MovilidadUrbana.MAUI/`, `src/MovilidadUrbana.Web/Infrastructure/Persistence/SessionSeeder.cs`,
> `tests/MovilidadUrbana.UnitTests/*.cs`, `README.md`, `CHANGELOG.md`.
>
> **Vigencia**: versión 3.1, generada el 2026-10-25 sobre el commit `8fb4c3a` (2026-09-18).
>
> **Vecinos**: cómo se reparten las capas y se componen → [01](01_Arquitectura.md); sesión,
> base, siembra y repositorios → [03](03_Sesiones-Y-Persistencia.md); cómo la web muestra estas
> reglas → [04](04_Interfaz-Y-Pantallas.md); rutas y `ValidationProblemDetails` de la API →
> [12](12_Api-REST.md); ViewModels de Android → [13](13_App-Android.md); suites y conteos →
> [05](05_Pruebas.md); por qué está hecho así → [08](08_Decisiones-Y-Trampas.md); términos →
> [09](09_Glosario.md).

---

## 1. Un solo dominio, tres copias idénticas

El dominio y la aplicación **no son una biblioteca compartida**: cada app trae su copia
(`README.md`, «tres proyectos independientes»). Se verificó con `diff` (normalizando el espacio de
nombres) que los 18 archivos de `Domain/` (6) + `Application/` (12) de la web, la API y MAUI son
**idénticos salvo el namespace** (`MovilidadUrbana.Web.*`, `MovilidadUrbana.ApiWeb.*`,
`MovilidadUrbana.MAUI.*`), y que ninguna copia tiene archivos extra.

```
Domain/                         (sin dependencias)
├── Catalogos.cs                Provincias, Medios, Frecuencias, Motivos + EtiquetaDe*()
├── Entities/
│   ├── Localidad.cs
│   ├── RespuestaDeEncuesta.cs
│   └── Session.cs              marca de "sesión ya sembrada"
└── Rules/
    ├── LocalidadRules.cs       límites y predicados del ABM
    └── EncuestaRules.cs        rangos y predicados de la encuesta
Application/
├── Result.cs                   resultado de caso de uso (éxito, mensaje, errores por campo)
├── DependencyInjection.cs      AddApplication(): LocalidadService + EncuestaService (scoped)
├── Abstractions/               ILocalidadRepository, IEncuestaRepository, ISessionContext
├── Localidades/                LocalidadModel, LocalidadPolicy, LocalidadService
└── Encuestas/                  EncuestaModel, EncuestaPolicy, EncuestaService, ResumenDeEncuesta
```

Consecuencia: un cambio de regla hay que replicarlo **tres veces**. Las pruebas unitarias
(`tests/MovilidadUrbana.UnitTests`) referencian solo la copia de la web
(`MovilidadUrbana.UnitTests.csproj` → `MovilidadUrbana.Web.csproj`); la copia de MAUI se ejercita
por `MovilidadUrbana.MAUI.Tests` y la de la API por `MovilidadUrbana.ApiWeb.Tests` (ver
[05](05_Pruebas.md)).

---

## 2. Entidades

| Entidad | Campos | Notas | Fuente |
| --- | --- | --- | --- |
| `Localidad` | `Id:int`, `SessionId:string`, `Nombre`, `Provincia`, `CodigoPostal:string`, `Habitantes:int` | `SessionId` aísla los datos por visitante | `Domain/Entities/Localidad.cs` |
| `RespuestaDeEncuesta` | `Id`, `SessionId`, `Nombre`, `Edad:int`, `Localidad:string`, `Medios:IReadOnlyList<string>`, `Frecuencia`, `Distancia:double`, `Minutos:int`, `Motivo`, `RegistradaEn:DateTimeOffset` | `Localidad` es el **nombre**, no una clave foránea; `Medios` se persiste como texto separado por comas | `Domain/Entities/RespuestaDeEncuesta.cs` |
| `Session` | `Id:string`, `CreatedAt:DateTimeOffset` | Marca que la sesión ya recibió su siembra; sin ella, borrar todo volvería a sembrar | `Domain/Entities/Session.cs` |

Relación entre entidades (no hay navegación EF ni FK):

```
Session.Id ──(mismo valor)── Localidad.SessionId
           └─(mismo valor)── RespuestaDeEncuesta.SessionId
RespuestaDeEncuesta.Localidad  ≈  Localidad.Nombre   (copia del texto al registrar)
```

Por eso la baja de una localidad **no arrastra dependientes**: «las respuestas de encuesta guardan
el nombre de la localidad y no su clave» (`Components/Pages/Localidades.razor.cs`,
`ConfirmDeleteAsync`; `README.md`, «Lo que no aplica, declarado»).

Los límites de largo del esquema (`HasMaxLength`) y la siembra inicial por sesión (Corrientes y
Resistencia, de las que dependen las pruebas) son de persistencia: [03](03_Sesiones-Y-Persistencia.md)
§8 y §10.

---

## 3. Catálogos (`Domain/Catalogos.cs`)

| Catálogo | Valores (clave → etiqueta) | Lo usa |
| --- | --- | --- |
| `Provincias` | Buenos Aires, Chaco, Córdoba, Corrientes, Entre Ríos, Mendoza, Santa Fe (7, sin clave aparte) | `<select>` de alta y filtro del ABM; MAUI (`LocalidadEditorViewModel`, `LocalidadesViewModel`) |
| `Medios` | `colectivo`→Colectivo · `auto`→Auto particular · `bicicleta`→Bicicleta · `moto`→Moto · `caminata`→A pie · `tren`→Tren (6) | Casillas del paso 2; orden canónico al registrar |
| `Frecuencias` | `diaria`→Todos los días · `semanal`→Algunos días por semana · `ocasional`→Ocasionalmente (3) | `<select>` del paso 2 |
| `Motivos` | `trabajo`→Trabajo · `estudio`→Estudio · `salud`→Salud · `otros`→Otros (4) | `<select>` del paso 3 |

`EtiquetaDeMedio/Frecuencia/Motivo(clave)` devuelven la etiqueta o, si la clave no está en el
catálogo, **la clave cruda** (`FirstOrDefault(...).Etiqueta ?? clave`).

Lo que persiste es la **clave**; lo que se muestra (resumen) es la **etiqueta**.

---

## 4. Reglas (`Domain/Rules/`)

### 4.1 `LocalidadRules`

| Constante | Valor | Predicado | Qué acepta |
| --- | --- | --- | --- |
| `LargoMinimoDelNombre` | 3 | `NombreValido(n)` | `Trim().Length >= 3`; `null` → falso |
| `LargoMaximoDelNombre` | 60 | — | **No lo valida ninguna regla** (ver §8) |
| — | — | `ProvinciaValida(p)` | `!IsNullOrWhiteSpace(p)` — cualquier texto no vacío |
| `DigitosDelCodigoPostal` | 4 | `CodigoPostalValido(cp)` | regex `^\d{4}$` sobre `Trim()` |
| `HabitantesMinimos` | 1 | `HabitantesValidos(h)` | `h is not null && h >= 1`; sin máximo |
| — | — | `MismaLocalidad(nA, pA, nB, pB)` | nombre: `Trim()` + `OrdinalIgnoreCase`; provincia: `Ordinal` (distingue mayúsculas) |

### 4.2 `EncuestaRules`

| Constante | Valor | Predicado | Qué acepta |
| --- | --- | --- | --- |
| `TotalDePasos` | 3 | — | Número de pasos del asistente (web, API, MAUI) |
| `LargoMinimoDelNombre` / `LargoMaximoDelNombre` | 3 / 80 | `NombreValido(n)` | `Trim().Length >= 3`; el máximo **no** se valida |
| `EdadMinima` / `EdadMaxima` | 16 / 110 | `EdadValida(e)` | `e is >= 16 and <= 110`, ambos bordes incluidos |
| `DistanciaMinima` / `DistanciaMaxima` | 0 / 500 (km, `double`) | `DistanciaValida(d)` | `0 <= d <= 500`; **0 es válido** («se puede no viajar») |
| `MinutosMinimos` / `MinutosMaximos` | 1 / 600 | `MinutosValidos(m)` | `1 <= m <= 600`; **0 no es válido** |

Cobertura unitaria (contada en `tests/MovilidadUrbana.UnitTests/`): `LocalidadRulesTests` 25 casos
(Nombre 6, Provincia 4, CP 8, Habitantes 5, `MismaLocalidad` 2) y `EncuestaRulesTests` 24 (Nombre 5,
Edad 6, Distancia 6, Minutos 6, `TotalDePasos` 1) = **49**, igual que declara `README.md`.
`LargoMaximoDelNombre` y `DigitosDelCodigoPostal` no tienen caso propio.

---

## 5. Políticas: el requisito que se muestra antes del intento

Las `*Policy` enuncian la regla **para la persona**, derivada de las constantes de `*Rules`, para
que la vista no transcriba límites (`Application/Localidades/LocalidadPolicy.cs`,
`Application/Encuestas/EncuestaPolicy.cs`). La web las muestra bajo cada campo
(ver [04](04_Interfaz-Y-Pantallas.md)).

| Política | Propiedad | Texto resultante | ¿Lo garantiza la regla? |
| --- | --- | --- | --- |
| `LocalidadPolicy` | `RequisitoDelNombre` | «Entre 3 y 60 caracteres, único por provincia.» | 3 y unicidad sí; 60 solo por `maxlength` de la web (MAUI corta en 80, ver H2) |
| | `RequisitoDeLaProvincia` | «Una de las provincias del catálogo.» | **No**: la regla acepta cualquier texto no vacío |
| | `RequisitoDelCodigoPostal` | «4 dígitos.» | Sí |
| | `RequisitoDeLosHabitantes` | «Un número entero de 1 en adelante.» | Sí |
| `EncuestaPolicy` | `RequisitoDelNombre` | «Al menos 3 caracteres.» | Sí |
| | `RequisitoDeLaEdad` | «Entre 16 y 110 años.» | Sí |
| | `RequisitoDeLaLocalidad` | «Una de las localidades cargadas en el ABM.» | **No**: solo se exige no vacío |
| | `RequisitoDeLosMedios` | «Al menos uno.» | Parcial (ver §8) |
| | `RequisitoDeLaFrecuencia` | «Con qué asiduidad usa esos medios.» | Solo no vacío |
| | `RequisitoDeLaDistancia` | «Entre 0 y 500 km por día.» | Sí |
| | `RequisitoDeLosMinutos` | «Entre 1 y 600 minutos.» | Sí |
| | `RequisitoDelMotivo` | «El motivo principal del viaje.» | Solo no vacío |

---

## 6. Casos de uso

### 6.1 `LocalidadService` (`Application/Localidades/LocalidadService.cs`)

| Operación | Flujo | Resultado |
| --- | --- | --- |
| `GetAllAsync()` | Delegado al repositorio (filtra por sesión, siembra si hace falta, orden por `Id`) | `IReadOnlyList<Localidad>` |
| `SaveAsync(LocalidadModel)` | 1) `Validate` por campo → 2) duplicado (`MismaLocalidad` contra todas las de la sesión, excluyendo `model.Id`) → 3) si `Id` → actualizar, si no → alta. Recorta `Nombre` y `CodigoPostal`; `Provincia` va tal cual | `Result` |
| `DeleteAsync(id)` | Busca; si no está → inválido; si está → borra | `Result` |

`LocalidadModel` (lo que edita la pantalla): `Id:int?` (`IsEdit => Id is not null`), `Nombre`,
`Provincia`, `CodigoPostal` (texto), `Habitantes:int?` —anulable «para distinguir vacío de cero»—;
`Clear()` lo vuelve a modo alta.

```
SaveAsync(model)
  ├─ errores de campo? ──sí──► Result.Invalid(errores)             (no toca la base)
  ├─ duplicada?        ──sí──► Invalid("nombre", "Ya existe…")
  ├─ model.Id != null
  │    ├─ no existe    ──────► Invalid("nombre", "La localidad ya no existe.")
  │    └─ UpdateAsync  ──────► Success("Se actualizó la localidad {nombre}.")
  └─ AddAsync          ──────► Success("Se agregó la localidad {nombre}.")
```

### 6.2 `EncuestaService` (`Application/Encuestas/EncuestaService.cs`)

| Operación | Qué hace |
| --- | --- |
| `CountAsync()` | Encuestas registradas **por la sesión actual** |
| `ValidarPaso(paso, model)` | Devuelve `IReadOnlyDictionary<campo, mensaje>` solo con las reglas de ese paso; `paso` fuera de 1–3 → diccionario vacío |
| `RegistrarAsync(model)` | **No valida**: arma la `RespuestaDeEncuesta` (`Nombre.Trim()`, `Edad!.Value`, `Distancia!.Value`, `Minutos!.Value`, `RegistradaEn = UtcNow`, medios en orden del catálogo), la persiste y la devuelve. Quien llama debe haber validado los tres pasos |

Reparto de campos por paso (`EncuestaModel.cs`):

| Paso | Rótulo (web/MAUI) | Campos | Claves de error |
| --- | --- | --- | --- |
| 1 | Datos de la persona | `Nombre`, `Edad:int?`, `Localidad` | `nombre`, `edad`, `localidad` |
| 2 | Medios que utiliza para viajar | `Medios:HashSet<string>` (`AlternarMedio(clave, elegido)`), `Frecuencia` | `medios`, `frecuencia` |
| 3 | Distancia recorrida | `Distancia:double?`, `Minutos:int?`, `Motivo` | `distancia`, `minutos`, `motivo` |

Quién valida antes de registrar:

| App | Cómo | Fuente |
| --- | --- | --- |
| Web | `FinishAsync` valida **solo el paso vigente (3)**; los pasos 1 y 2 quedaron validados al avanzar | `Components/Pages/Encuesta.razor.cs` |
| API | `POST /api/v1/encuestas` valida los **tres** pasos y responde 400 con todos los errores | `Controllers/EncuestasController.cs` |
| MAUI | Ver [13](13_App-Android.md) | `Presentation/Encuestas/EncuestaViewModel.cs` |

### 6.3 `ResumenDeEncuesta.De(respuesta)` — la ficha de revisión

Lista de `CampoDeResumen(Clave, Etiqueta, Valor)` ya formateada; la vista la recorre y no formatea
(`Application/Encuestas/ResumenDeEncuesta.cs`). La API la devuelve como `Resumen` del 201.

| Clave | Etiqueta | Valor | Ejemplo (prueba E2E, es-AR) |
| --- | --- | --- | --- |
| `persona` | Persona | `"{Nombre} ({Edad} años)"` | Ana Pérez (34 años) |
| `localidad` | Localidad | `Localidad` | Corrientes |
| `medios` | Medios | etiquetas unidas por `", "` en orden del catálogo | Colectivo, Bicicleta |
| `frecuencia` | Frecuencia | etiqueta | Todos los días |
| `distancia` | Distancia diaria | `"{Distancia:0.###} km"` (cultura del hilo) | 12,5 km |
| `minutos` | Tiempo de viaje | `"{Minutos} min"` | 45 min |
| `motivo` | Motivo | etiqueta | Trabajo |

Los ejemplos salen de `RecorreLosTresPasosMuestraElResumenYRegistraLaRespuesta`
(`tests/MovilidadUrbana.E2ETests/EncuestaTests.cs`). La coma decimal depende de que la app fije
`es-AR` (`src/MovilidadUrbana.Web/Program.cs`).

---

## 7. Catálogo de mensajes

### 7.1 `Result` (`Application/Result.cs`)

`Result(IsSuccess, Message, Errors)`. `Success(mensaje)` sin errores; `Invalid(errores)` lleva
siempre el mensaje general **«Revise los campos marcados en rojo.»**; `Invalid(campo, mensaje)`
es atajo de un solo error. Las claves de `Errors` son los nombres de campo que la pantalla conoce.

### 7.2 ABM de localidades

| Clave | Disparador | Mensaje exacto |
| --- | --- | --- |
| `nombre` | `NombreValido` falso | El nombre debe tener al menos 3 caracteres. |
| `provincia` | `ProvinciaValida` falso | Seleccione una provincia. |
| `codigoPostal` | `CodigoPostalValido` falso | El código postal debe tener 4 dígitos. |
| `habitantes` | `HabitantesValidos` falso | Ingrese una cantidad de habitantes mayor a cero. |
| `nombre` | Duplicado en la provincia | Ya existe una localidad con ese nombre en la provincia. |
| `nombre` | Editar o borrar un `Id` que no está en la sesión | La localidad ya no existe. |
| (éxito) | Alta / modificación / baja | Se agregó la localidad {nombre}. · Se actualizó la localidad {nombre}. · Se eliminó la localidad {nombre}. |

La validación de campos ocurre toda junta (se ven los cuatro errores a la vez); el duplicado solo
se evalúa si los campos pasaron.

### 7.3 Encuesta

| Paso | Clave | Mensaje exacto |
| --- | --- | --- |
| 1 | `nombre` | Ingrese nombre y apellido (mínimo 3 caracteres). |
| 1 | `edad` | La edad debe estar entre 16 y 110 años. |
| 1 | `localidad` | Seleccione una localidad. |
| 2 | `medios` | Seleccione al menos un medio de transporte. |
| 2 | `frecuencia` | Seleccione la frecuencia de uso. |
| 3 | `distancia` | Ingrese una distancia entre 0 y 500 km. |
| 3 | `minutos` | Ingrese un tiempo entre 1 y 600 minutos. |
| 3 | `motivo` | Seleccione el motivo principal del viaje. |

Avisos de superficie (no son del servicio): «Complete los datos del paso antes de continuar.»
(web `Encuesta.razor.cs`; MAUI `EncuestaViewModel.IncompleteStepNotice`) y «No pudimos registrar la
encuesta. Volvé a intentar en unos segundos.» (ambas). La API usa otro título para el 400: «La
solicitud tiene datos inválidos.» (`Controllers/ValidationProblems.cs`, ver [12](12_Api-REST.md)).

Mismos mensajes en las tres apps: el texto sale del servicio de aplicación, que es idéntico
(§1; `README.md`, tabla de MAUI: «los mensajes de error son los mismos que en la web y la API»).

---

## 8. Huecos de validación (leídos en el código, sin prueba que los cubra)

Salvo H7 (que tiene caso unitario), ninguno de estos puntos tiene caso de prueba en las siete
suites (búsqueda por las claves y valores en `tests/`). Se derivan de leer las reglas; **no se
ejecutaron**.

| # | Hueco | Efecto esperable | Dónde se ve |
| --- | --- | --- | --- |
| H1 | `ProvinciaValida` solo exige no vacío | Por la API (`LocalidadRequest.Provincia`) se puede dar de alta una provincia fuera del catálogo; la web no lo permite porque es un `<select>` | `LocalidadRules.cs`; contradice `LocalidadPolicy.RequisitoDeLaProvincia` |
| H2 | `LargoMaximoDelNombre` (60 / 80) no está en ninguna regla | La web lo frena con `maxlength` (`Localidades.razor:49`, `Encuesta.razor:40`); la API no lo valida; MAUI pone `MaxLength="80"` también al nombre de la **localidad** (`Pages/LocalidadEditorPage.xaml:22`), no 60. El `HasMaxLength` de EF sobre SQLite no impone el largo (comportamiento conocido de SQLite, **no verificado en este repo**) | `LocalidadRules.cs`, `EncuestaRules.cs`, `AppDbContext.cs` |
| H3 | La localidad de la encuesta solo exige no vacío | Por la API se registra una encuesta con una localidad inexistente | `EncuestaService.ValidarPaso` caso 1; contradice `RequisitoDeLaLocalidad` |
| H4 | `medios` se valida por cantidad, no contra el catálogo, y `RegistrarAsync` descarta las claves desconocidas | Por la API, `Medios: ["avion"]` pasa la validación y se registra con **lista vacía** | `ValidarPaso` caso 2 vs. `RegistrarAsync` |
| H5 | `Frecuencia` y `Motivo` solo exigen no vacío | Una clave desconocida se guarda y el resumen la muestra cruda (fallback de `EtiquetaDe*`) | `ValidarPaso`; `Catalogos.EtiquetaDe*` |
| H6 | `RegistrarAsync` no valida y usa `!.Value` | Llamarlo sin validar antes lanza `InvalidOperationException` por nulos; las tres apps validan antes | `EncuestaService.cs` |
| H7 | Comparación de provincia `Ordinal` en `MismaLocalidad` | «Goya/corrientes» y «Goya/Corrientes» no son duplicado (cubierto por `LaProvinciaSeComparaDeFormaOrdinal`); combinado con H1, la API admite variantes de mayúsculas | `LocalidadRules.cs`; `LocalidadRulesTests.cs` |

---

## 9. Rastros de nombres previos al renombre

El renombre `946d023` (y `e9dea2a` para los `cref`) pasó la arquitectura al inglés y dejó el
dominio en español (`CHANGELOG.md`, 2026-09-18). Los rastros de las capas de dominio
(`SesionId` en `Localidad.cs`, tabla `Sesiones` en `SessionSeeder.cs`, `ObtenerAsync` en
`LocalidadRepository.cs`, ×3 apps; `Domain/Reglas` en el `README.md`) están inventariados en
[01](01_Arquitectura.md) §8.3; el comentario de prueba sobre la «barra de progreso», en
[05](05_Pruebas.md) §13. Lo propio de este índice:

| Rastro | Dónde | Nombre vigente |
| --- | --- | --- |
| `ReglasDeLocalidad`, `ReglasDeEncuesta`, `PoliticaDeLocalidades`, `PoliticaDeEncuestas`, `Dominio/Reglas` | `CHANGELOG.md` (entradas 2026-08-30 y 2026-09-04) | `LocalidadRules`, `EncuestaRules`, `LocalidadPolicy`, `EncuestaPolicy` — historia, correcto que quede |

En la API, el rastro de `Localidad.cs` llega además al XML de
documentación del ensamblado (`GenerateDocumentationFile` en `MovilidadUrbana.ApiWeb.csproj`); la
entidad no se expone como DTO, así que no se verificó que aparezca en el documento OpenAPI
(ver [12](12_Api-REST.md)).
