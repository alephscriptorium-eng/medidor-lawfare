# Buffer MCS-5 — Zapatero / Plus Ultra

## Origen

- **Agente:** modelo + operador | **Fecha:** 2026-06-17
- **Caso:** Zapatero / Plus Ultra — `ZAP-PU-2026-06-17`
- **Propósito:** calendario electoral focal; timeline PSOE/segunda línea Zapatero; tensiones Sánchez–Trump/Musk 2025–2026; contexto geopolítico ZP; origen internacional Plus Ultra

---

## 1. Introducción y Contexto

El 17 de junio de 2026, el expresidente del Gobierno español, José Luis Rodríguez Zapatero, declaró como investigado ante la Audiencia Nacional (juez José Luis Calama). Se le investiga en el marco del "caso Plus Ultra" por presuntos delitos que incluyen tráfico de influencias, organización criminal, blanqueo de capitales, falsedad documental, delitos fiscales y contrabando (vinculado a joyas halladas en su oficina). El juez denegó medidas cautelares, pero señaló "indicios racionales de criminalidad".

El objetivo de este estudio es modelar matemáticamente el impacto potencial de este suceso en las próximas elecciones generales en España.

## 2. Marco Temporal (La Variable Independiente)

Para establecer la línea temporal, definimos los hitos clave:

*   **Fecha del Suceso ($t_s$):** 17 de junio de 2026.
*   **Fecha Límite de las Elecciones Generales ($t_e$):** 22 de agosto de 2027 (fecha máxima legal para agotar la legislatura de 4 años desde el 23 de julio de 2023).
*   **Tiempo hasta las elecciones ($\Delta t$):** $t_e - t_s = 431 \text{ días}$ (aproximadamente 14.2 meses).

## 3. Modelo de Decaimiento del Impacto Electoral

Para responder a la solicitud de graduar el caso respecto al calendario real, estableceremos un modelo donde la relevancia de un escándalo político decae con el tiempo, un fenómeno bien documentado en la ciencia política ("efecto memoria del votante").

### 3.1. Definición de la Escala
*   **Relevancia Máxima ($R_{max} = 100\%$):** Suceso ocurrido el día exacto antes de las elecciones ($\Delta t = 1 \text{ día}$).
*   **Relevancia Mínima ($R_{min} \approx 0\%$):** Suceso ocurrido el día después de las elecciones anteriores ($\Delta t \approx 1460 \text{ días}$ o 4 años).

### 3.2. Ecuación de Decaimiento Exponencial
La memoria pública y mediática suele seguir una curva de decaimiento exponencial, no lineal. Modelaremos la Relevancia Electoral ($R$) en función de los días restantes hasta los comicios ($d$):

$$R(d) = 100 \cdot e^{-k \cdot d}$$

Donde $k$ es la constante de decaimiento. Para calcular $k$, asumimos empíricamente que un evento a mitad de legislatura (aprox. 730 días) retiene solo un 10% de su impacto inicial crudo (sin reactivaciones judiciales).
$10 = 100 \cdot e^{-k \cdot 730} \rightarrow k \approx 0.00315$

La función queda:
$$R(d) = 100 \cdot e^{-0.00315 \cdot d}$$

## 4. Resultados Aplicados al Caso Zapatero

Aplicando nuestro modelo al escenario actual:

*   Días hasta las elecciones ($d$): **431 días**.

Calculamos la Relevancia Teórica Base ($R_{base}$):
$$R(431) = 100 \cdot e^{-0.00315 \cdot 431} \approx 100 \cdot e^{-1.357} \approx \textbf{25.7\%}$$

### 4.1. Interpretación del Dato

Un resultado del **25.7% de relevancia electoral** significa que el impacto directo en la intención de voto el día de las urnas será de aproximadamente un cuarto del impacto que tendría si la declaración se hubiera producido en la semana de reflexión.

**Factores de Amortiguación (Por qué es un 25.7%):**
1.  **Distancia temporal (14 meses):** Es tiempo suficiente para que surjan múltiples crisis o debates nuevos que desplacen la atención mediática.
2.  **Lentitud judicial:** Los tiempos de la Audiencia Nacional garantizan que el juicio oral (el momento de mayor exposición) difícilmente se celebrará antes de agosto de 2027.

## 5. Variables de Modulación (El "Ruido" en el Modelo)

El modelo de decaimiento asume que el evento del 17 de junio es estático. Sin embargo, en la ciencia política el impacto real ($I_R$) se ajusta multiplicando la $R_{base}$ por factores moduladores ($M$):

$$I_R = R_{base} \cdot (M_{judicial} \cdot M_{partidista} \cdot M_{mediatico})$$

*   **$M_{judicial}$ (Riesgo de Reactivación):** Alto (>1.0). Si el juez dicta auto de procesamiento formal o apertura de juicio oral justo en la primavera de 2027 (época de elecciones municipales y autonómicas en mayo), el "reloj" de la relevancia se reinicia, disparando el impacto por encima del 70%.
*   **$M_{partidista}$ (Vinculación Directa):** Medio (~1.0). Zapatero **no está en primera línea electoral nacional** (sin cargo electivo, sin lista, sin ministerio), lo que amortigua el castigo directo al voto. Sin embargo, **sí mantiene segunda línea internacional documentable** respaldada por el PSOE (mediación Venezuela, actos Colombia, Congreso PSOE 2024): no es un exdirigente retirado del mapa político, sino figura con visibilidad internacional que puede amplificar cobertura mediática del caso.
*   **$M_{mediatico}$ (Retroalimentación):** Medio (1.0). Dependerá de la capacidad de la oposición de mantener el tema en el debate parlamentario.

**Nota metodológica:** el modelo de amortiguación (25.7%, $M_{partidista}$) es **contexto documental** para la sesión y cuarentena del cribado (L3); el motor MCN solo acumula señales positivas por ranura y no corrige Sincronía/Ventana por «elecciones lejanas».

## 6. Conclusión

Si evaluamos el suceso de hoy (declaración sin medidas cautelares a 431 días de las urnas) como un hecho aislado, su gradación en la escala de impacto electoral es **moderada-baja (aprox. 26/100)**. El tiempo juega a favor de la amortiguación del impacto.

Sin embargo, el verdadero riesgo electoral no radica en la declaración de hoy, sino en los hitos procesales futuros. Si los tiempos de la instrucción judicial sitúan el cierre del sumario o el inicio del juicio oral entre marzo y julio de 2027, el impacto se multiplicará exponencialmente, interfiriendo directamente en la campaña de las generales y en las autonómicas de mayo de 2027.

---

## 7. Timeline — Zapatero, PSOE y segunda línea internacional

Secuencia factual: rol institucional PSOE respalda canal internacional → imputación/registros Plus Ultra (may–jun 2026). Sin inferencia causal en esta tabla.

| Fecha | Hecho | Fuente | Relevancia PSOE |
|-------|-------|--------|-----------------|
| 2015–2026 | Mediación autodeclarada en Venezuela | El Periódico, 24-sep-2024 | Canal bilateral independiente del ejecutivo |
| 2023 | Intervención en acto sobre Colombia **organizado por el PSOE** (Madrid) | Pulzo | Respaldo partidista explícito |
| 2023 | Conferencia Bogotá «paz total» Petro; contactos entorno Petro | BluRadio | Segunda línea internacional |
| Sep-2024 | PSOE presenta enmienda al Congreso pidiendo reconocer «toda la labor de mediación» de Zapatero | El Confidencial, 10-sep-2024 | Respaldo institucional formal |
| Sep-2024 | Zapatero reconoce facilitación salida Edmundo González; acto con ministro Bolaños | ABC / El Periódico | Coordinación con Gobierno |
| Dic-2024 | Comparecencia en 41º Congreso PSOE Sevilla como figura destacada | Libertad Digital / prensa congreso | Presencia en órgano máximo partido |
| Dic-2025 | Apertura evento Frente Amplio Colombia con Zapatero como figura central | El País Colombia | Visibilidad internacional sostenida |

---

## 8. Tensiones geopolíticas documentadas

**Nota metodológica:** distinguir **presión/injerencia narrativa o comercial** (Trump/Musk en medios) de **cooperación judicial** (FR/CH en Plus Ultra). Son vectores distintos; no fusionar en un solo párrafo.

### 8A — Mandato Zapatero (2004–2011)

Contexto histórico del actor; no prueba directa del caso Plus Ultra 2026.

| Actor | Hecho verificable | Fuente |
|-------|-------------------|--------|
| **EEUU** | Presión diplomática contra venta de patrulleras/aviones a Venezuela (2008–2010); comunicaciones embajada USA Madrid | El País (cables WikiLeaks, 8-dic-2010) |
| **EEUU** | Retirada tropas Irak 2004; fricción inicial con administración Bush | Historiografía / prensa contemporánea |
| **China** | Zapatero visitó China 4 veces en mandato; partnership estratégico 14-nov-2005 | Springer (Fox/Godement) |
| **Rusia** | Zapatero declaró a Putin intención de relaciones «intensas y profundas» (2010) | Kremlin.ru, rueda prensa 2010 |

### 8B — Gobierno Sánchez vs agentes externos (2025–2026)

Capa distinta de §8A: documenta capacidad de presión/injerencia narrativa sobre el **Gobierno Sánchez** en el periodo inmediato al caso Plus Ultra.

#### Trump — OTAN La Haya (jun-2025)

| Fecha | Hecho documentado | Fuente |
|-------|-------------------|--------|
| 24–25-jun-2025 | Cumbre OTAN La Haya: aliados acuerdan meta 5% PIB defensa 2035; Sánchez mantiene objetivo 2,1% invocando flexibilidad | BBC Mundo, El País |
| 24-jun-2025 | Trump desde Air Force One: «España es un problema» por gasto defensa | El País 24-jun-2025 |
| 25-jun-2025 | Trump **amenazó** represalias comerciales: «Les vamos a hacer pagar el doble»; acusa a España de «viajar gratis» en seguridad | BBC Mundo, RFI |
| 25-jun-2025 | Moncloa responde; Economía recuerda competencia comercial de la Comisión Europea | El País 25-jun-2025 |

**Matiz:** Trump **amenazó** aranceles/expulsión; a jun-2026 **no consta** expulsión de OTAN ni aranceles bilaterales ejecutados (El País, mar-2026: comercio sigue operativo pese a retórica).

#### Trump — Bases Rota/Morón y Operación Furia Épica (2026)

| Fecha | Hecho documentado | Fuente |
|-------|-------------------|--------|
| Mar-2026 | Gobierno deniega uso bases Rota/Morón y espacio aéreo para operación USA-Israel contra Irán («Furia Épica»); invoca convenio 1988 art. 2.2 | El País 30-mar-2026, La Razón |
| Mar-2026 | Trump califica a España «aliado terrible»; **amenazó** cortar relaciones comerciales | El País 30-mar-2026 |
| Mar–may-2026 | Rubio: revisar relación OTAN por veto español; «¿Para qué estás en la OTAN?» | Cadena SER 21-may-2026, Diario Las Américas |
| Mar-2026 | Casa Blanca: «no necesita a España» para la misión; Cuerpo afirma sin represalias comerciales materializadas a un mes | El País 30-mar-2026 |

#### Musk — Plan España Crece (ene-2026)

| Fecha | Hecho documentado | Fuente |
|-------|-------------------|--------|
| 15-ene-2026 | Sánchez anuncia fondo soberano «España Crece» vía ICO; objetivo movilizar 120.000 M€; sectores incluyen IA, digitalización, computación cuántica | El Mundo, La Moncloa 16-feb-2026 |
| Feb-2026 | ICO: inyección 13.300 M€; Consejo de Ministros activa fondo | ico.es |

#### Musk — Redes sociales y choque directo (feb-2026)

| Fecha | Hecho documentado | Fuente |
|-------|-------------------|--------|
| 03-feb-2026 | Sánchez anuncia en Dubái: prohibición RRSS menores 16 años; responsabilidad penal directivos; tipificación manipulación algorítmica | La Moncloa, RTVE |
| 03-feb-2026 | Musk en X: «tirano y traidor al pueblo de España»; «fascista totalitario» | El País, BBC Mundo |
| Ene-2026 (previo) | Cruce previo migraciones: Sánchez responde a Musk «Marte puede esperar, la humanidad no» | RTVE 03-feb-2026 |
| 04-feb-2026 | Sánchez en X: «Deja que los tecno-oligarcas ladren, Sancho, es señal de que cabalgamos» (contexto Musk + Durov/Telegram) | Público, Infobae |

**Puente factual con caso foco (sin causalidad):**

- Rescate Plus Ultra **53 M€** (2021) fue decisión del **Gobierno Sánchez** (SEPI); trama investigada vincula fondos **venezolanos** (RTVE, El País).
- Imputación Zapatero **19-may-2026** y declaración **17-jun-2026** coinciden temporalmente con pico de tensión Sánchez–Trump (Irán/Rota) y choque Sánchez–Musk (feb-2026).
- Zapatero = segunda línea PSOE en Venezuela; Sánchez = primera línea bajo presión USA/tech. **Correlación temporal documentable; injerencia externa en instrucción judicial no.**

### 8C — Dualidad vías Venezuela 2024

| Hecho | Fuente |
|-------|--------|
| Ago-2024: España firma declaración conjunta con EEUU reconociendo victoria de González en Venezuela | Público; State.gov |
| Paralelo: Zapatero mantiene canal bilateral con Maduro (mediación 2015–2026) | El Periódico, El Confidencial sep-2024 |

Tensión de **doble vía** en política exterior venezolana 2024: Gobierno Sánchez en declaración multilateral USA; Zapatero en canal bilateral con Maduro.

---

## 9. Origen internacional del caso Plus Ultra

Cooperación judicial documentada (distinto de injerencia política):

| Fecha | Hecho | Fuente |
|-------|-------|--------|
| Jul-2024 | Fiscalía Anticorrupción recibe comisión rogatoria Suiza + orden europea investigación Francia sobre blanqueo vinculado a Venezuela | El País, Newtral, elDiario |
| Oct-2024 | Denuncia Fiscalía Anticorrupción; Plus Ultra como firmante/beneficiaria de préstamos con sociedades de red FR/CH/ES | RTVE, BBC Mundo |
| — | BBC Mundo: solicitudes FR/CH apuntaban inicialmente a **6 personas**; Zapatero **no** figuraba entre ellas | BBC Mundo |
| Mar-2026 | Juez Calama (Audiencia Nacional) | El País |
| 19-may-2026 | Imputación Zapatero (auto Calama) | buffer-04.md / prensa |
| 17-jun-2026 | Declaración como investigado; delitos citados; denegación cautelares | Auto AN Calama |

**Nota:** procedimientos paralelos en Francia, Suiza y **Estados Unidos** (p. ej. juicio Alex Saab, Miami, red CLAP Venezuela) documentan red de blanqueo relacionada temáticamente — **no** prueba de que EEUU impulsara imputación española a Zapatero.

**Verificado (Newtral, La Vanguardia):** origen **no** es Manos Limpias ni entrevista Aldama (diciembre 2025); Anticorrupción investigaba antes.

---

## 10. Vacío documental / Nota interpretativa (L3)

### Vacío documental — injerencia USA en lawfare español

**Búsqueda:** no aparece documento público que vincule Departamento de Estado, CIA, DOJ o agencia USA con la **imputación** de Zapatero ante Calama.

Lo verificable (L0/L1) entra al JSON; lo siguiente **no** entra sin ancla procesal:

- «La acusación se valió de ayuda USA para lawfare»
- «Washington neutralizó a Zapatero por Venezuela/China»

### Notas interpretativas (cuarentena L3 — Δ=0 en motor)

1. **Hipótesis lawfare focal:** el caso Plus Ultra podría neutralizar el canal internacional PSOE (Zapatero) — cadena causal interpretativa, no hecho verificable.
2. **Hipótesis agentes externos:** Trump/Musk amplificaron contexto adversarial sobre Sánchez en 2025–2026 — correlación temporal sí; injerencia en auto Calama no documentada.
3. **Modelo electoral:** ecuación 25.7% + $M_{partidista}$ corregido (§5) — contexto analítico, no señal MCN.

---

## Fuentes / Datos duros

1. **Auto AN 17-jun-2026** (Calama): delitos investigados (tráfico influencias, organización criminal, blanqueo, falsedad documental, delitos fiscales, contrabando); denegación medidas cautelares; «indicios racionales de criminalidad».
2. **LOREG** + investidura **23-jul-2023** → límite legal **22-ago-2027** (431 días desde declaración).
3. **Imputación previa 19-may-2026** (auto Calama) — ver buffer-04.md.
4. **Cooperación judicial FR/CH jul-2024** — comisión rogatoria Suiza, orden europea Francia (El País, Newtral).
5. **Timeline PSOE/Venezuela/Colombia** — El Periódico, El Confidencial, ABC, Pulzo, BluRadio, El País Colombia.
6. **Tensiones Sánchez–Trump/Musk** — BBC Mundo, El País, RFI, Cadena SER, La Moncloa, RTVE, Público.
7. **Declaración conjunta España–EEUU Venezuela ago-2024** — Público; State.gov.
