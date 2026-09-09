# Aplicación del template SDD por defecto a los proyectos base

**Fecha:** 2026-09-01
**Alcance:** `src/WebBlazor.E2E.Base.HolaMundo` y `src/WebBlazor.E2E.Base.Login`
**Bases de conocimiento aplicadas:**

| Documento | Qué aporta |
| --- | --- |
| `Knowledge-Template-HTML-SDD-Default.md` | Forma constructiva de la maqueta: tokens, vocabulario de estados, convención de nombres, anatomías de patrón, accesibilidad y anti-patrones |
| `Knowledge-Template-Blazor-Interactive-Server-SDD-Default.md` | Cómo se lleva esa forma a Blazor Interactive Server sin librería de componentes |
| `Design-Rules-Web-Generico.md` §2 | Valor de referencia de cada token del catálogo |

Los dos proyectos quedan escritos como si los hubiese construido quien redactó esas
bases: el mismo marcado, las mismas clases `mq-`, la misma fuente única de valores
visuales y el mismo reparto entre superficie, componente y servicio.

---

## 1. Qué se aplicó

### 1.1 Tokens y estilos

- `wwwroot/css/Tokens.css` — el bloque `:root` completo del catálogo, con los nombres
  de variable del catálogo y la única regla de `prefers-reduced-motion`. Es idéntico
  en los dos proyectos: la trazabilidad entre diseño e implementación se apoya en que
  el nombre no cambie.
- `wwwroot/css/Componentes.css` — reset acotado, `.mq-sr-only`, `.mq-skip`, foco
  visible, los dos shells, los componentes y el único punto de quiebre de 768px. No
  contiene ni un literal de color, de tipografía ni de espaciado.
- Se retiraron `app.css`, los tres `.razor.css` del andamiaje y la copia de Bootstrap
  de `wwwroot/lib`: reintroducirían una segunda fuente de valores visuales.

### 1.2 Tema

`Theme/Iconos.cs` (trazos SVG de grilla 24 y trazo 1.75, heredando `currentColor`),
`Theme/RolesDeIcono.cs` (24 navegación · 20 tarjeta · 16 inline · 15 fila),
`Theme/Tono.cs`, `Theme/UbicacionDelSello.cs` y `Theme/EstadoDeSuperficie.cs` con el
vocabulario de estados, sin agregados ni recortes.

### 1.3 Componentes propios, uno por patrón

`Icono`, `Insignia`, `Banda`, `EstadoVacio`, `EstadoIndisponible`, `Esqueleto`,
`SelloDeVersion` y —sólo en el proyecto con acceso— `Redireccion`. Ninguna superficie
reimplementa uno de ellos en línea.

### 1.4 Shells

- **Trabajo:** `MainLayout` + `BarraLateral` + `main#mq-main` + sello al pie.
- **Acceso:** `AccesoLayout`, lienzo con tarjeta angosta y sello, sin navegación.
- La transición entre shells es una navegación completa a otra ruta, no un
  condicional adentro del layout de trabajo.

### 1.5 Identidad, en el proyecto Login

- `Paginas/Identidad/Ingreso.razor` **sin `@rendermode`**: SSR estático, campos
  nativos con `autocomplete`, token antifalsificación y `data-enhance="false"`.
- `Endpoints/IdentidadEndpoints.cs` publica `POST /identidad/ingreso` y
  `POST /identidad/salida`: la cookie se emite en el ciclo de request, fuera del
  circuito.
- El cierre de sesión es un `form` POST con el botón adentro, al pie del chrome y a
  un clic desde cualquier superficie del shell de trabajo.
- `Servicios/CatalogoDeResultados.cs` es el único origen de los textos de resultado;
  el rechazo de credenciales es indiferenciado y no expone parámetros de la política.
- Guard en tres capas: ruteo (`AuthorizeRouteView` + `Redireccion` con
  `replace: true`), superficie (`OnInitializedAsync`) y acción (el endpoint).

### 1.6 Identidad de versión

`Servicios/IIdentidadDeVersion.cs` + `IdentidadDeVersion.cs`, registrado como
`Singleton` en `Program.cs` —el único archivo donde se registran servicios—. El sello
se exhibe en las dos ubicaciones obligatorias: el pie del shell de trabajo y el
lienzo de acceso.

---

## 2. Decisiones tomadas al aplicar, declaradas como tales

| Bifurcación | Qué se resolvió | Por qué |
| --- | --- | --- |
| Estructura de carpetas | Se adoptó la del documento Blazor (`Theme/`, `Servicios/`, `Endpoints/`, `Componentes/`, `Paginas/`) conservando la raíz `Components/` que el andamiaje de .NET referencia desde `Program.cs` | Mover la raíz no aporta nada y rompe la convención del SDK |
| Enumerados de vocabulario (`Tono`, `EstadoDeSuperficie`, `UbicacionDelSello`) | Viven en `Theme/` | Es la carpeta que ya se importa globalmente; separarlos obligaría a un segundo `using` en cada superficie |
| UI de reconexión | Se conserva el elemento `<dialog id="components-reconnect-modal">`, su módulo JavaScript y el contrato de clases de estado del circuito; se reemplaza el marcado de adentro por bandas `mq-banda--atencion` / `--error` en una región activa | El esqueleto del documento muestra un `div` suelto, pero el circuito conmuta clases sobre ese elemento y su módulo llama `showModal()`: un `div` dejaría la reconexión muda |
| Aviso de error no manejado (`#blazor-error-ui`) | Se estiliza con la banda de error y queda oculto en reposo | El circuito le escribe el `display` en línea; la hoja sólo define el reposo |
| Foco del contenido principal | `#mq-main:focus-visible { outline: none; }` | Recibe el foco por programa al navegar y no se alcanza con el tabulador: no es un control, y el anillo ahí es ruido. El foco visible **no** se suprime en ningún control |
| Estado `Enviando` de la superficie Hola Mundo | Se declara y se conmuta, aunque la operación no viaje a ningún servicio | El estado de envío es un estado de la superficie; la bandera se setea antes del `await` y se libera en `finally` |
| Estado `Indisponible` de la superficie Hola Mundo | Se declara «no aplica» en un comentario del marcado | La frase no viaja a ningún servicio externo: no hay servicio que pueda no responder |
| `data-testid="mensaje-error"` de la superficie de ingreso | Pasa a llamarse `mensaje-resultado` | La banda publica cualquier código del catálogo —incluido «Cerraste la sesión»—, y el nombre viejo mentía. Ninguna prueba lo referenciaba |
| Página `/logout` | Se retira; el cierre de sesión vive en el chrome como `form` POST | Una superficie de confirmación para una acción reversible es fricción sin consecuencia que graduar |

**Lo que no se tocó:** el `Framework SDD`, los identificadores de prueba que la guía
E2E documenta (`campo-frase`, `boton-mostrar-frase`, `campo-mensaje`,
`campo-usuario`, `campo-clave`, `boton-ingresar`, `boton-cerrar-sesion`), las rutas
(`/`, `/HolaMundo`, `/login`, `/not-found`, `/Error`) ni la credencial de
laboratorio.

---

## 3. Criterios de aceptación, verificados

Los `[enumerable]` se verificaron contando sobre el árbol; los `[interpretativo]`,
leyendo los dos lados y mirando las capturas de `evidencia/2026-09-01-aplicacion-template/`.

| Criterio | Estado | Cómo se comprobó |
| --- | --- | --- |
| `Tokens.css` es el bloque `:root` del catálogo, sin agregados ni quitados | cumple | Comparación contra `Design-Rules-Web-Generico.md` §2 |
| Sin literales de color, tipografía ni espaciado fuera de `:root` | cumple | `grep` de hexadecimales y de `font-size`/`margin`/`padding`/`gap` sin `var(--…)` devuelve cero |
| Ningún `style=` en línea | cumple | `grep -rn "style=" --include=*.razor` devuelve cero |
| Ninguna superficie de identidad declara `@rendermode` | cumple | `Ingreso.razor` no lo declara |
| Identidad y cierre de sesión por `form method="post"` con antifalsificación y navegación mejorada desactivada | cumple | `Ingreso.razor` y `BarraLateral.razor` |
| Ningún componente usa `localStorage` ni `sessionStorage` | cumple | `grep` devuelve cero |
| Todo servicio se registra en `Program.cs` y en ningún otro archivo | cumple | Los dos `Program.cs` |
| Bandera de proceso antes del `await`, liberada en `finally` | cumple | `HolaMundo.razor` |
| Todo componente que suscribe libera sus recursos | cumple | `BarraLateral` implementa `IDisposable` y desuscribe `LocationChanged` |
| Sello de versión en las dos ubicaciones obligatorias | cumple | Capturas `login-01` (lienzo) y `login-03` / `holamundo-03` (pie) |
| Un componente propio por patrón, ninguna página lo reimplementa en línea | cumple | `Components/Componentes/` |
| Los mensajes salen de un catálogo de códigos, sin traza ni detalle técnico | cumple | `CatalogoDeResultados`; la superficie de error sólo expone el identificador de pedido |
| Cada superficie declara vacío, cargando, con datos y error, o declara «no aplica» con su motivo | cumple | `HolaMundo.razor`; `Inicio.razor` declara la ausencia de colección |
| `filtrado-sin-resultados` separado de `vacio` | no aplica | Ninguna superficie presenta colección filtrable; el enumerado lo conserva |
| Todo control tiene `label for` visible | cumple | Capturas `holamundo-03` y `login-01` |
| El foco visible no se suprime en ningún control | cumple | Sólo se suprime en el contenedor `#mq-main`, que no es un control |
| Sin scroll horizontal a 320px | cumple | Medición en el navegador, `verificacion.log` |
| UI de reconexión estilizada y anunciada en región activa | cumple | `ReconnectModal.razor` |
| El guard existe en las tres capas y ninguna expone el motivo | cumple | `Routes.razor`, `Inicio`/`HolaMundo`, endpoints |

**Pendiente declarado.** `tests/WebBlazor.E2E.Base.Login.E2ETests` sigue sin casos: el
recorrido de ingreso, rechazo y cierre de sesión hoy está cubierto por el guion de
`evidencia/`, no por la batería. Escribirlo excede el alcance de esta aplicación.

---

## 4. Cómo se reprodujo

Con el SDK en contenedor, los dos proyectos en la misma red, y el guion de Playwright
del directorio de evidencia:

```bash
docker network create labe2e
docker run -d --name app-holamundo --network labe2e -v "$PWD":/w -w /w \
  -e ASPNETCORE_ENVIRONMENT=Development mcr.microsoft.com/dotnet/sdk:10.0 \
  dotnet run --project src/WebBlazor.E2E.Base.HolaMundo/WebBlazor.E2E.Base.HolaMundo.csproj --urls http://0.0.0.0:8080
docker run -d --name app-login --network labe2e -v "$PWD":/w -w /w \
  -e ASPNETCORE_ENVIRONMENT=Development mcr.microsoft.com/dotnet/sdk:10.0 \
  dotnet run --project src/WebBlazor.E2E.Base.Login/WebBlazor.E2E.Base.Login.csproj --urls http://0.0.0.0:8080

docker run --rm --network labe2e \
  -v "$PWD/evidencia/2026-09-01-aplicacion-template":/e2e -v "$PWD/salida":/salida -w /e2e \
  mcr.microsoft.com/playwright:v1.62.1-noble bash -lc 'npm i playwright@1.62.1 --silent; node verificar.mjs'
```

Salida de la corrida del 2026-09-01: `evidencia/2026-09-01-aplicacion-template/verificacion.log`
—diez comprobaciones, todas en verde— y las doce capturas del mismo directorio.
