from fastapi import FastAPI
from pydantic import BaseModel
import json
import os
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi.responses import HTMLResponse,RedirectResponse
from typing import List
from fastapi import Form
from groq import Groq

GROQ_API_KEY="use your own key here , get it by signing into groq and generate a key"
app = FastAPI()

class Run(BaseModel):
    project_name: str
    schema_name: str
    dataset: Dict[str, Any] = {}
    model: Dict[str, Any] = {}
    features: Dict[str, Any] = {}
    architecture: Dict[str, Any] = {}
    parameters: Dict[str, Any] = {}
    metrics: Dict[str, Any] = {}
    derived_metrics: Dict[str, Any] = {}
    training_info: Dict[str, Any] = {}
    artifacts: Dict[str, Any] = {}
    leaderboard: Dict[str, Any] = {}
    notes: str = ""
    code: Dict[str, Any] = {}

class Schema(BaseModel):
    project_name:str
    schema_name:str
    dataset:Dict[str,str]={}
    model:Dict[str,str]={}
    features:Dict[str,str]={}
    architecture:Dict[str,str]={}
    parameters:Dict[str,str]={}
    metrics:Dict[str,str]={}
    derived_metrics:Dict[str,str]={}
    training_info:Dict[str,str]={}
    artifacts:Dict[str,str]={}
    leaderboard:Dict[str,str]={}

# ---------- STORAGE ----------
RUNS_DIR = "runs"
os.makedirs(RUNS_DIR, exist_ok=True)
# ---------- HOME ----------
@app.get("/",response_class=HTMLResponse)
def home():
    return """
    <html>
    <body>
    <h1>ML Tracker</h1>
    <p><a href="/projects">Projects</a></p>
    <p><a href="/runs">All Runs</a></p>
    <p><a href="/create_project_page">Create Project</a></p>
    </body>
    </html>
    """

@app.get("/create_schema_page/{project_name}",response_class=HTMLResponse)
def create_schema_page(project_name:str):

    return f"""
    <html>
    <body>

    <h1>Create Schema</h1>

    <form action="/create_schema_ui" method="post">

        <input type="hidden" name="project_name" value="{project_name}">

        <p>Schema Name</p>
        <input name="schema_name">

        <p>Dataset Fields</p>
        <textarea name="dataset" rows="5" cols="60"></textarea>

        <p>Model Fields</p>
        <textarea name="model" rows="5" cols="60"></textarea>

        <p>Features Fields</p>
        <textarea name="features" rows="5" cols="60"></textarea>

        <p>Architecture Fields</p>
        <textarea name="architecture" rows="5" cols="60"></textarea>

        <p>Parameter Fields</p>
        <textarea name="parameters" rows="5" cols="60"></textarea>

        <p>Metrics Fields</p>
        <textarea name="metrics" rows="5" cols="60"></textarea>

        <p>Derived Metrics Fields</p>
        <textarea name="derived_metrics" rows="5" cols="60"></textarea>

        <p>Training Info Fields</p>
        <textarea name="training_info" rows="5" cols="60"></textarea>

        <p>Artifact Fields</p>
        <textarea name="artifacts" rows="5" cols="60"></textarea>

        <p>Leaderboard Fields</p>
        <textarea name="leaderboard" rows="5" cols="60"></textarea>

        <br><br>

        <button type="submit">Create Schema</button>

    </form>

    </body>
    </html>
    
    """
def parse_section(text):
    result={}
    for line in text.splitlines():
        line=line.strip()
        if not line or ":" not in line:
            continue
        k,v=line.split(":",1)
        result[k.strip()]=v.strip()
    return result

@app.post("/create_schema_ui",response_class=HTMLResponse)
def create_schema_ui(
    project_name:str=Form(...),schema_name:str=Form(...),dataset:str=Form(""),model:str=Form(""),features:str=Form(""),architecture:str=Form(""),parameters:str=Form(""),
    metrics:str=Form(""),derived_metrics:str=Form(""),training_info:str=Form(""),artifacts:str=Form(""),leaderboard:str=Form("")):
    schema_data={
    "schema_name":schema_name,
    "dataset":parse_section(dataset),
    "model":parse_section(model),
    "features":parse_section(features),
    "architecture":parse_section(architecture),
    "parameters":parse_section(parameters),
    "metrics":parse_section(metrics),
    "derived_metrics":parse_section(derived_metrics),
    "training_info":parse_section(training_info),
    "artifacts":parse_section(artifacts),
    "leaderboard":parse_section(leaderboard)
    }

    schemas_dir=os.path.join(RUNS_DIR,project_name,"schemas")
    os.makedirs(schemas_dir,exist_ok=True)

    with open(os.path.join(schemas_dir,f"{schema_name}.json"),"w") as f:
        json.dump(schema_data,f,indent=4)

    return f"""
        <html>
        <body>

        <h2>Schema Created</h2>

        <p>{schema_name}</p>

        <p>
        <a href="/schema/{project_name}/{schema_name}">
        View Schema
        </a>
        </p>

        <p>
        <a href="/schemas_page/{project_name}">
        Back To Schemas
        </a>
        </p>

        </body>
        </html>
        """

@app.get("/create_project_page",response_class=HTMLResponse)
def create_project_page():

    return """
    <html>
    <body>

    <h1>Create Project</h1>

    <form action="/create_project" method="post">

        <input name="project_name" placeholder="Project Name">

        <button type="submit">Create</button>

    </form>

    </body>
    </html>
    """
@app.post("/create_project",response_class=HTMLResponse)
def create_project(project_name:str=Form(...)):

    os.makedirs(os.path.join(RUNS_DIR,project_name),exist_ok=True)

    return f"""
    <html>
    <body>

    <h2>Project Created</h2>

    <p>{project_name}</p>

    <a href="/projects">Go To Projects</a>

    </body>
    </html>
    """
# ----------CREATE SCHEMA------
@app.post("/create_schema")
def create_schema(schema: Schema):

    project_dir = os.path.join(
        RUNS_DIR,
        schema.project_name
    )

    schemas_dir = os.path.join(
        project_dir,
        "schemas"
    )

    os.makedirs(
        schemas_dir,
        exist_ok=True
    )

    schema_data={
    "schema_name":schema.schema_name,"dataset":schema.dataset,"model":schema.model,"features":schema.features,
    "architecture":schema.architecture,"parameters":schema.parameters,"metrics":schema.metrics,
    "derived_metrics":schema.derived_metrics,"training_info":schema.training_info,"artifacts":schema.artifacts,"leaderboard":schema.leaderboard
}

    schema_file = os.path.join(
        schemas_dir,
        f"{schema.schema_name}.json"
    )

    with open(schema_file, "w") as f:
        json.dump(
            schema_data,
            f,
            indent=4
        )

    return {
        "message": "schema created",
        "schema_name": schema.schema_name
    }

@app.get("/schemas_page/{project_name}",response_class=HTMLResponse)
def schemas_page(project_name:str):

    schemas_dir=os.path.join(RUNS_DIR,project_name,"schemas")

    if not os.path.exists(schemas_dir):
        return "No schemas"

    html=f"""
<html><body>

<a href="/">Home</a> |
<a href="/projects">Projects</a> |
<a href="/runs/{project_name}">Project Runs</a>

<h1>{project_name} Schemas</h1>

<p>
<a href="/create_schema_page/{project_name}">
Create New Schema
</a>
</p>
"""

    for file in os.listdir(schemas_dir):
        if file.endswith(".json"):
            schema=file.replace(".json","")
            html+=f"""
                <div style="border:1px solid #ddd;padding:10px;margin:10px">
                <h3><a href="/schema/{project_name}/{schema}">{schema}</a></h3>
                <p><a href="/clone_schema/{project_name}/{schema}">Clone Schema</a></p>
                <p><a href="/generate_knowledge/{project_name}/{schema}">Generate Knowledge</a></p>
                </div>
                """
    return html

@app.get("/schema/{project_name}/{schema_name}",response_class=HTMLResponse)
def show_schema(project_name:str,schema_name:str):

    file=os.path.join(RUNS_DIR,project_name,"schemas",f"{schema_name}.json")

    if not os.path.exists(file):
        return "Schema not found"

    with open(file) as f:
        schema=json.load(f)

    return f"""
<html><body>
<a href="/schemas_page/{project_name}">Back To Schemas</a>
<h1>{schema_name}</h1>
<a href="/">Home</a> |
<a href="/projects">Projects</a> |
<a href="/runs/{project_name}">Project Runs</a> |
<a href="/schemas_page/{project_name}">Schemas</a>
<p><a href="/clone_schema/{project_name}/{schema_name}">Clone Schema</a></p>
<p><a href="/knowledge/{project_name}/{schema_name}">View Saved Knowledge</a></p>
<p><a href="/generate_knowledge/{project_name}/{schema_name}">Generate Knowledge</a></p>
<pre>{json.dumps(schema,indent=4)}</pre>
</body></html>
"""

@app.get("/clone_schema/{project_name}/{schema_name}",response_class=HTMLResponse)
def clone_schema(project_name:str,schema_name:str):

    file=os.path.join(RUNS_DIR,project_name,"schemas",f"{schema_name}.json")

    if not os.path.exists(file):
        return "Schema not found"

    with open(file) as f:
        schema=json.load(f)

    def section_text(section):
        return "\n".join(f"{k}:{v}" for k,v in section.items())

    return f"""
    <html>
    <body>

    <h1>Clone Schema</h1>

    <form action="/create_schema_ui" method="post">

    <input type="hidden" name="project_name" value="{project_name}">

    <p>Schema Name</p>
    <input name="schema_name" value="{schema_name}_v2">

    <p>Dataset Fields</p>
    <textarea name="dataset" rows="5" cols="60">{section_text(schema["dataset"])}</textarea>

    <p>Model Fields</p>
    <textarea name="model" rows="5" cols="60">{section_text(schema["model"])}</textarea>

    <p>Features Fields</p>
    <textarea name="features" rows="5" cols="60">{section_text(schema["features"])}</textarea>

    <p>Architecture Fields</p>
    <textarea name="architecture" rows="5" cols="60">{section_text(schema["architecture"])}</textarea>

    <p>Parameter Fields</p>
    <textarea name="parameters" rows="5" cols="60">{section_text(schema["parameters"])}</textarea>

    <p>Metrics Fields</p>
    <textarea name="metrics" rows="5" cols="60">{section_text(schema["metrics"])}</textarea>

    <p>Derived Metrics Fields</p>
    <textarea name="derived_metrics" rows="5" cols="60">{section_text(schema["derived_metrics"])}</textarea>

    <p>Training Info Fields</p>
    <textarea name="training_info" rows="5" cols="60">{section_text(schema["training_info"])}</textarea>

    <p>Artifact Fields</p>
    <textarea name="artifacts" rows="5" cols="60">{section_text(schema["artifacts"])}</textarea>

    <p>Leaderboard Fields</p>
    <textarea name="leaderboard" rows="5" cols="60">{section_text(schema["leaderboard"])}</textarea>

    <br><br>

    <button type="submit">Save Schema</button>

    </form>

    </body>
    </html>
    """


@app.get("/run/{project_name}/{run_id}",response_class=HTMLResponse)
def show_run(project_name:str,run_id:int):

    file=os.path.join(RUNS_DIR,project_name,f"run_{run_id}.json")

    if not os.path.exists(file):
        return "Run not found"

    with open(file) as f:
        run=json.load(f)

    return f"""
<html>
<body>

<a href="/runs/{project_name}">Back To Project</a>

<h1>Run #{run['run_id']}</h1>

<h2>Project</h2>
<pre>{project_name}</pre>

<h2>Schema</h2>
<pre>{run.get("schema_name","")}</pre>

<h2>Dataset</h2>
<pre>{json.dumps(run.get("dataset",{}),indent=4)}</pre>

<h2>Model</h2>
<pre>{json.dumps(run.get("model",{}),indent=4)}</pre>

<h2>Features</h2>
<pre>{json.dumps(run.get("features",{}),indent=4)}</pre>

<h2>Architecture</h2>
<pre>{json.dumps(run.get("architecture",{}),indent=4)}</pre>

<h2>Parameters</h2>
<pre>{json.dumps(run.get("parameters",{}),indent=4)}</pre>

<h2>Metrics</h2>
<pre>{json.dumps(run.get("metrics",{}),indent=4)}</pre>

<h2>Derived Metrics</h2>
<pre>{json.dumps(run.get("derived_metrics",{}),indent=4)}</pre>

<h2>Training Info</h2>
<pre>{json.dumps(run.get("training_info",{}),indent=4)}</pre>

<h2>Artifacts</h2>
<pre>{json.dumps(run.get("artifacts",{}),indent=4)}</pre>

<h2>Leaderboard</h2>
<pre>{json.dumps(run.get("leaderboard",{}),indent=4)}</pre>

<h2>Notes</h2>
<pre>{run.get("notes","")}</pre>

<h2>Code</h2>
<pre>{json.dumps(run.get("code",{}),indent=4)}</pre>

</body>
</html>
"""



# -------- LIST SCHEMAS ---------
@app.get("/schemas/{project_name}")
def get_schemas(project_name: str):
    project_dir = os.path.join(RUNS_DIR,project_name)
    schemas_dir = os.path.join(project_dir,"schemas")
    if not os.path.exists(schemas_dir):
        return {"schemas": []}
    schemas = []
    for file in os.listdir(schemas_dir):
        if not file.endswith(".json"):
            continue
        schemas.append(file.replace(".json", ""))
    return {"project": project_name,"schemas": schemas}
# ---------- SAVE RUN ----------
def check_type(v,t):
    if t=="int": return isinstance(v,int)
    if t=="float": return isinstance(v,(int,float))
    if t=="str": return isinstance(v,str)
    if t=="list": return isinstance(v,list)
    if t=="dict": return isinstance(v,dict)
    return True
def validate_section(schema_section, run_section, section_name):
    errors=[]
    for k,t in schema_section.items():
        if k not in run_section:
            errors.append({"field":k,"error":"missing","section":section_name})
        elif not check_type(run_section[k],t):
            errors.append({"field":k,"error":"type_mismatch","expected":t,"received":type(run_section[k]).__name__,"section":section_name})
    return errors

@app.post("/save_run")
def save_run(run: Run):
    project_dir = os.path.join(RUNS_DIR, run.project_name)
    schema_file = os.path.join(project_dir,"schemas",f"{run.schema_name}.json")
    if not os.path.exists(schema_file):
        return {"error": "schema not found"}
    with open(schema_file) as f:
        schema = json.load(f)
    missing = []
    missing+=validate_section(schema["dataset"],run.dataset,"dataset")
    missing+=validate_section(schema["model"],run.model,"model")
    missing+=validate_section(schema["features"],run.features,"features")
    missing+=validate_section(schema["architecture"],run.architecture,"architecture")
    missing+=validate_section(schema["parameters"],run.parameters,"parameters")
    missing+=validate_section(schema["metrics"],run.metrics,"metrics")
    missing+=validate_section(schema["derived_metrics"],run.derived_metrics,"derived_metrics")
    missing+=validate_section(schema["training_info"],run.training_info,"training_info")
    missing+=validate_section(schema["artifacts"],run.artifacts,"artifacts")
    missing+=validate_section(schema["leaderboard"],run.leaderboard,"leaderboard")
    if missing:
        return {"error": "missing fields","fields": missing}
    os.makedirs(project_dir, exist_ok=True)
    existing = [f for f in os.listdir(project_dir) if f.startswith("run_") and f.endswith(".json")]
    run_id = len(existing) + 1
    data = run.model_dump()
    data["run_id"] = run_id
    data["timestamp"] = datetime.now().isoformat()
    with open(os.path.join(project_dir, f"run_{run_id}.json"), "w") as f:
        json.dump(data, f, indent=4)
    return {"message": "run saved","run_id": run_id}
@app.get("/runs", response_class=HTMLResponse)
def get_runs():
    runs = []
    for project in os.listdir(RUNS_DIR):
        project_dir = os.path.join(RUNS_DIR, project)
        if not os.path.isdir(project_dir):
            continue
        for file in os.listdir(project_dir):
            if not file.endswith(".json"):
                continue
            with open(os.path.join(project_dir, file)) as f:
                run = json.load(f)
            run["project_name"] = project
            runs.append(run)
    runs.sort(key=lambda x: x["run_id"])
    html = """
    <html>
    <head>
        <title>ML Runs</title>
        <style>
            body { font-family: Arial; padding: 20px; }
            .run { border: 1px solid #ddd; margin: 10px; padding: 10px; }
        </style>
    </head>
    <body>
        <h1>ML Experiment Runs</h1>
    """
    for r in runs:
        html += f"""
        <div class="run">
            <h3>Run #{r['run_id']}</h3>

            <p><b>Project:</b> {r['project_name']}</p>

            <p><b>Model:</b> {r['model']['name']}</p>

            <p><b>Test Accuracy:</b> {r['metrics'].get('test_accuracy')}</p>

            <p><b>Overfit Gap:</b> {r.get('derived_metrics', {}).get('overfit_gap')}</p>
        </div>
        """
    html += """
    </body>
    </html>
    """
    return html
@app.get("/projects", response_class=HTMLResponse)
def projects():
    projects = []
    for project in os.listdir(RUNS_DIR):
        project_dir = os.path.join(RUNS_DIR, project)
        if not os.path.isdir(project_dir):
            continue
        run_count = len([f for f in os.listdir(project_dir) if f.endswith(".json")])
        projects.append((project, run_count))
    html = """
    <html>
    <body>
    <h1>Projects</h1>
    """
    for project, count in projects:
        html+=f"""
        <p>
        <a href="/runs/{project}">{project}</a>
        ({count} runs)
        |
        <a href="/schemas_page/{project}">Schemas</a>
        |
        <a href="/comparisons/{project}">View Comparisons</a>
        </p>
        """
    html += """
    </body>
    </html>
    """
    return html

@app.get("/runs/{project_name}", response_class=HTMLResponse)
def project_runs(project_name: str):
    project_dir = os.path.join(
    RUNS_DIR,
    project_name
    )

    if not os.path.exists(project_dir):
        return f"Project '{project_name}' not found"
    runs = []

    for file in os.listdir(project_dir):

        if not file.endswith(".json"):
            continue

        with open(os.path.join(project_dir, file)) as f:
            runs.append(json.load(f))
    runs.sort(key=lambda x: x["run_id"])
    test_accs = []
    gaps = []

    for r in runs:

        acc = r["metrics"].get("test_accuracy")

        if acc is not None:
            test_accs.append(acc)

        gap = r.get(
            "derived_metrics",
            {}
        ).get("overfit_gap")

        if gap is not None:
            gaps.append(gap)
    best_acc = max(test_accs) if test_accs else None

    avg_acc = (
        round(sum(test_accs)/len(test_accs), 4)
        if test_accs else None
    )

    max_gap = max(gaps) if gaps else None
    html = f"""
    <html>
    <body>
    <a href="/">Home</a> |
    <a href="/projects">Projects</a> |
    <a href="/schemas_page/{project_name}">Schemas</a>
    <p><a href="/compare_page/{project_name}">Compare Runs</a></p>
    <p><a href="/schemas_page/{project_name}">View Schemas</a></p>
    <p><a href="/create_schema_page/{project_name}">Create Schema</a></p>
    <h1>{project_name}</h1>
    <a href="/projects">Back to Projects</a>
    <br><br>

    <p><b>Total Runs:</b> {len(runs)}</p>
    <p><b>Best Test Accuracy:</b> {best_acc}</p>
    <p><b>Average Test Accuracy:</b> {avg_acc}</p>
    <p><b>Most Overfit Gap:</b> {max_gap}</p>

    <hr>

"""
    for r in runs:
        html += f"""
        <div style="border:1px solid #ddd;padding:10px;margin:10px">

            <h3>
            <a href="/run/{project_name}/{r['run_id']}">
            Run #{r['run_id']}
            </a>
            </h3>

            <p><b>Model:</b> {r['model']['name']}</p>

            <p><b>Test Accuracy:</b>
            {r['metrics'].get('test_accuracy')}</p>

            <p><b>Overfit Gap:</b>
            {r.get('derived_metrics', {}).get('overfit_gap')}</p>

        </div>
        """
    html += "</body></html>"
    return html

def flatten(d,prefix=""):
    out={}
    for k,v in d.items():
        key=f"{prefix}.{k}" if prefix else k
        if isinstance(v,dict): out.update(flatten(v,key))
        else: out[key]=v
    return out
def best_of(runs,ids,section,field,mode="max"):
    vals=[]
    for i,r in enumerate(runs):
        v=r.get(section,{}).get(field)
        if isinstance(v,(int,float)): vals.append((ids[i],v))
    if not vals: return None
    return min(vals,key=lambda x:x[1]) if mode=="min" else max(vals,key=lambda x:x[1])
def make_ai_analysis(comparison):
    client=Groq(api_key=GROQ_API_KEY)
    ai_input={
        "best_summary":comparison.get("best_summary",{}),
        "differences":comparison.get("differences",{}),
        "plot_data":comparison.get("plot_data",{})
    }
    prompt=f"""
You are an expert ML experiment analyst.

Use only the comparison data below. Do not invent fields, models, datasets, or metrics.
Only recommend next experiments using fields that appear in the comparison data, unless you explicitly label them as general suggestions.

Return EXACTLY these sections:

# Key Findings

# Likely Causes

# Recommended Next Experiments

# Warnings / Risks

Comparison Data:
{json.dumps(ai_input,indent=2)}
"""
    r=client.chat.completions.create(model="llama-3.3-70b-versatile",messages=[{"role":"user","content":prompt}],temperature=0.2)
    return r.choices[0].message.content

@app.get("/compare/{project_name}/{run_ids}",response_class=HTMLResponse)
def compare_runs(project_name:str,run_ids:str,ai:int=0):
    ids=[int(x) for x in run_ids.split(",")]
    runs=[]
    for run_id in ids:
        file=os.path.join(RUNS_DIR,project_name,f"run_{run_id}.json")
        if not os.path.exists(file):
            return f"Run {run_id} not found"
        with open(file) as f:
            runs.append(json.load(f))
    if len(runs)>4:
        return "Maximum 4 runs allowed"
    schemas={r["schema_name"] for r in runs}
    if len(schemas)!=1:
        return "All runs must use same schema"
    flat_runs=[flatten(r) for r in runs]
    all_fields=sorted(set().union(*[set(r.keys()) for r in flat_runs]))

    table_data={}
    for field in all_fields:
        table_data[field]={}
        for i,r in enumerate(flat_runs):
            table_data[field][f"run_{ids[i]}"]=r.get(field,"")
    best_summary={
    "best_test_score":best_of(runs,ids,"metrics","test_accuracy","max"),
    "best_train_score":best_of(runs,ids,"metrics","train_accuracy","max"),
    "least_overfit":best_of(runs,ids,"derived_metrics","overfit_gap","min")
}
    differences={}
    for field,vals in table_data.items():
        unique={json.dumps(v,sort_keys=True) for v in vals.values()}
        if len(unique)>1: differences[field]=vals
    plot_data={}
    plot_data["test_accuracy"]={
    "x":ids,
    "y":[
        r.get("metrics",{}).get("test_accuracy")
        for r in runs
    ]
}
    plot_data["train_accuracy"]={
    "x":ids,
    "y":[
        r.get("metrics",{}).get("train_accuracy")
        for r in runs
    ]
}
    plot_data["overfit_gap"]={
    "x":ids,
    "y":[
        r.get("derived_metrics",{}).get("overfit_gap")
        for r in runs
    ]
}
    
    comparison_dir=os.path.join(RUNS_DIR,project_name,"comparisons")
    os.makedirs(comparison_dir,exist_ok=True)
    existing=[f for f in os.listdir(comparison_dir) if f.startswith("comparison_")]
    comparison_id=len(existing)+1
    ai_text=""
    comparison={

    "comparison_id":comparison_id,

    "project_name":project_name,

    "run_ids":ids,

    "schema_name":runs[0]["schema_name"],

    "created_at":datetime.now().isoformat(),

    "table_data":table_data,

    "best_summary":best_summary,

    "differences":differences,

    "plot_data":plot_data,

    "ai_analysis":ai_text
}
    if ai==1: 
        comparison["ai_analysis"]=make_ai_analysis(comparison)
    with open(os.path.join(comparison_dir,f"comparison_{comparison_id}.json"),"w") as f:
        json.dump(comparison,f,indent=4)
    def fmt_best(x):
        return "N/A" if x is None else f"Run #{x[0]} ({x[1]})"

    html=f"""
    <html><body>
    <a href="/runs/{project_name}">Back To Project</a>
    <h1>Comparison #{comparison_id}</h1>
    <p><b>Runs:</b> {ids}</p>
    <p><b>Schema:</b> {comparison["schema_name"]}</p>
    <h2>Summary</h2>
    <p><b>Best Test Score:</b> {fmt_best(best_summary["best_test_score"])}</p>
    <p><b>Best Train Score:</b> {fmt_best(best_summary["best_train_score"])}</p>
    <p><b>Least Overfit:</b> {fmt_best(best_summary["least_overfit"])}</p>
    <hr>
    <h2>Comparison Table</h2>
    <table border="1" cellpadding="6" cellspacing="0">
    <tr><th>Field</th>
    """
    for rid in ids: 
        html+=f"<th>Run #{rid}</th>"
        html+="</tr>"
    for field,vals in table_data.items():
        html+=f"<tr><td>{field}</td>"
    for rid in ids: 
        html+=f"<td>{vals.get(f'run_{rid}','')}</td>"
        html+="</tr>"
        html+="</table><hr><h2>Differences Only</h2><table border='1' cellpadding='6' cellspacing='0'><tr><th>Field</th>"
    for rid in ids: 
        html+=f"<th>Run #{rid}</th>"
        html+="</tr>"
    for field,vals in differences.items():
        html+=f"<tr><td>{field}</td>"
    for rid in ids:    
        html+=f"<td>{vals.get(f'run_{rid}','')}</td>"
        html+="</tr>"
        html+=f"""
    </table>
    <hr>
    <h2>AI Analysis</h2>
    <p>{comparison["ai_analysis"]}</p>
    </body></html>
    """
    return html

@app.get("/comparisons/{project_name}",response_class=HTMLResponse)
def comparisons_page(project_name:str):
    comp_dir=os.path.join(RUNS_DIR,project_name,"comparisons")
    if not os.path.exists(comp_dir): return "No comparisons found"
    html=f"<html><body><a href='/runs/{project_name}'>Back To Project</a><h1>{project_name} Comparisons</h1>"
    for file in os.listdir(comp_dir):
        if not file.startswith("comparison_") or not file.endswith(".json"): continue
        with open(os.path.join(comp_dir,file)) as f: comp=json.load(f)
        cid=comp["comparison_id"]
        html+=f"<div style='border:1px solid #ddd;padding:10px;margin:10px'><h3><a href='/comparison/{project_name}/{cid}'>Comparison #{cid}</a></h3><p><b>Runs:</b> {comp['run_ids']}</p><p><b>Schema:</b> {comp['schema_name']}</p><p><b>Created:</b> {comp['created_at']}</p></div>"
    html+="</body></html>"
    return html

@app.get("/comparison/{project_name}/{comparison_id}",response_class=HTMLResponse)
def show_comparison(project_name:str,comparison_id:int):
    file=os.path.join(RUNS_DIR,project_name,"comparisons",f"comparison_{comparison_id}.json")
    if not os.path.exists(file): return "Comparison not found"
    with open(file) as f: comparison=json.load(f)
    ids=comparison["run_ids"]; table_data=comparison["table_data"]; differences=comparison["differences"]; best_summary=comparison["best_summary"]
    def fmt_best(x): return "N/A" if x is None else f"Run #{x[0]} ({x[1]})"
    html=f"<html><body><a href='/comparisons/{project_name}'>Back To Comparisons</a><h1>Comparison #{comparison_id}</h1><p><b>Runs:</b> {ids}</p><p><b>Schema:</b> {comparison['schema_name']}</p><h2>Summary</h2><p><b>Best Test Score:</b> {fmt_best(best_summary['best_test_score'])}</p><p><b>Best Train Score:</b> {fmt_best(best_summary['best_train_score'])}</p><p><b>Least Overfit:</b> {fmt_best(best_summary['least_overfit'])}</p><hr><h2>Comparison Table</h2><table border='1' cellpadding='6' cellspacing='0'><tr><th>Field</th>"
    for rid in ids: html+=f"<th>Run #{rid}</th>"
    html+="</tr>"
    for field,vals in table_data.items():
        html+=f"<tr><td>{field}</td>"
        for rid in ids: html+=f"<td>{vals.get(f'run_{rid}','')}</td>"
        html+="</tr>"
    html+="</table><hr><h2>Differences Only</h2><table border='1' cellpadding='6' cellspacing='0'><tr><th>Field</th>"
    for rid in ids: html+=f"<th>Run #{rid}</th>"
    html+="</tr>"
    for field,vals in differences.items():
        html+=f"<tr><td>{field}</td>"
        for rid in ids: html+=f"<td>{vals.get(f'run_{rid}','')}</td>"
        html+="</tr>"
    html+=f"""
        <hr>
        <h2>AI Analysis</h2>
        <p>{comparison.get('ai_analysis','')}</p>
        <p><a href="/generate_ai_analysis/{project_name}/{comparison_id}">Generate AI Analysis</a></p>
        </body></html>
        """
    return html

@app.get("/compare_page/{project_name}",response_class=HTMLResponse)
def compare_page(project_name:str):
    project_dir=os.path.join(RUNS_DIR,project_name)
    if not os.path.exists(project_dir): return "Project not found"
    groups={}
    for file in os.listdir(project_dir):
        if not file.startswith("run_") or not file.endswith(".json"): continue
        with open(os.path.join(project_dir,file)) as f: r=json.load(f)
        schema=r.get("schema_name","N/A")
        if schema not in groups: groups[schema]=[]
        groups[schema].append(r)
    html=f"<html><body><a href='/runs/{project_name}'>Back To Project</a><h1>Compare Runs - {project_name}</h1>"
    for schema,runs in groups.items():
        runs.sort(key=lambda x:x["run_id"])
        html+=f"<h2>Schema: {schema}</h2><form action='/compare_selected/{project_name}' method='post'>"
        for r in runs:
            html+=f"<p><input type='checkbox' name='run_ids' value='{r['run_id']}'> Run #{r['run_id']} | Test: {r.get('metrics',{}).get('test_accuracy')} | Train: {r.get('metrics',{}).get('train_accuracy')}</p>"
        html+="<p><input type='checkbox' name='ai_analysis' value='yes'> Generate AI analysis now</p>"
        html+="<button type='submit'>Compare Selected</button></form><hr>"
    html+="</body></html>"
    return html

@app.post("/compare_selected/{project_name}")
def compare_selected(project_name:str,run_ids:List[int]=Form(...),ai_analysis:str=Form(None)):
    if len(run_ids)<2: return "Select at least 2 runs"
    if len(run_ids)>4: return "Maximum 4 runs allowed"
    ids=",".join(str(x) for x in run_ids)
    ai=1 if ai_analysis=="yes" else 0
    return RedirectResponse(url=f"/compare/{project_name}/{ids}?ai={ai}",status_code=303)

def format_ai_text(text):
    html=""
    for line in text.splitlines():
        line=line.strip()
        if not line: continue
        if line.startswith("# "): html+=f"<h2>{line[2:]}</h2>"
        elif line.startswith("- "): html+=f"<li>{line[2:]}</li>"
        else: html+=f"<p>{line}</p>"
    return html

@app.get("/generate_ai_analysis/{project_name}/{comparison_id}")
def generate_ai_analysis(project_name:str,comparison_id:int):
    file=os.path.join(RUNS_DIR,project_name,"comparisons",f"comparison_{comparison_id}.json")
    if not os.path.exists(file): return "Comparison not found"
    with open(file) as f: comparison=json.load(f)
    if not comparison.get("ai_analysis"): 
        comparison["ai_analysis"]=make_ai_analysis(comparison)
        with open(file,"w") as f: json.dump(comparison,f,indent=4)
    return RedirectResponse(url=f"/comparison/{project_name}/{comparison_id}",status_code=303)

def num_vals(runs,section,field):
    vals=[]
    for r in runs:
        v=r.get(section,{}).get(field)
        if isinstance(v,(int,float)): vals.append((r["run_id"],v))
    return vals

def summarize(vals,mode="max"):
    if not vals: return None
    chosen=max(vals,key=lambda x:x[1]) if mode=="max" else min(vals,key=lambda x:x[1])
    avg=round(sum(v for _,v in vals)/len(vals),4)
    return {"selected_run":chosen[0],"selected_value":chosen[1],"average":avg,"mode":mode}

def make_knowledge_analysis(knowledge):
    client=Groq(api_key=GROQ_API_KEY)
    ai_input={"metric_summary":knowledge.get("metric_summary",{}),"run_profiles":knowledge.get("run_profiles",[])}
    prompt=f"""
You are an expert ML experiment analyst.

Analyze all runs under one schema. Use only the data provided. Do not invent fields, metrics, models, or results.

Return EXACTLY these sections:

# Overall Summary
# Parameter Trends
# Feature Trends
# Model Trends
# Repeated Issues
# Best Approach So Far
# Suggestions for Next Runs

Rules:
- Mention low confidence if run_count < 5.
- Discuss parameter changes only if they appear in run_profiles.
- Discuss feature trends only if feature data appears.
- Discuss overfitting if overfit_gap exists.
- Be practical and specific.

Knowledge Data:
{json.dumps(ai_input,indent=2)}
"""
    r=client.chat.completions.create(model="llama-3.3-70b-versatile",messages=[{"role":"user","content":prompt}],temperature=0.2)
    return r.choices[0].message.content

@app.get("/generate_knowledge/{project_name}/{schema_name}",response_class=HTMLResponse)
def generate_knowledge(project_name:str,schema_name:str):
    project_dir=os.path.join(RUNS_DIR,project_name)
    if not os.path.exists(project_dir): return "Project not found"
    runs=[]
    for file in os.listdir(project_dir):
        if not file.startswith("run_") or not file.endswith(".json"): continue
        with open(os.path.join(project_dir,file)) as f: r=json.load(f)
        if r.get("schema_name")==schema_name: runs.append(r)
    if not runs: 
        return "No runs found for this schema"
    
    knowledge_dir=os.path.join(project_dir,"knowledge")
    os.makedirs(knowledge_dir,exist_ok=True)
    test_vals=num_vals(runs,"metrics","test_accuracy")
    train_vals=num_vals(runs,"metrics","train_accuracy")
    gap_vals=num_vals(runs,"derived_metrics","overfit_gap")



    metric_summary={
        "test_accuracy":summarize(test_vals,"max"),
        "train_accuracy":summarize(train_vals,"max"),
        "overfit_gap":summarize(gap_vals,"min")
    }
    run_profiles=[]
    for r in runs:
        run_profiles.append({
            "run_id":r["run_id"],
            "timestamp":r.get("timestamp"),
            "model":r.get("model",{}),
            "features":r.get("features",{}),
            "architecture":r.get("architecture",{}),
            "parameters":r.get("parameters",{}),
            "metrics":r.get("metrics",{}),
            "derived_metrics":r.get("derived_metrics",{}),
            "leaderboard":r.get("leaderboard",{}),
            "notes":r.get("notes","")
        })
    knowledge={
    "project_name":project_name,
    "schema_name":schema_name,
    "run_count":len(runs),
    "run_ids":[r["run_id"] for r in runs],
    "created_at":datetime.now().isoformat(),
    "metric_summary":metric_summary,
    "run_profiles":run_profiles,
    "ai_knowledge":""
}
    knowledge["ai_knowledge"]=make_knowledge_analysis(knowledge)
    with open(os.path.join(knowledge_dir,f"{schema_name}_knowledge.json"),"w") as f: json.dump(knowledge,f,indent=4)
    ai_html=format_ai_text(knowledge.get("ai_knowledge",""))
    html=f"""
    <html><body>
    <a href="/schema/{project_name}/{schema_name}">Back To Schema</a>
    <h1>Knowledge Extracted</h1>
    <p><b>Project:</b> {project_name}</p>
    <p><b>Schema:</b> {schema_name}</p>
    <p><b>Run Count:</b> {knowledge["run_count"]}</p>
    <p><b>Run IDs:</b> {knowledge["run_ids"]}</p>
    <h2>Metric Summary</h2>
    <pre>{json.dumps(knowledge["metric_summary"],indent=4)}</pre>
    <hr>
    <h1>AI Knowledge</h1>
    {ai_html}
    </body></html>
    """
    return html

@app.get("/knowledge/{project_name}/{schema_name}",response_class=HTMLResponse)
def show_knowledge(project_name:str,schema_name:str):
    file=os.path.join(RUNS_DIR,project_name,"knowledge",f"{schema_name}_knowledge.json")
    if not os.path.exists(file): return "Knowledge file not found"
    with open(file) as f: knowledge=json.load(f)
    ai_html=format_ai_text(knowledge.get("ai_knowledge",""))
    return f"""
    <html><body>
    <a href="/schema/{project_name}/{schema_name}">Back To Schema</a>
    <a href="/">Home</a> |
    <a href="/projects">Projects</a> |
    <a href="/runs/{project_name}">Project Runs</a> |
    <a href="/comparisons/{project_name}">Comparisons</a>
    <h1>Knowledge Extracted</h1>
    <p><b>Project:</b> {project_name}</p>
    <p><b>Schema:</b> {schema_name}</p>
    <p><b>Run Count:</b> {knowledge["run_count"]}</p>
    <p><b>Run IDs:</b> {knowledge["run_ids"]}</p>
    <h2>Metric Summary</h2>
    <pre>{json.dumps(knowledge["metric_summary"],indent=4)}</pre>
    <hr>
    <h1>AI Knowledge</h1>
    {ai_html}
    </body></html>
    """