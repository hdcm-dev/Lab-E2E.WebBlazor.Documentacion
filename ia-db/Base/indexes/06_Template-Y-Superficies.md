# 06 — El template SDD y la forma de las superficies

> **Propósito**: registrar con qué forma constructiva están escritas las dos aplicaciones desde el
> 2026-09-01, para que un agente que toque una superficie la escriba igual y no reintroduzca lo que
> se retiró.
> **Fuente primaria**: `Guides/Template-SDD-Aplicado.md`, `wwwroot/css/Tokens.css`,
> `wwwroot/css/Componentes.css`, `Theme/`, `Components/Componentes/` y `Components/Layout/`.
> **Vigencia**: 2026-09-02, commit `6af2049`.

Este dominio no existía en el indexado del 2026-09-01: hasta el commit `f4ee8df` los dos proyectos
eran la plantilla estándar de Blazor con Bootstrap vendorizado. Los commits `d32b4ab` y `eaa151a`
aplicaron el **template por defecto del Framework SDD**, y `0b5c4c7` dejó la memoria de esa
aplicación versionada.

## Las tres bases de conocimiento aplicadas

Según `Guides/Template-SDD-Aplicado.md`:

| Documento | Qué aporta |
| --- | --- |
| `Knowledge-Template-HTML-SDD-Default.md` | Forma de la maqueta: tokens, vocabulario de estados, convención de nombres, anatomías de patrón, accesibilidad y anti-patrones |
| `Knowledge-Template-Blazor-Interactive-Server-SDD-Default.md` | Cómo se lleva esa forma a Blazor Interactive Server sin librería de componentes |
| `Design-Rules-Web-Generico.md` §2 | Valor de referencia de cada token del catálogo |

> Los tres viven fuera de este repositorio, en el Framework SDD. La guía no los copia: los cita.

## Estilos: dos hojas y ninguna tercera fuente

| Archivo | Qué es |
| --- | --- |
| `wwwroot/css/Tokens.css` | El bloque `:root` del catálogo —61 variables— más la única regla de `prefers-reduced-motion`. **Idéntico en los dos proyectos**: la trazabilidad entre diseño e implementación se apoya en que el nombre no cambie |
| `wwwroot/css/Componentes.css` | Reset acotado, accesibilidad y foco; los dos shells; los componentes; las utilitarias con nombre; y **un solo** punto de quiebre, en 768px. Sin un literal de color, tipografía o espaciado |

`App.razor` las enlaza en ese orden —tokens primero, componentes después, porque el segundo consume
las variables del primero— y luego el `.styles.css` del proyecto.

**Se retiraron** `app.css`, los tres `.razor.css` del andamiaje (`MainLayout`, `NavMenu`,
`ReconnectModal`) y la copia completa de Bootstrap de `wwwroot/lib/`: reintroducirían una segunda
fuente de valores visuales. Son ~120.000 líneas borradas entre los dos proyectos.

Secciones de `Componentes.css`, en orden: reset y foco · shell de trabajo y barra lateral · shell de
acceso y tarjeta · componentes (encabezado, botones, campos, insignias, bandas, tarjetas, tabla,
esqueleto, estados vacío e indisponible, ficha clave/valor, diálogo, sello de versión, aviso de error
no manejado, reconexión) · utilitarias con nombre · el punto de quiebre.

## Tema: el vocabulario en C#

`Theme/`, importado globalmente desde `_Imports.razor`:

| Archivo | Qué define |
| --- | --- |
| `Iconos.cs` | Trazos SVG de grilla 24 y trazo 1.75, heredando `currentColor` |
| `RolesDeIcono.cs` | Los cuatro tamaños: 24 navegación · 20 tarjeta · 16 inline · 15 fila |
| `Tono.cs` | El tono de una banda o una insignia |
| `UbicacionDelSello.cs` | `Pie` (shell de trabajo) y `Lienzo` (shell de acceso) |
| `EstadoDeSuperficie.cs` | El vocabulario de estados, diez en total: `Cargando`, `Vacio`, `FiltradoSinResultados`, `ConDatos`, `Indisponible`, `Enviando`, `ErrorDeEntrada`, `ErrorDeOperacion`, `Exito`, `Reconectando` |

Los enumerados de vocabulario viven en `Theme/` y no en una carpeta propia: es la que ya se importa
globalmente, y separarlos obligaría a un segundo `using` en cada superficie.

## Componentes: uno por patrón

`Components/Componentes/` — siete en `HolaMundo`, ocho en `Login`:

| Componente | Para qué |
| --- | --- |
| `Icono` | Envuelve un trazo de `Iconos` con su rol de tamaño |
| `Insignia` | Etiqueta con tono |
| `Banda` | Mensaje de resultado con tono (es lo que usan `mensaje-error` y `mensaje-resultado`) |
| `EstadoVacio` | Superficie sin datos todavía, con acción |
| `EstadoIndisponible` | El servicio no resolvió; con reintento |
| `Esqueleto` | Carga, por filas |
| `SelloDeVersion` | El sello, con su `UbicacionDelSello` |
| `Redireccion` | Solo en `Login`: resuelve un guard navegando con `replace: true` |

**Ninguna superficie reimplementa uno de ellos en línea.** Es la regla que conviene verificar antes
de agregar marcado nuevo.

## Shells

| Shell | Composición |
| --- | --- |
| Trabajo | `MainLayout` → `BarraLateral` + `main#mq-main` + `SelloDeVersion` al pie + `#blazor-error-ui` |
| Acceso | `AccesoLayout` (solo `Login`) → lienzo con tarjeta angosta, identidad, `@Body` y sello |

La transición entre shells es una **navegación completa a otra ruta**, no un condicional adentro del
layout de trabajo.

## Identidad de versión

`Servicios/IIdentidadDeVersion.cs` + `IdentidadDeVersion.cs`, registrado como **singleton** en
`Program.cs` —el único archivo donde se registran servicios—. El sello se exhibe en las dos
ubicaciones obligatorias: el pie del shell de trabajo y el lienzo de acceso.

## Decisiones declaradas al aplicar

`Guides/Template-SDD-Aplicado.md` §2 las lista como bifurcaciones resueltas. Las que más condicionan
un cambio futuro:

| Decisión | Por qué |
| --- | --- |
| Se conserva la raíz `Components/` del andamiaje, con `Theme/`, `Servicios/`, `Endpoints/`, `Componentes/` y `Paginas/` adentro o al lado | Mover la raíz no aporta nada y rompe la convención del SDK |
| Se conserva el `<dialog id="components-reconnect-modal">` y su módulo JS, y se reemplaza solo el marcado de adentro | El circuito conmuta clases sobre ese elemento y su módulo llama `showModal()`: un `div` dejaría la reconexión muda |
| `#blazor-error-ui` se estiliza como banda de error y queda oculto en reposo | El circuito le escribe el `display` en línea; la hoja solo define el reposo |
| `#mq-main:focus-visible { outline: none; }` | Recibe el foco por programa al navegar y no se alcanza con el tabulador. El foco visible **no** se suprime en ningún control |
| La superficie `HolaMundo` declara y conmuta `Enviando` aunque nada viaje a un servicio | El estado de envío es un estado de la superficie |
| La superficie `HolaMundo` declara `Indisponible` como «no aplica», en un comentario | No hay servicio externo que pueda no responder |
| `mensaje-error` de la superficie de ingreso pasa a `mensaje-resultado` | La banda publica cualquier código del catálogo, incluido «Cerraste la sesión»; ninguna prueba lo referenciaba |
| Se retira la página `/logout`; el cierre de sesión vive en el chrome como `form` POST | Una superficie de confirmación para una acción reversible es fricción sin consecuencia que graduar |

**Lo que no se tocó**, según la misma guía: el Framework SDD, los `data-testid` que documenta la guía
E2E, las rutas (`/`, `/HolaMundo`, `/login`, `/not-found`, `/Error`) y la credencial de laboratorio.

## Criterios de aceptación y su verificación

La guía §3 lista 19 criterios con su estado —18 «cumple» y uno «no aplica»
(`filtrado-sin-resultados`, porque ninguna superficie presenta colección filtrable)— y **cómo se
comprobó cada uno**: los enumerables por conteo o `grep` sobre el árbol, los interpretativos leyendo
los dos lados y mirando las capturas.

La corrida quedó versionada en `evidencia/2026-09-01-aplicacion-template/`: `verificar.mjs`,
`verificacion.log` con diez comprobaciones en verde y doce capturas. El comando exacto —dos
contenedores con el SDK, uno con la imagen de Playwright 1.62.1 y una red compartida— está en §4 de
la guía.

**Pendiente declarado por la propia guía**: `tests/WebBlazor.E2E.Base.Login.E2ETests` sigue sin
casos; el recorrido de ingreso, rechazo y cierre está cubierto por el guion de evidencia y no por la
batería. Ver [05_Estado-Y-Divergencias.md](05_Estado-Y-Divergencias.md).

## Cómo verificar todo esto

| Afirmación | Comprobación |
| --- | --- |
| Los `Tokens.css` son idénticos | `diff src/*/wwwroot/css/Tokens.css` |
| Sin literales de color fuera de `:root` | `grep -n '#[0-9a-fA-F]\{3,6\}' src/*/wwwroot/css/Componentes.css` |
| Ningún `style=` en línea | `grep -rn 'style=' --include=*.razor src/` |
| Bootstrap retirado | `ls src/*/wwwroot/lib` (no existe) |
| Un componente por patrón | `ls src/*/Components/Componentes/` |
| Servicios registrados solo en `Program.cs` | `grep -rn 'builder.Services' src/` |
