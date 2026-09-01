# 01 — Las dos aplicaciones

> **Propósito**: describir qué hace cada aplicación, qué pantallas tiene y con qué `data-testid` se
> las ubica desde una prueba.
> **Fuente primaria**: `src/WebBlazor.E2E.Base.HolaMundo/` y `src/WebBlazor.E2E.Base.Login/`.

Las dos son la **plantilla estándar de Blazor Web App** con render *interactive server*, con una o
dos páginas agregadas. Comparten `App.razor`, `Routes.razor`, `MainLayout`, `NavMenu`,
`ReconnectModal`, `Error`, `NotFound` y `wwwroot/lib/bootstrap/`.

## WebBlazor.E2E.Base.HolaMundo

Es el ejemplo canónico del repositorio: lo mínimo para que exista algo que probar.

| Ruta | Componente | Contenido |
| --- | --- | --- |
| `/` | `Pages/Home.razor` | «Hello, world!» de la plantilla |
| `/HolaMundo` | `Pages/HolaMundo.razor` | La página del ejemplo |

`Program.cs` es el de la plantilla: `AddRazorComponents().AddInteractiveServerComponents()`,
`UseExceptionHandler` + `UseHsts` fuera de Development, `UseStatusCodePagesWithReExecute("/not-found")`,
`UseHttpsRedirection()`, `UseAntiforgery()`, `MapStaticAssets()` y
`MapRazorComponents<App>().AddInteractiveServerRenderMode()`.

### La página HolaMundo

Declara `@rendermode InteractiveServer` y `@attribute [StreamRendering]` a nivel de página —a
diferencia del laboratorio grande, donde el modo se fija en `App.razor` sobre `<Routes>`—.

| Elemento | `data-testid` | Qué es |
| --- | --- | --- |
| `InputText` | `campo-frase` | Enlazado a `Frase`, con valor inicial «Hola Mundo» |
| `button` | `boton-mostrar-frase` | Copia `Frase` en `Mensaje` |
| `div` | `campo-mensaje` | Muestra `Mensaje` |

El propio `.razor` lleva comentados los tres llamados de Playwright que corresponden a cada
elemento (`FillAsync`, `ClickAsync`, `ToHaveTextAsync`): la página está escrita **como material
didáctico**, no solo como aplicación.

Detalle a tener presente: el `InputText` usa el `@bind-Value` por defecto, que escucha `onchange`.
El caso de prueba funciona porque hace clic en el botón después de llenar —y ese clic quita el foco
del campo—; con una aserción inmediata tras `FillAsync` no llegaría el valor. En el laboratorio
grande el mismo problema se resuelve con `@bind:event="oninput"`.

## WebBlazor.E2E.Base.Login

La misma plantilla, más autenticación por cookies. El detalle del esquema está en
[02_Autenticacion.md](02_Autenticacion.md).

| Ruta | Componente | Autorización | Render |
| --- | --- | --- | --- |
| `/` y `/index` | `Pages/Home.razor` | `[Authorize]` | `InteractiveServer` + `[StreamRendering]` |
| `/HolaMundo` | `Pages/AuthenticatedHolaMundo.razor` | `[Authorize]` | `InteractiveServer` + `[StreamRendering]` |
| `/login` | `Pages/Login.razor` | pública | **SSR estático a propósito** |
| `/logout` | `Pages/Logout.razor` | `[Authorize]` | **SSR estático a propósito** |

`AuthenticatedHolaMundo.razor` es `HolaMundo.razor` con `[Authorize]` agregado: mismos tres
`data-testid`, mismos comentarios didácticos.

### data-testid de las pantallas de sesión

| Elemento | `data-testid` | Dónde |
| --- | --- | --- |
| Campo usuario | `campo-usuario` | `Login.razor` |
| Campo clave | `campo-clave` | `Login.razor` |
| Botón ingresar | `boton-ingresar` | `Login.razor` |
| Mensaje de error | `mensaje-error` | `Login.razor`, solo si hay error |
| Botón cerrar sesión | `boton-cerrar-sesion` | `Logout.razor` |
| Mensaje de no autorizado | `mensaje-no-autorizado` | `Routes.razor`, bloque `<NotAuthorized>` |

### Layouts

`DefaultLayout.razor` es un contenedor mínimo (`<div class="container py-4">@Body</div>`) que usan
`Login` y `Logout` mediante `@layout`; el resto usa el `MainLayout` de la plantilla.

`NavMenu.razor` usa `<AuthorizeView>` para alternar entre el enlace «Ingresar» y «Cerrar sesión».

## Puertos de arranque

De `Properties/launchSettings.json`:

| Aplicación | Perfil `http` | Perfil `https` |
| --- | --- | --- |
| `HolaMundo` | `http://localhost:5027` | `https://localhost:7230` (+ 5027) |
| `Login` | `http://localhost:5181` | `https://localhost:7212` (+ 5181) |

Ambas aplican `UseHttpsRedirection()`, así que en la práctica las pruebas deben apuntar al perfil
`https`. **La prueba de `HolaMundo` no apunta a ninguno de estos puertos**: ver
[05_Estado-Y-Divergencias.md](05_Estado-Y-Divergencias.md).
