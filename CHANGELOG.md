# Changelog

Todos los cambios relevantes de este repositorio de documentación se registran acá.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

## [Sin publicar] - 2026-08-30

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
  - `03-Mejora-Continuar-Mesa-Evaluadora.md` — marco de orquestación multiagente para
    *spec-driven development*: el ciclo cerrado de revisión, veredicto, corrección y verificación
    que ejecuta la mesa evaluadora. Fija la composición del panel por señales del artefacto y no
    por plantilla, la escala de evidencia E1–E4 —una conjetura sin ancla habilita una pregunta,
    nunca una corrección—, la separación entre quien diseña el parche y quien lo aprueba, la
    reparación en la capa de origen, la lista cerrada de disparadores de escalada al usuario y los
    criterios de parada. Es el marco con el que se revisaron las dos guías de este repositorio.
- **`CHANGELOG.md`** — este archivo.

### Cambiado

- **Ciclo de revisión por panel** sobre las dos guías (9 especialistas a ciegas, 54 hallazgos, 33
  grupos, 41 correcciones aplicadas y verificadas). Lo sustantivo:
  - **`Guides/Beginner-Guide.md`** — §7.4 y §7.9 dejan de pedir `scripts/publicar.sh` y
    `playwright.ps1 install` como pasos previos: el fixture publica e instala por su cuenta. Se
    distingue la publicación dependiente del framework (fixture) de la autocontenida (CI y
    `publicar.sh`), que la guía presentaba como un solo artefacto «idéntico en dev y CI». Se suma la
    tabla de las siete variables de entorno del fixture, dónde vive la base de las pruebas y cómo se
    la impone, y la condición física del paralelismo (WAL y tiempo de espera del bloqueo). Se
    reanclan las citas de §4.5 y §7.4, que habían quedado desfasadas. §8.2 y §8.4 corrigen el grafo
    de dependencias de los jobs; `ci-ok` deja de describirse como resumen de todos. Se quita el
    «95 %» de defectos por navegador, que no estaba medido. §9.1 declara sobre qué estado se corrió
    cada verificación. §9.3 deja de ser bitácora del laboratorio y pasa a ser un par de casos de
    estudio. El Anexo A unifica el nombre del helper con el del código, el Anexo C.1 admite la
    excepción de localizadores por CSS que §6.2 ya reconocía, el Anexo D cubre el segundo sentido de
    «fixture» y la ruta de lectura del Anexo F pasa por lo que §6 da por sabido.
  - **`Guides/Quick-Guide-ABM.md`** — §2.3 reemplaza «lo único que se toca son dos nombres» por la
    lista real de puntos de adaptación; §2.4 suma la marca de sesión sembrada sin la cual el caso 8
    no puede pasar; §2.5 marca como extracto el alta que citaba incompleta y condiciona la matriz a
    las reglas que tenga cada ABM; §2.6 dice que `pruebas.runsettings` se crea a mano y dónde; §2.7
    corrige la contradicción entre su párrafo y su tabla. Se agregan los enlaces a la guía de
    estudio que el preámbulo prometía.
- **`Guides/Beginner-Guide.md`** — §3.2 y §4.3 suman el proyecto de pruebas unitarias y explican por
  qué es hermano del de E2E y no parte de él; §5.2 desarrolla el reparto entre unitarias y E2E; §7.6
  y §7.9 se completan con la traza y con la corrida de unitarias; **§7.11 es nueva** y desarrolla la
  captura de traza —por qué hay que escribirla a mano con el binding de .NET, por qué se graba
  siempre y se conserva solo lo fallido, y qué cuesta—; §8.3 documenta el paso de unitarias de
  `ci.yml` y el criterio de «lo barato primero»; el Anexo A incorpora el `[TearDown]` de la traza a
  la plantilla de la clase base; §9.1 suma la corrida de verificación del 2026-08-24 y §9.2 declara
  lo que quedó sin comprobar del visor de trazas; las tres mejoras propuestas de §9.3 se renuevan,
  porque las anteriores están implementadas.
- **`Guides/Quick-Guide-ABM.md`** — §2.3 describe la traza dentro de la clase base y enlaza a §7.11;
  la lista de verificación suma el control de traza y el de unitarias; §5 registra las dos
  comprobaciones nuevas.
- **`Guides/Beginner-Guide.md`** — §7.7 y §9.3 reflejan que la cantidad de workers pasó a declararse
  en un solo lugar (`NumberOfTestWorkers` del `.runsettings`); §8.6 reemplaza «Sobre el runner
  autoalojado» por «Sobre el runner», con la comparación entre runners de GitHub y propios, el paso
  de `actions/setup-dotnet` y la caché de navegadores; §9.1 suma la corrida de verificación del
  2026-08-24 y §9.3 marca como resueltas las dos observaciones corregidas en el laboratorio. Se
  actualizaron las citas de línea de `ci.yml` y `e2e.yml`, desplazadas por la migración de runner.
- **`Guides/Quick-Guide-ABM.md`** — §2.6 elimina `[assembly: LevelOfParallelism(3)]` del fragmento
  de paralelismo, en línea con el cambio anterior.
- **`README.md`** — deja de ser solo el título del repositorio: describe de qué laboratorio es la
  documentación, indexa las guías con su destinatario y lo que deja cada una, y señala el propósito
  de `PROMPTs/`.
