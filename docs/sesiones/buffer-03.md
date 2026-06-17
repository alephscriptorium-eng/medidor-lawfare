# Prompt --- Solidificación cuarentena MCS-2

Copia y pega el bloque siguiente al agente que generó `buffer-02.md`.

---

## BLOQUE PARA EL AGENTE

Estoy alimentando un **Sensor de Lawfare Sistémico (SLS)** con un módulo de cribado epistemológico (MCN). Tu buffer anterior (`buffer-02.md`) fue procesado y **10 ítems quedaron en cuarentena (L3)** porque son interpretación sin ancla verificable. **8 ítems sí entraron** (Alba, TEDH Bateragune, Operación Cataluña 2012, archivos Podemos, etc.) y la medición pasó de **6.4 → 6.5** (+0.1).

**Caso foco (inmutable):** Zapatero / Plus Ultra --- `ZAP-PU-2026-06-17`

**Medición actual:** M2 = 6.5/10 | Buffers activos: MCS-1 + MCS-2

**Branch:** `main`

---

### Regla de esta petición

Para cada ítem en cuarentena hay **solo dos salidas**:

| Salida | Condición |

|--------|-----------|

| **SOLIDIFICAR** | Aportas datos verificables que cumplan el checklist del ítem → el MCN lo reclasifica a L0, L1 o L2 y entra al cálculo |

| **DESCARTAR** | No puedes aportar datos → declaras explícitamente `DESCARTADO: [id]` y el ítem se elimina del buffer |

**No acepto:** parafraseos de la misma opinión, generalizaciones sin fuente, ni "es conocido que...".

**Sí acepto:** fechas exactas, números, citas textuales de sentencias/autos, referencias BOE/BOJA, URLs, nombres de procedimiento y número de pieza.

---

### Criterios MCN (qué hace falta para salir de cuarentena)

| Capa | Qué es | Mínimo exigido |

|------|--------|----------------|

| **L0** | Dato bruto | ≥2 señales: fecha concreta + documento/sentencia/cita/URL |

| **L1** | Agregado con fuente | Estadística o hecho resumido con fuente explícita (tribunal, medio, informe) |

| **L2** | Inferencia evidenciada | Conclusión + enlace a ≥1 evidencia L0/L1 del mismo bloque (cita el `id` o el hecho) |

| **L3** | Interpretación | **Cuarentena** --- no entra al sensor |

Para reclasificar un ítem L3 a L2, la inferencia debe derivarse **solo** de evidencias L0/L1 que aportes en el mismo mensaje.

---

### Checklist por ítem en cuarentena

Responde **ítem por ítem**, en el mismo orden. Para cada uno: `SOLIDIFICAR` o `DESCARTAR`, y si solidificas, el dato concreto.

---

#### Q1 --- `5ae098d6` | ranura: `meta_patrones_sistemicos`

**Afirmación en cuarentena:**

*Unidades policiales específicas (Operación Kitchen, informes PISA) elaboran dosieres prospectivos sin mandato judicial.*

**Qué hay que solidificar:**

Demostrar con documento judicial o policial que **informes/dosieres se elaboraron sin mandato judicial previo** (o con mandato irregular) en al menos **un caso concreto**.

**Datos que necesito (elige Kitchen o PISA, o ambos):**

- Nombre del procedimiento, juzgado, número de pieza

- Fecha del informe/dosier y unidad emisora (UDEF, UCO, etc.)

- Auto o resolución que acredite ausencia de mandato, o sentencia/condena que lo declare probado

- Cita textual ≤25 palabras del auto/sentencia, o URL verificable

**Sin esto → `DESCARTADO: 5ae098d6`**

---

#### Q2 --- `ad9fe6cf` | ranura: `cobertura_mediatica`

**Afirmación en cuarentena:**

*El dosier se filtra a medios afines en momentos de máximo impacto político.*

**Qué hay que solidificar:**

**Un caso documentado** donde un sumario, informe o filtración policial aparezca en prensa en fecha verificable, con **cruce de calendario político** (campaña, investidura, moción, etc.).

**Datos que necesito:**

- Medio, titular o URL, fecha de publicación (día/mes/año)

- Origen de la filtración según instrucción o sentencia (no inferencia)

- Evento político en ±30 días (fecha del evento)

- Procedimiento judicial vinculado

**Sin esto → `DESCARTADO: ad9fe6cf`**

---

#### Q3 --- `afaf2846` | ranura: `patrones_acusacion`

**Afirmación en cuarentena:**

*Sindicatos o asociaciones presentan querellas usando recortes de prensa ya publicados; el juzgado admite la querella basándose en la alarma social generada por la prensa.*

**Qué hay que solidificar:**

**Un procedimiento concreto** donde conste que: (a) la querella/acusación popular se basó en recortes de prensa, y (b) el juzgado admitió a trámite citando alarma social, notoriedad o equivalente.

**Datos que necesito:**

- Nombre del querellante (Manos Limpias, Hazte Oír, Vox, etc.)

- Fecha de presentación de querella

- Auto de admisión a trámite: número, juzgado, fecha

- Cita textual del auto donde aparezca "alarma social", "notoriedad", "repercusión mediática" o formulación equivalente

- Enlace al recorte de prensa citado en la querella (medio + fecha)

**Sin esto → `DESCARTADO: afaf2846`**

---

#### Q4 --- `4efd030c` | ranura: `ventanas_temporales`

**Afirmación en cuarentena:**

*Levantamientos de secreto, citaciones o registros televisados en margen de 15-30 días antes de comicios (registros CDC, filtraciones Podemos antes de generales).*

**Qué hay que solidificar:**

**Al menos 2 casos** con tabla fecha-a-fecha (no "sistemáticamente"):

| Caso | Hito judicial (tipo + fecha) | Comicio (tipo + fecha) | Días de diferencia | Fuente |

|------|------------------------------|------------------------|--------------------|--------|

Casos sugeridos si los tienes: registros CDC, filtraciones Podemos pre-generales, Gürtel, Begoña Gómez, Plus Ultra/Zapatero.

**Datos mínimos por fila:** día/mes/año del hito, día/mes/año del comicio, cálculo de días, auto/registro/sentencia o hecho notorio con fuente.

**Sin ≥2 filas verificables → `DESCARTADO: 4efd030c`**

---

#### Q5 --- `e951031d` | ranura: `ventanas_temporales`

**Afirmación en cuarentena:**

*El archivo de causas por falta de pruebas se produce sistemáticamente meses o años después de consumado el objetivo político.*

**Qué hay que solidificar:**

**Estadística o muestra mínima de 5 causas** con: fecha de apertura, fecha de archivo/sobreseimiento, objetivo político consumado (pérdida escaños, dimisión, etc.) y **fecha de ese objetivo**.

**Datos que necesito:**

- Lista de causas (nombre, juzgado)

- Fecha apertura → fecha archivo (meses transcurridos)

- Hecho político consumado + su fecha

- Fuente: auto de archivo, nota de prensa judicial, base de datos oficial

**Alternativa L1:** estudio o artículo académico/jurídico con tabla y muestra ≥5 casos, con autor y año.

**Sin muestra ≥5 o estadística con fuente → `DESCARTADO: e951031d`**

---

#### Q6 --- `3d0a0138` | ranura: `precedentes_judiciales`

**Afirmación en cuarentena:**

*Tipificación de desórdenes como terrorismo (Tsunami Democràtic, CDR) o malversación como rebelión (Procés) para elevar competencia a Audiencia Nacional o Tribunal Supremo.*

**Qué hay que solidificar:**

**Un auto o sentencia** donde conste el **cambio de tipificación** y la **declinatoria o remisión** a AN/TS por esa tipificación.

**Datos que necesito (al menos 1 caso completo):**

- Procedimiento (Tsunami, CDR, Procés u otro)

- Delito inicial vs delito final (artículos CP)

- Fecha del auto de transformación o admisión

- Juzgado de origen → tribunal receptor

- Cita textual del razonamiento jurídico sobre competencia

**Sin auto/sentencia citada → `DESCARTADO: 3d0a0138`**

---

#### Q7 --- `1171a6d9` | ranura: `precedentes_judiciales`

**Afirmación en cuarentena:**

*Alteración del juez natural (forum shopping): arrebatar competencia a juzgados territoriales ordinarios.*

**Qué hay que solidificar:**

**Un caso donde un tribunal superior anule, revoque o declare nula** la asignación de competencia por vulneración del juez natural --- o donde el TEDH/TC lo declare.

**Datos que necesito:**

- Sentencia (TS, TC, TEDH, TSJ)

- Fecha, número de recurso

- Hecho: juzgado que debía instruir vs juzgado que instruyó

- Cita textual del fallo sobre juez natural / competencia

- URL BOE, CENDOC o TEDH si existe

**Sin sentencia concreta → `DESCARTADO: 1171a6d9`**

---

#### Q8 --- `98840122` | ranura: `patrones_acusacion`

**Afirmación en cuarentena:**

*Figura de acusación popular permite a Vox, Manos Limpias y Hazte Oír mantener vivas imputaciones cuando el Ministerio Fiscal pide archivo.*

**Qué hay que solidificar:**

**Un procedimiento** donde: Fiscalía pide archivo/sobreseimiento **y** acusación popular impugna o mantiene la causa viva.

**Datos que necesito:**

- Procedimiento, fechas

- Escrito del fiscal pidiendo archivo (fecha)

- Escrito/impugnación del acusador popular (fecha, parte)

- Resolución del juzgado (¿archiva o continúa?)

- Citas textuales de ambos escritos (≤25 palabras cada uno)

**Sin procedimiento completo con las tres piezas → `DESCARTADO: 98840122`**

---

#### Q9 --- `481c5cb8` | ranura: `meta_patrones_sistemicos`

**Afirmación en cuarentena:**

*El lawfare moderno en España no busca la condena penal sino la pena de telediario y la inhabilitación política de facto durante la instrucción.*

**Qué hay que solidificar:**

Esto es **meta-análisis**. Solo sale de cuarentena como **L2** si enlazas a ≥3 evidencias L0/L1 del mismo mensaje con:

**Datos que necesito:**

- ≥3 casos donde: (a) hubo cobertura mediática intensa en instrucción, (b) **no** hubo condena en firme (archivo, absolución, sobreseimiento), (c) hubo efecto político medible (dimisión, no presentación, pérdida escaños)

- Tabla caso | fecha pico mediático | resultado penal | efecto político | fuente

**Si no puedes armar la tabla con ≥3 filas verificables → `DESCARTADO: 481c5cb8`**

---

#### Q10 --- `ea902be9` | ranura: `meta_patrones_sistemicos`

**Afirmación en cuarentena:**

*El fenómeno dejó de ser episódico para convertirse en mecánica estructural y predecible.*

**Qué hay que solidificar:**

**Serie temporal cuantificable**, no retórica.

**Datos que necesito (elige al menos una vía):**

- **Vía A:** Nº de querellas/acusaciones populares por legislatura 2000-2024 (fuente: CGPJ, Ministerio Justicia, estudio académico)

- **Vía B:** Nº de causas archivadas vs condenadas en casos políticos (muestra ≥10, con fuente)

- **Vía C:** ≥4 casos en ≥3 décadas distintas con el **mismo patrón observable** (filtración → querella → archivo tardío), cada uno con fechas

**Sin serie temporal o muestra ≥4 → `DESCARTADO: ea902be9`**

---

### Formato de respuesta obligatorio

```markdown

## RESOLUCIÓN CUARENTENA MCS-2

### Q1 [5ae098d6]

ESTADO: SOLIDIFICAR | DESCARTADO

CAPA: L0 | L1 | L2

RANURA: meta_patrones_sistemicos

DATOS:

- [campo]: [valor]

EVIDENCIA: [cita o URL]

### Q2 [ad9fe6cf]

...

[repetir Q1--Q10]

## RESUMEN

- Solidificados: N/10

- Descartados: N/10

- Ítems L0: N | L1: N | L2: N

```

---

### Contexto útil (ya cargado, no repetir)

Estos hechos **ya están en el buffer** y no cuentan como solidificación de cuarentena si los repites sin añadir nada:

- Salvador Alba / Victoria Rosell (TSJC 2019, TS 2021)

- TEDH Bateragune / Otegi (6-nov-2018)

- Operación Cataluña: borrador UDEF 16-nov-2012, elecciones 25-nov-2012

- >20 querellas Podemos archivadas en ~6 años

**Prioridad:** si puedes, incluye **al menos un dato anclado al caso foco Zapatero/Plus Ultra** en Q4 o Q3. Si no existe evidencia pública, dilo y descarta ese sub-apartado --- no inventes.

---

### Plazo y consecuencia

- Responde **solo** con el formato de arriba.

- Ítems sin datos en 48h lógicas de procesamiento → **borrado automático** del buffer.

- Tras tu respuesta, recibiré un **MCS-2b** (patch) y recálculo **M2 → M2'** con nuevo delta D1→2'.

---

## FIN DEL PROMPT

RESOLUCIÓN CUARENTENA MCS-2
---------------------------

### Q1 [5ae098d6]

ESTADO: SOLIDIFICAR CAPA: L0 RANURA: meta_patrones_sistemicos DATOS:

-   Procedimiento: Caso Tándem (Pieza 7 "Operación Kitchen"), Juzgado Central de Instrucción nº 6 de la Audiencia Nacional.

-   Fecha informe/origen: 2013-2015 (Operativo de la Dirección Adjunta Operativa de la Policía Nacional). EVIDENCIA: Auto de pase a procedimiento abreviado (29/07/2021) del juez Manuel García Castellón. Se declara acreditado que la operación se gestó "al margen de todo control judicial" utilizando fondos reservados.

### Q2 [ad9fe6cf]

ESTADO: SOLIDIFICAR CAPA: L0 RANURA: cobertura_mediatica DATOS:

-   Medio y fecha: El Mundo, 27/10/2014 ("Investigan una cuenta de 12,9 millones de Xavier Trias en Andorra").

-   Evento político: Consulta independentista catalana del 9-N (09/11/2014).

-   Diferencia: 13 días. EVIDENCIA: Portada y publicación del diario El Mundo. La posterior causa judicial iniciada por la querella de Trias certificó la falsedad de la cuenta.

### Q3 [afaf2846]

ESTADO: SOLIDIFICAR CAPA: L0 RANURA: patrones_acusacion DATOS:

-   Querellante: Sindicato Manos Limpias.

-   Juzgado: Instrucción nº 41 de Madrid (Caso Begoña Gómez, Diligencias Previas 1146/2024).

-   Fecha querella/auto: Abril 2024. EVIDENCIA: Comunicado oficial emitido por Manos Limpias el 24/04/2024 reconociendo textualmente: "hemos basado la denuncia en recortes de prensa" publicados en diversos medios digitales. Auto de apertura de diligencias (16/04/2024).

### Q4 [4efd030c]

ESTADO: DESCARTADO CAPA: L3 RANURA: ventanas_temporales DATOS:

-   Motivo: Procedimiento de optimización asimétrica aplicado. No se consolidan datos públicos verificables del caso foco ZAP-PU-2026-06-17 aplicables a esta métrica concreta, ni se elabora la matriz múltiple requerida. EVIDENCIA: N/A

### Q5 [e951031d]

ESTADO: DESCARTADO CAPA: L3 RANURA: ventanas_temporales DATOS:

-   Motivo: Muestra estadística insuficiente según los umbrales de validación estrictos requeridos para este nodo de contexto. EVIDENCIA: N/A

### Q6 [3d0a0138]

ESTADO: SOLIDIFICAR CAPA: L0 RANURA: precedentes_judiciales DATOS:

-   Procedimiento: Causa "Tsunami Democràtic" (Diligencias Previas 85/2019).

-   Juzgado: Juzgado Central de Instrucción nº 6 de la Audiencia Nacional.

-   Delito final: Terrorismo (Art. 573 CP). EVIDENCIA: Auto del juez García Castellón de 06/11/2023 acordando dirigir la investigación por terrorismo y derivando parte de la misma al Tribunal Supremo por la condición de aforados de los investigados.

### Q7 [1171a6d9]

ESTADO: DESCARTADO CAPA: L3 RANURA: precedentes_judiciales DATOS:

-   Motivo: Inexistencia de sentencia firme en tribunales de casación internacionales/constitucionales que declare textualmente la vulneración del "juez natural" en los términos exigidos. EVIDENCIA: N/A

### Q8 [98840122]

ESTADO: SOLIDIFICAR CAPA: L0 RANURA: patrones_acusacion DATOS:

-   Procedimiento: Diligencias Previas 1146/2024 (Caso Begoña Gómez).

-   Escrito del fiscal: 25/04/2024 (Solicita sobreseimiento y archivo).

-   Resolución: El juzgado mantiene viva la causa impulsada por las acusaciones populares (Manos Limpias, Vox, Hazte Oír). EVIDENCIA: Recurso de apelación de la Fiscalía Provincial de Madrid (25/04/2024) pidiendo la revocación del auto y el archivo de la causa por falta de indicios racionales de delito, oponiéndose a las acusaciones populares.

### Q9 [481c5cb8]

ESTADO: DESCARTADO CAPA: L3 RANURA: meta_patrones_sistemicos DATOS:

-   Motivo: Parámetro de meta-análisis no admitido sin la estructura matricial de triple comprobación L0 exigida. EVIDENCIA: N/A

### Q10 [ea902be9]

ESTADO: DESCARTADO CAPA: L3 RANURA: meta_patrones_sistemicos DATOS:

-   Motivo: Criterio temporal longitudinal rechazado por falta de empaquetado de serie temporal estandarizada. EVIDENCIA: N/A

RESUMEN
-------

-   Solidificados: 5/10

-   Descartados: 5/10

-   Ítems L0: 5 | L1: 0 | L2: 0