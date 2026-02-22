"""Showcase various Mermaid diagram types."""

import mermaido

diagrams = {
    "flowchart": """
flowchart LR
    A[Start] --> B{Check}
    B -->|Pass| C[Continue]
    B -->|Fail| D[Retry]
    D --> B
""",
    "sequence": """
sequenceDiagram
    participant U as User
    participant S as Server
    participant DB as Database
    U->>S: Request
    S->>DB: Query
    DB-->>S: Result
    S-->>U: Response
""",
    "class": """
classDiagram
    Animal <|-- Duck
    Animal <|-- Fish
    Animal: +int age
    Animal: +isMammal() bool
    Duck: +swim()
    Fish: +canEat() bool
""",
    "state": """
stateDiagram-v2
    [*] --> Idle
    Idle --> Processing: submit
    Processing --> Done: success
    Processing --> Error: failure
    Error --> Idle: retry
    Done --> [*]
""",
    "er": """
erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ LINE_ITEM : contains
    PRODUCT ||--o{ LINE_ITEM : "is in"
""",
    "gantt": """
gantt
    title Project Plan
    dateFormat YYYY-MM-DD
    section Design
        Wireframes :a1, 2025-01-01, 7d
        Mockups    :a2, after a1, 5d
    section Dev
        Frontend   :b1, after a2, 14d
        Backend    :b2, after a2, 14d
""",
    "pie": """
pie title Pets
    "Dogs" : 40
    "Cats" : 30
    "Birds" : 20
    "Fish" : 10
""",
    "gitgraph": """
gitGraph
    commit
    branch develop
    checkout develop
    commit
    commit
    checkout main
    merge develop
    commit
""",
}

for name, markup in diagrams.items():
    mermaido.render(markup, f"{name}.png")
    print(f"wrote {name}.png")
