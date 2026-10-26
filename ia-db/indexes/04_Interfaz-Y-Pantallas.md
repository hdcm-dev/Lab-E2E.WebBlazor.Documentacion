# 04 — Interfaz y pantallas de la web de Movilidad Urbana

> **Propósito**: describir cada pantalla de `MovilidadUrbana.Web` —rutas, anatomía, comportamiento,
> estados, textos y anuncios— y el inventario completo de `data-testid`, marcando cuáles usa la
> suite E2E y cuáles no usa ninguna prueba.
>
> **Fuente primaria**: `src/MovilidadUrbana.Web/Components/App.razor`, `Components/Routes.razor`,
> `Components/Layout/MainLayout.razor`, `Components/Pages/*.razor(.cs)`, `Components/Shared/*`,
> `Services/*.cs`, `wwwroot/js/*.js`, `wwwroot/css/Componentes.css` (punto de quiebre),
> `Program.cs`; `tests/MovilidadUrbana.E2ETests/*.cs`; `README.md` (sección «Diseño»);
> `CHANGELOG.md` (2026-09-04).
>
> **Vigencia**: versión 3.1, generada el 2026-10-25 sobre el commit `8fb4c3a` (2026-09-18).
>
> **Vecinos**: cómo están construidos tokens, componentes, `SurfaceState` y shells →
> [11](11_Template-Y-Superficies.md); las reglas y mensajes que estas pantallas muestran →
> [02](02_Dominio-Y-Reglas.md); cookie de sesión y puente `App.razor → Routes` →
> [03](03_Sesiones-Y-Persistencia.md); casos E2E, fixture y variables → [05](05_Pruebas.md);
> pantallas de Hola Mundo y Login → [10](10_Hola-Mundo-Y-Login.md); pantallas de Android y
> `AutomationId` → [13](13_App-Android.md); trampas (hidratación, `oninput`) →
> [08](08_Decisiones-Y-Trampas.md).

---

## 1. Mapa de rutas

| Ruta | Componente | `<PageTitle>` | `h1` (`data-testid="titulo"`) | Prueba E2E |
| --- | --- | --- | --- | --- |
| `/` | `Pages/Home.razor` | Movilidad Urbana — Inicio | Demostración de pruebas E2E | `NavigationTests` (2 de sus 4 casos) |
| `/localidades` | `Pages/Localidades.razor` (+ `.razor.cs`) | Movilidad Urbana — Localidades | Localidades | `LocalidadesTests` (9) + `NavigationTests.ElMenuMarcaLaPaginaActiva` y `DesdeLaPortadaSeLlegaAlAbmYALaEncuesta` |
| `/encuesta`, `/encuesta/{Paso:int}` | `Pages/Encuesta.razor` (+ `.razor.cs`) | Movilidad Urbana — Encuesta | Encuesta de uso del transporte | `EncuestaTests` (9) + `NavigationTests.DesdeLaPortadaSeLlegaAlAbmYALaEncuesta` (solo `/encuesta`) |
| `/no-encontrado` | `Pages/NotFound.razor` | Movilidad Urbana — No encontrado | No encontrado | `UnaDireccionInexistenteMuestraLaPantallaDeNoEncontrado` |
| `/Error` | `Pages/Error.razor` | Movilidad Urbana — Error | Error | ninguna |

- Toda ruta inexistente cae en `NotFound`: por el `Router` (`NotFoundPage="typeof(Pages.NotFound)"`,
  `Routes.razor`) y por `UseStatusCodePagesWithReExecute("/no-encontrado")` (`Program.cs`).
  `/encuesta/abc` no cumple `{Paso:int}`, así que también termina ahí (inferido de la restricción
  de ruta; sin prueba).
- `/Error` solo es el manejador de excepciones **fuera de Development**
  (`UseExceptionHandler("/Error")`, `Program.cs`). Muestra el identificador de la petición
  (`Activity.Current?.Id ?? HttpContext.TraceIdentifier`) y «Volver al inicio».
- Casos E2E contados: 4 + 9 + 9 = **22** (`[Test]` en `tests/MovilidadUrbana.E2ETests/*.cs`).

---

## 2. Shell de trabajo (todas las pantallas)

```
<body class="mq-body">                                   App.razor (render estático)
├─ a.mq-skip "Ir al contenido" → #mq-main
├─ <Routes @rendermode=InteractiveServer SessionId=…>    raíz interactiva (ver 03)
│   └─ MainLayout
│       ├─ div.mq-shell
│       │   ├─ Sidebar  nav[aria-label="Navegación principal"]
│       │   │   ├─ a.mq-identidad  "Movilidad Urbana"          testid marca
│       │   │   └─ Inicio · Localidades · Encuesta             testid nav-inicio / nav-localidades / nav-encuesta
│       │   └─ div.mq-shell-contenido
│       │       ├─ main#mq-main[tabindex=-1]  ← @Body
│       │       └─ VersionStamp "Movilidad Urbana — {versión}"  testid sello-version
│       ├─ DialogHost                 (único, monta Dialog cuando hay confirmación pendiente)
│       ├─ ReconnectionNotice         (#components-reconnect-modal, banda role=status)
│       ├─ div[hidden] testid estado-app  data-interactivo="false|true"
│       └─ #blazor-error-ui  "Se produjo un error inesperado…" + "Recargar la pantalla"
└─ scripts: mq-dialogo.js, mq-foco.js, blazor.web.js
```

| Pieza | Comportamiento | Fuente |
| --- | --- | --- |
| Ítem activo | `aria-current="page"` + clase `mq-nav-item--activo` si la ruta relativa (sin query, sin `/`) coincide (`OrdinalIgnoreCase`); se recalcula en `LocationChanged`. Como compara la ruta entera, en `/encuesta/2` y `/encuesta/3` el ítem «Encuesta» queda sin marcar (lectura de código; sin prueba) | `Shared/Sidebar.razor` |
| Foco al navegar | `FocusOnNavigate Selector="#mq-main"` | `Routes.razor` |
| Testigo de hidratación | `data-interactivo` = `RendererInfo.IsInteractive`; `false` en el prerender, `true` con el circuito conectado. Toda prueba lo espera antes del primer click (`WaitForInteractiveAsync`) | `Layout/MainLayout.razor`, `tests/…/Infrastructure/E2ETestBase.cs` |
| Sello de versión | `DisplayVersion` desde `AssemblyInformationalVersion` (sin `+metadatos`); insignia «preliminar» si hay `-`; «origen indeterminado» si no hay `+`; «versión no declarada» si falta el atributo | `Shared/VersionStamp.razor`, `Services/VersionIdentity.cs` |
| Aviso de reconexión | Estados `reconectando`, `reintentando` (cuenta segundos), `fallo` (botón «Reintentar la conexión»), `pausada` y `fallo-al-retomar` (botón «Retomar la sesión»); `rejected` → `location.reload()`; tras `failed` reintenta al volver a la pestaña. No es modal | `Shared/ReconnectionNotice.razor(.js/.css)` |
| Punto de quiebre | Único, `@media (max-width: 768px)`: el shell pasa a una columna, la barra lateral a navegación superior (sin menú desplegable), el ABM a una columna, la tabla se oculta y aparecen las tarjetas apiladas | `wwwroot/css/Componentes.css` |
| Cultura | `es-AR` fija para todo el proceso: miles con punto, decimales con coma | `Program.cs` |

---

## 3. Inicio (`/`)

- Encabezado + párrafo `mq-prosa` («Dos pantallas típicas de una aplicación de gestión…»).
- Dos tarjetas de acceso, **toda la tarjeta es el enlace**: `ir-localidades` → `localidades`
  («ABM de localidades») e `ir-encuesta` → `encuesta` («Encuesta de transporte»), con ícono
  `Icons.Localidad` / `Icons.Encuesta` a tamaño `IconRoles.Card` (20).

---

## 4. ABM de localidades (`/localidades`)

### 4.1 Anatomía (orden canónico de la superficie)

```
h1 Localidades · "Cada fila se edita en el panel de la izquierda."
p.mq-sr-only[role=status][aria-live=polite]          ← anuncios
Band (aviso)  tono Exito | Error                      ← resultado de la última acción
── si Indisponible ───────────────────────────────────────────────────────────────
UnavailableState "No pudimos traer las localidades" + "Reintentar traer las localidades"
── si no ─────────────────────────────── .mq-columnas-abm ──────────────────────────
┌ Panel formulario ─────────────────┐  ┌ Panel listado ─────────────────────────────┐
│ titulo-formulario                 │  │ "Listado" [contador] (de N si hay filtro)  │
│  "Alta de localidad" |            │  │ Buscar (campo-buscar) · Provincia (filtro) │
│  "Editar localidad"               │  │ Grid: Cargando→Skeleton | Vacio→sin-datos  │
│ Nombre · Provincia · CP · Hab.    │  │   | FiltradoSinResultados→sin-resultados   │
│ [Cancelar] [Guardar|Actualizar]   │  │   | ConDatos → tabla + tarjetas apiladas   │
└───────────────────────────────────┘  └────────────────────────────────────────────┘
```

### 4.2 Campos del formulario

| Campo | Control | Requisito (antes del intento) | Atributos | Fuente del requisito |
| --- | --- | --- | --- | --- |
| Nombre | `input text`, `autocomplete=off` | Entre 3 y 60 caracteres, único por provincia. | `maxlength=60` | `LocalidadPolicy` |
| Provincia | `select` con «Seleccione…» + 7 provincias | Una de las provincias del catálogo. | — | `LocalidadPolicy` |
| Código postal | `input text`, `inputmode=numeric`, `placeholder=3400`, `autocomplete=postal-code` | 4 dígitos. | — | `LocalidadPolicy` |
| Habitantes | `input number`, `min=1`, `step=1`, `@bind:event="oninput"` | Un número entero de 1 en adelante. | — | `LocalidadPolicy` |

Cada campo es un `FormField`: rótulo visible arriba, requisito `{id}-requisito`, error
`{id}-error`, ambos citados en `aria-describedby`; con error el control lleva
`mq-input--invalido` / `mq-select--invalido` (`Shared/FormField.razor`, `Shared/FieldContext.cs`).
Los textos de error son los del servicio ([02](02_Dominio-Y-Reglas.md) §7.2).

### 4.3 Comportamiento

| Acción | Qué pasa | Fuente |
| --- | --- | --- |
| Carga | `SurfaceState.Cargando` + anuncio «Cargando las localidades.» → `GetAllAsync` → filtro. Excepción → `Indisponible` (se loguea; la pantalla dice qué pasó) | `Localidades.razor.cs` `LoadAsync` |
| Guardar | Bandera `_busy` **antes** del `await` (evita doble envío); botón deshabilitado con spinner y «Guardando…». Inválido → banda Error con «Revise los campos marcados en rojo.» + errores por campo. Éxito → banda Éxito, formulario vuelve a alta, recarga la lista. Excepción → banda «No pudimos guardar la localidad. Volvé a intentar en unos segundos.» | `SaveAsync` |
| Editar (fila) | Copia la fila al modelo; título «Editar localidad», botón «Actualizar»; limpia errores y aviso | `Edit` |
| Cancelar | Vuelve a modo alta, sin errores ni aviso | `Cancel` |
| Eliminar (fila) | Diálogo de primer grado: título «Dar de baja la localidad {nombre}», aviso «La operación no se deshace. Las encuestas ya registradas conservan el nombre de la localidad.», acción «Dar de baja» (destructiva). Confirmar → si se estaba editando esa misma, el formulario vuelve a alta → `DeleteAsync` → banda con el mensaje → recarga. Excepción → «No pudimos dar de baja la localidad. Volvé a intentar en unos segundos.» | `ConfirmDeleteAsync`, `DeleteAsync` |
| Buscar | Por `oninput`; subcadena **sin distinguir mayúsculas** en `Nombre` **o** `CodigoPostal`, sobre lo ya traído (no consulta la base) | `ApplyFilter`, `OnSearch` |
| Filtro provincia | `select` «todas» + 7; igualdad exacta; `@bind:after="ApplyFilter"` | `ApplyFilter` |
| Estados del listado | `_all` vacío → `Vacio`; `_visible` vacío → `FiltradoSinResultados`; si no → `ConDatos` | `ApplyFilter` |
| «Cargar la primera localidad» | Botón del estado vacío: pone el foco en el campo Nombre | `FocusNameAsync` |
| «Limpiar el filtro» | Vacía búsqueda y provincia y recalcula | `ClearFilter` |
| Contador | `Badge` con `_visible.Count`; si hay filtro agrega «de {total}» | `Localidades.razor` |

Anuncios en la región viva: «Cargando las localidades.», «No pudimos traer las localidades.»,
«Todavía no hay localidades.», «Ninguna localidad coincide con el filtro.», «Se muestran {n}
localidades de {total}.» y el mensaje del `Result` cuando falla.

### 4.4 Grilla

| Columna | Encabezado | Celda | testid |
| --- | --- | --- | --- |
| Nombre (encabezado de fila, `th scope=row`) | Nombre | Iniciales (`aria-hidden`; 1 palabra → 1 letra, 2+ → 2) + nombre | `celda-nombre` |
| Provincia | Provincia | texto | `celda-provincia` |
| CP | CP | texto | `celda-codigo-postal` |
| Habitantes (`IsNumeric`, a la derecha) | Habitantes | `ToString("N0")` → «89.000» | `celda-habitantes` |
| Acciones | Operaciones | «Editar» (`aria-label="Editar la localidad {n}"`) · «Eliminar» (`aria-label="Eliminar la localidad {n}"`) | `boton-editar`, `boton-eliminar` |

- `caption` (solo lector): «Localidades cargadas, con su provincia, su código postal y sus
  habitantes». Cada `tr` lleva `data-testid="fila"` y `data-id="{Id}"`.
- **Tabla y tarjetas apiladas están siempre las dos en el marcado**; las conmuta el CSS. La tarjeta
  (`article role=listitem`, `data-testid="tarjeta"`) titula con la columna de encabezado y une el
  resto con « · ». Por eso las pruebas buscan la acción en la presentación **visible**
  (`[data-testid=fila], [data-testid=tarjeta]` + `Visible = true`, `LocalidadesTests.PresentacionDe`).
- Consecuencia para quien cuenta: `GetByTestId("fila")` cuenta filas de la tabla aunque esté oculta
  en móvil; la tarjeta no tiene `data-id`.

---

## 5. Encuesta (`/encuesta`, `/encuesta/{Paso}`)

### 5.1 Anatomía

```
h1 Encuesta de uso del transporte · "Tres pasos. Se puede volver atrás sin perder lo cargado."
   Badge contador-encuestas "Registradas: {n}"            (n = encuestas de la sesión)
p.mq-sr-only[role=status]                                 ← anuncios de la página
Band (aviso) tono Error                                   ← "Complete los datos…" / fallo al registrar
── sin respuesta ── Wizard (panel) ────────────────────────────────────────────────
  nav "Progreso del asistente": ol > li[data-paso=1..3].mq-paso--completado|actual|pendiente
       (aria-current="step" en el vigente; ✓ en completados)  · etiqueta-paso "Paso N de 3"
  EditForm formulario → WizardStep paso-N (solo se dibuja el vigente, con su h2)
  pie: [Anterior] … [Siguiente] | [Registrando… (boton-procesando)] | [✓ Registrar la encuesta]
── con respuesta ── estado de éxito (no es un cuarto paso) ───────────────────────────
  etiqueta-paso "Encuesta completada"
  section resumen: Band Exito mensaje-envio "Encuesta registrada. ¡Gracias por participar!"
                   dl.mq-kv con resumen-{clave} × 7          [Cargar otra encuesta] boton-reiniciar
```

### 5.2 Pasos y campos

| Paso (`h2`) | Campo | Control | Requisito | Atributos |
| --- | --- | --- | --- | --- |
| 1 Datos de la persona | Nombre y apellido | `input text`, `autocomplete=name` | Al menos 3 caracteres. | `maxlength=80` |
| | Edad | `input number` | Entre 16 y 110 años. | `min=16 max=110 step=1`, `oninput` |
| | Localidad | `select` «Seleccione…» + localidades **de la sesión** como «{Nombre} ({Provincia})», valor = `Nombre` | Una de las localidades cargadas en el ABM. | — |
| 2 Medios que utiliza para viajar | ¿Qué medios utiliza para viajar? | `fieldset` con 6 casillas `medio-{clave}`; el error es del grupo (el `fieldset` cita `medios-requisito` y, con error, también `medios-error` en `aria-describedby`) | Al menos uno. | — |
| | Frecuencia de uso | `select` «Seleccione…» + 3 | Con qué asiduidad usa esos medios. | — |
| 3 Distancia recorrida | Distancia diaria (km) | `input number` | Entre 0 y 500 km por día. | `min=0 max=500 step=0.1`, `oninput` |
| | Tiempo de viaje (minutos) | `input number` | Entre 1 y 600 minutos. | `min=1 max=600 step=1`, `oninput` |
| | Motivo principal | `select` «Seleccione…» + 4 | El motivo principal del viaje. | — |

Valores de catálogo y mensajes de error: [02](02_Dominio-Y-Reglas.md) §3 y §7.3.

### 5.3 Reglas de navegación del asistente (`Encuesta.razor.cs`)

| Situación | Comportamiento |
| --- | --- |
| Avanzar («Siguiente»; el `OnSubmit` del `EditForm` también llama a `AdvanceAsync`, pero que Enter lo dispare **no está verificado**: el formulario no tiene botón `submit`) | Valida **solo el paso vigente** con `EncuestaService.ValidarPaso`; con errores no avanza, muestra «Complete los datos del paso antes de continuar.» (banda + anuncio) |
| Retroceder (Anterior) | **Nunca valida**; conserva lo cargado. «Anterior» deshabilitado en el paso 1 |
| Cambiar de paso | Limpia aviso y errores; actualiza `_pasoMaximoAlcanzado`; anuncia «Paso N de 3: {rótulo}»; `NavigateTo(/encuesta[/N], replace: true)` (no ensucia el historial); foco a `#mq-main` por `IFocusService` |
| Paso por dirección | `Clamp(Paso ?? 1, 1, 3)` y luego `Min(pedido, _pasoMaximoAlcanzado)`: **no se puede saltear** pasos entrando por URL. Al cargar `/encuesta/3` en frío se muestra el paso 1 y la URL no se corrige (lectura de código; sin prueba) |
| Último paso | «Siguiente» se reemplaza por «Registrar la encuesta» (`boton-finalizar`); mientras viaja, por un botón **distinto** y deshabilitado «Registrando…» (`boton-procesando`) |
| Registrar | Guarda contra doble click con `_busy`; valida el paso 3; `RegistrarAsync`; recalcula el contador; anuncia «Encuesta registrada.». Excepción → banda «No pudimos registrar la encuesta. Volvé a intentar en unos segundos.» |
| Cargar otra encuesta | Modelo nuevo, paso 1, máximo alcanzado 1, vuelve a `/encuesta`; el contador **no** se reinicia |

El desplegable de localidades y el contador se leen una vez en `OnInitializedAsync`: el ABM y la
encuesta comparten almacén por sesión ([03](03_Sesiones-Y-Persistencia.md)).

---

## 6. Diálogo de confirmación (montado por el shell)

`IDialogService.ConfirmAsync(ConfirmationRequest)` abre; `DialogHost` dibuja `Dialog` sobre
`<dialog>` nativo con `mqDialogo.abrir` (`showModal`, foco al primer control) y `mqDialogo.cerrar`
(devuelve el foco al disparador). Una confirmación nueva cancela la pendiente con `false`
(`Services/DialogService.cs`, `wwwroot/js/mq-dialogo.js`).

| Elemento | testid | Nota |
| --- | --- | --- |
| `dialog` | `dialogo` | `aria-labelledby="dialogo-titulo"` |
| Título | `dialogo-titulo` | |
| Aviso de consecuencia | — | `Band` tono Atención, `id="dialogo-aviso"` |
| Campo de confirmación escrita | `dialogo-confirmacion` | Solo si `PideEscritura` (segundo grado). **Ninguna pantalla lo pide** (`README.md`: «implementado en el componente y sin uso») |
| Cancelar | `boton-cancelar-dialogo` | Va antes de la acción |
| Acción | `boton-confirmar-dialogo` | Verbo exacto (`RotuloDeAccion`); `mq-btn--destructivo` si `EsDestructiva` (por defecto `true`) |

---

## 7. Inventario de `data-testid`

**84** valores concretos en la web (enumerados desde los `.razor`, expandiendo `medio-{clave}`,
`paso-{N}`, `resumen-{clave}` y los `nav-*`). **63** los usa `MovilidadUrbana.E2ETests`
(`GetByTestId`, `IrPorMenuAsync` y el localizador `[data-testid=fila], [data-testid=tarjeta]`);
**21 no los usa ninguna prueba** (cruce hecho con script sobre `tests/`). Ninguna otra suite toca
la web por `data-testid`.

### 7.1 Shell e Inicio

| testid | Elemento | Usado por E2E |
| --- | --- | --- |
| `estado-app` | Testigo `data-interactivo` | Sí (todas, vía `WaitForInteractiveAsync`) |
| `marca` | Enlace de identidad | **No** |
| `nav-inicio` | Ítem Inicio | **No** |
| `nav-localidades` | Ítem Localidades | Sí (`ElMenuMarcaLaPaginaActiva`) |
| `nav-encuesta` | Ítem Encuesta | Sí |
| `sello-version` | Sello de versión | **No** |
| `titulo` | `h1` de cada página | Sí (Inicio, Localidades, No encontrado; ni el de Encuesta ni el de `/Error`) |
| `ir-localidades`, `ir-encuesta` | Tarjetas de acceso | Sí |

### 7.2 Localidades

| testid | Elemento | Usado por E2E |
| --- | --- | --- |
| `aviso` | Banda de resultado (compartido con Encuesta) | Sí |
| `indisponible`, `boton-reintentar` | Estado indisponible y su reintento | **No** |
| `titulo-formulario` | Cabecera Alta/Editar | Sí |
| `formulario` | `EditForm` del ABM | **No** en esta pantalla (el valor sí se usa en Encuesta) |
| `campo-nombre`, `campo-provincia`, `campo-codigo-postal`, `campo-habitantes` | Controles | Sí |
| `error-nombre`, `error-provincia`, `error-codigo-postal`, `error-habitantes` | Errores por campo | Sí |
| `boton-guardar` | Guardar/Actualizar | Sí |
| `boton-cancelar` | Cancelar edición | **No** |
| `contador` | Insignia del listado | Sí |
| `campo-buscar`, `filtro-provincia` | Barra de filtros | **No** |
| `cuerpo-tabla`, `fila`, `tarjeta` | `tbody`, `tr`, tarjeta apilada | Sí |
| `celda-codigo-postal`, `celda-habitantes` | Celdas | Sí |
| `celda-nombre`, `celda-provincia` | Celdas | **No** |
| `boton-editar`, `boton-eliminar` | Acciones de fila | Sí |
| `sin-datos` | Estado vacío | Sí |
| `boton-cargar-la-primera` | Acción del vacío | **No** |
| `sin-resultados`, `boton-limpiar-filtro` | Filtrado sin resultados y su salida | **No** |
| `dialogo`, `dialogo-titulo`, `boton-cancelar-dialogo`, `boton-confirmar-dialogo` | Diálogo | Sí |
| `dialogo-confirmacion` | Confirmación escrita | **No** (no se dibuja nunca) |

### 7.3 Encuesta

| testid | Elemento | Usado por E2E |
| --- | --- | --- |
| `contador-encuestas` | «Registradas: n» | Sí |
| `formulario` | `EditForm` del asistente | Sí (oculto tras registrar) |
| `paso-1`, `paso-2`, `paso-3` | `section` del paso vigente | Sí |
| `campo-nombre`, `campo-edad`, `campo-localidad`, `error-nombre`, `error-edad`, `error-localidad` | Paso 1 | Sí |
| `grupo-medios` | Contenedor de casillas | **No** |
| `medio-colectivo`, `medio-bicicleta` | Casillas | Sí |
| `medio-auto`, `medio-moto`, `medio-caminata`, `medio-tren` | Casillas | **No** |
| `error-medios`, `campo-frecuencia`, `error-frecuencia` | Paso 2 | Sí |
| `campo-distancia`, `campo-minutos`, `campo-motivo`, `error-distancia`, `error-minutos` | Paso 3 | Sí |
| `error-motivo` | Paso 3 | **No** |
| `etiqueta-paso` | «Paso N de 3» / «Encuesta completada» (dos elementos excluyentes) | Sí |
| `boton-anterior`, `boton-siguiente`, `boton-finalizar` | Pie del asistente | Sí |
| `boton-procesando` | Estado de envío | **No** |
| `resumen`, `mensaje-envio`, `resumen-persona`, `resumen-localidad`, `resumen-medios`, `resumen-frecuencia`, `resumen-distancia`, `resumen-minutos`, `resumen-motivo` | Estado de éxito | Sí |
| `boton-reiniciar` | «Cargar otra encuesta» | Sí |

Otros atributos de prueba que no son `data-testid`: `data-interactivo` (testigo), `data-paso`
(indicador de pasos, usado por `ElIndicadorDePasosAcompanaElAvance` junto con `aria-current` y las
clases `mq-paso--*`) y `data-id` (fila; no lo usa ninguna prueba).

Testids compartidos entre pantallas (`titulo`, `aviso`, `formulario`, `campo-nombre`,
`error-nombre`): no chocan porque cada prueba está en una sola ruta.

Testids **retirados** con el template (2026-09-04, `README.md` «Lo que cambió en las pruebas»):
`modal-nombre`, `boton-cancelar-baja`, `boton-confirmar-baja` → `dialogo-titulo`,
`boton-cancelar-dialogo`, `boton-confirmar-dialogo`; `progreso-contenedor` (con `aria-valuenow`) →
`[data-paso]` con `aria-current="step"`. Ya no existen en `src/`; si una guía los cita, está vencida.

---

## 8. Promesas de la interfaz sin caso E2E

Verificado contra los 22 casos actuales (ninguna prueba navega a estas rutas ni usa estos testids):

| Promesa | Dónde se promete | Estado |
| --- | --- | --- |
| No saltear pasos por URL (`/encuesta/2`, `/encuesta/3`) | `Encuesta.razor.cs` `OnParametersSet` | Sin prueba; ya anotado como «Encontrado, no resuelto» en `CHANGELOG.md` (2026-09-04) y sigue igual |
| Estado de envío `boton-procesando` y el `catch` de `FinishAsync` | `Wizard.razor`, `Encuesta.razor.cs` | Sin prueba; mismo registro del `CHANGELOG.md` (no hay punto de inyección de fallas) |
| Filtro por texto/provincia, «sin resultados», «Limpiar el filtro» | `Localidades.razor.cs` | Sin prueba web (en Android sí: ver [13](13_App-Android.md)) |
| Estado `Indisponible` y reintento | `Localidades.razor.cs` `LoadAsync` | Sin prueba (mismo motivo: no hay inyección de fallas) |
| Cancelar edición, «Cargar la primera localidad» (foco) | `Localidades.razor.cs` | Sin prueba |
| Pantalla `/Error` | `Error.razor` | Sin prueba (solo existe fuera de Development) |
| Sello de versión, aviso de reconexión | `VersionStamp.razor`, `ReconnectionNotice.razor` | Sin prueba |

---

## 9. Desfasajes y rastros encontrados

| # | Qué | Evidencia | Tipo |
| --- | --- | --- | --- |
| D1 | El texto visible del estado indisponible dice **«El service no respondió.»** | `Localidades.razor` línea 29; `git log -S` lo ubica en `946d023`, que cambió «El servicio» → «El service». Contradice la regla del propio renombre: «No cambian el texto visible» (`CHANGELOG.md`, 2026-09-18) | Regresión de texto por el renombre (igual en `Error.razor` de Hola Mundo y Login, ver [10](10_Hola-Mundo-Y-Login.md)) |
| D2 | El esqueleto dice mostrarse «por encima de los 400ms de espera» | Comentario de `Shared/Skeleton.razor`; en `Componentes.css` `.mq-esqueleto` no tiene demora y el componente se dibuja apenas `State` es `Cargando` | Comentario sin respaldo en el código |
| D3 | La descripción de un caso nombra «Nueva encuesta» | `EncuestaTests.NuevaEncuestaDevuelveElAsistenteAlPaso1` `[Description("«Nueva encuesta»…")]`; el botón dice «Cargar otra encuesta» | Texto de prueba desfasado |
| D4 | La guía `Quick-Guide-ABM.md` cita `boton-confirmar-baja`, testid retirado (§7, al final) | Detalle y líneas en [07](07_Guias.md) §5 | Guía desfasada |
| D5–D6 | Rótulos del README («Grilla», «Campo», «Asistente»…) y mensajes/comentarios de componentes con nombres previos al renombre (`GridColumn.cs`, `FieldContext.cs`, `Theme/Icons.cs`, `IDialogService.cs`) | Inventariados en [01](01_Arquitectura.md) §8.3 (README, `GridColumn.cs`, `Theme/Icons.cs`) y [11](11_Template-Y-Superficies.md) §10 (`FieldContext.cs`, `IDialogService.cs`) | Rastros de `946d023` / `e9dea2a` |
| D7 | `EmptyState` con `ActionHref` no emite `data-testid` en el enlace | `Shared/EmptyState.razor` (solo la rama botón usa `ActionTestid`); hoy ninguna pantalla usa `ActionHref` | Asimetría latente, sin efecto actual |

No hay capturas de pantalla de la web de Movilidad Urbana en `evidencia/`: las de
`evidencia/2026-09-01-aplicacion-template/` son de Hola Mundo y Login, y las de
`evidencia/2026-09-12-maui/` y `evidencia/2026-09-13-uitests/` son de Android. La evidencia de la
web son los logs de corrida con 22/22 en verde
(`evidencia/2026-09-12-capas-y-api/movilidad-e2e-tras-extraer-capas.log`,
`evidencia/2026-09-12-unificacion/movilidad-script-por-defecto.log`), ambos de commits del
2026-09-12 (`88e5caa`, `f9f3ca2`; el segundo se borró en `e0f3e9d` y se restauró en `910b42b`), **anteriores** al renombre `946d023` del 2026-09-18.
`evidencia/2026-09-12-renombre/` corresponde a otro renombre (el prefijo `E2E.Base`, `e0f3e9d`) y
solo trae `holamundo.log` y `login.log`. Para el estado posterior a `946d023` solo existe la
declaración del `CHANGELOG.md` (2026-09-18, «Verificado: … 22 E2E de Movilidad Urbana … en
verde»), sin log en `evidencia/`: **no verificado** con evidencia guardada.
