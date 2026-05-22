import google.generativeai as genai

genai.configure(api_key="AIzaSyAH4hM6_MW1-gqm1yerpGtzL5Mxi3_DyaM")

for model in genai.list_models():
    methods = model.supported_generation_methods

    if "generateContent" in methods:
        print(model.name)
        print(methods)
        print("-" * 50)