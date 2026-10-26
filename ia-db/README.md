# ia-db — Lab-E2E.WebBlazor

> **Instrucción para IA**: este archivo es el **punto de entrada único** de la base de conocimiento del laboratorio Lab-E2E.WebBlazor. Leé primero el resumen ejecutivo; después, con la tabla «Necesitás saber…», cargá **solo** los 1–2 índices de `indexes/` que tu tarea necesita. Cada índice abre con su propósito, su fuente primaria y su vigencia, y cita archivos del repo fuente para el detalle: ampliá a las fuentes solo si el índice no alcanza. Si la evidencia del repo contradice un índice, prevalece la evidencia. Todo lo marcado **no verificado** en los índices no debe darse por cierto.

---

## Necesitás saber… → leé este índice

| Necesitás saber… | Leé |
| --- | --- |
| Qué es el laboratorio, sus 5 aplicaciones y 12 proyectos, stack con versiones, puertos, devcontainer, decisiones clave, desfasajes documentales | [00_MASTER-INDEX.md](indexes/00_MASTER-INDEX.md) |
| Cómo se reparten `Domain`/`Application`/`Infrastructure` en cada app, cómo componen `Program.cs` y `MauiProgram.cs`, la convención inglés/español y sus rastros | [01_Arquitectura.md](indexes/01_Arquitectura.md) |
| Entidades, catálogos, reglas, políticas, mensajes de error y casos de uso de Movilidad Urbana; huecos de validación | [02_Dominio-Y-Reglas.md](indexes/02_Dominio-Y-Reglas.md) |
| Aislamiento por sesión (cookie, `X-Sesion-Id`, dispositivo), qué base SQLite usa cada app y cada suite, `AppDbContext`, siembra, WAL, repositorios | [03_Sesiones-Y-Persistencia.md](indexes/03_Sesiones-Y-Persistencia.md) |
| Pantallas de la web de Movilidad Urbana, su comportamiento y el inventario de `data-testid` (incluidos los que ninguna prueba usa) | [04_Interfaz-Y-Pantallas.md](indexes/04_Interfaz-Y-Pantallas.md) |
| Las siete suites y sus casos, cómo se corren, infraestructura E2E, variables de entorno, evidencia, deuda de cobertura | [05_Pruebas.md](indexes/05_Pruebas.md) |
| Los seis workflows de GitHub Actions: qué hacen, disparadores, runner, corridas observadas | [06_CI-Y-Workflows.md](indexes/06_CI-Y-Workflows.md) |
| Dónde están hoy las guías de estudio, qué pregunta responde cada una, enlaces vencidos | [07_Guias.md](indexes/07_Guias.md) |
| Por qué algo está hecho así, qué no revertir, trampas ya pagadas (web, renombre, Android, Appium) | [08_Decisiones-Y-Trampas.md](indexes/08_Decisiones-Y-Trampas.md) |
| Qué significa un término del proyecto y dónde se usa | [09_Glosario.md](indexes/09_Glosario.md) |
| Hola Mundo y Login: acceso por cookies, guard, catálogo de resultados, pruebas sin fixture contra URL fija | [10_Hola-Mundo-Y-Login.md](indexes/10_Hola-Mundo-Y-Login.md) |
| Forma constructiva de las superficies de las tres webs: tokens, componentes, `SurfaceState`, shells | [11_Template-Y-Superficies.md](indexes/11_Template-Y-Superficies.md) |
| La API REST: rutas, contratos, sesión por encabezado, errores, OpenAPI/Scalar, arnés de pruebas | [12_Api-REST.md](indexes/12_Api-REST.md) |
| La app Android MAUI: pantallas, compilación en devcontainer, pruebas de ViewModels y UITests con Appium | [13_App-Android.md](indexes/13_App-Android.md) |

---

## Resumen ejecutivo

| Dato | Valor |
| --- | --- |
| Proyecto | **Lab-E2E.WebBlazor** — laboratorio de pruebas de extremo a extremo con Playwright sobre Blazor Interactive Server, integradas en GitHub Actions |
| Tipo | Laboratorio didáctico: una solución .NET con **5 aplicaciones** (web Blazor, API REST, app Android MAUI de *Movilidad Urbana*, más dos webs escalón: Hola Mundo y Login) y **7 proyectos de prueba** = **12 proyectos**, 118 casos |
| Stack | **.NET 10** (`net10.0`, `net10.0-android`) · Blazor Web App Interactive Server sin librería de componentes (template SDD con tokens propios) · ASP.NET Core controllers + `Microsoft.AspNetCore.OpenApi` 10.0.11 + `Scalar.AspNetCore` 2.17.3 · .NET MAUI (`$(MauiVersion)`) + `CommunityToolkit.Mvvm` 8.4.2 · EF Core SQLite 10.0.11 · NUnit 4.3.2 · `Microsoft.Playwright.NUnit` 1.62.0 · `Microsoft.AspNetCore.Mvc.Testing` 10.0.11 · `Appium.WebDriver` 8.0.0 (UIAutomator2) · GitHub Actions (6 workflows, runner `ubuntu-latest` + uno autoalojado `i7infra-dev`) · Docker (`mcr.microsoft.com/dotnet/sdk:10.0`, `mcr.microsoft.com/playwright:v1.62.1-noble`) |
| Repositorio | `https://github.com/hdcm-dev/Lab-E2E.WebBlazor`, rama `main`, indexado en el commit `8fb4c3a` (2026-09-18), árbol limpio. Clon local: `/LAB/Lab-E2E.WebBlazor/Lab-E2E.WebBlazor/` |
| Versión del producto | **No declarada**: los `.csproj` web no fijan `<Version>`, no hay etiquetas git y el `CHANGELOG.md` agrupa por fecha bajo «[Sin publicar]». La app Android declara `ApplicationDisplayVersion 1.0` |
| Documentación asociada | Guías de estudio en `/LAB/Lab-Documentos/Lab-Documentos/Guides/Testing/Lab-E2E.WebBlazor-Guides/` (repo `hdcm-dev/Lab-Documentos`; copia vieja previa al renombre en `…/Guides/Testing/E2E-Guide/`). Esta ia-db y los prompts del laboratorio viven en `/LAB/Lab-E2E.WebBlazor/Lab-E2E.WebBlazor.Documentacion/`. El `README.md` del código todavía enlaza las guías en `Lab-E2E.WebBlazor.Documentacion/Guides`, que ya no existe ([07](indexes/07_Guias.md)) |

**Función principal**: enseñar a escribir, estabilizar y llevar a la CI pruebas E2E de una aplicación con estado en el servidor. Movilidad Urbana ofrece un ABM de localidades y una encuesta de transporte en tres pasos, con datos aislados por sesión sobre un único SQLite para que las pruebas corran en paralelo; la misma temática se repite como API REST (sesión por encabezado `X-Sesion-Id`) y como app Android (pruebas de ViewModels y de interfaz con Appium). Hola Mundo y Login son los escalones previos: una superficie con estados y la misma superficie detrás de un acceso por cookie.

**Arquitectura en una línea**: tres aplicaciones de Movilidad Urbana **independientes**, cada una con sus propias carpetas `Domain → Application → Infrastructure` (código repetido a propósito, sin referencias entre proyectos) más su presentación (Blazor, controllers, MVVM), y dos webs sin capas; arquitectura en inglés, dominio en español.

---

## Estructura del repositorio fuente (primer nivel)

```
Lab-E2E.WebBlazor/
├── src/
│   ├── MovilidadUrbana.Web/       web Blazor Interactive Server (ABM + encuesta), cookie de sesión, SQLite
│   ├── MovilidadUrbana.ApiWeb/    API REST /api/v1, X-Sesion-Id, OpenAPI + Scalar (Development)
│   ├── MovilidadUrbana.MAUI/      app Android (MVVM), SQLite en el teléfono
│   ├── WebBlazor.HolaMundo/       escalón 1: una superficie interactiva y sus estados
│   └── WebBlazor.Login/           escalón 2: la misma superficie detrás de acceso por cookie
├── tests/                         7 suites: E2ETests (22), UnitTests (49), ApiWeb.Tests (13),
│                                  MAUI.Tests (18), MAUI.UITests (5), HolaMundo.E2ETests (1), Login.E2ETests (10)
├── scripts/                       dotnet.sh · publicar.sh · pruebas.sh (todo en contenedor, sin instalar nada)
├── .github/workflows/             ci · e2e (reutilizable + cron) · e2e-holamundo · e2e-login · android · verificacion-entorno
├── .devcontainer/                 Dockerfile + devcontainer.json + dev.sh para compilar y probar Android por USB
├── evidencia/                     logs y capturas fechadas (2026-09-01 a 2026-09-13) que respaldan las afirmaciones
├── Lab-E2E.WebBlazor.sln          12 proyectos
├── Lab-E2E.WebBlazor.SinMaui.slnf 11 proyectos, sin la app Android (lo que compila CI)
├── pruebas.runsettings            navegador, timeouts y workers de las suites Playwright
└── README.md · CHANGELOG.md · .gitignore
```

Generados al correr e ignorados por git: `datos/`, `datos-e2e/`, `publicacion/`, `resultados/`, `.dotnet/`, `.navegadores/`, `.nuget/`.

Esta base:

```
ia-db/
├── README.md        ← este archivo (entrada única + manifiesto)
└── indexes/         00 maestro · 01–08 temáticos · 09 glosario · 10–13 por aplicación/zona
```

---

## Restricciones para IA

- **No modificar el repo fuente** a partir de esta base: es de lectura. Para cambiar código, abrí el archivo citado y verificá contra él.
- **No tomar la base como vigente más allá de `8fb4c3a`**: si el repo avanzó, comprobá con `git log 8fb4c3a..HEAD` y, si hay cambios, corré el prompt de actualización del manifiesto.
- **No completar por inferencia** lo marcado como **no verificado** (corridas sin log, comportamiento en Visual Studio, versiones sin fijar, interpretaciones de corridas de CI).
- **No «corregir» rastros ni desviaciones** sin leer [08](indexes/08_Decisiones-Y-Trampas.md): varias rarezas son decisiones con costo ya pagado (render mode en la raíz, fixture que publica, `ParallelScope.Fixtures`, jobs sin `container:`, código de capas repetido).
- **No traducir ni renombrar** texto visible, URL, contrato JSON, `data-testid`, `AutomationId` ni comentarios: las pruebas y las guías los citan literalmente ([01](indexes/01_Arquitectura.md) §8).
- **No duplicar** entre índices: cada tema tiene un índice dueño; los demás enlazan.
- **No reindexar** las exclusiones del manifiesto ni los datos de sesión/base de ejecuciones locales.
- **No commitear, pushear ni abrir PR** desde una tarea de indexado.
- Las rutas fuera del repo fuente se escriben desde la raíz del workspace (`/LAB/...`, `/IA/...`).

---

## Manifiesto de generación

- **Generado por**: `/IA/PROMPTs/IA.Prompts/Tool-Prompts/Indexado-Documentado/Iniciar-Indexado.md` (invocado desde `PROMPTs/Indexado/Crear-Indexado.md` de este repositorio, `Lab-E2E.WebBlazor.Documentacion`), con el Profile `/IA/PROMPTs/IA.Prompts/PromptFramework/Profiles/Knowledge-Indexing.md` y la regla `/IA/PROMPTs/IA.Prompts/PromptFramework/Rules/Rule-Indexing.md`.
- **Alcance**: un proyecto (modo proyecto) — `Lab-E2E.WebBlazor`, con sus guías asociadas de Lab-Documentos como fuente secundaria.
- **Destino**: `/LAB/Lab-E2E.WebBlazor/Lab-E2E.WebBlazor.Documentacion/ia-db/` (`README.md` + `indexes/00`–`13`).
- **Fuentes**:
  - Repo fuente (solo lectura): `/LAB/Lab-E2E.WebBlazor/Lab-E2E.WebBlazor/` — `src/`, `tests/`, `scripts/`, `.github/workflows/`, `.devcontainer/`, `evidencia/` (logs y README; de las capturas solo la referencia), `Lab-E2E.WebBlazor.sln`, `Lab-E2E.WebBlazor.SinMaui.slnf`, `pruebas.runsettings`, `.gitignore`, `README.md`, `CHANGELOG.md`, y el historial `git log` (`7679135`…`8fb4c3a`).
  - Guías (solo lectura): `/LAB/Lab-Documentos/Lab-Documentos/Guides/Testing/Lab-E2E.WebBlazor-Guides/` y `/LAB/Lab-Documentos/Lab-Documentos/Guides/Testing/E2E-Guide/`.
  - Externas consultadas: API pública de GitHub Actions de `hdcm-dev/Lab-E2E.WebBlazor` (runs, jobs, annotations, artifacts, branches) el 2026-10-25, para [06](indexes/06_CI-Y-Workflows.md); `README.md` y `git log` de `Lab-E2E.WebBlazor.Documentacion` y de `Lab-Documentos`, para [07](indexes/07_Guias.md).
- **Exclusiones**: `.git`, `.nuget/`, `.dotnet/`, `.navegadores/`, `publicacion/`, `datos-e2e/`, `datos/`, `resultados/`, `bin/`, `obj/`, binarios e imágenes (de `evidencia/` solo la referencia), lo ignorado por `.gitignore` (p. ej. `*.trx`, `*.db`), y cualquier ia-db previa (la base se regeneró desde las fuentes, sin leer la anterior; solo el crítico final usó la 3.0 como lista de control de cobertura, y cada hecho que tomó de ella se verificó contra el repo antes de incorporarlo).
- **Estado del repositorio**: rama `main`, commit `8fb4c3a` (2026-09-18) «README y CHANGELOG enlazan la guía de nomenclatura de la documentación», árbol limpio, sin etiquetas.
- **Método**: seis redactores por grupos de índices (01+03, 02+04, 05+10, 06+07, 08+11, 12+13), un verificador adversarial por grupo (N afirmaciones revisadas = 1077), un redactor de maestro, glosario y entrada (00, 09 y este README) y un crítico de completitud y coherencia entre índices (conteos y nombres unificados contra la fuente, duplicados reemplazados por enlaces al índice dueño —los rastros del renombre tienen a [01](indexes/01_Arquitectura.md) §8.3 como inventario general y cada índice de zona guarda solo los propios—, enlaces relativos y referencias `§` comprobados, rutas citadas del repo comprobadas en disco). Conteos hechos con `grep`/`ls`/`git ls-files`, no estimados.
- **Generado**: 2026-10-25 · **Versión**: 3.1 — regeneración completa e independiente que sucede a la 3.0 (2026-10-18, mismo commit `8fb4c3a`, nunca commiteada).
- **Actualizar**: `/IA/PROMPTs/IA.Prompts/Tool-Prompts/Indexado-Documentado/Actualizar-Indexado.md` (invocado desde `PROMPTs/Indexado/Actualizar-Indexado.md` de este repositorio): detectar cambios desde `8fb4c3a` y rehacer solo los índices afectados, actualizando fecha y versión de este manifiesto.
