# 04 — Interfaz y pantallas de Movilidad Urbana

> **Propósito**: catalogar las pantallas de Movilidad Urbana, su comportamiento y los `data-testid`
> con los que las pruebas las ubican, para poder escribir o corregir un caso E2E sin abrir cada
> `.razor`.
> **Fuente primaria**: `src/MovilidadUrbana.Web/Components/`, incluidos `App.razor` y `Routes.razor`.
> **Vigencia**: 2026-09-12, commit `7262395`. Las superficies de Hola Mundo y Login están en
> [10](10_Hola-Mundo-Y-Login.md); la forma constructiva común a las tres, en
> [11](11_Template-Y-Superficies.md).

Desde el 2026-09-04 la interfaz es el **template del Framework SDD**: ya no hay Bootstrap, y varios
identificadores cambiaron. La correspondencia está al final, en
[«Identificadores que cambiaron»](#identificadores-que-cambiaron).

## Rutas

| Ruta | Componente | Qué es |
| --- | --- | --- |
| `/` | `Pages/Inicio.razor` | Portada con acceso a las dos pantallas |
| `/localidades` | `Pages/Localidades.razor` | ABM de localidades |
| `/encuesta` y `/encuesta/{Paso:int}` | `Pages/Encuesta.razor` | Asistente en tres pasos; el paso vigente está en la dirección |
| `/Error` | `Pages/Error.razor` | Página de error (fuera de Development) |
| `/no-encontrado` | `Pages/NoEncontrado.razor` | Reejecución de `UseStatusCodePagesWithReExecute` |

## Documento y render — App.razor

| Pieza | Qué hace |
| --- | --- |
| `<HeadOutlet @rendermode="InteractiveServer" />` y `<Routes @rendermode="InteractiveServer" SesionId="…" />` | El render mode se fija **en la raíz** y no por página: el identificador de sesión se lee en `App.razor`, el único lugar con la petición HTTP a mano, y se pasa a `Routes`. Es una desviación declarada del template |
| `<a class="mq-skip" href="#mq-main">Ir al contenido</a>` | Salto al contenido |
| `FocusOnNavigate` sobre `#mq-main` (en `Routes.razor`) | Mueve el foco al contenido al navegar |
| Hojas | `Tokens.css` → `Componentes.css` → `MovilidadUrbana.Web.styles.css` |
| Scripts | `js/mq-dialogo.js`, `js/mq-foco.js`, `_framework/blazor.web.js` |

## El shell — MainLayout

`Components/Layout/MainLayout.razor`.

| Elemento | `data-testid` | Nota |
| --- | --- | --- |
| Barra lateral (`Componentes/BarraLateral.razor`) | `marca`; ítems `nav-inicio`, `nav-localidades`, `nav-encuesta` | El ítem activo lleva `aria-current="page"` |
| Contenido | — | `main#mq-main` |
| Sello de versión | `sello-version` | Resuelto en el host por `IIdentidadDeVersion` |
| Host de diálogos | — | `DialogoHost`, único en el layout |
| Aviso de reconexión | — | `AvisoDeReconexion`, banda de atención que no bloquea la interacción |
| **Testigo de interactividad** | `estado-app` | `div hidden` con `data-interactivo` |

Debajo del único punto de quiebre, 768px, la barra lateral pasa a navegación superior **con los
enlaces a la vista**: no hay menú que desplegar. Por eso `IrPorMenuAsync` de las pruebas ya solo hace
clic.

El testigo `estado-app` es la pieza central de la estabilidad de las pruebas: sin circuito conectado
la pantalla se ve pero no responde, y los clics se pierden de forma intermitente — ver
[08_Decisiones-Y-Trampas.md](08_Decisiones-Y-Trampas.md).

## Inicio

`data-testid`: `titulo`, `ir-localidades`, `ir-encuesta`. Toda la tarjeta de acceso es el área
activable.

## Localidades — el ABM

| Zona | `data-testid` |
| --- | --- |
| Título y aviso | `titulo`, `aviso` —una `Banda` con tono de éxito o de error— |
| Formulario | `titulo-formulario`, `formulario`, `boton-guardar`, `boton-cancelar` |
| Campos | `campo-nombre`, `campo-provincia`, `campo-codigo-postal`, `campo-habitantes` |
| Errores por campo | `error-nombre`, `error-provincia`, `error-codigo-postal`, `error-habitantes` |
| Filtros | `campo-buscar` (nombre o código postal), `filtro-provincia` |
| Colección (`Grilla`) | `contador`, `cuerpo-tabla`, `fila` (con `data-id`), `tarjeta`; celdas `celda-nombre`, `celda-provincia`, `celda-codigo-postal`, `celda-habitantes` |
| Acciones de fila | `boton-editar`, `boton-eliminar` |
| Estados | `indisponible` + `boton-reintentar` · `sin-datos` + `boton-cargar-la-primera` · `sin-resultados` + `boton-limpiar-filtro` |
| Diálogo de baja (`Dialogo`) | `dialogo`, `dialogo-titulo`, `dialogo-confirmacion`, `boton-cancelar-dialogo`, `boton-confirmar-dialogo` |

Comportamiento:

| Acción | Qué pasa |
| --- | --- |
| Guardar | Llama a `ServicioDeLocalidades.GuardarAsync`. Con errores, banda de error y error asociado a cada campo por `aria-describedby`; si va bien, banda de éxito y formulario limpio. Si la operación falla, «No pudimos guardar la localidad. Volvé a intentar en unos segundos.» |
| Editar / Cancelar | El formulario pasa a modo edición y vuelve a modo alta |
| Eliminar | Pide confirmación con `IServicioDeDialogos.ConfirmarAsync` —primer grado—, y la baja muestra su banda |
| Buscar / filtrar | Filtra lo ya traído; si hay datos y el filtro no encuentra nada, estado `FiltradoSinResultados` |

- **La colección se presenta de dos formas, las dos siempre en el marcado**: tabla con `caption` y
  `scope`, y tarjetas apiladas. Las conmuta el punto de quiebre, así que las pruebas buscan las
  acciones de fila **sobre la presentación visible**.
- **`Vacio` y `FiltradoSinResultados` son estados distintos**, con acciones distintas: cargar la
  primera localidad o limpiar el filtro.
- El diálogo es el `<dialog>` nativo: confinamiento de foco y cierre con Escape los trae el
  navegador, y el foco vuelve al control que lo abrió. La confirmación escrita —segundo grado— está
  implementada en el componente y no se usa.

## Encuesta — el asistente

| Zona | `data-testid` |
| --- | --- |
| Cabecera | `titulo`, `contador-encuestas` —una `Insignia` con «Registradas: N»— |
| Aviso y formulario | `aviso`, `formulario` |
| Indicador de pasos (`Asistente`) | `etiqueta-paso` («Paso N de 3»); los `li[data-paso]` con `aria-current="step"` en el vigente y clases `mq-paso--completado`, `--actual`, `--pendiente` |
| Secciones (`PasoDeAsistente`) | `paso-1`, `paso-2`, `paso-3` |
| Paso 1 | `campo-nombre`, `campo-edad`, `campo-localidad` + `error-nombre`, `error-edad`, `error-localidad` |
| Paso 2 | `grupo-medios`, `medio-<clave>`, `campo-frecuencia` + `error-medios`, `error-frecuencia` |
| Paso 3 | `campo-distancia`, `campo-minutos`, `campo-motivo` + `error-distancia`, `error-minutos`, `error-motivo` |
| Navegación | `boton-anterior`, `boton-siguiente`, `boton-finalizar`, `boton-procesando`, `boton-reiniciar` |
| Resumen | `resumen`, `mensaje-envio`, `resumen-<clave>` |

Comportamiento (`Encuesta.razor` y `Encuesta.razor.cs`):

- `boton-anterior` está deshabilitado en el paso 1; en el paso 3 `boton-siguiente` se reemplaza por
  `boton-finalizar`, y mientras se registra, por `boton-procesando`.
- **Se avanza solo con el paso vigente válido** (`ServicioDeEncuestas.ValidarPaso`); si no, banda
  «Complete los datos del paso antes de continuar.». **Hacia atrás nunca se valida** y lo cargado se
  conserva.
- **El paso vigente está en la dirección**: cada cambio hace `NavigateTo("/encuesta/N", replace:
  true)`. `OnParametersSet` **impide saltear** pasos pedidos por dirección, acotando al paso máximo
  alcanzado.
- Registrada la respuesta, la superficie pasa a su estado de éxito: `etiqueta-paso` dice «Encuesta
  completada» y el resumen se recorre desde `ResumenDeEncuesta`. `boton-reiniciar` («Cargar otra
  encuesta») vuelve al paso 1 con el modelo vacío.
- **El desplegable de localidades se alimenta del ABM**, y `contador-encuestas` sale de
  `ServicioDeEncuestas.ContarAsync()`, los dos acotados a la sesión.
- Si registrar falla, banda de error. **Ni ese camino ni el paso direccionable tienen caso de
  prueba**: está registrado en `Guides/E2E-Guide/Caso-Encuesta-Page.md` §6, en
  `Lab-E2E.WebBlazor.Documentacion`.

## Enlace de datos: `oninput`, no `onchange`

**`FillAsync` de Playwright dispara `input`, no `change`.** Con el `@bind` por defecto —que escucha
`onchange`— el valor no llega al servidor hasta que el campo pierde el foco, y la validación rechaza
un formulario que en pantalla se ve completo. Por eso:

| Pantalla | `@oninput` directo | `@bind:event="oninput"` | `@bind` a secas (`<select>`) |
| --- | --- | --- | --- |
| Localidades | `campo-nombre`, `campo-codigo-postal`, `campo-buscar` | `campo-habitantes` | `campo-provincia`, `filtro-provincia` (este con `@bind:after`) |
| Encuesta | `campo-nombre` | `campo-edad`, `campo-distancia`, `campo-minutos` | `campo-localidad`, `campo-frecuencia`, `campo-motivo` |

Los `<select>` usan `@bind` a secas porque un cambio de selección sí dispara `change`.

## Estilos

`wwwroot/css/Tokens.css` y `Componentes.css`, más el CSS aislado de `AvisoDeReconexion`. Ningún
`.razor` escribe un color, una tipografía o un espaciado. El detalle, en
[11_Template-Y-Superficies.md](11_Template-Y-Superficies.md).

<a id="identificadores-que-cambiaron"></a>

## Identificadores que cambiaron

Con el template (2026-09-04). La suite siguió siendo de 22 casos y ninguna verificación se aflojó.

| Antes | Ahora | Por qué |
| --- | --- | --- |
| `.navbar-toggler` y `#menu` con clase `show` | No existen | La barra lateral no se colapsa: pasa a navegación superior con los enlaces a la vista |
| `modal-nombre`, `boton-cancelar-baja`, `boton-confirmar-baja` | `dialogo-titulo`, `boton-cancelar-dialogo`, `boton-confirmar-dialogo` | El diálogo es un componente único gobernado por el servicio |
| `progreso-contenedor`, `progreso`, `indicador-paso` | `li[data-paso]` con `aria-current="step"` y clases de estado; `etiqueta-paso` | El catálogo norma el indicador de pasos; la barra de progreso era un segundo canal |
| `tabla`; avisos con `alert-*` y `d-none` | `Grilla` con `cuerpo-tabla`, `fila` y `tarjeta`; avisos como `Banda` | Tabla y tarjetas conviven en el marcado |

Fuente: la tabla «Lo que cambió en las pruebas» de `README.md` y el `CHANGELOG.md` del 2026-09-04.
