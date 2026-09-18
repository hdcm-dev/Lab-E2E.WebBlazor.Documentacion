# Nomenclatura en soluciones .NET — arquitectura en inglés, dominio en español

Instrucciones para un agente que tenga que **nombrar** código nuevo o **renombrar** una solución
existente con este criterio. Es lo que se aplicó a `Lab-E2E.WebBlazor` el 2026-09-18 (commits
`946d023` y `e9dea2a`); el procedimiento de la sección 4 es el que se siguió, con los errores que
hubo y cómo se evitan. Un agente en un contexto nuevo tiene que poder repetirlo sin más
información que este documento y el repositorio.

## 1. La regla, en una frase

**Lo que viene del estándar va en inglés; lo que viene del problema va en español.**

Los estándares de organización de la arquitectura (Clean Architecture, patrones, framework) están
escritos en inglés y fijan **los espacios de nombres, las carpetas, las terminaciones de las clases
y los nombres de las operaciones de patrón**. Las palabras propias del dominio del problema —lo que
el usuario del sistema nombraría— van en español y son **el prefijo o la raíz** del nombre.

```
EncuestasController     LocalidadService     ILocalidadRepository     EncuestaViewModel
└──────┘└────────┘      └───────┘└─────┘     └────────┘└────────┘     └──────┘└───────┘
 dominio  estándar       dominio  estándar     dominio    estándar      dominio  estándar
```

No es una traducción parcial ni un compromiso: es una separación de responsabilidades en el
nombre. El sufijo dice **qué es** la pieza según el estándar; el prefijo dice **de qué trata**.

## 2. Tabla de decisión

Ante cada identificador, preguntar: *¿esta palabra existiría si el sistema fuera de otro negocio?*
Si sí, es del estándar → inglés. Si no, es del dominio → español.

| Categoría | Idioma | Ejemplos |
| --- | --- | --- |
| Carpetas y espacios de nombres de capa | inglés | `Domain`, `Application`, `Infrastructure`, `Presentation`, `Services`, `Pages`, `Controls`, `Converters`, `Components/Shared`, `Contracts`, `Sessions`, `Persistence`, `Entities`, `Rules`, `Abstractions` |
| Carpetas de agrupación por dominio dentro de una capa | español | `Application/Encuestas/`, `Application/Localidades/`, `Features/Productos/` |
| Sufijo de rol de una clase | inglés | `…Controller`, `…Service`, `…Repository`, `…Policy`, `…Rules`, `…Model`, `…ViewModel`, `…Request`, `…Dto`, `…Command`, `…Query`, `…Handler`, `…Page`, `…Tests`, `…TestBase` |
| Raíz de la clase (el concepto) | español | `Localidad`, `Encuesta`, `Provincia`, `Producto`, `Frase` |
| Entidades, atributos y catálogos del dominio | español | `Localidad.CodigoPostal`, `Habitantes`, `Provincia`, `MediosDeTransporte` |
| Operaciones de patrón (CRUD de Repository, Service) | inglés | `GetAllAsync`, `GetByIdAsync`, `AddAsync`, `UpdateAsync`, `DeleteAsync`, `RemoveAsync`, `CountAsync`, `SaveAsync`, `Create`, `Set`, `IsValid` |
| Operaciones de framework y extensión | inglés | `AddApplication`, `AddInfrastructure`, `UseSession`, `OnInitializedAsync`, `OnAppearing` |
| Acciones propias del caso de uso (intención del usuario) | español | `RegistrarAsync`, `ValidarPaso`, `AlternarMedio`, `CrearProductoCommand`, `ObtenerProductosQuery` |
| Reglas de negocio | español, con sufijo de rol en inglés | `LocalidadRules.NombreValido`, `EncuestaRules.EdadValida`, `EncuestaRules.TotalDePasos` |
| Piezas técnicas sin dominio | inglés | `Result`, `AppDbContext`, `SessionContext`, `SessionMiddleware`, `DatabaseInitializer`, `DependencyInjection`, `ValidationProblems`, `ShellNavigationService`, `DeviceSession`, `OnScreenKeyboard` |
| Componentes de UI técnicos (reutilizables, sin dominio) | inglés | `Grid`, `GridColumn`, `Dialog`, `DialogHost`, `Wizard`, `WizardStep`, `FormField`, `Skeleton`, `EmptyState`, `UnavailableState`, `Badge`, `Icon`, `Band`, `Sidebar`, `VersionStamp`, `ReconnectionNotice`, `DecimalEntry`, `InvertedBoolConverter` |
| Páginas técnicas (scaffold) | inglés | `Home`, `NotFound`, `Login`, `Redirect`, `AuthLayout` |
| Páginas de dominio | español | `Localidades`, `Encuesta`, `LocalidadesPage`, `EncuestaPage` |
| Miembros técnicos de ViewModel | inglés | `SearchText`, `IsRefreshing`, `IsLoading`, `Title`, `LoadCommand`, `EditCommand`, `SaveCommand`, `IsFirstStep`, `Progress` |
| Miembros de dominio de ViewModel | español | `Nombre`, `NombreError`, `PuedeRegistrar`, `Resumen`, `Completada`, `Paso` |
| Tipos de estado técnico | inglés | `SurfaceState`, `ListState`, `SignInResults`, `Tone` |
| **Valores** de estado que las guías usan como vocabulario | español | `Cargando`, `ConDatos`, `Vacio`, `FiltradoSinResultados`, `Indisponible`, `SesionRequerida` |
| Nombres de métodos de prueba | español | `RecorreRegistraYMuestraElResumen`, `NoAvanzaConElPaso1Vacio` (describen comportamiento del dominio, no piezas) |
| Helpers de infraestructura de prueba | inglés | `E2ETestBase`, `TestAppServer`, `ApiWebApplicationFactory`, `AppiumSession`, `FindById`, `Tap`, `TypeText`, `WaitFor`, `Capture` |
| Nombres de proyecto y solución | **no se cambian** | `MovilidadUrbana.Web`, `WebBlazor.HolaMundo` |

Casos límite resueltos así:

- **`Session`/`Sesion`**: la entidad que persiste la sesión de aislamiento por navegador es técnica
  (existiría en cualquier negocio) → `Session`. Cambia la tabla de EF (ver §5).
- **Estados de superficie**: el tipo es técnico (`SurfaceState`), los valores quedan en español
  porque las guías E2E los usan como vocabulario didáctico (`Vacio`, `Indisponible`). Se tradujeron
  y se volvieron atrás; no repetirlo.
- **`Theme.Icons`/`IconRoles`**: catálogo técnico → inglés. Los nombres de cada ícono dentro del
  catálogo son del dominio si lo son (`Transporte`), técnicos si no (`Close`).
- **`Result` con `IsSuccess`/`Message`/`Errors`**: pieza técnica completa → todo en inglés.
- **Un `Controller` de dominio**: `EncuestasController` (plural, como el recurso REST) y sus
  acciones siguen las de patrón (`GetAll`, `GetById`, `Create`), no `ObtenerTodas`.

## 3. Lo que NO se traduce nunca

Son contratos observables o prosa; cambiarlos rompe clientes, pruebas o documentación:

| Elemento | Motivo |
| --- | --- |
| Texto visible para la persona (etiquetas, mensajes, títulos) | es el producto |
| URL y rutas (`/localidades`, `/encuesta/{Paso}`, `/login?estado=…`) | contrato público; además la ruta de Blazor exige que el nombre del parámetro coincida con la propiedad → el parámetro `Paso` sigue siendo `Paso` |
| Contrato JSON de la API (nombres de propiedad serializados) | contrato público; si un DTO se renombra por dentro, se conserva el nombre en el JSON |
| `data-testid` (web) y `AutomationId` (MAUI) | los testigos que las pruebas y las guías citan |
| Clases CSS y selectores | el CSS no distingue capas |
| Comentarios y documentación XML (`///`) | prosa didáctica que las guías citan textualmente — **pero los `cref` sí se renombran** (§5) |
| Nombres de proyecto, solución, `.csproj`, workflows | identidad del repositorio, referencias cruzadas en CI y docs |
| Nombres de columnas y tablas ya existentes en una base con datos | migración aparte; en el laboratorio se borran las bases de prueba |

## 4. Procedimiento para renombrar una solución existente

Lo que sigue es el orden que funcionó. Saltarse un paso cuesta una corrida de CI.

### 4.1 Preparar

1. Trabajar sobre `main` limpio con todas las suites en verde **antes** de tocar nada; anotar los
   conteos (unitarias, integración, E2E, dispositivo). Son el criterio de éxito.
2. Confirmar la regla con el dueño del proyecto mostrándole tres o cuatro nombres resueltos
   (`FabricaDeApi` → `ApiWebApplicationFactory`, `ServicioDeLocalidades` → `LocalidadService`,
   `ReglasDeEncuesta` → `EncuestaRules`). Un intento previo «todo en inglés» se descartó y quedó en
   un stash: acordar el criterio primero evita rehacerlo.
3. No tocar carpetas del dueño (`PROMPTs/`, cambios sin commitear ajenos). Stagear rutas explícitas,
   nunca `git add -A` en la raíz.

### 4.2 Construir el glosario

Un JSON `{ "NombreViejo": "NombreNuevo" }` por proyecto, generado a partir de un inventario de
identificadores (`grep -ohE '\b[A-Z][A-Za-z0-9]+\b'` sobre `.cs`, `.razor`, `.xaml`, `.csproj`,
sin `obj/` ni `bin/`) y resuelto con la tabla de §2. Reglas del glosario:

- Solo identificadores **completos** (`ServicioDeLocalidades`), nunca fragmentos (`Servicio`):
  un fragmento se pega en cualquier palabra.
- Incluir las variantes derivadas: interfaz (`IServicioDeLocalidades`), campo generado por
  `[ObservableProperty]` (`textoDeBusqueda` → `searchText`), comando generado por `[RelayCommand]`
  (`EditarCommand` → `EditCommand`), método `partial OnXxxChanged`, archivos `.razor.cs`,
  `.razor.css`, `.razor.js`, `.xaml.cs`.
- Incluir carpetas y espacios de nombres (`Dominio` → `Domain`, `Aplicacion.Encuestas` →
  `Application.Encuestas`).
- Ordenar de más largo a más corto al aplicar, para que `IServicioDeLocalidades` no quede
  parcialmente reemplazado por `ServicioDeLocalidades`.

En el laboratorio salieron 98 entradas comunes + 257 (Web) + 350 (MAUI) + 24 (UITests) + las del
Hola Mundo / Login.

### 4.3 Aplicar sobre el código, respetando la sintaxis

El reemplazo no es un `sed` global: hay que distinguir código de prosa y de contratos. Lo que se
implementó y hace falta reproducir:

- **C# (`.cs`)**: reemplazar por palabra completa **fuera** de literales de cadena y de comentarios.
  En cadenas interpoladas, los huecos `{…}` sí son código y se transforman.
- **Razor (`.razor`)**: escáner que reconoce etiquetas, atributos, directivas `@…` (salvo `@page` y
  `@rendermode`, que llevan rutas y nombres de framework), bloques `@code`, `@{ }`, `@( )` y las
  sentencias sueltas que siguen a un `}` (`else`, `var`). Un atributo se trata como código si es
  `On*`, `@bind*`, o un parámetro de componente (`Model`, `Items`, `Context`, `Value`, `TItem`,
  `State`, `Columns`, …), o si su valor parece expresión; si no, solo se transforman los tokens
  `@expr` embebidos. El texto entre etiquetas es prosa y no se toca.
- **XAML (`.xaml`)**: `x:Class`, `x:DataType`, `x:Name`, `clr-namespace:`, elementos con prefijo
  (`<controles:EntradaDecimal>` → `<controls:DecimalEntry>`), manejadores de eventos y **todos** los
  `{Binding …}` con llaves balanceadas, incluidos los anidados
  (`{Binding EditarCommand, Source={RelativeSource AncestorType={x:Type vm:…}}}`). Un binding sin
  renombrar no falla al compilar: falla en el teléfono, en silencio o con `SIGSEGV`.
- **`.csproj`**: rutas de `<Compile Include>`/`LinkBase` (las pruebas de MAUI compilan las capas como
  archivos enlazados).
- **Archivos y carpetas**: con `git mv`, saltando `obj/`, `bin/`, `wwwroot/` y resultados.

Guardar un `rutas.json` con cada `ruta-vieja → ruta-nueva`; lo usa la documentación (§4.5).

### 4.4 Corregir a mano lo que ningún reemplazo ve

Cada uno de estos costó un ciclo. Revisarlos **antes** del primer build:

| Síntoma | Causa | Corrección |
| --- | --- | --- |
| `CS0104` ambiguo `DependencyInjection` | dos capas exponen la misma clase de extensión | calificar en `Program.cs`: `MovilidadUrbana.ApiWeb.Infrastructure.DependencyInjection.…` |
| `Application` no es una clase | el espacio `MovilidadUrbana.MAUI.Application` tapa `Microsoft.Maui.Controls.Application` | `public partial class App : Microsoft.Maui.Controls.Application` |
| `CS1574` cref no resuelto (**solo en CI**) | la herramienta protege comentarios y deja `<see cref="ReglasDeEncuesta"/>` | pasada aparte sobre los `cref="…"`; compilar con `--no-incremental` (el build incremental local no lo detectó) |
| tabla no existe / datos viejos | la entidad renombrada cambia la tabla; `EnsureCreated` no migra | borrar las bases SQLite de corridas anteriores (`datos-e2e/`) |
| módulo JS 404 | `import("./Components/Shared/AvisoDeReconexion.razor.js")` es una cadena | actualizar la ruta a mano |
| página no recibe el parámetro | `@page "/encuesta/{Paso:int?}"` debe coincidir con la propiedad | mantener `Paso` (no traducir la propiedad) |
| `[ObservableProperty]`/`[RelayCommand]` no encuentran el nombre | el campo o el método fuente no se renombró junto con el uso generado | renombrar origen y uso a la vez (glosario, §4.2) |
| tap en la fila no abre el editor (MAUI) | binding anidado sin renombrar | escáner de llaves balanceadas (§4.3) |
| `mq-paso` reemplazado en clase CSS | reemplazo dentro de un atributo mixto (`class="mq-@Clase"`) | no tocar clases CSS; revisar diffs de atributos con `@` |
| testid `medio-…` traducido | prefijo de `data-testid` construido en código | los `data-testid` no se traducen, ni siquiera sus partes |
| Appium falla antes de la primera pantalla | arranque en frío ~21 s tras instalar (`Skipped 1272 frames`) | reintentar la espera inicial ante `WebDriverException` hasta 120 s |

### 4.5 Actualizar la documentación que cita el código

Las guías citan rutas, clases y líneas (`[E: src/…/Archivo.cs:42]`). Regla: el renombre no agrega
ni quita líneas, así que los números siguen válidos; solo cambian nombres y rutas.

1. Reemplazar las rutas de `rutas.json` y las carpetas derivadas, en todo el texto.
2. Reemplazar los identificadores compuestos (`ServicioDeLocalidades`) en todo el texto.
3. Reemplazar los identificadores **cortos** (`Grilla`, `Entorno`, `Resultado`) **solo dentro de
   bloques** ```` ```csharp ````, ```` ```razor ````, ```` ```xml ```` y entre backticks. Fuera
   de ahí son palabras del español: la primera pasada convirtió «Estandares-Modelo-Ramas» en
   «Estandares-ToModel-Ramas» dentro de un bloque YAML y hubo que revertir con `git checkout`.
4. Verificar que todas las citas `[E: …]` y enlaces relativos resuelven a un archivo existente
   (resolver los `../` relativos al documento, no al repositorio).
5. Actualizar el commit ancla de la evidencia (README y tabla de marcas) al commit del renombre.
6. Declarar la convención en el README del código (sección «Convención de nombres») y en el
   CHANGELOG de los dos repositorios, con lo que se dejó sin traducir y por qué.

### 4.6 Verificar y publicar

1. `dotnet build … -c Release -warnaserror --no-incremental` sobre la solución filtrada sin MAUI.
2. Todas las suites: unitarias, integración de API, ViewModels de MAUI, E2E por navegador de cada
   app, APK, y la suite Appium en el dispositivo. Los conteos tienen que ser los de §4.1.
3. Comprobar que los `data-testid` y `AutomationId` no cambiaron (diff filtrado) y que las clases
   CSS referidas existen en el CSS.
4. Commit con mensaje que declare la regla, lo excluido y la verificación. Push y **esperar la CI**:
   compila desde cero y ve lo que el build incremental no.
5. Devolver el `adb` y detener el devcontainer si se usó el teléfono.

## 5. Para código nuevo

No hace falta nada de §4: aplicar la tabla de §2 al nombrar. Chequeo rápido antes de crear una
clase:

1. ¿Cuál es su rol según el estándar? → ese es el **sufijo**, en inglés.
2. ¿De qué concepto del negocio trata? → ese es el **prefijo**, en español. Si no trata de ninguno,
   es técnica y va toda en inglés.
3. ¿En qué capa vive? → carpeta y espacio de nombres en inglés; subcarpeta de agrupación en
   español si agrupa por concepto.
4. Sus operaciones: las de patrón en inglés; las que expresan una intención del usuario, en español.
5. Lo que la persona ve, las URL, los testigos y el JSON: el idioma del producto, no el del código.

## 6. Referencias

- Aplicación en `Lab-E2E.WebBlazor`: commits `946d023` (migración) y `e9dea2a` (los `cref`), y su
  `README.md`, sección «Convención de nombres».
- Criterio general para arquitecturas .NET: `LAB/Lab-Documentos/Guides/Arquitectura/Dot-NET-Arquitectura-Guide.md`.
- Las guías que citan el código renombrado: [`E2E-Guide/`](E2E-Guide/) y [`Test-Guide/`](Test-Guide/).
