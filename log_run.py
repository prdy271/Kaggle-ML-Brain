#This will go in the kaggle noteboook and run it right after the training is complete

import os,json,time,requests

def log_run(
    server_url,project_name,schema_name,dataset,model,features,
    architecture,parameters,metrics,derived_metrics,training_info,artifacts,leaderboard,notes="",code={}):

    dataset_names=[]

    if os.path.exists("/kaggle/input"):
        dataset_names=os.listdir("/kaggle/input")

    dataset["dataset_names"]=dataset_names

    payload={
        "project_name":project_name,
        "schema_name":schema_name,

        "dataset":dataset,
        "model":model,
        "features":features,

        "architecture":architecture,
        "parameters":parameters,

        "metrics":metrics,
        "derived_metrics":derived_metrics,

        "training_info":training_info,
        "artifacts":artifacts,

        "leaderboard":leaderboard,

        "notes":notes,
        "code":code
    }

    r=requests.post(
        f"{server_url}/save_run",
        json=payload
    )

    print(r.json())