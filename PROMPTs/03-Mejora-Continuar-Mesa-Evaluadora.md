# Tool-Prompt — Mejora-Continuar-Mesa-Evaluadora

> **Invocación**: Leer y ejecutar `/LAB/Lab-E2E.WebBlazor.Documentacion/PROMPTs/03-Mejora-Continuar-Mesa-Evaluadora.md`
>
> **Overview**: El marco define un ciclo cerrado de revisión, veredicto, corrección y verificación sobre artefactos de especificación, ejecutado por un conjunto de agentes coordinados y con autonomía decisoria acotada.
>
> La composición del panel se determina por caso y no por plantilla. Un núcleo permanente —requisitos, verificación, lectura desde la perspectiva de un implementador sin contexto previo y refutación adversarial— se convoca siempre, dado que sus funciones no dependen del dominio. El resto de las especialidades se activa mediante señales observables en el artefacto, citadas con su ubicación: la presencia de umbrales, pesos o cuantificadores activa el rol formal-matemático; la de entidades y ciclos de vida, el de datos; y así con las demás. Cuando el caso exige una competencia ausente del catálogo, se instancia un agente ad hoc con una carta de mandato que declara tanto su competencia como sus límites. La decisión de composición corresponde a la mesa y no se eleva al usuario.
>
> Cada especialista produce su informe de forma independiente y sin acceso a los de sus pares, condición que evita el anclaje y preserva el valor informativo del panel. Todo hallazgo declara un nivel de evidencia según una escala que distingue el resultado ejecutable, la cita literal, el contraejemplo construido y la regla declarada; las conjeturas sin ancla no habilitan correcciones, solo preguntas. Un especialista que detecta una anomalía fuera de su mandato no emite hallazgo: emite una solicitud de convocatoria.
>
> Los informes consolidados pasan a un jurado de cinco miembros con funciones objetivo diferenciadas —evidencia, impacto, costo-beneficio, coherencia con decisiones previas y riesgo de irreversibilidad—, que vota hallazgo por hallazgo con fundamento explícito y determina si corresponde aplicar correcciones. Los hallazgos aprobados pasan a un cuerpo auditor que diseña parches concretos, con texto exacto, costo, reversibilidad, artefactos derivados afectados y criterio de verificación. La aprobación se resuelve por argumentación en la mesa, con cuatro resultados posibles: aplicar, mejorar el plan antes de aplicar, no aplicar registrando el defecto como deuda asumida, o escalar. La separación entre quien diseña la corrección y quien la aprueba es estructural.
>
> Aplicada la corrección, se ejecuta su criterio de verificación y se reversa automáticamente ante regresión. Rige el principio de reparación en la capa de origen: un defecto nacido en la especificación no se parchea aguas abajo, y toda corrección marca los artefactos derivados como pendientes de revalidación.
>
>La escalada al usuario opera por excepción y bajo una lista cerrada de disparadores: ambigüedad de intención irresoluble por evidencia, conflicto entre restricciones duras, cambio de alcance, irreversibilidad con impacto material, dominios con consecuencia externa, empate persistente del jurado y reapertura de una decisión cerrada. Fuera de esos casos la mesa resuelve; ante duda sobre si escalar, se aplica el criterio por defecto y se registra. Las consultas se emiten agrupadas, con opciones, recomendación fundada y comportamiento previsto ante ausencia de respuesta.
>
> El objetivo declarado no es la exhaustividad sino la coherencia verificable, entendida como ausencia de contradicciones, trazabilidad completa entre requisitos, tareas y pruebas, y univocidad terminológica. El ciclo termina por agotamiento de hallazgos relevantes, por rendimientos decrecientes o por presupuesto, y emite un registro de cierre que documenta la composición del panel y sus motivos, las correcciones aplicadas y verificadas, la deuda asumida deliberadamente y las consultas pendientes.

---


# Marco de orquestación multiagente para Spec-Driven Development

Ciclo cerrado de revisión, veredicto, corrección y verificación sobre artefactos de especificación.
Genérico: no asume lenguaje, framework ni herramienta de orquestación.

---

## 0. Qué cambia respecto del pedido original

| Problema del prompt original | Corrección en este marco |
|---|---|
| El ciclo no tiene condición de corte: puede iterar para siempre | §7 criterios de parada, con presupuesto de ciclos y detección de rendimientos decrecientes |
| "Que la mesa evalúe si me necesita" queda a criterio del modelo | §6 lista cerrada de disparadores de escalada; fuera de esa lista, la mesa decide sola |
| "Evidencias contrastables" no está definido | §3 escala E1–E4; un hallazgo sin ancla no puede fundar una corrección, solo una pregunta |
| Jurado de 5 sin regla de votación ni desempate | §5.3 regla de mayoría, quórum, veto acotado y qué pasa ante empate |
| Los auditores diseñan la corrección y la mesa aprueba, pero nada impide que sean el mismo criterio | §4 separación de funciones: quien diseña no vota su propio parche |
| Informes en prosa libre → imposible deduplicar, comparar o auditar | §8 esquemas JSON obligatorios para hallazgo, veredicto, parche y escalada |
| Nada verifica que la corrección haya funcionado | §5.6 toda corrección viaja con su criterio de verificación y se re-ejecuta |
| No es específico de SDD | §2 el objeto bajo revisión es la cadena spec → plan → tareas → código/pruebas, y §5.5 obliga a reparar en la capa de origen |
| Panel fijo: sobra gente para un caso y falta para otro | §4.1 núcleo permanente + catálogo activado por señal + agentes ad hoc con carta de mandato; §5.1 la mesa dirime la composición |

---

## 1. Principios

1. **Reparar en la capa de origen.** Si el defecto nace en la especificación, no se parchea el código. Corregir aguas abajo un defecto de arriba genera deuda invisible.
2. **Propagación explícita.** Toda corrección de una capa marca como "a revalidar" los artefactos derivados de ella.
3. **Autonomía por defecto, escalada por excepción.** El humano se consulta solo ante los disparadores de §6. Todo lo demás lo resuelve la mesa.
4. **Nada se afirma sin ancla.** Ver §3.
5. **Separación de funciones.** Detectar, juzgar, diseñar la corrección y aprobarla son cuatro roles distintos.
6. **Desacuerdo obligatorio antes que consenso.** El consenso temprano es señal de anclaje, no de calidad.
7. **El presupuesto no existe para ahorrar, existe para forzar convergencia.** Un ciclo sin techo no converge: acumula hallazgos cosméticos.
8. **El panel se arma por caso.** La composición es una decisión del ciclo, no una plantilla, y se justifica con señales observables en el artefacto.
9. **Nadie opina fuera de su mandato.** Un agente que detecta algo ajeno a su competencia pide que se convoque a quien corresponda; no improvisa la especialidad.

---

## 2. Contrato de entrada (Fase 0)

El ciclo no arranca sin esto. Si falta un campo, ese es el primer hallazgo.

```yaml
objeto:
  artefacto: <spec | plan | tareas | implementación>
  ruta/id: <identificador estable>
  version: <hash o número>
  capas_derivadas: [<artefactos que dependen de este>]
objetivo: <qué debe lograr el artefacto, en una oración>
restricciones_duras: [<no negociables: plazos, stack, normativa, compatibilidad>]
decisiones_cerradas: [<lo ya decidido y que NO se reabre salvo contradicción demostrada>]
fuera_de_alcance: [<lo que el panel no debe tocar>]
umbral_de_calidad: <qué severidades bloquean el cierre; por defecto S1 y S2>
presupuesto: { ciclos_max: 3, hallazgos_max_por_especialista: 7 }
```

`decisiones_cerradas` es lo que evita el patrón más caro de estos sistemas: cada ciclo redescubre y rediscute lo mismo. Solo se reabre una decisión cerrada si un hallazgo con evidencia E1 o E2 demuestra que es **contradictoria**, no que es mejorable.

---

## 3. Definiciones operativas

### Evidencia

| Nivel | Qué es | Puede fundar |
|---|---|---|
| **E1** | Resultado ejecutable reproducible: prueba que falla, build roto, linter, verificación de esquema | corrección directa |
| **E2** | Cita literal del artefacto con ubicación (sección/línea) que muestra contradicción, ambigüedad u omisión | corrección directa |
| **E3** | Contraejemplo construido: un caso concreto de entrada/escenario que el artefacto no resuelve | corrección directa |
| **E4** | Regla externa declarada en el contrato de entrada (norma, convención del equipo, restricción dura) | corrección directa |
| **C** | Conjetura, experiencia general, "suele ser mejor" | **solo** una pregunta o un pedido de evidencia, nunca un parche |

Regla dura: un hallazgo nivel C que sobrevive a dos ciclos sin ascender de nivel se descarta y se registra como descartado.

### Severidad

- **S1 — bloqueante**: hace inejecutable o inconsistente el artefacto. Contradicción interna, requisito sin criterio de aceptación posible, restricción dura violada.
- **S2 — grave**: se puede implementar, pero con alta probabilidad de retrabajo o de interpretación divergente entre implementadores.
- **S3 — moderado**: pérdida de calidad acotada, sin riesgo de retrabajo.
- **S4 — cosmético**: estilo, redacción, orden.

Por defecto S4 no entra a jurado: se aplica o se descarta en lote.

### Confianza

Número en `[0,1]` que declara cada especialista por hallazgo. Es la probabilidad subjetiva de que el hallazgo sea real *y* relevante. Se usa en §6 para decidir escaladas, no para reemplazar el voto.

### Coherencia (métrica, no adjetivo)

Un artefacto es coherente cuando, verificablemente:
- no hay dos afirmaciones que no puedan ser ambas verdaderas;
- todo requisito tiene ID, criterio de aceptación y al menos una prueba que lo referencia;
- toda tarea referencia al menos un requisito;
- no hay requisito huérfano (sin tarea) ni tarea huérfana (sin requisito);
- todo término del glosario se usa con un solo sentido.

Estas cinco condiciones son chequeables mecánicamente y son la línea de base del panel: si alguna falla, hay un S1 antes de que nadie opine.

---

## 4. Roles

### 4.1 Panel de especialistas (detectan)

El panel **no es fijo**: se arma por caso. Hay un núcleo que se convoca siempre y un catálogo variable que se activa por señal detectada en el artefacto (§4.1.2). La composición la dirime la mesa de convocatoria (§5.1).

Cada especialista emite su informe **sin ver el de los demás**. La independencia es la fuente de valor del panel; si trabajan en secuencia con contexto compartido, el segundo repite al primero.

#### 4.1.1 Núcleo permanente

Se convoca siempre, cualquiera sea el artefacto. Son los roles que no dependen del dominio sino de la naturaleza del objeto.

| Rol | Pregunta que responde |
|---|---|
| **Requisitos** | ¿Cada requisito es unívoco, atómico y verificable? ¿Falta algún caso? |
| **Verificación / QA** | ¿Cómo se prueba cada afirmación? ¿Qué requisito no es testeable? |
| **Implementador ingenuo** | ¿Un dev que no participó de la discusión puede implementar esto sin preguntar nada? Cada pregunta que necesita hacer es un hallazgo |
| **Abogado del diablo** | Mandato explícito de atacar la propuesta dominante. Entra después de leer al resto |

#### 4.1.2 Catálogo variable y señales de convocatoria

Cada especialidad se activa por una señal **observable en el artefacto**, no por intuición. La señal se cita como cualquier evidencia: con ubicación.

| Rol | Se convoca cuando el artefacto contiene… |
|---|---|
| **Arquitectura** | más de un componente, integración entre sistemas, o una restricción dura de stack |
| **Formal / matemático** | condiciones compuestas, umbrales numéricos, estimaciones, pesos, prioridades calculadas, cuantificadores ("todos", "siempre", "ninguno") |
| **Datos y dominio** | entidades, estados, ciclos de vida, persistencia, migraciones |
| **Seguridad y privacidad** | autenticación, permisos, datos personales, exposición pública, secretos |
| **Operación y entrega** | despliegue, ambientes, disponibilidad, observabilidad, versionado |
| **Concurrencia / tiempo** | procesos simultáneos, colas, reintentos, idempotencia, orden de eventos |
| **Rendimiento y costo** | volumen declarado, latencia prometida, límites de consumo |
| **Interfaz / consumidor externo** | API pública, contrato con terceros, retrocompatibilidad |
| **Cumplimiento / normativa** | obligaciones legales, auditoría, retención de datos |
| **Accesibilidad / uso** | interfaz de usuario, flujos con personas |

El rol formal/matemático es de convocatoria automática: si su señal aparece, entra sin discusión.

#### 4.1.3 Agentes ad hoc

Si el caso exige una competencia que el catálogo no cubre, la mesa **instancia un agente nuevo** con una carta de mandato:

```yaml
agente_ad_hoc:
  id: AH-001
  nombre: <especialidad>
  señal_que_lo_justifica: { descripción: "...", ubicación: "§X, línea N" }
  pregunta_que_responde: <UNA pregunta, la razón de su existencia>
  competencia: <qué sabe y qué NO le corresponde opinar>
  evidencia_admisible: [E1, E2, E3, E4]
  tope_hallazgos: 5
  se_disuelve_cuando: <condición explícita>
```

Un agente sin carta de mandato no puede emitir hallazgos: sus salidas se descartan en la consolidación. La carta es lo que impide que un agente "de dominio X" opine sobre todo.

#### 4.1.4 Mandato y disolución

- **Nadie opina fuera de su mandato.** Si un especialista detecta algo fuera de su competencia, no emite hallazgo: emite una **solicitud de convocatoria** (§5.2). Opinar fuera de mandato es la vía más común por la que estos sistemas producen ruido con apariencia de rigor.
- Un especialista variable que en dos ciclos consecutivos no produce ningún hallazgo con veredicto `PROCEDE` **no se reconvoca** en el ciclo siguiente. Se registra como "señal presente, aporte nulo". Sigue disponible si aparece una señal nueva.
- Los agentes ad hoc se disuelven al cumplirse su `se_disuelve_cuando`, o al cierre del ciclo si no se especificó.
- **Techo de panel**: núcleo + hasta 5 variables/ad hoc por ciclo. Si hay más señales que cupo, la mesa prioriza por severidad esperada y registra las especialidades postergadas; entran en el ciclo siguiente.

### 4.2 Relator (consolida, no vota)

Deduplica hallazgos, los agrupa por raíz común, detecta contradicciones **entre especialistas** y las eleva como ítem separado al jurado. No emite juicio propio ni edita el contenido de un hallazgo.

### 4.3 Jurado (juzgan, mínimo 5)

Cada juez tiene una función objetivo distinta, para que la diversidad sea estructural y no de personalidad:

1. **Juez de evidencia** — ¿el hallazgo está probado al nivel que declara?
2. **Juez de impacto** — si no se corrige, ¿qué pasa concretamente?
3. **Juez de costo/beneficio** — ¿el costo de corregir es menor al daño de no hacerlo?
4. **Juez de coherencia histórica** — ¿esto reabre una decisión cerrada? ¿es consistente con veredictos previos del mismo ciclo?
5. **Juez de riesgo e irreversibilidad** — ¿la corrección es revertible? ¿qué se rompe si sale mal?

El jurado es **fijo en función, no en dominio**: estas cinco preguntas son las mismas para una spec de facturación que para una de infraestructura, así que no se convocan jueces por especialidad. Cuando un hallazgo exige conocimiento que ningún juez tiene, se convoca un **perito**: el especialista que lo emitió responde preguntas del jurado, pero **no vota**. Así el quórum queda impar y el que detecta no se juzga a sí mismo.

### 4.4 Cuerpo auditor (diseña las correcciones)

Recibe solo los hallazgos con veredicto "procede". Produce un parche concreto sobre el artefacto —texto nuevo, no consejo— con costo, riesgo, artefactos derivados afectados y criterio de verificación.

**No vota la aprobación de sus propios parches.** Puede argumentar ante la mesa; no puntúa.

---

## 5. El ciclo

### 5.1 Base mecánica y convocatoria

**a) Chequeos mecánicos.** Antes de cualquier agente: correr los cinco chequeos de coherencia de §3. Lo que falle entra como S1 con evidencia E1. Esto es barato y evita gastar un panel entero en descubrir que faltan IDs.

**b) Barrido de señales.** Un agente relevador —sin voto y sin capacidad de emitir hallazgos— recorre el artefacto y lista las señales del catálogo (§4.1.2) que aparecen, cada una con su ubicación. Su salida es un inventario, no un juicio.

**c) Mesa de convocatoria.** Los mismos 5 jueces resuelven la composición del panel, votando por especialidad propuesta:

- `CONVOCAR` — la señal está presente y el aporte esperado es real.
- `NO_CONVOCAR` — la señal aparece pero es marginal, o la cubre el núcleo. Se registra el motivo: si después aparece un defecto en esa área, el registro es lo que permite corregir el criterio.
- `INSTANCIAR_AD_HOC` — no hay rol en el catálogo; se redacta la carta de mandato de §4.1.3 y se vota sobre ella, no sobre la idea.

Reglas: mayoría simple; ante empate, **se convoca** (el costo de un especialista de más es un informe descartable, el de uno de menos es un punto ciego); techo de 5 variables; los que no entran por cupo quedan en cola priorizada.

La convocatoria se registra completa —convocados, descartados con motivo y postergados—, y ese registro se compara al cierre contra los hallazgos reales. Es el mecanismo con el que el marco aprende a armar paneles: si la especialidad X se convoca cinco veces y nunca aporta un `PROCEDE`, su señal está mal definida.

### 5.2 Panel independiente

Cada especialista, en paralelo y a ciegas, produce hasta `hallazgos_max_por_especialista`. El tope es deliberado: sin él, cada agente justifica su existencia inflando hallazgos.

Cada uno declara además explícitamente: **"lo que revisé y está bien"** (máximo 3 ítems). Sirve para distinguir "no lo miró" de "lo miró y no hay problema".

**Solicitud de convocatoria en caliente.** Si un especialista encuentra algo fuera de su mandato, no opina: emite

```yaml
solicitud_convocatoria:
  solicitante: <rol>
  especialidad_faltante: <...>
  señal: { descripción: "...", ubicación: "§X, línea N" }
  qué_no_puedo_afirmar_sin_ella: <una oración>
```

Las solicitudes se resuelven en una convocatoria breve al cerrar el panel, con la misma regla de votación. Si se aprueba, el nuevo especialista trabaja a ciegas sobre el artefacto —no ve los informes existentes— y su salida entra a la misma consolidación. Máximo **una** ronda de convocatoria en caliente por ciclo: lo que aparezca después, entra al ciclo siguiente.

### 5.3 Jurado y veredicto

El relator consolida; el jurado vota **por hallazgo**, no en bloque. Tres opciones:

- `PROCEDE` — se corrige
- `NO_PROCEDE` — se archiva con motivo
- `INSUFICIENTE` — hay algo, pero la evidencia no alcanza; vuelve al especialista con un pedido concreto (una vez; a la segunda se archiva)

Reglas:
- **Quórum**: 5 votos. Menos de 5, no hay veredicto.
- **Mayoría simple** (≥3) decide.
- **Empate o 2-2-1**: pasa a `INSUFICIENTE` automáticamente en la primera ronda. Si vuelve a empatar en la segunda, es disparador de escalada (§6).
- **Veto acotado**: el juez de riesgo puede vetar un `PROCEDE` únicamente si la corrección es irreversible *y* la severidad es S3 o menor. El veto no archiva: convierte el ítem en escalada.
- Los votos se registran con una línea de fundamento cada uno. Un voto sin fundamento no cuenta para el quórum.

### 5.4 Diseño de correcciones

Los auditores producen, por hallazgo aprobado, un parche con: texto exacto a reemplazar/agregar, capa donde se aplica, artefactos derivados a revalidar, criterio de verificación y plan de reversión.

Si dos parches tocan la misma sección, se fusionan en uno solo antes de la aprobación. Parches solapados aplicados en secuencia son la causa más común de que un ciclo automatizado rompa el artefacto.

### 5.5 Aprobación (mesa de decisión)

Cuatro resultados posibles por parche o lote:

- `APLICAR`
- `MEJORAR_PLAN` — el hallazgo es válido, el parche no. Vuelve a auditoría con la objeción concreta. Máximo 2 vueltas.
- `NO_APLICAR` — el costo o el riesgo del parche supera al del defecto. Se registra el defecto como aceptado conscientemente (deuda declarada, no ignorada).
- `ESCALAR` — §6.

Chequeo obligatorio antes de aplicar: **¿este parche corrige en la capa donde nació el defecto?** Si no, se rechaza y se reformula contra la capa de origen.

### 5.6 Aplicación y verificación

Se aplica, se corre el criterio de verificación de cada parche y se re-corren los chequeos mecánicos de §5.1. Si la verificación falla, se revierte ese parche y su hallazgo vuelve a auditoría marcado como `regresión`.

Se registra un changelog: hallazgo → veredicto → parche → resultado de verificación → versión nueva del artefacto.

### 5.7 Cierre o nuevo ciclo

Ver §7.

---

## 6. Cuándo consultar al humano

**Regla general: la mesa decide sola.** Se escala si y solo si aparece uno de estos disparadores:

1. **Ambigüedad de intención irresoluble por evidencia** — el artefacto admite dos lecturas legítimas y ninguna evidencia disponible desempata. Es una pregunta sobre qué se quiso, no sobre qué es correcto.
2. **Conflicto entre restricciones duras** — no existe solución que satisfaga todas las declaradas en el contrato de entrada.
3. **Cambio de alcance** — la corrección agrega, quita o redefine lo que el sistema promete hacer.
4. **Irreversibilidad con impacto real** — migraciones de datos, contratos públicos de API, cualquier cosa cuya reversión cueste más que la corrección.
5. **Dominio con consecuencia externa** — dinero, datos personales, obligaciones legales o de terceros.
6. **Empate persistente** — el jurado no resuelve tras dos rondas.
7. **Reapertura de decisión cerrada** — el panel sostiene que una decisión de `decisiones_cerradas` es contradictoria.

Todo lo demás —redacción, estructura, trazabilidad faltante, criterios de aceptación ausentes, nombres, orden de tareas, elección técnica dentro de las restricciones ya dadas— se resuelve sin consultar.

### Formato de la escalada

Una escalada mal formateada es peor que no escalar: devuelve al humano el trabajo de reconstruir el contexto. Formato obligatorio:

```yaml
escalada:
  id: ESC-001
  disparador: <cuál de los 7>
  pregunta: <UNA pregunta cerrada>
  contexto: <máximo 5 líneas: qué se encontró y por qué la mesa no puede decidir>
  opciones:
    - id: A
      descripción: <...>
      consecuencia: <...>
    - id: B
      descripción: <...>
      consecuencia: <...>
  recomendación_de_la_mesa: <A o B, con una línea de fundamento y el reparto de votos>
  si_no_respondés: <qué hace la mesa por defecto y qué queda bloqueado>
```

Las escaladas se acumulan y se entregan **juntas al final del ciclo**, no de a una. Salvo las de tipo 2 y 3, que bloquean el ciclo y salen en el momento.

---

## 7. Criterios de parada

El ciclo cierra cuando se cumple **cualquiera**:

- No quedan hallazgos abiertos por encima del `umbral_de_calidad`.
- **Rendimientos decrecientes**: el ciclo N produjo menos del 20% de hallazgos válidos nuevos (severidad ≥ S3, veredicto `PROCEDE`) respecto del ciclo N-1.
- Se agotó `ciclos_max`.
- Hay una escalada bloqueante sin responder.

Al cerrar, se emite:

```yaml
cierre:
  version_final: <...>
  ciclos_ejecutados: <n>
  panel:
    convocados: [<rol: hallazgos_procedentes>]
    descartados: [<rol: motivo>]
    ad_hoc: [<id: pregunta que respondió y qué aportó>]
    postergados_por_cupo: [<rol>]
    aporte_nulo: [<roles a no reconvocar el próximo ciclo>]
  hallazgos: { detectados: n, procedentes: n, aplicados: n, revertidos: n }
  coherencia: { contradicciones: 0, requisitos_sin_criterio: 0, requisitos_sin_prueba: 0, tareas_huérfanas: 0 }
  deuda_declarada: [<hallazgos NO_APLICAR con su motivo>]
  escaladas_pendientes: [<...>]
  capas_a_revalidar: [<artefactos derivados afectados>]
```

`deuda_declarada` y `capas_a_revalidar` son la salida más valiosa del ciclo y la que estos sistemas suelen perder.

---

## 8. Esquemas

```json
{
  "hallazgo": {
    "id": "H-001",
    "especialista": "requisitos",
    "capa_origen": "spec",
    "ubicación": "§4.2, línea 118",
    "afirmación": "una oración: qué está mal",
    "evidencia": { "nivel": "E2", "ancla": "cita literal o comando y su salida" },
    "severidad": "S2",
    "confianza": 0.8,
    "impacto_si_no_se_corrige": "una oración concreta",
    "propuesta_de_dirección": "qué habría que lograr, no cómo redactarlo"
  },
  "veredicto": {
    "hallazgo_id": "H-001",
    "votos": [{ "juez": "evidencia", "voto": "PROCEDE", "fundamento": "..." }],
    "resultado": "PROCEDE",
    "conteo": "4-1"
  },
  "parche": {
    "id": "P-001",
    "hallazgos_cubiertos": ["H-001", "H-007"],
    "capa": "spec",
    "cambio": { "reemplazar": "<texto exacto>", "por": "<texto exacto>" },
    "costo": "bajo|medio|alto",
    "reversible": true,
    "derivados_a_revalidar": ["plan", "tareas"],
    "verificación": "chequeo concreto que debe pasar después de aplicar"
  }
}
```

---

## 9. Salvaguardas contra fallas típicas

| Falla | Salvaguarda en el marco |
|---|---|
| **Teatro deliberativo**: agentes que actúan un debate sin cambiar nada | Todo voto exige fundamento; todo parche exige texto exacto, no consejo |
| **Anclaje**: todos repiten al primero | Panel a ciegas (§5.2); abogado del diablo con mandato explícito |
| **Inflación de hallazgos** | Tope por especialista; nivel C no funda correcciones; descarte automático tras dos ciclos |
| **Consenso vacío** | Si el jurado vota 5-0 en más del 80% de los ítems, el ciclo se marca como sospechoso de homogeneidad y el abogado del diablo revisa los `NO_PROCEDE` |
| **Regresión por corrección** | Verificación post-aplicación con reversión automática (§5.6) |
| **Parcheo en la capa equivocada** | Chequeo obligatorio de capa de origen antes de aplicar (§5.5) |
| **Loop infinito** | Rendimientos decrecientes + `ciclos_max` |
| **Escaladas que devuelven el problema al humano** | Formato con opciones, recomendación y default (§6) |
| **Convocatoria inflada**: se llama a todos "por las dudas" | Toda convocatoria exige señal con ubicación; techo de 5 variables; no reconvocatoria tras dos ciclos de aporte nulo |
| **Punto ciego**: falta la especialidad que importaba | Barrido de señales previo, solicitud de convocatoria en caliente, y empate en la mesa se resuelve convocando |
| **Agente ad hoc que opina de todo** | Carta de mandato obligatoria con competencia y no-competencia; sin carta, sus salidas se descartan |
| **Panel armado por costumbre** | El registro de convocatoria se contrasta al cierre contra los hallazgos reales |

---

## 10. Prompt de arranque

> Vas a ejecutar un ciclo de mejora sobre el artefacto adjunto, siguiendo el marco de orquestación que te paso. Reglas no negociables:
>
> 1. Empezá validando el contrato de entrada (§2). Si falta un campo, ese es tu primer hallazgo y lo resolvés con supuestos declarados, no preguntándome.
> 2. Corré los cinco chequeos mecánicos de coherencia (§3) antes de convocar a ningún especialista.
> 3. **Armá el panel para este caso, no por plantilla.** Relevá las señales del artefacto, convocá el núcleo permanente más las especialidades que esas señales justifiquen, e instanciá agentes ad hoc con carta de mandato si el catálogo no alcanza. La composición la vota la mesa y queda registrada con motivos, incluidos los descartes.
> 4. El panel trabaja a ciegas y en paralelo. Ningún especialista ve el informe de otro hasta la consolidación. Si alguno encuentra algo fuera de su mandato, emite una solicitud de convocatoria en lugar de opinar.
> 5. Todo hallazgo declara nivel de evidencia. Las conjeturas no generan correcciones.
> 6. El jurado son 5 jueces con las funciones objetivo de §4.3, votan por hallazgo y cada voto lleva fundamento. Los jueces no cambian según el dominio: si hace falta conocimiento que no tienen, llaman como perito al especialista, que responde pero no vota.
> 7. Los auditores diseñan parches con texto exacto y criterio de verificación. No aprueban sus propios parches.
> 8. **Decidís sin consultarme salvo que se dispare uno de los 7 casos de §6.** Si dudás si escalar, no escales: aplicá el default y registralo en `deuda_declarada`. La composición del panel nunca es motivo de escalada: es tuya.
> 9. Las escaladas van juntas al final, con opciones, recomendación y qué hacés si no respondo.
> 10. Parás según §7 y emitís el bloque de cierre completo.
>
> Entregame: el registro de convocatoria, los informes del panel, la tabla de veredictos, los parches aplicados con su verificación, el bloque de cierre y las escaladas si las hubiera. No me entregues la deliberación completa salvo que se la pida.
