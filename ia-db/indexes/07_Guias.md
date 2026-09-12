# 07 — Guías de estudio

> **Propósito**: saber dónde están las guías y cuál responde qué pregunta, sin abrirlas todas.
> **Fuente primaria**: `CHANGELOG.md` de `Lab-E2E.WebBlazor` (2026-09-09) y el árbol `Guides/` de
> `Lab-E2E.WebBlazor.Documentacion`, con la tabla de su `README.md`.
> **Vigencia**: 2026-09-12, commit `88e5caa` del laboratorio. Inventario tomado ese día sobre
> `Lab-E2E.WebBlazor.Documentacion`.

## Ya no viven en el repositorio de código

Desde el 2026-09-09 **toda la documentación de estudio vive en
[`Lab-E2E.WebBlazor.Documentacion`](https://github.com/hdcm-dev/Lab-E2E.WebBlazor.Documentacion)**:
las de pruebas en `Guides/E2E-Guide/` y las de ramas e integración continua en `Guides/`. El motivo
que registra el `CHANGELOG.md`: las mismas guías estaban repartidas entre `Lab-E2E.WebBlazor` y
`Lab-E2E.WebBlazor.Base`, con dos copias que podían divergir sin que nada avisara.

Ese día `Lab-E2E.WebBlazor.sln` retiró las carpetas de solución `Guides` y `E2E-Guide`, y la sección
«Guías» del `README.md` pasó a remitir al repositorio de documentación.

**Consecuencia práctica.** Las guías citan el código del laboratorio por ruta relativa
(`../../../Lab-E2E.WebBlazor/src/…`), así que se leen bien solo con los dos repositorios clonados
como carpetas hermanas. En github.com esos enlaces no resuelven: una ruta relativa no puede salir de
su repositorio.

## Inventario

| Documento | Líneas |
| --- | --- |
| `Guides/E2E-Guide/Mapa-Del-Conjunto.md` | 228 |
| `Guides/E2E-Guide/Del-Requerimiento-Al-Caso.md` | 714 |
| `Guides/E2E-Guide/Quick-Guide-Primer-Proyecto.md` | 536 |
| `Guides/E2E-Guide/Beginner-Guide.md` | 1816 |
| `Guides/E2E-Guide/Quick-Guide-ABM.md` | 345 |
| `Guides/E2E-Guide/Caso-HolaMundo-Page.md` | 861 |
| `Guides/E2E-Guide/Caso-Login-Page.md` | 465 |
| `Guides/E2E-Guide/Caso-Encuesta-Page.md` | 437 |
| `Guides/E2E-Guide/Marco-La-Superficie-Verificable.md` | 446 |
| `Guides/E2E-Guide/Template-SDD-Aplicado.md` | 169 |
| `Guides/E2E-Guide/Notas.GitHub.md` | 19 |
| `Guides/E2E-Guide/Imagenes/` | 3 capturas del Explorador de pruebas y del workload de Visual Studio |
| `Guides/Estandares-Modelo-Ramas.md` | 2034 |
| `Guides/Guia-Practica-GitFlow.md` | 1183 |
| `Guides/Guia-Practica-GitHubFlow.md` | 1072 |
| `Guides/GitHub-Action-Guide.md` | 2978 |
| `Guides/Anexos/workflows/` | `README.md` (114) + `ci.yml`, `release.yml`, `auditoria-convergencia.yml` |

Cada documento abre con un abstract —*de qué va, para quién, qué deja*— y con su índice.

## Qué responde cada una

Tomado de la tabla del `README.md` de `Lab-E2E.WebBlazor.Documentacion`, que es la que mantiene esa
correspondencia.

### Pruebas de extremo a extremo

Se leen en este orden la primera vez; después, por la columna del medio.

| Documento | Para quién | De qué va |
| --- | --- | --- |
| `Mapa-Del-Conjunto.md` | Quien llega y no sabe por dónde entrar | Qué documento responde a qué pregunta, cómo se cruzan los dos vocabularios y quién es dueño de cada tema |
| `Del-Requerimiento-Al-Caso.md` | Quien recibe un pedido y no tiene nada escrito | Cómo se llega de un problema contado en desorden hasta superficies, promesas y estados, antes de que exista una pantalla. Método propuesto: su §10 declara qué tiene respaldo |
| `Quick-Guide-Primer-Proyecto.md` | Quien nunca creó un proyecto de pruebas | Crear el proyecto NUnit con Playwright y la primera prueba, sobre Hola Mundo |
| `Beginner-Guide.md` | Quien nunca escribió una prueba E2E | Qué es una E2E, cómo se arma el proyecto en .NET, cómo se escribe y se estabiliza un caso y cómo se ata al merge |
| `Quick-Guide-ABM.md` | Quien ya escribió pruebas E2E | La receta corta para las de un ABM, con las trampas de Blazor *interactive server* |
| `Caso-HolaMundo-Page.md` | Quien tiene que decidir **qué** probar | El caso mínimo: superficie, estados y el testigo de hidratación |
| `Caso-Login-Page.md` | Ídem, con postura de seguridad | La promesa negativa, que se verifica comparando dos observaciones |
| `Caso-Encuesta-Page.md` | Ídem, con un acto divisible | Por qué tres pasos de un asistente son **una** superficie y no tres |
| `Marco-La-Superficie-Verificable.md` | Quien quiere ir más lejos | De qué tradición viene cada concepto, con bibliografía y con lo que se reinventó sin saberlo |
| `Template-SDD-Aplicado.md` | Quien construye la superficie | Qué se aplicó del template SDD, qué se decidió al aplicarlo y cómo se verificó — ver [11](11_Template-Y-Superficies.md) |
| `Notas.GitHub.md` | Quien administra el repositorio | Cómo evitar que un PR desde un fork corra en el runner propio |

Los tres casos de diseño se corresponden con las tres aplicaciones: Hola Mundo y Login están en
[10](10_Hola-Mundo-Y-Login.md) y la Encuesta de Movilidad Urbana en
[04](04_Interfaz-Y-Pantallas.md).

### Ramas, integración y releases

| Documento | Para quién | De qué va |
| --- | --- | --- |
| `Estandares-Modelo-Ramas.md` | El equipo entero | Qué modelos de ramas hay, cómo se elige uno y cómo se opera el ciclo de vida de las versiones; el adoptado está en su §6 |
| `Guia-Practica-GitFlow.md` | Un equipo de tres que rota roles | Los ocho escenarios ejecutables del modelo adoptado |
| `Guia-Practica-GitHubFlow.md` | Ídem | Los mismos ocho sobre el modelo que **no** se adoptó, como línea de base |
| `GitHub-Action-Guide.md` | Quien nunca escribió un workflow | Vocabulario, sintaxis y escenarios completos, con ejemplos que corren en este workspace |
| `Anexos/workflows/` | Quien monta la CI | Los tres workflows listos para copiar |

El punto de contacto entre las dos familias es el escenario del **PR que rompe la regresión**: ahí
entran las E2E de este laboratorio, y el bloque de pull requests y pruebas del documento de
estándares explica cuándo esa verificación bloquea un merge.

## Cómo verificar todo esto

| Afirmación | Comprobación |
| --- | --- |
| Las guías no están en el repositorio de código | `ls Guides` (no existe) y `grep -n Guides Lab-E2E.WebBlazor.sln` (sin resultados), en `Lab-E2E.WebBlazor` |
| Qué documentos hay | `find Guides -name '*.md' \| sort`, en `Lab-E2E.WebBlazor.Documentacion` |
| Las guías citan el código por ruta relativa | `grep -c 'Lab-E2E.WebBlazor/' Guides/E2E-Guide/Caso-HolaMundo-Page.md` (17 el 2026-09-12) |
