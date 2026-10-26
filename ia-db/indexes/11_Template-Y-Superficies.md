# 11 — Template y superficies

> **Propósito**: forma constructiva de la interfaz de las tres webs (Hola Mundo, Login y Movilidad Urbana): de dónde sale el template, qué hojas y tokens hay, qué componente realiza cada patrón, cómo se declara el estado de una superficie (`SurfaceState`) y cómo se arman los shells. Sirve para tocar la vista sin romper el contrato del template.
> **Fuente primaria**: `src/MovilidadUrbana.Web/wwwroot/css/`, `src/MovilidadUrbana.Web/Components/{App.razor,Routes.razor,Layout/,Shared/}`, `src/MovilidadUrbana.Web/{Theme,Services}/`, `src/WebBlazor.HolaMundo/{Theme,Components,Services,wwwroot}/`, `src/WebBlazor.Login/{Theme,Components,Services,wwwroot}/`, `README.md` § «Diseño», `CHANGELOG.md` (2026-09-04, 2026-09-18); commits `b0c828e`, `11620e9`, `946d023`, `e9dea2a`.
> **Vigencia**: versión 3.1, generada el 2026-10-25 sobre el commit `8fb4c3a` (2026-09-18).
> **Vecinos**: las pantallas, su comportamiento y todos los `data-testid` están en [04](04_Interfaz-Y-Pantallas.md); el acceso por cookies, el guard y las pruebas de Hola Mundo y Login en [10](10_Hola-Mundo-Y-Login.md); la convención inglés/español y el inventario completo de rastros en [01](01_Arquitectura.md); el porqué de cada desviación y lo que no hay que revertir en [08](08_Decisiones-Y-Trampas.md); la guía `Template-SDD-Aplicado.md` y demás documentos en [07](07_Guias.md). La paleta de la app Android, en [13](13_App-Android.md).

---

## 1. Origen: dos aplicaciones del mismo template

El template es el del Framework SDD y **no usa librería de componentes ni framework de CSS** (`README.md` l. 16). Se aplicó dos veces, en momentos y repositorios distintos, y eso explica las diferencias entre las webs (§ 7).

| Aplicación del template | Fecha | Dónde | Evidencia / fuente |
| --- | --- | --- | --- |
| `WebBlazor.HolaMundo` y `WebBlazor.Login` | 2026-09-01 | En `Lab-E2E.WebBlazor.Base` (retirado: «el repositorio de origen, que ya no existe», `e0f3e9d`; no está en `/LAB`); llegaron «idénticos byte a byte» con `11620e9` (79 archivos, 2026-09-12) | Guía `/LAB/Lab-Documentos/Lab-Documentos/Guides/Testing/Lab-E2E.WebBlazor-Guides/E2E-Guide/Template-SDD-Aplicado.md`; `evidencia/2026-09-01-aplicacion-template/` (`verificar.mjs`, `verificacion.log` con 10 comprobaciones OK, 12 capturas) |
| `MovilidadUrbana.Web` | 2026-09-04 | En este repo, PR #11 (`b0c828e`, merge `7a9edaa`) | `CHANGELOG.md` 2026-09-04; `README.md` § Diseño |

Bases de conocimiento aplicadas (rutas desde la raíz del workspace, verificadas en disco):

| Documento | Qué aporta |
| --- | --- |
| `/IA/SDD/IA.SDD/Conocimiento/Knowledge-Template-HTML-SDD-Default.md` | Maqueta: tokens, vocabulario de estados (`data-mq-estado`), clases `mq-`, anatomías de patrón |
| `/IA/SDD/IA.SDD/Conocimiento/Knowledge-Template-Blazor-Interactive-Server-SDD-Default.md` | Realización en Blazor Interactive Server sin librería |
| `/IA/SDD/IA.SDD/SDD/Devs/References/Design/Design-Rules-Web-Generico.md` §2 | Valor de cada token del catálogo |

> **Enlace vencido**: el `README.md` enlaza esas tres bases como `../../IA/SDD/IA.SDD/...`, relativo al clon. Desde `/LAB/Lab-E2E.WebBlazor/Lab-E2E.WebBlazor/` eso resuelve a `/LAB/IA/...`, que no existe (verificado). Los archivos viven en `/IA/SDD/IA.SDD/...`.

En `MovilidadUrbana.Web` el template reemplazó a **Bootstrap** (se retiraron la hoja vendorizada y `estilos.css`); en Hola Mundo y Login se retiraron `app.css`, los tres `.razor.css` del andamiaje y `wwwroot/lib` (`CHANGELOG.md` 2026-09-04; `Template-SDD-Aplicado.md` §1.1).

---

## 2. Cadena de estilos

```
App.razor  (<head>, orden contractual)
 ├─ css/Tokens.css            ← :root con los tokens del catálogo (única fuente de valor visual)
 ├─ css/Componentes.css       ← patrones con clases mq-, consumen var(--…)
 ├─ <Proyecto>.styles.css     ← bundle de CSS aislado (en Web: ReconnectionNotice.razor.css)
 └─ js: mq-dialogo.js, mq-foco.js (solo Web) y _framework/blazor.web.js
```

| Regla | Cómo se cumple | Fuente |
| --- | --- | --- |
| Tokens primero, componentes después | Comentario en el `<head>` de los tres `App.razor` | `src/*/Components/App.razor` |
| Ningún `style=` en línea | `grep -rn 'style=' --include=*.razor src` devuelve 0 (verificado) | utilitarias de § 5 de `Componentes.css` |
| Ningún color, tipografía ni espaciado fuera de `Tokens.css` | Sí; **pero** hay medidas literales de dimensión. En Web: `min-height` 26/32/40px, íconos 12–36px, `minmax(190px…)`/`minmax(200px…)`, breakpoint 768px, diálogo `min(420px, …)`; en la Base además `max-width: 360px` y `380px` | `grep` sobre las dos `Componentes.css` |
| Anchos de contenido en `ch` (desviación 4 de Web) | Tres medidas: `68ch`, `60ch`, `38ch` (`.mq-ancho-38`) | `src/MovilidadUrbana.Web/wwwroot/css/Componentes.css` l. 252, 731, 847 |
| Un solo punto de quiebre | `@media (max-width: 768px)`: sidebar → navegación superior; tabla → tarjetas apiladas; `.mq-acciones-pie` en `column-reverse` | § 6 de las dos `Componentes.css` |
| Movimiento reducido | Una única regla `prefers-reduced-motion` en `Tokens.css` | ambos `Tokens.css` |

Orden interno fijo de `Componentes.css` (las dos variantes): 1 reset/accesibilidad/foco · 2 shell de trabajo y barra lateral · 3 shell de acceso · 4 componentes · 5 utilitarias con nombre · 6 el único punto de quiebre. En Web la sección 3 está **vacía a propósito**: «No aplica… Se declara para que la ausencia del shell de acceso sea deliberada» (l. 215).

| Archivo | Web | Hola Mundo = Login |
| --- | --- | --- |
| `Tokens.css` (líneas / propiedades `--`) | 113 / 61 | 115 / 61 (md5 idéntico entre los dos) |
| `Componentes.css` (líneas / clases `.mq-` distintas) | 920 / 96 | 581 / 69 (md5 idéntico entre los dos) |

---

## 3. Tokens

Familias del `:root` (mismos valores en las tres webs salvo lo marcado en § 7):

| Familia | Variables | Nota |
| --- | --- | --- |
| Superficies | `--color-background-{primary,secondary,tertiary}` | `#FFFFFF`, `#F1F1EF`, `#F7F6F4` (lienzo) |
| Texto | `--color-text-{primary,secondary,tertiary,danger,on-brand}` | |
| Bordes | `--color-border-{secondary,tertiary,danger}` | `secondary` 1px controles, `tertiary` hairline 0.5px |
| Marca | `--color-brand-primary` `#0F6E56` + oscuro `#04342C` + tint `#E1F5EE` | **nombres distintos** según la web (§ 7) |
| Acento por módulo | `--color-accent-module-{a,b,c,d}` | «codifican pertenencia, no estética»; Web usa el modificador `.mq-tarjeta-entrada--modulo-b` (→ `--color-accent-module-b`) en la tarjeta de Encuesta (`Home.razor` l. 31; `Componentes.css` l. 559–561) |
| Semánticos | `--color-{text,background}-{success,warning,error,info}`, `--color-border-info` | siempre par texto + tint |
| Velo | `--color-backdrop: rgba(26, 26, 24, 0.45)` | lo nombra la maqueta (§3.6 de `Knowledge-Template-HTML-SDD-Default.md`) sin valor; §2 de `Design-Rules-Web-Generico.md` no lo trae. Se deriva de `color.text.primary` (comentario de `Tokens.css`) |
| Tipografía | `--font-sans`, `--font-mono`, cinco escalones `--font-size/weight-{title,body-strong,body,caption,meta}` (17/14/13/12/11px) y dos interlineados | |
| Espaciado | `--space-1` … `--space-9` (4, 8, 12, 14, 16, 18, 20, 22, 28px) | |
| Radios y bordes | `--radius-{md,lg,pill,icon}`, `--border-hairline`, `--border-control` | |
| Movimiento | `--motion-fast` 150ms, `--motion-base` 200ms, `--motion-ease` | |
| Layout | `--shell-sidebar-width: 168px` | catálogo §3.1 «~168px» |

---

## 4. Un componente propio por patrón

### 4.1 Movilidad Urbana (`src/MovilidadUrbana.Web/Components/Shared/`)

| Patrón del catálogo | Componente | Qué concentra |
| --- | --- | --- |
| §4.1 Navegación lateral | `Sidebar.razor` | Identidad (`data-testid="marca"`), tres destinos (`nav-inicio`, `nav-localidades`, `nav-encuesta`), `aria-current="page"`, clase `mq-nav-item--activo`; suscribe `LocationChanged` y la libera en `Dispose` |
| §4.2 Tarjeta de acceso | `.mq-tarjeta-entrada` en `Pages/Home.razor` | Toda la tarjeta es el área activable |
| §4.3 Grilla de listado | `Grid.razor` + `Grid.razor.cs` + `GridColumn.cs` | Tabla con `caption` (`mq-sr-only`) y `scope`, y tarjetas apiladas **las dos siempre en el marcado**; resuelve `Cargando` (→ `Skeleton`), `Vacio` (→ `Empty`), `FiltradoSinResultados` (→ `NoResults`) y el resto como datos. `GridColumn` no emite marcado: se registra en la grilla por `CascadingValue` y pide un render más |
| §4.4 Formulario de edición | `FormField.razor` + `FieldContext.cs` | Rótulo visible, requisito antes del intento (`{Id}-requisito`), error (`{Id}-error`) y `aria-describedby` armado por el componente; `FieldContext` da `InputClass`/`SelectClass` con `--invalido` |
| §4.5 Asistente | `Wizard.razor` (109 líneas) + `WizardStep.razor` | Círculo, conector y rótulo por paso; tres estados (`completado`/`actual`/`pendiente`); `aria-current="step"`; contador `etiqueta-paso` «Paso N de T»; región activa; botones `boton-anterior`, `boton-siguiente`, `boton-finalizar`, `boton-procesando`. El paso pedido lo concede la superficie (`OnStepChange`) |
| §4.8 Insignia | `Badge.razor` | Tono `BadgeTone` (`Neutro, Brand, Exito, Atencion, Peligro, Info`); el texto siempre se imprime |
| §5 Estados | `EmptyState.razor`, `UnavailableState.razor`, `Skeleton.razor`, `Band.razor` | Vacío / filtrado sin resultados, indisponible (`role="alert"`), cargando (`aria-hidden`), bandas `BandTone` (`Exito, Atencion, Error, Info`; `Error` → `role="alert"`, resto `status`) |
| §5.4 template Blazor · diálogo | `Dialog.razor` + `Dialog.razor.cs` + `DialogHost.razor`, servicio `Services/DialogService.cs` | `<dialog>` nativo, host único en el layout; dos grados de confirmación (el segundo, escrito, implementado y sin uso) |
| §6 Iconografía | `Icon.razor` + `Theme/Icons.cs` + `Theme/IconRoles.cs` | SVG inline, `currentColor`, grilla 24, trazo 1.75; con `Title` es `role="img"`, sin él `aria-hidden`. Tamaños por rol: 24 navegación · 20 tarjeta · 16 inline · 15 fila |
| Identidad de versión | `VersionStamp.razor` + `Services/VersionIdentity.cs` | Versión resuelta una vez en `Program.cs` (`VersionIdentity.FromAssembly`), sin metadatos `+…` → «origen indeterminado»; con `-` → insignia «preliminar» |
| Reconexión | `ReconnectionNotice.razor` (+ `.razor.css`, `.razor.js`) | Banda no modal `role="status"`; el `.js` traduce `components-reconnect-state-changed` a `data-estado` y recarga ante `rejected` |

Piezas no visuales de la misma carpeta: `SurfaceState.cs` (§ 5) y `Tonos.cs` (los dos enumerados de tono).

**Servicios de interfaz** (registrados `Scoped` en `src/MovilidadUrbana.Web/Program.cs`: «Estado de interfaz del circuito: ni un almacenamiento de navegador improvisado»):

| Servicio | Contrato | Interop JS |
| --- | --- | --- |
| `IDialogService` / `DialogService` | `ConfirmAsync(ConfirmationRequest)` → `Task<bool>`; `Resolve(bool)`; una confirmación nueva resuelve la anterior en `false` | `mqDialogo.abrir` (`showModal()`, guarda el disparador, enfoca el primer control) / `mqDialogo.cerrar` (devuelve el foco) |
| `IFocusService` / `FocusService` | `FocusMainContentAsync()` | `mqFoco.alContenidoPrincipal` → `#mq-main` |
| `IVersionIdentity` | `DisplayVersion`, `IsPrerelease`, `UnknownSource` | — (Singleton) |

`ConfirmationRequest(Title, Aviso, RotuloDeAccion, EsDestructiva = true, RotuloDelCampo, ValorEsperado)`; `PideEscritura` cuando hay rótulo y valor esperado (`Services/IDialogService.cs`).

### 4.2 Hola Mundo y Login (`src/WebBlazor.{HolaMundo,Login}/`)

| Pieza | Hola Mundo | Login |
| --- | --- | --- |
| `Components/Shared/` | `Badge`, `Band`, `EmptyState`, `Icon`, `Skeleton`, `UnavailableState`, `VersionStamp` (7, idénticos byte a byte con Login) | los mismos 7 + `Redirect.razor` |
| `Components/Layout/` | `MainLayout`, `Sidebar`, `ReconnectModal` (+ `.razor.js`) | los mismos + `AuthLayout.razor` |
| `Theme/` | `Icons`, `IconRoles`, `SurfaceState`, `Tone`, `StampPlacement` | ídem (solo cambia el `namespace`) |
| `Services/` | `IVersionIdentity`, `VersionIdentity` | ídem + `IIdentityService`, `IdentityService`, `SignInResults` (ver [10](10_Hola-Mundo-Y-Login.md)) |

Diferencias de API respecto de Web: un solo enumerado `Tone` (`Neutro, Exito, Atencion, Peligro, Info`) para insignia y banda; `Badge` recibe `Value` (texto) en vez de `ChildContent`; `Band` acepta atributos sueltos (`CaptureUnmatchedValues`, así recibe `data-testid`); `VersionStamp` tiene `Placement` (`StampPlacement.Pie` / `.Lienzo`); `VersionIdentity` expone además `BuildId` y se construye por `AddSingleton<IVersionIdentity, VersionIdentity>()`.

---

## 5. `SurfaceState`: el estado de una superficie

Realiza el `data-mq-estado` de la maqueta: una propiedad de la superficie y **un bloque `@if` por estado**. El vocabulario «no se agrega ni se recorta» (`SurfaceState.cs` de Web; la Base dice «sin agregados ni recortes»): los diez valores están en las tres webs aunque no todos se alcancen.

| Valor | Significado (doc del enum) | Lo usa (conteo con `grep` en `Components/Pages` y `Grid`) |
| --- | --- | --- |
| `Cargando` | operación asíncrona en curso → esqueletos | Localidades, `Grid` |
| `Vacio` | no hay datos; acción: crear el primero | Localidades, `Grid`; Hola Mundo y Login (estado inicial) |
| `FiltradoSinResultados` | hay datos y el filtro no encontró; acción: limpiar el filtro | Localidades, `Grid` |
| `ConDatos` | hay contenido | Localidades, Hola Mundo, Login |
| `Indisponible` | el servicio no respondió | Localidades (`UnavailableState`); `HolaMundo.razor` de Login |
| `Enviando` | una acción viaja al servidor | Hola Mundo y Login (bandera antes del `await`, liberada en `finally`) |
| `ErrorDeEntrada` | lo cargado no cumple la política | Hola Mundo y Login |
| `ErrorDeOperacion`, `Exito` | rechazo no de entrada; acción completada | ninguna superficie los asigna (declarados) |
| `Reconectando` | circuito cortado | lo gobierna el framework (`ReconnectionNotice` / `ReconnectModal`) |

- `Vacio` y `FiltradoSinResultados` son **estados distintos con acciones distintas**; para que el segundo signifique algo, el ABM sumó la barra de filtros (`CHANGELOG.md` 2026-09-04). En Hola Mundo y Login «no aplica» (ninguna superficie presenta colección filtrable: `Template-SDD-Aplicado.md` §3).
- `Localidades.razor.cs` decide el estado así: `_all.Count == 0 → Vacio`, `_visible.Count == 0 → FiltradoSinResultados`, si no `ConDatos` (l. 75–77).
- `Encuesta` **no usa** `SurfaceState`: su estado lo llevan el `Wizard` y la revisión como estado de éxito (desviación 3, § 8).
- `Indisponible` de Hola Mundo se declara «no aplica» en un comentario del marcado: «la frase no viaja a ningún servicio externo» (`src/WebBlazor.HolaMundo/Components/Pages/HolaMundo.razor`).

---

## 6. Shells

```
Web (MovilidadUrbana.Web)                         Hola Mundo / Login
App.razor  (lee la cookie, SessionId → Routes)    App.razor
 └─ <Routes @rendermode=InteractiveServer>         ├─ <Routes/> (sin render mode en la raíz)
     └─ MainLayout                                 │   └─ MainLayout | AuthLayout (solo Login)
         ├─ Sidebar                                ├─ <ReconnectModal/> (en App.razor)
         ├─ main#mq-main (tabindex=-1) + VersionStamp
         ├─ DialogHost  ─┐ hosts únicos            └─ cada página interactiva declara
         ├─ ReconnectionNotice ┘                       @rendermode InteractiveServer
         ├─ testigo estado-app (RendererInfo.IsInteractive)
         └─ #blazor-error-ui
```

| Aspecto | Web | Hola Mundo / Login |
| --- | --- | --- |
| Render mode | En la raíz (`<Routes @rendermode="InteractiveServer" SessionId=…>` y `<HeadOutlet @rendermode…>`) — desviación 1 | Por página: `HolaMundo.razor`, y en Login `Home.razor` y `HolaMundo.razor`; `Pages/Account/Login.razor` **sin** `@rendermode` (SSR estático) |
| Shell de trabajo | `.mq-shell` = `Sidebar` + `.mq-shell-contenido` (`main#mq-main` + sello) | igual, con `VersionStamp Placement="Pie"` |
| Shell de acceso | No aplica (no hay superficies sin sesión) | Login: `AuthLayout` = `.mq-lienzo` + `main.mq-tarjeta-acceso` + sello en `Lienzo` |
| Foco al navegar | `FocusOnNavigate Selector="#mq-main"` | ídem |
| Salto al contenido | `<a class="mq-skip" href="#mq-main">Ir al contenido</a>` | ídem |
| Testigo de hidratación | `<div hidden data-testid="estado-app" data-interactivo=…>` en `MainLayout`, con `RendererInfo.IsInteractive` | `<span class="mq-sr-only" data-testid="estado-app">` en la página, puesto a `true` en `OnAfterRender` |
| Reconexión | `ReconnectionNotice`: `div#components-reconnect-modal` como banda **no modal** | `ReconnectModal`: conserva `<dialog id="components-reconnect-modal">` y las clases `components-reconnect-*` que conmuta el circuito |
| Error no recuperable | `#blazor-error-ui` con banda de atención y «Recargar la pantalla» | banda de error `role="alert"` y «Recargar la página» |
| Router | `Router` + `RouteView`, `NotFoundPage=Pages.NotFound` (`/no-encontrado`) | Hola Mundo igual (`/not-found`); Login `AuthorizeRouteView` + `Redirect` a `/login?estado=…` |
| Barra lateral | 3 destinos, clase `mq-nav-item` / `--activo` | Hola Mundo 2 destinos (`Inicio`, `Hola Mundo`), clase `mq-nav__item`; Login suma al pie un `form` POST a `/identidad/salida` con `boton-cerrar-sesion` |

---

## 7. Divergencias entre las dos aplicaciones del template

Verificadas con `diff`/`md5sum` entre `src/MovilidadUrbana.Web/` y `src/WebBlazor.HolaMundo/` (Login es igual a Hola Mundo en todo lo que sigue).

| Tema | Web | Hola Mundo / Login | Contra el catálogo |
| --- | --- | --- | --- |
| Marca oscura / tint | `--color-brand-primary-dark`, `--color-brand-primary-tint` | `--color-brand-dark`, `--color-brand-tint` | El catálogo nombra `color.brand.primary.dark` / `.tint` (§2.1 de `Design-Rules-Web-Generico.md`): coincide Web. La maqueta (§3.6 de `Knowledge-Template-HTML-SDD-Default.md`) abrevia `--color-brand-primary` \| `-dark` \| `-tint`, notación que en las demás filas reemplaza el último segmento (daría `--color-brand-dark`, como la Base): lectura ambigua, **no verificado** cuál siguió cada aplicación. Los `Tokens.css` dicen que los nombres «no se cambian» (Web) / «no se renombran» (Base) |
| `--radius-md` | 8px | 10px | El catálogo da «8–10px»: los dos caben |
| Interlineado de texto | `--line-height-prosa` | `--line-height-texto` | §2.2 del catálogo da el valor («Interlineado 1.4–1.5 en bloques de texto; títulos en 1.2») pero ningún nombre de token; tampoco la maqueta §3.6: **no verificado** de dónde sale cada nombre |
| `--font-sans` / `--font-mono` | incluye `"Noto Sans"`; mono con `ui-monospace` | sin `Noto Sans`; mono con `SFMono-Regular` | — |
| `.mq-ancho-38` | `max-width: 38ch` | `width: 100%; max-width: 380px` | Mismo nombre, otra unidad |
| Ítem de navegación | `.mq-nav-item` + `.mq-nav-item--activo` | `.mq-nav__item` (activo por `aria-current`) | — |
| Id de `EmptyState` / `UnavailableState` | derivado del título: «tiene que ser el mismo en el prerenderizado y en el circuito» | `Guid.NewGuid()` por instancia | ver [08](08_Decisiones-Y-Trampas.md) |
| Tonos | `BadgeTone` + `BandTone` (`Tonos.cs`, en `Components/Shared`) | `Tone` único (en `Theme/`) | — |
| Ubicación de `SurfaceState` | `Components/Shared/SurfaceState.cs` | `Theme/SurfaceState.cs` («la carpeta que ya se importa globalmente», `Template-SDD-Aplicado.md` §2) | — |

---

## 8. Lo que no aplica y las desviaciones declaradas (Web)

`README.md` § Diseño. El porqué largo y qué no revertir está en [08](08_Decisiones-Y-Trampas.md).

| Tipo | Qué | Motivo en una línea |
| --- | --- | --- |
| No aplica | Shell de acceso, endpoints de identidad, guard en tres capas | No hay credenciales: la sesión la reparte un middleware por cookie |
| No aplica | Host de avisos efímeros | Resultados como banda; un aviso que se autodescarta ataría la evidencia E2E a un temporizador |
| No aplica | Conmutador y confirmación escrita en uso | Ninguna pantalla tiene toggle; la baja no arrastra dependientes (las encuestas guardan el nombre, no la clave) |
| No aplica | Dataset de maqueta, barra de validación, recarga automática | Instrumentos de la maqueta |
| Desviación 1 | Render mode en la raíz | El id de sesión se lee en `App.razor` y viaja como parámetro de `Routes` ([03](03_Sesiones-Y-Persistencia.md)) |
| Desviación 2 | `EditForm` sin `DataAnnotationsValidator` | La política vive en `Domain/Rules` y la valida el servicio; el requisito sale de `LocalidadPolicy` / `EncuestaPolicy` |
| Desviación 3 | Revisión del asistente = estado de éxito, no cuarto paso | `TotalDePasos` es regla de dominio; `ResumenDeEncuesta` se recorre |
| Desviación 4 | Anchos en `ch` | El catálogo no tiene token de ancho y promover uno no es decisión del producto |

Hola Mundo **sí** usa `DataAnnotationsValidator` + `ValidationMessage` (validación «de conveniencia» en el modelo de la página: `HolaMundo.razor`). Las decisiones al aplicar el template a Hola Mundo y Login (estructura de carpetas, `<dialog>` de reconexión, foco de `#mq-main` sin anillo, `mensaje-error` → `mensaje-resultado`, retiro de `/logout`) están en la tabla §2 de `Template-SDD-Aplicado.md`.

---

## 9. Cómo se compone una superficie (receta extraída del código)

```
Página (Pages/X.razor + X.razor.cs)
 ├─ encabezado .mq-encabezado con h1 (data-testid="titulo" en Web)
 ├─ región activa <p class="mq-sr-only" role="status" aria-live="polite">@_announcement</p>
 ├─ Band para el resultado de la acción
 ├─ FormField × N  (Control recibe FieldContext → id, aria-describedby, clase)
 ├─ Grid<TItem> State=_state con <Columns><GridColumn …/></Columns>, Empty, NoResults, Actions
 └─ acciones: Dialogs.ConfirmAsync(new ConfirmationRequest(...)) — nunca un modal propio
```

- Campos con `@bind:event="oninput"`: 3 en `Encuesta.razor`, 1 en `Localidades.razor` (conteo con `grep`); los de texto usan `@oninput` escrito a mano (1 en `Encuesta.razor`, 3 en `Localidades.razor`, incluida la búsqueda) y los `select` siguen con `@bind`. Motivo en [08](08_Decisiones-Y-Trampas.md).
- Íconos siempre por `Icons.*` + `IconRoles.*`; el tamaño «no se escribe en la vista: se nombra por su rol» (`Theme/IconRoles.cs`).
- La interop JS invocada desde C# se reduce a `mq-dialogo.js` («Lo mínimo que no se puede escribir en C#») y `mq-foco.js` («Es lo mínimo, y nada más que eso…»), según sus encabezados; aparte está el módulo `ReconnectionNotice.razor.js`, que no se invoca desde C#.

---

## 10. Rastros de nombres previos al renombre en esta zona

El renombre (`946d023`, 2026-09-18) llevó `Components/Componentes/` → `Components/Shared/` y los componentes al inglés (`Grilla`→`Grid`, `ColumnaDeGrilla`→`GridColumn`, `Campo`→`FormField`, `ContextoDeCampo`→`FieldContext`, `Asistente`→`Wizard`, `PasoDeAsistente`→`WizardStep`, `Dialogo`→`Dialog`, `DialogoHost`→`DialogHost`, `Insignia`→`Badge`, `Banda`→`Band`, `EstadoVacio`→`EmptyState`, `EstadoIndisponible`→`UnavailableState`, `Esqueleto`→`Skeleton`, `Icono`→`Icon`, `BarraLateral`→`Sidebar`, `SelloDeVersion`→`VersionStamp`, `AvisoDeReconexion`→`ReconnectionNotice`, `EstadoDeSuperficie`→`SurfaceState`, `Iconos`/`RolesDeIcono`→`Icons`/`IconRoles`, `IIdentidadDeVersion`→`IVersionIdentity`, `IServicioDeDialogos`→`IDialogService`; en Base: `Tono`→`Tone`, `UbicacionDelSello`→`StampPlacement`, `AccesoLayout`→`AuthLayout`, `Redireccion`→`Redirect`, `Paginas/`→`Pages/`). Quedaron, en texto que el renombre no tocó:

| Dónde | Rastro |
| --- | --- |
| `src/MovilidadUrbana.Web/Components/Shared/FieldContext.cs` | Doc cita `Campo.razor` y `<param name="Descriptores">`/`"Invalido"`; los parámetros reales son `DescribedBy`/`Invalid` |
| `src/MovilidadUrbana.Web/Services/IDialogService.cs` | `<param name="Titulo">` para la propiedad `Title`; el resto del record quedó en español (`Aviso`, `RotuloDeAccion`, `EsDestructiva`…) |
| Parámetro `Icon.Nombre` (las tres webs) | Parámetro de pieza técnica en español |
| Guía `Template-SDD-Aplicado.md` §1.5–1.6 | Cita `Pages/Identidad/Ingreso.razor` y `Services/IIdentidadDeVersion.cs` (`Endpoints/IdentityEndpoints.cs` sí está al día); hoy `Pages/Account/Login.razor` y `Services/IVersionIdentity.cs`. Su «Pendiente declarado» (Login.E2ETests sin casos) quedó viejo: hay 10 casos ([10](10_Hola-Mundo-Y-Login.md)) |

Otros rastros de esta zona ya inventariados en [01](01_Arquitectura.md) §8.3: el mensaje de excepción de `GridColumn.cs` l. 38 («ColumnaDeGrilla … <Columnas> de una Grilla»), `Icono.razor`/`Iconos` en `Theme/Icons.cs` e `Icon.razor`, los textos de enlace del `README.md` § Diseño y su `Domain/Reglas` (l. 224). El manejador `OnSignInRejected` de `HolaMundo.razor`, en [10](10_Hola-Mundo-Y-Login.md) §7.

Los identificadores de JS (`mqDialogo`, `mqFoco`), las clases `mq-*`, los `data-testid` y los estados de `SurfaceState` quedan en español **por regla**, no como rastro (`CHANGELOG.md` 2026-09-18).
