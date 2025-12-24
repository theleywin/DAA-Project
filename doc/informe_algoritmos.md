# Informe Técnico: Algoritmos para Coloreado de Grafos de Costo Mínimo

Este documento describe los algoritmos implementados para resolver el problema de Coloreado de Grafos de Costo Mínimo, incluyendo su funcionamiento, estrategias y análisis de complejidad.

## 1. Algoritmo Greedy Básico (Voraz)

### Funcionamiento
Es el enfoque más simple y directo. Itera sobre los nodos del grafo en un orden predeterminado (por defecto, el orden secuencial de índices 0 a N-1). Para cada nodo, selecciona el primer color válido que minimice el costo localmente.

### Estrategia
1.  Iterar por cada nodo $v$ en $V$.
2.  Identificar los colores usados por los vecinos de $v$.
3.  Asignar a $v$ el color de menor costo que no esté en uso por sus vecinos.

### Análisis de Complejidad
-   **Tiempo**: $O(V \times D_{max} \times K)$, donde $V$ es el número de vértices, $D_{max}$ el grado máximo y $K$ el número de colores. Para cada nodo, revisamos sus vecinos y luego probamos colores. En el peor caso (grafo completo) es $O(V^2)$.
-   **Espacio**: $O(V)$ para almacenar las asignaciones.

---

## 2. Algoritmo Welsh-Powell

### Funcionamiento
Es una extensión del algoritmo voraz que mejora la calidad de la solución ordenando los nodos antes de colorearlos. La idea es que los nodos con mayor grado (más conexiones) son más difíciles de colorear y deben ser procesados primero.

### Estrategia
1.  Calcular el grado de cada nodo.
2.  Ordenar los nodos de mayor a menor grado.
3.  Aplicar la estrategia Greedy Básico siguiendo este orden.

### Análisis de Complejidad
-   **Tiempo**: $O(V \log V + V^2)$. El ordenamiento toma $V \log V$ y el coloreado posterior sigue siendo $O(V^2)$ en el peor caso.
-   **Espacio**: $O(V)$ para almacenar grados y orden.

---

## 3. Algoritmo DSATUR (Degree of Saturation)

### Funcionamiento
Es un algoritmo voraz dinámico. A diferencia de Welsh-Powell, el orden de los nodos no es estático, sino que se decide paso a paso basándose en la "saturación" de cada nodo.

### Estrategia
1.  **Saturación**: Se define como el número de colores *diferentes* usados por los vecinos colereados de un nodo.
2.  Inicialmente, elegir el nodo con mayor grado.
3.  En cada paso subsiguiente, elegir el nodo no coloreado con mayor grado de saturación. (Desempate por grado original).
4.  Asignar el color válido de menor costo.
5.  Actualizar la saturación de los vecinos.

### Análisis de Complejidad
-   **Tiempo**: $O(V^2)$. En cada paso (V veces), buscar el siguiente nodo maximizando saturación puede tomar $O(V)$ (o $O(\log V)$ con estructuras de datos avanzadas como montículos), y actualizar vecinos toma proporcional a su grado.
-   **Espacio**: $O(V^2)$ o $O(E)$ para mantener la información de adyacencia y saturación eficientemente.

---

## 4. Backtracking (Búsqueda Exacta)

### Funcionamiento
Es un algoritmo de fuerza bruta inteligente que explora sistemáticamente todas las posibles asignaciones de colores para encontrar la óptima global.

### Estrategia
1.  Asignar recursivamente colores a los nodos uno a uno.
2.  **Poda (Pruning)**: Si el costo actual parcial + una estimación mínima supera el mejor costo encontrado hasta ahora, se descarta esa rama completa. 
3.  **Optimización**: Se inicializa con una solución Greedy/DSATUR como "cota superior" (upper bound). Esto permite podar ramas mucho antes.

### Análisis de Complejidad
-   **Tiempo**: $O(K^V)$ en el peor caso. Es exponencial, lo que lo hace inviable para $N > 15-20$.
-   **Espacio**: $O(V)$ por la profundidad de la recursión.

---

## 5. Simulated Annealing (Recocido Simulado)

### Funcionamiento
Es una metaheurística probabilística inspirada en la termodinámica. Busca escapar de los "mínimos locales" (donde los algoritmos greedy se atascan) permitiendo movimientos "malos" (que aumentan el costo) temporalmente.

### Estrategia
1.  Comenzar con una solución inicial (ej. salida de DSATUR).
2.  **Perturbación**: Elegir un nodo al azar y cambiar su color a otro válido al azar.
3.  Calcular la diferencia de costo $\Delta E$.
4.  **Criterio de Aceptación**:
    -   Si $\Delta E < 0$ (mejora), aceptar siempre.
    -   Si $\Delta E > 0$ (empeora), aceptar con probabilidad $P = e^{-\Delta E / T}$.
5.  **Enfriamiento**: Reducir la temperatura $T$ gradualmente ($T = T \times \alpha$).

### Análisis de Complejidad
-   **Tiempo**: Depende del número de iteraciones configurado ($Iter$). Por iteración es muy rápido ($O(D_{max})$ para verificar validez y costo local). Total: $O(Iter \times D_{max})$.
-   **Espacio**: $O(V)$ para mantener la solución.

---

## 6. Tabu Search Repair (Búsqueda Tabú de Reparación)

### Funcionamiento
A diferencia de los anteriores que construyen una solución válida paso a paso, este enfoque comienza desde una solución **infactible** (asignando a cada nodo su color más barato absoluto) y trata de "reparar" los conflictos iterativamente.

### Estrategia
1.  **Inicio**: Asignar a cada nodo el color de costo mínimo absoluto, ignorando conflictos.
2.  **Ciclo de Reparación**:
    -   Identificar nodos en conflicto (vecinos con el mismo color).
    -   Evaluar movimientos: Cambiar el color de un nodo en conflicto.
    -   **Función Objetivo**: Minimizar $F = (W \times \text{Conflictos}) + \text{Costo Total}$. ($W$ es muy grande para priorizar factibilidad).
    -   **Lista Tabú**: Evitar revertir un cambio reciente para no caer en ciclos.

### Análisis de Complejidad
-   **Tiempo**: Depende de las iteraciones. Puede ser costoso si hay muchos conflictos iniciales.
-   **Espacio**: $O(V)$ para la lista tabú y asignaciones.

---

## Resumen Comparativo Final

| Algoritmo | Tipo | Complejidad | Calidad Solución | Nota |
| :--- | :--- | :--- | :--- | :--- |
| **Greedy Básico** | Voraz | $O(V^2)$ | Baja | Muy rápido, pero miope. |
| **Welsh-Powell** | Voraz | $O(V^2)$ | Media | Mejora ordenando nodos. |
| **DSATUR** | Voraz Dinámico | $O(V^2)$ | **Alta** | **Mejor relación calidad/tiempo**. |
| **Backtracking** | Exacto | $O(K^V)$ | **Óptima** | Solo para $N < 15$. |
| **Sim. Annealing**| Metaheurística| $O(Iter)$ | Muy Alta | Robusto para escapar mínimos locales. |
| **Tabu Repair** | Reparación | $O(Iter)$ | Variable | Útil cuando la factibilidad es difícil. |
