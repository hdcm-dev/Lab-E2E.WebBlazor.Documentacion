# Changelog

Todos los cambios relevantes de este repositorio de documentación se registran acá.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

## [Sin publicar] - 2026-09-03

### Añadido

- **`ia-db/Base/indexes/06_Template-Y-Superficies.md`** — índice nuevo: con qué forma constructiva
  están escritas las dos aplicaciones desde que se les aplicó el template por defecto del Framework
  SDD (commits `d32b4ab`…`6af2049`). Registra las tres bases de conocimiento aplicadas, las dos
  hojas de estilo —`Tokens.css` y `Componentes.css`— como única fuente de valores visuales, y qué se
  retiró a propósito: `app.css`, los `.razor.css` del andamiaje y la copia de Bootstrap. Existe para
  que un agente que toque una superficie la escriba igual y no reintroduzca lo que se sacó.
- **`PROMPTs/Analisis/02-Paginas-Authorized/`** — tool-prompt sobre cómo se prueba una página con
  `[Authorize]` en `WebBlazor.E2E.Base.Login`, con su `OUTPUTs/Notas.md` (`doc_id: AUTH-00`,
  `status: en-debate`): qué hay que hacer *antes* de que la página exista para el navegador de la
  prueba, y el nudo de la cookie que la prueba no puede inventar.

### Cambiado

- **`ia-db/Base/` pasa a versión 1.1** (vigencia 2026-09-02, commit `6af2049`). Se rehicieron los
  índices 00 a 05 por la aplicación del template SDD: el `README.md` cambia la advertencia de estado
  —el repositorio avanzó, pero el proyecto de pruebas del login **no compila**—, el resumen ejecutivo
  deja de decir «Bootstrap (plantilla estándar)», la estructura suma `evidencia/` y las restricciones
  para IA suman «no reintroducir Bootstrap ni una segunda fuente de valores visuales».
- **`ia-db/Root/` pasa a versión 1.1**: `07_Guias.md` se sincroniza con la consolidación de
  `Guides/` —dos familias en cinco carpetas, un documento por guía, con su mapa de líneas y
  `doc_id`— y deja registrada la duplicación en pie de los cinco anexos sueltos y el desalineo
  entre el árbol de trabajo y `HEAD`. `09_Glosario.md` corrige una referencia. El resto de los
  índices no registró cambios.

## [Sin publicar] - 2026-09-01

### Añadido

- **`ia-db/`** — base de conocimiento indexada, pensada para que un agente de IA responda sobre los
  laboratorios sin recorrerlos enteros. Dos workspaces federados, cada uno con su `README.md` como
  punto de entrada único y sus índices temáticos:
  - **`ia-db/Root/`** — indexado de `/LAB/Lab-E2E.WebBlazor`. Diez índices: maestro, arquitectura,
    dominio y reglas, sesiones y persistencia, interfaz y pantallas, pruebas, CI y workflows, guías,
    decisiones y trampas, y glosario.
  - **`ia-db/Base/`** — indexado de `/LAB/Lab-E2E.WebBlazor.Base`. Seis índices: maestro,
    aplicaciones, autenticación, pruebas, CI y workflow, y estado y divergencias. Este último
    registra lo que en ese repositorio está incompleto o copiado sin adaptar, y el `README.md`
    advierte que se lo lea antes de afirmar que algo funciona.
- **`PROMPTs/Indexado/Crear-Indexado.md`** y **`PROMPTs/Indexado/Actualizar-Indexado.md`** —
  tool-prompts que generan y refrescan esos dos workspaces con el procedimiento de
  `/IA/PROMPTs/IA.Prompts/Tool-Prompts/Indexado-Documentado/`.
- **`PROMPTs/Analisis/01-Extraer-Template-SDD-Default/`** — tool-prompt que extrae, de la maqueta
  generada por el Framework SDD, la forma constructiva de sus subagentes de UX y UI, más sus
  `OUTPUTs/`: `Knowledge-Template-HTML-SDD-Default.md` (maqueta HTML/CSS/JS con los cuatro tipos de
  diálogo), `Knowledge-Template-Blazor-Interactive-Server-SDD-Default.md` (el delta para realizarlo
  en Blazor *interactive server* sin librería de componentes), `Index-Knowledge-Filas.md` con las
  dos filas de índice, `Registro-De-Mesa.md` con la convocatoria, los veredictos y la deuda
  declarada, y un `README.md` con el procedimiento de alta en un fork. El conocimiento vive acá a
  propósito: **no se tocó el Framework SDD**.
- **`PROMPTs/Features/01-Aplicar-Template-HTML/`** — tool-prompt que aplica esos dos conocimientos a
  las aplicaciones `HolaMundo` y `Login` de `/LAB/Lab-E2E.WebBlazor.Base`.

### Cambiado

- **`PROMPTs/`** se reordena por tipo de encargo —`Solicitudes/`, `Analisis/`, `Features/`,
  `Indexado/`— y cada tool-prompt con salidas propias pasa a tener su carpeta con `OUTPUTs/`.
  `01-Crear-Una-Solucion.md` se mueve de `Indexado/` a `Solicitudes/`, que es lo que siempre fue.
- **`README.md`** — refleja el nuevo contenido: las guías ya no viven acá y se las indexa en su
  destino, y se suma la sección de `ia-db/` con los dos workspaces y su punto de entrada.

### Quitado

- **`Guides/Beginner-Guide.md`** y **`Guides/Quick-Guide-ABM.md`** — se mudaron al propio
  laboratorio, a `/LAB/Lab-E2E.WebBlazor/Guides/E2E-Guide/`, donde quedan junto a las demás familias
  de guías y al código que citan.
- **`PROMPTs/Indexado/02-Crear-Developer-Guide.md`**,
  **`PROMPTs/Indexado/03-Mejora-Continuar-Mesa-Evaluadora.md`** y
  **`PROMPTs/Fixs/01-Mejoras-Documentacion.md`** — encargos de las guías que se fueron y del ciclo de
  mesa que las revisó; siguen su rastro en los repositorios donde ahora se los ejecuta.

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
- **`Guides/Beginner-Guide.md`** — los cinco bloques de preguntas guía (§1, §5, §6, §7 y §8) suman
  un apartado «Cómo leer estas preguntas»: por cada pregunta, qué criterio busca formar, con qué
  parte del texto y con qué archivo del laboratorio se responde, y un **reparo** que la discute con
  un ejemplo concreto —la pregunta que invita a contestar «todo», la que confunde repetitivo con
  automatizable en E2E, la que pediría borrar el caso de andamiaje, la que se conforma con la
  partición lógica del estado, la que da por buena la respuesta «un solo check»—. Las preguntas
  quedan tal como estaban; el análisis se agrega debajo, dentro de la misma cita.
- **`README.md`** — deja de ser solo el título del repositorio: describe de qué laboratorio es la
  documentación, indexa las guías con su destinatario y lo que deja cada una, y señala el propósito
  de `PROMPTs/`.
