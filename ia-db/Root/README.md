# ia-db — Lab-E2E.WebBlazor

> **Instrucción para IA**: este archivo es el **punto de entrada único** a la base de conocimiento
> del repositorio `Lab-E2E.WebBlazor`. Leelo entero —es una pantalla— y después cargá **solo** el o
> los índices que la tabla de navegación indique para tu tarea. No recorras el repositorio completo
> ni cargues toda la documentación mientras esta base responda la pregunta; ampliá a las fuentes
> citadas únicamente ante insuficiencia comprobada.

## Necesitás saber… → leé este índice

| Necesitás saber… | Leé |
| --- | --- |
| De qué trata el laboratorio, cuáles son sus tres aplicaciones y qué decisiones lo definen | [00_MASTER-INDEX.md](indexes/00_MASTER-INDEX.md) |
| Cómo se reparten las capas de Movilidad Urbana, qué depende de qué y dónde se compone todo | [01_Arquitectura.md](indexes/01_Arquitectura.md) |
| Qué entidades y reglas de negocio existen, y qué valida cada una | [02_Dominio-Y-Reglas.md](indexes/02_Dominio-Y-Reglas.md) |
| Cómo se aísla el estado por sesión y cómo se persiste en SQLite | [03_Sesiones-Y-Persistencia.md](indexes/03_Sesiones-Y-Persistencia.md) |
| Qué pantallas tiene Movilidad Urbana, qué hace cada una y con qué `data-testid` se la ubica | [04_Interfaz-Y-Pantallas.md](indexes/04_Interfaz-Y-Pantallas.md) |
| Cómo se corren las pruebas de las tres aplicaciones, qué cubre cada suite y qué variables las gobiernan | [05_Pruebas.md](indexes/05_Pruebas.md) |
| Qué hace cada workflow —uno por aplicación—, cuándo se dispara y qué se observó corriendo | [06_CI-Y-Workflows.md](indexes/06_CI-Y-Workflows.md) |
| Dónde están las guías de estudio y cuál responde qué pregunta | [07_Guias.md](indexes/07_Guias.md) |
| Por qué el proyecto está hecho así y qué trampas ya se pagaron | [08_Decisiones-Y-Trampas.md](indexes/08_Decisiones-Y-Trampas.md) |
| Qué significa un término del proyecto | [09_Glosario.md](indexes/09_Glosario.md) |
| Qué hacen Hola Mundo y Login, cómo es el acceso por cookies y cómo se prueban sin fixture | [10_Hola-Mundo-Y-Login.md](indexes/10_Hola-Mundo-Y-Login.md) |
| Con qué forma constructiva se escriben las superficies de las tres aplicaciones | [11_Template-Y-Superficies.md](indexes/11_Template-Y-Superficies.md) |

## Resumen ejecutivo

| Dato | Valor |
| --- | --- |
| Proyecto | `Lab-E2E.WebBlazor` (`LAB/Lab-E2E.WebBlazor`) |
| Tipo | Laboratorio didáctico: tres aplicaciones web de complejidad creciente, sus pruebas E2E y su pipeline |
| Stack | .NET 10 · Blazor Web App *interactive server* · EF Core 10 sobre SQLite (Movilidad Urbana) · Playwright 1.62 + NUnit 4 · template del Framework SDD, sin librería de componentes |
| Repositorio | `https://github.com/hdcm-dev/Lab-E2E.WebBlazor` · rama `main` |
| Versión | Sin versionar: el `CHANGELOG.md` agrupa por fecha, no por número (última entrada: 2026-09-12) |
| Documentación asociada | `Lab-E2E.WebBlazor.Documentacion` (este repositorio), donde viven también las guías |

**Función principal** — enseñar a escribir, estabilizar y automatizar pruebas de extremo a extremo
con Playwright sobre Blazor, y a atarlas a las puertas de un pipeline de GitHub Actions. Las tres
aplicaciones escalonan la dificultad: una superficie sola, la misma detrás de un acceso, y un caso de
negocio de juguete —*movilidad urbana*: un ABM y una encuesta en tres pasos— con servidor y base.

**Arquitectura en una línea** — tres aplicaciones web —Hola Mundo y Login sin capas, Movilidad
Urbana con Clean Architecture en carpetas—, cada una con su proyecto E2E y su workflow, más las
pruebas unitarias de Movilidad Urbana.

## Estructura

```
Lab-E2E.WebBlazor/
├── Lab-E2E.WebBlazor.sln         Siete proyectos + carpetas de solución (github-workflow, scripts, Solution Items)
├── src/
│   ├── MovilidadUrbana.Web/          Dominio, Aplicacion, Infraestructura, Components
│   ├── WebBlazor.E2E.Base.HolaMundo/ La superficie más simple
│   └── WebBlazor.E2E.Base.Login/     La misma superficie detrás de un acceso
├── tests/
│   ├── MovilidadUrbana.E2ETests/                22 casos + fixture que levanta la aplicación
│   ├── MovilidadUrbana.UnitTests/               49 casos sobre las reglas de dominio
│   ├── WebBlazor.E2E.Base.HolaMundo.E2ETests/   1 caso, sin fixture
│   └── WebBlazor.E2E.Base.Login.E2ETests/       10 casos, sin fixture
├── scripts/                      dotnet.sh, publicar.sh, pruebas.sh (todo por contenedor)
├── .github/workflows/            ci.yml, e2e.yml, e2e-holamundo.yml, e2e-login.yml, verificacion-entorno.yml
├── evidencia/                    Registros de corridas que respaldan lo que afirman las guías
├── pruebas.runsettings           Navegador, timeouts y workers de las E2E
├── README.md                     Documento de referencia del repositorio (extenso)
└── CHANGELOG.md                  Registro por fecha
```

## Restricciones para IA

- **No inventar**: toda afirmación de estos índices apunta a un archivo del repositorio. Si algo no
  figura acá, verificalo en la fuente antes de afirmarlo.
- **No uniformar las tres aplicaciones**: que Hola Mundo y Login no tengan fixture, que prueben contra
  una URL fija y que cada una tenga un workflow distinto es **deliberado** — ver
  [10](indexes/10_Hola-Mundo-Y-Login.md) y [06](indexes/06_CI-Y-Workflows.md).
- **No proponer cambios de estructura** por «prolijidad»: las decisiones no obvias —publicar en el
  fixture, `ParallelScope.Fixtures`, la cookie de sesión, `EnsureCreated`— están justificadas en
  [08_Decisiones-Y-Trampas.md](indexes/08_Decisiones-Y-Trampas.md).
- **No dar por verificado lo que no lo está**: la ejecución desde el Explorador de pruebas de Visual
  Studio nunca se probó desde esta máquina. Los workflows, en cambio, sí se observaron corriendo — ver
  [06](indexes/06_CI-Y-Workflows.md).
- **`Lab-E2E.WebBlazor.Base` ya no existe como repositorio aparte**: se unificó en este. Su
  conocimiento vigente está en [10](indexes/10_Hola-Mundo-Y-Login.md) y
  [11](indexes/11_Template-Y-Superficies.md); no hay `ia-db/Base` que consultar.
- Si una tarea cambia el código o la documentación, **actualizar esta base de forma incremental** con
  `Actualizar-Indexado.md`, no reconstruirla.

## Manifiesto de generación

- Generado por : `/IA/PROMPTs/IA.Prompts/Tool-Prompts/Indexado-Documentado/Iniciar-Indexado.md`
  (invocado desde `/LAB/Lab-E2E.WebBlazor.Documentacion/PROMPTs/Indexado/Crear-Indexado.md`)
- Alcance      : `/LAB/Lab-E2E.WebBlazor` — modo proyecto. Desde la versión 1.2 absorbe el
  conocimiento vigente del workspace `ia-db/Base/` (`Lab-E2E.WebBlazor.Base`), retirado al unificarse
  los dos repositorios
- Fuentes      : `README.md`, `CHANGELOG.md`, `Lab-E2E.WebBlazor.sln`, `pruebas.runsettings`, `src/`
  (tres proyectos), `tests/` (cuatro), `scripts/`, `.github/workflows/`, `evidencia/`
- Exclusiones  : `.git`, `.nuget/`, `.dotnet/`, `.navegadores/`, `publicacion/`, `datos-e2e/`,
  `resultados/`, `bin/`, `obj/`, las capturas de `evidencia/` (solo se referencian) y lo ignorado por
  `.gitignore`
- Estado del repositorio : rama `main`, último commit `7262395` (2026-09-12)
- Generado     : 2026-09-01 · Versión: 1.0
- Actualizado  : 2026-09-02 · Versión: 1.1 — sincronizado `07_Guias.md` con la consolidación de
  `Guides/` y corregida una referencia en `09_Glosario.md`
- Actualizado  : 2026-09-12 · Versión: 1.2 — unificación con `Lab-E2E.WebBlazor.Base`: índices nuevos
  `10` y `11` con lo vigente de `ia-db/Base/`, que se retira; `00`, `04`, `05`, `06` y `07` rehechos
  por el template (2026-09-04), la mudanza de las guías (2026-09-09) y la unificación; `01`, `02`,
  `08` y `09` corregidos en puntos; `03` sin cambios
- Actualizar   : `/IA/PROMPTs/IA.Prompts/Tool-Prompts/Indexado-Documentado/Actualizar-Indexado.md`
