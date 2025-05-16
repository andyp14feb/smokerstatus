from flask import Flask, render_template, request
import importlib
import os
from dotenv import load_dotenv
import sys

import pandas as pd
import random
from werkzeug.datastructures import MultiDict

print("---------------------------------------------------------------")
print("---------------------------------------------------------------")
print("Current virtual environment path:", sys.prefix)
print("VIRTUAL_ENV:", os.environ.get("VIRTUAL_ENV", "Not in a virtual environment"))
load_dotenv()
print("FLASK_ENV:", os.getenv("FLASK_ENV"))
print("---------------------------------------------------------------")
print("---------------------------------------------------------------")

app = Flask(__name__)
model_dir = 'models'

def get_models():
    return [d for d in os.listdir(model_dir)
            if os.path.isdir(os.path.join(model_dir, d))]

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    models = get_models()
    prediction = None

    if request.method == 'POST':
        model_name = request.form.get('model')
        try:
            mod = importlib.import_module(f'{model_dir}.{model_name}.modelrun')
            importlib.reload(mod)
            # panggil fungsi modelflow yang menerima form data
            prediction = mod.runflow(request.form)
        except (ModuleNotFoundError, AttributeError) as e:
            prediction = f"Error loading model '{model_name}': {e}"    
    return render_template(
    'index.html',
    models=models,
    prediction=prediction,
    request_form=request.form
    )



@app.route('/simulate')
def simulate_submission():
    # Load example data from static ; will ambil 1 row from train data to be used as isian form
    data_path = os.path.join('static', 'data_contoh.csv')
    df = pd.read_csv(data_path)
    #nama kolom disamakan with text box names / variables in index.html form 
    namaKolom=  ['id','age',
                        'height',
                        'weight',
                        'waist',
                        'eyesight_left',
                        'eyesight_right',
                        'hearing_left',
                        'hearing_right',
                        'systolic',
                        'relaxation',
                        'fasting_blood_sugar',
                        'cholesterol',
                        'triglyceride',
                        'hdl',
                        'ldl',
                        'hemoglobin',
                        'urine_protein',
                        'serum_creatinine',
                        'ast',
                        'alt',
                        'gtp',
                        'dental_caries','smoking']
    # print(df.columns)
    # print(namaKolom)
    df.columns=namaKolom
    # print(df.columns)
    # print(df[['hearing_left','hearing_right','dental_caries']])

    # Select one random row
    random_row = df.sample(n=1).iloc[0]

    # Extract smoking (target) value
    true_smoking = random_row['smoking']

    # Drop id and smoking columns
    input_data = random_row.drop(['id', 'smoking'])

    # Convert to dict of str (Flask form values must be string)
    # form_data = {k: str(v) for k, v in input_data.items()}
    form_data = {k: str(int(v)) 
                    if str(v).strip().isdigit() or 
                    str(v).strip().endswith('.0') 
                    else str(v).strip()
                for k, v in input_data.items()}

    # Randomly select a model from available list
    models = get_models()
    selected_model = random.choice(models)
    form_data['model'] = selected_model

    # Save smoking value (optional for future use) 
    print("=================================")
    print("True smoking status:", true_smoking)
    print("=================================")

    # Wrap in MultiDict
    simulated_data = MultiDict(form_data)

    # Run prediction
    prediction = None
    try:
        mod = importlib.import_module(f'{model_dir}.{selected_model}.modelrun')
        importlib.reload(mod)
        prediction = mod.runflow(simulated_data)
    except (ModuleNotFoundError, AttributeError) as e:
        prediction = f"Error loading model '{selected_model}': {e}"

    return render_template(
        'index.html',
        models=models,
        prediction=prediction,
        request_form=simulated_data
    )

if __name__ == '__main__':
    app.run(debug=True)
