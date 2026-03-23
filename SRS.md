# Software Requirements Specification (SRS)

## Project Title

**Synthesis- Ai Research Paper Generator**

## Version

v1.0

## Prepared For

Antigravity AI

## Prepared By

Nishant Awasthi

---

## 1. Introduction

### 1.1 Purpose

The purpose of this document is to provide a **complete, unambiguous, and developer-ready Software Requirements Specification (SRS)** for the *Research Paper Maker* platform. This document is intended to be directly handed over to the development team for implementation.

The platform aims to assist **students, researchers, academicians, and professionals** in creating high-quality research papers with AI-assisted workflows while ensuring **academic integrity, citation accuracy, plagiarism awareness, and structured research methodology**.

---

### 1.2 Scope of the System

The Research Paper Maker (RPM) is a **web-based AI-powered research assistant** that helps users:

* Generate structured research papers
* Assist in literature review
* Manage citations and references
* Check grammar, clarity, and formatting
* Detect plagiarism (awareness, not bypass)
* Export papers in standard academic formats

The system is **research-supportive**, not a plagiarism generator.

---

### 1.3 Definitions, Acronyms, Abbreviations

| Term | Meaning                                           |
| ---- | ------------------------------------------------- |
| RPM  | Research Paper Maker                              |
| AI   | Artificial Intelligence                           |
| DOI  | Digital Object Identifier                         |
| SRS  | Software Requirements Specification               |
| NLP  | Natural Language Processing                       |
| APA  | American Psychological Association                |
| IEEE | Institute of Electrical and Electronics Engineers |

---

## 2. Overall Description

### 2.1 Product Perspective

RPM is a **standalone SaaS platform** that integrates:

* AI/NLP models
* Research databases (metadata-level)
* Document formatting engines
* Citation management systems

It will be accessible via modern web browsers and scalable for future mobile app integration.

---

### 2.2 User Classes and Characteristics

| User Type           | Description                           | Technical Level       |
| ------------------- | ------------------------------------- | --------------------- |
| Student             | Undergraduate / Postgraduate students | Basic–Intermediate    |
| Research Scholar    | PhD / MS researchers                  | Intermediate–Advanced |
| Professor           | Academic mentors                      | Intermediate          |
| Industry Researcher | Corporate R&D                         | Advanced              |
| Admin               | Platform management                   | Advanced              |

---

### 2.3 Operating Environment

* Platform: Web-based
* Frontend: React / Next.js
* Backend: Node.js / Python (FastAPI)
* Database: PostgreSQL + Vector DB
* AI Models: LLM + Research-specific embeddings
* Cloud: AWS / GCP / Azure

---

### 2.4 Design Constraints

* Must not generate plagiarized content intentionally
* Must respect academic ethics
* GDPR-compliant user data handling
* Free-tier limitations

---

## 3. System Features (Functional Requirements)

### 3.1 User Authentication & Profile Management

**Features:**

* Email/Google login
* Academic profile setup
* Research interest tagging

**Functional Requirements:**

* FR-1: System shall allow users to create accounts
* FR-2: System shall store academic preferences

---

### 3.2 Research Topic Ideation

**Features:**

* Topic suggestion based on domain
* Novelty score estimation

**Workflow:**

1. User enters domain + keywords
2. AI suggests multiple research topics
3. User selects one

---

### 3.3 Research Paper Structure Generator

**Supported Sections:**

* Abstract
* Introduction
* Literature Review
* Methodology
* Results
* Discussion
* Conclusion
* References

**FRs:**

* FR-10: System shall generate section-wise outlines
* FR-11: User can edit each section manually

---

### 3.4 Literature Review Assistant

**Features:**

* Paper summarization
* Keyword extraction
* Citation suggestion

**Constraints:**

* No full-paper piracy
* Metadata + abstract-based analysis only

---

### 3.5 Citation & Reference Manager

**Supported Formats:**

* APA
* IEEE
* MLA
* Chicago

**FRs:**

* FR-20: System shall auto-generate citations
* FR-21: System shall manage reference list

---

### 3.6 AI Writing Assistant (Ethical Mode)

**Features:**

* Sentence refinement
* Academic tone conversion
* Clarity improvement

**Explicit Limitation:**

* Cannot rewrite content to bypass plagiarism

---

### 3.7 Plagiarism Awareness Module

**Features:**

* Similarity score indication
* Highlight overlapping phrases

**Note:**

* Awareness, not evasion

---

### 3.8 Formatting & Export

**Export Options:**

* PDF
* DOCX
* LaTeX

**FRs:**

* FR-30: System shall export formatted papers

---

## 4. User Workflow

### 4.1 High-Level User Flow

1. User registers/logs in
2. Selects research domain
3. Generates topic ideas
4. Chooses structure
5. Builds sections iteratively
6. Adds citations
7. Reviews plagiarism score
8. Exports final paper

---

## 5. Data Workflow

### 5.1 Input Data

* User prompts
* Research keywords
* Uploaded drafts

### 5.2 Processing

* NLP preprocessing
* Semantic embeddings
* Section-wise generation

### 5.3 Output Data

* Structured paper
* Citation metadata
* Exported documents

---

## 6. Non-Functional Requirements

### 6.1 Performance

* Response time < 5 seconds per section

### 6.2 Scalability

* Horizontal scaling for AI workloads

### 6.3 Security

* Encrypted data storage
* Secure authentication

### 6.4 Usability

* Minimal academic learning curve

---

## 7. Free vs Paid Model (As Discussed)

### Free Tier

* Limited papers/month
* Limited AI credits
* Basic formatting

### Paid Tier (Future)

* Unlimited drafts
* Advanced plagiarism insights
* Collaboration tools

---

## 8. Future Enhancements

* Multi-author collaboration
* Journal-specific formatting
* Reviewer response generator
* Research dataset analysis

---

## 9. Assumptions & Dependencies

* Internet connectivity required
* AI model availability
* External citation APIs

---

## 10. Conclusion

This SRS defines a **research-first, ethics-aligned, developer-ready blueprint** for building the Research Paper Maker platform usable by **all researchers globally**, including students, scholars, and industry professionals.

---

**END OF DOCUMENT**

---

## UML & SYSTEM DIAGRAMS

### 1. Use Case Diagram (Mermaid)

```mermaid
usecaseDiagram

actor Researcher
actor Supervisor
actor System
actor "Open-Access Research Sources" as OARS
actor "Google Colab" as Colab
actor Internet

System --> (Continuously Fetch Latest Research Papers)
OARS --> (Continuously Fetch Latest Research Papers)
System --> (Generate Embeddings)
System --> (Update Vector Database)

Researcher --> (Submit Original Research Idea)
Researcher --> (Discover Similar Existing Research)
Researcher --> (Refine Research Novelty)

Researcher --> (Design Experiment via Chat)
Researcher --> (Generate Google Colab Notebook)
Colab --> (Execute Experiment)

Researcher --> (Upload Existing Notebook)
Researcher --> (Upload Experimental Results)
Researcher --> (Validate Experimental Results)

System --> (Proceed to Paper Writing)
System --> (Warn to Recheck Results)

Researcher --> (Draft Paper Sections)
Researcher --> (Continuous Reasoning & Feedback)
Researcher --> (Check Cross-Section Consistency)

Researcher --> (Retrieve Citations)
Internet --> (Retrieve Citations)
Researcher --> (Validate References)

Researcher --> (Check Reproducibility)
Researcher --> (Generate Ethics & AI Disclosure)
Researcher --> (Submission Readiness Check)

Supervisor --> (Review Research Progress)
Supervisor --> (Provide Feedback)
```

---

### 2. Sequence Diagram (End-to-End Research Flow)

```mermaid
sequenceDiagram
participant R as Researcher
participant UI as Web Interface
participant AI as AI Engine
participant VDB as Vector DB
participant NET as Internet
participant COL as Google Colab

R->>UI: Submit Research Idea
UI->>AI: Process Idea
AI->>VDB: Similarity Search
VDB-->>AI: Related Papers
AI-->>UI: Novelty Feedback

R->>UI: Design Experiment (Chat)
UI->>AI: Generate Experiment Plan
AI-->>UI: Experiment Steps

R->>UI: Generate Colab Notebook
UI->>AI: Create Notebook
AI-->>COL: Deploy Notebook
COL-->>R: Execution Results

R->>UI: Upload Results
UI->>AI: Validate Results
AI-->>UI: Valid / Warning

R->>UI: Draft Paper Sections
UI->>AI: Assist Writing
AI->>NET: Fetch Citations
NET-->>AI: References
AI-->>UI: Final Draft
```

---

### 3. Data Flow Diagram (DFD – Level 0)

```mermaid
graph TD
Researcher -->|Idea / Results| System
System -->|Draft Paper| Researcher
System -->|Citations| Internet
Internet -->|References| System
System -->|Experiments| GoogleColab
GoogleColab -->|Results| System
System -->|Papers| VectorDB
```

---

### 4. Data Flow Diagram (DFD – Level 1)

```mermaid
graph TD

R[Researcher]
P1[Idea Analysis Module]
P2[Similarity Detection]
P3[Experiment Generator]
P4[Result Validation]
P5[Paper Drafting Engine]
P6[Citation Engine]

VDB[(Vector Database)]
NET[(Internet)]
COL[(Google Colab)]

R --> P1
P1 --> P2
P2 --> VDB
VDB --> P2
P2 --> R

R --> P3
P3 --> COL
COL --> P4
P4 --> R

R --> P5
P5 --> P6
P6 --> NET
NET --> P6
P6 --> P5
P5 --> R
```

---

## User Workflow (End-to-End)

### Step 1: Authentication

* User registers or logs in using email / OAuth
* Role assigned: Researcher (default)

### Step 2: Research Topic Submission

* User enters:

  * Research title / topic
  * Domain / niche
  * Optional abstract or problem statement

### Step 3: Similar Work Discovery

* System performs similarity search using Vector DB
* Displays:

  * Closely related existing papers
  * Overlap score / novelty indicator
* User refines idea if needed

### Step 4: AI-Assisted Draft Generation

* LLM generates an initial research paper draft:

  * Abstract
  * Introduction
  * Related Work
  * Methodology (placeholder)
  * Conclusion (draft)

### Step 5: Experiment Result Integration

User chooses one of the following:

* Upload experimental results as text (metrics, tables)
* Upload Jupyter / Colab notebook
* Generate a Google Colab notebook via chat

  * Upload dataset
  * Define model / experiment via chat

### Step 6: Experiment Validation

* System executes / analyzes results
* If valid:

  * Results integrated into paper
* If inconsistent:

  * Warning shown: "Please recheck results"

### Step 7: Iterative Section Building

* User builds sections iteratively via chat:

  * Methodology
  * Experiments
  * Results
  * Discussion
* Cross-section consistency checks applied

### Step 8: Citation Management

* System fetches citations via internet + RAG
* User reviews and approves references
* Citations auto-formatted (APA / IEEE / ACM)

### Step 9: Plagiarism & Ethics Review

* Plagiarism score generated
* AI disclosure & ethics statement suggested

### Step 10: Editing & Refinement

* User edits:

  * Via chat (instruction-based)
  * Via manual typing (editor)

### Step 11: Export

* Export LaTeX source code
* User can manually edit LaTeX
* Final export as PDF
