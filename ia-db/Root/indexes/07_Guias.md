# 07 — Guías de estudio

> **Propósito**: mapear las guías de `Guides/` para poder ir directo a la que responde una pregunta,
> sin abrirlas todas.
> **Fuente primaria**: `Guides/` y la sección «Guías» de `README.md`.
> **Vigencia**: revisado el 2026-09-02 sobre el árbol de trabajo, no sobre `HEAD` — ver
> [«Consolidación en curso»](#consolidacion-en-curso) al final.

Son **dos familias en cinco carpetas**: una sobre pruebas de extremo a extremo, otra sobre el modelo
de ramas —guía de estudio y dos guías prácticas—, y la guía de GitHub Actions, que explica la
maquinaria que ejecuta las puertas que las otras describen.

Desde el 2026-09-01 cada guía es **un solo documento**: las carpetas que antes tenían un archivo por
capítulo quedaron con un único `.md` que los consolida. Solo `E2E-Guide/` conserva dos documentos,
porque son dos guías distintas y no dos capítulos.

## Mapa de la carpeta

| Carpeta | Documento | Líneas | `doc_id` |
| --- | --- | --- | --- |
| `E2E-Guide/` | `Beginner-Guide.md` | 1812 | — |
| `E2E-Guide/` | `Quick-Guide-ABM.md` | 325 | — |
| `Estandares-Modelo-Ramas-Guide/` | `Estandares-Modelo-Ramas.md` | 2029 | `GF-GUIA` |
| `GitFlow-Practice-Guide/` | `Guia-Practica-GitFlow.md` | 1178 | `GF-09-ESCENARIOS` |
| `GitHubFlow-Practice-Guide/` | `Guia-Practica-GitHubFlow.md` | 1067 | `GHF-GUIA` |
| `GitHub-Action-Guide/` | `GitHub-Action-Guide.md` | 2974 | — |

Las guías del modelo de ramas llevan **frontmatter YAML** (`doc_id`, `doc_type`, `status`, `origin`,
`confidence`, `owner`, `last_review`, `audience`, `traces`): vienen de `Lab-GitFlow.Documentacion` y
conservan su convención de trazabilidad.

## E2E-Guide — pruebas de extremo a extremo

| Documento | Para quién | Qué deja |
| --- | --- | --- |
| `Guides/E2E-Guide/Beginner-Guide.md` | Quien nunca escribió una prueba E2E | Nueve capítulos y seis anexos: qué es una E2E, marco de escenarios y actores, anatomía del proyecto en .NET, qué testear, cómo se escribe y estabiliza un caso, lo propio de una aplicación con servidor, y la integración con GitHub Actions |
| `Guides/E2E-Guide/Quick-Guide-ABM.md` | Quien ya escribió pruebas E2E | La receta corta para montar las de un ABM: siete pasos, las trampas de Blazor *interactive server* y una lista de verificación |

> Los dos documentos existen **también** en `Lab-E2E.WebBlazor.Documentacion/Guides/E2E-Guide/`
> (verificado el 2026-09-01). Ante una diferencia, comprobar cuál está vigente antes de citarlos.

## GitHub-Action-Guide

`Guides/GitHub-Action-Guide/GitHub-Action-Guide.md` (agregada el 2026-08-31, 2974 líneas). Va del
marco conceptual —qué es un pipeline, una puerta, qué significa «continuo»— a la anatomía de un
workflow sección por sección, y de ahí a escenarios completos: compilar y probar, E2E, publicar un
paquete, subir un sitio, imagen de contenedor, app móvil.

Los ejemplos salen de workflows que existen y corren en el workspace —los de este laboratorio entre
ellos—; lo ilustrativo se marca como tal con su fuente. Queda al lado de las guías del modelo de
ramas porque explica **la maquinaria que ejecuta las puertas** que aquéllas describen.

## Estandares-Modelo-Ramas-Guide — ramas, integración y releases

`Guides/Estandares-Modelo-Ramas-Guide/Estandares-Modelo-Ramas.md` (`doc_id: GF-GUIA`,
`last_review: 2026-08-23`). Documento único que **consolida los trece anteriores**: su frontmatter
los declara en `consolida: [GF-01 … GF-08, GF-AX-GL, GF-AX-PL, GF-AX-LV, GF-AX-PF, GF-AX-FU]`.

La carpeta se llama *Estandares-Modelo-Ramas* y no *GitFlow* a propósito: lo que documenta es la
**elección** entre modelos. GitFlow es uno de los comparados, pero el modelo adoptado es otro
—tronco con ramas de release—.

| Bloque | De qué trata |
| --- | --- |
| Marco de referencia | Escenarios, contextos y actores: el vocabulario que usa todo lo demás |
| Mapa conceptual | Entradas por escenario, por rol y por artefacto |
| Fundamentos de Git | Merge, squash, rebase, cherry-pick y tags |
| GitFlow | El modelo original, sus reglas y la nota de 2020 de su autor |
| Cómo elegir el modelo | GitHub Flow, GitFlow, GitLab Flow y tronco: comparación y criterio |
| Modelo adoptado | Las siete reglas, guardarraíles y antipatrones |
| Integración y versionado | Ambientes, promoción, versionado semántico y releases |
| Pull requests y pruebas | Ciclo del pull request, protección de rama y qué verifica el pipeline |
| Anexos | Glosario, plantillas, listas de verificación, preguntas frecuentes y fuentes |

El documento declara que fuera de él quedan **solo dos cosas**: los tres workflows de ejemplo listos
para copiar en `Anexos/workflows/` (`ci.yml`, `release.yml`, `auditoria-convergencia.yml`, con su
`README.md`) y las dos guías prácticas.

> **Duplicación en pie.** Los cinco anexos siguen existiendo como archivos sueltos en
> `Anexos/` —`Glosario.md`, `Plantillas.md`, `Listas-De-Verificacion.md`, `Preguntas-Frecuentes.md`,
> `Fuentes.md`, entre 84 y 102 líneas cada uno— aunque su contenido ya está adentro del documento
> consolidado. Ante una diferencia, el consolidado es el que el frontmatter declara vigente.

## Las dos guías prácticas

Cada una es un recorrido de **ocho escenarios ejecutables** sobre un repositorio real, para un
equipo de tres personas que rotan por los roles. Se practican sobre
[`Lab-GitFlow`](https://github.com/hdcm-dev/Lab-GitFlow), con la aplicación de este laboratorio como
sistema bajo prueba.

| Guía | Qué ejercita |
| --- | --- |
| `GitFlow-Practice-Guide/Guia-Practica-GitFlow.md` | El **modelo adoptado**: preparación, funcionalidad nueva, defecto con release abierta, corte de release, PR que rompe la regresión, emergencia en producción, versión de demostración, cierre y auditoría |
| `GitHubFlow-Practice-Guide/Guia-Practica-GitHubFlow.md` | El modelo que **no** se adoptó, como línea de base: preparación, funcionalidad nueva, corrección hacia adelante, PR que rompe la regresión, cambio grande con feature flag, reversión, vista previa para demostración, cierre y auditoría |

Las dos declaran leerse «sin depender de ningún otro documento de esta carpeta».

El punto de contacto entre las dos familias es concreto: el escenario del **PR que rompe la
regresión** es donde las E2E de este laboratorio entran en la historia, y el bloque de **pull
requests y pruebas** del documento de estándares explica cuándo esa verificación bloquea un merge y
quién decide.

Las guías del modelo de ramas se tomaron de
[`Lab-GitFlow.Documentacion`](https://github.com/hdcm-dev/Lab-GitFlow.Documentacion) el 2026-08-30,
para poder leerlas junto al código que las pruebas verifican.

<a id="consolidacion-en-curso"></a>

## Consolidación en curso — qué está desalineado

**Hecho**, verificado el 2026-09-02 con `git status` sobre `Lab-E2E.WebBlazor`:

| Estado | Archivos |
| --- | --- |
| Borrados sin commitear (` D`) | Los 8 numerados + `README.md` de `Estandares-Modelo-Ramas-Guide/`; los 8 + `README.md` de `GitFlow-Practice-Guide/`; los 8 + `README.md` de `GitHubFlow-Practice-Guide/` — 27 en total |
| Sin versionar (`??`) | Los tres documentos consolidados |

El último commit del repositorio sigue siendo `c870628` (2026-08-31): **la consolidación está solo
en el árbol de trabajo**.

**Consecuencia comprobable.** Dos artefactos siguen apuntando a los archivos que ya no existen:

| Artefacto | Qué referencia |
| --- | --- |
| `Lab-E2E.WebBlazor.sln` | Las carpetas de solución `Guides` listan los 27 archivos borrados (líneas 33-41, 46-54 y 81-89) y ninguno de los tres consolidados |
| `README.md` | La sección «Guías» enlaza `01-Marco-De-Referencia.md` … `08-Pull-Requests-Y-Pruebas.md` y los `README.md` de las dos guías prácticas (líneas 104-131) |

**Interpretación.** Abrir la solución en Visual Studio muestra las guías con el ícono de archivo
faltante, y los enlaces del README dan 404 en GitHub. Es trabajo a medio terminar, no un error de
este índice: al commitear la consolidación corresponde actualizar el `.sln`, el `README.md` y el
`CHANGELOG.md`, que todavía no la registra.

## Cómo verificar todo esto

| Afirmación | Comprobación |
| --- | --- |
| Qué documentos hay | `find Guides -type f -name '*.md' \| sort` |
| Consolidación sin commitear | `git status --porcelain Guides/` |
| Referencias muertas en la solución | `grep -n 'Guides.\+[0-9][0-9]-' Lab-E2E.WebBlazor.sln` |
| Referencias muertas en el README | `grep -n 'Estandares-Modelo-Ramas-Guide/0' README.md` |
| Anexos duplicados | `wc -l Guides/Estandares-Modelo-Ramas-Guide/Anexos/*.md` frente al bloque de anexos del consolidado |
