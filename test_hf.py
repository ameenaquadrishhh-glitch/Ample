from huggingface_hub import list_models

print("Hugging Face connection works!")
models = list(list_models(limit=5))

for model in models:
    print(model.id)