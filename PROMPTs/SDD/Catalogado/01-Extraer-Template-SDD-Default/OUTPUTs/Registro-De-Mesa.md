# Registro de la mesa — Extracción del template SDD por defecto

**Fecha:** 2026-09-01
**Marco aplicado:** `IA/PROMPTs/IA.Prompts/Base/Mesa-Evaluadora.md`
**Objeto:** producir dos documentos de conocimiento contra `Rules-Base-Conocimiento.md` 2.2

---

## 1. Contrato de entrada

| Campo | Valor |
| --- | --- |
| Artefacto | Dos documentos de conocimiento nuevos, no existentes al arrancar |
| Objetivo | Que un agente sin contexto pueda construir una maqueta HTML de la familia SDD, y luego realizarla en Blazor Interactive Server puro |
| Restricciones duras | No inventar información; toda afirmación con evidencia verificable; no modificar el Framework SDD; salida fuera del repositorio del framework |
| Decisiones cerradas | Blazor Interactive Server; sin MudBlazor; las páginas de ingreso no son interactivas |
| Fuera de alcance | Arquitectura interna de la solución, despliegue, pruebas, el qué funcional |
| Umbral de calidad | S1 y S2 bloquean el cierre |
| Presupuesto | Un ciclo de relevamiento, cuatro especialistas |

**Hallazgo H-000, resuelto con supuesto declarado y no elevado.** El prompt indicaba una carpeta de
salida —`01-Extraer-Template-V2-GDA/OUTPUTs`— que no existía en el árbol, mientras el propio prompt vive
en `01-Extraer-Template-SDD-Default/`. Se consultó por ser una decisión de destino de entrega, y el
prompt fue corregido en el origen a la ruta usada.

## 2. Convocatoria

| Rol | Señal que lo justifica | Resultado |
| --- | --- | --- |
| Desarrollador frontend senior — piso normativo de maqueta | `Maqueta-Rules.md` y `Templates/Modelo-Generico/` son el artefacto a caracterizar | Convocado |
| UX-UI senior — catálogo de diseño | Siete documentos de `References/Design/` gobiernan superficies, estados y accesibilidad | Convocado |
| Frontend senior con foco en UX — maqueta real | El prompt pide contrastar contra una maqueta generada por el framework | Convocado |
| Arquitecto .NET / Blazor senior | El segundo documento es sobre stack .NET con render interactivo de servidor | Convocado |
| Seguridad y privacidad | Hay autenticación y cookies en el alcance | **No convocado.** El esquema de credenciales y la postura de seguridad son de la categoría 05, declarados fuera de alcance. Lo que sí toca la interfaz —rechazo indiferenciado, no exponer parámetros de política— lo cubrió el catálogo de diseño |
| Datos y dominio | Hay entidades y ciclos de vida en los ejemplos | **No convocado.** Los ejemplos son sintéticos y ofuscados; el modelo de datos real es de 02 |

Los cuatro especialistas trabajaron **a ciegas y en paralelo**, sin ver los informes de los otros.

## 3. Hallazgos con veredicto

| Id | Hallazgo | Evidencia | Sev. | Veredicto | Cómo se resolvió |
| --- | --- | --- | --- | --- | --- |
| H-001 | El catálogo de diseño **no tiene patrón agnóstico de diálogo modal**: sus diez patrones no incluyen uno, y el modal sólo aparece mapeado en la capa de stack | Barrido sobre `References/Design/` | S2 | PROCEDE | §5.4 del documento HTML describe la forma constructiva observada más lo que exige la accesibilidad, y §8 declara que **no es norma** |
| H-002 | No hay reglas de paginación ni de ordenamiento en el piso; quedan delegadas a un modelo capturado y a la librería de componentes | `Design-Rules-Web-Generico.md` §4.3; `Rules-Design-Modelo-Template.md` §2 | S3 | PROCEDE | Registrado en §4 del documento HTML como **deuda del artefacto**, no como decisión |
| H-003 | `Design-Rules-Blazor-Mudblazor.md` **no rotula sus reglas como decisión de stack o como método**, a diferencia de `Maqueta-Rules.md` §4. Sin ese rótulo, apartarse de MudBlazor no es sustitución sino conflicto | `Rules-Base-Conocimiento.md` §0.4; `Maqueta-Rules.md` §4 | S1 | PROCEDE | El documento Blazor lleva `Sustituye: —` y declara la desviación con justificación en su §8.1, que es la vía que la regla habilita |
| H-004 | El framework **no norma** separación de code-behind, `EditForm`, inyección en componentes, ciclo de vida, prerrenderizado, ni la estructura de carpetas del proyecto de interfaz —sólo tres archivos— | Barrido de `Blazor` sobre `IA.SDD/`; `Rules-Arquitectura-Tecnica.md` no menciona Blazor | S2 | PROCEDE | El documento Blazor decide esos puntos y los marca como **decisión propia, no norma**, en su §8.2 |
| H-005 | La causa real de que el ingreso no pueda ser interactivo está enunciada de forma elíptica: se dice que la credencial se emite en el ciclo de request, sin nombrar la cookie ni la cabecera | `Design-Rules-Blazor-Mudblazor.md` §4.2 | S2 | PROCEDE | §3.1 del documento Blazor explicita el mecanismo, sin contradecir la regla |
| H-006 | El template de referencia del framework **no demuestra** modales, formularios reales, avisos emergentes ni paginación; el conmutador de estados y la divulgación progresiva cubren todo | Barrido sobre `Templates/Modelo-Generico/` | S2 | PROCEDE | Los esqueletos de esos cuatro se tomaron de la maqueta real y de la anatomía normada, con la procedencia declarada |
| H-007 | La lista de estados no es única entre documentos del framework: seis en el catálogo base, con `sin conexión` sólo en la regla de categoría, y cuatro en su tabla de ejemplo | `Design-Rules-Web-Generico.md` §5 vs. `Rules-UX-UI-DX.md` §4.2 y §4.3 | S3 | NO PROCEDE | Es una inconsistencia del framework, no de estos documentos. Se adopta el piso de cuatro, que es el que las tres fuentes comparten, y el vocabulario ampliado de la maqueta real |
| H-008 | Contraste dudoso de `--color-text-tertiary` sobre fondo primario, cerca de 3.3:1, por debajo del 4.5:1 exigido, en tres clases del template de referencia | Cálculo sobre los valores de token | S2 | NO PROCEDE **en este alcance** | Es un defecto del template del framework, y corregirlo sería modificar el framework, que está prohibido por el contrato de entrada. Queda como deuda declarada |
| H-009 | Los dos documentos superan el techo de 600 líneas de la naturaleza `propio` | `Rules-Base-Conocimiento.md` §6.2 | S3 | PROCEDE | Los dos se acogen a la excepción de §4.3 y la declaran en su §0, con el motivo |

## 4. Deuda declarada

| Id | Qué queda sin resolver | Por qué |
| --- | --- | --- |
| D-001 | Paginación y ordenamiento no están normados ni caracterizados | El piso no los tiene y la maqueta relevada no los implementa. Inventarlos sería violar la regla de no inventar |
| D-002 | El contraste de `--color-text-tertiary` queda como está | Corregirlo es intervenir el framework |
| D-003 | La lista de estados sigue difiriendo entre tres archivos del framework | Fuera del alcance de una extracción de conocimiento |
| D-004 | El catálogo de modelos UX-UI del framework está vacío, y el documento reservado para frontend sin librería de componentes no existe todavía | Se deja constancia; el documento Blazor ocupa ese hueco sin tocar ninguna regla |

## 5. Escaladas

Una sola, ya resuelta antes de escribir: la ruta de salida, registrada como H-000. Ninguna pendiente.

## 6. Cierre

| Campo | Valor |
| --- | --- |
| Ciclos ejecutados | 1 |
| Hallazgos detectados | 10, contando H-000 |
| Procedentes | 8 |
| No procedentes | 2, los dos por quedar fuera del alcance del contrato de entrada |
| Documentos emitidos | 2 de conocimiento, más las filas de índice y este registro |
| Capas a revalidar | Ninguna: no se modificó ningún artefacto existente |
| Framework modificado | No |

**Criterio de parada aplicado:** agotamiento de hallazgos relevantes por encima del umbral. Los dos
hallazgos S1 y S2 restantes —H-008 y H-007— son defectos del framework, no de la salida, y su corrección
está prohibida por el contrato de entrada.
