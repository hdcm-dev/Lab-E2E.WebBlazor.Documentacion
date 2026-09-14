# ia-db — Lab-E2E.WebBlazor

> **Instrucción para IA**: este archivo es el **punto de entrada único** a la base de conocimiento
> del repositorio `Lab-E2E.WebBlazor`. Leelo entero —es una pantalla— y después cargá **solo** el o
> los índices que la tabla de navegación indique para tu tarea. No recorras el repositorio completo
> ni cargues toda la documentación mientras esta base responda la pregunta; ampliá a las fuentes
> citadas únicamente ante insuficiencia comprobada.

## Necesitás saber… → leé este índice

| Necesitás saber… | Leé |
| --- | --- |
| De qué trata el laboratorio, cuáles son sus aplicaciones, con qué stack y qué decisiones lo definen | [00_MASTER-INDEX.md](indexes/00_MASTER-INDEX.md) |
| Cómo se reparten las capas dentro de cada aplicación de Movilidad Urbana, por qué se repiten y dónde se compone cada una | [01_Arquitectura.md](indexes/01_Arquitectura.md) |
| Qué entidades y reglas de negocio existen, y qué valida cada una | [02_Dominio-Y-Reglas.md](indexes/02_Dominio-Y-Reglas.md) |
| Cómo se aísla el estado por sesión —cookie, encabezado o dispositivo— y cómo se persiste en SQLite | [03_Sesiones-Y-Persistencia.md](indexes/03_Sesiones-Y-Persistencia.md) |
| Qué pantallas tiene la web de Movilidad Urbana, qué hace cada una y con qué `data-testid` se la ubica | [04_Interfaz-Y-Pantallas.md](indexes/04_Interfaz-Y-Pantallas.md) |
| Cómo se corren las pruebas de las cuatro aplicaciones, qué cubre cada suite y qué variables las gobiernan | [05_Pruebas.md](indexes/05_Pruebas.md) |
| Qué hace cada workflow, cuándo se dispara y qué se observó corriendo | [06_CI-Y-Workflows.md](indexes/06_CI-Y-Workflows.md) |
| Dónde están las guías de estudio y cuál responde qué pregunta | [07_Guias.md](indexes/07_Guias.md) |
| Por qué el proyecto está hecho así y qué trampas ya se pagaron | [08_Decisiones-Y-Trampas.md](indexes/08_Decisiones-Y-Trampas.md) |
| Qué significa un término del proyecto | [09_Glosario.md](indexes/09_Glosario.md) |
| Qué hacen Hola Mundo y Login, cómo es el acceso por cookies y cómo se prueban sin fixture | [10_Hola-Mundo-Y-Login.md](indexes/10_Hola-Mundo-Y-Login.md) |
| Con qué forma constructiva se escriben las superficies de las tres aplicaciones web | [11_Template-Y-Superficies.md](indexes/11_Template-Y-Superficies.md) |
| Qué expone la API REST de Movilidad Urbana, cómo identifica la sesión y cómo se prueba | [12_Api-REST.md](indexes/12_Api-REST.md) |
| Qué es la aplicación Android, cómo se compone, cómo se compila sin SDKs en el host y cómo se prueban sus ViewModels | [13_App-Android.md](indexes/13_App-Android.md) |

## Resumen ejecutivo

| Dato | Valor |
| --- | --- |
| Proyecto | `Lab-E2E.WebBlazor` (`LAB/Lab-E2E.WebBlazor`) |
| Tipo | Laboratorio didáctico: tres aplicaciones web de complejidad creciente más una app Android, sus pruebas y sus pipelines |
| Stack | .NET 10 · Blazor Web App *interactive server* · ASP.NET Core Web API con controllers, OpenAPI 3.1 y Scalar · .NET MAUI 10 (solo Android) con CommunityToolkit.Mvvm 8.4.2 · EF Core 10 sobre SQLite · Playwright 1.62 + NUnit 4 · `WebApplicationFactory` para la API · template del Framework SDD, sin librería de componentes |
| Repositorio | `https://github.com/hdcm-dev/Lab-E2E.WebBlazor` · rama `main` |
| Versión | Sin versionar: el `CHANGELOG.md` agrupa por fecha, no por número (última entrada: 2026-09-12) |
| Documentación asociada | `Lab-E2E.WebBlazor.Documentacion` (este repositorio), donde viven también las guías |

**Función principal** — enseñar a escribir, estabilizar y automatizar pruebas de extremo a extremo
con Playwright sobre Blazor, y a atarlas a las puertas de un pipeline de GitHub Actions. Las tres
aplicaciones web escalonan la dificultad: una superficie sola (Hola Mundo), la misma detrás de un
acceso (Login), y un caso de negocio de juguete —*movilidad urbana*: un ABM y una encuesta en tres
pasos— con servidor y base (Movilidad Urbana). Movilidad Urbana tiene además una API REST y una
app Android sobre la misma temática.

**Arquitectura en una línea** — once proyectos: Hola Mundo y Login sin capas; Movilidad Urbana como
**tres aplicaciones independientes** —web Blazor, API REST y app Android— que **repiten a propósito**
sus capas `Dominio/`, `Aplicacion/` e `Infraestructura/` como carpetas propias y no se referencian
entre sí; cada web con su proyecto E2E, más las suites unitaria, de la API y de los ViewModels.

## Estructura

```
Lab-E2E.WebBlazor/
├── Lab-E2E.WebBlazor.sln           Once proyectos + carpetas de solución (src, tests, github-workflow, scripts, Solution Items)
├── Lab-E2E.WebBlazor.SinMaui.slnf  La solución sin la app Android: lo que compila CI sin el workload de MAUI
├── src/
│   ├── MovilidadUrbana.Web/        Blazor interactive server; trae Dominio/, Aplicacion/, Infraestructura/, Sesiones/
│   ├── MovilidadUrbana.ApiWeb/     API REST; trae las mismas tres capas en su propio namespace
│   ├── MovilidadUrbana.MAUI/       App Android (XAML + MVVM); las mismas tres capas + Presentacion/
│   ├── WebBlazor.HolaMundo/        La superficie más simple
│   └── WebBlazor.Login/            La misma superficie detrás de un acceso por cookies
├── tests/
│   ├── MovilidadUrbana.E2ETests/         22 casos Playwright + fixture que publica y levanta la web
│   ├── MovilidadUrbana.UnitTests/        49 casos sobre las reglas de dominio de la web
│   ├── MovilidadUrbana.ApiWeb.Tests/     13 casos sobre la API, en proceso
│   ├── MovilidadUrbana.MAUI.Tests/       18 casos sobre los ViewModels, con las capas enlazadas
│   ├── WebBlazor.HolaMundo.E2ETests/     1 caso, sin fixture
│   └── WebBlazor.Login.E2ETests/         10 casos, sin fixture
├── scripts/                        dotnet.sh, publicar.sh, pruebas.sh (todo por contenedor)
├── .devcontainer/                  Imagen con SDK + JDK 17 + Android SDK + workload; dev.sh para el teléfono USB
├── .github/workflows/              ci.yml, e2e.yml, e2e-holamundo.yml, e2e-login.yml, android.yml, verificacion-entorno.yml
├── evidencia/                      Registros y capturas que respaldan lo que afirman README y guías (seis carpetas)
├── pruebas.runsettings             Navegador, timeouts y workers de las E2E
├── README.md                       Documento de referencia del repositorio (extenso)
└── CHANGELOG.md                    Registro por fecha
```

## Restricciones para IA

- **No inventar**: toda afirmación de estos índices apunta a un archivo del repositorio. Si algo no
  figura acá, verificalo en la fuente antes de afirmarlo.
- **No extraer proyectos compartidos** entre la web, la API y la app Android de Movilidad Urbana: la
  repetición de `Dominio/`, `Aplicacion/` e `Infraestructura/` es **deliberada** (cada aplicación se
  estudia, compila y lleva por separado) — ver [01](indexes/01_Arquitectura.md) y
  [08](indexes/08_Decisiones-Y-Trampas.md). Un cambio en una regla se replica a mano en las tres.
- **No uniformar las tres aplicaciones web**: que Hola Mundo y Login no tengan fixture, que prueben
  contra una URL fija y que cada una tenga un workflow distinto es **deliberado** — ver
  [10](indexes/10_Hola-Mundo-Y-Login.md) y [06](indexes/06_CI-Y-Workflows.md).
- **No proponer cambios de estructura** por «prolijidad»: las decisiones no obvias —publicar en el
  fixture, `ParallelScope.Fixtures`, la cookie de sesión, `EnsureCreated`— están justificadas en
  [08_Decisiones-Y-Trampas.md](indexes/08_Decisiones-Y-Trampas.md).
- **No dar por verificado lo que no lo está**: la ejecución desde el Explorador de pruebas de Visual
  Studio nunca se probó desde esta máquina. Los workflows, en cambio, sí se observaron corriendo — ver
  [06](indexes/06_CI-Y-Workflows.md). La app Android se recorrió en un solo teléfono (moto e6 play).
- **La app Android no se compila desde el host ni desde CI con la solución completa**: exige el
  workload `maui-android`; se usa `.devcontainer/dev.sh` o `android.yml`, y CI compila el filtro
  `Lab-E2E.WebBlazor.SinMaui.slnf` — ver [13](indexes/13_App-Android.md).
- **`Lab-E2E.WebBlazor.Base` ya no existe como repositorio aparte**: se unificó en este el
  2026-09-12. Su conocimiento vigente está en [10](indexes/10_Hola-Mundo-Y-Login.md) y
  [11](indexes/11_Template-Y-Superficies.md); no hay una ia-db separada que consultar.
- **No modificar el repositorio indexado desde esta base**: la ia-db vive en
  `Lab-E2E.WebBlazor.Documentacion`, no en `Lab-E2E.WebBlazor`.
- Si una tarea cambia el código o la documentación, **actualizar esta base de forma incremental** con
  `Actualizar-Indexado.md`, no reconstruirla.

## Manifiesto de generación

- Generado por : `/IA/PROMPTs/IA.Prompts/Tool-Prompts/Indexado-Documentado/Iniciar-Indexado.md`
  (invocado desde `/LAB/Lab-E2E.WebBlazor.Documentacion/PROMPTs/Indexado/Crear-Indexado.md`)
- Alcance      : `/LAB/Lab-E2E.WebBlazor` — modo proyecto, un solo repositorio (once proyectos:
  tres aplicaciones independientes de Movilidad Urbana —web, API, Android—, dos webs simples, tres
  suites E2E, una unitaria, una de la API y una de ViewModels)
- Destino      : `/LAB/Lab-E2E.WebBlazor.Documentacion/ia-db` (estructura canónica plana)
- Fuentes      : `README.md`, `CHANGELOG.md`, `Lab-E2E.WebBlazor.sln`, `Lab-E2E.WebBlazor.SinMaui.slnf`,
  `pruebas.runsettings`, `.gitignore`, `src/` (cinco proyectos), `tests/` (seis), `scripts/`,
  `.devcontainer/`, `.github/workflows/` (seis), `evidencia/` (`.log`, `.txt`, `.mjs` y los `README.md`;
  las capturas solo se referencian). Para el índice 07, el árbol `Guides/` y el `README.md` de
  `Lab-E2E.WebBlazor.Documentacion`. Para las corridas observadas del índice 06, la API pública de
  GitHub Actions consultada el 2026-09-12 (hora local; el último `push` figura como 2026-09-13 UTC)
- Exclusiones  : `.git`, `.nuget/`, `.dotnet/`, `.navegadores/`, `publicacion/`, `datos-e2e/`,
  `datos/`, `resultados/`, `bin/`, `obj/`, las capturas `.png` de `evidencia/`, las fuentes `.ttf` y
  los `.svg` de `Resources/` de la app Android, y lo ignorado por `.gitignore`
- Estado del repositorio : rama `main`, último commit `10ce735` (2026-09-12, «Agregar
  MovilidadUrbana.MAUI y volver independientes las tres aplicaciones»), árbol de trabajo limpio
- Generado     : 2026-09-12 · Versión: 2.0 — regeneración completa. Sucede a la versión 1.1 (commit
  `677d0c9` de este repositorio, indexaba `88e5caa`/`3b53d14` con las capas en proyectos propios),
  que quedó desactualizada por el commit `10ce735` y de la que en el árbol de trabajo solo sobrevivía
  una regeneración parcial sin `README.md`. Índice nuevo: `13_App-Android.md`; `00`, `01`, `03`,
  `05`, `06`, `08`, `09` y `12` reescritos o ampliados; `02`, `04`, `07`, `10` y `11` con rutas y
  vigencia al día
- Actualizar   : `/IA/PROMPTs/IA.Prompts/Tool-Prompts/Indexado-Documentado/Actualizar-Indexado.md`
  (invocado desde `/LAB/Lab-E2E.WebBlazor.Documentacion/PROMPTs/Indexado/Actualizar-Indexado.md`)
