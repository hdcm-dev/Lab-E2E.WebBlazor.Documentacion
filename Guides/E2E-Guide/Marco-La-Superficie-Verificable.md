# La superficie verificable — marco conceptual y procedencia

**Qué es:** el encuadre de los dos documentos de caso de esta carpeta. De dónde viene
cada concepto que usan, qué se le cambió al traerlo, y qué es propio de este laboratorio.

**Por qué existe:** los dos documentos de caso enseñan un método sin decir de dónde sale.
Eso tiene dos costos. El lector no puede ir más lejos por su cuenta, y quien escribe
**reinventa cosas que ya están formalizadas** — nos pasó dos veces, y las dos están
señaladas más abajo.

---

## Índice

- **[1. Qué encuadra este documento](#1-que-encuadra-este-documento)**
- **[2. Las tres tradiciones](#2-las-tres-tradiciones)** — y por qué casi nunca se cruzan
- **[3. Tradición I — Especificación y verificación formal](#3-tradicion-i--especificacion-y-verificacion-formal)** — de dónde sale «promesa», y el hallazgo de las hiperpropiedades
- **[4. Tradición II — Diseño de interacción centrado en el uso](#4-tradicion-ii--diseno-de-interaccion-centrado-en-el-uso)** — de dónde salen «superficie» y «estado»
- **[5. Tradición III — Especificación ejecutable y prueba](#5-tradicion-iii--especificacion-ejecutable-y-prueba)** — de dónde sale la forma del caso
- **[6. Lo que este laboratorio agrega](#6-lo-que-este-laboratorio-agrega)**
- **[7. Tabla de procedencia](#7-tabla-de-procedencia)**
- **[8. Bibliografía, con su grado de verificación](#8-bibliografia-con-su-grado-de-verificacion)**
- **[9. Lo que este documento no cubre](#9-lo-que-este-documento-no-cubre)**

---

## 1. Qué encuadra este documento

Los dos documentos de caso —[Hola Mundo](Caso-HolaMundo-Page.md) y
[acceso](Caso-Login-Page.md)— usan un vocabulario propio: *superficie*, *promesa*,
*estado*, *testigo*, *promesa negativa*. Ese vocabulario **no se inventó acá**. Casi todo
viene de tres tradiciones que existen desde hace décadas, y el aporte de este laboratorio
es haberlas puesto a trabajar juntas sobre un mismo archivo.

Este documento hace tres cosas:

1. **Nombra las tres tradiciones** y dice por qué normalmente no se hablan entre sí.
2. **Da la procedencia de cada concepto**, con su fuente, y muestra qué se le cambió.
3. **Señala dónde reinventamos** algo que ya tenía nombre — que es la parte más útil,
   porque abre la puerta a la versión madura de cada idea.

---

## 2. Las tres tradiciones

### 2.1 ¿Cuáles son?

**Respuesta: especificación formal, diseño de interacción, y prueba automatizada.**

| | Tradición | Qué aporta | Su pregunta |
| --- | --- | --- | --- |
| **I** | **Especificación y verificación formal** | Qué es una promesa, y cómo se clasifica | *¿Qué significa que el sistema sea correcto?* |
| **II** | **Diseño de interacción centrado en el uso** | Qué es una superficie y qué es un estado | *¿Cuál es la unidad de diseño de una interfaz?* |
| **III** | **Especificación ejecutable y prueba automatizada** | Qué forma tiene un caso, y cómo no se rompe | *¿Cómo se comprueba, y quién lo entiende?* |

Una precisión sobre el encuadre, porque cambia la lectura: **dos de las tres son
tradiciones de oficio y la tercera es académica.** El diseño de interacción y la prueba
automatizada se practican todos los días; la especificación formal casi nunca aparece
fuera de sistemas críticos. Y sin embargo es la que dio la respuesta más precisa a la
pregunta más difícil de estos documentos (§3.3).

### 2.2 ¿Por qué casi nunca se cruzan?

**Respuesta: porque cada una tiene su propio objeto, y ninguno es «la pantalla».**

| Tradición | Su objeto | Qué le queda afuera |
| --- | --- | --- |
| I | El **programa** o el sistema, como objeto matemático | La persona, y lo que ve |
| II | La **experiencia** y la tarea de la persona | Que eso se pueda comprobar solo |
| III | El **código de prueba** y su relación con el de producción | De dónde salió lo que se decidió probar |

**La superficie es exactamente el punto donde los tres objetos coinciden**: es una unidad
de diseño (II), que enuncia una promesa clasificable (I), y que resulta observable desde
afuera (III). Ese es el aporte del encuadre, y es la respuesta a *«¿a qué cuerpo del
conocimiento pertenece?»* — a ninguno de los tres por separado.

---

## 3. Tradición I — Especificación y verificación formal

### 3.1 «Promesa» viene del contrato, pero cambió de partes

**Fuente:** Bertrand Meyer, *Design by Contract* — *Object-Oriented Software
Construction* (1988; 2ª ed. 1997).

**La idea original.** Un componente declara **precondiciones** —lo que exige de quien lo
llama—, **postcondiciones** —lo que garantiza a cambio— e **invariantes** —lo que siempre
es cierto—. El contrato es *entre dos piezas de software*, y su valor es que reparte la
culpa sin ambigüedad: si falla una precondición, el error es de quien llamó.

**Qué se le cambió acá.** Las partes del contrato. En estos documentos el contrato es
entre **el sistema y una persona**, así que:

| Design by Contract | Acá |
| --- | --- |
| Precondición | El **estado del que parte** el caso (`[SetUp]`) |
| Postcondición | El **desenlace observable** que se afirma |
| Invariante | Lo que **toda** superficie del proyecto cumple (el vocabulario de estados) |
| Quién verifica | El compilador o el runtime → **la prueba E2E, desde afuera** |

**Y una diferencia que no es cosmética:** el contrato de Meyer se verifica *hacia adentro*
—se puede inspeccionar el estado del objeto—; una promesa de superficie **solo se puede
verificar desde afuera**, mirando lo que la persona vería. De ahí sale el criterio de
[§3.1 del caso Hola Mundo](Caso-HolaMundo-Page.md): no inspeccionar el campo privado.

**El parentesco más cercano** es la *Promise Theory* de Mark Burgess, donde los agentes
son autónomos y **prometen** en vez de recibir órdenes. Que la palabra elegida haya sido
«promesa» y no «contrato» apunta hacia ahí: una superficie no obliga a nadie, se
compromete.

### 3.2 Las promesas se clasifican, y la clasificación clásica no alcanza

**Fuente:** Leslie Lamport, «Proving the Correctness of Multiprocess Programs» (1977),
donde aparece la distinción; formalizada por Bowen Alpern y Fred Schneider en «Defining
Liveness» (1985).

**La idea original.** Toda propiedad de un programa se descompone en dos:

| Clase | Dice | Se viola |
| --- | --- | --- |
| **Safety** | «Nada malo ocurre» | En un **momento** finito, que se puede señalar |
| **Liveness** | «Algo bueno termina ocurriendo» | Solo al final, mirando la ejecución completa |

**Aplicado a nuestras dos promesas:**

| Promesa | Clase |
| --- | --- |
| «Escribo una frase y aparece» | *Liveness* — algo bueno termina ocurriendo |
| «Con la credencial correcta se pasa» | *Liveness* |
| «Sin la credencial no se pasa» | *Safety* — nada malo ocurre |
| **«…y lo que se dice no le enseña nada a quien prueba suerte»** | **Ninguna de las dos** ← §3.3 |

Esa última fila es la que llevó al hallazgo.

### 3.3 El hallazgo: la «promesa negativa» es una hiperpropiedad

**Fuentes:** Joseph Goguen y José Meseguer, «Security Policies and Security Models», *IEEE
Symposium on Security and Privacy* (1982), pp. 11–20 — donde se define la
**no-interferencia**. Y Michael Clarkson y Fred Schneider, «Hyperproperties», *Computer
Security Foundations Symposium* (2008), luego en *Journal of Computer Security* 18 (2010),
pp. 1157–1210.

**La idea original.** Una *propiedad* es **un conjunto de trazas** de ejecución: para
saber si se cumple, alcanza con mirar **una** ejecución y decidir si pertenece al
conjunto. Una **hiperpropiedad** es un conjunto de propiedades — y para decidirla hace
falta mirar **un conjunto de ejecuciones a la vez**.

Clarkson y Schneider lo dicen con todas las letras: *la no-interferencia no es una
propiedad de trazas sino de conjuntos de trazas, y por eso es inexpresable como safety o
como liveness*. Y le ponen nombre a su forma más simple: **2-safety** — la que se decide
observando **dos** ejecuciones.

**Lo que escribimos en [§2.4 del caso de acceso](Caso-Login-Page.md), sin saber que
tenía nombre:**

> *«La promesa no vive en un estado: vive en que dos estados sean indistinguibles entre
> sí.»*

**Es la definición de 2-safety, dicha en castellano llano.** Y el caso de prueba que
escribimos ejecuta exactamente dos veces el ingreso y compara los desenlaces:

```csharp
await IngresarAsync(identificador: "nadie");
var conIdentificadorInexistente = await Page.GetByTestId("mensaje-resultado").TextContentAsync();

await Page.GotoAsync("/login");
await IngresarAsync(secreto: "lo-que-no-es");
var conSecretoIncorrecto = await Page.GetByTestId("mensaje-resultado").TextContentAsync();

Assert.That(conSecretoIncorrecto, Is.EqualTo(conIdentificadorInexistente));
```

**Dos trazas, comparadas entre sí. Eso es una prueba de 2-safety escrita a mano.**

#### Qué gana el documento al saberlo

| | |
| --- | --- |
| **Deja de ser una astucia** | Comparar dos desenlaces no es un truco: es el **único** método posible para esa clase de propiedad |
| **Aparece el límite** | Hay hiperpropiedades que **no** son 2-safety y necesitan más de dos trazas. Nuestra suite no las cubriría |
| **Se explica el modo de falla** | Una violación de no-interferencia **no rompe nada**: el sistema funciona y además cuenta algo. Por eso ninguna prueba funcional la detecta |
| **Hay adónde ir** | Existe literatura y herramientas de verificación de hiperpropiedades. Nuestro caso es la versión artesanal |

**Y una consecuencia práctica inmediata:** cada vez que alguien escriba una promesa de la
forma *«y no se puede llegar a saber X»*, ya sabe tres cosas — que no la va a poder
verificar mirando, que va a necesitar al menos dos ejecuciones, y que si no escribe ese
caso **nada más la va a vigilar**.

---

## 4. Tradición II — Diseño de interacción centrado en el uso

### 4.1 «Superficie» tiene un antecedente directo: el contexto de interacción

**Fuente:** Larry Constantine y Lucy Lockwood, *Software for Use: A Practical Guide to
the Models and Methods of Usage-Centered Design* (Addison-Wesley, 1999).

**La idea original.** El *usage-centered design* modela tres cosas: **roles de usuario**,
**casos de uso esenciales** —abstractos, sin detalle de interfaz— y **contextos de
interacción** (*interaction contexts*): las unidades dentro de las cuales la persona
interactúa con el sistema. El contexto de interacción **no es la ventana ni el
componente**: es el recorte funcional donde una intención se satisface.

**Qué se le cambió acá.** Le agregamos un **criterio de corte operativo** y un requisito
de verificabilidad:

> El conjunto más chico de marcado que tiene **una promesa propia, verificable de punta a
> punta**.

Constantine y Lockwood recortan por *intención*; nosotros recortamos por *promesa
comprobable*, que es más estrecho. Por eso podemos decir que la barra lateral **no** es
una superficie —no hay nada que afirmar de ella de punta a punta— mientras que un modal
de confirmación **sí** lo es.

**Nota de vocabulario.** «Superficie» también existe en diseño de producto (*product
surface*) y en seguridad (*attack surface*), pero con otro sentido —la extensión de lo
expuesto—. El parentesco real es con el contexto de interacción.

### 4.2 Los estados de una superficie vienen del UI Stack

**Fuentes:** Scott Hurff, «Why your user interface is awkward — you're ignoring the UI
Stack» y *Designing Products People Love* (O'Reilly, 2016). A su vez construye sobre el
*Three State Solution* de 37signals en *Getting Real* (2006).

**La idea original.** Toda pantalla tiene cinco estados, no uno:

| 37signals (2006) | Hurff (UI Stack) |
| --- | --- |
| Blank | **Blank** — vacío |
| — | **Loading** — cargando |
| — | **Partial** — parcial |
| Error | **Error** |
| Ideal | **Ideal** |

Y la advertencia central de Hurff: *estos estados no existen en el vacío; el trabajo del
diseñador es contemplarlos todos y decidir cómo la pantalla se mueve entre ellos*.

**Qué se le cambió acá.** Tres cosas, y las tres apuntan a la verificabilidad:

1. **Son un `enum` compartido, no una guía de estilo.** [`EstadoDeSuperficie.cs`](../../../Lab-E2E.WebBlazor.Base/src/WebBlazor.E2E.Base.HolaMundo/Theme/EstadoDeSuperficie.cs)
   tiene diez estados con nombre, y cada superficie **elige de esa lista** en vez de
   inventar los suyos.
2. **Son excluyentes por construcción.** El `@if / else if / else` de
   [`HolaMundo.razor` 87–110](../../../Lab-E2E.WebBlazor.Base/src/WebBlazor.E2E.Base.HolaMundo/Components/Paginas/HolaMundo.razor#L87-L110)
   es el marco que los ordena.
3. **La ausencia se declara.** Que `Indisponible` no aplique se escribe **en el marcado**,
   con su motivo.

**Y un refinamiento que no está en el UI Stack.** Hurff distingue *blank* de *error*, pero
el catálogo separa además `Vacio` de `FiltradoSinResultados`, con este criterio:

> *«En el primero hay datos y el filtro no encontró nada, y la acción es limpiar el
> filtro; en el segundo no hay datos, y la acción es crear el primero. Confundirlos le
> ofrece a la persona la acción equivocada.»*

**Dos estados son distintos cuando la salida que se le ofrece a la persona es distinta.**
Ese criterio —que aparece en el `<remarks>` del `enum` y no en ninguna guía— es lo que
impide que el catálogo crezca por estética.

**El parentesco formal**, para quien quiera ir más lejos: un conjunto finito de estados
excluyentes con transiciones declaradas es una **máquina de estados**, y su formalismo
visual estándar son los *statecharts* de David Harel (1987). El marco de una superficie es
una máquina de estados escrita en el lenguaje de la vista.

---

## 5. Tradición III — Especificación ejecutable y prueba

### 5.1 «La frase antes del caso» es especificación por ejemplo

**Fuentes:** Dan North, «Introducing BDD» (2006), de donde sale *Given–When–Then*; y
Gojko Adzic, *Specification by Example* (Manning, 2011). Emparentado con las **tres C** de
una historia —*Card, Conversation, Confirmation*— de Ron Jeffries.

**La idea original.** El criterio de aceptación se escribe **en el lenguaje del negocio y
desde el lado de quien usa**, y esa misma frase se vuelve ejecutable. La especificación
deja de ser un documento que envejece aparte del código.

**Qué se le cambió acá.** Le dimos un **segundo uso, diagnóstico**:

> *«Si no podés escribir la frase, el problema casi nunca es de la prueba. Es del
> diseño.»*

En BDD la frase es el punto de partida y se asume disponible. Acá **la dificultad para
escribirla es información**: las [cinco preguntas](Caso-HolaMundo-Page.md) y el catálogo
de superficies que no las pasan existen para convertir esa dificultad en un diagnóstico
—alcance, encuadre, altitud o diseño sin cerrar—.

### 5.2 Iniciar / Actuar / Verificar es Arrange–Act–Assert

**Fuente:** Bill Wake nombró el patrón **3A** en 2001; Kent Beck lo cita en
*Test-Driven Development: By Example* (2002).

**Qué se le cambió acá.** Casi nada en la forma, y una insistencia en el fondo: que
**«Arrange» es donde se rompen las pruebas**. En la literatura de 3A el arreglo es
preparación; en estos documentos es la **precondición del contrato** (§3.1), y declararla
mal es la causa de casi toda intermitencia. El testigo de hidratación (§5.4) es
exactamente eso: una precondición que estaba mal declarada.

### 5.3 Probar la promesa y no la implementación

**Fuente:** el principio rector de Testing Library, de Kent C. Dodds: *cuanto más se
parezcan tus pruebas a la forma en que tu software se usa, más confianza pueden darte*.
Emparentado con el *Page Object* descrito por Martin Fowler, que existe para que la
prueba hable del dominio y no del DOM.

**Qué se le cambió acá.** Le dimos un criterio de decisión operable —la **Pregunta 4**:
probá la frase contra un cambio hipotético inocente y mirá si la pondría en rojo— y una
regla derivada que en la literatura suele quedar implícita:

> **Nunca se fabrica el estado que la prueba debería obtener actuando.**

Es la regla que el archivo original de este laboratorio violaba al inyectar una cookie a
mano, y su costo no es que no funcione: es que **el circuito de ingreso queda sin probar**
aunque funcione.

### 5.4 El testigo de hidratación ya existía: es un IdlingResource

**Fuente:** los *Idling Resources* de Espresso, en Android
(`developer.android.com/training/testing/espresso/idling-resource`).

**La idea original.** Espresso sincroniza con la aplicación: solo actúa y afirma cuando la
app está **ociosa**. Pero solo conoce la cola de mensajes de la UI y sus tareas asíncronas
propias; **cualquier otro trabajo en segundo plano le es invisible**. Para eso existe el
`IdlingResource`: un objeto con el que **la aplicación le dice al test cuándo está
ocupada**, y el test espera esa señal.

**Es el mismo problema y la misma solución.** Playwright también sincroniza —sus cuatro
comprobaciones antes de cada clic— y también tiene un punto ciego: **no sabe si el
circuito de Blazor ya adoptó el marcado**. Nuestro `data-interactivo` es la aplicación
diciéndole al test que ya no está ocupada.

| Espresso | Acá |
| --- | --- |
| `IdlingResource` registrado en el framework | Un atributo en el DOM, leído con `Expect` |
| La app declara *ocupada / ociosa* | La superficie declara *sin circuito / con circuito* |
| El framework espera solo | La prueba espera con una aserción que reintenta |

**Qué se le cambió acá, y qué se perdió.** Ganamos que no hay que registrar nada en el
framework —el atributo viaja en el HTML— y que la señal es legible por cualquier
herramienta. Perdimos lo que Espresso hace bien: **la espera es explícita en cada prueba**
en vez de automática, así que si alguien olvida la línea, la prueba vuelve a ser
intermitente. Un `CountingIdlingResource` maneja además varias tareas concurrentes; el
nuestro es un solo bit.

**Y la lección de método:** que Espresso —un framework maduro, de otra plataforma— haya
necesitado exactamente esta pieza es la mejor evidencia de que el problema es estructural
de las interfaces asíncronas, y no una rareza de Blazor Server.

---

## 6. Lo que este laboratorio agrega

Con todo lo anterior descontado, queda esto:

| Aporte | Por qué no está en las fuentes |
| --- | --- |
| **La cadena completa** — promesa → superficie → estados → identificadores → caso | Cada eslabón es conocido; la articulación de punta a punta pertenece a las tres tradiciones a la vez, y por eso no vive en ninguna |
| **El criterio de corte de la superficie** — el conjunto más chico con promesa propia verificable | Constantine recorta por intención; el requisito de verificabilidad lo agregamos acá |
| **El criterio de distinción entre estados** — la salida que se le ofrece a la persona | El UI Stack enumera estados; no da la regla para decidir si dos son el mismo |
| **La ausencia declarada en el sitio** — el motivo escrito en el marcado o en la prueba, no en un documento aparte | Es afín a los ADR de Michael Nygard («Documenting Architecture Decisions», 2011), pero aplicado a línea de código y no a arquitectura |
| **La promesa de dos sujetos** — legítimo y adversario, escrita dos veces | El modelo de amenaza lo tiene; el diseño de interacción no lo trae a la definición de la pantalla |

**Y un aporte de método, que es el que más se transfiere:** que la dificultad para
enunciar la promesa **se lea como diagnóstico de diseño** y no como una molestia previa a
escribir la prueba.

---

## 7. Tabla de procedencia

Todo el mapa en una pantalla.

| Concepto | Fuente | Tradición | Qué se le cambió |
| --- | --- | --- | --- |
| **Promesa** | Meyer, *Design by Contract* | I | El contrato es con una persona, y se verifica desde afuera |
| **Precondición → estado de partida** | Meyer / Wake (3A) | I, III | Se lo trata como la causa principal de intermitencia |
| **Safety / liveness** | Lamport (1977); Alpern & Schneider (1985) | I | Se usa para clasificar promesas de interfaz |
| **Promesa negativa = hiperpropiedad (2-safety)** | Clarkson & Schneider (2008); Goguen & Meseguer (1982) | I | **Se llegó por la práctica; el nombre es de ellos** |
| **Superficie** | Constantine & Lockwood, *interaction contexts* (1999) | II | Se agrega el corte por promesa verificable |
| **Estados de superficie** | Hurff, *UI Stack*; 37signals, *Getting Real* (2006) | II | `enum` compartido, excluyente, con la ausencia declarada |
| **Marco de estados** | Harel, *statecharts* (1987) | I, II | Escrito en el lenguaje de la vista |
| **La frase antes del caso** | North, BDD (2006); Adzic, *Specification by Example* (2011) | III | Se usa además como diagnóstico de diseño |
| **Iniciar / Actuar / Verificar** | Wake, 3A (2001); Beck, *TDD by Example* (2002) | III | Sin cambios de forma |
| **Probar el uso, no la implementación** | Dodds (Testing Library); Fowler (*Page Object*) | III | Se agrega la Pregunta 4 como criterio operable |
| **Testigo de hidratación** | Espresso, `IdlingResource` | III | **Se llegó por la práctica; el patrón ya existía** |
| **Ausencia declarada** | Nygard, ADR (2011) | — | Aplicado a línea de código, no a arquitectura |

---

## 8. Bibliografía, con su grado de verificación

**Verificadas en la sesión del 2026-09-04**, contra fuentes en línea:

| Referencia | Qué se confirmó |
| --- | --- |
| Clarkson, M. & Schneider, F. «Hyperproperties». CSF 2008; *Journal of Computer Security* 18 (2010), 1157–1210 | Autoría, sede y año; que una propiedad es un conjunto de trazas y una hiperpropiedad un conjunto de propiedades; que la no-interferencia es inexpresable como safety o liveness y es un ejemplo de **2-safety** |
| Goguen, J. & Meseguer, J. «Security Policies and Security Models». *IEEE Symposium on Security and Privacy*, 1982, pp. 11–20 | Autoría, sede, año y páginas; que ahí se define la no-interferencia |
| Constantine, L. & Lockwood, L. *Software for Use*. Addison-Wesley, 1999 | Autoría y año; que *interaction contexts* es un término de la metodología, junto a roles de usuario y casos de uso esenciales |
| Hurff, S. *UI Stack* — *Designing Products People Love*, O'Reilly, 2016 | Los cinco estados (blank, loading, partial, error, ideal); que construye sobre el *Three State Solution* de 37signals en *Getting Real* (2006) |
| Espresso `IdlingResource` — documentación de Android | Que existe para que la app le declare al test cuándo está ocupada, porque Espresso no ve el trabajo en segundo plano |
| Wake, B. — patrón 3A, 2001 | Que lo nombró en 2001 y que Kent Beck lo cita en *TDD by Example* (2002) |

**No verificadas en esta sesión.** Se citan de memoria, con confianza alta por ser obras
estables y muy citadas, pero **sin haber contrastado la formulación exacta ni las páginas**:

- Meyer, B. *Object-Oriented Software Construction*. Prentice Hall, 1988; 2ª ed. 1997.
- Lamport, L. «Proving the Correctness of Multiprocess Programs». *IEEE TSE*, 1977.
- Alpern, B. & Schneider, F. «Defining Liveness». *Information Processing Letters*, 1985.
- Burgess, M. *Promise Theory*.
- Harel, D. «Statecharts: A Visual Formalism for Complex Systems». 1987.
- North, D. «Introducing BDD». 2006.
- Adzic, G. *Specification by Example*. Manning, 2011.
- Beck, K. *Test-Driven Development: By Example*. Addison-Wesley, 2002.
- Jeffries, R. — las tres C de una historia.
- Jacobson, I. — casos de uso; Cockburn, A. *Writing Effective Use Cases* (2000) — flujos alternos.
- Fowler, M. «PageObject».
- Dodds, K. C. — principio rector de Testing Library.
- Nygard, M. «Documenting Architecture Decisions». 2011.

**Antes de citar cualquiera de esas en un trabajo formal, verificalas.** La distinción se
mantiene acá a propósito: un documento que presenta todas sus referencias con la misma
seguridad obliga a desconfiar de todas por igual.

---

## 9. Lo que este documento no cubre

| No cubre | Por qué |
| --- | --- |
| **Verificación formal aplicada** | Model checking, lógicas de hiperpropiedades (HyperLTL) y herramientas asociadas. Se nombra la frontera; cruzarla es otro oficio |
| **La pirámide de pruebas y el reparto unidad/integración/E2E** | Es una discusión de estrategia, no de diseño de un caso |
| **Accesibilidad** | Tiene su propio cuerpo normativo (WCAG) y sus propias herramientas |
| **La postura de seguridad completa** | Modelo de amenaza, hash de secretos, control de intentos. Acá solo entra lo que la superficie promete y se puede observar |
| **Si existe un campo que ya integre las tres** | **No encontré uno**, y eso no es lo mismo que decir que no exista. Puede vivir bajo un nombre que no conozco, en ingeniería de requisitos o en HCI |

---

## 10. El criterio, en una línea

> **La superficie es donde la promesa deja de ser una intención y se vuelve observable —y
> por eso es el único lugar donde el diseño y la prueba hablan del mismo objeto.**
