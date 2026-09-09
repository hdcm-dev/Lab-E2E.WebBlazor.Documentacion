# Caso de prueba: la superficie de acceso

> **De qué va** — Cómo se decide qué probar cuando además del usuario hay un adversario.
> **Para quién** — Ídem, con postura de seguridad.
> **Qué deja** — La promesa negativa y por qué se verifica comparando dos observaciones en vez de mirar una, y por qué una superficie SSR no necesita testigo de hidratación.

**Superficie:** `Components/Paginas/Identidad/Ingreso.razor`
**Pruebas:** `tests/WebBlazor.E2E.Base.Login.E2ETests/LoginE2ETests.cs`
**Base común:** `tests/WebBlazor.E2E.Base.Login.E2ETests/PruebaDeSuperficie.cs`
**Qué tipo de superficie es:** SSR estático (**sin** `@rendermode`)

## Índice

- **[1. Definiciones](#1-definiciones)** — guard, credencial de sesión, rechazo indiferenciado
- **[2. Qué promete esta superficie](#2-qué-promete-esta-superficie)** — una promesa **negativa**:
  por qué tiene dos sujetos y por qué no se puede verificar mirando
- **[3. La diferencia que ordena todo el resto](#3-la-diferencia-que-ordena-todo-el-resto)** —
  SSR frente a interactiva
- **[4. Los criterios de diseño de estos casos](#4-los-criterios-de-diseño-de-estos-casos)**
- **[5. El mapa de los casos](#5-el-mapa-de-los-casos)**
- **[6. Un hallazgo que apareció al escribir estos casos](#6-un-hallazgo-que-apareció-al-escribir-estos-casos)**
- **[7. Lo que estos casos deliberadamente no prueban](#7-lo-que-estos-casos-deliberadamente-no-prueban)**
- **[8. Cómo se corren](#8-cómo-se-corren)**
- **[9. Los criterios, en una lista](#9-los-criterios-en-una-lista)**

> **De dónde viene todo esto:** el vocabulario de este documento —promesa, superficie,
> estado, promesa negativa— tiene procedencia, y está en
> [Marco-La-Superficie-Verificable.md](Marco-La-Superficie-Verificable.md). Ahí se dice qué concepto viene de qué tradición, qué se le cambió al
> traerlo, y en qué dos casos reinventamos algo que ya tenía nombre.

El caso hermano —la superficie interactiva— está en
[`Caso-HolaMundo-Page.md`](Caso-HolaMundo-Page.md). Conviene leer los dos juntos:
casi todo lo que cambia entre ellos se explica por una sola diferencia.

---

## 1. Definiciones

### 1.1 Guard

**Lo que decide si alguien pasa.** Acá está declarado en tres capas, y cada una corta
en un momento distinto:

| Capa | Dónde | Cuándo corta |
| --- | --- | --- |
| **Ruteo** | El middleware de autenticación, y el `<NotAuthorized>` de `Routes.razor` | Antes de resolver la superficie |
| **Superficie** | `OnInitializedAsync` de la página | Al abrirse el componente |
| **Acción** | El endpoint `POST /identidad/ingreso` | Al ejecutar la operación |

### 1.2 Credencial de sesión

**La cookie que el servidor emite y firma** al aceptar un ingreso. Acá se llama
`auth_token`, es `HttpOnly` y `SameSite=Strict`. Que esté **firmada** es lo que hace
imposible fabricarla desde afuera.

### 1.3 Rechazo indiferenciado

**Un solo desenlace para todas las formas de fallar.** «El identificador no existe» y
«el secreto no es» producen exactamente el mismo mensaje, porque distinguirlos le
confirma la existencia de una identidad a quien no debería saberlo.

### 1.4 Catálogo de resultados

**La tabla única de la que salen los mensajes que la persona lee.** Un código sin
entrada cae en el mensaje genérico, nunca en el código crudo ni en la traza.

---

## 2. Qué promete esta superficie

> **Con la credencial correcta se pasa; sin ella no, y lo que se dice al respecto no
> le enseña nada a quien está probando suerte.**

La segunda mitad de esa frase es lo interesante. Esta superficie no promete solo un
comportamiento: promete **un silencio**. Y un silencio también se prueba.

> Cómo se llega a una frase así —y cómo se sabe si la que escribiste sirve— está en
> [§2 del caso Hola Mundo](Caso-HolaMundo-Page.md#2-qué-promete-esta-superficie): las cinco preguntas y
> los ejemplos de superficies que no la pasan. Es criterio compartido y no se repite
> acá; lo que sigue es ese criterio **aplicado a esta promesa**, que tiene otra forma.

### 2.1 ¿Por qué esta frase es más larga que la del Hola Mundo?

**Respuesta: porque no tiene la misma forma. Tiene dos mitades, y la segunda es negativa.**

Puestas al lado se ve que la diferencia no es de longitud:

| | Hola Mundo | Acceso |
| --- | --- | --- |
| **Estructura** | acción → desenlace | condición → desenlace, **+ lo que no se puede deducir** |
| **Signo** | Positiva | Positiva **y negativa** |
| **Qué afirma** | Que algo **ocurre** | Que algo ocurre **y que algo no se filtra** |
| **Cómo se prueba** | Haciéndolo una vez | La primera mitad sí; **la segunda, comparando dos desenlaces** |

Una **promesa positiva** dice qué pasa. Una **promesa negativa** dice qué no se puede
llegar a saber. Las dos son legítimas y las dos se prueban, pero no de la misma manera —
y confundirlas es lo que produce suites que verifican mucho y no detectan una fuga.

### 2.2 ¿Las cinco preguntas dan lo mismo en las dos?

**Respuesta: sí. El método no cambia con el dominio.**

Las mismas cinco preguntas, aplicadas a las dos frases:

| | Hola Mundo | Acceso |
| --- | --- | --- |
| **1. ¿Quién es el sujeto?** | «Escribo», «muestro» — la persona | «se pasa», «se dice» — la persona… **y alguien más**, §2.3 |
| **2. ¿Se verifica mirando?** | Aparece la frase | Se ve la superficie protegida |
| **3. ¿Cuántos «y»?** | Uno encadenado: el desenlace de la acción | Uno **real**: son dos promesas, y por eso dos grupos de casos |
| **4. ¿Sobrevive al cambio?** | Si la frase se guardara en una base, sigue cierta | Si la sesión pasara a un token, sigue cierta |
| **5. ¿Puede ser falsa?** | Si la frase no aparece | Si se pasa sin credencial, **o si los dos rechazos difieren** |

La fila 5 muestra el trabajo extra: esta promesa tiene **dos formas de ser falsa**, y la
segunda no se parece en nada a un error.

### 2.3 ¿Quién es el sujeto de una promesa de acceso?

**Respuesta: dos personas. Y la segunda es la que casi siempre falta.**

La Pregunta 1 dice que el sujeto es la persona. Acá hay **dos**:

| Sujeto | Qué le promete la superficie |
| --- | --- |
| Quien tiene la credencial | «Se pasa» |
| **Quien está probando suerte** | «De acá no te llevás información» |

La segunda mitad de la frase está escrita **desde el lado de quien no debería entrar**, y
por eso se enuncia como un límite a lo que puede aprender, no como una funcionalidad.

> **La regla, para reusar:** en una superficie con postura de seguridad, la promesa se
> escribe **dos veces** —una desde el usuario legítimo y otra desde quien no lo es— y la
> segunda es la que se olvida. Una superficie de acceso cuya única promesa es «con la
> credencial correcta se pasa» está a mitad de camino, y su prueba también.

Dónde aparece esa segunda promesa, hecha código:

| Pieza | Cómo la sostiene |
| --- | --- |
| [`ServicioDeIdentidad.cs`](../../../Lab-E2E.WebBlazor.Base/src/WebBlazor.E2E.Base.Login/Servicios/ServicioDeIdentidad.cs) | Un solo desenlace de rechazo, para todas las formas de fallar |
| [`CatalogoDeResultados.cs`](../../../Lab-E2E.WebBlazor.Base/src/WebBlazor.E2E.Base.Login/Servicios/CatalogoDeResultados.cs) | Un código sin entrada cae en el mensaje genérico, **nunca en el código crudo ni en la traza** |
| [`IdentidadEndpoints.cs`](../../../Lab-E2E.WebBlazor.Base/src/WebBlazor.E2E.Base.Login/Endpoints/IdentidadEndpoints.cs) | Solo se admiten rutas locales: un destino externo sería una redirección abierta |

Las tres son la misma promesa, sostenida en tres lugares distintos.

### 2.4 ¿Por qué una promesa negativa no se puede mirar?

**Respuesta: porque no tiene estado. Es una promesa sobre la *relación* entre estados.**

Los estados de una superficie son bloques del marco que los ordena —[§1.2 del caso Hola
Mundo](Caso-HolaMundo-Page.md#12-estado-de-una-superficie)—, y cada uno se puede señalar con el dedo: acá
está el vacío, acá el de carga, acá el error.

**«No le enseña nada a quien está probando suerte» no tiene bloque.** No existe ningún
lugar del marcado que diga *«acá no filtré información»*. La promesa no vive en un
estado: vive en que **dos estados sean indistinguibles entre sí**.

| Clase de promesa | Dónde se cumple | Cómo se verifica |
| --- | --- | --- |
| Positiva | **En un** estado | Mirando ese estado |
| Negativa | **Entre dos** estados | Comparándolos |

De ahí sale —y no como una astucia, sino como consecuencia— que el caso
`ElRechazoNoDistingueQueCampoFallo` **no compare contra ningún texto literal** (§4.4).

**Y de ahí sale el modo de falla que hay que temer.** Una promesa positiva rota se nota:
algo no aparece. Una promesa negativa rota **no se nota nunca**, porque el sistema sigue
funcionando perfectamente —solo que además está contando algo—. Si no hay un caso que la
vigile, no hay nada más que la vigile.

> **Esto tiene nombre, y no lo inventamos acá.** Una propiedad que no se puede decidir
> mirando **una** ejecución sino un conjunto de ellas es una **hiperpropiedad** (Clarkson
> y Schneider, 2008); el caso concreto de «el observador no debe poder distinguir dos
> ejecuciones» es la **no-interferencia** (Goguen y Meseguer, 1982), y su forma más
> simple —la que se decide con **dos** trazas— se llama **2-safety**. El caso de §4.4
> ejecuta exactamente dos ingresos y los compara: es una prueba de 2-safety escrita a
> mano. La procedencia completa está en [Marco-La-Superficie-Verificable.md](Marco-La-Superficie-Verificable.md#33-el-hallazgo-la-promesa-negativa-es-una-hiperpropiedad).

---

## 3. La diferencia que ordena todo el resto

Esta superficie **no lleva `@rendermode`**. Es SSR estático, y su formulario viaja por
POST a un endpoint.

### 3.1 ¿Por qué no es interactiva? ¿Es una preferencia de estilo?

**Respuesta: no. Es que un ingreso interactivo, en Blazor Server, no puede funcionar.**

La credencial de sesión se emite **en el ciclo de request**. Con el circuito ya
establecido, la respuesta HTTP ya se envió, y entonces **no hay dónde escribir la
cabecera que crea la cookie**.

**La lección general:** cuando una superficie está construida de una forma que parece
anticuada, la primera pregunta no es «¿la modernizo?» sino «¿qué restricción la puso
así?». Acá la restricción es del protocolo, y ninguna cantidad de interactividad la
levanta.

### 3.2 ¿Qué consecuencia tiene para la prueba?

**No hay ventana de hidratación, así que no hay testigo que esperar.**

En la superficie interactiva, el problema central era que el botón se ve listo antes
de estarlo ([§4 del caso Hola Mundo](Caso-HolaMundo-Page.md)). Acá ese problema no
existe: el `<form method="post">` es HTML nativo, funciona con el primer byte que
llega, y el envío es **una navegación** —de las que las esperas de Playwright ya
cubren por sí solas—.

> Esta es la lección que hace útil comparar los dos documentos: **el andamiaje de una
> prueba no se elige por gusto, se deriva de cómo está construida la superficie.**

| | Hola Mundo | Acceso |
| --- | --- | --- |
| Render | `InteractiveServer` | SSR estático |
| Cómo actúa | `@onclick` sobre el circuito | POST del navegador |
| ¿Ventana de hidratación? | **Sí** | No |
| ¿Testigo en el `[SetUp]`? | **Sí** | No hace falta |
| Estado del que parte | *Con* sesión | *Sin* sesión |

---

## 4. Los criterios de diseño de estos casos

### 4.1 ¿Cómo compruebo que la sesión existe?

**Respuesta: por su efecto —poder ver lo protegido—, nunca leyendo la cookie.**

```csharp
// Así:
await Expect(Page).ToHaveURLAsync($"{UrlBase}/");
await Expect(Page.GetByRole(AriaRole.Heading, new() { Name = "Inicio" })).ToBeVisibleAsync();
```

Si mañana la sesión pasara a un token en otro lado, la promesa seguiría siendo la
misma y la prueba no debería enterarse.

De ahí sale también la regla inversa, y es la que más veces se rompe en la práctica:

> **Nunca se fabrica el estado que la prueba debería obtener actuando.**

El archivo del que salió esta clase intentaba justamente eso: inyectaba a mano una
cookie con un GUID. No podía funcionar —la sesión real la firma el servidor—, pero el
problema de fondo es anterior: **una prueba que fabrica su propio estado deja de
probar el camino por el que la persona pasa**. Aun si la cookie hubiese funcionado, el
circuito de ingreso habría quedado sin probar.

### 4.2 ¿Dónde va el «ingresar» que todos los casos necesitan?

**Respuesta: en la base, y solo porque no dice nada sobre ningún caso en particular.**

```csharp
protected async Task IngresarAsync(string? identificador = null, string? secreto = null)
{
    await Page.GetByTestId("campo-usuario").FillAsync(identificador ?? Identificador);
    await Page.GetByTestId("campo-clave").FillAsync(secreto ?? Secreto);
    await Page.GetByTestId("boton-ingresar").ClickAsync();
}
```

El método vive en la clase base porque **todas** las pruebas del proyecto lo
necesitan, incluida la de la superficie protegida, que lo usa solo para llegar a su
punto de partida.

Los parámetros son opcionales a propósito: quien llama sin argumentos dice «una
credencial válida, no me importa cuál»; quien pasa uno dice «esta credencial es
parte de lo que estoy probando». La firma del método distingue el trámite del caso.

### 4.3 ¿De qué estado parten estos casos?

**Respuesta: de *sin sesión*, que es con lo que arranca todo contexto nuevo.**

Por eso el `[SetUp]` casi no hace nada:

```csharp
// El estado conocido del que parten estos casos es *sin sesión*, que es con lo
// que arranca todo contexto nuevo de Playwright. El [SetUp] solo abre la pantalla.
[SetUp]
public Task Setup() => Page.GotoAsync("/login");
```

Playwright le da a cada caso **un contexto de navegador propio**, con cookies y
almacenamiento nuevos. El aislamiento no hay que construirlo: viene puesto. Lo que sí
hay que hacer es **no romperlo**, y es lo que se rompe cuando se comparte sesión entre
casos para que corran más rápido.

### 4.4 ¿Cómo se prueba que algo *no* se puede deducir?

**Respuesta: provocando dos desenlaces distintos y afirmando que son indistinguibles.**

El rechazo indiferenciado (§1.3) es una promesa de las difíciles: no dice qué debe
pasar, dice qué **no** debe poder deducirse. Mirando un solo desenlace no se ve nada.

| | |
| --- | --- |
| ❌ | «Con un usuario inexistente, el mensaje dice *No pudimos validar el ingreso*» |
| ✅ | «Con un usuario inexistente y con un secreto incorrecto, el mensaje es **el mismo**» |

La primera pasa aunque el sistema filtre información —basta con que uno de los dos
mensajes sea ese—. Solo la segunda puede detectar la fuga.

```csharp
[Test]
[Description("El rechazo no dice cuál de los dos campos falló")]
public async Task ElRechazoNoDistingueQueCampoFallo()
{
    await IngresarAsync(identificador: "nadie");
    var conIdentificadorInexistente = await Page.GetByTestId("mensaje-resultado").TextContentAsync();

    await Page.GotoAsync("/login");
    await IngresarAsync(secreto: "lo-que-no-es");
    var conSecretoIncorrecto = await Page.GetByTestId("mensaje-resultado").TextContentAsync();

    Assert.That(conSecretoIncorrecto, Is.EqualTo(conIdentificadorInexistente));
}
```

Notá que **no se compara contra un texto literal**. Se comparan los dos desenlaces
entre sí. Si mañana el mensaje cambia, este caso sigue siendo válido: lo que afirma no
es *qué* dice, sino que **dice lo mismo en los dos casos**.

Y no es una astucia de la prueba: es la única forma posible. La promesa **no vive en
ningún estado** —vive en que dos estados sean indistinguibles—, así que no hay nada que
mirar, solo algo que comparar. El porqué está en §2.4.

### 4.5 ¿Cuánto detalle se afirma?

**Respuesta: lo que tendría que fallar con razón. Lo reversible se deja suelto.**

```csharp
[Test]
[Description("Un destino externo no se honra: el ingreso no es una redirección abierta")]
public async Task UnDestinoExternoNoSeHonra()
{
    await Page.GotoAsync("/login?returnurl=https://ejemplo.invalido/");
    await IngresarAsync();

    // El caso se escribe desde la promesa —«de acá no se sale»— y no desde el
    // detalle de a qué ruta local se cae, que es una decisión reversible.
    await Expect(Page).ToHaveURLAsync(new Regex($"^{Regex.Escape(UrlBase)}/"));
}
```

La promesa es «un `returnurl` externo no convierte al ingreso en una redirección
abierta». Que el destino de repuesto sea `/` y no otra ruta local es una decisión que
alguien puede cambiar mañana con toda razón, y no debería poner una prueba en rojo.

**Regla práctica:** cuando dudes de cuánto afirmar, preguntate qué tendría que pasar
para que este caso falle *con razón*. Si la respuesta incluye un cambio inocente,
estás afirmando de más.

### 4.6 ¿Cuándo un caso es en realidad dos?

**Respuesta: cuando puede fallar por dos motivos y el reporte no dice cuál.**

Un caso que verifica el rebote del guard **y además** que después se llega al destino
falla por dos causas distintas. Se parten:

```csharp
[Test] public async Task LaSuperficieProtegidaExigeSesion() { ... }  // el rebote ocurre
[Test] public async Task ElDestinoSobreviveAlRebote()      { ... }  // el rebote sirvió
```

---

## 5. El mapa de los casos

Diez casos, y cada uno cubre un tramo distinto del circuito.

| # | Caso | Qué afirma |
| --- | --- | --- |
| 1 | `IngresoAceptadoAbreLaSuperficieDeTrabajo` | Con la credencial correcta, se pasa |
| 2 | `IngresoAceptadoVuelveAlDestinoPedido` | Se vuelve a donde se quería ir |
| 3 | `UnDestinoExternoNoSeHonra` | El ingreso no es una redirección abierta |
| 4 | `IngresoRechazadoVuelveAlAccesoConElMensajeDelCatalogo` | El rechazo se dice con el texto del catálogo |
| 5 | `ElRechazoNoDistingueQueCampoFallo` | El rechazo no enseña nada |
| 6 | `UnEnvioIncompletoNoSale` | Lo que falta no se intenta |
| 7 | `LaSuperficieProtegidaExigeSesion` | Sin sesión hay rebote, y se anota el destino |
| 8 | `ElDestinoSobreviveAlRebote` | El rebote sirvió para algo |
| 9 | `CerrarLaSesionRevocaElPaso` | La salida surte efecto |
| 10 | `MostrarMensaje` *(en `HolaMundoE2ETest`)* | La superficie protegida funciona una vez adentro |

### 5.1 ¿De dónde salieron estos diez y no otros?

**Respuesta: de las promesas, no de la cobertura de líneas.**

Cada caso sale de **una frase que la superficie promete**, y el conjunto se cierra
cuando ninguna promesa queda sin caso. Las promesas están en
el marcado y en los comentarios de diseño del `src`: `Ingreso.razor` dice que el
rechazo es indiferenciado, `IdentidadEndpoints.cs` dice que solo se admiten rutas
locales. **Cada una de esas afirmaciones es un caso esperando a ser escrito.**

---

## 6. Un hallazgo que apareció al escribir estos casos

Vale dejarlo anotado, porque ilustra para qué sirven estas pruebas.

El caso 7 se escribió primero afirmando `/login?estado=sesion-requerida`, que es lo
que produce el `<Redireccion>` del `<NotAuthorized>` en `Routes.razor`. **Falló.** Lo
que la aplicación produce de verdad es:

```
/login?returnurl=%2FHolaMundo
```

Es decir: la capa del guard que efectivamente actúa es **el middleware de
autenticación por cookies** —`options.LoginPath` con `ReturnUrlParameter`—, que corta
antes de que el `Router` llegue a evaluar su `<NotAuthorized>`.

Dos consecuencias, ninguna resuelta acá:

1. El `<NotAuthorized>` de `Routes.razor` es **camino muerto** para las páginas con
   `[Authorize]`.
2. La entrada `SesionRequerida` del catálogo —«Ingresá para ver esa superficie.»—
   **nunca se le muestra a nadie**.

Las pruebas se ajustaron a lo que la aplicación hace, no al revés: **corregir el
comportamiento es una decisión de diseño, y no la toma la prueba**. Queda anotado.

---

## 7. Lo que estos casos deliberadamente no prueban

### ¿Por qué una superficie de seguridad tiene tan pocas pruebas de seguridad?

**Respuesta: porque casi nada de la postura de seguridad se verifica desde un navegador.**

Es la confusión más frecuente en esta superficie: como el tema es la identidad, se
espera que la prueba E2E cubra el tema. Pero la E2E solo alcanza **lo que se observa
por la interfaz**. Lo demás se verifica leyendo la configuración, o con otras
herramientas, o no se verifica porque no existe.

| No se prueba | Por qué |
| --- | --- |
| El **token antifalsificación** | Es una defensa del servidor. Se prueba desde afuera del navegador, no manejándolo. |
| Los **atributos de la cookie** (`HttpOnly`, `SameSite`) | Es configuración, y se verifica leyendo el `Program.cs`. Una E2E ahí solo agregaría lentitud. |
| El **control de intentos**, el hash del secreto | No existen: la identidad es de laboratorio y lo declara en su propio `<remarks>`. |
| La **accesibilidad** del formulario | Otra clase de verificación, con otras herramientas. |

---

## 8. Cómo se corren

```bash
scripts/pruebas.sh login
REPETIR=8 scripts/pruebas.sh login
```

---

## 9. Los criterios, en una lista

Cada uno es la respuesta corta a la pregunta que lo abre, arriba.

1. **Afirmá el efecto, no el mecanismo.** La cookie es cómo; la superficie visible es qué.
2. **Nunca fabriques el estado que la prueba debería obtener actuando.**
3. **Derivá el andamiaje de cómo está construida la superficie**, no de la costumbre.
4. **Una propiedad negativa se prueba comparando dos desenlaces**, no mirando uno.
5. **Afirmá lo que tendría que fallar con razón**; lo reversible, dejalo suelto.
6. **Un caso, un motivo de falla.**
7. **Cada promesa escrita en el `src` es un caso esperando a ser escrito.**
8. **En una superficie de seguridad, escribí la promesa dos veces**: desde quien entra y
   desde quien no debería. La segunda es la que falta.
9. **Una promesa negativa rota no se nota nunca.** Si no hay un caso que la vigile, no hay
   nada más que la vigile.
