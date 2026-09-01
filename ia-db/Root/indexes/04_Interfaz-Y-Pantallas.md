# 04 — Interfaz y pantallas

> **Propósito**: catalogar las pantallas, su comportamiento y los `data-testid` con los que las
> pruebas las ubican, para poder escribir o corregir un caso E2E sin abrir cada `.razor`.
> **Fuente primaria**: `src/MovilidadUrbana.Web/Components/`.

## Rutas

| Ruta | Componente | Qué es |
| --- | --- | --- |
| `/` | `Pages/Inicio.razor` | Portada con acceso a las dos pantallas |
| `/localidades` | `Pages/Localidades.razor` | ABM de localidades |
| `/encuesta` | `Pages/Encuesta.razor` | Asistente de encuesta en tres pasos |
| `/Error` | `Pages/Error.razor` | Página de error (fuera de Development) |
| `/no-encontrado` | `Pages/NoEncontrado.razor` | Reejecución de `UseStatusCodePagesWithReExecute` |

`Routes.razor` declara además `NotFoundPage="typeof(Pages.NoEncontrado)"`.

## MainLayout — lo que comparten todas las pantallas

`Components/Layout/MainLayout.razor`.

| Elemento | `data-testid` | Nota |
| --- | --- | --- |
| Marca de la barra | `marca` | |
| Enlaces del menú | `nav-inicio`, `nav-localidades`, `nav-encuesta` | La activa lleva `class="active"` y `aria-current="page"` |
| **Testigo de interactividad** | `estado-app` | `div` oculto con `data-interactivo="true|false"` según `RendererInfo.IsInteractive` |

Dos comportamientos con consecuencia en las pruebas:

- **El menú colapsable se resuelve con estado del componente**, no con el JavaScript de Bootstrap.
  El alternador es `.navbar-toggler` y el panel `#menu` recibe la clase `show`. En viewport chico
  hay que desplegarlo antes de hacer clic en un enlace: eso lo encapsula `IrPorMenuAsync`.
- Al navegar, `LocationChanged` cierra el menú: sin recarga de página quedaría abierto sobre la
  pantalla siguiente.

El testigo `estado-app` es la pieza central del laboratorio: durante el prerender vale `false` y
pasa a `true` cuando el circuito quedó conectado. Sin esperarlo, los clics se pierden y las pruebas
fallan de manera intermitente solo en máquinas cargadas — ver
[08_Decisiones-Y-Trampas.md](08_Decisiones-Y-Trampas.md).

## Inicio

`data-testid`: `titulo`, `ir-localidades`, `ir-encuesta`.

## Localidades — el ABM

Formulario a la izquierda, tabla a la derecha, diálogo de confirmación para la baja.

| Zona | `data-testid` |
| --- | --- |
| Título / aviso | `titulo`, `aviso` |
| Formulario | `titulo-formulario`, `formulario`, `boton-guardar`, `boton-cancelar` |
| Campos | `campo-nombre`, `campo-provincia`, `campo-codigo-postal`, `campo-habitantes` |
| Errores por campo | `error-nombre`, `error-provincia`, `error-codigo-postal`, `error-habitantes` |
| Tabla | `tabla`, `cuerpo-tabla`, `fila` (con `data-id`), `contador`, `sin-datos` |
| Celdas | `celda-nombre`, `celda-provincia`, `celda-codigo-postal`, `celda-habitantes` |
| Acciones de fila | `boton-editar`, `boton-eliminar` (con `aria-label` que nombra la localidad) |
| Diálogo de baja | `modal-nombre`, `boton-cancelar-baja`, `boton-confirmar-baja` |

Comportamiento (bloque `@code` de `Localidades.razor`):

| Acción | Qué pasa |
| --- | --- |
| Guardar | Llama a `ServicioDeLocalidades.GuardarAsync`. Si falla, aviso `alert-danger` y campos con `is-invalid`; si va bien, aviso `alert-success`, formulario limpio y recarga |
| Editar | Copia la fila al modelo, limpia errores y aviso; el formulario pasa a modo edición |
| Cancelar | Vuelve el formulario a modo alta |
| Eliminar | Abre el diálogo; **Confirmar** da la baja con aviso `alert-warning`, y si se estaba editando esa misma localidad el formulario vuelve a modo alta |

El aviso muestra el tipo en la clase: `alert-success`, `alert-warning` o `alert-danger`; cuando no
hay aviso el contenedor lleva `d-none`.

El **diálogo es marcado propio** gobernado por `_pendienteDeBaja`, no el modal de Bootstrap: sin
animación de apertura no existe la ventana en la que un clic sobre «Eliminar» se pierde.

`celda-habitantes` se formatea con `ToString("N0")`, es decir con separador de miles **es-AR**. Es
una de las razones por las que la cultura del servidor y el `Locale` del contexto de navegador están
fijados.

## Encuesta — el asistente

| Zona | `data-testid` |
| --- | --- |
| Cabecera | `titulo`, `etiqueta-paso`, `indicador-paso`, `contador-encuestas`, `progreso-contenedor`, `progreso` |
| Aviso y formulario | `aviso`, `formulario` |
| Secciones | `paso-1`, `paso-2`, `paso-3` |
| Paso 1 | `campo-nombre`, `campo-edad`, `campo-localidad` (+ `error-*`) |
| Paso 2 | `grupo-medios`, `medio-colectivo` … `medio-tren`, `campo-frecuencia` (+ `error-medios`, `error-frecuencia`) |
| Paso 3 | `campo-distancia`, `campo-minutos`, `campo-motivo` (+ `error-*`) |
| Navegación | `boton-anterior`, `boton-siguiente`, `boton-finalizar`, `boton-reiniciar` |
| Resumen | `resumen`, `mensaje-envio`, `resumen-persona`, `resumen-localidad`, `resumen-medios`, `resumen-frecuencia`, `resumen-distancia`, `resumen-minutos`, `resumen-motivo` |

Comportamiento:

- `_paso` va de 1 a `ReglasDeEncuesta.TotalDePasos` (3). `boton-anterior` está `disabled` en el paso 1.
- En el paso 3 `boton-siguiente` se reemplaza por `boton-finalizar`; tras registrar, el pie muestra
  solo `boton-reiniciar` («Nueva encuesta»), que devuelve el asistente al paso 1 con el modelo vacío.
- `Siguiente` valida el paso actual con `ValidarPaso`; si hay errores no avanza y muestra «Complete
  los datos del paso antes de continuar.».
- `Anterior` limpia aviso y errores pero **conserva lo cargado** (hay una prueba dedicada).
- `Porcentaje` = `paso × 100 / 3` redondeado, y 100 una vez completada.
- `EtiquetaDelPaso`: «Paso N de 3 — <título>», con los títulos «Datos de la persona», «Medios que
  utiliza para viajar» y «Distancia recorrida»; ya completada dice «Encuesta completada».
- **El desplegable de localidades se alimenta del ABM**: `OnInitializedAsync` llama a
  `ServicioDeLocalidades.ListarAsync()`. Las dos pantallas comparten el mismo almacén por sesión.
- `contador-encuestas` sale de `ServicioDeEncuestas.ContarAsync()`, también acotado a la sesión.
- `resumen-distancia` se formatea con `"0.###"` y `resumen-medios` sale en el orden del catálogo.

## Enlace de datos: `oninput`, no `onchange`

Los campos numéricos (`campo-habitantes`, `campo-edad`, `campo-distancia`, `campo-minutos`) usan
`@bind:event="oninput"`, y los de texto (`campo-nombre`, `campo-codigo-postal`) enganchan `@oninput`
directamente sobre el modelo.

El motivo es de pruebas: **`FillAsync` dispara `input`, no `change`**. Con el `@bind` por defecto
—que escucha `onchange`— el valor no llega al servidor hasta que el campo pierde el foco, y la
validación rechaza un formulario que en pantalla se ve completo. Los `<select>` sí usan `@bind` a
secas, porque un cambio de selección dispara `change`.

## Estilos

Bootstrap 5.3.8 vendorizado en `wwwroot/vendor/bootstrap/bootstrap.min.css` —sin CDN y **sin el
bundle de JavaScript**—, más `wwwroot/css/estilos.css` y el CSS aislado del proyecto
(`MovilidadUrbana.Web.styles.css`). Los tres se enlazan desde `App.razor` con `@Assets[…]`.
