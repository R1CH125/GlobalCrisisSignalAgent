# System Architecture

```mermaid
flowchart LR

A[Social APIs]
B[News APIs]
C[Environmental APIs]

A --> D[Signal Normalization]
B --> D
C --> D

D --> E[Anomaly Detection]

E --> F[AI Reasoning Layer]

F --> G[Crisis Scoring Engine]

G --> H[Alert Dispatcher]

H --> I[Dashboard]
```
