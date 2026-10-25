# ADR-0006 — OC2 Booch-inspired UML baseline

**Status:** Accepted for v2.0.1 documentation baseline.  
**Decision:** Keep version-controlled static domain, dynamic sequence, component, and deployment/boundary views under `docs/uml/`. Use PlantUML for UML notation, Mermaid for GitHub inline preview, and Graphviz for reproducible SVG/PNG architecture output. Annotate concrete code correspondence and planned links distinctly.  
**Rationale:** Enable review of abstraction, encapsulation, modularity, hierarchy, class responsibilities, ownership, dependency direction and runtime behavior without claiming nonexistent functionality.  
**Tradeoffs:** PlantUML rendering requires an optional local tool. Generated SVG/PNG are checked in for immediate viewing.  
**Verification:** Run `python3 scripts/check_architecture.py`, `swift test`, and Python unit tests. Device runtime and scientific validation remain separate release gates.
