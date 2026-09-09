---
doc_id: E2E-03
doc_type: documento-integrador
title: Del requerimiento al caso — puerta de entrada y mapa del conjunto
status: vigente
origin: agente
confidence: media
owner: Lab-E2E.WebBlazor.Documentacion
last_review: 2026-09-09
audience: [desarrollo, qa, po]
traces: [E2E-00, E2E-01, E2E-02]
---

# Del requerimiento al caso

Este documento es la puerta de entrada al conjunto. Hace dos cosas que ningún otro hace:

1. **Cubre el primer eslabón**, el que va del requerimiento hablado a la superficie — antes de que
   exista una pantalla que mirar (§1).
2. **Une los dos vocabularios** del conjunto y dice qué documento es dueño de cada tema, para que
   una corrección se haga en un solo lugar (§2 y §3).

Los demás documentos enseñan a probar **una pantalla que ya existe**. Este empieza antes.

## Marcas de evidencia

| Marca | Significado |
| --- | --- |
| **[E: ruta]** | *Evidencia en el repositorio*: se comprueba abriendo ese archivo |
| **[V]** | *Verificado por ejecución*: se corrió y se observó el resultado |
| **[C]** | *Criterio*: decisión del laboratorio, defendible y discutible |

---

# 1. Del requerimiento a la superficie

## 1.1 El eslabón que faltaba

El conjunto documenta esta cadena:

```
requerimiento → actos → superficies → estados → pantallas → identificadores → casos
                                   └────────── acá empezaba el corpus ──────────┘
```

Los tres casos de diseño —[Hola Mundo](Caso-HolaMundo-Page.md), [acceso](Caso-Login-Page.md) y
[encuesta](Caso-Encuesta-Page.md)— parten de una pantalla ya construida, porque documentan
laboratorios que ya existían. Eso enseña el camino **de vuelta**: dada una pantalla, deducir qué
promete.

En el trabajo real se llega al revés. Alguien plantea una necesidad y no hay pantallas, ni botones,
ni campos: hay que **decidir** cuántas superficies existen antes de dibujar nada.

Y conviene decirlo, porque ordena: **el camino de ida es el original de la tradición de la que esto
sale.** En *usage-centered design* los casos de uso esenciales son abstractos, **sin detalle de
interfaz**, y el contexto de interacción se define antes que la ventana
([Marco §4.1](Marco-La-Superficie-Verificable.md)). La superficie **no se deduce de la pantalla: se
deduce del acto.**

> **La pantalla es una decisión posterior.** Cuántas superficies junto en una vista, o en cuántos
> tramos parto una, se decide después — y por eso la promesa sobrevive al rediseño.

## 1.2 Las cinco preguntas de ida

Se responden sobre el requerimiento hablado, sin abrir un editor. **[C]**

### P1 — ¿Qué actos necesita completar alguien?

Verbos, en primera persona, sin interfaz. Un acto es **una unidad de trabajo que alguien necesita
terminar**, no una funcionalidad del sistema.

| | |
| --- | --- |
| ✅ | «responder la encuesta», «dar de alta una localidad» |
| ❌ | «gestionar el módulo de encuestas», «CRUD de localidades» |

La segunda columna no nombra actos: nombra cajones. Si no podés poner un sujeto humano adelante del
verbo, todavía no llegaste al acto.

### P2 — ¿Quién hace cada uno?

Dos roles distintos sobre el mismo dato **casi siempre son dos superficies**, aunque la pantalla se
parezca. Quien responde una encuesta y quien administra el catálogo que la alimenta no comparten
promesa, aunque los dos toquen «localidades».

### P3 — Si abandono en el medio, ¿queda algo hecho?

Es la prueba de corte de [§3.1 del caso de la encuesta](Caso-Encuesta-Page.md), aplicada **a la
tarea y no al marcado**:

| Respuesta | Conclusión |
| --- | --- |
| **No queda nada** | Era **una sola** superficie, por más tramos que tenga |
| **Queda algo que la persona puede usar** | Eran **varias**: entre una y otra hay un desenlace |

Un acto que se completa en tramos por comodidad de carga sigue siendo **un** acto: eso es un *acto
divisible*, y sus tramos son estados, no superficies.

### P4 — ¿Qué necesita tener listo antes de empezar?

La que más rinde, porque **descubre actos que el requerimiento no nombró**. «¿De qué localidad
sos?» pide una lista controlada; esa lista no se administra sola; aparece *administrar localidades*,
que nadie pidió y es una superficie entera con su propio rol.

Un requerimiento que se contesta con una sola superficie casi siempre tiene una precondición sin
mirar.

### P5 — ¿Qué puede faltar, fallar o tardar?

Acá salen los **estados**, todavía sin dibujar nada. El *UI Stack* sirve de lista de control —vacío,
cargando, parcial, error, ideal— con el criterio que el marco le agrega
([Marco §4.2](Marco-La-Superficie-Verificable.md)):

> **Dos estados son distintos cuando la salida que se le ofrece a la persona es distinta.**

Por eso «no hay datos» y «el filtro no encontró nada» son dos: en el primero la salida es crear el
primero, en el segundo es limpiar el filtro. Confundirlos le ofrece a la persona la acción
equivocada.

## 1.3 Ejemplo trabajado: la encuesta, deducida al derecho

El requerimiento, como lo diría quien lo pide — sin una sola pantalla adentro:

> *«Necesito saber cómo se mueve la gente en la ciudad para planificar el transporte. Quiero que la
> gente pueda cargar sus datos de viaje, y quiero ver cuántas respuestas llevo.»*

| Paso | Qué sale |
| --- | --- |
| **P1** actos | responder la encuesta · ver cuántas respuestas hay |
| **P2** roles | quien responde · quien planifica |
| **P3** abandono | responder: si abandono no queda nada → **una** superficie |
| **P4** precondiciones | la localidad sale de una lista controlada → **aparece el ABM de localidades** |
| **P5** qué falla | datos incompletos · el registro no se completa · todavía no hay respuestas |

### El caso de borde, que es donde se ve si el criterio sirve

**¿«Ver cuántas van» es una superficie propia?** Se decide con P1 y P3:

- **P1**: no tiene acto propio. Es un dato que se mira al pasar, no algo que alguien *complete*.
- **P3**: no se puede abandonar a la mitad, porque no hay mitad.

**No es superficie: es un estado visible de la otra.** Y el criterio muestra dónde estaría el
límite: si el requerimiento hubiera dicho *«quiero ver el listado de respuestas y filtrarlo»*, ahí
sí hay acto propio, rol propio y abandono posible — otra superficie.

### Lo que todavía no apareció en ningún renglón

Que sean tres tramos. Que haya «Anterior» y «Siguiente». Que el error se pinte de rojo. Que el
contador viva arriba a la derecha.

**Nada de eso es estructura: es diseño de interacción, y viene después.** Que la promesa se haya
fijado antes que la pantalla es exactamente lo que la hace sobrevivir a que mañana el asistente sea
un acordeón ([Pregunta 4](Caso-HolaMundo-Page.md)).

## 1.4 Qué **no** se decide en este paso

| No se decide acá | Se decide después |
| --- | --- |
| Cuántas pantallas | Al diseñar la interacción: una superficie puede ocupar varias vistas, y una vista alojar varias superficies |
| Los `data-testid` | Al escribir la vista, por quien la escribe ([Beginner §5.3](Beginner-Guide.md#53-el-contrato-de-selección)) |
| Cuántos casos de prueba | Al escribir la suite: un caso por promesa, y un motivo de falla por caso |
| Qué se prueba con E2E y qué con unitarias | Con los tres filtros de [Beginner §5.1](Beginner-Guide.md#51-el-criterio-de-selección) |

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
| **E2E-Resumen** *(este)* | ¿De dónde salen las superficies, y qué documento leo para qué? |
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
| Del requerimiento a la superficie | **E2E-Resumen §1** | — |
| Definición de superficie y estado | Caso-HolaMundo §1 | Caso-Encuesta §1, este §2 |
| Las cinco preguntas de la frase | Caso-HolaMundo §2.2 | este §1 |
| Acto divisible y prueba de corte | Caso-Encuesta §1.2 y §3 | este §1.2 |
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
| **Tengo un requerimiento y no hay nada escrito** | §1 de este documento → [Caso-HolaMundo §2](Caso-HolaMundo-Page.md) → [Caso-Encuesta §3](Caso-Encuesta-Page.md) |
| **Nunca hice una E2E** | [Quick-Guide-Primer-Proyecto](Quick-Guide-Primer-Proyecto.md) → [Beginner §1 y §4](Beginner-Guide.md) → [Anexo A](Beginner-Guide.md#anexo-a--plantilla-comentada-de-la-clase-base) → [Beginner §6](Beginner-Guide.md#6-cómo-se-escribe-un-caso) |
| **Tengo que decidir qué probar** | §1 y §2 de este documento → los tres casos de diseño, en orden de dificultad |
| **Ya sé, quiero el camino corto** | [Quick-Guide-ABM](Quick-Guide-ABM.md) |
| **Trabajo sobre Blazor Server** | [Beginner §7](Beginner-Guide.md#7-lo-que-aparece-cuando-la-aplicación-tiene-servidor) completo |
| **QA / analista** | §1 y §2 de este documento → [Beginner §2 y §5](Beginner-Guide.md) → [Anexo C](Beginner-Guide.md#anexo-c--listas-de-verificación) |
| **DevOps** | [Beginner §8](Beginner-Guide.md#8-los-workflows-de-github-actions) → [§7.4](Beginner-Guide.md#74-la-aplicación-hay-que-compilarla-antes-de-probarla) |
| **PO / autoridad de cambio** | §1 de este documento → [Beginner §5.1](Beginner-Guide.md#51-el-criterio-de-selección) → [§8.4](Beginner-Guide.md#84-atar-las-pruebas-al-merge-del-pull-request) |
| **Quiero ir más lejos** | [Marco](Marco-La-Superficie-Verificable.md) completo |

---

# 4. Los criterios, en una lista

De §1, que es lo propio de este documento:

1. **La superficie se deduce del acto, no de la pantalla.** La pantalla es una decisión posterior.
2. **Un acto es lo que alguien necesita terminar**, con sujeto humano adelante del verbo. Un cajón
   —«gestionar el módulo»— no es un acto.
3. **Dos roles sobre el mismo dato casi siempre son dos superficies**, aunque la pantalla se parezca.
4. **Si al abandonar en el medio no queda nada, era una sola superficie**, por más tramos que tenga.
5. **La precondición descubre actos que el requerimiento no nombró.** Es la pregunta que más rinde.
6. **Dos estados son distintos cuando la salida que se le ofrece a la persona es distinta.**
7. **Lo que no apareció en las cinco preguntas es diseño de interacción**, y no pertenece a la
   promesa.

Y de §2, para no perder el hilo con el resto del conjunto:

8. **Una clase por superficie; un método por promesa; un motivo de falla por método.**
9. **Un estado se observa, una promesa se ejercita.**
10. **Una corrección se hace en el documento dueño del tema**, y los demás enlazan.

---

> **Estado de este documento.** La §1 es material nuevo, escrito el 2026-09-09: no está respaldada
> por un caso del laboratorio, sino por la aplicación del criterio existente al camino inverso. Su
> `confidence` es **media** a propósito, y la forma de subirla es usarla para deducir una superficie
> que todavía no exista y ver qué falla. **[C]**
