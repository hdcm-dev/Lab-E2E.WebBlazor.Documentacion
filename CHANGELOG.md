# Changelog

Todos los cambios relevantes de este repositorio de documentación se registran acá.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

## [Sin publicar] - 2026-09-09

### Añadido

- **`Guides/`** — la documentación de los dos laboratorios pasa a vivir acá, en una sola copia.
  Llegan desde `Lab-E2E.WebBlazor` la guía de estudio (`Beginner-Guide.md`), la receta de ABM
  (`Quick-Guide-ABM.md`), el caso de la encuesta y las cuatro guías de ramas e integración
  continua; y desde `Lab-E2E.WebBlazor.Base` los casos de Hola Mundo y de acceso, el marco
  conceptual, el template SDD aplicado, las notas de GitHub y las tres imágenes. El motivo de la
  mudanza es que varias vivían duplicadas entre los dos repositorios de código.
- **`Guides/E2E-Guide/E2E-Resumen.md`** — documento integrador nuevo, y puerta de entrada al
  conjunto. Cubre el eslabón que ningún otro documento tenía: **del requerimiento hablado a la
  superficie**, antes de que exista una pantalla que mirar. Los tres casos de diseño parten de una
  pantalla ya construida y enseñan el camino de vuelta; el de ida —que es el original de la
  tradición de la que sale el vocabulario, donde el contexto de interacción se define antes que la
  ventana— queda escrito acá como cinco preguntas: qué actos hay que completar, quién los hace, si
  al abandonar en el medio queda algo hecho, qué hace falta tener listo antes de empezar —la que
  más rinde, porque descubre actos que el requerimiento no nombró— y qué puede faltar, fallar o
  tardar. Va con un ejemplo trabajado que deduce la encuesta desde un requerimiento sin pantallas,
  incluido el caso de borde que muestra si el criterio sirve: por qué «ver cuántas van» **no** es
  una superficie propia. El documento hace además dos cosas que faltaban en el conjunto: une los
  dos vocabularios —superficie/promesa/estado por un lado, escenario/contexto/actor por el otro,
  que hasta ahora no se mencionaban entre sí— y declara **quién es dueño de cada tema**, para que
  una corrección se haga en un solo lugar y las repeticiones no diverjan.
- **`Guides/E2E-Guide/Del-Requerimiento-Al-Caso.md` §6.5, nueva** — el caso que aparece apenas el
  catálogo crece: el tramo pide un identificador y se abre un buscador, que es el mismo listado que
  en otro lado es un ABM. La respuesta es que **pertenece a la superficie que lo abre y no a la del
  ABM**, con el fundamento explícito: la superficie no es el marcado, es el marcado más la promesa;
  lo que se reutiliza es el componente. El laboratorio tiene la versión chica de este caso —un
  desplegable alimentado por el ABM— y con ella la regla ya escrita, *un caso vive donde está la
  promesa que verifica, no donde está el dato que usa*; el buscador modal es esa misma regla un
  escalón más arriba. Quedan escritas la separación de los tres dueños —componente, acto anidado y
  ABM—, la regla de qué se prueba de nuevo —**la costura, no el componente**: que lo elegido aterrice
  en el campo correcto, que cerrar sin elegir no deje rastro y que al volver siga lo ya cargado— y
  los dos peligros de reutilizar así: que viajen los botones de editar y borrar, que es una promesa
  negativa de las que no rompen nada al violarse, y el patrón «buscá, y si no está, creala», donde la
  promesa que más se rompe es volver con lo recién creado ya elegido. Se marca en §10.3 que el
  buscador modal no existe en ningún laboratorio.

- **`Guides/E2E-Guide/Del-Requerimiento-Al-Caso.md`, nuevo** — el tramo de análisis se separa a un
  documento propio. Había nacido como §1 de `E2E-Resumen.md` y creció hasta ocupar dos tercios del
  archivo, que dejó de ser una puerta de entrada para ser un tratado. El criterio con el que se
  separa es el mismo con el que se argumentó no unificar todo el conjunto: **un documento por
  pregunta**, y una pregunta se reconoce porque tiene audiencia propia y ritmo de cambio propio.
  El documento declara además **qué clase de cosa es**: `doc_type: metodo-propuesto`, porque ninguno
  de los tres casos de diseño recorre el camino de ida que describe. Su §10 audita afirmación por
  afirmación qué tiene respaldo y qué no, y el resultado es el que ordena su lectura: de los siete
  recursos de interfaz que clasifica, **cuatro existen en los laboratorios** —formulario simple,
  asistente, listado con ficha y modal, cada uno con su archivo— y **tres no existen en ninguno**
  —pestañas, maestro-detalle y página de llegada—, verificado el 2026-09-09 recorriendo las trece
  superficies y las cinco clases de prueba de los dos laboratorios. Las filas de esos tres son
  razonamiento por analogía y quedan marcadas como hipótesis. Las tres eras del diseño de
  formularios quedan declaradas como encuadre y no como afirmación histórica documentada: no se
  citan fuentes de historia de interfaces porque no se investigaron.

- **`Guides/E2E-Guide/E2E-Resumen.md` §1.6, nueva** — qué promesas y qué estados trae cada recurso,
  que es lo que faltaba para poder usar la elección de §1.5. Arranca separando las promesas en dos
  familias: **la del acto sobrevive al cambio de recurso** —es la que sigue siendo cierta si el
  asistente pasa a ser un acordeón— y **las del recurso se reemplazan en bloque con él**; si al
  cambiar el recurso se rompe el caso central, la promesa estaba mal escrita porque afirmaba el cómo.
  Sigue con la tabla por recurso —formulario, asistente, ABM, modal, pestañas, maestro-detalle y
  página de llegada— con las promesas que cada uno agrega y los estados que trae, y con una
  comprobación de que la tabla dice lo que tiene que decir: la conservación aparece en los cinco que
  fragmentan y en ninguno de los dos que no. Cierra con cómo se distingue una promesa de un estado
  —verbo contra sustantivo, se ejercita contra se observa, método contra aserción— y con la prueba
  que los separa cuando hay duda: **un estado nunca lleva caso propio**, aparece dentro de un caso
  como punto de partida o de llegada. Se agrega además §1.6.4, que muestra que P2 no es burocracia:
  si la encuesta la carga un tercero y no cada persona, aparece el acto «cargar varias seguidas», y
  de ahí sale el botón «Cargar otra encuesta» del laboratorio con la mitad que se olvida —reinicia el
  acto pero no borra lo ya registrado—.
- **`Guides/E2E-Guide/E2E-Resumen.md` §1.5.1 y §1.5.2** — la tabla de recursos usaba un solo eje y no
  alcanzaba: un mismo acto divisible se puede montar saltando de página, cambiando de panel o
  superponiendo, y el eje estructural no elige entre esas tres. Se agrega el **eje atencional** —qué
  pasa con el contexto de la persona: el modal se superpone y lo conserva a la vista, el asistente lo
  reemplaza a propósito para concentrar, el maestro-detalle los hace coexistir—, con la regla de que
  los dos ejes se leen en orden: el estructural dice cuántas superficies hay y descarta lo
  incompatible, el atencional elige entre lo que queda. Poner un asistente donde el acto no es
  divisible es un error del primer eje; ponerlo donde la persona necesitaba seguir viendo el resto es
  del segundo, y se paga en abandono y no en datos mal cargados.
  Y se corrige algo que la entrada anterior había dejado mal atado: **conservar lo cargado no es la
  propiedad que define al modal, porque es transversal** —el asistente conserva al volver, las
  pestañas al cambiar, el maestro-detalle al pasar de un detalle a otro—, así que no sirve para
  elegir ningún recurso. Importa por otro motivo, y queda escrito como regla: *cada vez que un
  recurso fragmenta un acto, nace una promesa de conservación, y es la que más se da por sentada*.
  Se da por sentada porque parece trivial, y lo trivial es exactamente lo que nadie escribe. Va con
  la tabla del gesto que la pone a prueba en cada recurso, incluida la fila que más se olvida: al
  volver de una ficha al listado, el filtro que había puesto también es estado que se conserva o se
  pierde.
- **`Guides/E2E-Guide/E2E-Resumen.md` §1.3.4 y §1.5** — dos ajustes que salieron de discutir la
  sección. El **modal** estaba caracterizado por «un punto sin retorno dentro de otro acto», que es
  el caso de la confirmación y no la propiedad general: se redefine como un **acto anidado que
  interrumpe otro sin abandonarlo, conservando el punto de retorno**, lo que cubre además el caso de
  agregar algo a un catálogo sin perder lo cargado, y da el desmentido exacto —si al volver se perdió
  el contexto, era una navegación disfrazada—. Queda anotada su consecuencia para las pruebas:
  conservar el punto de retorno es en sí una promesa, así que un modal lleva dos casos y no uno. Y se
  agrega **§1.3.4, «Cuando el pedido ya trae las necesidades de datos»**: si quien pide llega con los
  datos formulados, el propósito no hace falta para estructurar y se entra directo en §1.4; donde sí
  se paga es en las reglas que la estructura no determina —obligatoriedad, granularidad, qué hacer
  con lo incompleto y de dónde salen los límites—, que son cuatro preguntas puntuales sobre un campo
  y no una entrevista sobre objetivos. A eso se lo llama el *propósito mínimo*.
- **`Guides/E2E-Guide/E2E-Resumen.md` §1, reescrita y ampliada** — la primera versión empezaba con
  un cliente que decía «quiero saber cómo se mueve la gente», que ya es un pedido de información y
  no una necesidad: era la primera conclusión del analista puesta en boca de quien pide. La sección
  ahora plantea el escenario real —alguien tira su problema encima, entero y desordenado, y hay que
  ordenarlo— y se organiza así: por qué el eslabón se volvió necesario, con las tres eras del diseño
  de formularios y la observación de que la era 3 agregó una decisión que las dos anteriores no
  tenían que tomar (§1.1); quién interviene y qué se pregunta cada uno (§1.2); el punto cero, con
  las cinco alturas a las que puede llegar un pedido y el movimiento que corresponde a cada una,
  más el caso incómodo de quien ya decidió y viene a respaldar, y el exploratorio de quien no sabe
  nada —donde la hipótesis reemplaza a la decisión y «¿qué te sorprendería?» es la pregunta que
  rinde— (§1.3); las cinco preguntas de ida (§1.4); **qué recurso representa el acto**, que es la
  regla que faltaba, con la tabla de qué propiedad justifica cada recurso y el par asistente/pestañas
  que se ve igual y es opuesto (§1.5); los retornos, porque la cadena no es una tubería (§1.6); y dos
  ejemplos trabajados de orígenes distintos, uno desde un síntoma y otro desde la exploración, para
  que la sección no enseñe un solo camino (§1.7).
- **`Guides/E2E-Guide/Quick-Guide-Primer-Proyecto.md`** — es el antiguo `E2E-Guides.md` de
  `Lab-E2E.WebBlazor.Base`, renombrado al mudarse para entrar en la familia de nombres de la
  carpeta y decir lo que hace. Conserva las tres capturas del Explorador de pruebas de Visual
  Studio, que se mudaron con él.
- **`Guides/Anexos/workflows/`** — los tres workflows de ejemplo y su README, que las guías de
  ramas citaban y no estaban en ningún repositorio de esta familia. Se traen desde
  `Lab-Documentos.Documentacion`, que es donde viven las cuatro guías de Git de las que estas son
  copia, para que los enlaces resuelvan sin salir del repositorio.

### Cambiado

- **Referencias de todos los documentos mudados** — quedaron cien enlaces relativos rotos y se
  corrigieron todos. Cincuenta y tres los rompió la mudanza: los que apuntaban al código de los dos
  laboratorios ahora salen del repositorio (`../../../Lab-E2E.WebBlazor/src/…` y
  `../../../Lab-E2E.WebBlazor.Base/src/…`), y los cruces entre documentos que antes vivían en
  repositorios distintos ahora son enlaces entre hermanos de carpeta. Los cuarenta y siete
  restantes estaban rotos de antes, en las cuatro guías de Git: apuntaban a una estructura de una
  carpeta por guía —`../Estandares-Modelo-Ramas-Guide/`, `../GitFlow-Practice-Guide/`— que es la
  del repositorio del que se copiaron y que acá nunca existió.
- **Anclas de los índices de cinco documentos** — veintidós enlaces internos escribían el ancla sin
  acentos (`#2-que-promete-esta-superficie`) mientras GitHub los conserva en el identificador que
  genera, así que no saltaban a ninguna parte. Estaban rotos desde antes de la mudanza, en
  `Caso-HolaMundo-Page.md`, `Caso-Login-Page.md`, `Caso-Encuesta-Page.md`,
  `Marco-La-Superficie-Verificable.md` y `Quick-Guide-Primer-Proyecto.md`.
- **`Guides/E2E-Guide/E2E-Resumen.md` vuelve a ser lo que su nombre dice**: el mapa del conjunto. Su
  §1 pasa a ser la cadena en una pantalla, con el diagrama de qué documento cubre cada tramo; el
  vocabulario y la tabla de dueños quedan; y sus criterios propios pasan a ser tres, los que
  sostienen la organización del corpus en vez de los del método. `confidence` sube a **alta**, porque
  lo que afirma es verificable abriendo los documentos que lista.
- **`README.md`** — la sección «Guías» dejaba de estar al día: remitía a `Lab-E2E.WebBlazor` y
  listaba dos documentos de los nueve. Ahora describe las dos carpetas propias con una fila por
  documento y para quién es cada uno.

## [Sin publicar] - 2026-09-06

### Añadido

- **`PROMPTs/Root/Inicio/02-Crear-Una-Solucion.md`** — encarga replantear el ejemplo de páginas
  estáticas de `/LAB/Lab-E2E.StaticHtml` como una aplicación .NET Blazor *interactive server* en
  `/LAB/Lab-Ejemplo`, con SQLite, arquitectura Clean y un único proyecto en la solución.
- **`PROMPTs/Root/Features/01-Aplicar-Template-HTML/`** — dos encargas nuevas de template, ambas
  sobre `/LAB/Lab-E2E.WebBlazor/src/MovilidadUrbana.Web`, que se distinguen por la fuente:
  `Aplicar-Template-HTML-Lab-E2E.WebBlazor.md` toma las dos bases de conocimiento del template SDD
  por defecto, y `Aplicar-Template-HTML-Lab-Ejemplo.md` las de GDA V2
  (`Knowledge-Template-HTML-GDA-V2.md` y `Knowledge-Template-Blazor-Interactive-Server-GDA-V2.md`).
  Quedan así las dos formas constructivas como encargas separadas y comparables.

### Cambiado

- **`PROMPTs/` se reordena por workspace destino**: los tool-prompts que apuntan a
  `/LAB/Lab-E2E.WebBlazor` pasan a `PROMPTs/Root/` —`Solicitudes/01-Crear-Una-Solucion.md` a
  `Root/Inicio/`, y `Features/` a `Root/Features/`, ambos sin cambios de contenido— y los que
  apuntan a `/LAB/Lab-E2E.WebBlazor.Base` viven bajo `PROMPTs/Base/`. `Analisis/` e `Indexado/`
  no se movieron.
- **`PROMPTs/Base/Features/01-Aplicar-Template-HTML/Aplicar-Template-HTML-Lab-E2E.WebBlazor.Base.md`**
  — es el antiguo `PROMPTs/Features/01-Aplicar-Template-HTML/Aplicar-Template-HTML.md`, que siempre
  apuntó a las dos aplicaciones de `/LAB/Lab-E2E.WebBlazor.Base` (`HolaMundo` y `Login`). Cambia de
  nombre y de carpeta, y su título deja de decir «Extracción de comportamientos» para decir lo que
  el cuerpo ya pedía: aplicar el template. El encargo en sí no cambió.
- **`README.md`** — la sección «PROMPTs» describía el orden viejo (`Solicitudes/`, `Analisis/`,
  `Features/` e `Indexado/`); pasa a describir el orden por workspace destino.

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
