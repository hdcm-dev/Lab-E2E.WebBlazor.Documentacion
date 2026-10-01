# Template HTML de maqueta — forma constructiva por defecto del Framework SDD

**Alias:** Template-HTML-SDD-Default
**Naturaleza:** propio
**Tema:** Forma constructiva de una maqueta HTML/CSS/JS sin proceso de build: layout de archivos, tokens, conmutador declarativo de estados, y los cuatro tipos de diálogo (ABM clásico, asistente de varios niveles, ventana modal y presentación de datos)
**Consumidor:** 03, AG-00031
**Condicion-de-carga:** proyectos de código con `requiere_maqueta == true` que construyan la maqueta con HTML, CSS y JavaScript planos
**Hereda-de:** —
**Sustituye:** —
**Compatible-con:** Rules-Base-Conocimiento.md 2.2
**Versión:** 1.0
**Estado:** Vigente
**Fecha:** 2026-09-01

---

## 0. Propósito y alcance

Este documento caracteriza **cómo se construye** una maqueta de la familia que el Framework SDD produce
hoy: qué archivos tiene, qué contrato hay entre el HTML y el JavaScript, cómo se declara y se conmuta el
estado de una superficie, y con qué forma se resuelven los cuatro tipos de diálogo que un producto de
gestión necesita —ABM clásico, asistente de varios niveles, ventana modal y presentación de datos—.

La medida del documento es una sola: **un agente que nunca vio una maqueta SDD tiene que poder producir
una equivalente leyendo sólo esto**.

**Qué queda explícitamente afuera:**

| Fuera de alcance | Dónde vive |
| --- | --- |
| Qué superficies hay que maquetar y con qué mínimo por tipo D8 | `Maqueta-Rules.md` §4.4 |
| Los criterios de aceptación de la maqueta y sus anti-patrones de proceso | `Maqueta-Rules.md` §8 y §9 |
| Cuándo corre la fase de maqueta, cómo se valida con el humano y cómo se retroalimenta 03 | `Maqueta-Rules.md` §3 |
| Los tokens semánticos y su valor de referencia, los diez patrones y el mapa canónico de estados | `Design-Rules-Web-Generico.md` §2, §4 y §5 |
| La línea de base visual, el contrato de datos y los umbrales de deriva | `Deriva-Rules.md` §2 y §3 |
| El qué funcional y la arquitectura de la capa de presentación | Categorías 02 y 05 |

**Omisiones declaradas.** §5 supera el techo de 600 líneas de `Rules-Base-Conocimiento.md` §6.2 sumado al
resto del documento. Se acoge a la excepción de §4.3 y §6.2: los esqueletos son la única forma en que las
formas constructivas del HTML, del CSS y del JavaScript se transmiten sin pérdida —el mismo criterio que
`Templates/README.md` invoca— y partirlos por tipo de diálogo produciría documentos que hay que cargar
de a cuatro para resolver una sola superficie.

**Verificación de ofuscación.** Los esqueletos se relevaron de una maqueta real de un proyecto de código
concreto y se reescribieron con entidades neutras: `Entidad`, `Registro`, `Elemento`, `Usuario`, con
identificadores `REG-0001` y roles `rol-a` / `rol-b`. Se buscaron y se eliminaron los términos del
dominio de origen, los nombres propios de personas y de instituciones, y los nombres de archivo de sus
superficies. Falso positivo léxico declarado, uno solo: **«elemento»**, que aparece como nombre de
entidad neutra y no como término del dominio de origen.

---

## 1. Identidad del artefacto

| Rasgo | Valor |
| --- | --- |
| Qué es | Una maqueta navegable estática: una página HTML por superficie, sin backend y sin llamadas de red |
| Stack | HTML5 semántico, CSS con variables nativas, JavaScript ES5 en IIFE, Bootstrap 5.0 por CDN |
| Proceso de build | Ninguno. Lo que se edita es lo que se sirve |
| Dependencias | Sólo la hoja de Bootstrap por CDN. Sin gestor de paquetes, sin `node_modules` |
| Cómo se abre | Servidor liviano (`python3 -m http.server 8080`, Live Server) o doble clic sobre `index.html` |
| Autonomía | Total. Ninguna llamada a servicios reales; los filtros y las búsquedas actúan sobre lo ya renderizado |
| Idioma del código | Español: clases, funciones, atributos y datos |

**Supuestos.** El navegador soporta `&lt;dialog&gt;` con `showModal()`, variables CSS, `URLSearchParams` y
`sessionStorage`. El template degrada de forma explícita cuando alguno falta, en lugar de fallar.

**La elección de stack es sustituible; lo que la maqueta tiene que demostrar, no.** Una organización que
construye siempre con proceso de build declara la sustitución de `Maqueta-Rules.md §4.1 · tecnología de
construcción` en su propio documento de conocimiento. Los tokens del catálogo, la autonomía sin backend,
los cuatro estados por superficie y WCAG 2.2 AA se cumplen igual con la tecnología que sea.

---

## 2. Estructura

### 2.1 Layout de archivos

```text
<Nombre-Proyecto-De-Codigo>/
├── README.md                    naturaleza, cómo se corre, alcance, procedencia de los datos,
│                                mapa de corrección a mano y reglas de arquitectura
├── index.html                   portada: navegación a todas las superficies, contrato de campos
│                                e invariantes de la maqueta
├── <Superficie>.html            una por superficie, con el nombre canónico de su wireframe
└── assets/
    ├── css/Estilos-Maqueta.css  tokens del catálogo como variables CSS y patrones de componente
    ├── js/Datos-Maqueta.js      fuente única de datos de ejemplo, catálogos, textos y contrato
    ├── js/Maqueta.js            armazón, conmutación de estados, render de lo que dos superficies comparten
    └── img/                     vacía por defecto: los íconos son SVG inline
```

**Regla de reparto entre `Maqueta.js` y el HTML de cada superficie**: un bloque que **dos o más**
superficies presentan vive en `Maqueta.js`; un bloque exclusivo de una superficie vive en el `&lt;script&gt;`
inline de esa superficie. Duplicarlo obligaría a corregirlo dos veces, que es exactamente lo que la
validación manual del humano no tolera.

### 2.2 Las tres piezas de JavaScript y su orden

El orden de carga es contractual y no se puede alterar:

| Orden | Archivo | Publica | Consume |
| --- | --- | --- | --- |
| 1 | `assets/js/Datos-Maqueta.js` | `window.DatosMaqueta` | nada |
| 2 | `&lt;script&gt;` inline de la superficie | `window.renderSuperficie`, opcionalmente `window.alCambiarEstado` | nada, sólo declara |
| 3 | `assets/js/Maqueta.js` | `window.Maqueta`, y **arranca solo** | los dos anteriores |

`Maqueta.js` arranca en `DOMContentLoaded` —o de inmediato si el documento ya cargó—, pinta el armazón,
**llama al hook `renderSuperficie(Maqueta, DatosMaqueta)`**, releva del DOM los estados declarados y
aplica el estado inicial. Es inversión de control: la página no llama al motor, el motor llama a la
página.

### 2.3 Los dos shells

| Shell | Cuándo | Marcado raíz | Qué tiene | Qué no tiene |
| --- | --- | --- | --- | --- |
| **Acceso** | Sin sesión, o acto indivisible de primer arranque | `.mq-lienzo` + `main.mq-tarjeta-acceso` | Marca, tarjeta angosta anclada arriba, sello de versión al pie | Navegación, barra lateral, barra superior |
| **Trabajo** | Con sesión | `.mq-shell` + `nav.mq-shell-sidebar` + `.mq-shell-contenido > main` | Barra lateral con el ítem activo, contenido, sello al pie | — |

La transición entre shells es **una navegación completa a otro archivo**, nunca un `hidden` dentro de la
misma superficie. Una superficie que legítimamente tiene los dos cursos —establecer una credencial por
primera vez y cambiarla estando adentro— lleva los dos árboles completos, mutuamente excluyentes por
estado, y por lo tanto dos `&lt;main&gt;` con `id` distinto.

### 2.4 Secciones del CSS

`Estilos-Maqueta.css` se carga **después** de Bootstrap y lo sobreescribe. Orden interno fijo:

1. `:root` con todos los tokens y la única regla de `prefers-reduced-motion`.
2. Reset acotado, `.mq-sr-only`, `.mq-skip`, `:focus-visible`.
3. Shell de trabajo y barra lateral.
4. Shell de acceso y tarjeta.
5. Componentes: botones, campos, insignias, bandas, tablas, tarjetas apiladas, esqueletos, vacíos,
   diálogos, árbol.
6. Utilitarias de composición con nombre.
7. El único `@media (max-width: 768px)`.

### 2.5 Secciones del JavaScript

`Maqueta.js` es una IIFE única sobre `window`, dividida en bloques comentados, sin objetos-namespace y
sin módulos ES. Bloques mínimos: sello de la maqueta, iconografía, utilidades, navegación entre
superficies, los dos shells, sello de versión, conmutación de estados, barra de validación, render de
colecciones compartidas, diálogos y arranque. Un submódulo con estado propio —si el producto tiene un
componente con bitácora, por ejemplo— se escribe como IIFE anidada que devuelve un objeto.

---

## 3. Contrato de uso

### 3.1 Atributos del `&lt;body&gt;`

| Atributo | Valores | Quién lo consume |
| --- | --- | --- |
| `data-superficie` | Nombre canónico de la superficie | Clave de `sessionStorage` del estado elegido, y rótulo de la barra de validación |
| `data-shell` | `acceso` \| `trabajo` \| `mixto` | Documental; el shell efectivo lo decide la presencia de `[data-mq-sidebar]` |
| `data-papel` | `rol-a` \| `rol-b` | Arma la barra lateral y decide qué acciones se dibujan |
| `data-destino` | Identificador del ítem de navegación activo | Marca `aria-current="page"` en la barra lateral |
| `data-estado-inicial` | Identificador de estado | Estado que se aplica al terminar el arranque |

### 3.2 El conmutador de estados

**`data-mq-estado="a b c"` en cualquier nodo significa: este bloque se ve sólo si el estado vigente es
`a`, `b` o `c`.** Un nodo sin el atributo se ve siempre. La conmutación es una sola pasada que setea
`hidden`, y el inventario de estados **se releva del DOM**, no se declara en JavaScript: agregar un
estado es agregar un bloque con su atributo, y aparece solo en la barra de validación.

Ese único mecanismo resuelve los cuatro estados obligatorios —`vacio`, `cargando`, `con-datos`,
`error`— y todos los que el wireframe declare de más. Vocabulario de estados de esta familia, agrupado:

| Grupo | Identificadores |
| --- | --- |
| Ciclo de datos | `cargando`, `vacio`, `filtrado-sin-resultados`, `con-datos`, `indisponible` |
| Ciclo de acción | `enviando`, `error-entrada`, `error-operacion`, `exito` |
| Confirmación | `confirmando-<accion>`, `aplicando-<accion>` |
| Transporte | `reconectando`, `recuperado`, `transporte-replegado`, `fallo-no-clasificado` |
| Identidad de versión | `version-preliminar`, `origen-indeterminado` |

`filtrado-sin-resultados` es un estado **distinto** de `vacio`: en el primero hay datos y el filtro no
encontró nada, y la acción es «Limpiar el filtro»; en el segundo no hay datos, y la acción es crear el
primero. Confundirlos le miente al validador humano.

Una superficie que no presenta ninguna colección **declara igual su bloque de vacío**, con el texto «No
aplica. Esta superficie no presenta ninguna colección. Se declara para que la ausencia sea deliberada.»

### 3.3 Los dos hooks de página

```js
// Obligatorio. Corre una vez, después de que el armazón está pintado.
window.renderSuperficie = function (M, D) { /* hidratación de esta superficie */ };

// Opcional. Corre ANTES de la pasada de visibilidad, en cada cambio de estado.
// Sólo para lo que no se resuelve mostrando y ocultando: repoblar una tabla, mover el foco.
window.alCambiarEstado = function (id) { /* … */ };
```

`M` es la fachada `window.Maqueta`; `D` es `window.DatosMaqueta`. **Ninguna superficie toca las globales
por nombre**: las recibe por parámetro, para que el contrato sea visible en la firma.

### 3.4 Fachada mínima que `Maqueta.js` expone

| Miembro | Qué hace |
| --- | --- |
| `$(sel, raiz)` / `$$(sel, raiz)` | `querySelector` / `querySelectorAll` como arreglo |
| `esc(texto)` | Escapa `& < > "`. **Obligatorio antes de todo `innerHTML`** |
| `icono(nombre, tamanio, titulo)` | Devuelve el SVG inline. Sin `titulo` es decorativo (`aria-hidden`); con `titulo`, significativo (`role="img"` + `&lt;title&gt;`) |
| `insignia(valor)` | Devuelve la insignia de estado. **Siempre imprime el texto**: el color nunca es el único canal |
| `parametro(nombre)` | Lee un parámetro de la URL |
| `papelVigente()` | Resuelve el rol desde la URL o desde `data-papel` |
| `hrefDetalle(id, papel, desde)` | Construye la URL de detalle. Los caminos de navegación son funciones nombradas, no cadenas armadas en línea |

### 3.5 Parámetros de URL

Cuatro, y ninguno más: `?t=` identificador de la entidad en foco, `?papel=` rol vigente, `?desde=`
superficie de retorno, `?estado=` estado inicial forzado. El último es de la maqueta, no del producto:
permite abrir cualquier superficie directamente en cualquiera de sus estados, que es lo que hace
verificable la validación.

### 3.6 Tokens y su gobierno

Todo valor visual sale de una variable de `:root`. Familias, con el rol de cada una:

| Familia | Tokens |
| --- | --- |
| Superficies | `--color-background-primary` \| `-secondary` \| `-tertiary` |
| Texto | `--color-text-primary` \| `-secondary` \| `-tertiary` \| `-danger`, `--color-text-on-brand` |
| Bordes | `--color-border-secondary` \| `-tertiary` \| `-danger` |
| Marca | `--color-brand-primary` \| `-dark` \| `-tint` |
| Acento por módulo | `--color-accent-module-a` … `-d`. Codifican pertenencia, no estética |
| Semánticos, **siempre en par texto+tint** | `--color-text-success` / `--color-background-success`, e igual para `warning`, `error`, `info` |
| Velo | `--color-backdrop` |
| Tipografía | `--font-sans`, `--font-mono`, y cinco escalones con **par size+weight**: `title` 17/500, `body-strong` 14/500, `body` 13/400, `caption` 12/400, `meta` 11/500 |
| Espaciado | `--space-1` … `--space-9`, escala 4, 8, 12, 14, 16, 18, 20, 22, 28 |
| Radios y bordes | `--radius-md` \| `-lg` \| `-pill` \| `-icon`, `--border-hairline`, `--border-control` |
| Movimiento | `--motion-fast` 150ms, `--motion-base` 200ms, `--motion-ease` |
| Layout | `--shell-sidebar-width` |

**Qué se toca al derivar el template**: los tres tokens de marca si el producto tiene acento propio, el
diccionario de íconos, `Datos-Maqueta.js` entero y los rótulos de entidad en los HTML. **Qué no se
toca**: los nombres de las variables, que son los del catálogo y sostienen la trazabilidad entre el
diseño y la implementación. Un valor visual nuevo **se promueve al catálogo antes de usarse**.

### 3.7 Convención de nombres

| Familia | Convención | Ejemplo |
| --- | --- | --- |
| Archivos de superficie | Título-Con-Guiones, sin sufijo de versión. `index.html` es la única minúscula | `Panel-De-Registros.html` |
| Clases CSS | Prefijo `mq-`, BEM parcial: `--` para modificador siempre, `__` para elemento sólo cuando el componente tiene partes nombradas | `.mq-btn--destructivo`, `.mq-barra-validacion__rotulo` |
| Utilitarias | Con nombre y valor de token. Existen para que **ningún HTML lleve `style=` en línea** | `.mq-mt-5`, `.mq-ancho-38`, `.mq-prosa` |
| Ganchos JS | `data-mq-<cosa>`, kebab-case en el HTML, camelCase al leerlos por `dataset` | `data-mq-filas-registros` |
| Funciones | Español. `pintar*` arma el HTML de una zona del armazón; `render*` llena una colección dentro de un host existente; sustantivo-función para consultas | `pintarBarraLateral`, `renderListadoDeRegistros`, `papelVigente` |
| Tablas de configuración | MAYÚSCULA_CON_GUION_BAJO, al tope de su bloque | `ICONOS`, `ROTULOS_DE_ESTADO` |
| Identificadores del dataset | Prefijo de entidad + número | `REG-0001`, `ELM-0003` |

### 3.8 Contrato del dataset

`Datos-Maqueta.js` es una IIFE que publica un único objeto global. Organizado en bloques numerados y
comentados, cada uno con la procedencia documental de sus datos.

```js
window.DatosMaqueta = (function () {
  'use strict';

  var IDENTIDAD_DE_VERSION = { versionLegible: 'v1.4.0', identificadorDeConstruccion: '…',
                               esPreliminar: false, origenIndeterminado: false };

  var REGISTROS = [
    { id: 'REG-0001', nombre: 'Registro de ejemplo 01', iniciales: 'R1',
      atributo: 'ejemplo01@dominio.test',
      estado: 'Habilitado',              // valor del modelo de dominio
      etiquetaEstado: 'Habilitada',      // rótulo de interfaz, concordado en género
      fechaAlta: '05/08/2026',           // ya formateada; la maqueta no formatea
      operable: true,                    // regla de negocio materializada como bandera
      origen: 'Wireframes-Panel-De-Registros.md §2' }
  ];

  var INSIGNIAS = {
    'Borrador':   { clase: 'mq-insignia--neutro',   nota: '…' },
    'Pendiente':  { clase: 'mq-insignia--atencion', nota: '…' },
    'Finalizado': { clase: 'mq-insignia--exito',    nota: '…' },
    'Rechazado':  { clase: 'mq-insignia--peligro',  nota: '…' }
  };

  var TEXTOS = { indisponibleTitulo: '…', indisponibleCuerpo: '…', avisoDeArrastre: '…' };

  var CONTRATO_DE_CAMPOS = [
    { entidad: 'Registro', campo: 'atributo', tipo: 'texto',
      ejemplo: 'ejemplo01@dominio.test', origen: 'Modelo conceptual 02 §3' }
  ];

  var INVARIANTES = ['El total de registros habilitados del caso canónico es 3.'];

  return {
    identidadDeVersion: IDENTIDAD_DE_VERSION, registros: REGISTROS, insignias: INSIGNIAS,
    textos: TEXTOS, contratoDeCampos: CONTRATO_DE_CAMPOS, invariantes: INVARIANTES,
    // Ayudas de lectura: el "acceso a datos" del dataset. Relaciones por clave foránea,
    // nunca por objetos anidados.
    registro: function (id) { return REGISTROS.filter(function (r) { return r.id === id; })[0] || null; },
    elementosDe: function (registroId) {
      return ELEMENTOS.filter(function (e) { return e.registroId === registroId; });
    }
  };
}());
```

Cinco reglas del dataset, todas verificables:

1. **Fuente única.** Ningún HTML hardcodea datos.
2. **Cada registro lleva `origen`**, la traza al documento del que sale. Lo que no tiene respaldo
   documental lleva `origen: 'compuesto-para-la-maqueta'` y **no se traslada a la especificación sin una
   decisión explícita**.
3. **El valor del dominio y su rótulo son campos distintos.**
4. **Las relaciones se resuelven por clave foránea y ayudas de lectura**, no por anidamiento.
5. **Cantidad suficiente para los casos límite** declarados en los casos de uso: la fila más larga, el
   valor nulo, la categoría con muchos elementos, el estado de error.

---

## 4. Decisiones ya tomadas

| Bifurcación | Qué resolvió el template | Criterio |
| --- | --- | --- |
| Framework de componentes vs. HTML plano | HTML plano con Bootstrap sólo como base | Sin build, lo que se edita es lo que se sirve; el humano corrige a mano y no pierde su trabajo |
| ES5 con `var` e IIFE vs. módulos ES | ES5 en IIFE | Sin transpilación, sin `type="module"`, y abre desde `file://` sin servidor |
| Estado en JavaScript vs. estado declarado en el marcado | Declarado en el marcado con `data-mq-estado` | El inventario de estados se releva del DOM; agregar un estado no toca código |
| Router vs. una página por superficie | Una página por superficie, enlaces `&lt;a href&gt;` planos, contexto por query string | Cada superficie es un archivo con el nombre canónico de su wireframe, y se abre sola |
| Responsive por reflow vs. dos presentaciones | Tabla y tarjetas apiladas **ambas siempre en el DOM**, conmutadas por CSS | Una tabla que reflowea deja de ser tabla; cambiar el tipo de presentación es deriva mayor |
| Librería de modales vs. `&lt;dialog&gt;` nativo | `&lt;dialog&gt;` nativo con `showModal()` | Trae confinamiento de foco y cierre por Escape sin código, con degradación explícita |
| Asistente multipaso vs. superficies encadenadas | **Superficies encadenadas por URL**, con acuse en la superficie de destino | Un asistente se abandona a la mitad y deja el sistema en estado parcial. Se usa asistente sólo donde el acto es divisible y reanudable |
| Acción no disponible: deshabilitada vs. no dibujada | **No se dibuja**, ni siquiera inhabilitada | Lo que no aplica no se muestra; mostrarlo deshabilitado sugiere una granularidad que no existe |
| Botón único con `disabled` dinámico vs. dos botones | Dos botones conmutados por estado | El estado de envío es un estado de la superficie, no una propiedad del control |
| Confirmación destructiva: una sola forma vs. dos grados | Dos grados: confirmación simple, y confirmación **escrita** cuando la baja arrastra dependientes | La fricción se gradúa por la consecuencia, no por el gusto |
| `style=` en línea vs. utilitarias con nombre | Utilitarias con nombre, cada una materializando un token | Un `style=` es un literal visual ad hoc con otro nombre |
| Íconos por CDN o raster vs. SVG inline | Diccionario de trazos SVG inline con `currentColor`, grilla de 24, trazo 1.75 | Hereda el color, escala, y no depende de una red |
| Validación real vs. exhibición de estados | `&lt;form novalidate&gt;`, botones `type="button"`, la maqueta **no valida ni envía** | La maqueta demuestra la superficie; la validación que decide vive en el sistema |

**Deuda declarada del artefacto, no decisión.** El template no trae paginación ni ordenamiento de
columnas, y el catálogo de diseño tampoco los norma: quedan a cargo del modelo UX-UI que se capture. Si
el producto los necesita, se diseñan y se declaran, no se dan por heredados.

---

## 5. Esqueletos de referencia

### 5.1 Página base

```html
<!DOCTYPE html>
<html lang="es-AR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Panel de registros — Maqueta &lt;Proyecto&gt;-Web</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css">
<link rel="stylesheet" href="assets/css/Estilos-Maqueta.css">
</head>
<body class="mq-body"
      data-superficie="Panel-De-Registros" data-shell="trabajo"
      data-papel="rol-b" data-destino="registros" data-estado-inicial="con-datos">
<a class="mq-skip" href="#mq-main">Ir al contenido</a>

<div class="mq-shell">
  <nav class="mq-shell-sidebar" aria-label="Navegación principal" data-mq-sidebar></nav>
  <div class="mq-shell-contenido">
    <main id="mq-main" tabindex="-1">
      <!-- contenido de la superficie -->
    </main>
  </div>
</div>

<div data-mq-barra-validacion></div>

<script src="assets/js/Datos-Maqueta.js"></script>
<script>
window.renderSuperficie = function (M, D) { /* … */ };
window.alCambiarEstado = function (id) { /* … */ };
</script>
<script src="assets/js/Maqueta.js"></script>
</body>
</html>
```

Shell de acceso, para las superficies sin sesión:

```html
<div class="mq-lienzo">
  <main id="mq-main" class="mq-tarjeta-acceso">
    <span class="mq-identidad" data-mq-marca></span>
    <h1>Ingresar</h1>
    <!-- bandas de resultado, formulario -->
  </main>
  <div data-mq-sello-acceso></div>
</div>
```

### 5.2 ABM clásico — orden canónico de la superficie

Siempre en este orden vertical, y cada bloque con su `data-mq-estado`:

1. Encabezado: `h1` + subtítulo + acción primaria a la derecha.
2. Bandas de resultado, una por estado de acción.
3. Barra de filtros.
4. Bloque `cargando` con esqueletos.
5. Bloques `vacio` y `filtrado-sin-resultados`, **separados**.
6. Bloque `indisponible`.
7. Bloque `con-datos`: tabla y tarjetas apiladas, ambas en el DOM.
8. Los `&lt;dialog&gt;`, hermanos del shell y no hijos de él.

```html
<div class="mq-encabezado">
  <div>
    <h1>Registros</h1>
    <p class="mq-caption">Cada fila abre su vista de detalle.</p>
  </div>
  <a class="mq-btn mq-btn--primario mq-ml-auto" href="Alta-De-Registro.html">Nuevo registro</a>
</div>

<p class="mq-banda mq-banda--exito" role="status" data-mq-estado="exito">
  Registro guardado. Ya aparece en el listado.
</p>
<p class="mq-banda mq-banda--error" role="alert" data-mq-estado="error-operacion">
  No se pudo guardar el registro. Volvé a intentar en unos segundos.
</p>

<div class="mq-filtros" data-mq-estado="con-datos filtrado-sin-resultados reconectando">
  <div class="mq-campo mq-campo-busqueda">
    <label for="pr-buscar">Buscar por nombre o atributo</label>
    <span data-mq-ico-buscar aria-hidden="true"></span>
    <input class="mq-input" id="pr-buscar" type="search" placeholder="nombre o atributo">
  </div>
  <div class="mq-campo">
    <label for="pr-estado">Situación</label>
    <select class="mq-select" id="pr-estado">
      <option>todas</option><option>Pendiente</option>
      <option>Habilitada</option><option>Bloqueada</option>
    </select>
  </div>
</div>

<div data-mq-estado="cargando" aria-hidden="true">
  <div class="mq-esqueleto mq-esqueleto--fila"></div>
  <div class="mq-esqueleto mq-esqueleto--fila"></div>
  <div class="mq-esqueleto mq-esqueleto--fila"></div>
</div>

<section class="mq-vacio" data-mq-estado="vacio" aria-labelledby="pr-vacio-h">
  <span data-mq-ico-vacio aria-hidden="true"></span>
  <h2 id="pr-vacio-h">Todavía no hay registros</h2>
  <p>Cuando cargues el primero, va a aparecer acá con su situación.</p>
  <a class="mq-btn mq-btn--primario mq-mt-5" href="Alta-De-Registro.html">Cargar el primer registro</a>
</section>

<section class="mq-vacio" data-mq-estado="filtrado-sin-resultados" aria-labelledby="pr-filtro-h">
  <h2 id="pr-filtro-h">Ningún registro coincide con el filtro</h2>
  <p>Hay registros cargados; ninguno cumple lo que buscaste.</p>
  <button type="button" class="mq-btn mq-btn--secundario mq-mt-5">Limpiar el filtro</button>
</section>

<section class="mq-aviso-indisponible" data-mq-estado="indisponible" role="alert"
         aria-labelledby="pr-indisp-h">
  <h2 id="pr-indisp-h"><span data-mq-ico-alerta aria-hidden="true"></span> No pudimos traer los registros</h2>
  <p>El servicio no respondió. Lo que ves puede estar desactualizado.</p>
  <button type="button" class="mq-btn mq-btn--secundario mq-mt-3">Reintentar traer los registros</button>
</section>

<div data-mq-estado="con-datos reconectando">
  <div class="mq-tabla-envoltorio">
    <table class="mq-tabla">
      <caption class="mq-sr-only">Registros, con su situación y la operación que esa situación admite</caption>
      <thead>
        <tr>
          <th scope="col">Registro</th><th scope="col">Atributo</th>
          <th scope="col">Situación</th><th scope="col">Fecha de alta</th>
          <th scope="col" class="mq-td-acciones">Operaciones</th>
        </tr>
      </thead>
      <tbody data-mq-filas-registros></tbody>
    </table>
  </div>
  <div class="mq-tarjetas-apiladas" data-mq-tarjetas-registros role="list"></div>
</div>
```

Fila y tarjeta, armadas en el hook de la superficie:

```js
function fila(M, r) {
  return '<tr>' +
    '<th scope="row" class="mq-th-plano mq-th-plano--cuerpo">' +
      '<span class="mq-iniciales" aria-hidden="true">' + M.esc(r.iniciales) + '</span> ' +
      M.esc(r.nombre) + '</th>' +
    '<td>' + M.esc(r.atributo) + '</td>' +
    '<td>' + M.insignia(r.etiquetaEstado) + '</td>' +
    '<td class="mq-num">' + M.esc(r.fechaAlta) + '</td>' +
    '<td class="mq-td-acciones"><span class="mq-acciones-fila">' + acciones(M, r) + '</span></td>' +
  '</tr>';
}

function tarjeta(M, r) {
  return '<article class="mq-tarjeta-fila" role="listitem">' +
    '<div class="mq-tarjeta-fila-cabecera">' +
      '<h3 class="mq-body-strong">' + M.esc(r.nombre) + '</h3>' + M.insignia(r.etiquetaEstado) +
    '</div>' +
    '<p class="mq-caption mq-mt-2">' + M.esc(r.atributo) + ' · ' + M.esc(r.fechaAlta) + '</p>' +
    '<div class="mq-acciones-fila">' + acciones(M, r) + '</div>' +
  '</article>';
}

// Lo que el estado no admite no se dibuja, ni siquiera inhabilitado.
// Y la transición ofrecida es UNA, la que corresponde a la situación vigente.
var VERBO = { 'Pendiente': 'Habilitar', 'Habilitada': 'Bloquear', 'Bloqueada': 'Rehabilitar' };

function acciones(M, r) {
  var a = ['<a class="mq-btn mq-btn--secundario" href="' + M.hrefDetalle(r.id) + '">' +
           M.icono('abrir') + 'Abrir<span class="mq-sr-only"> «' + M.esc(r.nombre) + '»</span></a>'];
  if (r.operable) {
    a.push('<button type="button" class="mq-btn mq-btn--secundario" aria-label="' +
      M.esc(VERBO[r.etiquetaEstado] + ' el registro de ' + r.nombre) + '">' +
      M.esc(VERBO[r.etiquetaEstado]) + '</button>');
    a.push('<button type="button" class="mq-btn mq-btn--destructivo" data-mq-baja="' + r.id + '">' +
      M.icono('eliminar') + 'Dar de baja<span class="mq-sr-only"> «' + M.esc(r.nombre) + '»</span></button>');
  }
  return a.join('');
}
```

**Nombre accesible de las acciones de fila.** El texto visible dice el verbo; el nombre accesible dice
el verbo **y la fila**. Se logra con `aria-label` completo o con un `&lt;span class="mq-sr-only"&gt;` interno.
Sin eso, un lector de pantalla anuncia veinte botones «Abrir» indistinguibles.

### 5.3 Formulario de alta y edición

El alta **no es un modal**: es una superficie propia, con su encabezado, su acción de retorno y su
estado `enviando`.

```html
<form novalidate>
  <div class="mq-campo">
    <label for="ar-nombre">Nombre</label>
    <input class="mq-input" id="ar-nombre" type="text" autocomplete="off"
           aria-describedby="ar-nombre-req">
    <span class="mq-requisito" id="ar-nombre-req">Entre 3 y 60 caracteres.</span>
  </div>

  <div class="mq-campo">
    <label for="ar-atributo">Atributo</label>
    <input class="mq-input" id="ar-atributo" type="email" autocomplete="email"
           aria-describedby="ar-atributo-error">
    <span class="mq-requisito" id="ar-atributo-error" data-mq-estado="atributo-ya-registrado">
      Ese atributo ya está registrado.
    </span>
  </div>

  <div class="mq-acciones-pie">
    <a class="mq-btn mq-btn--secundario" href="Panel-De-Registros.html">Cancelar</a>
    <button type="button" class="mq-btn mq-btn--primario"
            data-mq-estado="con-datos error-entrada vacio">Guardar el registro</button>
    <button type="button" class="mq-btn mq-btn--primario" disabled data-mq-estado="enviando">
      <span class="mq-spinner"></span> Guardando…
    </button>
  </div>
</form>
```

Cuatro reglas del formulario: `label` visible con `for` —el placeholder nunca lo sustituye—;
`autocomplete` declarado; el requisito **antes del intento**, asociado por `aria-describedby`; y el
verbo del botón nombra la acción exacta, nunca «Enviar» ni «Aceptar».

En una superficie sin estado previo al que volver —el primer arranque— **no hay «Cancelar»**, y su
ausencia se declara en un comentario del marcado para que no se lea como olvido.

### 5.4 Ventana modal

```html
<dialog class="mq-dialogo" id="pr-dlg-baja" aria-labelledby="pr-dlg-h">
  <h2 id="pr-dlg-h">Dar de baja el registro de <span data-mq-dlg-nombre></span></h2>
  <p class="mq-banda mq-banda--atencion" id="pr-arrastre" data-mq-aviso-arrastre></p>

  <div class="mq-campo">
    <label for="pr-confirmacion">Para confirmar, escribí el atributo del registro:
      <strong data-mq-dlg-atributo></strong></label>
    <input class="mq-input" id="pr-confirmacion" type="text" autocomplete="off"
           aria-describedby="pr-arrastre">
  </div>

  <div class="mq-acciones-pie">
    <button type="button" class="mq-btn mq-btn--secundario" data-mq-cierra-dialogo>Cancelar</button>
    <button type="button" class="mq-btn mq-btn--destructivo" disabled data-mq-dlg-baja>Dar de baja</button>
  </div>
</dialog>
```

Cableado global, idempotente, que sirve a todos los diálogos de la maqueta:

```js
function activarDialogos(raiz) {
  $$('[data-mq-abre-dialogo]', raiz).forEach(function (boton) {
    if (boton.dataset.mqDlgCableado) { return; }   // se puede volver a llamar sin duplicar
    boton.dataset.mqDlgCableado = '1';
    boton.addEventListener('click', function () {
      var dlg = document.getElementById(boton.getAttribute('data-mq-abre-dialogo'));
      if (!dlg) { return; }
      dlg.returnValue = '';
      if (dlg.showModal) { dlg.showModal(); } else { dlg.setAttribute('open', ''); }
      var primero = $('input, button, [href]', dlg);
      if (primero) { primero.focus(); }
      dlg.addEventListener('close', function alVolver() {
        dlg.removeEventListener('close', alVolver);
        boton.focus();                              // el foco vuelve al control que lo abrió
      });
    });
  });
  $$('[data-mq-cierra-dialogo]', raiz).forEach(function (b) {
    if (b.dataset.mqDlgCableado) { return; }
    b.dataset.mqDlgCableado = '1';
    b.addEventListener('click', function () { b.closest('dialog').close(); });
  });
}
```

Habilitación del destructivo por confirmación escrita:

```js
campo.addEventListener('input', function () {
  confirmar.disabled = campo.value.trim() !== esperado;
});
```

Siete reglas del modal:

1. **Un `&lt;dialog&gt;` por acción, no por fila.** El disparador recibe `data-mq-abre-dialogo` desde el
   render de la fila, y el diálogo se repuebla con los datos de esa fila.
2. **Velo por `::backdrop` con token**, nunca un `&lt;div&gt;` de overlay propio.
3. **`aria-labelledby` al `&lt;h2&gt;`**; el aviso de consecuencia se asocia por `aria-describedby` a la
   acción destructiva o al campo de confirmación.
4. **Foco al primer control al abrir; foco de vuelta al disparador al cerrar.**
5. **Orden de botones fijo**: Cancelar primero, acción última. En pantalla angosta el pie invierte a
   `column-reverse`, con lo que la acción queda arriba y al alcance del pulgar.
6. **Dos grados de confirmación**: simple cuando la acción es reversible o acotada; escrita cuando
   arrastra dependientes, y en ese caso el aviso de arrastre es la descripción del campo.
7. **El modal confirma; no es un formulario de alta.** Un alta con más de dos campos es una superficie.

### 5.5 Asistente de varios niveles

**Sólo para actos divisibles y reanudables.** Para el acto indivisible —el primer arranque, el
aprovisionamiento— rige una superficie y un solo acto: un asistente ahí se abandona a la mitad y deja el
sistema en estado parcial.

Anatomía normada: círculo numerado por paso, conector entre pasos, etiqueta debajo; tres estados de paso
—pendiente en superficie secundaria, actual en marca con el número, completado en marca con tilde y la
línea anterior pintada—; contador «Paso X de N»; «Anterior» deshabilitado y sin eventos en el primer
paso; «Siguiente» que vira a la acción de confirmación en el último; y **paso final de revisión con
resumen en filas clave/valor**.

```html
<nav class="mq-pasos" aria-label="Progreso del asistente">
  <p class="mq-sr-only" role="status" aria-live="polite" data-mq-anuncio-paso></p>
  <ol class="mq-pasos-lista">
    <li class="mq-paso mq-paso--completado" data-mq-paso="1">
      <span class="mq-paso__marca" aria-hidden="true"></span>
      <span class="mq-paso__rotulo">Identificación</span>
    </li>
    <li class="mq-paso mq-paso--actual" data-mq-paso="2" aria-current="step">
      <span class="mq-paso__marca" aria-hidden="true">2</span>
      <span class="mq-paso__rotulo">Atributos</span>
    </li>
    <li class="mq-paso mq-paso--pendiente" data-mq-paso="3">
      <span class="mq-paso__marca" aria-hidden="true">3</span>
      <span class="mq-paso__rotulo">Vinculaciones</span>
    </li>
    <li class="mq-paso mq-paso--pendiente" data-mq-paso="4">
      <span class="mq-paso__marca" aria-hidden="true">4</span>
      <span class="mq-paso__rotulo">Revisión</span>
    </li>
  </ol>
  <p class="mq-caption" data-mq-contador-paso>Paso 2 de 4</p>
</nav>

<section data-mq-estado="paso-1" aria-labelledby="as-h1"><h2 id="as-h1">Identificación</h2>…</section>
<section data-mq-estado="paso-2" aria-labelledby="as-h2"><h2 id="as-h2">Atributos</h2>…</section>
<section data-mq-estado="paso-3" aria-labelledby="as-h3"><h2 id="as-h3">Vinculaciones</h2>…</section>

<section data-mq-estado="paso-4" aria-labelledby="as-h4">
  <h2 id="as-h4">Revisión</h2>
  <dl class="mq-kv" data-mq-resumen></dl>
  <div class="mq-campo mq-campo--conmutador">
    <input class="mq-conmutador" id="as-activar" type="checkbox" role="switch">
    <label for="as-activar">Dejar el registro activo al terminar</label>
  </div>
</section>

<div class="mq-acciones-pie">
  <button type="button" class="mq-btn mq-btn--secundario" data-mq-paso-anterior>Anterior</button>
  <button type="button" class="mq-btn mq-btn--primario"
          data-mq-estado="paso-1 paso-2 paso-3" data-mq-paso-siguiente>Siguiente</button>
  <button type="button" class="mq-btn mq-btn--primario"
          data-mq-estado="paso-4">Crear el registro</button>
  <button type="button" class="mq-btn mq-btn--primario" disabled data-mq-estado="enviando">
    <span class="mq-spinner"></span> Creando…
  </button>
</div>
```

Los pasos son estados de la superficie, con lo que **la barra de validación permite saltar a cualquier
paso directamente**, que es lo que hace verificable el asistente sin recorrerlo entero. El avance:

```js
window.alCambiarEstado = function (id) {
  var n = Number((id.match(/^paso-(\d)$/) || [])[1]);
  if (!n) { return; }
  M.$$('[data-mq-paso]').forEach(function (li) {
    var i = Number(li.dataset.mqPaso);
    li.className = 'mq-paso ' + (i < n ? 'mq-paso--completado'
                               : i === n ? 'mq-paso--actual' : 'mq-paso--pendiente');
    if (i === n) { li.setAttribute('aria-current', 'step'); }
    else { li.removeAttribute('aria-current'); }
  });
  M.$('[data-mq-contador-paso]').textContent = 'Paso ' + n + ' de 4';
  M.$('[data-mq-anuncio-paso]').textContent = 'Paso ' + n + ' de 4: ' + rotulo(n);
  M.$('[data-mq-paso-anterior]').disabled = (n === 1);
  if (n === 4) { pintarResumen(); }
  M.$('#mq-main').focus();          // el foco va al encabezado del paso nuevo
};
```

**Validación por paso**: la maqueta no valida; demuestra el estado `error-entrada` del paso, con el
mensaje asociado al campo. **Persistencia del borrador**: la maqueta no persiste nada del producto; si
el asistente es reanudable, se demuestra con un estado `borrador-recuperado` y su banda de acuse.

### 5.6 Presentación de datos

Cuatro formas, y el criterio para elegir entre ellas:

| Forma | Cuándo | Marcado |
| --- | --- | --- |
| Tabla | Colección homogénea que se compara columna a columna | `&lt;table class="mq-tabla"&gt;` con `&lt;caption class="mq-sr-only"&gt;`, `&lt;th scope="col"&gt;` y primera celda `&lt;th scope="row"&gt;` |
| Tarjetas apiladas | La misma colección en menos de 768px | `&lt;article class="mq-tarjeta-fila" role="listitem"&gt;` dentro de un `role="list"` |
| Ficha clave/valor | Una sola entidad, con sus campos | `&lt;dl class="mq-kv"&gt;` recorriendo el **contrato de campos**, no una lista escrita a mano |
| Árbol | Jerarquía navegable | `role="tree"` / `role="group"` / `role="treeitem"` |

La ficha se arma recorriendo `contratoDeCampos`, con lo que agregar un campo al modelo lo hace aparecer
en la ficha sin tocar la vista:

```js
var kv = M.$('[data-mq-kv]');
kv.innerHTML = D.contratoDeCampos.map(function (c) {
  var valor = c.campo === 'estado' ? M.insignia(registro.estado)
            : M.esc(String(registro[c.campo]));
  var clase = (c.tipo === 'numerico' || c.tipo === 'fecha') ? ' mq-num' : '';
  return '<div><dt class="mq-kv__clave">' + M.esc(c.etiqueta) + '</dt>' +
         '<dd class="mq-kv__valor' + clase + '">' + valor + '</dd></div>';
}).join('');
```

Del árbol, tres reglas que son las que más se rompen: **un solo portador de rol y de estado por nodo**
—el `&lt;li role="treeitem"&gt;` lleva `aria-expanded` y `aria-selected`, y su interior es un `&lt;span&gt;` de
presentación, porque con dos portadores el lector anuncia dos elementos por nodo—; **tabindex móvil**,
un solo nodo enfocable por vez; y **navegación y selección en funciones distintas**: flechas arriba y
abajo entre nodos visibles, Home y End a los extremos, derecha despliega, izquierda pliega, Enter y
Espacio seleccionan.

### 5.7 Barra de validación

Instrumento de la maqueta, no parte del producto, y rotulada como tal:

```js
'<p class="mq-barra-validacion__rotulo">' + icono('alerta', 16) +
'<span>Barra de validación de maqueta — no forma parte del producto</span></p>'
```

Tres controles: selector de estado poblado con los estados relevados del DOM; interruptor de recarga
automática; y retorno a la portada. La recarga cumple cinco condiciones: apagada por defecto y
**persistida en el navegador**; detección por comparación del identificador de versión del recurso
—`fetch` con `HEAD` sobre `ETag`, `Last-Modified` y `Content-Length`—, no por descarga completa;
intervalo de entre dos y cinco segundos; **suspensión cuando la pestaña no está visible**; y degradación
silenciosa sobre `file://`, donde el interruptor se muestra deshabilitado con la razón a la vista.

El estado se recuerda por superficie en la sesión y se puede fijar por dirección con
`Superficie.html?estado=<id>`.

---

## 6. Criterios de aceptación

Se verifica leyendo el árbol de la maqueta. `[enumerable]` se decide contando o comparando;
`[interpretativo]` se decide leyendo los dos lados.

- [ ] `[enumerable]` El layout de §2.1 está completo: los cuatro archivos obligatorios y `README.md`.
- [ ] `[enumerable]` Cada superficie tiene los cinco atributos del `&lt;body&gt;` de §3.1.
- [ ] `[enumerable]` El orden de los tres `&lt;script&gt;` de §2.2 es el declarado en todas las páginas.
- [ ] `[enumerable]` Ningún archivo HTML ni JavaScript lleva un atributo `style=` en línea.
- [ ] `[enumerable]` No hay literales de color, tipografía ni espaciado fuera del bloque `:root`.
- [ ] `[enumerable]` Ningún HTML hardcodea datos; toda colección sale de `Datos-Maqueta.js`.
- [ ] `[enumerable]` Cada superficie declara bloques para `vacio`, `cargando`, `con-datos` y el estado de error, o declara «No aplica» con su motivo.
- [ ] `[enumerable]` Cada registro del dataset lleva `origen`, y lo compuesto está marcado como tal.
- [ ] `[enumerable]` Todo `&lt;th&gt;` lleva `scope`, y toda `&lt;table&gt;` lleva `&lt;caption class="mq-sr-only"&gt;`.
- [ ] `[enumerable]` Todo control de formulario tiene `&lt;label for&gt;` visible.
- [ ] `[enumerable]` Todo `&lt;dialog&gt;` lleva `aria-labelledby` y su pie ordena Cancelar antes de la acción.
- [ ] `[enumerable]` La barra de validación lleva su rótulo literal y ofrece el interruptor de recarga apagado por defecto.
- [ ] `[interpretativo]` `filtrado-sin-resultados` está separado de `vacio`, con acciones distintas.
- [ ] `[interpretativo]` Ninguna acción no disponible se dibuja inhabilitada.
- [ ] `[interpretativo]` El nombre accesible de cada acción de fila desambigua la fila.
- [ ] `[interpretativo]` Cada acción de reintento nombra la acción concreta, no «Reintentar» a secas.
- [ ] `[interpretativo]` El foco vuelve al disparador al cerrar cada diálogo.
- [ ] `[interpretativo]` Un agente sin contexto previo puede producir una superficie nueva leyendo sólo este documento.

---

## 7. Anti-patrones

| Anti-patrón | Por qué | Qué hacer |
| --- | --- | --- |
| Datos de ejemplo dentro del HTML | La maqueta deja de servir para validar el modelo de datos, y cada corrección hay que hacerla N veces | Fuente única en `Datos-Maqueta.js` |
| Un `style=` en línea «por esta vez» | Es un literal visual ad hoc con otro nombre; el diseño se desalinea y no se puede capitalizar | Utilitaria con nombre que materialice un token |
| Un valor de color o espaciado nuevo escrito directo en una regla | Rompe la trazabilidad entre el diseño y la implementación | Promover el token al catálogo antes de usarlo |
| Agregar un paso de build «para hacerlo bien» | Rompe la edición manual del humano y ata la maqueta a un toolchain de vida corta | Estático, servido tal cual está en disco |
| Estado de superficie resuelto con una rama en JavaScript | El estado deja de ser relevable del DOM y desaparece de la barra de validación | Un bloque con su `data-mq-estado` |
| Un solo estado vacío para «no hay datos» y «el filtro no encontró nada» | Le miente al validador sobre qué pasó y ofrece la acción equivocada | Dos secciones separadas |
| Acción no disponible dibujada como control inhabilitado | Sugiere una capacidad que no existe y obliga a explicar por qué está apagada | No dibujarla |
| Las tres transiciones de estado ofrecidas a la vez en la fila | El usuario elige entre opciones que la situación no admite | Una sola transición, la que la situación vigente admite |
| Modal para el alta de una entidad | Un formulario de varios campos dentro de un modal no tiene estados propios ni URL, y no se puede validar por dirección | Superficie propia |
| Un `&lt;dialog&gt;` por fila | Multiplica el marcado y desincroniza el contenido | Uno por acción, repoblado desde la fila |
| Asistente multipaso para un acto indivisible | Se abandona a la mitad y deja el sistema en estado parcial | Una superficie, un acto; el resto se configura después |
| Botón con `disabled` alternado por script en lugar de dos botones por estado | El estado de envío deja de ser un estado de la superficie y no se puede exhibir | Dos botones conmutados por `data-mq-estado` |
| Placeholder en lugar de `label` | El rótulo se pierde al escribir | `label` visible con `for`, y placeholder de ejemplo |
| Requisito de validación que aparece recién al fallar | El usuario descubre la regla equivocándose | Declararlo antes del intento, asociado por `aria-describedby` |
| Insignia que comunica sólo con color | Falla en daltonismo y contra el criterio de un solo canal | Color más texto, siempre |
| Ícono raster o pack por CDN | No hereda el color, no escala y ata la maqueta a una red | SVG inline con `currentColor` |
| `&lt;li role="treeitem"&gt;` con un `&lt;button&gt;` interno que repite `aria-expanded` | El lector de pantalla anuncia dos elementos por nodo | Un solo portador de rol y de estado |
| Maqueta sin accesibilidad «porque es sólo una maqueta» | Enseña al validador humano a aprobar una superficie inaccesible | WCAG 2.2 AA como piso también acá |

---

## 8. Frontera con las reglas

Lo que sigue es **normativo del framework y no se decide en este documento**. Si algo de acá contradice
lo de allá, manda la regla:

| Tema | Archivo de reglas |
| --- | --- |
| Qué superficies se maquetan y con qué mínimo por tipo D8 | `Maqueta-Rules.md` §4.4 |
| Que la maqueta sea autónoma y sin llamadas de red; la fuente única de datos; los cuatro estados; el sello de versión; la iconografía SVG; WCAG 2.2 AA | `Maqueta-Rules.md` §4.2 a §4.7 |
| Criterios de aceptación de la maqueta como entregable y anti-patrones de proceso | `Maqueta-Rules.md` §8 y §9 |
| Los tokens semánticos, los diez patrones y el mapa canónico de estados | `Design-Rules-Web-Generico.md` §2, §4 y §5 |
| Anatomía del asistente, del shell, de la grilla de ABM y de la búsqueda | `Design-Rules-Web-Generico.md` §4.1 a §4.10 |
| Shell partido, catálogo de códigos de resultado, política de sesión | `Design-Rules-Acceso-Monousuario.md` |
| Acto indivisible, guard en tres capas, prohibición del asistente para el primer arranque | `Design-Rules-Primer-Arranque.md` |
| Identificadores `SUP-`, `CMP-`, `EST-`, `NAV-` y umbrales de deriva | `Deriva-Rules.md` §2 y §3 |
| Artefactos de la categoría 03 y su trazabilidad | `Rules-UX-UI-DX.md` |

**Desviación declarada.** Ninguna. Este documento **no sustituye** ningún ítem del piso: el stack que
describe es el que `Maqueta-Rules.md` §4.1 ya elige. Es una caracterización de esa elección, no un
reemplazo.

**Dos huecos del piso que este documento llena sin normar.** El catálogo de diseño no tiene patrón
agnóstico de diálogo modal ni reglas de paginación y ordenamiento. Lo que §5.4 y §5.6 describen es la
forma constructiva observada y lo que las reglas de accesibilidad exigen; **no es norma**, y si el
framework incorpora un patrón de modal, manda el framework.

---

## 9. Trazabilidad

| Vínculo | Valor |
| --- | --- |
| Índice al que pertenece | `Index-Knowledge.md` de la base que lo aloje |
| Documento hermano | `Knowledge-Template-Blazor-Interactive-Server-SDD-Default.md`, que hereda de éste |
| Consumidor declarado | Categoría 03, y el subagente de maqueta AG-00031 |
| Artefacto de referencia | Ninguno depositado. El template ejecutable del framework es `Templates/Modelo-Generico/` |
| Fuentes del relevamiento | `Maqueta-Rules.md`; `Design-Rules-Web-Generico.md`; `Design-Rules-Acceso-Monousuario.md`; `Design-Rules-Primer-Arranque.md`; `Design-Rules-Config-Esquema.md`; `Design-Rules-Identidad-De-Version.md`; `Rules-UX-UI-DX.md`; `Deriva-Rules.md`; `Templates/Modelo-Generico/`; una maqueta real generada por el framework, ofuscada según §0 |

---

## 10. Control de cambios

| Versión | Fecha | Cambios |
| --- | --- | --- |
| 1.0 | 2026-09-01 | Emisión inicial. Relevamiento del piso normativo de maqueta, del catálogo de diseño y de una maqueta real generada por el framework. |
