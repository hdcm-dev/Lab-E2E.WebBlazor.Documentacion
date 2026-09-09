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

1. **Cubre el primer eslabón**: alguien te tira su problema encima, entero y desordenado, y hay que
   ordenarlo hasta llegar a superficies, promesas y estados — antes de que exista una pantalla que
   mirar (§1).
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

## 1.1 Por qué este eslabón se volvió necesario

El conjunto documenta esta cadena:

```
situación → propósito → actos → superficies → recurso → estados → pantallas → identificadores → casos
                                           └──────────── acá empezaba el corpus ────────────┘
```

Los tres casos de diseño —[Hola Mundo](Caso-HolaMundo-Page.md), [acceso](Caso-Login-Page.md) y
[encuesta](Caso-Encuesta-Page.md)— parten de una pantalla ya construida, porque documentan
laboratorios que ya existían. Eso enseña el camino **de vuelta**: dada una pantalla, deducir qué
promete. En el trabajo real se llega al revés.

Y hay un motivo histórico por el que este tramo hoy hace falta y antes no. **[C]**

| Era | Qué se diseñaba | Dónde estaba la decisión |
| --- | --- | --- |
| **1. El papel** | El formulario | En el formulario mismo: la estructura del acto y la del artefacto **coincidían por fuerza** — una hoja, un orden, sin estados |
| **2. La transcripción** | La pantalla, calcada del papel | Seguía en el papel: la pantalla heredaba una estructura que nadie volvió a justificar |
| **3. Los recursos** | Maestro-detalle, asistentes, pestañas, modales | **En ningún lado**: aparecieron varias formas posibles para el mismo acto, y ninguna regla para elegir |

La era 1 no estaba equivocada: el papel **era** la superficie, porque el acto era «completar el
formulario» y la hoja era toda la interfaz. Lo que se perdió al llegar la era 3 no fue rigor: fue la
coincidencia forzada. Ahora hay libertad, y la libertad sin criterio se llena con lo que está de
moda —«hagamos un asistente»—.

> **La era 3 agregó una decisión que las dos anteriores no tenían que tomar: qué recurso representa
> el acto. Esa decisión, y el tramo que la precede, son lo que esta sección cubre.**

Y una advertencia que ordena el resto: en *usage-centered design* los casos de uso esenciales son
abstractos, **sin detalle de interfaz**, y el contexto de interacción se define antes que la ventana
([Marco §4.1](Marco-La-Superficie-Verificable.md)). **La superficie no se deduce de la pantalla: se
deduce del acto.**

## 1.2 Quién interviene, y qué se pregunta cada uno

Cada eslabón recibe algo, se hace **una** pregunta propia y entrega algo distinto. Lo importante no
es el organigrama —una misma persona puede ocupar varias filas— sino que **ninguna fila se saltee**.

| # | Quién | Con qué llega | Su pregunta | Qué entrega |
| --- | --- | --- | --- | --- |
| 1 | **Quien pide** | Una situación | ¿Qué me está pasando, y qué haría al respecto? | El propósito |
| 2 | **Quien releva** | El propósito | ¿Qué hace falta saber para eso? ¿Quién lo provee, y qué tiene que estar listo antes? | Los **datos** y los **actos** |
| 3 | **Quien diseña la interacción** | Los actos | ¿Qué recurso representa este acto? ¿En qué estados puede quedar? | Las **superficies**, su recurso y sus estados |
| 4 | **Quien construye** | Superficies y estados | ¿Qué componentes? ¿Qué publico para que se pueda nombrar desde afuera? | La vista y los `data-testid` |
| 5 | **Quien prueba** | La promesa | ¿Qué promete, y cómo lo veo sin espiar por dentro? | Los casos |
| 6 | **PO / autoridad de cambio** | Todo lo anterior | ¿Qué recorrido no puede romperse nunca? | Qué bloquea el merge |

**Dónde se rompe en la práctica:** se saltea el eslabón 3. Se pasa de los actos directo a la
pantalla y el recurso se elige por costumbre. Cuando eso pasa, el eslabón 5 hereda el desorden — y
ahí es donde alguien pregunta «¿esto son tres pruebas o una?» y no hay con qué contestarlo (§1.5).

## 1.3 El punto cero: con qué llega realmente quien pide

**El escenario que se estudia acá es este:** alguien te tira su problema encima, entero y
desordenado, mezclando lo que le pasa con lo que ya decidió y con lo que se imagina que habría que
hacer. Ordenar eso es el trabajo, y empieza por reconocer que **nadie llega con un requerimiento**:
se llega con una **situación**, contada a una altura que casi nunca es la que hace falta.

No hay una primera pregunta universal. Hay que **darse cuenta a qué altura te están hablando** y
recién entonces elegir el movimiento. **[C]**

| Lo que dice | Qué es en realidad | Qué falta | El movimiento |
| --- | --- | --- | --- |
| «Quiero una app para encuestar» | Una **solución** ya elegida | El problema | **Subir**: ¿qué pasa si no la hacés? |
| «Quiero poner líneas de colectivo» | Una **decisión ya tomada** | El motivo, y qué la haría cambiar | **Subir con cuidado** → §1.3.1 |
| «La gente se queja del transporte» | Un **síntoma** | El diagnóstico | **Al costado**: ¿quién, de qué, dónde, desde cuándo? |
| «Quiero mejorar la movilidad» | Una **meta** | La decisión | **Bajar**: ¿qué vas a hacer distinto? |
| «No sé cómo funciona mi ciudad» | **Exploración legítima** | La hipótesis | **Acompañar** → §1.3.2 |

Ninguna de esas frases es un mal punto de partida: son **el punto de partida normal**. Lo que sería
un error es tratarlas todas igual, o pedirle a quien pide que llegue con la altura ya resuelta.

### 1.3.1 El caso incómodo: cuando ya decidió

Pasa seguido y casi nunca se dice: **a veces no se viene a decidir, se viene a respaldar.** La
decisión está tomada por razones que no son de datos —de gestión, de oportunidad, de política— y lo
que se necesita es evidencia que la sostenga.

Eso no lo vuelve ilegítimo, pero **cambia el producto**:

- No hace falta un instrumento de exploración sino de **evidencia**: trazable, auditable, defendible
  ante alguien que la va a discutir.
- Y aparece un riesgo que hay que poner sobre la mesa **antes** de construir nada:
  **¿qué hacemos si los datos dicen lo contrario?** Si la respuesta es «no los publicamos», lo que se
  está por construir no es un relevamiento, y conviene saberlo entre todos.

Preguntarlo es del eslabón 2, no del 1. Es lo que evita construir algo que después nadie quiere
mirar.

### 1.3.2 Cuando no se sabe: la exploración

Este caso rompe la pregunta «¿qué decisión vas a tomar?», porque **no tiene respuesta — y la
ignorancia es un punto de partida legítimo**, no un cliente mal preparado. Querer entender cómo
funciona algo antes de decidir nada es un propósito válido.

Pero explorar no es preguntar cualquier cosa. Lo que reemplaza a la decisión es la **hipótesis**:

> **¿Qué esperás encontrar? ¿Y qué te sorprendería?**

La segunda mitad es la que rinde, porque pide algo **falsable**. «Me sorprendería que en el sur
viajen más de una hora» produce campos —origen, tiempo, transbordos— igual que los produciría una
decisión.

Y hay que decir lo que la exploración cuesta, porque es real: un relevamiento sin decisión atrás es
**más ancho, más caro y más lento de convertir en algo**. La contrapartida es lo que ninguna
decisión previa habría preguntado: si el formulario se derivó de una decisión sobre colectivos,
nunca van a aparecer las bicisendas ni una ordenanza de transporte aéreo.

### 1.3.3 Lo que hay que conseguir: el criterio de relevancia

Ni «la decisión» ni «los requerimientos». De quien pide hace falta **una sola cosa**, y admite dos
formas:

> **El criterio de relevancia: qué hace que un dato valga la pena capturarse.**

| Origen | Quién provee el criterio | Un campo entra si… |
| --- | --- | --- |
| Hay una decisión | La decisión | …puede cambiarla |
| Hay exploración | Las hipótesis | …puede confirmarlas o refutarlas |
| No hay ninguna de las dos | **Nadie** | …«por las dudas» ← acá se para |

Esa última fila es un diagnóstico que hay que saber dar: **todavía no hay con qué diseñar nada.** Es
un resultado válido de una reunión, y mucho más barato que descubrirlo con el formulario hecho.

### 1.3.4 Cuando el pedido ya trae las necesidades de datos

No siempre hace falta el diagnóstico de altura. A veces el pedido llega ya formulado en datos —«quiero
saber cuántas personas se mueven, dónde y con qué frecuencia»— y quien lo trae es el experto del
dominio. Ahí **el propósito no hace falta para estructurar**: eso alcanza para P1 a P5, y entrar a
interrogar la intención hace perder tiempo sin agregar nada. Se salta a §1.4 y listo.

**Donde el propósito se sigue pagando es en otro lado: no para armar la pantalla, sino para decidir
las reglas** — que es justamente lo que después verifica la prueba. La estructura no las determina:

| Lo que la estructura no contesta | Por qué necesita el propósito |
| --- | --- |
| ¿La edad es obligatoria? | Depende de si se va a segmentar por edad |
| «Frecuencia» ¿es *diaria/semanal* o *cantidad de viajes por semana*? | Depende de qué se va a calcular |
| ¿Se acepta una respuesta incompleta? | Para contar porcentajes tal vez sí; para trazar recorridos no |
| ¿La distancia se limita en 200 km? | El límite sale del dominio de la decisión, no del tipo de dato |

Ninguna de esas cuatro es «¿para qué querés esto?». Son preguntas puntuales sobre un campo, y se
hacen **solo donde la estructura queda indeterminada**. A eso conviene llamarlo el **propósito
mínimo**: no relevar la intención entera, sino tirar del hilo ahí donde hay que elegir y el dato no
elige solo. **[C]**

> **El riesgo de no hacerlo** es tomar los nombres de campo como si fueran datos. *«Frecuencia»* es
> una etiqueta, no una medida. Si nadie pregunta cómo se va a mirar, sale un panel prolijo que
> produce datos que después no se pueden cruzar — y eso no se descubre hasta que alguien quiso
> usarlos.

**En resumen**, §1.3 aplica cuando el pedido llega vago. Cuando ya trae las necesidades de datos, se
entra directo en §1.4 y se vuelve acá solo por lo que quedó indeterminado.

## 1.4 Las cinco preguntas de ida

Con el criterio de relevancia en la mano, y todavía sin abrir un editor. **[C]**

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

La que más rinde, porque **descubre actos que nadie nombró**. «¿De qué localidad sos?» pide una lista
controlada; esa lista no se administra sola; aparece *administrar localidades*, que no estaba en
ningún pedido y es una superficie entera con su propio rol.

Un propósito que se contesta con una sola superficie casi siempre tiene una precondición sin mirar.

### P5 — ¿Qué puede faltar, fallar o tardar?

Acá salen los **estados**, todavía sin dibujar nada. El *UI Stack* sirve de lista de control —vacío,
cargando, parcial, error, ideal— con el criterio que el marco le agrega
([Marco §4.2](Marco-La-Superficie-Verificable.md)):

> **Dos estados son distintos cuando la salida que se le ofrece a la persona es distinta.**

Por eso «no hay datos» y «el filtro no encontró nada» son dos: en el primero la salida es crear el
primero, en el segundo es limpiar el filtro. Confundirlos le ofrece a la persona la acción
equivocada.

## 1.5 Qué recurso representa el acto

Es la decisión que la era 3 dejó sin regla (§1.1), y se puede dar una: **el recurso no se elige, se
deriva de dos propiedades del acto** — si es divisible, y si sus partes prometen algo por separado.
**[C]**

| Recurso | Qué propiedad del acto lo justifica | La señal que lo confirma | Qué lo desmiente |
| --- | --- | --- | --- |
| **Formulario simple** | Acto indivisible: se completa de una | Todo se necesita junto para que pase algo | Se abandona por cantidad de campos |
| **Asistente** | Acto **divisible**: se parte por comodidad y hay orden, porque un tramo condiciona al siguiente | Si abandono en el medio, **no queda nada** | Alguna etapa ya entrega algo → era un recorrido |
| **Pestañas** | **Varios** actos sobre el mismo sujeto, independientes entre sí | Puedo usar una y ninguna otra, y sigue teniendo sentido | Hay orden obligatorio → era un asistente |
| **Maestro-detalle** | Dos actos anidados: el detalle no existe sin el maestro y se repite N veces para el mismo | Necesito ver el maestro **mientras** trabajo el detalle | El detalle es uno solo → era un campo más |
| **Listado + ficha (ABM)** | Acto de administración recurrente sobre un catálogo | Antes de actuar hay que **encontrar** | No hay búsqueda posible → era un formulario |
| **Modal** | Un acto **anidado** que interrumpe otro sin abandonarlo | Al cerrarlo sigo en el mismo acto, no en otro | Al volver aterricé en otro lado → era una navegación disfrazada |
| **Página de llegada** | No hay acto: hay una condición que llega de afuera | El verbo es *llego*, no *hago* | Hay algo que completar → es una superficie de acto |

**El par que más se confunde es asistente contra pestañas**, y es instructivo porque se ven casi
igual —contenido partido en secciones— y son estructuralmente opuestos:

| | Asistente | Pestañas |
| --- | --- | --- |
| ¿Alguna parte promete sola? | **Ninguna** | **Todas** |
| ¿Hay orden obligatorio? | Sí | No |
| Superficies | **Una**, con estados | **Varias** |
| Clases de prueba | Una | Una por pestaña |

Se distinguen con P3, hecha antes de dibujar: **si abandono en el medio, ¿queda algo hecho?**

**Una precisión sobre el modal, porque se lo suele reducir a la confirmación.** Confirmar un borrado
es *un caso* de acto anidado; la propiedad general cubre también «agregar una localidad que no está
en la lista» en el medio de la encuesta. Lo que lo define no es la gravedad de lo que pregunta, sino
que **al cerrarlo se sigue en el mismo acto**.

### 1.5.1 El segundo eje: qué pasa con la mirada

La tabla de arriba usa un solo eje, el **estructural** —si el acto es divisible y si sus partes
prometen solas—, y ese eje decide **cuántas superficies** hay. Pero no alcanza para elegir el
recurso, porque varios son estructuralmente compatibles con el mismo acto. Un flujo de tres tramos
se puede montar saltando de página, cambiando de panel en la misma página o superponiendo. Lo que
decide entre esos es otro eje, **atencional**: qué se hace con el contexto de la persona. **[C]**

| Recurso | Qué pasa con el contexto | Para qué |
| --- | --- | --- |
| **Modal** | **Se conserva a la vista**: se superpone, no reemplaza | Interrumpir sin desorientar |
| **Asistente** | **Se reemplaza, a propósito** | Concentrar en un subconjunto de la información |
| **Pestañas** | Se reemplaza, pero el mapa completo queda visible en los rótulos | Ofrecer sin imponer orden |
| **Maestro-detalle** | **Coexisten los dos** en la misma vista | Trabajar el detalle sin perder de vista el todo |
| **Listado + ficha** | Se reemplaza, con vuelta al listado | Encontrar primero, actuar después |
| **Formulario simple** | No hay contexto que perder | — |

**Los dos ejes se leen en orden**: el estructural dice cuántas superficies hay y descarta los
recursos incompatibles; el atencional elige entre los que quedan. Poner un asistente donde el acto
no es divisible es un error del primer eje; poner un asistente donde la persona necesitaba seguir
viendo el resto es un error del segundo, y se paga en abandono, no en datos mal cargados.

### 1.5.2 Lo que **no** distingue: conservar lo cargado

Es tentador usar la conservación para definir el modal —«te devuelve donde estabas»—, y es un error:
**conservar es transversal.** Un asistente que salta de página también conserva al volver, las
pestañas conservan al cambiar, el maestro-detalle conserva al pasar de un detalle a otro. No sirve
para elegir nada.

**Pero justamente por eso importa**, y de otra manera:

> **Cada vez que un recurso fragmenta un acto, nace una promesa de conservación — y es la que más se
> da por sentada.**

Se da por sentada porque parece lógica y trivial: *claro que si vuelvo, lo que cargué sigue ahí*. Y
lo trivial es exactamente lo que nadie escribe, y por eso lo que se rompe sin que nadie se entere.
Que la encuesta del laboratorio tenga el caso `PermiteVolverAtrasConservandoLoCargado` no es obvio:
alguien se tomó el trabajo de escribir lo evidente
**[E: ../../../Lab-E2E.WebBlazor/tests/MovilidadUrbana.E2ETests/EncuestaTests.cs]**.

El gesto que hay que probar cambia con el recurso, pero siempre existe:

| Recurso | El gesto que lo pone a prueba |
| --- | --- |
| **Asistente** | Volver al tramo anterior |
| **Modal** | Cerrarlo o cancelarlo |
| **Pestañas** | Cambiar de pestaña y volver |
| **Maestro-detalle** | Cambiar de detalle y volver |
| **Listado + ficha** | Volver al listado — **¿y el filtro que había puesto?** |

Esa última fila es la que más se olvida, porque la conservación no es solo de lo que la persona
escribió: también es de **cómo dejó la vista**.

Y se verifica como toda promesa sobre la memoria: **yendo y volviendo, nunca leyendo el modelo**
([Caso-Encuesta §4.2](Caso-Encuesta-Page.md)). Un recurso que fragmenta no lleva un caso: lleva el
del acto, y el de que fragmentar no costó nada. **[C]**

## 1.6 La cadena no es una tubería

Los eslabones existen, pero no se recorren una sola vez ni en orden. Los retornos más frecuentes:

| Vuelve | Cuándo |
| --- | --- |
| **2 → 1** | Al buscar los actos se ve que el propósito no alcanza para decidir qué se pregunta |
| **3 → 2** | Al elegir el recurso aparece un acto que faltaba — la precondición de P4 es exactamente eso |
| **5 → 3** | Al escribir la promesa no sale la frase: *si no podés escribirla, el problema casi nunca es de la prueba, es del diseño* ([Caso-HolaMundo §2](Caso-HolaMundo-Page.md)) |

Lo que sí es firme es el **orden de dependencia**: no se puede elegir el recurso sin saber el acto,
ni escribir el caso sin saber la promesa. El recorrido es de ida y vuelta; la dependencia no.

## 1.7 Dos ejemplos trabajados

Dos orígenes distintos, para que la sección no enseñe un solo camino.

### A. Desde un síntoma

> *«Me están reventando con el transporte. En los barrios del sur dicen que no llegan a horario. No
> sé si es verdad o es la oposición.»*

Un síntoma, y con desconfianza sobre el propio síntoma. **Nadie pidió una encuesta.**

| Movimiento | Qué pasa |
| --- | --- |
| Al costado | *«¿Quién se queja, de qué exactamente, y desde cuándo?»* → tarda, no llega, no pasa |
| Hacia abajo | *«Si fuera cierto, ¿qué harías?»* → agregar frecuencia, o una línea → **aparece la decisión** |
| Al costado otra vez | *«¿Y si fuera cierto pero no en el sur?»* → «necesito saber dónde» → **la localidad se vuelve obligatoria** |
| Honesto (§1.3.1) | *«¿Y si los datos dicen que llegan bien?»* → «lo quiero saber igual» → **es una duda genuina, no un pedido de respaldo** |

Recién ahí hay criterio de relevancia. Y aparece algo que sin este tramo no se habría visto: la duda
es **sobre la validez del síntoma**, así que el instrumento tiene que poder decir *que no* — lo cual
cambia hasta cómo se pregunta.

Con eso, las cinco preguntas:

| Paso | Qué sale |
| --- | --- |
| **P1** actos | responder la encuesta · ver cuántas respuestas hay |
| **P2** roles | quien responde · quien planifica |
| **P3** abandono | responder: si abandono no queda nada → **una** superficie |
| **P4** precondiciones | la localidad sale de una lista controlada → **aparece el ABM de localidades** |
| **P5** qué falla | datos incompletos · el registro no se completa · todavía no hay respuestas |

Y §1.5: ocho campos derivados, nada se entrega en el medio, hay orden →
**acto divisible → asistente**. Los tres tramos aparecen **acá**, y con motivo.

#### El caso de borde, que es donde se ve si el criterio sirve

**¿«Ver cuántas van» es una superficie propia?** Se decide con P1 y P3:

- **P1**: no tiene acto propio. Es un dato que se mira al pasar, no algo que alguien *complete*.
- **P3**: no se puede abandonar a la mitad, porque no hay mitad.

**No es superficie: es un estado visible de la otra.** Y el criterio muestra dónde estaría el
límite: si el propósito hubiera pedido *ver el listado de respuestas y filtrarlo*, ahí sí hay acto
propio, rol propio y abandono posible — otra superficie, con su recurso propio (listado + ficha).

### B. Desde la exploración

> *«No sé cómo funciona mi ciudad. Capaz faltan líneas, capaz faltan avenidas, capaz hay que pensar
> bicisendas o hasta transporte aéreo. Quiero entender antes de prometer nada.»*

No hay decisión, y forzar una sería falsear la conversación. El movimiento es **acompañar** y pedir
hipótesis (§1.3.2): *¿qué esperás encontrar, y qué te sorprendería?* De ahí salen tres o cuatro
frases falsables, y **de esas frases salen los campos**.

Lo que cambia respecto de A, y conviene tenerlo escrito:

| | Desde una decisión (A) | Desde la exploración (B) |
| --- | --- | --- |
| Criterio de relevancia | La decisión | Las hipótesis |
| Ancho del instrumento | Angosto y justificado | **Más ancho**, y hay que decir que cuesta |
| Qué se pregunta | Lo que cambia la decisión | Lo que puede refutar una creencia |
| Qué se descubre | Lo que se fue a buscar | **Lo que nadie habría preguntado** |
| Riesgo | Perder lo que la decisión no contempló | Recolectar mucho y no poder concluir |

**Y algo que suele aparecer solo en B**: si las hipótesis son sobre modos que hoy no existen
—bicisendas, transporte aéreo—, el acto ya no es «responder por cómo viajo» sino también «decir cómo
querría viajar». Son **dos actos**, y P3 los separa: cada uno se puede completar sin el otro.

## 1.8 Qué **no** se decide en este tramo

| No se decide acá | Se decide después |
| --- | --- |
| Cuántas pantallas | Al diseñar la interacción: una superficie puede ocupar varias vistas, y una vista alojar varias superficies |
| Los `data-testid` | Al escribir la vista, por quien la escribe ([Beginner §5.3](Beginner-Guide.md#53-el-contrato-de-selección)) |
| Cuántos casos de prueba | Al escribir la suite: un caso por promesa, y un motivo de falla por caso |
| Qué se prueba con E2E y qué con unitarias | Con los tres filtros de [Beginner §5.1](Beginner-Guide.md#51-el-criterio-de-selección) |

Y una consecuencia que vale por toda la sección: **los tres tramos de la encuesta no son un
requerimiento ni un dato del dominio.** Son la respuesta de §1.5 a una propiedad del acto. Si mañana
los campos bajan de ocho a tres, el asistente sobra y la promesa sigue intacta — que es exactamente
por qué la prueba no se rompe con el rediseño.

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
| El punto cero y las alturas de llegada | **E2E-Resumen §1.3** | — |
| El criterio de relevancia | **E2E-Resumen §1.3.3** | — |
| El propósito mínimo | **E2E-Resumen §1.3.4** | — |
| Las cinco preguntas de ida | **E2E-Resumen §1.4** | — |
| Qué recurso representa el acto | **E2E-Resumen §1.5** | — |
| Los dos ejes: estructural y atencional | **E2E-Resumen §1.5.1** | — |
| La promesa de conservación | **E2E-Resumen §1.5.2** | Caso-Encuesta §4.2 |
| Definición de superficie y estado | Caso-HolaMundo §1 | Caso-Encuesta §1, este §2 |
| Las cinco preguntas de la frase | Caso-HolaMundo §2.2 | este §1.4 |
| Acto divisible y prueba de corte | Caso-Encuesta §1.2 y §3 | este §1.4 y §1.5 |
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

1. **Nadie llega con un requerimiento**: llega con una situación, a una altura que casi nunca es la
   que hace falta. El primer trabajo es reconocer la altura, no aplicar una secuencia.
2. **Lo que hay que conseguir no es «la decisión» sino el criterio de relevancia**: qué hace que un
   dato valga la pena capturarse. Lo provee una decisión, o lo proveen hipótesis.
3. **No saber es un punto de partida legítimo.** En la exploración la hipótesis reemplaza a la
   decisión, y la pregunta que rinde es *qué te sorprendería*.
4. **A veces no se viene a decidir sino a respaldar.** Preguntar qué se hace si los datos dicen lo
   contrario, antes de construir.
5. **Sin decisión ni hipótesis no hay con qué diseñar**, y decirlo es un resultado válido.
6. **Si el pedido ya trae los datos, se estructura sin preguntar el propósito.** El propósito mínimo
   se pide solo donde la estructura no determina una regla: obligatoriedad, granularidad, qué hacer
   con lo incompleto y de dónde salen los límites.
7. **La superficie se deduce del acto, no de la pantalla.** La pantalla es una decisión posterior.
8. **Un acto es lo que alguien necesita terminar**, con sujeto humano adelante del verbo. Un cajón
   —«gestionar el módulo»— no es un acto.
9. **Dos roles sobre el mismo dato casi siempre son dos superficies**, aunque la pantalla se parezca.
10. **Si al abandonar en el medio no queda nada, era una sola superficie**, por más tramos que tenga.
11. **La precondición descubre actos que nadie nombró.** Es la pregunta que más rinde.
12. **Dos estados son distintos cuando la salida que se le ofrece a la persona es distinta.**
13. **El recurso se decide con dos ejes.** El estructural —si el acto es divisible y si sus partes
    prometen solas— dice cuántas superficies hay y descarta lo incompatible; el atencional —si el
    contexto se conserva a la vista o se reemplaza— elige entre lo que queda.
14. **Conservar lo cargado no distingue ningún recurso: es transversal.** Y por eso es la promesa que
    más se da por sentada — cada vez que un recurso fragmenta un acto, nace una, y lo trivial es
    justamente lo que nadie escribe.
15. **La cadena tiene retornos, pero la dependencia no**: no se elige recurso sin acto, ni se escribe
    el caso sin promesa.

Y de §2, para no perder el hilo con el resto del conjunto:

16. **Una clase por superficie; un método por promesa; un motivo de falla por método.**
17. **Un estado se observa, una promesa se ejercita.**
18. **Una corrección se hace en el documento dueño del tema**, y los demás enlazan.

---

> **Estado de este documento.** La §1 es material nuevo: no está respaldada por ningún caso del
> laboratorio, porque los tres existentes parten de pantallas ya construidas. Es la aplicación del
> criterio del conjunto al camino de ida, más el tramo que la era 3 volvió necesario (§1.1). Su
> `confidence` es **media** a propósito, y la forma de subirla es una sola: **usarla para deducir una
> superficie que todavía no exista, construirla, y anotar en qué falló el método** — no en qué falló
> el producto. Hasta que eso pase, §1 es una hipótesis de trabajo bien argumentada, no un
> procedimiento verificado. **[C]**
