---
doc_id: E2E-03
doc_type: documento-integrador
title: Mapa del conjunto — qué se lee para qué, y quién es dueño de cada tema
status: vigente
origin: agente
confidence: alta
owner: Lab-E2E.WebBlazor.Documentacion
last_review: 2026-09-09
audience: [desarrollo, qa, po]
traces: [E2E-00, E2E-01, E2E-02, E2E-04]
---

# Mapa del conjunto

Este documento es la puerta de entrada al conjunto. Hace dos cosas que ningún otro hace:

1. **Ubica cada documento en la cadena** que va de la situación de alguien hasta el caso de prueba
   (§1).
2. **Une los dos vocabularios** del conjunto —superficie/promesa/estado por un lado,
   escenario/contexto/actor por el otro— y dice qué documento es dueño de cada tema, para que una
   corrección se haga en un solo lugar (§2 y §3).

No enseña a probar ni a diseñar: **manda a leer al que corresponde.**

## Marcas de evidencia

| Marca | Significado |
| --- | --- |
| **[E: ruta]** | *Evidencia en el repositorio*: se comprueba abriendo ese archivo |
| **[V]** | *Verificado por ejecución*: se corrió y se observó el resultado |
| **[C]** | *Criterio*: decisión del laboratorio, defendible y discutible |

---

# 1. La cadena, en una pantalla

El conjunto documenta este recorrido:

```
situación → propósito → actos → superficies → recurso → estados → pantallas → identificadores → casos
└──────────── Del-Requerimiento-Al-Caso ────────────┘  └─ casos de diseño ─┘  └───── Beginner ─────┘
```

**El tramo de análisis —de la situación hasta los estados— tiene documento propio:**
[Del-Requerimiento-Al-Caso.md](Del-Requerimiento-Al-Caso.md). Ahí están el punto cero, las cinco
alturas con las que llega un pedido, las cinco preguntas de ida, la elección del recurso con sus dos
ejes, y qué promesas y estados trae cada recurso. Es un **método propuesto**, no una práctica
asentada, y declara en su §10 qué parte tiene respaldo en los laboratorios y qué parte no.

Este documento se ocupa de lo otro: **unir los dos vocabularios del conjunto (§2) y decir qué se lee
para qué y quién es dueño de cada tema (§3).**

---

# 2. El vocabulario, en una cadena

## 2.1 La traducción

Lo que se ve al mirar un producto, cómo lo nombra el conjunto, y adónde va a parar:

| Lo que ves | Se llama | Va a parar a |
| --- | --- | --- |
| Una página, un modal, un recorte con sentido propio | **Superficie** | Una clase `[TestFixture]` |
| El punto donde siempre arrancás | **Estado de partida** | El `[SetUp]` |
| «Acá puedo hacer esto» | **Promesa** | Un método `[Test]` |
| «La pantalla puede quedar así» | **Estado** | Una aserción dentro de un método |
| «Esto no se puede llegar a saber» | **Promesa negativa** | Un método que compara **dos** observaciones |
| Lo que nombrás para poder actuar | **Identificador** | Un `data-testid` en la vista |

**La distinción que más ordena**: un estado se **observa**, una promesa se **ejercita**. Un estado se
dice con un sustantivo; una promesa con un verbo en primera persona. Y la relación entre las dos:

> **La promesa es lo que se prueba. Los estados son de dónde parte y adónde llega esa prueba.**

## 2.2 Los criterios de la clase y del método

| Unidad | Criterio |
| --- | --- |
| **Clase** | Una por superficie. Si no hay una frase que abarque toda la clase, no era una clase: era un recorrido |
| **Método** | **Un caso, un motivo de falla.** Si puede fallar por dos razones, el reporte no dirá cuál |

La prueba práctica de la clase es escribir el `[SetUp]`: si sale uno solo y natural, es una clase. En
el laboratorio `NavegacionTests` **no tiene ninguno**, y esa ausencia es la señal en el código de que
ahí no hay una superficie sino un recorrido entre varias
**[E: ../../../Lab-E2E.WebBlazor/tests/MovilidadUrbana.E2ETests/NavegacionTests.cs]**.

## 2.3 Los dos ejes del conjunto, y cómo se cruzan

El conjunto organiza por dos ejes distintos, y hasta ahora ninguno mencionaba al otro:

| Eje | Pregunta que responde | Dónde vive |
| --- | --- | --- |
| **Superficie / promesa / estado** | ¿**Qué** hay que probar, y dónde corta? | Los casos de diseño y el marco |
| **Escenario / contexto / actor** (ESC, CTX, ACT) | ¿**Cuándo** se prueba, **dónde** corre y **quién** decide? | [Beginner §2](Beginner-Guide.md#2-marco-de-referencia) |

Son compatibles y se cruzan en un punto concreto: **ESC-01 «se escribe una pantalla nueva» es el
escenario en el que se aplican las cinco preguntas de §1**, y su salida —«recorridos críticos
cubiertos antes del merge»— es la lista de promesas de §1.2. El resto de los escenarios opera sobre
una suite que ya existe.

---

# 3. El mapa del conjunto

## 3.1 Qué responde cada documento

| Documento | La pregunta que contesta |
| --- | --- |
| **E2E-Resumen** *(este)* | ¿Qué leo para qué, y quién es dueño de cada tema? |
| [Del-Requerimiento-Al-Caso](Del-Requerimiento-Al-Caso.md) | Alguien me tiró un problema encima: ¿cómo llego de ahí a superficies, promesas y estados? |
| [Quick-Guide-Primer-Proyecto](Quick-Guide-Primer-Proyecto.md) | ¿Cómo creo el proyecto y escribo la primera prueba? |
| [Beginner-Guide](Beginner-Guide.md) | ¿Cómo se escribe, se estabiliza y se ata a la CI una suite E2E? |
| [Quick-Guide-ABM](Quick-Guide-ABM.md) | ¿Cuál es el camino corto para un ABM más? |
| [Caso-HolaMundo-Page](Caso-HolaMundo-Page.md) | ¿Cómo decido qué probar, en el caso mínimo? |
| [Caso-Login-Page](Caso-Login-Page.md) | ¿Y cuando hay un adversario además de un usuario? |
| [Caso-Encuesta-Page](Caso-Encuesta-Page.md) | ¿Y cuando el acto se recorre en tramos? |
| [Marco-La-Superficie-Verificable](Marco-La-Superficie-Verificable.md) | ¿De dónde sale este vocabulario y adónde se puede ir? |
| [Template-SDD-Aplicado](Template-SDD-Aplicado.md) | ¿Cómo se construye la superficie del lado de la vista? |

## 3.2 Quién es dueño de cada tema

Varios temas aparecen en más de un documento, y está bien: repetir ayuda a leer. Lo que no puede
pasar es que dos versiones diverjan en silencio —*«una configuración duplicada no es redundancia, es
una contradicción esperando fecha»*, [Beginner §9.3](Beginner-Guide.md#93-dos-errores-frecuentes-con-su-corrección)—.

**Una corrección se hace en el dueño; los demás enlazan. [C]**

| Tema | Dueño | Lo mencionan también |
| --- | --- | --- |
| El punto cero y las alturas de llegada | **Del-Requerimiento-Al-Caso §3** | — |
| El criterio de relevancia | **Del-Requerimiento-Al-Caso §3.3** | — |
| El propósito mínimo | **Del-Requerimiento-Al-Caso §3.4** | — |
| Las cinco preguntas de ida | **Del-Requerimiento-Al-Caso §4** | — |
| Qué recurso representa el acto | **Del-Requerimiento-Al-Caso §5** | — |
| Los dos ejes: estructural y atencional | **Del-Requerimiento-Al-Caso §5.1** | — |
| La promesa de conservación | **Del-Requerimiento-Al-Caso §5.2** | Caso-Encuesta §4.2 |
| Promesas del acto contra promesas del recurso | **Del-Requerimiento-Al-Caso §6.1** | — |
| Qué promesas y estados trae cada recurso | **Del-Requerimiento-Al-Caso §6.2** | — |
| Definición de superficie y estado | Caso-HolaMundo §1 | Caso-Encuesta §1, este §2 |
| Las cinco preguntas de la frase | Caso-HolaMundo §2.2 | Del-Requerimiento-Al-Caso §4 |
| Acto divisible y prueba de corte | Caso-Encuesta §1.2 y §3 | Del-Requerimiento-Al-Caso §4 y §5 |
| Promesa negativa y sus dos observaciones | Caso-Login §2.4 | Marco §3.3 |
| Testigo de hidratación | Caso-HolaMundo §4 | Beginner §7.2, Quick-ABM §3, Marco §5.4 |
| Creación del proyecto | Quick-Guide-Primer-Proyecto §1 | Beginner §4.2 |
| Aislamiento del estado por sesión | Beginner §7.3 | Quick-ABM §2.4 |
| Paralelismo y su techo | Beginner §7.7 | Quick-ABM §2.6 |
| Workflows y protección de rama | Beginner §8 | Quick-ABM §2.7 |
| Procedencia de los conceptos | Marco | todos |

## 3.3 Por dónde entrar

| Perfil | Recorrido |
| --- | --- |
| **Tengo un requerimiento y no hay nada escrito** | [Del-Requerimiento-Al-Caso](Del-Requerimiento-Al-Caso.md) entero → [Caso-HolaMundo §2](Caso-HolaMundo-Page.md) → [Caso-Encuesta §3](Caso-Encuesta-Page.md) |
| **Nunca hice una E2E** | [Quick-Guide-Primer-Proyecto](Quick-Guide-Primer-Proyecto.md) → [Beginner §1 y §4](Beginner-Guide.md) → [Anexo A](Beginner-Guide.md#anexo-a--plantilla-comentada-de-la-clase-base) → [Beginner §6](Beginner-Guide.md#6-cómo-se-escribe-un-caso) |
| **Tengo que decidir qué probar** | [Del-Requerimiento-Al-Caso](Del-Requerimiento-Al-Caso.md) → §2 de este documento → los tres casos de diseño, en orden de dificultad |
| **Ya sé, quiero el camino corto** | [Quick-Guide-ABM](Quick-Guide-ABM.md) |
| **Trabajo sobre Blazor Server** | [Beginner §7](Beginner-Guide.md#7-lo-que-aparece-cuando-la-aplicación-tiene-servidor) completo |
| **QA / analista** | [Del-Requerimiento-Al-Caso](Del-Requerimiento-Al-Caso.md) → §2 de este documento → [Beginner §2 y §5](Beginner-Guide.md) → [Anexo C](Beginner-Guide.md#anexo-c--listas-de-verificación) |
| **DevOps** | [Beginner §8](Beginner-Guide.md#8-los-workflows-de-github-actions) → [§7.4](Beginner-Guide.md#74-la-aplicación-hay-que-compilarla-antes-de-probarla) |
| **PO / autoridad de cambio** | [Del-Requerimiento-Al-Caso](Del-Requerimiento-Al-Caso.md) §1 a §3 → [Beginner §5.1](Beginner-Guide.md#51-el-criterio-de-selección) → [§8.4](Beginner-Guide.md#84-atar-las-pruebas-al-merge-del-pull-request) |
| **Quiero ir más lejos** | [Marco](Marco-La-Superficie-Verificable.md) completo |

---

# 4. Los criterios de este documento

Los del tramo de análisis viven en
[Del-Requerimiento-Al-Caso §11](Del-Requerimiento-Al-Caso.md). Los que sostienen **este** mapa son
tres:

1. **Un documento por pregunta.** Una pregunta se reconoce porque tiene audiencia propia y ritmo de
   cambio propio: un marco conceptual se toca una vez por año y una receta de ABM cada vez que
   aparece un ABM. Juntarlos ata el ritmo del rápido al del lento. **[C]**
2. **Una corrección se hace en el documento dueño del tema**, y los demás enlazan. Repetir ayuda a
   leer; lo que no puede pasar es que dos versiones diverjan en silencio —*«una configuración
   duplicada no es redundancia, es una contradicción esperando fecha»*,
   [Beginner §9.3](Beginner-Guide.md#93-dos-errores-frecuentes-con-su-corrección)—.
3. **Un documento declara qué clase de cosa es.** Una guía de estudio, una receta, un caso de diseño
   y un método propuesto no se leen igual, y el `doc_type` con el `confidence` del encabezado son lo
   primero que hay que mirar. **[C]**

---

> **Este documento cambió de alcance el 2026-09-09.** Nació conteniendo también el tramo de análisis,
> que creció hasta ocupar dos tercios y dejó de ser una puerta de entrada para ser un tratado. Se
> separó a [Del-Requerimiento-Al-Caso.md](Del-Requerimiento-Al-Caso.md) aplicando el criterio 1, que
> es el mismo con el que se argumentó no unificar todo el conjunto en un solo archivo.
