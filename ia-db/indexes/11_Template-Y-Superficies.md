# 11 — El template SDD y la forma de las superficies

> **Propósito**: registrar con qué forma constructiva están escritas las tres aplicaciones, para que
> un agente que toque una superficie la escriba igual y no reintroduzca lo que se retiró.
> **Fuente primaria**: `wwwroot/css/Tokens.css` y `Componentes.css` de cada aplicación,
> `Components/Componentes/`, `Theme/`, la sección «Diseño» de `README.md`,
> `evidencia/2026-09-01-aplicacion-template/` y `Guides/E2E-Guide/Template-SDD-Aplicado.md` (en
> `Lab-E2E.WebBlazor.Documentacion`).
> **Vigencia**: 2026-09-12, commit `06528d3`.

## Las tres aplicaciones, la misma forma

Las tres están construidas con el **template por defecto del Framework SDD**: Hola Mundo y Login
desde el 2026-09-01, Movilidad Urbana desde el 2026-09-04. Tokens del catálogo, clases `mq-`, un
componente propio por patrón, ninguna librería de componentes ni framework de CSS. **Bootstrap se
retiró de las tres.**

Las tres bases de conocimiento aplicadas viven fuera de este repositorio, en el Framework SDD
(`IA/SDD/IA.SDD/`): `Knowledge-Template-HTML-SDD-Default.md` (la forma de la maqueta),
`Knowledge-Template-Blazor-Interactive-Server-SDD-Default.md` (su realización en Blazor) y
`Design-Rules-Web-Generico.md` §2 (el valor de cada token).

## Estilos: dos hojas y ninguna tercera fuente

| Archivo | Qué es |
| --- | --- |
| `wwwroot/css/Tokens.css` | El bloque `:root` del catálogo —61 variables— más la regla de `prefers-reduced-motion` |
| `wwwroot/css/Componentes.css` | Reset, accesibilidad y foco; shells; componentes; utilitarias; **un solo** punto de quiebre, `@media (max-width: 768px)`. Sin un literal de color, tipografía o espaciado |

`App.razor` las enlaza en ese orden y después el `.styles.css` del proyecto. Ningún `.razor`,
`.razor.css` ni `.cs` escribe un valor visual, y no hay `style=` en línea.

**Los `Tokens.css` no son idénticos entre aplicaciones** (verificado el 2026-09-12): Hola Mundo y
Login comparten el suyo byte a byte; el de Movilidad Urbana tiene tres nombres distintos
(`--color-brand-primary-dark`, `--color-brand-primary-tint`, `--line-height-prosa` frente a
`--color-brand-dark`, `--color-brand-tint`, `--line-height-texto`) y algunos valores distintos. Son las
mismas 61 variables por cantidad, no por nombre.

## El vocabulario en C#

| Pieza | Movilidad Urbana | Hola Mundo y Login |
| --- | --- | --- |
| `EstadoDeSuperficie` | `Components/Componentes/EstadoDeSuperficie.cs` | `Theme/EstadoDeSuperficie.cs` |
| Tonos | `Components/Componentes/Tonos.cs` (`TonoDeBanda`) | `Theme/Tono.cs` |
| Íconos y sus tamaños | `Theme/Iconos.cs`, `Theme/RolesDeIcono.cs` | ídem |
| Ubicación del sello | — (solo shell de trabajo) | `Theme/UbicacionDelSello.cs` |

`EstadoDeSuperficie` tiene **diez estados** en las tres aplicaciones: `Cargando`, `Vacio`,
`FiltradoSinResultados`, `ConDatos`, `Indisponible`, `Enviando`, `ErrorDeEntrada`, `ErrorDeOperacion`,
`Exito`, `Reconectando`. Cada superficie elige de esa lista y resuelve cada estado en un bloque
`@if`. Dos estados son distintos cuando la salida que se le ofrece a la persona es distinta: por eso
`Vacio` («cargar la primera») y `FiltradoSinResultados` («limpiar el filtro») no se confunden, y por
eso el ABM ganó una barra de filtros.

## Componentes: uno por patrón

| Componente | Movilidad Urbana | Hola Mundo | Login |
| --- | --- | --- | --- |
| `Icono`, `Insignia`, `Banda`, `EstadoVacio`, `EstadoIndisponible`, `Esqueleto`, `SelloDeVersion` | ✓ | ✓ | ✓ |
| `BarraLateral` | `Componentes/` | `Layout/` | `Layout/` |
| `Grilla` + `ColumnaDeGrilla`, `Campo` + `ContextoDeCampo`, `Asistente` + `PasoDeAsistente`, `Dialogo` + `DialogoHost`, `AvisoDeReconexion` | ✓ | — | — |
| `Redireccion` | — | — | ✓ |
| Reconexión | `AvisoDeReconexion` (banda, no bloquea; con `.razor.css` y `.razor.js` propios) | `ReconnectModal` del andamiaje, restilizado | ídem |

**Ninguna superficie reimplementa uno de ellos en línea.** Es la regla que conviene verificar antes
de agregar marcado nuevo.

Mapa patrón del catálogo → componente en Movilidad Urbana (de la sección «Diseño» de `README.md`):
§4.1 navegación lateral → `BarraLateral`; §4.2 tarjeta de acceso → `.mq-tarjeta-entrada` en
`Inicio`; §4.3 grilla → `Grilla` + `ColumnaDeGrilla`; §4.4 formulario → `Campo`; §4.5 asistente →
`Asistente` + `PasoDeAsistente`; §4.8 insignia → `Insignia`; §5 estados → `EstadoVacio`,
`EstadoIndisponible`, `Esqueleto`, `Banda`; diálogo → `Dialogo` + `DialogoHost`; §6 iconografía →
`Icono` + `Iconos` (SVG inline con `currentColor`, grilla de 24, trazo 1.75); identidad de versión →
`SelloDeVersion`.

## Shells

| Shell | Dónde | Composición |
| --- | --- | --- |
| Trabajo | las tres | `MainLayout` → `BarraLateral` + `main#mq-main` + `SelloDeVersion` al pie; en Movilidad Urbana además `DialogoHost` y `AvisoDeReconexion` |
| Acceso | solo Login | `AccesoLayout` → lienzo con tarjeta angosta, identidad, `@Body` y sello, sin navegación |

La transición entre shells es una navegación completa a otra ruta, no un condicional dentro del
layout. Todas llevan el enlace «Ir al contenido» y `FocusOnNavigate` sobre `#mq-main`.

## Desviaciones declaradas de Movilidad Urbana

Del `README.md`, sección «Diseño»:

1. **El render mode se declara en la raíz** (`App.razor`) y no por página, porque el identificador
   de sesión se lee ahí. Hola Mundo y Login sí lo declaran por página.
2. **`EditForm` sin `DataAnnotationsValidator`**: la política vive en `Dominio/Reglas` y la valida el
   servicio; se conserva el error por campo asociado por `aria-describedby`. Hola Mundo sí usa
   anotaciones.
3. **El paso de revisión del asistente es el estado de éxito**, no un cuarto paso.
4. **Anchos de contenido en `ch`**, porque el catálogo no tiene token de ancho.

Y lo que **no aplica**, declarado: shell de acceso, endpoints de identidad y guard (no hay
credenciales), host de avisos efímeros (la evidencia E2E no debe depender de un temporizador),
conmutador y confirmación escrita, y los instrumentos de la maqueta (dataset, barra de validación,
recarga automática).

## Verificación

- Hola Mundo y Login: `Guides/E2E-Guide/Template-SDD-Aplicado.md` lista 19 criterios —18 «cumple»,
  uno «no aplica» (`filtrado-sin-resultados`, sin colección filtrable)— y la corrida quedó en
  `evidencia/2026-09-01-aplicacion-template/`: `verificar.mjs` (Playwright para Node),
  `verificacion.log` con diez comprobaciones en verde y doce capturas (`holamundo-01` … `-07`,
  `login-01` … `-05`).
- Movilidad Urbana: la suite E2E siguió siendo de 22 casos tras aplicar el template, adaptada en
  cuatro puntos — ver [04](04_Interfaz-Y-Pantallas.md#identificadores-que-cambiaron) — y las cuatro
  configuraciones pasaron el 2026-09-04 (`README.md` §Evidencia).

## Cómo verificar todo esto

| Afirmación | Comprobación |
| --- | --- |
| Los `Tokens.css` y en qué difieren | `diff src/MovilidadUrbana.Web/wwwroot/css/Tokens.css src/WebBlazor.HolaMundo/wwwroot/css/Tokens.css` |
| 61 variables por hoja | `grep -cE '^\s*--[a-z0-9-]+\s*:' src/*/wwwroot/css/Tokens.css` |
| Sin literales de color fuera de `:root` | `grep -n '#[0-9a-fA-F]\{3,6\}' src/*/wwwroot/css/Componentes.css` |
| Ningún `style=` en línea | `grep -rn 'style=' --include=*.razor src/` |
| Bootstrap retirado | `grep -rli bootstrap src --include=*.razor --include=*.css` (sin resultados) |
| Un componente por patrón | `ls src/*/Components/Componentes/` |
