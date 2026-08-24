# Changelog

Todos los cambios relevantes de este repositorio de documentación se registran acá.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

## [Sin publicar] - 2026-08-24

### Añadido

- **`Guides/Beginner-Guide.md`** (`doc_id: E2E-00`) — guía de estudio para quien nunca escribió
  una prueba de extremo a extremo. Nueve capítulos y seis anexos: qué es una prueba E2E y dónde se
  ubica frente a las demás, el marco de escenarios/contextos/actores, la anatomía de un proyecto
  E2E en .NET, criterios sobre qué testear y qué no, cómo se escribe y estabiliza un caso
  (localizadores, aserciones que esperan, siembra de datos), lo que aparece cuando la aplicación
  tiene servidor —el circuito de Blazor con render *interactive server*, el aislamiento del estado,
  la publicación previa a la corrida— y la integración con GitHub Actions, incluido el control del
  merge de un pull request y la ejecución a pedido. Se apoya en el laboratorio
  `/LAB/Lab-E2E.WebBlazor`, con marcas de evidencia que separan lo comprobado en el repositorio
  **[E]**, lo verificado por ejecución **[V]**, lo fundamentado en documentación externa **[F]** y
  el criterio del autor **[C]**.
- **`Guides/Quick-Guide-ABM.md`** (`doc_id: E2E-01`) — guía rápida para quien ya escribió pruebas
  E2E y necesita el camino corto para montar las de un ABM: el ciclo de una corrida, siete pasos
  desde poner el contrato en la pantalla hasta atar las pruebas a la integración continua, las
  trampas propias de Blazor *interactive server* y una lista de verificación. Toma como base el ABM
  de localidades del laboratorio y remite a `Beginner-Guide.md` para el fundamento.
- **`PROMPTs/`** — tool-prompts que gobiernan el laboratorio y esta documentación.
  - `01-Crear-Una-Solucion.md` — encarga replantear el laboratorio de páginas estáticas
    `/LAB/Lab-E2E.StaticHtml` como una aplicación .NET Blazor con páginas *interactive server* en
    `/LAB/Lab-E2E.WebBlazor`, con SQLite, Clean Architecture y un único proyecto en la solución,
    más el workflow de GitHub Actions sobre el runner `[self-hosted, i7infra-dev]`.
  - `02-Crear-Developer-Guide.md` — encarga la guía de estudio de `Guides/Beginner-Guide.md`:
    secciones jerárquicas con definiciones, ejemplos, diagramas mermaid y fragmentos de código,
    incluida la construcción de los workflows de GitHub Actions para controlar el merge del PR.
- **`CHANGELOG.md`** — este archivo.

### Cambiado

- **`README.md`** — deja de ser solo el título del repositorio: describe de qué laboratorio es la
  documentación, indexa las guías con su destinatario y lo que deja cada una, y señala el propósito
  de `PROMPTs/`.
