# 08 — Decisiones y trampas ya pagadas

> **Propósito**: reunir el porqué de las decisiones no obvias y los errores que ya se encontraron y
> se resolvieron, para no revertirlos por «prolijidad» ni volver a pisarlos.
> **Fuente primaria**: `README.md` (secciones «Lo que cambia respecto del ejemplo estático», «Los
> workflows» y «Evidencia») y los comentarios del código citado.

## Decisiones de fondo

### Playwright con el binding de .NET, no el runner de JavaScript

Se usan las vinculaciones oficiales `Microsoft.Playwright.NUnit` con un objetivo concreto: que las
pruebas se **descubran, ejecuten y depuren desde Visual Studio**, sin salir del IDE ni del lenguaje
de la aplicación.

Es una decisión con costo, y conviene tenerlo a la vista. El Explorador de pruebas de Visual Studio
soporta pruebas de JavaScript, pero solo de Mocha, Jasmine, Tape, Jest y Vitest: Playwright no está
en esa lista. A cambio de ganar el IDE se pierden funciones que solo existen en `@playwright/test`:
`--shard`, el reporter `blob` con `merge-reports` y el reporte HTML. Acá el reporte de cada
configuración es un TRX y el paralelismo lo maneja NUnit.

La alternativa —dejar las E2E fuera de la solución, en una carpeta `e2e/` con specs de TypeScript—
es la que eligió `dotnet/eShop`. **Las dos son defendibles**; esta prioriza el IDE.

### Publicar e instalar navegadores en el fixture, no en el build

Atado al build, el paso queda a merced de que el entorno decida compilar: Visual Studio evalúa por
su cuenta si el proyecto está al día y cómo invocar targets de otro proyecto, y cuando esa decisión
no sale como se espera **no hay publicación y todas las pruebas mueren en `OneTimeSetUp`**. En el
fixture corre siempre y de la misma forma en consola, IDE y CI.

`dotnet publish` es incremental: cuando no cambió nada tarda un par de segundos. Se paga ese costo
una vez por corrida a cambio de no ejercitar nunca un binario viejo.

Lo mismo con el navegador: la vía documentada (`pwsh playwright.ps1 install`) exige PowerShell 7
—un producto aparte del PowerShell que trae Windows— y acordarse de correrlo. El paquete expone el
mismo instalador como API, y se instala solo el navegador de la corrida.

### `EnsureCreated` en lugar de migraciones

El laboratorio no versiona el esquema, y así el binario publicado arranca en cualquier máquina sin
pasos previos. No es una omisión: es lo apropiado para el alcance.

## Las seis diferencias con el ejemplo estático

Lo que sigue es lo que **aparece recién cuando la aplicación tiene servidor**. Las decisiones de
fondo —selectores por `data-testid`, nada de esperas fijas, cuatro configuraciones de navegador con
una móvil— se mantienen del laboratorio estático.

### 1. Hay que esperar a que la página sea interactiva

Una aplicación *interactive server* se entrega primero como HTML prerenderizado y recién después se
establece el circuito por WebSocket. En el medio los botones **se ven pero no responden**: un clic
que llegue antes de la conexión se pierde sin dejar rastro, y el síntoma es una prueba que falla de
manera intermitente y solo en las máquinas cargadas.

`MainLayout.razor` publica un testigo con `RendererInfo.IsInteractive`; `EsperarInteractivoAsync` de
`PruebaE2E.cs` lo espera antes de tocar nada.

### 2. El estado es del servidor, así que hay que aislarlo

Detalle propio de Blazor Server: **un circuito no tiene acceso a la petición HTTP** que lo originó,
así que la cookie no se puede leer desde una página. El identificador se lee en `App.razor` —que sí
se renderiza dentro de la petición— y se pasa como parámetro al componente raíz `Routes`, puente
entre el render estático y el interactivo. Mecanismo completo en
[03_Sesiones-Y-Persistencia.md](03_Sesiones-Y-Persistencia.md).

### 3. La aplicación hay que compilarla antes de probarla

En CI se publica **autocontenida** para `linux-x64`, así el binario no depende del runtime del
ejecutor, y **una sola vez** para que todas las configuraciones la reutilicen. En la máquina de
quien desarrolla alcanza con una publicación dependiente del framework.

El fixture admite las dos formas: usa el apphost nativo si está —`MovilidadUrbana.Web.exe` en
Windows, sin extensión en Linux y macOS— y si no arranca con `dotnet MovilidadUrbana.Web.dll`.
**El nombre fijo de Linux era justamente lo que hacía fallar el descubrimiento en Windows.**

Trampa que cuesta un rato encontrar: **ASP.NET Core toma el directorio actual como raíz de
contenido**. Si se lanza el binario desde otra carpeta, `wwwroot` no se encuentra, los recursos
estáticos se sirven **vacíos —con `200` y `Content-Length: 0`, no con `404`—** y el circuito nunca
arranca porque `blazor.web.js` llega en blanco. Por eso el fixture fija `WorkingDirectory` en la
carpeta de la publicación.

### 4. Menos JavaScript, menos intermitencia

En la versión estática hubo que corregir dos defectos alrededor del modal de Bootstrap: el clic que
llegaba durante la animación de apertura y el orden del manejador de `data-bs-dismiss`. Acá el
diálogo es marcado propio gobernado por el estado del componente, así que esa clase de carrera no
existe y **no hace falta desactivar las animaciones**.

### 5. El enlace de datos tiene que escuchar el evento correcto

`FillAsync` dispara `input`, no `change`. Con el `@bind` por defecto —que escucha `onchange`— el
valor no llega al servidor hasta que el campo pierde el foco, y la validación rechaza un formulario
que en pantalla se ve completo. Los campos usan `@bind:event="oninput"`.

### 6. Con el binding de .NET, el paralelismo llega hasta la clase

NUnit no paraleliza por defecto. Pero subirlo a `ParallelScope.Children` —casos en paralelo dentro
de una misma clase— rompe la integración de Playwright, que lleva un registro de servicios por
worker: la corrida falla con `The given key 'Browser' was not present in the dictionary` y
`Collection was modified; enumeration operation may not execute`.

El límite práctico es **`ParallelScope.Fixtures`**. Es una diferencia real con `fullyParallel: true`
del runner de JavaScript, que reparte caso por caso.

Otra trampa: un `[SetUpFixture]` cubre **su** namespace y los que cuelgan de él, nunca el de arriba.
Puesto en `MovilidadUrbana.E2ETests.Infraestructura` no se ejecuta para las pruebas de
`MovilidadUrbana.E2ETests`, y el síntoma es desconcertante —la URL base llega vacía y Playwright se
queja de la cookie—.

## Trampas menores, ya resueltas

| Trampa | Solución en el repositorio |
| --- | --- |
| La cookie de sesión se emitía también en css y js, que el navegador pide en paralelo, y la primera visita generaba varios identificadores | `MiddlewareDeSesion.EsUnDocumento` filtra por GET, sin extensión y fuera de `/_framework` y `/_blazor` |
| Borrar todas las localidades volvía a sembrarlas | Marca en la tabla `Sesiones` |
| Dos peticiones de la misma sesión sembraban a la vez | `try/catch (DbUpdateException)` en `SembradorDeSesion` |
| Con `EMULAR_MOVIL=true` la emulación podía caer en silencio a escritorio | `ContextOptions()` lanza si Playwright no conoce el descriptor `Pixel 7` |
| El número de workers estaba declarado en dos lados y podía divergir | Se quitó `[assembly: LevelOfParallelism(3)]`; vive solo en `NumberOfTestWorkers` |
| Las carpetas de solución de `Guides` apuntaban a rutas inexistentes | Ahora reproducen el árbol del disco |
| Los artefactos de Actions pierden el bit de ejecución | `chmod +x` antes de arrancar |
| El resumen de la encuesta variaba con el orden de tipeo | Los medios se guardan en el orden del catálogo |
| Leer una salida del proceso con el búfer de la otra llena trababa el `dotnet publish` | Se leen ambas en paralelo |
| `/dev/shm` a 64 MB mata Chromium a media corrida | **Medido**: a esta escala no ocurre. Si apareciera: `--disable-dev-shm-usage` o más `--shm-size` |

## Límites conocidos

- La ejecución desde el Explorador de pruebas de Visual Studio **no se verificó** (no hay Windows en
  la máquina del autor).
- De los workflows **solo se validó la sintaxis YAML**; su comportamiento real no se comprobó.
- El runner autoalojado no admite jobs con `container:`: es él mismo un contenedor y no tiene montado
  el socket de Docker.
