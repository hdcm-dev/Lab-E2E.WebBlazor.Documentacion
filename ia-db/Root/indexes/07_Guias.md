# 07 — Guías de estudio

> **Propósito**: mapear las cuatro familias de guías de `Guides/` para poder ir directo a la que
> responde una pregunta, sin abrirlas todas.
> **Fuente primaria**: `Guides/` y la sección «Guías» de `README.md`.

Son **dos familias en cuatro carpetas**: una sobre pruebas de extremo a extremo, y otra sobre el
modelo de ramas —una guía de estudio y dos guías prácticas—. Se leen desde el repositorio o desde el
Explorador de soluciones, porque las carpetas de solución reproducen el árbol del disco.

## E2E-Guide — pruebas de extremo a extremo

| Documento | Para quién | Qué deja |
| --- | --- | --- |
| `Guides/E2E-Guide/Beginner-Guide.md` | Quien nunca escribió una prueba E2E | Nueve capítulos y seis anexos: qué es una E2E, marco de escenarios y actores, anatomía del proyecto en .NET, qué testear, cómo se escribe y estabiliza un caso, lo propio de una aplicación con servidor, y la integración con GitHub Actions |
| `Guides/E2E-Guide/Quick-Guide-ABM.md` | Quien ya escribió pruebas E2E | La receta corta para montar las de un ABM: siete pasos, las trampas de Blazor *interactive server* y una lista de verificación |

> Los dos documentos existen **también** en `Lab-E2E.WebBlazor.Documentacion/Guides/E2E-Guide/`
> (verificado el 2026-09-01). Ante una diferencia, comprobar cuál está vigente antes de citarlos.

## GitHub-Action-Guide

`Guides/GitHub-Action-Guide/GitHub-Action-Guide.md` (agregada el 2026-08-31). Va del marco
conceptual —qué es un pipeline, una puerta, qué significa «continuo»— a la anatomía de un workflow
sección por sección, y de ahí a escenarios completos: compilar y probar, E2E, publicar un paquete,
subir un sitio, imagen de contenedor, app móvil.

Los ejemplos salen de workflows que existen y corren en el workspace —los de este laboratorio entre
ellos—; lo ilustrativo se marca como tal con su fuente. Queda al lado de las guías del modelo de
ramas porque explica **la maquinaria que ejecuta las puertas** que aquéllas describen.

## Estandares-Modelo-Ramas-Guide — ramas, integración y releases

La carpeta se llama *Estandares-Modelo-Ramas* y no *GitFlow* a propósito: lo que documenta es la
**elección** entre modelos. GitFlow es uno de los comparados, pero el modelo adoptado es otro
—tronco con ramas de release—.

| # | Documento | De qué trata |
| --- | --- | --- |
| 01 | `01-Marco-De-Referencia.md` | Escenarios, contextos y actores: el vocabulario que usa todo lo demás |
| 02 | `02-Mapa-Conceptual.md` | Entradas por escenario, por rol y por artefacto |
| 03 | `03-Fundamentos-De-Git.md` | Merge, squash, rebase, cherry-pick y tags |
| 04 | `04-GitFlow.md` | El modelo original, sus reglas y la nota de 2020 de su autor |
| 05 | `05-Como-Elegir-El-Modelo.md` | GitHub Flow, GitFlow, GitLab Flow y tronco: comparación y criterio |
| 06 | `06-Modelo-Adoptado.md` | Las siete reglas, guardarraíles y antipatrones |
| 07 | `07-Integracion-Y-Versionado.md` | Ambientes, promoción, versionado semántico y releases |
| 08 | `08-Pull-Requests-Y-Pruebas.md` | Ciclo del pull request, protección de rama y qué verifica el pipeline |

Anexos en `Guides/Estandares-Modelo-Ramas-Guide/Anexos/`: `Glosario.md`, `Plantillas.md`,
`Listas-De-Verificacion.md`, `Preguntas-Frecuentes.md`, `Fuentes.md` y tres workflows de ejemplo
listos para copiar en `Anexos/workflows/` (`ci.yml`, `release.yml`, `auditoria-convergencia.yml`,
con su `README.md`).

## Las dos guías prácticas

Cada una es un recorrido de **ocho escenarios ejecutables** sobre un repositorio real, para un
equipo de tres personas que rotan por los roles. Se practican sobre
[`Lab-GitFlow`](https://github.com/hdcm-dev/Lab-GitFlow), con la aplicación de este laboratorio como
sistema bajo prueba.

| Guía | Qué ejercita |
| --- | --- |
| `Guides/GitFlow-Practice-Guide/` | El **modelo adoptado**: 00-Preparación, 01-Funcionalidad nueva, 02-Defecto con release abierta, 03-Corte de release, 04-PR que rompe la regresión, 05-Emergencia en producción, 06-Versión de demostración, 07-Cierre y auditoría |
| `Guides/GitHubFlow-Practice-Guide/` | El modelo que **no** se adoptó, como línea de base: 00-Preparación, 01-Funcionalidad nueva, 02-Corrección hacia adelante, 03-PR que rompe la regresión, 04-Cambio grande con feature flag, 05-Reversión, 06-Vista previa para demostración, 07-Cierre y auditoría |

El punto de contacto entre las dos familias es concreto: `04-PR-Que-Rompe-La-Regresion.md` es donde
las E2E de este laboratorio entran en la historia, y
`08-Pull-Requests-Y-Pruebas.md` explica cuándo esa verificación bloquea un merge y quién decide.

Las guías del modelo de ramas se tomaron de
[`Lab-GitFlow.Documentacion`](https://github.com/hdcm-dev/Lab-GitFlow.Documentacion) el 2026-08-30,
para poder leerlas junto al código que las pruebas verifican.
