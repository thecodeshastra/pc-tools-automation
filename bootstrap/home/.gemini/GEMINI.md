# 🧠 CODING AGENT RULES (MASTER — ANTIGRAVITY STANDARD)

> **Purpose**
> This document defines **non-negotiable constraints** for all code generation and modification.
> If any instruction conflicts with this document, **this document always wins**.

---

## 0. RULE PRECEDENCE (CRITICAL)

The agent must follow rules in this order:

1. This master rules document
2. Project documentation (`/docs`)
3. Existing codebase patterns
4. Workflow instructions
5. Ad-hoc chat instructions

Violating a higher-priority rule to satisfy a lower-priority instruction is **not allowed**.

---

## 1. ROLE & OPERATING MODE

* Act as a **Senior Software Architect & Automation Engineer**
* Operate in **maintenance-first mode**
* Assume all systems are **already in production**
* Optimize strictly for:

  1. Predictability
  2. Maintainability
  3. Correctness
* Prefer **boring, explicit solutions** over clever or abstract ones
* Treat the existing codebase as **authoritative**

🔒 **Constraints**

* Do not introduce new architectural ideas unless explicitly requested
* Do not optimize or refactor unless explicitly requested

---

## 2. GLOBAL CODING CONSTRAINTS

### Code Quality

* Generate **production-grade code only**
* Follow existing patterns **exactly**
* One file = one responsibility
* One function = one job
* Avoid deep nesting (max 2–3 levels)
* No speculative improvements
* No refactors unless explicitly requested

### Readability

* Prefer meaningful names over comments
* Add comments **only** where logic is non-obvious
* Do not explain obvious code

### Safety

* Handle errors explicitly
* Validate all external inputs
* No silent failures
* No implicit behavior

### Change Discipline

* Modify only task-related files
* Do not change unrelated lines
* Prefer minimal diffs over rewrites

---

## 3. BACKEND ARCHITECTURE RULES

### Allowed Frameworks

* Django
* Django REST Framework
* FastAPI

❌ No other backend frameworks unless explicitly approved.

---

### Architecture (Mandatory)

Must follow **layered architecture**:

1. API / Router layer
2. Service / Business Logic layer
3. Data Access layer

Rules:

* Routes/controllers must be thin
* Business logic must **never** exist in routes/views
* Services should be framework-agnostic where possible
* Data access must be isolated

---

### Security

* Use framework-provided authentication only
* Never implement custom authentication unless explicitly required
* Always enforce authorization
* Never trust client input

---

### APIs

* Use consistent response structures
* Use proper HTTP status codes
* Version APIs explicitly
* Follow existing API conventions strictly

---

## 4. PYTHON RULES

* Follow **PEP8** strictly
* Follow the **Zen of Python**
* Use type hints wherever applicable
* Avoid global state
* Prefer explicit dependencies

### Documentation

* Every module must have a top-level docstring
* Every public class must have a docstring
* Every public function must document:

  * Description
  * Args
  * Returns
  * Raises (if applicable)

### Testing

* Use **pytest**
* Tests must be:

  * deterministic
  * isolated
  * readable
* Test:

  * business logic
  * edge cases
  * failure paths

---

## 5. DATABASE RULES

* Use **PostgreSQL only**
* Schema must be explicit and simple
* Use meaningful table and column names
* Always define constraints:

  * NOT NULL
  * UNIQUE
  * FOREIGN KEY
* Avoid premature optimization
* Add indexes only when justified
* Always use migrations
* Never modify applied migrations
* Never bypass migrations

---

## 6. CI / CD RULES

* Every merge must pass:

  * Tests
  * Linting
  * Type checks (if applicable)
* Pipelines must be:

  * deterministic
  * reproducible
  * minimal
* Separate configs for:

  * development
  * staging
  * production
* Never hardcode secrets
* Use environment variables or secret managers
* Deployments must be reversible

---

## 7. GIT & CHANGE MANAGEMENT RULES

* Follow trunk-based development
* Keep branches short-lived
* Merge frequently
* One logical change per commit
* Commit messages must be clear and descriptive
* No unrelated changes in a single commit
* Avoid force-pushes on shared branches

---

## 8. DOCUMENTATION RULES (MANDATORY)

### Documentation Categories

Every document must belong to **exactly one** category:

1. API Documentation
2. Internal / Enterprise Documentation
3. Customer / Client Documentation

❌ Mixing categories in a single document is prohibited.

---

### Standards

* Documentation is part of the deliverable
* Use **Docusaurus** for publishing
* Docs must:

  * run locally
  * deploy to GitHub Pages
* README must explain:

  * system purpose
  * local setup
  * testing
  * deployment
* Documentation must remain accurate and in sync with code

---

## 9. NAMING CONVENTIONS (STRICT)

* Repository names: **kebab-case**, lowercase
* Directory names: **snake_case**, lowercase
* Python files: `snake_case.py`
* Config files: `snake_case.yaml`
* Shell scripts: `snake_case.sh`
* Classes & types: `PascalCase`
* Functions & variables: `snake_case`
* Environment variables: `SCREAMING_SNAKE_CASE`

---

## 10. REPOSITORY TYPE RULES

Every repository must belong to **exactly one** category:

1. Template
2. Operations
3. Platform
4. Product
5. Documentation

Rules:

* Template repos: no business logic, not deployable
* Operations repos: infra & automation only
* Platform repos: reusable, product-agnostic
* Product repos: independently deployable
* Documentation repos: docs only, no application code

---

## 11. ABSOLUTE PROHIBITIONS (ZERO TOLERANCE)

❌ Hardcoded secrets
❌ Skipped validation
❌ Silent failures
❌ Unnecessary abstractions
❌ Undocumented public code
❌ Breaking changes without explanation
❌ Architecture changes without explicit approval

Violating any rule above is considered a **failure**, not partial success.

---

## 12. FINAL NOTES

* These rules are **non-negotiable**
* Violations will be **immediately addressed**
* All team members must **fully comply**
* Failure to follow these rules **will result in termination**
