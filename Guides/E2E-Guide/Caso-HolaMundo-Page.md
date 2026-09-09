# Caso de prueba: la superficie Hola Mundo

> **De qué va** — Cómo se decide **qué** probar, en la superficie más simple que existe.
> **Para quién** — Quien tiene que decidir qué probar y no cómo escribirlo.
> **Qué deja** — Las definiciones de superficie y de estado, las cinco preguntas que validan la frase de una promesa, y por qué una superficie interactiva necesita un testigo de hidratación.

**Superficie:** `Components/Paginas/HolaMundo.razor`
**Prueba:** `tests/WebBlazor.E2E.Base.HolaMundo.E2ETests/HolaMundoE2ETests.cs`
**Qué tipo de superficie es:** interactiva (`@rendermode InteractiveServer`)

Este documento no explica *cómo se escribe* una prueba con Playwright —eso está en
[`Quick-Guide-Primer-Proyecto.md`](Quick-Guide-Primer-Proyecto.md)—, sino **cómo se decide qué probar** en una
superficie como esta, y por qué el caso quedó como quedó.

## Índice

- **[1. Definiciones](#1-definiciones)** — qué es una superficie, dónde está cada parte de
  la definición en el archivo real, cómo se relaciona con las historias, los casos de uso y
  las maquetas, y por qué sus estados no son superficies distintas
- **[2. Qué promete esta superficie](#2-qué-promete-esta-superficie)** — las cinco preguntas
  que se le hacen a una promesa, y doce superficies de ejemplo. Es la parte que **no depende
  de este proyecto**: sirve para cualquier pantalla.
- **[3. Los criterios de diseño del caso](#3-los-criterios-de-diseño-del-caso)**
- **[4. El criterio propio de una superficie interactiva](#4-el-criterio-propio-de-una-superficie-interactiva)** — el testigo de hidratación, y cuándo hace falta
- **[5. El caso, entero](#5-el-caso-entero)**
- **[6. Lo que este caso deliberadamente no prueba](#6-lo-que-este-caso-deliberadamente-no-prueba)**
- **[7. Cómo se corre](#7-cómo-se-corre)**
- **[8. El criterio, en una línea](#8-el-criterio-en-una-línea)**
- **[9. Y en la superficie de al lado](#9-y-en-la-superficie-de-al-lado)**

> **De dónde viene todo esto:** el vocabulario de este documento —superficie, promesa,
> estado, testigo— no se inventó acá. Su procedencia está en
> [Marco-La-Superficie-Verificable.md](Marco-La-Superficie-Verificable.md): qué concepto viene de qué tradición, qué se le cambió al traerlo, y en qué
> dos casos reinventamos algo que ya estaba formalizado —el testigo de hidratación es un
> `IdlingResource` de Espresso hecho a mano—.

---

## 1. Definiciones

Cuatro términos que se usan todo el tiempo más abajo. Conviene fijarlos primero.

### 1.1 Superficie

**La pantalla como unidad de diseño**: lo que la persona ve, lo que puede hacer y en
qué estados puede quedar. No es «el componente» ni «la página»: un componente es una
pieza de implementación, y una superficie es una promesa hecha a alguien.

#### Dónde está cada parte de esa definición

La definición es abstracta a propósito, pero **tiene una correspondencia física exacta**
en el archivo. Estas son las tres partes en
[`HolaMundo.razor`](../../../Lab-E2E.WebBlazor.Base/src/WebBlazor.E2E.Base.HolaMundo/Components/Paginas/HolaMundo.razor):

| La definición dice | En el archivo es | Líneas |
| --- | --- | --- |
| **lo que la persona ve** | El encabezado: el título y la bajada que enuncia de qué se trata | [19–24](../../../Lab-E2E.WebBlazor.Base/src/WebBlazor.E2E.Base.HolaMundo/Components/Paginas/HolaMundo.razor#L19-L24) |
| **lo que puede hacer** | El formulario: un campo, su requisito declarado antes del intento, y un botón | [38–81](../../../Lab-E2E.WebBlazor.Base/src/WebBlazor.E2E.Base.HolaMundo/Components/Paginas/HolaMundo.razor#L38-L81) |
| **en qué estados puede quedar** | El bloque de estados: *enviando*, *con datos*, *vacío* | [87–110](../../../Lab-E2E.WebBlazor.Base/src/WebBlazor.E2E.Base.HolaMundo/Components/Paginas/HolaMundo.razor#L87-L110) |
| | …y el cuarto, que va aparte porque interrumpe: *error de entrada* | [29–36](../../../Lab-E2E.WebBlazor.Base/src/WebBlazor.E2E.Base.HolaMundo/Components/Paginas/HolaMundo.razor#L29-L36) |

Fijate en el tercer renglón: **los estados no están dispersos, están juntos y son
excluyentes**. Ese `@if / else if / else` es la definición hecha código —«en qué estados
puede quedar»— y por eso se puede leer los tres de un vistazo.

Y fijate en el comentario de la línea [83–85](../../../Lab-E2E.WebBlazor.Base/src/WebBlazor.E2E.Base.HolaMundo/Components/Paginas/HolaMundo.razor#L83-L85):

> *«La superficie tiene tres estados de presentación, y cada uno es un bloque. El estado
> `Indisponible` no aplica: la frase no viaja a ningún servicio externo, así que no hay
> servicio que pueda no responder.»*

**Ahí se ve la superficie razonando sobre sí misma.** El vocabulario de estados es común
a todo el proyecto, y esta superficie declara cuál de ellos no le corresponde **y por
qué**. Sin esa línea, la ausencia de un estado de indisponibilidad se leería como
olvido — el mismo criterio de la §6, aplicado al marcado en vez de a la prueba.

#### Lo que la definición excluye, en este mismo archivo

| No es superficie | Qué es | Dónde se ve |
| --- | --- | --- |
| `Banda`, `EstadoVacio`, `Esqueleto`, `Icono` | **Componentes**: piezas reutilizables. Aparecen en muchas superficies y ninguno promete nada por sí solo | [33](../../../Lab-E2E.WebBlazor.Base/src/WebBlazor.E2E.Base.HolaMundo/Components/Paginas/HolaMundo.razor#L33), [90](../../../Lab-E2E.WebBlazor.Base/src/WebBlazor.E2E.Base.HolaMundo/Components/Paginas/HolaMundo.razor#L90), [107](../../../Lab-E2E.WebBlazor.Base/src/WebBlazor.E2E.Base.HolaMundo/Components/Paginas/HolaMundo.razor#L107) |
| `MainLayout`, `BarraLateral` | **Chrome**: el marco de navegación. Está presente, pero no es lo que la pantalla promete | fuera del archivo |
| `@page "/HolaMundo"` | **Una ruta**: dónde vive. Casi siempre hay una por superficie, pero es una coincidencia frecuente, no una regla | [1](../../../Lab-E2E.WebBlazor.Base/src/WebBlazor.E2E.Base.HolaMundo/Components/Paginas/HolaMundo.razor#L1) |

La última fila importa más de lo que parece, y es la que responde a «parto de una
pantalla, ¿es una página?»:

- Un **modal de confirmación** es una superficie —promete «confirmo y se borra»— y **no
  tiene ruta propia**.
- Una ruta con **pestañas** que muestran cosas sin relación entre sí son **varias
  superficies** en una sola dirección.
- Un **asistente de varios pasos** son varias superficies y un recorrido **si cada paso
  le entrega algo a la persona**; si es un solo acto partido en tramos —un *acto
  divisible*— es **una** superficie con estados. La señal: si al abandonar en el medio
  queda algo hecho, eran superficies distintas. Está tratado con un caso real en
  [`Caso-Encuesta-Page.md` §3](Caso-Encuesta-Page.md).

#### ¿Cómo sé dónde termina una superficie y empieza otra?

**Respuesta: es el conjunto más chico de marcado que tiene una promesa propia,
verificable de punta a punta.**

La prueba de corte: **partila en dos y mirá si alguna mitad sigue prometiendo algo.**

| | |
| --- | --- |
| ✅ | El formulario y el bloque de estados **son una sola superficie**: separados, ninguno promete nada —un campo sin desenlace, un desenlace sin causa— |
| ✅ | El modal de baja **es una superficie aparte** de la lista que lo abre: promete algo propio, «confirmo y desaparece» |
| ❌ | La barra lateral **no es** una superficie: no hay nada que se pueda afirmar de ella de punta a punta |

#### ¿Cómo se relaciona con las historias, los casos de uso y las maquetas?

**Respuesta: cada uno aporta una parte distinta, y ninguno se superpone con la superficie.**

Esta es la pregunta que más ordena, porque los cuatro artefactos hablan de «la pantalla»
y ninguno habla de lo mismo:

| Artefacto | Qué aporta | Qué **no** aporta |
| --- | --- | --- |
| **Historia de usuario** | El *para qué* y a quién le sirve | Los estados, y qué pasa cuando algo sale mal |
| **Caso de uso** | El *recorrido*: actor, precondición, flujo principal y **flujos alternos** | Dónde empieza y termina cada pantalla |
| **Maqueta / spec de diseño** | La *forma*: jerarquía visual, densidad, tono | Casi siempre, **todos los estados menos uno** |
| **Superficie** | El *corte donde la promesa se vuelve observable* | El valor de negocio: eso lo dice la historia |

Y las cardinalidades, que es donde se rompe la intuición de «una historia, una pantalla,
una prueba»:

| Relación | |
| --- | --- |
| Historia ↔ superficie | **muchos a muchos** — una historia cruza varias pantallas, y una pantalla sirve a varias historias |
| Caso de uso → superficie | **uno a muchos** — un recorrido atraviesa pantallas; por eso un caso de uso **no** es un caso de prueba E2E |
| Superficie → componente | **uno a muchos**, y al revés también |
| Superficie → ruta | **casi siempre uno a uno**, y por eso se confunden |

**Qué hacer con cada uno cuando llega el momento de probar:**

1. **De la historia** sale la frase de la §2. Es su mejor uso: la historia ya está escrita
   desde el lado de la persona, que es justo lo que la Pregunta 1 pide.
2. **De los flujos alternos del caso de uso** salen los casos que nadie escribe. «¿Qué
   pasa si el dato no cumple?» es un flujo alterno, y es exactamente el `ErrorDeEntrada`
   de la línea [29](../../../Lab-E2E.WebBlazor.Base/src/WebBlazor.E2E.Base.HolaMundo/Components/Paginas/HolaMundo.razor#L29).
3. **De la maqueta** sale una advertencia, no un caso: **la maqueta suele dibujar un solo
   estado**, el feliz. Si la lista de estados de la superficie sale de la maqueta, van a
   faltar el vacío, el de carga y el de error — que son los tres que más se rompen.

> **El resumen:** la historia dice *por qué*, el caso de uso dice *por dónde*, la maqueta
> dice *cómo se ve*, y la superficie es **el corte donde eso se puede observar y, por lo
> tanto, probar**. Una prueba E2E no verifica una historia: verifica la promesa de una
> superficie, y varias de esas juntas sostienen la historia.

### 1.2 Estado de una superficie

**Uno de los desenlaces excluyentes en los que la superficie puede quedar.** Los estados
**no son superficies distintas**: son representaciones distintas de la misma promesa, y
la superficie es el marco que las ordena.

#### ¿Un formulario con varios estados son varias superficies?

**Respuesta: no. El corte es la promesa, no la apariencia.**

Un formulario vacío, uno enviando, uno con error y uno con resultado se ven muy
distintos —a veces no comparten ni un píxel—, y aun así son **la misma superficie**,
porque la promesa no cambió: «escribo una frase y aparece» sigue siendo cierta en los
cuatro momentos. Lo que cambia es *dónde está* la persona dentro de esa promesa.

**La prueba de discriminación**, y es una sola pregunta:

> **¿Cambia lo que la persona puede esperar, o solo lo que ve?**

| Qué cambia | Qué es | Ejemplo |
| --- | --- | --- |
| Solo lo que ve | **Otro estado** | Aparece el esqueleto mientras se procesa |
| Lo que puede hacer, **al servicio de la misma promesa** | **Otro estado** | El botón se deshabilita mientras envía |
| Lo que puede **esperar** | **Otra superficie** | Un modal que promete «confirmo y se borra» |

La segunda fila es la que más confunde: que se deshabilite un control no abre una
superficie nueva. Sigue siendo el mismo trato, en otro momento.

#### El marco que las ordena

Esa intuición —**la superficie como marco estructurado donde se ordenan las
representaciones**— no es una metáfora: en este proyecto está hecha código, en dos
piezas.

**El vocabulario**, en [`EstadoDeSuperficie.cs`](../../../Lab-E2E.WebBlazor.Base/src/WebBlazor.E2E.Base.HolaMundo/Theme/EstadoDeSuperficie.cs): diez estados con nombre, comunes
a todas las superficies del proyecto. No los inventa cada pantalla; cada pantalla
**elige de esa lista**.

**El marco**, en [`HolaMundo.razor` 87–110](../../../Lab-E2E.WebBlazor.Base/src/WebBlazor.E2E.Base.HolaMundo/Components/Paginas/HolaMundo.razor#L87-L110): un `@if / else if / else` con
un bloque por estado. Excluyentes por construcción, y legibles los tres de un vistazo.

| Estado | Qué se muestra | Línea |
| --- | --- | --- |
| `Enviando` | Un esqueleto | [90](../../../Lab-E2E.WebBlazor.Base/src/WebBlazor.E2E.Base.HolaMundo/Components/Paginas/HolaMundo.razor#L90) |
| `ConDatos` | La tarjeta con la frase | [94–103](../../../Lab-E2E.WebBlazor.Base/src/WebBlazor.E2E.Base.HolaMundo/Components/Paginas/HolaMundo.razor#L94-L103) |
| `Vacio` | El estado vacío, con qué hacer para salir de él | [107–108](../../../Lab-E2E.WebBlazor.Base/src/WebBlazor.E2E.Base.HolaMundo/Components/Paginas/HolaMundo.razor#L107-L108) |
| `ErrorDeEntrada` | Una banda, **fuera del marco** porque interrumpe | [29–36](../../../Lab-E2E.WebBlazor.Base/src/WebBlazor.E2E.Base.HolaMundo/Components/Paginas/HolaMundo.razor#L29-L36) |

La última fila muestra el límite de la regla: un estado que **interrumpe** en vez de
ocupar el lugar del contenido va en su propio bloque, arriba. El marco ordena los
estados del contenido, no todos los estados del mundo.

#### Por qué los estados no son cosméticos

El `<remarks>` de [`EstadoDeSuperficie.cs` 9–12](../../../Lab-E2E.WebBlazor.Base/src/WebBlazor.E2E.Base.HolaMundo/Theme/EstadoDeSuperficie.cs#L9-L12) lo dice mejor que
cualquier explicación:

> *«`FiltradoSinResultados` es un estado DISTINTO de `Vacio`: en el primero hay datos y
> el filtro no encontró nada, y la acción es limpiar el filtro; en el segundo no hay
> datos, y la acción es crear el primero. Confundirlos le ofrece a la persona la acción
> equivocada.»*

**Ahí está el criterio entero.** Dos estados son distintos cuando **la salida que se le
ofrece a la persona es distinta**. Si la salida es la misma, la distinción es
decorativa y sobra. Por eso el catálogo tiene diez y no treinta.

#### Tres cosas que se confunden con un estado

| | Qué es | Ejemplo | Cómo se trata |
| --- | --- | --- | --- |
| **Estado** | En cuál de los desenlaces está **ahora** | `Enviando` | Un bloque en el marco |
| **Situación** | Una condición del contexto, no del desenlace | Sin permisos; pantalla de 320px | Fuera del marco: guard, o CSS |
| **Variante** | La misma superficie con otro contenido | Alta vs. edición del mismo formulario | Un parámetro, no un estado |

Meter una situación en el `enum` de estados es el error más común, y se nota enseguida:
aparece un estado que **nunca es consecuencia de una acción de la persona**.

#### ¿Cada estado es un caso de prueba?

**Respuesta: no. Solo los que la persona puede provocar y que prometen algo.**

| Estado | ¿Caso propio? | Por qué |
| --- | --- | --- |
| `ConDatos` | **Sí** | Es la promesa central |
| `ErrorDeEntrada` | **Sí** | Es un flujo alterno con su propia promesa |
| `Vacio` | No aparte | El `[SetUp]` ya pasa por él; verificarlo suma un caso que falla junto con el otro |
| `Enviando` | No | Es un tránsito. Afirmarlo obliga a atrapar un instante, y ahí nacen las pruebas intermitentes |
| `Indisponible` | **No aplica** | La frase no viaja a ningún servicio: no hay servicio que pueda no responder |

Las últimas tres filas son las tres clases de ausencia de la §6 —*no aparte*, *no* y *no
aplica*— y conviene no confundirlas: la primera es una decisión de economía, la segunda
de método, la tercera de diseño.

### 1.3 Circuito

**La conexión WebSocket entre el navegador y el servidor** que hace que una
superficie Blazor Server reaccione. Los manejadores —`@onclick`, `@bind-Value`— no
viven en el navegador: viven en el servidor, del otro lado del circuito.

### 1.4 Identificador de prueba

**Un `data-testid` declarado en el marcado, junto al control que nombra.** Es un
nombre estable y explícito, puesto ahí *para* que la prueba lo use. La alternativa
—buscar por clase CSS o por posición— ata la prueba a decisiones de presentación que
cambian sin aviso.

```razor
<InputText id="campo-frase" data-testid="campo-frase" class="mq-input"
           @bind-Value="_modelo.Frase" />
```

---

## 2. Qué promete esta superficie

Antes de escribir una prueba hay que poder decir en una frase qué promete la pantalla.
Si no se puede, no está lista para probarse.

> **Escribo una frase, la muestro, y la frase aparece.**

Eso es todo. La superficie no consulta ningún servicio, no persiste nada y no navega
a ningún lado. Es deliberadamente pobre: existe para que el andamiaje de la prueba se
vea sin ruido alrededor.

Es además una promesa **positiva**: dice qué pasa. Las hay también **negativas** —dicen
qué no se puede llegar a saber—, se prueban de otra manera y son las que más veces
quedan sin caso; la del acceso tiene una, y está tratada en
[§2.1 y §2.4 del caso de acceso](Caso-Login-Page.md#21-por-qué-esta-frase-es-más-larga-que-la-del-hola-mundo).

### 2.1 Por qué la frase va primero

Porque **la prueba no inventa qué verificar: lo copia de la promesa**. Un caso E2E es
la frase escrita en código. Si la frase no existe, lo que se escribe no es una prueba
sino una descripción de lo que el código ya hace —y una descripción nunca encuentra un
error, porque cambia junto con lo que describe—.

Y hay un efecto lateral que es el más valioso de todo esto:

> **Si no podés escribir la frase, el problema casi nunca es de la prueba. Es del
> diseño.** La superficie está haciendo demasiadas cosas, o todavía no se decidió qué
> hace. La prueba es el primer lugar donde eso se nota.

### 2.2 Cinco preguntas para saber si la frase sirve

No hay que responderlas por escrito cada vez. Al principio se responden a mano; después
se responden solas.

---

#### Pregunta 1 — ¿Quién es el sujeto de la frase?

**Respuesta: la persona. Nunca el sistema.**

| | |
| --- | --- |
| ✅ | «**Escribo** una frase y aparece» |
| ❌ | «El componente **enlaza** el input al modelo y **renderiza** el mensaje» |

La segunda no está mal escrita: está escrita desde adentro. Y una promesa hecha desde
adentro solo se puede verificar desde adentro —mirando el modelo, contando renders—,
que es exactamente lo que una prueba E2E no hace.

**Regla práctica:** si la frase menciona una clase, un método o un evento del framework,
está escrita desde el lado equivocado.

**El matiz: a veces hay más de un sujeto.** En una superficie con postura de seguridad,
la promesa se escribe **dos veces** —una desde el usuario legítimo y otra desde quien no
lo es—, y la segunda es la que se olvida. La de la superficie de acceso lo muestra: «con
la credencial correcta se pasa» es la mitad del usuario; «lo que se dice no le enseña
nada a quien está probando suerte» es la mitad del adversario. Está tratado en
[§2.3 del caso de acceso](Caso-Login-Page.md#23-quién-es-el-sujeto-de-una-promesa-de-acceso).

---

#### Pregunta 2 — ¿Se puede verificar mirando la pantalla?

**Respuesta: si hace falta un depurador, la frase no sirve.**

| | |
| --- | --- |
| ✅ | «La frase aparece» — se ve |
| ❌ | «La frase queda guardada en el modelo» — no se ve |
| ❌ | «El estado pasa a `ConDatos`» — no se ve |

`ConDatos` es un nombre interno. Lo que la persona percibe es que *apareció una tarjeta
con la frase adentro*. Que eso se implemente con un `enum` de tres valores es una
decisión reversible, y una prueba no debería atarse a decisiones reversibles.

---

#### Pregunta 3 — ¿Cuántos «y» tiene la frase?

**Respuesta: cada «y» que une dos cosas independientes es otra promesa, y otro caso.**

> ❌ «Escribo una frase **y** la muestro **y** queda en el historial **y** puedo
> exportarla»

Eso no es una promesa: es un inventario. Un caso que verifique las cuatro cosas falla
por cuatro motivos distintos, y el reporte no dice cuál —el problema que la §4.6 del
[caso de acceso](Caso-Login-Page.md) trata aparte—.

**Cuidado con el falso positivo:** una superficie **puede** tener varias promesas, una
por cada acción que ofrece. Eso está bien y es lo normal. Lo que no puede tener es
**ninguna**, ni una tan ancha que abarque todo lo que la pantalla hace.

El «y» que sí está bien es el que describe **un solo recorrido**: «escribo una frase
**y** aparece» es una sola promesa, porque la segunda mitad es la consecuencia de la
primera, no otra cosa.

---

#### Pregunta 4 — ¿Sobreviviría a un cambio de implementación?

**Respuesta: tiene que sobrevivir. Si no, está describiendo el cómo.**

Probá la frase contra un cambio hipotético:

| Cambio | «Escribo una frase y aparece» |
| --- | --- |
| La frase pasa a guardarse en una base de datos | **sigue siendo cierta** |
| El botón cambia de color, de texto o de lugar | **sigue siendo cierta** |
| La superficie migra a `InteractiveWebAssembly` | **sigue siendo cierta** |
| El mensaje deja de aparecer | **se vuelve falsa** ← lo que la prueba debe detectar |

Solo la última fila debería poner el caso en rojo. Si algún cambio inocente lo pone en
rojo, la frase está afirmando de más.

---

#### Pregunta 5 — ¿Qué tendría que pasar para que la frase sea falsa?

**Respuesta: si no lo podés contestar en una línea, no es una promesa. Es un eslogan.**

| | |
| --- | --- |
| ✅ | «La frase aparece» → *es falsa si no aparece*. Verificable. |
| ❌ | «La superficie es intuitiva» → ¿falsa cuándo? |
| ❌ | «Muestra la información del cliente» → ¿cuál información? ¿comparada contra qué? |

La segunda no es verificable **por naturaleza**: se evalúa con personas, no con
Playwright. La tercera sí es verificable, pero **todavía no**: le falta decidir cosas.
Son dos fracasos distintos y se resuelven distinto —una se acepta como no automatizable,
la otra se termina de diseñar—.

---

### 2.3 Superficies que pasan las cinco preguntas

Ejemplos breves, con su frase al lado. Ninguno es de este laboratorio salvo los dos
primeros: la idea es que se vea que el criterio no depende de este proyecto.

| Superficie | Su frase | Por qué funciona |
| --- | --- | --- |
| **Hola Mundo** *(la de acá)* | «Escribo una frase y aparece» | Una acción, un desenlace visible |
| **Acceso** *(la de al lado)* | «Con la credencial correcta se pasa; sin ella no, y lo que se dice no le enseña nada a quien prueba suerte» | Dos promesas, y **la segunda es una promesa negativa**: se prueba comparando dos rechazos entre sí |
| **Buscador de socios** | «Escribo un apellido y veo solo los socios que coinciden» | El «solo» es lo que la hace verificable: acota el desenlace en vez de describirlo |
| **Alta de un socio** | «Cargo los datos obligatorios y el socio queda dado de alta» | Se verifica buscándolo después: el efecto se observa desde afuera |
| **Confirmación de baja** | «Pido dar de baja, confirmo, y el socio deja de aparecer en la lista» | Un recorrido de tres pasos, pero **un solo desenlace** |
| **Detalle de una factura** | «Abro una factura y veo su número, su fecha y su total» | Es una superficie de solo lectura, y su promesa también: no hay acción, hay presencia |

Fijate que ninguna dice *cómo*. «El socio queda dado de alta» no dice si es un `INSERT`,
una cola de mensajes o un archivo.

---

### 2.4 Superficies que no la pasan — y qué hacer con cada una

Este es el cuadro más útil, porque casi todo lo que uno se encuentra cae acá.

#### a. El tablero de inicio

> «Muestra el resumen del día»

**Qué falla:** la Pregunta 3. No hay una frase: hay ocho, una por cada panel —los
turnos de hoy, la recaudación, las alertas, el gráfico—.

**Qué hacer:** no se prueba «el tablero». Se prueba **un panel por caso**, cada uno con
su frase: «con tres turnos cargados para hoy, el panel de turnos dice 3». El tablero
como conjunto queda para una verificación visual, que es otra herramienta.

---

#### b. La pantalla de configuración

> «Guardo los cambios y quedan guardados»

**Qué falla:** la Pregunta 5, de forma sutil. La frase *parece* verificable, pero es una
promesa **sobre el mecanismo de guardado**, no sobre ningún efecto. Que treinta opciones
«queden guardadas» no dice qué cambia en ninguna parte.

**Qué hacer:** buscar el efecto de cada opción. «Apago las notificaciones por correo y
al dar de alta un socio no sale ningún correo» es una frase verificable; «la opción
quedó guardada» no lo es. Y quedará claro que no hay treinta casos que valga la pena
escribir, sino dos o tres.

---

#### c. El asistente de varios pasos

> «Completo el alta en cuatro pasos»

**Qué falla:** la Pregunta 3, pero de una forma que hay que mirar de cerca, porque **la
respuesta depende de algo que la frase no dice**.

**Primero decidí qué tenés delante:**

| | Qué es | Cuántas superficies |
| --- | --- | --- |
| Cada paso **le entrega algo** a la persona antes del siguiente | Un **recorrido** | Varias, más el recorrido |
| Los pasos son tramos de **un solo acto** | Un **acto divisible** | **Una**, con estados |

**La señal más confiable:** si al abandonar en el medio **queda algo hecho**, eran
superficies distintas. Si no queda nada, era una sola.

**Qué hacer.** Si es un recorrido: cada paso tiene su promesa —«sin el documento no me
deja avanzar»— y el recorrido completo tiene la suya, y van por separado, porque un solo
caso largo que haga las dos cosas es el que después nadie sabe por qué falló. Si es un
acto divisible: **una** superficie, y los pasos son estados suyos —§1.2—.

Hay un caso real tratado entero, con un asistente de tres pasos que resulta ser **una
sola superficie**, en
[`Caso-Encuesta-Page.md`](Caso-Encuesta-Page.md).

---

#### d. La pantalla que depende de datos vivos

> «Muestra las cotizaciones del día»

**Qué falla:** la Pregunta 5. Es falsa… ¿cuándo? No hay contra qué comparar: el
desenlace correcto cambia cada minuto.

**Qué hacer:** separar lo que es de la superficie de lo que es del dato. La superficie
promete «pido las cotizaciones y las veo, o me entero de que no se pudo». Eso sí se
prueba —incluido el estado de error, que suele ser el que nunca se prueba—. La
exactitud del número es otra cosa y no se verifica desde el navegador.

---

#### e. La pantalla de administración que hace de todo

> «Administra los socios»

**Qué falla:** las Preguntas 3 y 5 a la vez. «Administrar» es un verbo paraguas: adentro
hay listar, filtrar, dar de alta, editar, dar de baja y exportar.

**Qué hacer:** una frase por acción, y **aceptar que son seis grupos de casos**. Esto
suele destapar además un problema de diseño real: una pantalla que hace seis cosas
distintas casi siempre debería ser más de una pantalla.

---

#### f. La pantalla que todavía no se decidió

> «Muestra la información relevante del cliente»

**Qué falla:** la Pregunta 5. Y es el caso más importante de los seis, porque **acá la
prueba no es la que tiene el problema**.

**Qué hacer:** no escribir la prueba. Ir a preguntar qué información, en qué orden, y
qué se muestra cuando no hay ninguna. Una frase vaga es el síntoma de un diseño sin
cerrar, y escribir igual el caso solo consigue **fijar en código una decisión que nadie
tomó**.

---

### 2.5 El resumen

| Si la frase… | El problema es | Se resuelve |
| --- | --- | --- |
| habla del sistema y no de la persona | de **encuadre** | reescribiéndola desde afuera |
| necesita un depurador para verificarse | de **encuadre** | buscando el efecto visible |
| tiene varios «y» independientes | de **alcance** | partiéndola en varios casos |
| se rompe con un cambio inocente | de **altitud** | afirmando menos |
| no se puede contradecir | de **diseño** | terminando de diseñar, no de probar |

Y el criterio que los engloba a los cinco:

> **Una promesa se escribe desde el lado de quien la recibe, y tiene que poder ser
> falsa.**

---

## 3. Los criterios de diseño del caso

Ya está la frase. Ahora hay cuatro decisiones que tomar, y cada una se toma
respondiendo una pregunta.

---

### 3.1 ¿Qué se mira para saber si la superficie cumplió?

**Respuesta: lo que la persona vería. Nada de lo que hay detrás.**

La prueba escribe, acciona y verifica desde afuera. No inspecciona el campo privado
`_mensaje`, no cuenta renders, no mide el circuito.

| | |
| --- | --- |
| ✅ | `Expect(Page.GetByTestId("campo-mensaje")).ToHaveTextAsync(frase)` |
| ❌ | Leer el modelo, contar invocaciones a `StateHasChanged`, mirar la cookie |

**Por qué:** lo de la derecha ata la prueba a la implementación, y entonces cambiar la
implementación —sin romper nada— pone la prueba en rojo. Si mañana la frase se guardara
en una base de datos, la prueba no debería enterarse: la promesa no cambió.

**Cómo se comprueba:** tapate el código del `src` y preguntate si el caso sigue
teniendo sentido. Si para entenderlo hace falta abrir el componente, está mirando
adentro.

---

### 3.2 ¿Desde dónde parte el caso?

**Respuesta: de un estado conocido, y declararlo es parte del caso —no un trámite—.**

| Parte | Dónde va | Qué hace |
| --- | --- | --- |
| **Iniciar** | `[SetUp]` | Deja la pantalla en un **estado conocido** |
| **Actuar** | `[Test]` | Hace la acción que la superficie ofrece |
| **Verificar** | `[Test]` | Afirma el desenlace observable |

**Por qué importa tanto la primera:** casi todas las pruebas intermitentes son pruebas
cuyo punto de partida estaba mal declarado. La de esta superficie lo fue —§4—: el
`[SetUp]` decía «la pantalla está abierta» cuando lo que hacía falta era «la pantalla
está **viva**».

| | |
| --- | --- |
| ✅ | «Abierta la pantalla y con el circuito ya establecido» |
| ⚠️ | «Abierta la pantalla» — cierto, pero insuficiente |
| ❌ | «Abierta la pantalla, y además ya escribí la frase» — eso ya es actuar |

La tercera es el error opuesto y también es común: cuando el `[SetUp]` empieza a hacer
la acción, el `[Test]` se queda sin nada que probar.

---

### 3.3 ¿A qué elementos les pongo `data-testid`?

**Respuesta: solo a los que la prueba toca. Ni uno más.**

Los tres de esta superficie —`campo-frase`, `boton-mostrar-frase`, `campo-mensaje`— son
exactamente los que el caso necesita nombrar.

| | |
| --- | --- |
| ✅ | El campo que se llena, el botón que se acciona, el elemento que se verifica |
| ❌ | Un `data-testid` en cada `div`, «por las dudas» |
| ❌ | Ninguno, y localizar por `.mq-input:first-child` |

**Por qué no todos:** un identificador es una promesa de estabilidad. Poner treinta es
comprometerse a mantener treinta nombres que nadie usa, y el día que alguien reordene
el marcado no va a saber cuáles importan.

**Por qué no ninguno:** localizar por clase o por posición ata la prueba a decisiones de
presentación, que cambian sin aviso y sin que nadie piense que rompió algo.

---

### 3.4 ¿Contra qué se compara?

**Respuesta: contra un elemento que contiene lo verificado y nada más.**

```razor
<p class="mq-kv__valor mq-mt-2" data-testid="campo-mensaje">@_mensaje</p>
```

| | |
| --- | --- |
| ✅ | `<p data-testid="campo-mensaje">@_mensaje</p>` |
| ❌ | `<p data-testid="campo-mensaje"><b>Frase:</b> @_mensaje <Icono /></p>` |

**Por qué:** con la segunda forma, `ToHaveTextAsync` obliga a comparar contra un texto
compuesto —`"Frase: Hola mundo!"`—, y la aserción empieza a depender de la maqueta. El
día que alguien cambie el rótulo, la prueba falla sin que la promesa se haya roto.

**La salida cuando no se puede:** si el elemento no puede ser atómico, se usa
`ToContainTextAsync` y se afirma menos. Es peor —deja pasar un texto de más— pero es
honesto. Lo que no se hace es escribir en la prueba el texto compuesto completo.

---

## 4. El criterio propio de una superficie interactiva

Este es el criterio que distingue a esta superficie de una estática, y es el único
verdaderamente difícil.

### 4.1 ¿Por qué una pantalla que se ve lista puede no estarlo?

**Respuesta: porque llega dos veces, y las dos veces se ve igual.**

Una superficie `InteractiveServer` no llega terminada:

| Momento | Qué hay | Qué se ve |
| --- | --- | --- |
| **1. La foto** | El HTML que armó el servidor, sin manejadores conectados | La pantalla completa |
| **2. La pantalla viva** | El circuito abierto; Blazor adoptó el marcado | La pantalla completa |

Se ven **idénticas**. Y entre una y otra pasan decenas o cientos de milisegundos.

Eso segundo es *hidratar*: el HTML llega deshidratado —con la forma correcta pero sin
nada corriendo adentro— y el circuito lo rehidrata.

### 4.2 ¿Por qué Playwright no lo detecta solo?

**Respuesta: porque sus cuatro comprobaciones se cumplen igual en la ventana muerta.**

Antes de cada clic verifica que el elemento **exista**, sea **visible**, esté
**habilitado** y esté **quieto**. Si algo falta, espera y reintenta.

**En la ventana entre los dos momentos, las cuatro condiciones se cumplen.** El botón
está ahí, se ve, no está `disabled`, no se mueve. Playwright hace clic, nadie lo
escucha, y **no reintenta**: desde su punto de vista el clic salió bien.

El fracaso aparece después, en la aserción, con un mensaje que habla de otra cosa:

```
Locator expected to have text 'Hola mundo! - que tal?' But was: '<element(s) not found>'
```

Una persona nunca lo nota, porque tarda medio segundo en mover el mouse. Una máquina
hace clic en cuanto puede.

> **Este no es un riesgo teórico.** El `CHANGELOG` del 2026-09-02 registró esta misma
> intermitencia con ese mismo mensaje: **1 de 8 corridas en rojo**, y la que fallaba
> era siempre la primera —la que paga el arranque frío y estira la ventana—.

### 4.3 ¿Cómo se le pregunta a la superficie si ya está viva?

**Respuesta: no se le pregunta. Se hace que ella lo declare.**

> **Testigo:** un elemento del marcado cuyo único trabajo es **afirmar en el DOM un
> hecho que la prueba no puede deducir mirando la pantalla**.

Su condición de validez es una sola:

> **Solo lo puede escribir código que ya corre del lado del circuito.**

Por eso su presencia no es una promesa, es una **prueba**. No dice «debería estar
hidratado». Dice «esto se ejecutó, y esto solo se ejecuta si hay circuito».

En el marcado:

```razor
<span class="mq-sr-only" data-testid="estado-app" data-interactivo="@_interactivo"></span>

@code {
    // Arranca en `false` y así viaja en el HTML del servidor: el testigo dice que no
    // hay circuito hasta que lo haya.
    private string _interactivo = "false";

    // `OnAfterRender` solo corre del lado del circuito: si esto se ejecutó, la
    // superficie ya responde.
    protected override void OnAfterRender(bool primeraVez)
    {
        if (!primeraVez || _interactivo == "true") { return; }

        _interactivo = "true";
        StateHasChanged();
    }
}
```

Dos detalles que no son de adorno:

- **Arranca en `"false"`**, y ese valor viaja en la foto del servidor. Si el testigo
  apareciera recién al hidratar, «todavía no existe» y «no existe porque me equivoqué
  de nombre» serían indistinguibles.
- **Está fuera de la vista** (`mq-sr-only`), porque es un dato para máquinas. Las
  aserciones de atributo no necesitan que el elemento sea visible.

Y en el `[SetUp]`, una línea:

```csharp
await Expect(Page.GetByTestId("estado-app"))
    .ToHaveAttributeAsync("data-interactivo", "true");
```

**`Expect` sí reintenta**, a diferencia del clic. La carrera se convierte en una
espera con una condición explícita, y si algo se rompe de verdad, el error nombra el
problema real.

### 4.4 ¿Y si igual hago clic antes de tiempo?

**Respuesta: no es que «no pasa nada». Pasa otra cosa.**

El botón es `type="submit"` dentro de un `<EditForm FormName="frase">`. Sin hidratar,
el clic **no es inerte**: dispara el envío HTML de toda la vida, la página se recarga
entera y el resultado difiere del esperado.

| | Qué se espera | Qué ocurre |
| --- | --- | --- |
| Con circuito | El `@onclick` corre en el servidor y actualiza la superficie | ✅ |
| Sin circuito | — | El navegador postea el `<form>` y recarga la página |

**Por qué eso empeora el diagnóstico:** un clic inerte deja la pantalla como estaba, y
eso al menos se parece a lo que pasó. Un clic que recarga la página deja la pantalla
en un estado *plausible pero distinto*, y ahí el error puede aparecer en cualquier lado.

### 4.5 ¿Cuándo hace falta un testigo, entonces?

**Respuesta: cuando la prueba necesita saber algo que la pantalla no muestra.**

| Situación | ¿Testigo? | Por qué |
| --- | --- | --- |
| La superficie abre circuito y la prueba la acciona | **Sí** | La ventana muerta existe |
| La superficie es SSR y su form viaja por POST | No | No hay ventana; el envío es una navegación |
| La superficie es interactiva pero la prueba solo *lee* | No | Leer no depende de los manejadores |
| La prueba espera un dato que llega de un servicio lento | Depende | Si hay un estado visible de carga, se espera eso; si no, testigo |

La tercera fila es la que más se confunde: **`InteractiveServer` no implica testigo por
sí solo**. Lo que lo implica es *actuar* sobre la superficie.

---

## 5. El caso, entero

```csharp
[Parallelizable(ParallelScope.Self)]
[TestFixture]
public class HolaMundoE2ETests : PageTest
{
    [SetUp]
    public async Task Setup()
    {
        await Page.GotoAsync("https://localhost:7071/HolaMundo");

        // La superficie llega pintada antes de que el circuito abra, y en esa ventana
        // el botón se ve y se puede clickear pero no responde. `Expect` reintenta:
        // la prueba queda detenida hasta que la superficie declara que ya es interactiva.
        await Expect(Page.GetByTestId("estado-app"))
            .ToHaveAttributeAsync("data-interactivo", "true");
    }

    [Test]
    [Description("Mostrar Mensaje de texto")]
    public async Task MostrarMensaje()
    {
        string frase = "Hola mundo! - que tal?";

        await Page.GetByTestId("campo-frase").FillAsync(frase);
        await Page.GetByTestId("boton-mostrar-frase").ClickAsync();
        await Expect(Page.GetByTestId("campo-mensaje")).ToHaveTextAsync(frase);
    }
}
```

---

## 6. Lo que este caso deliberadamente no prueba

### ¿Cómo sé si una ausencia es una decisión o un olvido?

**Respuesta: por si está escrita. Una ausencia sin explicar se lee como olvido, y con
razón.**

Y no todas las ausencias son iguales. Conviene distinguir tres, porque se resuelven
distinto:

| Tipo | Significa | Qué hacer |
| --- | --- | --- |
| **Pendiente** | Debería probarse y todavía no se hizo | Anotarlo, y que quede como deuda |
| **No aplica** | La situación no puede ocurrir en esta superficie | Explicar por qué no puede |
| **Otra herramienta** | Se verifica, pero no acá | Decir con qué se verifica |

Confundir «no aplica» con «pendiente» es lo que hace que una lista de deudas crezca con
cosas que nunca hubo que hacer. Y al revés: llamar «no aplica» a un pendiente es la
forma educada de barrerlo abajo de la alfombra.

| No se prueba | Por qué |
| --- | --- |
| El **error de entrada** (frase vacía o de más de 120 caracteres) | Es un caso legítimo y todavía no está escrito. Queda anotado como pendiente, no como decisión. |
| El **estado vacío** inicial | El `[SetUp]` ya pasa por él; verificarlo aparte agregaría un caso que falla junto con el otro. |
| El **estado `Indisponible`** | No aplica: la frase no viaja a ningún servicio externo, así que no hay servicio que pueda no responder. |
| La **accesibilidad** (región activa, rótulos, foco) | Es otra clase de verificación, con otras herramientas. No se mezcla acá. |

---

## 7. Cómo se corre

```bash
scripts/pruebas.sh holamundo      # una corrida
REPETIR=8 scripts/pruebas.sh holamundo   # ocho, para buscar intermitencias
```

El `REPETIR` no es un lujo. **Una prueba de concurrencia que pasó una vez no probó
nada**: fue así como la intermitencia de la hidratación quedó registrada, y fue así
como se comprobó que el testigo la cerraba —16 de 16 en verde, en
[`evidencia/2026-09-03-testigo-de-hidratacion/`](../../../Lab-E2E.WebBlazor.Base/evidencia/2026-09-03-testigo-de-hidratacion/)—.

---

## 8. El criterio, en una línea

> **Lo que la prueba necesita nombrar, se declara en el marcado.**

Vale para los controles —`campo-frase`, `campo-mensaje`— y vale igual para los
estados —`estado-app`—. Lo que la prueba tiene que adivinar, tarde o temprano lo
adivina mal.

---

## 9. Y en la superficie de al lado

La otra superficie de este laboratorio, la de acceso, **no lleva testigo**, y no es
un descuido: es SSR estático, sin circuito, y ahí el criterio cambia por completo.
Está en [`Caso-Login-Page.md`](Caso-Login-Page.md).
