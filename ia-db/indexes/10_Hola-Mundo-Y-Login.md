# 10 — Hola Mundo y Login

> **Propósito**: los dos primeros escalones del laboratorio —`WebBlazor.HolaMundo` (una superficie interactiva y sus estados) y `WebBlazor.Login` (la misma superficie detrás de un acceso por cookies)—: rutas, comportamiento, el guard y su capa que de verdad actúa, el catálogo de resultados, y sus 11 pruebas E2E sin fixture contra URL fija.
>
> **Fuente primaria**: `src/WebBlazor.HolaMundo/`, `src/WebBlazor.Login/` (`Program.cs`, `Endpoints/IdentityEndpoints.cs`, `Services/`, `Components/Routes.razor`, `Components/Pages/`, `Components/Layout/`, `Properties/launchSettings.json`, `*.csproj`), `tests/WebBlazor.HolaMundo.E2ETests/`, `tests/WebBlazor.Login.E2ETests/`, `scripts/pruebas.sh`, `.github/workflows/e2e-holamundo.yml`, `.github/workflows/e2e-login.yml`, `evidencia/2026-09-01-aplicacion-template/`, `evidencia/2026-09-03-testigo-de-hidratacion/`, `evidencia/2026-09-12-unificacion/`, `evidencia/2026-09-12-renombre/`, `CHANGELOG.md` (2026-09-12), commits `11620e9`, `f9f3ca2`, `e0f3e9d`, `946d023`; guías `/LAB/Lab-Documentos/Lab-Documentos/Guides/Testing/Lab-E2E.WebBlazor-Guides/E2E-Guide/Caso-Login-Page.md` y `Template-SDD-Aplicado.md` (misma carpeta).
>
> **Vigencia**: versión 3.1, generada el 2026-10-25 sobre el commit `8fb4c3a` (2026-09-18).
>
> **Vecinos**: tokens, componentes compartidos, `SurfaceState`, `Tone` y los shells en [11](11_Template-Y-Superficies.md); las siete suites, `pruebas.runsettings` y las variables de entorno en [05](05_Pruebas.md); los workflows completos y sus corridas en [06](06_CI-Y-Workflows.md); la tercera web (Movilidad Urbana, con cookie de sesión **sin** credenciales) en [03](03_Sesiones-Y-Persistencia.md) y [04](04_Interfaz-Y-Pantallas.md); las guías de caso en [07](07_Guias.md); el porqué de https→http y del testigo en [08](08_Decisiones-Y-Trampas.md).

---

## 1. Lugar en la escalera

| | Hola Mundo | Login | Movilidad Urbana (referencia) |
| --- | --- | --- | --- |
| Proyecto | `src/WebBlazor.HolaMundo` | `src/WebBlazor.Login` | `src/MovilidadUrbana.Web` |
| Qué suma | Una superficie interactiva con estados | Acceso por cookie, guard, catálogo de resultados | Capas, SQLite, sesión por cookie, ABM y asistente |
| Persistencia | ninguna | ninguna (identidad fija) | SQLite ([03](03_Sesiones-Y-Persistencia.md)) |
| Render mode | por página | por página (login en SSR estático) | en la raíz (`Routes`) |
| Testigo de hidratación | `OnAfterRender` en la página | ídem (copia de la página) | `RendererInfo.IsInteractive` en `MainLayout` |
| Prueba | 1 caso, sin fixture | 10 casos, sin fixture | 22 casos, fixture que publica y levanta |
| URL de la prueba | `http://localhost:5027` (escrita) | `http://localhost:5181` (escrita) | `http://127.0.0.1:<PUERTO\|4173>` o `URL_BASE` (`TestAppServer.StartAsync`; el comentario de `scripts/pruebas.sh` dice «puerto libre», no es así) |
| Workflow | `e2e-holamundo.yml` | `e2e-login.yml` | `e2e.yml` |

Fuentes: README «Estructura» y «Los workflows»; los `.razor`/`.cs` citados abajo. Los `.csproj` de las dos webs son mínimos: `net10.0`, `Nullable`, `ImplicitUsings` y `BlazorDisableThrowNavigationException=true`, sin paquetes.

**Procedencia** (historia por commit):

| Commit | Fecha | Qué pasó |
| --- | --- | --- |
| `11620e9` | 2026-09-12 | Llegan desde `Lab-E2E.WebBlazor.Base` (que se retira) «idénticos byte a byte» como `WebBlazor.E2E.Base.HolaMundo` / `.Login` (CHANGELOG 2026-09-12) |
| `f9f3ca2` | 2026-09-12 | Un workflow por web; pruebas pasan de https a http; Playwright 1.52.0 → 1.62.0 |
| `e0f3e9d` | 2026-09-12 | Se quita el prefijo `E2E.Base` de proyectos, carpetas, namespaces y workflows |
| `946d023` | 2026-09-18 | Renombre inglés/español: `Paginas/`→`Pages/`, `Componentes/`→`Shared/`, `Servicios/`→`Services/`, `Ingreso.razor`→`Pages/Account/Login.razor`, `PruebaDeSuperficie`→`SurfaceTestBase` |

---

## 2. `WebBlazor.HolaMundo`

### 2.1 Composición (`Program.cs`)

`AddRazorComponents().AddInteractiveServerComponents()` · `AddSingleton<IVersionIdentity, VersionIdentity>` · fuera de Development `UseExceptionHandler("/Error")` + `UseHsts` · `UseStatusCodePagesWithReExecute("/not-found")` · `UseHttpsRedirection` · `UseAntiforgery` · `MapStaticAssets` · `MapRazorComponents<App>().AddInteractiveServerRenderMode()`. `Routes.razor` usa `RouteView` (sin autorización) y `FocusOnNavigate` a `#mq-main`.

### 2.2 Rutas

| Ruta | Componente | Render | Contenido |
| --- | --- | --- | --- |
| `/` | `Pages/Home.razor` | SSR estático (sin `@rendermode`) | Tarjeta «Qué demuestra» + enlace a la superficie |
| `/HolaMundo` | `Pages/HolaMundo.razor` | `InteractiveServer` + `[StreamRendering]` | La superficie |
| `/Error` | `Pages/Error.razor` | SSR | `UnavailableState` + `identificador-pedido` (`Activity.Current?.Id ?? TraceIdentifier`) |
| `/not-found` | `Pages/NotFound.razor` | SSR | `EmptyState` con «Volver al inicio» |

Perfiles (`Properties/launchSettings.json`): `http` → `http://localhost:5027`; `https` → `https://localhost:7230;http://localhost:5027`.

### 2.3 La superficie `/HolaMundo`

| Aspecto | Cómo (en `Pages/HolaMundo.razor`) |
| --- | --- |
| Modelo | `FraseModel.Frase`, inicial `"Hola Mundo"`, `[Required]` + `[StringLength(120, MinimumLength = 1)]` |
| Validación | `EditForm` + `DataAnnotationsValidator` + `ValidationMessage`; requisito «Entre 1 y 120 caracteres.» declarado antes del intento |
| Envío válido | `MostrarLaFraseAsync`: bandera `_busy` antes del await (anti doble envío), `_message = Frase.Trim()`, estado `ConDatos` |
| Envío inválido | `OnSignInRejected` → estado `ErrorDeEntrada`, banda `mensaje-error` |
| Estados presentados | `Vacio` (`EmptyState`), `Enviando` (`Skeleton`), `ConDatos` (tarjeta con `campo-mensaje`), `ErrorDeEntrada` (banda). `Indisponible` declarado «no aplica» |
| Región activa | `<p role="status" aria-live="polite">` con `_announcement` |
| Testigo | `<span data-testid="estado-app" data-interactivo="@_interactive">`, arranca `"false"`; `OnAfterRender(primeraVez)` lo pasa a `"true"` (solo corre del lado del circuito) |

`data-testid` del proyecto (contados con `grep`): `campo-frase`, `boton-mostrar-frase`, `campo-mensaje`, `estado-app`, `mensaje-error`, `identificador-pedido`, `sello-version`.

---

## 3. `WebBlazor.Login`

### 3.1 Composición (`Program.cs`)

Lo de Hola Mundo, más:

| Pieza | Valor |
| --- | --- |
| Servicio de identidad | `AddScoped<IIdentityService, IdentityService>` |
| Esquema | `AddAuthentication(CookieAuthenticationDefaults.AuthenticationScheme).AddCookie(...)` |
| `Cookie.Name` | `auth_token` |
| `LoginPath` | `IdentityEndpoints.SuperficieDeAcceso` = `/login` |
| `AccessDeniedPath` | `/Error` |
| `ReturnUrlParameter` | `returnurl` |
| `Cookie.IsEssential` / `HttpOnly` / `SameSite` | `true` / `true` / `Strict` |
| `Cookie.MaxAge` | `null` (cookie de sesión del navegador) |
| Autorización | `AddAuthorization()` + `AddCascadingAuthenticationState()`; `UseAuthentication()` + `UseAuthorization()` antes de `UseAntiforgery()` |
| Endpoints | `app.MapearIdentidad()` (después de `MapRazorComponents`) |

### 3.2 Rutas y endpoints

| Ruta | Componente / handler | Render | Acceso |
| --- | --- | --- | --- |
| `/login` | `Pages/Account/Login.razor`, `@layout AuthLayout` | **SSR estático** (sin `@rendermode`) | anónimo |
| `/`, `/index` | `Pages/Home.razor` | `InteractiveServer` + `[StreamRendering]` | `[Authorize]` |
| `/HolaMundo` | `Pages/HolaMundo.razor` | `InteractiveServer` + `[StreamRendering]` | `[Authorize]` |
| `/Error`, `/not-found` | `Pages/Error.razor`, `Pages/NotFound.razor` | SSR | anónimo |
| `POST /identidad/ingreso` | `IdentityEndpoints` | — | form: `identificador`, `secreto`, `returnurl` + antiforgery |
| `POST /identidad/salida` | `IdentityEndpoints` | — | `SignOutAsync` → `/login?estado=sesion-cerrada` |

Perfiles: `http` → `http://localhost:5181`; `https` → `https://localhost:7212;http://localhost:5181`.

Por qué endpoints y no handlers de componente: la cookie se emite en el ciclo de request; con el circuito abierto la respuesta HTTP ya salió (comentarios de `IdentityEndpoints.cs` y `Login.razor`). Los dos `form` llevan `data-enhance="false"` y `<AntiforgeryToken />`.

### 3.3 Identidad de laboratorio

| Pieza | Comportamiento |
| --- | --- |
| `IdentityService.Authenticate` | Una sola credencial: `admin` / `admin` (comparación `Ordinal`). Vacío o blanco → `datos-incompletos`; cualquier otro rechazo → `credenciales-rechazadas` (no dice cuál campo falló). Aceptado → `ClaimsPrincipal` con `ClaimTypes.Name` |
| `AuthenticationResult(bool Aceptado, string Code, ClaimsPrincipal? Principal = null)` | Record en `IIdentityService.cs` |
| `DestinoSeguro(returnurl)` | Acepta solo URI relativa bien formada que empiece con `/` y no con `//`; si no, `/` (evita redirección abierta) |
| Rechazo en `/identidad/ingreso` | `Redirect("/login?estado=<code>")` — **no** conserva `returnurl` |

Catálogo `Services/SignInResults.cs` (los textos salen solo de acá; código desconocido → genérico):

| Código | Texto | Tono | ¿Se muestra alguna vez? |
| --- | --- | --- | --- |
| `credenciales-rechazadas` | «No pudimos validar el ingreso. Revisá el identificador y el secreto.» | `Peligro` | Sí (caso 4 y 5) |
| `sesion-cerrada` | «Cerraste la sesión.» | `Exito` | Sí (caso 9) |
| `sesion-requerida` | «Ingresá para ver esa superficie.» | `Info` | **No** (ver §4) |
| `datos-incompletos` | «Faltan datos para intentar el ingreso.» | `Peligro` | Solo si se saltea el `required` del navegador; sin caso |
| *(genérico)* | «No pudimos completar la operación. Volvé a intentarlo.» | `Peligro` | Sin caso |

`Login.razor` pinta el texto en `<Band data-testid="mensaje-resultado">` cuando llega `?estado=`; el `returnurl` de la query viaja como `input hidden`. Campos nativos con `required` y `autocomplete` (`username`, `current-password`). Sin «Cancelar», declarado.

### 3.4 Shells

| Layout | Dónde | Qué tiene |
| --- | --- | --- |
| `AuthLayout` | `/login` | Sin navegación; `main#mq-main.mq-tarjeta-acceso`, identidad «Ingreso», `VersionStamp` en lienzo |
| `MainLayout` | resto | `Sidebar` (Inicio, Hola Mundo) + `VersionStamp` al pie; en la barra, `form POST /identidad/salida` con `boton-cerrar-sesion` |

Detalle visual de los shells: [11](11_Template-Y-Superficies.md).

`data-testid` del proyecto: los siete de Hola Mundo más `campo-usuario`, `campo-clave`, `boton-ingresar`, `mensaje-resultado`, `boton-cerrar-sesion`.

---

## 4. El guard: tres capas declaradas y la que actúa

```
GET /HolaMundo sin cookie
  │
  ├─▶ middleware de cookies (LoginPath + ReturnUrlParameter) ─▶ /login?returnurl=%2FHolaMundo   ◀── LA QUE ACTÚA
  │     (el efecto lo fija la prueba 7; Caso-Login-Page.md §6 solo dice que el middleware corta
  │      antes de que el Router evalúe <NotAuthorized>; el mecanismo interno no está documentado: no verificado)
  │
  ├─ (1) ruteo:     Routes.razor <AuthorizeRouteView><NotAuthorized> <Redirect NavTarget="/login?estado=sesion-requerida"/>
  │                  └─ camino muerto para páginas con [Authorize]
  ├─ (2) superficie: OnInitializedAsync; si !IsAuthenticated → _state = Indisponible (HolaMundo) / nombre vacío (Home)
  └─ (3) acción:     /identidad/ingreso rechaza → /login?estado=<code> (sin decir qué falló)

POST /identidad/ingreso (admin/admin, returnurl=/HolaMundo) ─▶ SignInAsync (auth_token) ─▶ 302 DestinoSeguro(returnurl)
POST /identidad/salida ─▶ SignOutAsync ─▶ 302 /login?estado=sesion-cerrada
```

Las tres capas están nombradas en comentarios del código («Primera capa del guard: la del ruteo» en `Routes.razor`; «Segunda capa…: la de la superficie» en `HolaMundo.razor`/`Home.razor`; «Tercera capa…: la de la acción» en `IdentityEndpoints.cs`).

**Hallazgo documentado, no resuelto** (guía `/LAB/Lab-Documentos/Lab-Documentos/Guides/Testing/Lab-E2E.WebBlazor-Guides/E2E-Guide/Caso-Login-Page.md` §6): el caso 7 se escribió esperando `?estado=sesion-requerida` y falló; lo que actúa es el middleware de cookies (`LoginPath` + `ReturnUrlParameter`) antes de que el `Router` evalúe `<NotAuthorized>`. Consecuencias: ese `<NotAuthorized>` es camino muerto y `SesionRequerida` nunca se le muestra a nadie. La prueba se ajustó a lo que hace la app; corregir el comportamiento quedó como decisión de diseño pendiente.

**Observación de lectura** (no declarada en README ni guías): en `src/WebBlazor.Login/Components/Pages/HolaMundo.razor` la capa 2 asigna `SurfaceState.Indisponible`, pero el marcado no tiene bloque para ese estado (cae al `else` → `EmptyState`); además el comentario de la misma página dice que `Indisponible` «no aplica» (heredado de la copia de Hola Mundo). Con la capa del middleware delante, el camino debería ser inalcanzable (inferido de la lectura; no ejecutado).

---

## 5. Las pruebas (11 casos, sin fixture)

### 5.1 Qué significa «sin fixture»

| | Hola Mundo | Login |
| --- | --- | --- |
| Clase base | `PageTest` | `SurfaceTestBase : PageTest` |
| URL | absoluta en el `[SetUp]`: `http://localhost:5027/HolaMundo` | `const UrlBase = "http://localhost:5181"` → `ContextOptions() => new() { BaseURL = UrlBase }`; rutas relativas |
| Quién levanta la app | quien corre la prueba (perfil `http` en VS), `scripts/pruebas.sh` o el workflow | ídem |
| Quién instala el navegador | nadie desde la prueba: lo instala el CLI del paquete (script/workflow) o una corrida previa de Movilidad (VS) | ídem |
| Paralelismo | `[Parallelizable(ParallelScope.Self)]` | ídem, en cada una de las 2 clases |
| Sin app levantada | 1 rojo, `net::ERR_CONNECTION_REFUSED` | 10 rojos (`evidencia/2026-09-12-unificacion/`) |

La URL se escribe en dos lados que deben coincidir: la prueba y `scripts/pruebas.sh` / el `env` del workflow (comentario de `scripts/pruebas.sh`; `URL_APP` en `e2e-holamundo.yml:32` y `e2e-login.yml:50`).

### 5.2 `WebBlazor.HolaMundo.E2ETests` — 1 caso

| Clase | Caso | `[SetUp]` | Afirma |
| --- | --- | --- | --- |
| `HolaMundoE2ETests` | `MostrarMensaje` | `GotoAsync(…/HolaMundo)` + espera `estado-app[data-interactivo=true]` | Llena `campo-frase` con «Hola mundo! - que tal?», click `boton-mostrar-frase`, `campo-mensaje` tiene ese texto |

Queda una línea comentada `//await Expect(Page.GetByTestId("campo-mensaje")).ToHaveValueAsync(frase);` junto a la vigente `ToHaveTextAsync` (`HolaMundoE2ETests.cs:29`); la copia de Login no la tiene.

### 5.3 `WebBlazor.Login.E2ETests` — 10 casos

`SurfaceTestBase` aporta: `UrlBase`, `Identifier = "admin"`, `Secreto = "admin"`, `IngresarAsync(identificador?, secreto?)` (llena `campo-usuario`/`campo-clave`, click `boton-ingresar`; la cookie la emite el servidor, no se fabrica porque no estaría firmada) y `WaitForOpenCircuitAsync()` (mismo testigo).

| # | Clase · caso | Parte de | Afirma |
| ---: | --- | --- | --- |
| 1 | `LoginE2ETests.IngresoAceptadoAbreLaSuperficieDeTrabajo` | `/login` sin sesión | URL `{UrlBase}/` y heading «Inicio» visible |
| 2 | `…IngresoAceptadoVuelveAlDestinoPedido` | `/login?returnurl=/HolaMundo` | Termina en `/HolaMundo` |
| 3 | `…UnDestinoExternoNoSeHonra` | `returnurl=https://ejemplo.invalido/` | URL sigue bajo `UrlBase/` |
| 4 | `…IngresoRechazadoVuelveAlAccesoConElMensajeDelCatalogo` | secreto `lo-que-no-es` | `mensaje-resultado` contiene «No pudimos validar el ingreso.» |
| 5 | `…ElRechazoNoDistingueQueCampoFallo` | identificador `nadie` vs secreto malo | Los dos textos son **iguales** (se comparan dos observaciones) |
| 6 | `…UnEnvioIncompletoNoSale` | solo usuario | Sigue en `/login`, `mensaje-resultado` no visible (el `required` retiene el envío) |
| 7 | `…LaSuperficieProtegidaExigeSesion` | `GET /HolaMundo` | URL `/login?returnurl=%2FHolaMundo$` y `boton-ingresar` visible |
| 8 | `…ElDestinoSobreviveAlRebote` | `GET /HolaMundo` → ingresar | Termina en `/HolaMundo` |
| 9 | `…CerrarLaSesionRevocaElPaso` | ingresar → `boton-cerrar-sesion` | «Cerraste la sesión.»; luego `/HolaMundo` rebota de nuevo |
| 10 | `HolaMundoE2ETest.MostrarMensaje` | `/login` → ingresar → `/HolaMundo` → testigo | El mismo caso de Hola Mundo, detrás del acceso |

Criterio común (remarks de `LoginE2ETests`): se afirma lo que la persona ve —URL, texto—, nunca la cookie. La superficie de acceso es SSR, así que estos 9 casos no esperan testigo; solo el caso 10, que entra a una superficie interactiva.

### 5.4 Cómo se corren

| Dónde | Hola Mundo | Login |
| --- | --- | --- |
| Visual Studio (README; no verificado) | arrancar `WebBlazor.HolaMundo` con perfil `http`, luego el Explorador | arrancar `WebBlazor.Login` con perfil `http` |
| Docker | `PROYECTO=holamundo scripts/pruebas.sh [navegador]` | `PROYECTO=login scripts/pruebas.sh [navegador]` |
| Intermitencias | `REPETIR=8 PROYECTO=holamundo scripts/pruebas.sh` | `REPETIR=8 PROYECTO=login scripts/pruebas.sh` |
| CI | `e2e-holamundo.yml`: un job en `ubuntu-latest`, build Release, `install --with-deps chromium`, `dotnet run` en Development en `:5027`, `dotnet test --settings pruebas.runsettings`; sube resultados + `aplicacion.log` solo si falla | `e2e-login.yml`: job `publicar` (autocontenido `linux-x64`, artefacto `aplicacion-login`) → matriz de navegadores (`chromium` en push/PR; a pedido `chromium[,firefox[,webkit]]`); el binario corre **en Production** desde `publicacion/` con `chmod +x` |

Disparadores de los dos workflows: `push`/`pull_request` hacia `main` con filtro de rutas `src/WebBlazor.<X>/**`, `tests/WebBlazor.<X>.E2ETests/**` y el propio `.yml`, más `workflow_dispatch`. `URL_BASE` no aplica: la URL está escrita en la prueba. Corridas observadas en GitHub: [06](06_CI-Y-Workflows.md).

**https → http** (CHANGELOG 2026-09-12): con https no corrían en CI sin confiar un certificado; se verificó que, escuchando solo http, ninguna de las dos redirige, aunque ambas llaman a `UseHttpsRedirection` (y `UseHsts` fuera de Development).

### 5.5 Evidencia

| Carpeta | Qué |
| --- | --- |
| `evidencia/2026-09-01-aplicacion-template/` | `verificar.mjs` (Playwright JS, contra `http://app-holamundo:8080` y `http://app-login:8080`; cómo se levantaron esos hosts no está en el repo: lo trae la guía `Template-SDD-Aplicado.md`, contenedores `dotnet run --urls http://0.0.0.0:8080` en Development sobre una red `labe2e`) → `verificacion.log`: 10 OK (inicio, vacío, frase, error de entrada, sin scroll a 320px, guard, rechazo indiferenciado, ingreso, superficie protegida, cierre por POST); 12 capturas (7 holamundo, 5 login). La cita la guía `Template-SDD-Aplicado.md` |
| `evidencia/2026-09-03-testigo-de-hidratacion/` | `corrida.log`: 8 + 8 corridas en verde (16/16, el número que cita `Caso-HolaMundo-Page.md` §7; cada corrida de login con `Total: 1`, la suite tenía entonces un solo caso); `corrida-casos-de-login.log`: 5 corridas de holamundo (1/1) y 5 de login (10/10) |
| `evidencia/2026-09-12-unificacion/` | 3/3 corridas de cada una con el script; falsificaciones sin app (1 y 10 rojos); Login como lo corre `e2e-login.yml`: 10/10 en chromium (3 s) y firefox (10 s) |
| `evidencia/2026-09-12-renombre/` | Tras `e0f3e9d`: holamundo 1/1, login 10/10 |

Los logs de 2026-09-03 y de `unificacion/` nombran `WebBlazor.E2E.Base.*`: son previos a `e0f3e9d` (históricos, según CHANGELOG).

---

## 6. Lo que no prueban

| Sin caso | Motivo / estado |
| --- | --- |
| Estados `ErrorDeEntrada`, `Enviando`, vacío de Hola Mundo (`mensaje-error`, frase de 121 caracteres o en blanco) | No declarado; vacío y error de entrada (frase `"   "`) se miraron una vez en `verificar.mjs` (2026-09-01); `Enviando`, ni eso |
| `sesion-requerida`, `datos-incompletos`, mensaje genérico | El primero es inalcanzable (§4); el segundo lo retiene el navegador |
| `/Error`, `/not-found`, `identificador-pedido`, `sello-version` | Sin caso; `verificar.mjs` solo captura `/ruta-que-no-existe` (`holamundo-05-no-encontrado.png`) sin afirmar nada |
| Antiforgery, atributos de la cookie, control de intentos, hash, accesibilidad | Declarado fuera de alcance en `Caso-Login-Page.md` §7: defensa del servidor, configuración que se lee en `Program.cs`, cosas que no existen (identidad de laboratorio) u otra clase de herramienta |
| Rechazo que conserve `returnurl` | El endpoint no lo reenvía al rebotar por rechazo; ningún caso lo afirma ni lo niega |

---

## 7. Rastros del renombre (`946d023`) en estos dos proyectos

| Dónde | Hoy | Antes | Por qué es rastro |
| --- | --- | --- | --- |
| `Pages/HolaMundo.razor` (ambos proyectos) | `OnInvalidSubmit="OnSignInRejected"` | `AlRechazarLaEntrada` (`git show 946d023^:src/WebBlazor.HolaMundo/Components/Paginas/HolaMundo.razor` l. 39, 162) | Deriva semántica: rechaza la **frase**, no un ingreso; en `WebBlazor.HolaMundo` ni siquiera hay ingreso |
| `Pages/Error.razor` (ambos) | texto visible «El **service** no llegó a resolverlo…» | «El **servicio** no llegó…» | La herramienta tradujo texto visible, contra la regla «el texto que ve la persona no se traduce» (README «Convención de nombres») |
| `Shared/Redirect.razor` (solo Login), `Layout/Sidebar.razor` (ambos) | parámetro/record `NavTarget` | `Destino` | Traducción libre; en `TestAppServer` la misma palabra quedó para una carpeta (ver [05](05_Pruebas.md) §13) |
| `Services/IIdentityService.cs` | `AuthenticationResult(…, string Code, …)` | `ResultadoDeAutenticacion(…, string Codigo, …)` | El XML doc sigue diciendo `<param name="Codigo">`; `Aceptado` y `Principal` quedaron en español |
| `SurfaceTestBase` | `Identifier` junto a `Secreto` | `Identificador` / `Secreto` | Renombre parcial de un par |
| `Login.razor` | propiedad `Code` ← query `estado` | `Codigo` | Mezcla inglés/español en la misma superficie |
| Mapeo de archivos | `Pages/Account/Login.razor`, `AuthLayout`, `IdentityEndpoints`, `SignInResults`, `Shared/` | `Paginas/Identidad/Ingreso.razor`, `AccesoLayout`, `IdentidadEndpoints`, `CatalogoDeResultados`, `Componentes/` | `git show 946d023 --name-status -M` |

Otros rastros de estos proyectos, ya inventariados en el índice general (`PruebaDeSuperficie.UrlBase` en `scripts/pruebas.sh:50` y `e2e-login.yml:11`; `Icono`/`Iconos` en `Theme/Icons.cs` e `Icon.razor`) están en [01](01_Arquitectura.md) §8.3.

Se conservaron (no son rastro): `data-testid`, URL (`/login`, `/HolaMundo`, `/identidad/ingreso`), `MapearIdentidad`, `SuperficieDeAcceso`, nombres de los casos de prueba (en español por regla).

---

## 8. Guías que tratan estos proyectos

Rutas desde la raíz del workspace; el índice completo de guías está en [07](07_Guias.md).

| Guía | Qué responde |
| --- | --- |
| `/LAB/Lab-Documentos/Lab-Documentos/Guides/Testing/Lab-E2E.WebBlazor-Guides/E2E-Guide/Caso-HolaMundo-Page.md` | Superficie, estado, las cinco preguntas de una promesa, por qué una superficie interactiva necesita testigo |
| `/LAB/Lab-Documentos/Lab-Documentos/Guides/Testing/Lab-E2E.WebBlazor-Guides/E2E-Guide/Caso-Login-Page.md` | Promesa negativa (rechazo indiferenciado), SSR sin testigo, mapa de los 10 casos, el hallazgo del `NotAuthorized` |
| `/LAB/Lab-Documentos/Lab-Documentos/Guides/Testing/Lab-E2E.WebBlazor-Guides/E2E-Guide/Template-SDD-Aplicado.md` | La aplicación del template a estas dos webs (cita `evidencia/2026-09-01-aplicacion-template/`) |
| `/LAB/Lab-Documentos/Lab-Documentos/Guides/Testing/Lab-E2E.WebBlazor-Guides/E2E-Guide/Quick-Guide-Primer-Proyecto.md` | Cómo se escribe la primera prueba (remitida desde `Caso-HolaMundo-Page.md`) |

`Caso-HolaMundo-Page.md` §7 enlaza la evidencia con ruta relativa `../../../Lab-E2E.WebBlazor/evidencia/...`, que desde su ubicación actual en `Lab-Documentos` no resuelve al repositorio de código (enlace vencido; no se siguió el resto de los enlaces de la guía).
