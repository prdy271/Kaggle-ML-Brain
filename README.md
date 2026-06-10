# Kaggle ML Brain
Kaggle ML Brain is an AI-powered machine learning experiment management platform that tracks runs, enforces schemas, compares experiments, generates AI analysis, and extracts reusable knowledge from past projects.

---

# Features

## Run Tracking

* Store machine learning experiment runs
* Organize runs by project
* Validate runs against project schemas
* Store datasets name, features used, parameter, metrics, artifacts, notes, and code

## Schema System

* Create schemas through the website
* Clone existing schemas and edit to create new schemas instanlty
* Enforce consistent experiment logging
* Support different model architectures within the same project

## Run Comparison

* Compare up to 4 runs simultaneously
* Automatic schema compatibility checking
* Side-by-side comparison table
* Best metric identification
* Difference highlighting
* Saved comparison history

## AI Analysis

* AI-powered comparison analysis using Groq
* Key findings
* Likely causes
* Recommended next experiments
* Warnings and risks

## Knowledge Extraction

* Analyze all runs belonging to a schema
* Discover parameter trends
* Discover feature trends
* Discover model trends
* Detect repeated issues
* Generate project-level knowledge summaries

# Groq Setup

Create a Groq account:

https://console.groq.com

Create an API key.

Open `main.py` and replace it with your actual key.
---

# Ngrok Setup

Create an ngrok account:

https://ngrok.com

Install ngrok.

Add your auth token:

```bash
ngrok config add-authtoken YOUR_TOKEN
```

Start a tunnel:

```bash
ngrok http 8000
```

Example output:

```text
https://example-name.ngrok-free.dev
```

This URL will be used inside Kaggle notebooks as:

```python
SERVER_URL="https://example-name.ngrok-free.dev"
```

---

# Running the Backend

Start FastAPI:

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

---

# Website Pages

## Home

```text
/
```

Landing page.

---

## Projects

```text
/projects
```

View all projects.

---

## Project Dashboard

```text
/runs/{project_name}
```

View project statistics and runs.

---

## Create Schema

```text
/create_schema_page/{project_name}
```

Create a schema using the website.

---

## Schemas

```text
/schemas_page/{project_name}
```

View all schemas.

---

## View Schema

```text
/schema/{project_name}/{schema_name}
```

View schema details.

---

## Clone Schema

```text
/clone_schema/{project_name}/{schema_name}
```

Create a modified copy of a schema.

---

## Run Profile

```text
/run/{project_name}/{run_id}
```

View a complete experiment run.

---

## Compare Runs

```text
/compare_page/{project_name}
```

Select runs for comparison.

---

## Comparison History

```text
/comparisons/{project_name}
```

View saved comparisons.

---

## Knowledge Extraction

```text
/generate_knowledge/{project_name}/{schema_name}
```

Generate schema-level knowledge.

---

## View Knowledge

```text
/knowledge/{project_name}/{schema_name}
```

View saved knowledge extraction.

---

# Kaggle Usage

Set your server URL:

```python
SERVER_URL="https://your-ngrok-url.ngrok-free.dev"
```

Use the provided `log_run()` function after training.

Example:

```python
log_run(
    server_url=SERVER_URL,
    project_name="MNIST",
    schema_name="RF_v1",
    ...
)
```

---

# Typical Workflow

1. Start FastAPI backend
2. Start ngrok tunnel
3. Create a project
4. Create a schema
5. Train a model in Kaggle
6. Log runs using `log_run()`
7. Compare runs
8. Generate AI analysis
9. Generate knowledge extraction
10. Use extracted knowledge to guide future experiments

---

# Storage Structure

```text
runs/
│
├── Project_A/
│   ├── run_1.json
│   ├── run_2.json
│   │
│   ├── schemas/
│   │   ├── schema1.json
│   │   └── schema2.json
│   │
│   ├── comparisons/
│   │   ├── comparison_1.json
│   │   └── comparison_2.json
│   │
│   └── knowledge/
│       └── schema1_knowledge.json
```

---

# Future Improvements

* I am still working on some limitations like only being able to compare run profiles which has the same schema structures.
* Automated data logging on the Kaggle notebook becomes difficult if the schema changes, as the params or architecture might change so will build an improvised version of that

---

# License

MIT License
