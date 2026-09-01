# ia-db — Lab-E2E.WebBlazor

> **Instrucción para IA**: este archivo es el **punto de entrada único** a la base de conocimiento
> del repositorio `Lab-E2E.WebBlazor`. Leelo entero —es una pantalla— y después cargá **solo** el o
> los índices que la tabla de navegación indique para tu tarea. No recorras el repositorio completo
> ni cargues toda la documentación mientras esta base responda la pregunta; ampliá a las fuentes
> citadas únicamente ante insuficiencia comprobada.

## Necesitás saber… → leé este índice

| Necesitás saber… | Leé |
| --- | --- |
| De qué trata el laboratorio, con qué stack y qué decisiones lo definen | [00_MASTER-INDEX.md](indexes/00_MASTER-INDEX.md) |
| Cómo se reparten las capas, qué depende de qué y dónde se compone todo | [01_Arquitectura.md](indexes/01_Arquitectura.md) |
| Qué entidades y reglas de negocio existen, y qué valida cada una | [02_Dominio-Y-Reglas.md](indexes/02_Dominio-Y-Reglas.md) |
| Cómo se aísla el estado por sesión y cómo se persiste en SQLite | [03_Sesiones-Y-Persistencia.md](indexes/03_Sesiones-Y-Persistencia.md) |
| Qué pantallas hay, qué hace cada una y con qué `data-testid` se la ubica | [04_Interfaz-Y-Pantallas.md](indexes/04_Interfaz-Y-Pantallas.md) |
| Cómo se corren las pruebas, qué cubre cada suite y qué variables las gobiernan | [05_Pruebas.md](indexes/05_Pruebas.md) |
| Qué hace cada workflow, cuándo se dispara y qué exige la protección de rama | [06_CI-Y-Workflows.md](indexes/06_CI-Y-Workflows.md) |
| Qué guía de estudio responde qué pregunta | [07_Guias.md](indexes/07_Guias.md) |
| Por qué el proyecto está hecho así y qué trampas ya se pagaron | [08_Decisiones-Y-Trampas.md](indexes/08_Decisiones-Y-Trampas.md) |
| Qué significa un término del proyecto | [09_Glosario.md](indexes/09_Glosario.md) |

## Resumen ejecutivo

| Dato | Valor |
| --- | --- |
| Proyecto | `Lab-E2E.WebBlazor` (`LAB/Lab-E2E.WebBlazor`) |
| Tipo | Laboratorio didáctico: aplicación web + pruebas E2E + pipeline |
| Stack | .NET 10 · Blazor Web App *interactive server* · EF Core 10 sobre SQLite · Playwright 1.62 + NUnit 4 · Bootstrap 5.3.8 vendorizado |
| Repositorio | `https://github.com/hdcm-dev/Lab-E2E.WebBlazor` · rama `main` |
| Versión | Sin versionar: el `CHANGELOG.md` agrupa por fecha, no por número (última entrada: 2026-08-31) |
| Documentación asociada | `Lab-E2E.WebBlazor.Documentacion` (este repositorio) |

**Función principal** — enseñar a escribir, estabilizar y automatizar pruebas de extremo a extremo
con Playwright sobre una aplicación Blazor real, y a atarlas a las puertas de un pipeline de GitHub
Actions. El caso de negocio es de juguete —*movilidad urbana*: un ABM de localidades y una encuesta
de transporte en tres pasos—; lo que se estudia es todo lo que rodea a esas dos pantallas.

**Arquitectura en una línea** — un único proyecto web con las capas de Clean Architecture separadas
en carpetas (`Dominio` → `Aplicacion` → `Infraestructura` / `Components`, compuestas en
`Program.cs`), más dos proyectos de prueba hermanos —E2E y unitarias— en `tests/`.

## Estructura

```
Lab-E2E.WebBlazor/
├── Lab-E2E.WebBlazor.sln         Tres proyectos + carpetas de solución (Guides, scripts, workflows)
├── src/MovilidadUrbana.Web/      La aplicación: Dominio, Aplicacion, Infraestructura, Components
├── tests/
│   ├── MovilidadUrbana.E2ETests/     22 casos Playwright + su infraestructura de fixture
│   └── MovilidadUrbana.UnitTests/    49 casos sobre las reglas de dominio, sin navegador
├── scripts/                      dotnet.sh, publicar.sh, pruebas.sh (todo por contenedor)
├── Guides/                       Cuatro familias de guías de estudio
├── .github/workflows/            ci.yml, e2e.yml (reutilizable), verificacion-entorno.yml
├── pruebas.runsettings           Navegador, timeouts y workers de las E2E
├── README.md                     Documento de referencia del repositorio (extenso)
└── CHANGELOG.md                  Registro por fecha
```

## Restricciones para IA

- **No inventar**: toda afirmación de estos índices apunta a un archivo del repositorio. Si algo no
  figura acá, verificalo en la fuente antes de afirmarlo.
- **No confundir los dos laboratorios**: `Lab-E2E.WebBlazor.Base` es un repositorio distinto, con su
  propia ia-db en [`../Base/`](../Base/README.md). Comparten técnica y difieren en madurez.
- **No proponer cambios de estructura** por «prolijidad»: las decisiones no obvias —publicar en el
  fixture, `ParallelScope.Fixtures`, la cookie de sesión, `EnsureCreated`— están justificadas en
  [08_Decisiones-Y-Trampas.md](indexes/08_Decisiones-Y-Trampas.md).
- **No dar por verificado lo que el propio repositorio marca como no verificado**: la ejecución
  desde el Explorador de pruebas de Visual Studio y el comportamiento real de los workflows nunca
  se probaron desde esta máquina (solo se validó la sintaxis YAML).
- Si una tarea cambia el código o la documentación, **actualizar esta base de forma incremental** con
  `Actualizar-Indexado.md`, no reconstruirla.

## Manifiesto de generación

- Generado por : `/IA/PROMPTs/IA.Prompts/Tool-Prompts/Indexado-Documentado/Iniciar-Indexado.md`
  (invocado desde `/LAB/Lab-E2E.WebBlazor.Documentacion/PROMPTs/Indexado/Crear-Indexado.md`)
- Alcance      : `/LAB/Lab-E2E.WebBlazor` — modo proyecto
- Fuentes      : `README.md`, `CHANGELOG.md`, `Lab-E2E.WebBlazor.sln`, `pruebas.runsettings`,
  `src/MovilidadUrbana.Web/`, `tests/`, `scripts/`, `.github/workflows/`, `Guides/`
- Exclusiones  : `.git`, `.nuget/`, `.dotnet/`, `.navegadores/`, `publicacion/`, `datos-e2e/`,
  `bin/`, `obj/`, `wwwroot/vendor/` y `wwwroot/lib/` (Bootstrap vendorizado), y lo ignorado por
  `.gitignore`
- Estado del repositorio : rama `main`, último commit `c870628` (2026-08-31)
- Generado     : 2026-09-01 · Versión: 1.0
- Actualizar   : `/IA/PROMPTs/IA.Prompts/Tool-Prompts/Indexado-Documentado/Actualizar-Indexado.md`
