# 10 — Hola Mundo y Login

> **Propósito**: describir las dos aplicaciones simples de la solución —qué superficies tienen, con
> qué `data-testid` se las ubica, cómo está resuelto el acceso en Login y cómo se prueban sin
> fixture—, para que un agente no las confunda con Movilidad Urbana ni las «uniforme» con ella.
> **Fuente primaria**: `src/WebBlazor.HolaMundo/`, `src/WebBlazor.Login/`,
> `tests/WebBlazor.{HolaMundo,Login}/`, `evidencia/`.
> **Vigencia**: 2026-09-12, commit `06528d3`.

## De dónde vienen y para qué están

Llegaron el 2026-09-12 desde `Lab-E2E.WebBlazor.Base`, que se retira, **idénticas byte a byte** a
lo que había allá (`CHANGELOG.md`). Son los escalones 1 y 2 del laboratorio: la misma superficie,
primero sola y después detrás de un acceso, sin capas, sin dominio y sin persistencia. Lo que se
estudia en ellas es **la técnica desnuda**: `data-testid`, testigo de hidratación, estados de
superficie, y en Login el guard y la promesa negativa.

Comparten árbol y vocabulario: `Components/Paginas/`, `Components/Componentes/`, `Components/Layout/`,
`Theme/` (con `EstadoDeSuperficie`, `Tono`, `UbicacionDelSello`, `Iconos`, `RolesDeIcono`) y
`Servicios/`. La raíz `Components/` se conserva porque es la que referencia `Program.cs`. La forma
constructiva común está en [11](11_Template-Y-Superficies.md).

| | Hola Mundo | Login |
| --- | --- | --- |
| Proyecto web | `src/WebBlazor.HolaMundo/` | `src/WebBlazor.Login/` |
| Pruebas | `tests/WebBlazor.HolaMundo.E2ETests/` — 1 caso | `tests/WebBlazor.Login.E2ETests/` — 10 casos |
| URL de prueba (fija en el código) | `http://localhost:5027` | `http://localhost:5181` |
| Perfil `https` de `launchSettings` | 7230 | 7212 |
| Workflow | `e2e-holamundo.yml` | `e2e-login.yml` |
| Script | `PROYECTO=holamundo scripts/pruebas.sh` | `PROYECTO=login scripts/pruebas.sh` |

Ninguno de los dos proyectos de prueba **referencia** al de aplicación: prueban por HTTP contra la
URL, con la aplicación levantada aparte por quien corre la prueba.

## Hola Mundo

| Ruta | Componente | Render |
| --- | --- | --- |
| `/` | `Paginas/Inicio.razor` | SSR estático |
| `/HolaMundo` | `Paginas/HolaMundo.razor` | `@rendermode InteractiveServer` + `[StreamRendering]`, **por página** |
| `/Error` | `Paginas/Error.razor` | SSR estático; expone `identificador-pedido` |
| `/not-found` | `Paginas/NoEncontrado.razor` | SSR estático |

A diferencia de Movilidad Urbana, el render mode se fija en la página y no en `App.razor`.

### La superficie HolaMundo

Un `EditForm` con `DataAnnotationsValidator`, `OnValidSubmit` y `OnInvalidSubmit`; el modelo
`ModeloDeFrase` valida `[Required]` y `[StringLength(120, MinimumLength = 1)]`, con valor inicial
«Hola Mundo».

| Elemento | `data-testid` | Qué es |
| --- | --- | --- |
| Testigo de hidratación | `estado-app` | `span.mq-sr-only` con `data-interactivo`: `"false"` en el HTML del servidor, `"true"` desde `OnAfterRender` |
| `InputText` | `campo-frase` | La frase |
| `button` submit | `boton-mostrar-frase` | Se deshabilita mientras `_procesando` |
| `p` | `campo-mensaje` | Solo existe en `ConDatos`; contiene el mensaje y nada más |
| `Banda` | `mensaje-error` | Solo en `ErrorDeEntrada` |

Estados, un bloque cada uno: `Vacio` (`EstadoVacio`), `Enviando` (`Esqueleto`), `ConDatos` (la
tarjeta), `ErrorDeEntrada` (la banda, fuera del marco porque interrumpe). `Indisponible` está
**declarado «no aplica»** en un comentario: la frase no viaja a ningún servicio.

El `.razor` lleva comentados los llamados de Playwright de cada elemento: la superficie está escrita
como material didáctico. Es el caso tratado en `Guides/E2E-Guide/Caso-HolaMundo-Page.md`.

### Su prueba

`HolaMundoE2ETests : PageTest`, un caso. El `[SetUp]` navega a `http://localhost:5027/HolaMundo` y
**espera el testigo** antes de actuar; el `[Test] MostrarMensaje` llena la frase, la muestra y
afirma `campo-mensaje` con `ToHaveTextAsync`. Sin la espera del testigo la prueba era intermitente
—**1 de 8 corridas en rojo**, según `Caso-HolaMundo-Page.md`—; la evidencia de que el testigo lo
cerró está en `evidencia/2026-09-03-testigo-de-hidratacion/`: `corrida.log` (8 + 5 corridas de
Hola Mundo y de Login, todas en verde) y `corrida-casos-de-login.log`.

## Login

La misma superficie detrás de un acceso por cookies. Es el caso tratado en
`Guides/E2E-Guide/Caso-Login-Page.md`.

| Ruta | Componente | Autorización | Render |
| --- | --- | --- | --- |
| `/` y `/index` | `Paginas/Inicio.razor` | `[Authorize]` | InteractiveServer + `[StreamRendering]` |
| `/HolaMundo` | `Paginas/HolaMundo.razor` | `[Authorize]` | InteractiveServer + `[StreamRendering]` |
| `/login` | `Paginas/Identidad/Ingreso.razor` | pública | **SSR estático a propósito**, `@layout AccesoLayout` |
| `/Error`, `/not-found` | | pública | SSR estático |

### El acceso

`Program.cs` configura cookies —`auth_token`, `HttpOnly`, `SameSite=Strict`, `IsEssential`,
`MaxAge = null`, `LoginPath = /login`, `ReturnUrlParameter = returnurl`— y registra
`IServicioDeIdentidad` (scoped). `Endpoints/IdentidadEndpoints.cs` publica dos endpoints POST,
`/identidad/ingreso` y `/identidad/salida`, mapeados con `app.MapearIdentidad()`. **Son endpoints y
no manejadores de componente** porque la cookie se escribe en una cabecera, y con el circuito ya
establecido la respuesta HTTP ya se envió.

| Pieza | Qué sostiene |
| --- | --- |
| `Servicios/ServicioDeIdentidad.cs` | Credencial de laboratorio `admin`/`admin`. **Un solo desenlace de rechazo**: no dice cuál campo falló |
| `Servicios/CatalogoDeResultados.cs` | Único origen de los textos (`sesion-requerida` → «Ingresá para ver esa superficie.», etc.); un código desconocido cae en el genérico, nunca en el código crudo |
| `IdentidadEndpoints.DestinoSeguro` | Solo rutas locales: sin *open redirect* |
| `Ingreso.razor` | `<form method="post" action="/identidad/ingreso" data-enhance="false">` con `AntiforgeryToken`, campos nativos con `autocomplete` y `required` |
| `Layout/BarraLateral.razor` | Cierre de sesión como `form` POST a `/identidad/salida`, `boton-cerrar-sesion` |

**El guard, tal como actúa** (verificado al escribir las pruebas, según `Caso-Login-Page.md`): sin
sesión, `/HolaMundo` termina en `/login?returnurl=%2FHolaMundo`. Es el **middleware de cookies** el
que corta, con su `LoginPath`; el `<NotAuthorized>` de `Routes.razor` —que redirigiría a
`/login?estado=sesion-requerida`— **no llega a evaluarse** para páginas con `[Authorize]`, y el texto
«Ingresá para ver esa superficie.» del catálogo nunca se muestra. Está anotado como hallazgo no
resuelto en `Caso-Login-Page.md`.

### `data-testid` de Login

`campo-usuario`, `campo-clave`, `boton-ingresar`, `mensaje-resultado` (la banda del catálogo, en
`/login`); `boton-cerrar-sesion` (barra lateral); y los de Hola Mundo en `/HolaMundo` (`estado-app`,
`campo-frase`, `boton-mostrar-frase`, `campo-mensaje`, `mensaje-error`).

### Sus pruebas

`PruebaDeSuperficie : PageTest` es la base abstracta: `UrlBase = http://localhost:5181`,
`Identificador`/`Secreto` = `admin`, `IngresarAsync()` que **ingresa por la superficie** —la cookie la
emite el servidor; no se fabrica—, y `EsperarCircuitoAbiertoAsync()`.

| Clase | Casos |
| --- | --- |
| `LoginE2ETests` | 9: ingreso aceptado; vuelve al destino pedido; un destino externo no se honra; rechazo con el texto del catálogo; **el rechazo no distingue qué campo falló** (compara dos rechazos entre sí); un envío incompleto no sale; sin sesión hay rebote con el destino; el destino sobrevive al rebote; cerrar la sesión revoca el paso |
| `HolaMundoE2ETest` | 1: ingresa, abre `/HolaMundo`, espera el circuito y ejercita la superficie |

La lista con los nombres de método está en [05](05_Pruebas.md).

## Cómo se corren

La aplicación **la levanta quien corre la prueba**, en la URL que la prueba tiene escrita:

| Vía | Cómo |
| --- | --- |
| `scripts/pruebas.sh` | `PROYECTO=holamundo` o `PROYECTO=login`: compila, instala el navegador, levanta la aplicación con `dotnet run` en la URL, prueba y la apaga. `REPETIR=n` repite la batería |
| GitHub Actions | `e2e-holamundo.yml` (con `dotnet run`) y `e2e-login.yml` (con el binario publicado) — ver [06](06_CI-Y-Workflows.md) |
| Visual Studio | Arrancar antes la aplicación con su perfil `http`. **No verificado en Windows** |

Con https no podían correr en CI sin confiar un certificado; se verificó el 2026-09-12 que, escuchando
solo en http, ninguna de las dos redirige (`CHANGELOG.md`).

## Lo que quedó fuera al unificar

Del repositorio de origen no hacía falta traer su `README.md`, `CHANGELOG.md`, el `.slnx`, el
`.devcontainer/` —imagen de Playwright + SDK + `libnss3-tools`, para confiar el certificado de
desarrollo— ni su `scripts/pruebas.sh`: nada de eso es necesario con http. Se rescataron a
`evidencia/` las corridas del template (`2026-09-01-aplicacion-template/`, en el commit `06528d3`) y
del testigo (`2026-09-03-testigo-de-hidratacion/`).

## Cómo verificar todo esto

| Afirmación | Comprobación |
| --- | --- |
| URL fija de cada prueba | `grep -n localhost tests/WebBlazor.{HolaMundo,Login}/*.cs` |
| Testigo en el marcado | `grep -rn estado-app src/WebBlazor.{HolaMundo,Login}/Components/Paginas/HolaMundo.razor` |
| Cantidad de casos | `dotnet test <proyecto> --list-tests` |
| El guard corta en el middleware | `curl -s -o /dev/null -w '%{redirect_url}' http://localhost:5181/HolaMundo` con la aplicación levantada |
