# ⚡️ Knowledge: Ingeniería Eléctrica (Maestría)

*Compendio de fórmulas críticas para certificación y diseño (Luxemburgo).*

---

## 📐 1. Fórmulas de Potencia (AC)
El corazón del diseño eléctrico. Mantener $\cos\phi > 0.9$.

| Tipo | Potencia Activa ($P$) [W] | Potencia Aparente ($S$) [VA] |
| :--- | :--- | :--- |
| **Monofásico** | $V \cdot I \cdot \cos\phi$ | $V \cdot I$ |
| **Trifásico** | $\sqrt{3} \cdot U \cdot I \cdot \cos\phi$ | $\sqrt{3} \cdot U \cdot I$ |

## ⚙️ 2. Motores Eléctricos
Cálculo de corriente nominal ($I_n$) para protecciones:
$$I_n = \frac{P_{mec}}{\sqrt{3} \cdot U \cdot \cos\phi \cdot \eta}$$
*Donde $\eta$ es la eficiencia del motor.*

## 🛡️ 3. Dimensionamiento de Cables (Sección $S$)
Para cumplir con caída de tensión máxima ($\Delta u$) del 3%:
$$S = \frac{\sqrt{3} \cdot L \cdot P}{\gamma \cdot \Delta u \cdot U} \quad (\text{Trifásico})$$
*   $\gamma_{Cu} \approx 56$ (Conductividad del cobre).

## ⚠️ 4. Las 5 Reglas de Oro (Seguridad VDE)
1.  **Desconectar** (Corte visible).
2.  **Bloquear** (Enclavamiento).
3.  **Verificar** (Ausencia de tensión).
4.  **Poner a Tierra** y en cortocircuito.
5.  **Señalizar** la zona.

---
*Fuente: Manual de Referencia Brevet de Maîtrise.*
