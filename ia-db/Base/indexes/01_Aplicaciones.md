# 01 — Las dos aplicaciones

> **Propósito**: describir qué hace cada aplicación, qué superficies tiene y con qué `data-testid` se
> las ubica desde una prueba.
> **Fuente primaria**: `src/WebBlazor.E2E.Base.HolaMundo/` y `src/WebBlazor.E2E.Base.Login/`.
> **Vigencia**: 2026-09-02, commit `6af2049`. La forma constructiva —tokens, componentes, shells—
> está en [06_Template-Y-Superficies.md](06_Template-Y-Superficies.md).

Las dos comparten árbol y vocabulario: `Components/Paginas/`, `Components/Componentes/`,
`Components/Layout/`, `Theme/` y `Servicios/`. La raíz `Components/` se conserva porque es la que el
andamiaje de .NET referencia desde `Program.cs`; los nombres de adentro son los del template SDD.

```
src/<proyecto>/
├── Components/
│   ├── App.razor            Documento: Tokens.css → Componentes.css → styles.css
│   ├── Routes.razor         Router + FocusOnNavigate a #mq-main
│   ├── Componentes/         Un componente por patrón
│   ├── Layout/              MainLayout + BarraLateral + ReconnectModal (+ AccesoLayout en Login)
│   └── Paginas/             Las superficies
├── Servicios/               IIdentidadDeVersion (+ identidad, en Login)
├── Theme/                   Iconos, RolesDeIcono, Tono, UbicacionDelSello, EstadoDeSuperficie
└── wwwroot/css/             Tokens.css + Componentes.css
```

`_Imports.razor` importa globalmente `Componentes`, `Layout`, `Servicios` y `Theme`: por eso ninguna
superficie declara `@using` para citar un ícono o el vocabulario de estados.

## WebBlazor.E2E.Base.HolaMundo

Es el ejemplo canónico del repositorio: lo mínimo para que exista algo que probar, con sus estados a
la vista.

| Ruta | Componente | Render |
| --- | --- | --- |
| `/` | `Paginas/Inicio.razor` | SSR estático; declara por qué no tiene estado vacío |
| `/HolaMundo` | `Paginas/HolaMundo.razor` | `InteractiveServer` + `[StreamRendering]` |
| `/Error` | `Paginas/Error.razor` | SSR estático; expone solo `identificador-pedido` |
| `/not-found` | `Paginas/NoEncontrado.razor` | SSR estático, con `@layout MainLayout` |

`Program.cs` registra `AddRazorComponents().AddInteractiveServerComponents()` y el singleton
`IIdentidadDeVersion`, y arma el pipeline de la plantilla: `UseExceptionHandler` + `UseHsts` fuera de
Development, `UseStatusCodePagesWithReExecute("/not-found")`, `UseHttpsRedirection()`,
`UseAntiforgery()`, `MapStaticAssets()` y `MapRazorComponents<App>().AddInteractiveServerRenderMode()`.

### La superficie HolaMundo

Declara `@rendermode InteractiveServer` y `@attribute [StreamRendering]` a nivel de página —a
diferencia del laboratorio grande, donde el modo se fija en `App.razor` sobre `<Routes>`—.

| Elemento | `data-testid` | Qué es |
| --- | --- | --- |
| `InputText` | `campo-frase` | Enlazado a `_modelo.Frase`, valor inicial «Hola Mundo», `autocomplete="off"` |
| `button` (submit) | `boton-mostrar-frase` | Envía el `EditForm`; se deshabilita mientras `_procesando` |
| `p` | `campo-mensaje` | Solo existe en el estado `ConDatos`; contiene el mensaje y nada más |
| `Banda` | `mensaje-error` | Solo en el estado `ErrorDeEntrada` |

El `.razor` lleva comentados los tres llamados de Playwright que corresponden a cada elemento
(`FillAsync`, `ClickAsync`, `ToHaveTextAsync`): la superficie está escrita **como material
didáctico**, no solo como aplicación.

**Cambió el mecanismo de envío.** Ya no es un `@onclick` sobre un `InputText` con `@bind-Value` por
defecto: ahora hay un `EditForm EditContext="_contexto"` con `DataAnnotationsValidator`,
`OnValidSubmit="MostrarLaFraseAsync"` y `OnInvalidSubmit="AlRechazarLaEntrada"`. El modelo anidado
`ModeloDeFrase` valida `[Required]` y `[StringLength(120, MinimumLength = 1)]`.

Cuatro estados, cada uno un bloque, tomados de `EstadoDeSuperficie`:

| Estado | Qué se ve |
| --- | --- |
| `Vacio` | `EstadoVacio` con «Todavía no mostraste ninguna frase» |
| `Enviando` | `Esqueleto Filas="1"`; el botón muestra spinner y «Mostrando…» |
| `ConDatos` | La tarjeta «Frase mostrada» con `campo-mensaje` |
| `ErrorDeEntrada` | La banda `mensaje-error` + el `ValidationMessage` del campo |
| `Indisponible` | **Declarado «no aplica»** en un comentario: la frase no viaja a ningún servicio |

`_procesando` se setea antes del `await` y se libera en `finally`; un `<p class="mq-sr-only"
role="status" aria-live="polite">` anuncia el estado a lector de pantalla.

> **Consecuencia para las pruebas.** `campo-mensaje` **no existe** hasta que el envío se resuelve: la
> aserción tiene que esperarlo, cosa que `Expect(...).ToHaveTextAsync` hace por reintento. Y como el
> valor viaja por submit y no por `onchange`, la trampa del `@bind-Value` que documentaba la versión
> anterior de este índice ya no aplica.

## WebBlazor.E2E.Base.Login

La misma superficie detrás de un acceso. El detalle del esquema está en
[02_Autenticacion.md](02_Autenticacion.md).

| Ruta | Componente | Autorización | Render |
| --- | --- | --- | --- |
| `/` y `/index` | `Paginas/Inicio.razor` | `[Authorize]` | `InteractiveServer` + `[StreamRendering]` |
| `/HolaMundo` | `Paginas/HolaMundo.razor` | `[Authorize]` | `InteractiveServer` + `[StreamRendering]` |
| `/login` | `Paginas/Identidad/Ingreso.razor` | pública | **SSR estático a propósito**, `@layout AccesoLayout` |
| `/Error` | `Paginas/Error.razor` | pública | SSR estático |
| `/not-found` | `Paginas/NoEncontrado.razor` | pública | SSR estático |

**Ya no hay `/logout`**: el cierre de sesión es un `form` POST en la barra lateral, a un clic desde
cualquier superficie del shell de trabajo. La decisión está declarada en
`Guides/Template-SDD-Aplicado.md` §2.

`HolaMundo.razor` de este proyecto es el del otro más `[Authorize]` y la segunda capa del guard: su
`OnInitializedAsync` lee el `AuthenticationState` en cascada y, si no hay identidad, deja la
superficie en `Indisponible`.

### data-testid del repositorio

| `data-testid` | Dónde | Qué es |
| --- | --- | --- |
| `campo-frase` | `Paginas/HolaMundo.razor` (los dos proyectos) | Entrada de la frase |
| `boton-mostrar-frase` | ídem | Submit del formulario |
| `campo-mensaje` | ídem | La frase mostrada, solo en `ConDatos` |
| `mensaje-error` | ídem | Banda del estado `ErrorDeEntrada` |
| `identificador-pedido` | `Paginas/Error.razor` (los dos) | Lo único que la superficie de error expone |
| `sello-version` | `Componentes/SelloDeVersion.razor` (los dos) | Sello de versión |
| `campo-usuario` | `Paginas/Identidad/Ingreso.razor` | `input name="identificador"` |
| `campo-clave` | ídem | `input name="secreto"`, `type="password"` |
| `boton-ingresar` | ídem | Submit del `form` POST |
| `mensaje-resultado` | ídem | Banda del catálogo de resultados |
| `boton-cerrar-sesion` | `Layout/BarraLateral.razor` | Submit del `form` de salida |

> **Renombre.** El viejo `mensaje-error` de la pantalla de ingreso hoy se llama `mensaje-resultado`:
> la banda publica cualquier código del catálogo —incluido «Cerraste la sesión»— y el nombre anterior
> mentía. Está declarado en `Guides/Template-SDD-Aplicado.md` §2, que hace notar que ninguna prueba
> lo referenciaba. `mensaje-error` sigue existiendo, pero ahora nombra otra cosa: la banda de error
> de entrada de la superficie `HolaMundo`.
>
> **`estado-app` no existe** en el marcado de este repositorio, aunque una prueba lo busca — ver
> [05_Estado-Y-Divergencias.md](05_Estado-Y-Divergencias.md).

### Layouts

| Layout | Para qué |
| --- | --- |
| `Layout/MainLayout.razor` | Shell de trabajo: `BarraLateral` + `main#mq-main` + `SelloDeVersion` al pie + el aviso `#blazor-error-ui` |
| `Layout/AccesoLayout.razor` | Shell de acceso (solo en `Login`): lienzo con tarjeta angosta y sello, sin navegación |

La transición entre shells es una **navegación completa a otra ruta**, no un condicional adentro del
layout de trabajo. `BarraLateral` declara sus destinos en un array estático, marca el vigente con
`aria-current="page"` y —en `Login`— lleva el `form` POST de cierre de sesión al pie, separado por
hairline; implementa `IDisposable` para desuscribir `LocationChanged`.

## Puertos de arranque

De `Properties/launchSettings.json` (sin cambios respecto del indexado anterior):

| Aplicación | Perfil `http` | Perfil `https` |
| --- | --- | --- |
| `HolaMundo` | `http://localhost:5027` | `https://localhost:7230` (+ 5027) |
| `Login` | `http://localhost:5181` | `https://localhost:7212` (+ 5181) |

Ambas aplican `UseHttpsRedirection()`, así que en la práctica las pruebas deben apuntar al perfil
`https`. **La prueba de `HolaMundo` sigue sin apuntar a ninguno de estos puertos**: ver
[05_Estado-Y-Divergencias.md](05_Estado-Y-Divergencias.md).
