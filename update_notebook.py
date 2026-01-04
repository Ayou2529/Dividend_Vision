import json

nb_path = 'dividend_vision_colab.ipynb'

try:
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # The target line to replace
    target_cmd = "%pip uninstall -y -q numpy diffusers transformers accelerate tokenizers safetensors opencv-python opencv-contrib-python"
    # The new line with expanded cleanup list
    new_cmd = "%pip uninstall -y -q numpy diffusers transformers accelerate tokenizers safetensors opencv-python opencv-contrib-python opencv-python-headless jax jaxlib tensorflow keras shap pytensor torchtune peft dopamine-rl sentence-transformers numba"

    found = False
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            new_source = []
            for line in cell['source']:
                if target_cmd in line:
                    # Check if already updated to avoid duplication if run twice
                    if "tensorflow" in line:
                        print("ℹ️  Notebook already updated.")
                        found = True
                        break
                    new_source.append(line.replace(target_cmd, new_cmd))
                    found = True
                else:
                    new_source.append(line)
            cell['source'] = new_source
        if found: break

    if found:
        with open(nb_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
        print("✅ Successfully updated uninstall command in notebook")
    else:
        print("❌ Could not find target command to replace (or already updated)")

except Exception as e:
    print(f"❌ Error: {e}")
