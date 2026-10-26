# 07 — Guías

> **Propósito**: dónde viven hoy las guías de estudio del laboratorio, qué pregunta responde cada una, cómo llegaron ahí, y qué enlaces quedaron vencidos (desde el código hacia las guías, desde las guías hacia el código y entre guías).
> **Fuente primaria**: en el repo fuente, `README.md` (§«Guías», línea 103), `CHANGELOG.md` (entradas 2026-08-30 a 2026-09-18), `Lab-E2E.WebBlazor.sln`; fuera de él, `/LAB/Lab-Documentos/Lab-Documentos/Guides/Testing/Lab-E2E.WebBlazor-Guides/` y `/LAB/Lab-Documentos/Lab-Documentos/Guides/Testing/E2E-Guide/` (encabezados *De qué va / Para quién / Qué deja*, frontmatter y `E2E-Guide/Mapa-Del-Conjunto.md` §3), `/LAB/Lab-E2E.WebBlazor/Lab-E2E.WebBlazor.Documentacion/README.md` y su `git log` (commits `8f29d0e`, `64cac26`), `git log` de Lab-Documentos (commit `9162e07`).
> **Vigencia**: versión 3.1, generada el 2026-10-25 sobre el commit `8fb4c3a` (2026-09-18). El estado de las guías y de los enlaces se observó el 2026-10-25 (Lab-Documentos en `5d5c2b4`, 2026-10-11).
> **Vecinos**: los workflows que la guía de GitHub Actions cita → [06](06_CI-Y-Workflows.md); las suites que las guías de pruebas describen → [05](05_Pruebas.md); la convención de nombres en el código → [01](01_Arquitectura.md); la regla de diseño de las superficies → [11](11_Template-Y-Superficies.md); los casos Hola Mundo y Login → [10](10_Hola-Mundo-Y-Login.md); trampas que las guías cuentan → [08](08_Decisiones-Y-Trampas.md); términos (superficie, promesa, testigo…) → [09](09_Glosario.md).

---

## 1. Dónde están hoy

```
/LAB/Lab-Documentos/Lab-Documentos/Guides/Testing/      ← repo hdcm-dev/Lab-Documentos (público)
├── Lab-E2E.WebBlazor-Guides/          ← EL CORPUS VIGENTE del laboratorio (27 archivos, entró en 9162e07)
│   ├── E2E-Guide/                     11 .md + Imagenes/ (3 .png)     pruebas de extremo a extremo
│   ├── Test-Guide/                    README + 3 .md                  pruebas que no pasan por el navegador
│   ├── workflows/                     README + 3 .yml                 workflows de referencia para copiar
│   ├── Estandares-Modelo-Ramas.md     ┐
│   ├── Guia-Practica-GitFlow.md       │ ramas, integración, releases
│   ├── Guia-Practica-GitHubFlow.md    ┘
│   ├── GitHub-Action-Guide.md         GitHub Actions
│   └── Nomenclatura-Convensiones-Arquitecture-Dot-Net.md   convención de nombres
└── E2E-Guide/                         ← COPIA VIEJA de Lab-Documentos (Beginner-Guide, Quick-Guide-ABM), previa al renombre
```

Ni `Guides/README.md` ni el `README.md` raíz de Lab-Documentos mencionan `Testing/` (grep, 0 coincidencias). La única tabla de navegación del corpus está en `/LAB/Lab-E2E.WebBlazor/Lab-E2E.WebBlazor.Documentacion/README.md` §«Guías» (y, dentro del corpus, en `E2E-Guide/Mapa-Del-Conjunto.md` y `Test-Guide/README.md`).

### 1.1 Cómo llegaron ahí

| Fecha | Repo · commit | Movimiento |
| --- | --- | --- |
| 2026-08-30 | código · `6f5947e` | Las guías del modelo de ramas entran en `Guides/` del repo de código, tomadas de `Lab-GitFlow.Documentacion`; `Beginner-Guide` y `Quick-Guide-ABM` pasan a `Guides/E2E-Guide/` (`CHANGELOG.md`) |
| 2026-08-31 | código · `c870628` | Se suma `GitHub-Action-Guide` |
| 2026-09-03 | código · `4815823`, `7a069b3` | Cada guía de ramas pasa a **un solo documento** (27 archivos reemplazados); `.sln` puesto al día |
| 2026-09-09 | código · `98fde5f` | **`Guides/` sale del repo de código** hacia `Lab-E2E.WebBlazor.Documentacion` (`E2E-Guide/` y la raíz de `Guides/`); se quitan las carpetas de solución `Guides` y `E2E-Guide` del `.sln` |
| 2026-09-28 | Lab-Documentos · `9162e07` | Ingresa el corpus en `Guides/Testing/Lab-E2E.WebBlazor-Guides/`; `Anexos/workflows/` pasa a `workflows/` |
| 2026-10-01 | Documentacion · `8f29d0e` | Se retiran de Documentacion los 27 archivos («ya viven, idénticos» en Lab-Documentos) |
| 2026-10-02 | Documentacion · `64cac26` | Su `README.md` apunta a Lab-Documentos |

El repo de código **no siguió** los dos últimos pasos: en `8fb4c3a` su README y su CHANGELOG siguen remitiendo a `Lab-E2E.WebBlazor.Documentacion` (§4.1).

---

## 2. Qué pregunta responde cada guía

Columna «Pregunta» tomada de `Mapa-Del-Conjunto.md` §3.1 cuando la trae; si no, del bloque *De qué va* del propio documento. Líneas contadas con `wc -l`. `doc_id`, `owner` y `last_review` salen del frontmatter (vacío = el documento no tiene).

### 2.1 `E2E-Guide/` — pruebas de extremo a extremo

| Documento | Líneas | doc_id | Pregunta que responde | Para quién |
| --- | ---: | --- | --- | --- |
| `Mapa-Del-Conjunto.md` | 228 | E2E-03 | ¿Qué leo para qué, y quién es dueño de cada tema? (puerta de entrada; tabla de dueños §3.2, recorridos por perfil §3.3) | Quien llega y no sabe por dónde entrar |
| `Del-Requerimiento-Al-Caso.md` | 714 | E2E-04 | ¿Cómo llego de un problema contado en desorden a superficies, promesas y estados? — **método propuesto**, su §10 declara qué tiene respaldo | Quien recibe un pedido sin nada escrito |
| `Quick-Guide-Primer-Proyecto.md` | 536 | — | ¿Cómo creo el proyecto NUnit + Playwright y escribo la primera prueba? (ejemplo Hola Mundo) | Quien arranca de cero con Visual Studio |
| `Beginner-Guide.md` | 1816 | E2E-00 | ¿Cómo se escribe, se estabiliza y se ata a la CI una suite E2E? (9 capítulos, 6 anexos) | Quien nunca escribió una E2E |
| `Quick-Guide-ABM.md` | 345 | E2E-01 | ¿Cuál es el camino corto para un ABM más? (7 pasos, matriz de 9 casos, trampas de interactive server) | Quien ya escribió E2E |
| `Caso-HolaMundo-Page.md` | 861 | — | ¿Cómo decido qué probar, en el caso mínimo? (superficie, estado, testigo de hidratación) | Quien decide **qué** probar |
| `Caso-Login-Page.md` | 465 | — | ¿Y cuando hay un adversario además de un usuario? (promesa negativa por dos observaciones) | Ídem, postura de seguridad |
| `Caso-Encuesta-Page.md` | 437 | E2E-02 | ¿Y cuando el acto se recorre en tramos? (tres pasos = **una** superficie; dos promesas del código sin caso) | Ídem, acto divisible |
| `Marco-La-Superficie-Verificable.md` | 446 | — | ¿De dónde sale este vocabulario y adónde se puede ir? (procedencia y bibliografía) | Quien quiere ir más lejos |
| `Template-SDD-Aplicado.md` | 169 | — | ¿Cómo se construye la superficie del lado de la vista? (tokens, un componente por patrón, estados, desviaciones) | Quien construye la vista |
| `Notas.GitHub.md` | 19 | — | ¿Cómo evito que un PR desde un fork corra en el runner propio? (*Settings → Actions → General → Fork pull request workflows…*) | Quien administra el repo |
| `Imagenes/` | 3 .png | — | Capturas del Explorador de pruebas y del workload (solo referencia) | — |

### 2.2 `Test-Guide/` — más allá del navegador

| Documento | Líneas | Pregunta que responde | Para quién |
| --- | ---: | --- | --- |
| `README.md` | 55 | Mapa de la carpeta (escenarios S1–S6 → suite); anclado al commit `946d023` | — |
| `Panorama-De-Pruebas-Automatizadas.md` | 1030 | ¿Qué tipos de prueba hay y cuál va en cada lugar? (pirámide/trofeo, dobles de Meszaros, capa → tipo, «estoy acá → aplico esto»); define el marco de referencia | Quien sabe E2E y tiene que probar API, MAUI o dominio |
| `Pruebas-Unitarias-Y-Arquitectura.md` | 476 | ¿Qué es una unidad según dónde vive el código, y qué reemplazo por un doble? (regla, servicio, ViewModel; capas MAUI como archivos enlazados) | Quien escribe la primera prueba sin navegador |
| `Pruebas-De-Interfaz-Por-Pantalla.md` | 469 | ¿Cómo pruebo una interfaz sin DOM? (árbol de accesibilidad, Appium + `AutomationId`, lo hecho con `adb` y la suite Appium en un teléfono físico) | Quien prueba `MovilidadUrbana.MAUI` |

### 2.3 Raíz de `Lab-E2E.WebBlazor-Guides/`

| Documento | Líneas | doc_id · owner | Pregunta que responde | Para quién |
| --- | ---: | --- | --- | --- |
| `Estandares-Modelo-Ramas.md` | 2034 | GF-GUIA · Lab-GitFlow | ¿Qué modelos de ramas hay, cómo se elige uno y cómo se opera el ciclo de versiones? | El equipo entero |
| `Guia-Practica-GitFlow.md` | 1183 | GF-09-ESCENARIOS · Lab-GitFlow | Los ocho escenarios ejecutables del modelo adoptado | Equipo de tres que rota roles |
| `Guia-Practica-GitHubFlow.md` | 1072 | GHF-GUIA · Lab-GitFlow | Los mismos ocho, sobre el modelo **no** adoptado (línea de base) | Ídem |
| `GitHub-Action-Guide.md` | 2978 | GHA-00 · Lab-GitFlow | ¿Qué es un workflow, cómo se lee y cómo se arman los escenarios completos? Cita los workflows de este laboratorio como `W-E2E-CI`, `W-E2E-E2E`, `W-E2E-ENT` (§ fuentes, líneas 2920–2922) | Quien nunca escribió un workflow |
| `Nomenclatura-Convensiones-Arquitecture-Dot-Net.md` | 206 | — | ¿Cómo nombro o renombro con «arquitectura en inglés, dominio en español»? (tabla de decisión, lo que no se traduce, procedimiento con los escollos de `946d023`/`e9dea2a`) | Persona o agente que nombra o renombra |
| `workflows/README.md` + `ci.yml`, `release.yml`, `auditoria-convergencia.yml` | 114 + 92/74/90 | GF-AX-WF · Lab-GitFlow | Tres workflows **de ejemplo** para el repo de práctica de GitFlow (no son los de este repo; los de este repo → [06](06_CI-Y-Workflows.md)) | Quien monta la CI del equipo |

### 2.4 Por dónde entrar (resumen de `Mapa-Del-Conjunto.md` §3.3)

| Perfil | Recorrido |
| --- | --- |
| Tengo un requerimiento y nada escrito | Del-Requerimiento-Al-Caso → Caso-HolaMundo §2 → Caso-Encuesta §3 |
| Nunca hice una E2E | Quick-Guide-Primer-Proyecto → Beginner §1 y §4 → Anexo A → §6 |
| Ya sé, quiero el camino corto | Quick-Guide-ABM |
| Blazor Server | Beginner §7 |
| Tengo que decidir qué probar | Del-Requerimiento-Al-Caso → Mapa §2 → los tres casos de diseño, en orden de dificultad |
| QA / analista | Del-Requerimiento-Al-Caso → Mapa §2 → Beginner §2 y §5 → Anexo C |
| DevOps | Beginner §8 → §7.4 |
| PO / autoridad de cambio | Del-Requerimiento-Al-Caso §1 a §3 → Beginner §5.1 → §8.4 |
| Ir más lejos | Marco-La-Superficie-Verificable |

Regla del conjunto: **una corrección se hace en el documento dueño del tema; los demás enlazan** (`Mapa-Del-Conjunto.md` §3.2 y §4).

---

## 3. Las dos copias de `E2E-Guide/`

| | `Testing/E2E-Guide/` | `Testing/Lab-E2E.WebBlazor-Guides/E2E-Guide/` |
| --- | --- | --- |
| Archivos | 2 (`Beginner-Guide.md` 1812, `Quick-Guide-ABM.md` 325) | 11 + imágenes |
| Historia | `fab7258` (2026-09-13), movida a `Testing/` en `9162e07` | `9162e07` (2026-09-28) |
| Bloque *De qué va / Para quién / Qué deja* | No | Sí |
| Nombres de código | Previos al renombre (`Dominio/`, `Infraestructura/`, `ReglasDeLocalidad`, `ServidorDeLaAplicacion`, `PruebaE2E`, `NavegacionTests`…) | Renombrados |
| Citas `[E: …]` al código que no existen en `8fb4c3a` (ocurrencias) | Beginner 33 de 97 · Quick-ABM 13 de 22 | 0 |

`diff` entre las dos: abstract, índice, enlaces con un `../` más y los nombres renombrados. **La vigente es la de `Lab-E2E.WebBlazor-Guides/`**; la otra es un rastro previo al renombre (`946d023`).

---

## 4. Enlaces vencidos (relevados el 2026-10-25)

### 4.1 Del repo de código hacia las guías

| Dónde (en `8fb4c3a`) | Apunta a | Estado |
| --- | --- | --- |
| `README.md:103` | `github.com/hdcm-dev/Lab-E2E.WebBlazor.Documentacion/blob/main/Guides/Nomenclatura-Convensiones-Arquitecture-Dot-Net.md` | **404** |
| `README.md:259` | `…Documentacion/tree/main/Guides/E2E-Guide` | **404** |
| `README.md:260` | `…Documentacion/tree/main/Guides` | **404** (API `contents/Guides` → 404) |
| `README.md:254`, `CHANGELOG.md:9`, `CHANGELOG.md:176` | Raíz de `Lab-E2E.WebBlazor.Documentacion` | 200, pero el texto dice que las guías viven ahí: ya no |
| `README.md:262–263` | «se leen mejor con los dos clonados como carpetas hermanas» | Supone el layout viejo (código + Documentacion) |

Vigente en su lugar: `https://github.com/hdcm-dev/Lab-Documentos` → `Guides/Testing/Lab-E2E.WebBlazor-Guides/` (API `contents` → 200). Ningún archivo de `src/`, `tests/`, `scripts/`, `.github/` ni `evidencia/` enlaza guías (grep sobre el árbol, exclusiones aplicadas).

### 4.2 De las guías hacia el código

Las guías citan el código por ruta relativa `../../../Lab-E2E.WebBlazor/…`, calculada para cuando vivían en `Lab-E2E.WebBlazor.Documentacion/Guides/E2E-Guide/`. Al bajar dos niveles (`Guides/Testing/Lab-E2E.WebBlazor-Guides/E2E-Guide/`) y cambiar de repositorio, **ninguna resuelve**; en los 50 casos el archivo de destino sí existe en el repo de código.

| Documento | Enlaces markdown al código rotos | Enlaces internos OK |
| --- | ---: | ---: |
| `E2E-Guide/Caso-Encuesta-Page.md` | 22 | 3 |
| `E2E-Guide/Caso-HolaMundo-Page.md` | 19 | 8 |
| `E2E-Guide/Beginner-Guide.md` | 3 | 0 (+156 anclas) |
| `E2E-Guide/Caso-Login-Page.md` | 3 | 6 |
| `E2E-Guide/Marco-La-Superficie-Verificable.md` | 2 | 5 |
| `E2E-Guide/Quick-Guide-ABM.md` | 1 | 8 |
| **Total** | **50** | |

Las citas en texto `**[E: ruta]**` (no son enlaces) se comprobaron reponiendo la ruta sobre el repo de código (ocurrencias, sin contar los marcadores `[E: ruta]` y `[E:]` de las leyendas): Beginner 97, Quick-ABM 22, Del-Requerimiento 13, Panorama 28, Pruebas-Unitarias 26 (2 son «ídem»), Pruebas-De-Interfaz 22. Existen todas **salvo una**: `Test-Guide/Pruebas-De-Interfaz-Por-Pantalla.md:434` cita `Services/SesionDelDispositivo.cs`, que en `8fb4c3a` es `src/MovilidadUrbana.MAUI/Services/DeviceSession.cs` (rastro previo al renombre). Que los **rangos de línea** de esas citas sigan cayendo en el código correcto **no se verificó**. El layout que harían falta para que resuelvan (dónde clonar cada repo) **no está documentado** en el corpus.

### 4.3 Entre guías (internos) rotos por la mudanza

| Documento | Rotos | Causa |
| --- | ---: | --- |
| `Estandares-Modelo-Ramas.md` | 10 | Apuntan a `Anexos/workflows/…`; la carpeta es ahora `workflows/` |
| `Guia-Practica-GitFlow.md` | 3 | Ídem (`Anexos/workflows/README.md`, `auditoria-convergencia.yml`) |
| `Guia-Practica-GitHubFlow.md` | 2 | Ídem |
| `GitHub-Action-Guide.md` | 2 | `Anexos/workflows/README.md` y `../README.md` (no existe `Guides/Testing/README.md`) |
| `workflows/README.md` | 2 | `../../Guia-Practica-GitFlow.md#…`: sobra un `../` desde que `Anexos/workflows/` pasó a `workflows/` |
| **Total** | **19** | |

`E2E-Guide/Mapa-Del-Conjunto.md` (38), `Del-Requerimiento-Al-Caso.md` (21), `Quick-Guide-Primer-Proyecto.md` (5), `Nomenclatura…` (2) y los cuatro de `Test-Guide/` no tienen enlaces relativos rotos.

### 4.4 Del README de Documentacion hacia Lab-Documentos

`/LAB/Lab-E2E.WebBlazor/Lab-E2E.WebBlazor.Documentacion/README.md` enlaza `../Lab-Documentos/Guides/Testing/Lab-E2E.WebBlazor-Guides/…` («resuelven con `Lab-Documentos` clonado como carpeta hermana»). En este workspace resolvería a `/LAB/Lab-E2E.WebBlazor/Lab-Documentos/`, que **no existe**; el clon real está en `/LAB/Lab-Documentos/Lab-Documentos/`.

---

## 5. Desfasajes de contenido entre las guías y el código en `8fb4c3a`

| Guía · lugar | Dice | Lo verificado |
| --- | --- | --- |
| `Beginner-Guide.md` §8.3 (línea 1208) y línea 28 | «Los tres workflows del laboratorio» | Son seis ([06](06_CI-Y-Workflows.md) §1) |
| `Beginner-Guide.md` línea 1457 | Los jobs corren en `ubuntu-latest`, con el propio comentado | `e2e.yml` / `publicar` corre en `[self-hosted, i7infra-dev]` desde `4815823` |
| `Beginner-Guide.md` línea 1591 | Comportamiento real de los workflows: «No verificado» | 117 corridas observadas en la API ([06](06_CI-Y-Workflows.md) §6) |
| `Beginner-Guide.md` líneas 306–308 | `Infrastructure/ServidorDeLaAplicacion.cs`, `PruebaE2E.cs`, `ParalelismoDelEnsamblado.cs` | Los archivos son `TestAppServer.cs`, `E2ETestBase.cs`, `AssemblyParallelism.cs` (`ls tests/MovilidadUrbana.E2ETests/Infrastructure/`): renombre a medias, rastro |
| `Beginner-Guide.md` líneas 1560, 1576 | Build de `Lab-E2E.WebBlazor.sln` («los 3 proyectos») | Evidencia de agosto; hoy la solución tiene doce proyectos y CI compila `Lab-E2E.WebBlazor.SinMaui.slnf` |
| `GitHub-Action-Guide.md` líneas 698 y 1387 | `ci.yml` hace `dotnet restore/build Lab-E2E.WebBlazor.sln` | `ci.yml` usa `Lab-E2E.WebBlazor.SinMaui.slnf` (líneas 56 y 59) desde `10ce735` |
| `GitHub-Action-Guide.md` líneas 276–277 | Jobs `compilacion` y `e2e` en `ubuntu-latest` | `e2e` delega en `e2e.yml`, cuyo `publicar` es autoalojado |
| `GitHub-Action-Guide.md` líneas 2920–2922 | Fuentes `LAB/Lab-E2E.WebBlazor/.github/workflows/…` | En el workspace la ruta es `/LAB/Lab-E2E.WebBlazor/Lab-E2E.WebBlazor/.github/workflows/…` |
| `Quick-Guide-ABM.md` línea 289 («una regla de protección de rama que exija el check resumen») · `Beginner-Guide.md` línea 1344 (exige «un solo check: `CI aprobada`») | La protección de rama exige el check resumen | `main` con `protected: false` (API, 2026-10-25) |
| Frontmatter de E2E-00…E2E-04 | `owner: Lab-E2E.WebBlazor.Documentacion` | Viven en Lab-Documentos; los de ramas/Actions dicen `owner: Lab-GitFlow` |
| `Notas.GitHub.md` | «los jobs corren en i7infra-dev» | Solo `publicar` de `e2e.yml` |
| `E2E-Guide/Quick-Guide-ABM.md` línea 95 (y la copia vieja `Testing/E2E-Guide/Quick-Guide-ABM.md` línea 75) | Ejemplo de `boton-*`: `boton-confirmar-baja` | Testid retirado el 2026-09-04; hoy `boton-confirmar-dialogo` ([04](04_Interfaz-Y-Pantallas.md) §7) |

Los nombres viejos que aparecen en `Nomenclatura-Convensiones-Arquitecture-Dot-Net.md` (`ServicioDeLocalidades`, `ReglasDeEncuesta`, `Grilla`) **no** son rastros: son los ejemplos de «antes → después» del procedimiento de renombre.

---

## 6. Copias hermanas fuera de `Testing/`

`Guides/GitFlow/Estandares-Modelo-Ramas-Guide/Estandares-Modelo-Ramas.md`, `Guides/GitFlow/Git-Flow-Guides/GitFlow-Practice-Guide/Guia-Practica-GitFlow.md` y `…/GitHubFlow-Practice-Guide/Guia-Practica-GitHubFlow.md` en Lab-Documentos tienen el mismo nombre que las de `Lab-E2E.WebBlazor-Guides/` y **no son idénticas** (`diff -q`). Cuál es la canónica no está declarado en ninguna fuente: **no verificado**.
