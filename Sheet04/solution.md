### A4.1: Kontextfreie Grammatik (1P)

Berechnen die die _First-_ und _Follow-Mengen_ der Grammatik.

Zeigen Sie, dass die Grammatik LL(1) ist.

| Nicht-Terminal | First | Follow |
| -------------- | ----- | ------ |
| S              | {1,3} | {1,3$} |
| A              | {2,ϵ} | {1,3}  |

Die Grammatik ist LL(1)

## A4.6: Recherche und Diskussion

### Open-Source-Projekte mit Handgeschriebenen Recursive-Descent-Parsern

#### 1. Go Compiler (golang/go)

- **Gründe**:
  - Volle Kontrolle über Parse-Fehlerbehandlung und Fehlermeldungen
  - Performance-optimiert für häufige Compile-Vorgänge
  - Einfaches Debugging und Verständnis des Parser-Verhaltens
  - Go-native Implementation ohne externe Dependencies

#### Rust Compiler (rust-lang/rust)

- **Gründe**:
  - Sehr detaillierte, nutzerfreundliche Fehlermeldungen mit Suggestions
  - Granulare Kontrolle über den Parse-Prozess
  - Integration mit dem Error-Recovery-System
  - Minimale Runtime-Overhead für Performance-kritische Compilations

#### Google Protocol Buffers

- **Gründe**:
  - Maximale Performance und Kontrolle
  - Minimale Abhängigkeiten
  - Kritisch für High-Performance-Systeme

#### Node.js / V8 (JavaScript Engine)

- **Gründe**:
  - Extreme Performance-Anforderungen
  - Complex Error-Recovery für Live-Debugging
  - Speicher- und Geschwindigkeitsoptimierungen

### Vor und Nachteile von ANTLR

Die großen, produktiven Compiler-Projekte (Go, Rust, Swift, Kotlin) verwenden handgeschriebene Parser, weil:

- Sie täglich millionenfach aufgerufen werden
- Sie sind stabil und ändern sich selten fundamental

ANTLR ist ideal für:

- Lernzwecke und akademische Projekte
- Schnelle Prototyping
- Kleine bis mittlere Systeme

Aber nicht für Produktions-Compiler, wo Kontrolle und Performance essenziell sind.
