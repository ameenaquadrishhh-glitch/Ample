from roboflow import Roboflow

rf = Roboflow(api_key="ldExyoBH4BQc4U9kWCQ1")
project = rf.workspace("roboflow-universe-projects").project("fight-detection-tilhr")
version = project.version(3)
model = version.model

print("Model ready!")