# Template Blazor Interactive Server puro — realización del template HTML del Framework SDD

**Alias:** Template-Blazor-Interactive-Server-SDD-Default
**Naturaleza:** propio
**Tema:** Realización del template HTML de maqueta como proyecto .NET Blazor Web App con render mode Interactive Server y sin librería de componentes: estructura, componentes propios por patrón, formularios, diálogos, asistentes y superficies de identidad fuera del circuito
**Consumidor:** 03, 05
**Condicion-de-carga:** proyectos de código `web-monolith` sobre stack .NET con interfaz Blazor Web App en render mode Interactive Server, sin librería de componentes de terceros
**Hereda-de:** Template-HTML-SDD-Default
**Sustituye:** —
**Compatible-con:** Rules-Base-Conocimiento.md 2.2
**Versión:** 1.0
**Estado:** Vigente
**Fecha:** 2026-09-01

---

## 0. Propósito y alcance

Este documento dice **cómo se lleva a Blazor Interactive Server, sin librería de componentes, el
template caracterizado en [[Template-HTML-SDD-Default]]**. Hereda de él y por lo tanto **escribe sólo el
delta**: los tokens, las anatomías de patrón, el vocabulario de estados, las convenciones de nombre de
clase, los anti-patrones de diseño y los criterios de accesibilidad **no se repiten acá**. Lo que sigue
es qué cambia de forma cuando el que renderiza es un componente Razor sobre un circuito, y qué hay que
resolver que en HTML plano no existía.

**Qué queda explícitamente afuera:**

| Fuera de alcance | Dónde vive |
| --- | --- |
| Tokens, patrones visuales, estados, accesibilidad y anti-patrones de diseño | [[Template-HTML-SDD-Default]] y el catálogo de diseño del framework |
| Arquitectura interna de la solución: capas, acceso a datos, servicios de aplicación | Categoría 05, y el conocimiento de arquitectura que el producto cite |
| Esquema de credenciales, hash del secreto, control de intentos, protección antifalsificación | Categoría 05, postura de seguridad |
| Despliegue, ambientes, variables previas a la primera pantalla, versionado del artefacto | Categoría 09 |
| El qué funcional y sus casos de uso | Categoría 02 |
| Pruebas automatizadas de la interfaz | Categoría 08 |

**Omisiones declaradas.** §5 supera el techo de `Rules-Base-Conocimiento.md` §6.2 sumado al resto del
documento, y se acoge a la excepción de §4.3: los esqueletos Razor son la única forma de transmitir el
reparto entre marcado, ciclo de vida y servicios sin pérdida.

**Verificación de ofuscación.** Los ejemplos usan entidades neutras —`Registro`, `Elemento`, `Usuario`—
con identificadores `REG-0001`, y el espacio de nombres genérico `Producto.Web`. No hay nombres de
clientes, de instituciones ni de personas, ni cadenas de conexión, ni rutas de servicios internos.
Falso positivo léxico declarado: la palabra **«Producto»** aparece como raíz de espacio de nombres
neutra y como término del framework —«la unidad de trabajo es el producto»—, y en ningún caso designa un
producto comercial concreto.

---

## 1. Identidad del artefacto

| Rasgo | Valor |
| --- | --- |
| Qué es | Un proyecto .NET Blazor Web App que realiza el template HTML como componentes Razor propios |
| Render mode | `InteractiveServer` por página interactiva. **Las superficies de identidad quedan en SSR estático** |
| Librería de componentes | **Ninguna.** El patrón vive en componentes Razor propios del producto |
| Sistema de estilos | La misma hoja de tokens de la maqueta, servida desde `wwwroot`. Sin recompilación de estilos |
| Marcado | El mismo que la maqueta, con las mismas clases `mq-` |
| Estado de UI | En el componente o en servicios `Scoped` del circuito. **Sin `localStorage` ni `sessionStorage` improvisados** |

**Por qué sin librería de componentes.** Es una decisión del que adopta este conocimiento, y tiene tres
consecuencias que conviene tener a la vista antes de aceptarla:

1. **Se elimina el salto de tecnología entre la validación y la implementación.** La maqueta que el
   humano aprueba ya es HTML plano con esas clases; con componentes propios, el marcado aprobado se
   traslada literal en vez de traducirse a la API de una librería.
2. **Se pierde lo que la librería daba gratis**, y es exactamente la parte cara: la grilla con filtro,
   orden y paginación; el asistente; el diálogo con confinamiento de foco; el aviso emergente; y el
   recorrido por teclado con ARIA correcto de todos ellos. Hay que escribirlo, y la accesibilidad es la
   dimensión que **bloquea** en el sensado de deriva.
3. **El patrón tiene que vivir en un solo lugar igual.** La regla que el framework fija para el caso con
   librería —componentes Razor propios que envuelven, para que el patrón viva en un solo lugar— se
   aplica idéntica: lo único que cambia es qué hay adentro del componente.

---

## 2. Estructura

### 2.1 Del árbol de la maqueta al árbol del proyecto

| Pieza de la maqueta | Dónde va en el proyecto |
| --- | --- |
| `assets/css/Estilos-Maqueta.css`, bloque `:root` | `wwwroot/css/Tokens.css`, **copiado sin cambios**, servido con un `&lt;link&gt;` en `App.razor` |
| `assets/css/Estilos-Maqueta.css`, resto | `wwwroot/css/Componentes.css`, o CSS aislado por componente cuando la regla es exclusiva de él |
| Diccionario `ICONOS` de `Maqueta.js` | `Theme/Iconos.cs`, constantes `string` con el trazo SVG, importadas en `_Imports.razor` |
| `Datos-Maqueta.js` | **No viaja.** Los datos salen de los servicios de aplicación; el contrato de campos que la maqueta exhibía queda documentado en 03 |
| Conmutador `data-mq-estado` | Una propiedad `EstadoDeSuperficie` en el componente, y `@if` por bloque |
| Hooks `renderSuperficie` / `alCambiarEstado` | El ciclo de vida del componente y el `set` de la propiedad de estado |
| Barra de validación y recarga automática | **No viajan.** Son instrumentos de la maqueta |
| Una superficie HTML | Un `.razor` de página con su `@page` y su `@rendermode` |

### 2.2 Estructura de carpetas

El framework norma tres archivos —el tema, los íconos y su importación global— y nada más. El resto de
este árbol es decisión de este documento, declarada como tal:

```text
Producto.Web/
├── Program.cs                        composición: el único lugar donde se registran los servicios
├── _Imports.razor                    using globales, incluido Theme
├── App.razor                         documento raíz: <head>, <link> de tokens, <HeadOutlet>
├── Routes.razor                      Router, AuthorizeRouteView, layout por defecto
├── Theme/
│   ├── Iconos.cs                     trazos SVG como constantes string
│   └── RolesDeIcono.cs               tamaños por rol: 24 navegación, 20 tarjeta, 16 inline, 15 fila
├── Layout/
│   ├── MainLayout.razor              shell de trabajo: barra lateral, contenido, sello, hosts
│   ├── AccesoLayout.razor            shell de acceso: lienzo, tarjeta angosta, sello
│   └── BarraLateral.razor
├── Componentes/                      un componente por patrón del catálogo
│   ├── Grilla.razor / Grilla.razor.cs
│   ├── FilaDeAcciones.razor
│   ├── Insignia.razor
│   ├── Banda.razor
│   ├── EstadoVacio.razor
│   ├── EstadoIndisponible.razor
│   ├── Esqueleto.razor
│   ├── Dialogo.razor
│   ├── DialogoHost.razor
│   ├── AvisoHost.razor
│   ├── Asistente.razor / PasoDeAsistente.razor
│   ├── Conmutador.razor
│   ├── Icono.razor
│   └── SelloDeVersion.razor
├── Paginas/
│   ├── Registros/ Listado.razor, Detalle.razor, Alta.razor
│   └── Identidad/ Ingreso.razor, Aprovisionamiento.razor    (SSR estático)
├── Endpoints/
│   └── IdentidadEndpoints.cs         POST de ingreso, de cambio de secreto y de cierre de sesión
├── Servicios/
│   ├── IServicioDeDialogos.cs / ServicioDeDialogos.cs       Scoped
│   ├── IServicioDeAvisos.cs / ServicioDeAvisos.cs           Scoped
│   └── IIdentidadDeVersion.cs                               Singleton
└── wwwroot/css/Tokens.css, Componentes.css
```

**Separación `.razor` / `.razor.cs`.** Decisión de este documento: un componente lleva code-behind
cuando su bloque `@code` supera unas veinte líneas o tiene estado propio; si no, el bloque `@code` en el
mismo archivo. El criterio de fondo es el mismo que reparte `Maqueta.js` y el `&lt;script&gt;` de página en el
template HTML: lo que se comparte se separa, lo exclusivo queda al lado de su marcado.

### 2.3 Las tres capas de guard

Redundantes a propósito, todas contra el mismo predicado, y ninguna expone por qué rechazó:

| Capa | Dónde se implementa | Qué corta | Por qué no alcanza sola |
| --- | --- | --- | --- |
| Ruteo | `AuthorizeRouteView` en `Routes.razor` más un `NavigationManager.NavigateTo(destino, replace: true)` en el layout | Navegación a superficie protegida sin sesión ni aprovisionamiento | No cubre la entrada directa por URL a la superficie de aprovisionamiento |
| Superficie | `OnInitializedAsync` del componente de la superficie | Apertura fuera de tiempo, en los dos sentidos | Vive en el cliente; no protege el envío |
| Acción | El endpoint POST, del lado del servidor | Envío fuera de tiempo | Es el único no evitable, pero llega tarde para orientar |

El guard de la acción, ante un intento fuera de tiempo, **redirige a la superficie correcta en vez de
devolver un error**. Y la navegación de resolución **reemplaza la entrada del historial** —`replace:
true`— para que el botón de retroceso no devuelva a un limbo.

---

## 3. Contrato de uso

### 3.1 Render mode: qué es interactivo y qué no

| Superficie | Render mode | Motivo |
| --- | --- | --- |
| Listado, detalle, alta, asistente, configuración | `@rendermode InteractiveServer` | Necesitan reaccionar sin recargar |
| Ingreso, alta de identidad, cambio de secreto, aprovisionamiento inicial | **SSR estático, sin `@rendermode`** | Emiten la credencial de sesión en el ciclo de request |
| Componentes puramente presentacionales | Sin render mode propio | No abren circuito |

**La regla que gobierna todo el bloque de identidad**, y la que más se rompe: los formularios de
identidad y de aprovisionamiento **se envían por POST a endpoints, no por interactividad de
componente**. La credencial de sesión se emite en el ciclo de request, **fuera del circuito de render
interactivo**: una vez que el circuito está establecido, la respuesta HTTP ya se envió y no hay dónde
escribir la cabecera que crea la cookie. En consecuencia:

- Los campos son `&lt;input&gt;` **nativos**, con `autocomplete` declarado y token antifalsificación.
- El formulario se marca para que la navegación mejorada **no lo intercepte**.
- **El cierre de sesión es un `form` POST con el botón adentro, no un enlace de navegación**: muta
  estado y se envía como tal.
- La superficie de acceso vive en el shell de acceso; la transición al shell de trabajo es una
  navegación completa, no un cambio de estado.

### 3.2 Higiene del circuito

| Regla | Cómo se cumple |
| --- | --- |
| Toda acción que viaja al servidor muestra «cargando» | La superficie entra en su estado `Enviando` antes del `await` |
| Toda acción primaria previene el doble envío | `disabled="@_procesando"` en el botón, seteado antes del `await` y liberado en `finally` |
| Sin almacenamiento de navegador improvisado | El estado de UI vive en el componente o en un servicio `Scoped` del circuito |
| Evitar lógica pesada en el render | El trabajo va al ciclo de vida o al manejador; `StateHasChanged` con criterio |
| Comunicación hijo a padre | `EventCallback`, nunca un evento propio ni un servicio de mensajería para eso |
| La UI de reconexión se estiliza acorde a la marca | Se reemplaza el marcado por defecto por el bloque `mq-banda--atencion` con `role="status"` |
| Los recursos del circuito se liberan | `IAsyncDisposable` en todo componente que suscriba a un servicio o abra un temporizador |

**Prerrenderizado.** El framework no lo norma. Decisión de este documento: **prerrenderizado activo**,
con la consecuencia asumida de que la carga de datos del ciclo de vida corre dos veces. El componente lo
tolera porque su carga es idempotente y sin efectos; cuando no puede serlo, se persiste el resultado del
prerrenderizado en lugar de apagarlo por página.

### 3.3 Estado de superficie

El `data-mq-estado` del template HTML se realiza como un enumerado y un `@if` por bloque. **El
vocabulario de estados es el mismo**, sin agregados ni recortes.

```csharp
public enum EstadoDeSuperficie
{
    Cargando, Vacio, FiltradoSinResultados, ConDatos, Indisponible,
    Enviando, ErrorDeEntrada, ErrorDeOperacion, Exito, Reconectando
}
```

Dos reglas que se heredan y hay que sostener a mano: `FiltradoSinResultados` sigue siendo un estado
**distinto** de `Vacio`, con su propia acción; y una superficie sin colección declara su ausencia de
estado vacío en un comentario del marcado, para que se lea deliberada.

### 3.4 Servicios y su ciclo

| Servicio | Ciclo | Qué hace |
| --- | --- | --- |
| `IServicioDeDialogos` | `Scoped` | Abre un diálogo y devuelve el resultado esperado por el llamador |
| `IServicioDeAvisos` | `Scoped` | Encola avisos efímeros que `AvisoHost` publica en una región activa |
| `IIdentidadDeVersion` | `Singleton` | Resuelve la versión legible y el identificador de construcción **en el punto de composición del host** |
| Servicios de aplicación del producto | `Scoped` | Los que la arquitectura de 05 defina |

**Todo servicio se registra en `Program.cs` y en ningún otro lado.** El sello de versión toma su valor
del contrato resuelto en el host: **el componente no lo compone ni lo lee de una constante de la vista**,
y se exhibe en dos lugares obligatorios —la superficie de acceso y una superficie del sistema en
funcionamiento—.

### 3.5 Validación de formularios

Decisión de este documento, porque el framework no la norma: `EditForm` con `EditContext` explícito y
`DataAnnotationsValidator`, mensajes por campo con `ValidationMessage`, y **sin resumen de validación**
—el resumen desasocia el error de su campo, y la regla heredada es que el error se asocia al control por
`aria-describedby` y se anuncia—.

Tres cosas que la validación de interfaz **no** es:

1. **No es la que decide.** La validación que decide si la operación se concreta vive en el servicio de
   aplicación, contra la misma política que la superficie enuncia. La de la superficie es de
   conveniencia.
2. **No transcribe la política.** El requisito que se muestra bajo el campo se deriva de la política; no
   se escribe a mano en la vista, y se declara **antes del intento**.
3. **No expone parámetros de la política.** Los mensajes de resultado salen de un catálogo de códigos
   estables; un código sin entrada cae en un mensaje genérico, nunca en el código crudo ni en la traza.
   Y el rechazo de credenciales es indiferenciado por diseño.

---

## 4. Decisiones ya tomadas

| Bifurcación | Qué resuelve este documento | Criterio |
| --- | --- | --- |
| Librería de componentes vs. componentes propios | Componentes propios, uno por patrón del catálogo | El marcado aprobado en la maqueta se traslada literal; el patrón vive en un solo lugar igual |
| Tokens en C# tipado vs. tokens en CSS | En CSS, la misma hoja de la maqueta, copiada sin cambios | Elimina la doble indirección y hace que la maqueta y el producto compartan la fuente literal |
| Estilos globales vs. CSS aislado | Tokens y componentes en `wwwroot`; CSS aislado sólo para lo exclusivo de un componente | Las clases `mq-` son compartidas por definición |
| Render mode global vs. por página | Por página, y las de identidad sin render mode | La cookie se emite en el ciclo de request |
| Cierre de sesión como enlace vs. como POST | POST con el botón adentro | Muta estado; un enlace no |
| Prerrenderizado activo vs. apagado | Activo, con carga idempotente | Apagarlo por página degrada la primera pintura de todo el producto |
| Estado en `localStorage` vs. en el circuito | En el componente o en servicios `Scoped` | Regla heredada del framework |
| `EditForm` vs. manejo manual del formulario | `EditForm` con `EditContext` y anotaciones | Es el mecanismo nativo; evitarlo obliga a reescribir el seguimiento de campos |
| Resumen de validación vs. mensaje por campo | Por campo | El error se asocia al control y se anuncia; el resumen lo desasocia |
| Grilla genérica vs. tabla por página | Componente `Grilla&lt;T&gt;` genérico | Filtro, orden y estados en un solo lugar; escribirlo por página garantiza deriva |
| Diálogo por servicio vs. diálogo declarado en la página | Por servicio, con un host único en el layout | El diálogo se abre desde donde ocurre la acción, y su marcado vive una sola vez |
| `&lt;dialog&gt;` nativo vs. superposición propia | `&lt;dialog&gt;` nativo con interoperabilidad mínima | Trae confinamiento de foco y cierre por Escape; escribirlos a mano es donde se pierde la accesibilidad |
| Asistente con estado en el circuito vs. en la URL | En el circuito, con el paso reflejado en la URL | El paso tiene que ser direccionable para poder verificarse |

---

## 5. Esqueletos de referencia

### 5.1 Documento raíz y ruteo

```razor
@* App.razor *@
<!DOCTYPE html>
<html lang="es-AR">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <base href="/" />
    <link rel="stylesheet" href="css/Tokens.css" />
    <link rel="stylesheet" href="css/Componentes.css" />
    <HeadOutlet />
</head>
<body class="mq-body">
    <a class="mq-skip" href="#mq-main">Ir al contenido</a>
    <Routes />
    <script src="_framework/blazor.web.js"></script>
</body>
</html>
```

```razor
@* Routes.razor *@
<Router AppAssembly="typeof(Program).Assembly">
    <Found Context="ruta">
        <AuthorizeRouteView RouteData="ruta" DefaultLayout="typeof(Layout.MainLayout)">
            <NotAuthorized>
                @* Guard de ruteo: redirección neutra, sin decir por qué *@
                <Redireccion Destino="/ingreso" />
            </NotAuthorized>
        </AuthorizeRouteView>
        <FocusOnNavigate RouteData="ruta" Selector="#mq-main" />
    </Found>
</Router>
```

### 5.2 Los dos layouts

```razor
@* Layout/MainLayout.razor — shell de trabajo *@
@inherits LayoutComponentBase

<div class="mq-shell">
    <BarraLateral />
    <div class="mq-shell-contenido">
        <main id="mq-main" tabindex="-1">@Body</main>
        <SelloDeVersion Ubicacion="Ubicacion.Pie" />
    </div>
</div>

<DialogoHost />
<AvisoHost />

<div class="mq-banda mq-banda--atencion" role="status" id="components-reconnect-modal">
    Se perdió la conexión con el servicio. Estamos reconectando; lo que escribiste sigue acá.
</div>
```

```razor
@* Layout/AccesoLayout.razor — shell de acceso, sin navegación *@
@inherits LayoutComponentBase

<div class="mq-lienzo">
    <main id="mq-main" class="mq-tarjeta-acceso" tabindex="-1">
        <span class="mq-identidad"><Icono Nombre="@Iconos.Marca" Tamanio="20" /> Producto</span>
        @Body
    </main>
    <SelloDeVersion Ubicacion="Ubicacion.Lienzo" />
</div>
```

**La superficie sin chrome conserva su encabezado de primer nivel**: la ausencia de navegación no puede
dejar la página sin estructura semántica.

### 5.3 Componente de ícono

```razor
@* Componentes/Icono.razor *@
@if (string.IsNullOrEmpty(Titulo))
{
    <svg xmlns="http://www.w3.org/2000/svg" width="@Tamanio" height="@Tamanio" viewBox="0 0 24 24"
         fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round"
         stroke-linejoin="round" aria-hidden="true" focusable="false">@((MarkupString)Nombre)</svg>
}
else
{
    <svg xmlns="http://www.w3.org/2000/svg" width="@Tamanio" height="@Tamanio" viewBox="0 0 24 24"
         fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round"
         stroke-linejoin="round" role="img"><title>@Titulo</title>@((MarkupString)Nombre)</svg>
}

@code {
    [Parameter, EditorRequired] public string Nombre { get; set; } = default!;
    [Parameter] public int Tamanio { get; set; } = 16;
    [Parameter] public string? Titulo { get; set; }   // con título es significativo; sin título, decorativo
}
```

### 5.4 ABM clásico

```razor
@* Paginas/Registros/Listado.razor *@
@page "/registros"
@rendermode InteractiveServer
@inject IServicioDeRegistros Servicio
@inject IServicioDeDialogos Dialogos
@inject IServicioDeAvisos Avisos

<PageTitle>Registros</PageTitle>

<div class="mq-encabezado">
    <div>
        <h1>Registros</h1>
        <p class="mq-caption">Cada fila abre su vista de detalle.</p>
    </div>
    <a class="mq-btn mq-btn--primario mq-ml-auto" href="/registros/alta">Nuevo registro</a>
</div>

<p class="mq-sr-only" role="status" aria-live="polite">@_anuncio</p>

@if (_estado is EstadoDeSuperficie.Indisponible)
{
    <EstadoIndisponible Titulo="No pudimos traer los registros"
                        Cuerpo="El servicio no respondió. Lo que ves puede estar desactualizado."
                        AccionRotulo="Reintentar traer los registros"
                        AlReintentar="CargarAsync" />
}
else
{
    <div class="mq-filtros">
        <div class="mq-campo mq-campo-busqueda">
            <label for="f-buscar">Buscar por nombre o atributo</label>
            <Icono Nombre="@Iconos.Buscar" />
            <input class="mq-input" id="f-buscar" type="search" placeholder="nombre o atributo"
                   value="@_texto" @oninput="AlBuscar" />
        </div>
        <div class="mq-campo">
            <label for="f-estado">Situación</label>
            <select class="mq-select" id="f-estado" @bind="_situacion" @bind:after="Refiltrar">
                <option value="">todas</option>
                @foreach (var s in Situaciones) { <option value="@s">@s</option> }
            </select>
        </div>
    </div>

    <Grilla TItem="Registro" Items="_visibles" Estado="_estado"
            TituloAccesible="Registros, con su situación y la operación que esa situación admite">
        <Columnas>
            <ColumnaDeGrilla TItem="Registro" Titulo="Registro" EsEncabezadoDeFila="true">
                <Plantilla Context="r">
                    <span class="mq-iniciales" aria-hidden="true">@r.Iniciales</span> @r.Nombre
                </Plantilla>
            </ColumnaDeGrilla>
            <ColumnaDeGrilla TItem="Registro" Titulo="Atributo">
                <Plantilla Context="r">@r.Atributo</Plantilla>
            </ColumnaDeGrilla>
            <ColumnaDeGrilla TItem="Registro" Titulo="Situación">
                <Plantilla Context="r"><Insignia Valor="@r.EtiquetaEstado" /></Plantilla>
            </ColumnaDeGrilla>
            <ColumnaDeGrilla TItem="Registro" Titulo="Fecha de alta" EsNumerica="true">
                <Plantilla Context="r">@r.FechaAlta</Plantilla>
            </ColumnaDeGrilla>
        </Columnas>
        <Acciones Context="r">
            <a class="mq-btn mq-btn--secundario" href="/registros/@r.Id">
                <Icono Nombre="@Iconos.Abrir" Tamanio="15" />Abrir
                <span class="mq-sr-only"> «@r.Nombre»</span></a>
            @if (r.Operable)
            {
                <button type="button" class="mq-btn mq-btn--secundario"
                        aria-label="@($"{Verbo(r)} el registro de {r.Nombre}")"
                        @onclick="() => TransicionarAsync(r)">@Verbo(r)</button>
                <button type="button" class="mq-btn mq-btn--destructivo"
                        @onclick="() => DarDeBajaAsync(r)">
                    <Icono Nombre="@Iconos.Eliminar" Tamanio="15" />Dar de baja
                    <span class="mq-sr-only"> «@r.Nombre»</span></button>
            }
        </Acciones>
        <Vacio>
            <EstadoVacio Titulo="Todavía no hay registros"
                         Cuerpo="Cuando cargues el primero, va a aparecer acá con su situación."
                         AccionRotulo="Cargar el primer registro" AccionHref="/registros/alta" />
        </Vacio>
        <SinResultados>
            <EstadoVacio Titulo="Ningún registro coincide con el filtro"
                         Cuerpo="Hay registros cargados; ninguno cumple lo que buscaste."
                         AccionRotulo="Limpiar el filtro" AlAccionar="LimpiarFiltro" />
        </SinResultados>
    </Grilla>
}
```

```csharp
// Paginas/Registros/Listado.razor.cs
public partial class Listado : ComponentBase
{
    private EstadoDeSuperficie _estado = EstadoDeSuperficie.Cargando;
    private IReadOnlyList<Registro> _todos = [];
    private IReadOnlyList<Registro> _visibles = [];
    private string _texto = "", _situacion = "", _anuncio = "";

    // La transición ofrecida es UNA: la que la situación vigente admite.
    private static readonly Dictionary<string, string> Verbos = new()
    { ["Pendiente"] = "Habilitar", ["Habilitada"] = "Bloquear", ["Bloqueada"] = "Rehabilitar" };

    private static string Verbo(Registro r) => Verbos.GetValueOrDefault(r.EtiquetaEstado, "Revisar");

    protected override Task OnInitializedAsync() => CargarAsync();

    private async Task CargarAsync()
    {
        _estado = EstadoDeSuperficie.Cargando;
        _anuncio = "Cargando los registros.";
        try
        {
            _todos = await Servicio.ListarAsync();
            Refiltrar();
        }
        catch (ServicioNoDisponibleException)
        {
            _estado = EstadoDeSuperficie.Indisponible;
            _anuncio = "No pudimos traer los registros.";
        }
    }

    private void Refiltrar()
    {
        _visibles = _todos
            .Where(r => string.IsNullOrEmpty(_situacion) || r.EtiquetaEstado == _situacion)
            .Where(r => string.IsNullOrEmpty(_texto)
                        || r.Nombre.Contains(_texto, StringComparison.OrdinalIgnoreCase)
                        || r.Atributo.Contains(_texto, StringComparison.OrdinalIgnoreCase))
            .ToList();

        // Vacío de colección y vacío de filtrado son estados distintos, con acciones distintas.
        _estado = _todos.Count == 0 ? EstadoDeSuperficie.Vacio
                : _visibles.Count == 0 ? EstadoDeSuperficie.FiltradoSinResultados
                : EstadoDeSuperficie.ConDatos;

        _anuncio = _estado switch
        {
            EstadoDeSuperficie.Vacio => "Todavía no hay registros.",
            EstadoDeSuperficie.FiltradoSinResultados => "Ningún registro coincide con el filtro.",
            _ => $"Se muestran {_visibles.Count} registros de {_todos.Count}."
        };
    }

    private async Task DarDeBajaAsync(Registro r)
    {
        var arrastre = await Servicio.ContarDependientesAsync(r.Id);
        var confirmado = await Dialogos.ConfirmarConEscrituraAsync(new PedidoDeConfirmacion(
            Titulo: $"Dar de baja el registro de {r.Nombre}",
            Aviso: arrastre > 0
                ? $"La baja arrastra {arrastre} elementos vinculados. La operación no se deshace."
                : "La operación no se deshace.",
            RotuloDelCampo: "Para confirmar, escribí el atributo del registro:",
            ValorEsperado: r.Atributo,
            RotuloDeAccion: "Dar de baja"));

        if (!confirmado) { return; }

        await Servicio.DarDeBajaAsync(r.Id);
        Avisos.Exito($"El registro de {r.Nombre} quedó dado de baja.");
        await CargarAsync();
    }
}
```

**Lo que el estado no admite no se dibuja, ni siquiera inhabilitado**, y el nombre accesible de cada
acción desambigua la fila: las dos reglas se heredan del template HTML y acá se sostienen con
`aria-label` y con `mq-sr-only`.

El componente `Grilla&lt;T&gt;` concentra el marcado de tabla y tarjetas apiladas, con `&lt;caption
class="mq-sr-only"&gt;`, `&lt;th scope="col"&gt;` en el encabezado y `&lt;th scope="row"&gt;` en la primera celda de
cada fila. La conmutación entre tabla y tarjetas la sigue haciendo el único punto de quiebre del CSS:
**cambiar el tipo de presentación es deriva mayor**, así que las dos formas conviven en el marcado igual
que en la maqueta.

### 5.5 Formulario

```razor
@page "/registros/alta"
@rendermode InteractiveServer

<EditForm EditContext="_contexto" OnValidSubmit="GuardarAsync" FormName="alta-de-registro">
    <DataAnnotationsValidator />

    <div class="mq-campo">
        <label for="a-nombre">Nombre</label>
        <InputText class="mq-input" id="a-nombre" @bind-Value="_modelo.Nombre"
                   autocomplete="off" aria-describedby="a-nombre-req" />
        <span class="mq-requisito" id="a-nombre-req">@Politica.RequisitoDeNombre</span>
        <ValidationMessage For="() => _modelo.Nombre" class="mq-error-inline" />
    </div>

    <div class="mq-campo">
        <label for="a-atributo">Atributo</label>
        <InputText class="mq-input" id="a-atributo" type="email" @bind-Value="_modelo.Atributo"
                   autocomplete="email" aria-describedby="a-atributo-req" />
        <span class="mq-requisito" id="a-atributo-req">@Politica.RequisitoDeAtributo</span>
        <ValidationMessage For="() => _modelo.Atributo" class="mq-error-inline" />
    </div>

    <div class="mq-acciones-pie">
        <a class="mq-btn mq-btn--secundario" href="/registros">Cancelar</a>
        <button type="submit" class="mq-btn mq-btn--primario" disabled="@_procesando">
            @if (_procesando) { <span class="mq-spinner"></span><text> Guardando…</text> }
            else { <text>Guardar el registro</text> }
        </button>
    </div>
</EditForm>
```

```csharp
private async Task GuardarAsync()
{
    if (_procesando) { return; }
    _procesando = true;                       // se setea ANTES del await: previene el doble envío
    try
    {
        await Servicio.CrearAsync(_modelo);
        Avisos.Exito("Registro guardado. Ya aparece en el listado.");
        Navegacion.NavigateTo("/registros");
    }
    catch (OperacionRechazadaException ex)
    {
        _codigoDeError = ex.Codigo;           // el texto sale del catálogo, no de la excepción
    }
    finally { _procesando = false; }
}
```

El requisito bajo el campo **se deriva de la política y se muestra antes del intento**; el mensaje de
error sale del catálogo de códigos y nunca lleva la traza ni el detalle técnico. El verbo del botón
nombra la acción exacta.

### 5.6 Diálogo

```razor
@* Componentes/Dialogo.razor *@
<dialog class="mq-dialogo" @ref="_dialogo" aria-labelledby="@_idTitulo">
    <h2 id="@_idTitulo">@Titulo</h2>
    @if (!string.IsNullOrEmpty(Aviso))
    {
        <p class="mq-banda mq-banda--atencion" id="@_idAviso">@Aviso</p>
    }
    @if (PideEscritura)
    {
        <div class="mq-campo">
            <label for="@_idCampo">@RotuloDelCampo <strong>@ValorEsperado</strong></label>
            <input class="mq-input" id="@_idCampo" type="text" autocomplete="off"
                   aria-describedby="@_idAviso" value="@_escrito"
                   @oninput="e => _escrito = e.Value?.ToString() ?? string.Empty" />
        </div>
    }
    <div class="mq-acciones-pie">
        <button type="button" class="mq-btn mq-btn--secundario" @onclick="() => CerrarAsync(false)">
            Cancelar</button>
        <button type="button" class="mq-btn mq-btn--destructivo"
                disabled="@(PideEscritura && _escrito.Trim() != ValorEsperado)"
                @onclick="() => CerrarAsync(true)">@RotuloDeAccion</button>
    </div>
</dialog>
```

```csharp
// Abrir y cerrar pasan por una interoperabilidad mínima, porque showModal() no tiene equivalente
// administrado. Lo que se gana a cambio es el confinamiento de foco y el cierre por Escape nativos.
private async Task AbrirAsync()  => await Js.InvokeVoidAsync("mqDialogo.abrir", _dialogo);
private async Task CerrarAsync(bool resultado)
{
    await Js.InvokeVoidAsync("mqDialogo.cerrar", _dialogo);   // devuelve el foco al disparador
    await AlCerrar.InvokeAsync(resultado);
}
```

```js
// wwwroot/js/mq-dialogo.js — lo mínimo que no se puede escribir en C#
window.mqDialogo = {
  abrir: function (dlg) {
    dlg.__mqDisparador = document.activeElement;
    if (dlg.showModal) { dlg.showModal(); } else { dlg.setAttribute('open', ''); }
    var primero = dlg.querySelector('input, button, [href]');
    if (primero) { primero.focus(); }
  },
  cerrar: function (dlg) {
    if (dlg.close) { dlg.close(); } else { dlg.removeAttribute('open'); }
    if (dlg.__mqDisparador) { dlg.__mqDisparador.focus(); }
  }
};
```

Las siete reglas del modal se heredan sin cambio: velo por `::backdrop` con token, `aria-labelledby` al
encabezado, aviso asociado por `aria-describedby`, foco al primer control y de vuelta al disparador,
Cancelar antes de la acción, dos grados de confirmación, y el modal confirma pero no da de alta.

### 5.7 Asistente de varios niveles

```razor
@* Paginas/Registros/AltaAsistida.razor *@
@page "/registros/alta-asistida"
@page "/registros/alta-asistida/{Paso:int}"
@rendermode InteractiveServer

<Asistente PasoActual="_paso" Total="4" AlCambiarPaso="IrAlPaso"
           Rotulos="@(new[] { "Identificación", "Atributos", "Vinculaciones", "Revisión" })">
    <PasoDeAsistente Numero="1"><CampoDeIdentificacion Modelo="_modelo" /></PasoDeAsistente>
    <PasoDeAsistente Numero="2"><CamposDeAtributos Modelo="_modelo" /></PasoDeAsistente>
    <PasoDeAsistente Numero="3"><SelectorDeVinculaciones Modelo="_modelo" /></PasoDeAsistente>
    <PasoDeAsistente Numero="4">
        <dl class="mq-kv">
            @foreach (var campo in Resumen.De(_modelo))
            {
                <div><dt class="mq-kv__clave">@campo.Etiqueta</dt>
                     <dd class="mq-kv__valor">@campo.Valor</dd></div>
            }
        </dl>
        <div class="mq-campo mq-campo--conmutador">
            <Conmutador Id="as-activar" @bind-Valor="_modelo.ActivarAlTerminar"
                        Rotulo="Dejar el registro activo al terminar" />
        </div>
    </PasoDeAsistente>
</Asistente>
```

```csharp
private async Task IrAlPaso(int destino)
{
    // Sólo se avanza con el paso actual válido. Hacia atrás nunca se valida.
    if (destino > _paso && !_contextos[_paso].Validate()) { return; }
    _paso = destino;
    Navegacion.NavigateTo($"/registros/alta-asistida/{_paso}", replace: true);
    _anuncio = $"Paso {_paso} de 4: {Rotulos[_paso - 1]}";
    await Foco.EnviarAlContenidoPrincipalAsync();
}
```

El componente `Asistente` materializa la anatomía normada: círculo numerado y conector por paso, tres
estados de paso, contador «Paso X de N» en una región activa, «Anterior» deshabilitado y sin eventos en
el primero, «Siguiente» que vira a la acción de confirmación en el último, y paso final de revisión con
resumen en filas clave/valor.

**Dónde no se usa asistente.** En el acto indivisible —el primer arranque, el aprovisionamiento—: una
superficie, un acto, sin «Cancelar», porque no hay estado previo al que volver.

### 5.8 Superficies de identidad, fuera del circuito

```razor
@* Paginas/Identidad/Ingreso.razor — SIN @rendermode: SSR estático *@
@page "/ingreso"
@layout Layout.AccesoLayout

<h1>Ingresar</h1>

@if (Codigo is not null)
{
    <p class="mq-banda @Catalogo.ClaseDe(Codigo)"
       role="@(Catalogo.EsError(Codigo) ? "alert" : "status")">@Catalogo.TextoDe(Codigo)</p>
}

<form method="post" action="/identidad/ingreso" data-enhance="false">
    <AntiforgeryToken />

    <div class="mq-campo">
        <label for="in-identificador">Identificador</label>
        <input class="mq-input" id="in-identificador" name="identificador" type="text"
               autocomplete="username" required />
    </div>

    <div class="mq-campo">
        <label for="in-secreto">Secreto</label>
        <input class="mq-input" id="in-secreto" name="secreto" type="password"
               autocomplete="current-password" required />
    </div>

    <button type="submit" class="mq-btn mq-btn--primario mq-btn--ancho">Ingresar</button>
</form>

<p class="mq-caption mq-mt-5">
    Si perdiste el secreto, pedile al responsable de la instancia que lo restablezca.
</p>

@code {
    [SupplyParameterFromQuery(Name = "estado")] public string? Codigo { get; set; }
}
```

```csharp
// Endpoints/IdentidadEndpoints.cs
public static void MapearIdentidad(this IEndpointRouteBuilder app)
{
    app.MapPost("/identidad/ingreso", async (HttpContext ctx, [FromForm] string identificador,
                                             [FromForm] string secreto, IServicioDeIdentidad svc) =>
    {
        var r = await svc.AutenticarAsync(identificador, secreto);
        if (!r.Aceptado)
        {
            // Rechazo indiferenciado y sin parámetros de la política.
            return Results.Redirect($"/ingreso?estado={r.Codigo}");
        }
        // La cookie se emite acá, en el ciclo de request, fuera de todo circuito.
        await ctx.SignInAsync(r.Principal);
        return Results.Redirect(r.Destino);
    }).DisableAntiforgery(false);

    app.MapPost("/identidad/salida", async (HttpContext ctx) =>
    {
        await ctx.SignOutAsync();
        return Results.Redirect("/ingreso?estado=sesion-cerrada");
    });
}
```

Cierre de sesión, siempre a un clic desde cualquier superficie del shell de trabajo:

```razor
<form method="post" action="/identidad/salida" data-enhance="false">
    <AntiforgeryToken />
    <button type="submit" class="mq-btn mq-btn--secundario"
            aria-label="Cerrar la sesión y volver a la pantalla de ingreso">
        <Icono Nombre="@Iconos.Salir" Tamanio="15" />Cerrar sesión</button>
</form>
```

**La superficie de acceso lleva el mismo template que el resto**: las mismas clases, los mismos tokens,
el mismo shell de acceso, el mismo sello de versión. Lo único que la distingue es que no abre circuito.

### 5.9 Sello de versión

```razor
@* Componentes/SelloDeVersion.razor *@
@inject IIdentidadDeVersion Version

<span class="mq-sello-version mq-meta">
    @Version.VersionLegible
    @if (Version.EsPreliminar) { <span class="mq-insignia mq-insignia--atencion">preliminar</span> }
    @if (Version.OrigenIndeterminado) { <span class="mq-meta">origen indeterminado</span> }
</span>
```

Se exhibe en las **dos** ubicaciones obligatorias, y la cadena que ve el usuario es la misma que se
registra en el diagnóstico.

---

## 6. Criterios de aceptación

Además de los criterios de [[Template-HTML-SDD-Default]] §6, que rigen igual sobre el marcado
producido:

- [ ] `[enumerable]` `wwwroot/css/Tokens.css` es el bloque `:root` de la maqueta, sin valores agregados ni quitados.
- [ ] `[enumerable]` No hay literales de color, tipografía ni espaciado en ningún `.razor`, `.razor.css` ni `.cs`.
- [ ] `[enumerable]` Ninguna superficie de identidad declara `@rendermode`.
- [ ] `[enumerable]` Los formularios de identidad y el cierre de sesión son `form method="post"` con token antifalsificación y con la navegación mejorada desactivada.
- [ ] `[enumerable]` Ningún componente usa `localStorage` ni `sessionStorage`.
- [ ] `[enumerable]` Todo servicio se registra en `Program.cs` y en ningún otro archivo.
- [ ] `[enumerable]` Toda acción primaria que llama al servidor setea su bandera de proceso **antes** del `await` y la libera en `finally`.
- [ ] `[enumerable]` Todo componente que suscribe a un servicio o abre un temporizador implementa la liberación de recursos.
- [ ] `[enumerable]` El sello de versión aparece en la superficie de acceso y en al menos una superficie del sistema en funcionamiento.
- [ ] `[enumerable]` Existe un componente propio por patrón del catálogo, y ninguna página reimplementa uno de ellos en línea.
- [ ] `[enumerable]` Los mensajes de resultado salen de un catálogo de códigos; ningún texto visible incluye traza, nombre de archivo, dirección de servicio ni código crudo.
- [ ] `[interpretativo]` El marcado que produce cada componente es el mismo que el de la maqueta aprobada, con las mismas clases.
- [ ] `[interpretativo]` El recorrido por teclado de la grilla, del asistente y del diálogo está escrito y verificado; el foco visible no se suprime en ningún control.
- [ ] `[interpretativo]` La UI de reconexión está estilizada acorde a la marca y anuncia en una región activa.
- [ ] `[interpretativo]` El guard existe en las tres capas y ninguna expone el motivo del rechazo.
- [ ] `[interpretativo]` La carga del ciclo de vida es idempotente, o su resultado se persiste entre prerrenderizado y circuito.

---

## 7. Anti-patrones

| Anti-patrón | Por qué | Qué hacer |
| --- | --- | --- |
| Ingreso o cambio de secreto resueltos con un manejador de botón interactivo | La cookie no se puede emitir desde un circuito ya establecido: el intento falla en tiempo de ejecución y el diagnóstico es oscuro | POST a un endpoint, con campos nativos |
| Cierre de sesión como enlace de navegación | Muta estado y no se envía como tal; además se puede disparar por prefetch | `form` POST con el botón adentro |
| Resolver el acceso con un condicional dentro del layout de trabajo | La frontera entre shells deja de ser una navegación completa, y el chrome se ofrece a quien no tiene sesión | Dos layouts, dos rutas |
| Reintroducir colores en un `.razor.css` «porque es sólo este componente» | Se pierde la fuente única y la trazabilidad con el diseño | Variable del bloque de tokens |
| Copiar el marcado de una tabla en cada página que lista algo | El patrón deja de vivir en un solo lugar y las páginas derivan entre sí | Componente `Grilla&lt;T&gt;` |
| Traer una librería de componentes sólo para el diálogo o la grilla | Reintroduce la traducción entre la maqueta aprobada y la implementación, que es lo que este documento existe para evitar | Componente propio, y si la decisión se revisa, se revisa entera |
| Escribir la superposición del diálogo a mano en lugar de usar `&lt;dialog&gt;` | Se pierden el confinamiento de foco y el cierre por Escape, y perder el recorrido por teclado es deriva mayor | `&lt;dialog&gt;` nativo con la interoperabilidad mínima de §5.6 |
| Botón que se deshabilita después del `await` | La ventana entre el clic y el `await` alcanza para el doble envío | Bandera antes del `await`, liberación en `finally` |
| Estado de UI en almacenamiento de navegador | Regla del framework; además queda fuera del circuito y se desincroniza | Componente o servicio `Scoped` |
| Lógica pesada dentro del render | Cada interacción cruza el circuito; el costo se paga por interacción | Ciclo de vida o manejador |
| `ValidationSummary` en lugar de mensaje por campo | Desasocia el error de su control, contra la regla de asociación por `aria-describedby` | `ValidationMessage` por campo |
| Transcribir la política de validación como literal en la vista | Dos fuentes de verdad que se desincronizan | Derivarla del servicio que la define |
| Mostrar el detalle técnico de la excepción al usuario | Filtra información del sistema y no dice qué hacer | Catálogo de códigos, con mensaje genérico como respaldo |
| Distinguir «identificador inexistente» de «secreto incorrecto» | Confirma la existencia de la identidad a quien no debería saberlo | Mensaje único e indiferenciado |
| Cuenta regresiva de la restricción temporal de acceso | Expone un parámetro de la política | Enunciar el estado sin el número |
| Apagar el prerrenderizado página por página para evitar la doble carga | Degrada la primera pintura de todo el producto y esconde el problema real | Carga idempotente, o persistencia del resultado |
| Asistente para el primer arranque | Se abandona a la mitad y deja el sistema en estado parcial | Una superficie, un acto indivisible |

---

## 8. Frontera con las reglas

| Tema | Archivo de reglas |
| --- | --- |
| Render mode por defecto, prohibición de almacenamiento de navegador, feedback y prevención de doble envío, reconexión estilizada, comunicación por `EventCallback`, componentes propios donde el patrón vive en un solo lugar, tema como fuente única, íconos SVG con `currentColor` | `Design-Rules-Blazor-Mudblazor.md` §2, §6 y §8 |
| Envío de los formularios de identidad por POST fuera del circuito, y cierre de sesión como POST | `Design-Rules-Blazor-Mudblazor.md` §4.2 |
| Nomenclatura: Título-Con-Guiones en documentos, PascalCase en código .NET | `Design-Rules-Blazor-Mudblazor.md` §8 y D3 |
| Shell partido, política de sesión, catálogo de códigos de resultado, rechazo indiferenciado | `Design-Rules-Acceso-Monousuario.md` |
| Acto indivisible, guard en tres capas, requisito declarado antes del intento | `Design-Rules-Primer-Arranque.md` |
| Contrato de identidad de versión y sus dos ubicaciones obligatorias | `Design-Rules-Identidad-De-Version.md` |
| Tokens, patrones, estados, accesibilidad, anti-patrones de diseño | `Design-Rules-Web-Generico.md` |
| Umbrales de deriva entre la maqueta aprobada y la implementación | `Deriva-Rules.md` §3 |
| Arquitectura interna de la solución | Categoría 05 |

### 8.1 Desviación declarada respecto de `Design-Rules-Blazor-Mudblazor.md`

**Qué se desvía.** Ese archivo mapea los diez patrones del catálogo a componentes de una librería
concreta, y su criterio de aceptación cierra con: los patrones se realizan con los componentes mapeados,
**no con HTML propio cuando existe componente equivalente**. Este documento invierte esa cláusula: los
patrones se realizan con componentes Razor propios.

**Por qué no es una sustitución.** `Rules-Base-Conocimiento.md` §0.4 sólo habilita sustituir un ítem del
piso **que el archivo de reglas haya rotulado como decisión de stack**. `Design-Rules-Blazor-Mudblazor.md`
no lleva ese rótulo en ninguna de sus reglas, con lo que el caso no es sustitución sino conflicto, y ante
conflicto **manda la regla de la categoría, salvo que el documento declare la desviación con su
justificación**. Es lo que hace esta sección. El campo `Sustituye` de la cabecera queda en `—` a
propósito.

**Justificación.** Tres razones, en orden de peso:

1. **La maqueta que el humano aprueba es HTML plano.** Con una librería de componentes hay un salto de
   tecnología entre lo validado y lo construido, y ese salto es donde nace la deriva visual. Con
   componentes propios el marcado aprobado se traslada literal.
2. **La cláusula invertida conserva su intención.** Lo que prohíbe es reinventar el patrón por pantalla,
   y eso se sigue cumpliendo: el patrón vive en un componente propio, que pasa a ser el «componente
   equivalente» al que la regla se refiere. Es además lo que el mismo archivo ya manda en su §8.
3. **El framework tiene reservado el lugar para este caso.** El índice del catálogo de diseño declara un
   documento pendiente para frontend sin framework de componentes; hasta que exista, este conocimiento
   ocupa ese hueco sin tocar ninguna regla.

**Qué cuesta la desviación, declarado.** Se pierde la accesibilidad que la librería resolvía: el
recorrido por teclado y el ARIA de grilla, asistente, diálogo y menú. En el sensado de deriva, perder el
recorrido por teclado, el foco visible o el contraste **es deriva mayor y bloquea**. Por eso los
criterios de §6 incluyen la verificación explícita de teclado en esos tres componentes, y por eso
`&lt;dialog&gt;` nativo no es negociable.

### 8.2 Huecos del framework que este documento llena sin normar

El framework no norma la separación `.razor` / `.razor.cs`, ni `EditForm` y sus anotaciones, ni la
inyección de dependencias en componentes, ni el ciclo de vida, ni el prerrenderizado y la persistencia
de estado, ni la estructura de carpetas del proyecto de interfaz —sólo tres archivos—, ni los render
modes distintos del interactivo de servidor. Todo lo que este documento dice sobre esos temas es
**decisión suya, no norma**: si el framework las incorpora, manda el framework.

---

## 9. Trazabilidad

| Vínculo | Valor |
| --- | --- |
| Índice al que pertenece | `Index-Knowledge.md` de la base que lo aloje |
| Documento del que hereda | [[Template-HTML-SDD-Default]] |
| Consumidor declarado | Categorías 03 y 05 |
| Artefacto de referencia | Ninguno depositado |
| Fuentes del relevamiento | `Design-Rules-Blazor-Mudblazor.md`; `Design-Rules-Web-Generico.md`; `Index-Design-Rules.md`; `Design-Rules-Acceso-Monousuario.md`; `Design-Rules-Primer-Arranque.md`; `Design-Rules-Identidad-De-Version.md`; `Rules-UX-UI-DX.md`; `Rules-Arquitectura-Tecnica.md`; `Maqueta-Rules.md`; `Deriva-Rules.md`; `Knowledge-Clean-Architecture-DataManager.md` |

---

## 10. Control de cambios

| Versión | Fecha | Cambios |
| --- | --- | --- |
| 1.0 | 2026-09-01 | Emisión inicial. Realización del template HTML sobre Blazor Interactive Server sin librería de componentes, con la desviación de §8.1 declarada y justificada. |
