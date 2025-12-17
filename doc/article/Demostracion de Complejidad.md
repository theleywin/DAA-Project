
# Complejidad Computacional del Problema de Asignación de Frecuencias con Costos

## 1. Definición del Problema

Consideramos el **Problema de Asignación de Frecuencias con Costos (PAFC)**, definido de la siguiente manera:

Sea $ G = (V, E)$ un grafo no dirigido, donde cada vértice $ v \in V$ representa una torre de telecomunicaciones y cada arista $ (u, v) \in E$ indica que las torres $ u$ y $ v$ no pueden operar en la misma frecuencia debido a interferencias.

Sea $ C = \{c_1, c_2, \dots, c_k\}$ un conjunto finito de frecuencias disponibles (colores).  
Sea $ w : V \times C \rightarrow \mathbb{R}_{\ge 0}$ una función de costo que asigna un costo no negativo a la asignación de una frecuencia a una torre.

El objetivo es encontrar una función de asignación:
$$f : V \rightarrow C$$
tal que:

1. $ f(u) \neq f(v)$ para toda arista $ (u, v) \in E$,
2. el costo total $ \sum_{v \in V} w(v, f(v))$ sea mínimo.

Dado que este es un problema de optimización, analizamos su **versión de decisión** para estudiar su complejidad computacional.

---

## 2. Versión de Decisión del Problema

Definimos la versión de decisión del PAFC como sigue:

**Problema de Asignación de Frecuencias con Costos – Decisión (PAFC-D)**  

**Entrada**:  

- Un grafo $ G = (V, E)$  
- Un conjunto de $ k$ colores $ C$  
- Una función de costo $ w : V \times C \rightarrow \mathbb{R}_{\ge 0}$  
- Un entero $ B \ge 0$  

**Pregunta**:  
¿Existe una coloración válida $ f : V \rightarrow C$ tal que
$$\sum_{v \in V} w(v, f(v)) \le B \, ?$$

---

## 3. El Problema PAFC-D pertenece a NP

Para demostrar que PAFC-D pertenece a la clase NP, basta con mostrar que una solución candidata puede ser verificada en tiempo polinomial.

### Certificado

Una función de asignación $ f : V \rightarrow C$.

### Verificación

1. Para cada arista $ (u, v) \in E$, verificar que $ f(u) \neq f(v)$.  
   Esto puede hacerse en tiempo $ O(|E|)$.
2. Calcular el costo total $ \sum_{v \in V} w(v, f(v))$ en tiempo $ O(|V|)$.
3. Verificar que el costo total sea menor o igual a $ B$.

Dado que todos estos pasos se ejecutan en tiempo polinomial, concluimos que:

$$\text{PAFC-D} \in \text{NP}$$

---

## 4. PAFC-D es NP-Hard

Para demostrar que PAFC-D es NP-Hard, reducimos desde el problema **k-Coloring**, conocido por ser NP-completo para todo $ k \ge 3$.

### Problema k-Coloring

Dado un grafo $ G = (V, E)$, determinar si existe una coloración válida de $ G$ utilizando a lo sumo $ k$ colores.

---

### Reducción

Sea una instancia arbitraria de k-Coloring dada por un grafo $ G = (V, E)$.

Construimos una instancia de PAFC-D de la siguiente manera:

1. Utilizamos el mismo grafo $ G = (V, E)$.
2. Definimos el conjunto de colores $ C = \{1, 2, \dots, k\}$.
3. Definimos la función de costo como:
   $$   w(v, c) = 0 \quad \forall v \in V, \forall c \in C

$$
4. Definimos el presupuesto como:
   $$   B = 0
$$

Esta construcción puede realizarse en tiempo polinomial.

---

### Correctitud de la Reducción

- (**Si**)  
  Si el grafo $ G$ es k-colorable, entonces existe una coloración válida que cumple las restricciones de adyacencia.  
  Dado que todos los costos son cero, el costo total es $ 0 \le B$, por lo que la instancia de PAFC-D responde **sí**.

- (**Solo si**)  
  Si existe una solución a la instancia de PAFC-D con costo total menor o igual a $ B = 0$, entonces necesariamente se trata de una coloración válida del grafo $ G$ con $ k$ colores, lo que implica que $ G$ es k-colorable.

Por lo tanto, la instancia de k-Coloring tiene solución si y solo si la instancia construida de PAFC-D tiene solución.

---

## 5. Conclusión

Dado que:

- PAFC-D pertenece a NP, y
- PAFC-D es NP-Hard,

concluimos que:

$$\text{PAFC-D es NP-completo}$$

En consecuencia, el problema original de optimización de asignación de frecuencias con costos es **NP-Hard** y **NP-Completo**.

---

## 6. Implicaciones Prácticas

Este resultado justifica el uso de algoritmos exponenciales como backtracking, así como el desarrollo de heurísticas, técnicas de poda (branch and bound) y algoritmos aproximados para instancias de gran tamaño, dado que no se espera la existencia de algoritmos polinómicos exactos salvo que $ \text{P} = \text{NP}$.
