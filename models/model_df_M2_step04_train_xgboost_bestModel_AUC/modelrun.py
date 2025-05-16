from flask import request
import pandas as pd
import pickle
import os

def capping_features_based_on_threshold(df, thresholds_df):
    for _, row in thresholds_df.iterrows():
        col = row['feature']
        min_val = row['min']
        max_val = row['max']
                
        df[col] = df[col].clip(lower=min_val, upper=max_val)
    
    return df
#--------------------------------------------------------------------------

def add_combined_features(dfnya):
    #kurus/gemuk (ukuran kegemukan)
    dfnya['new_bmi'] = (dfnya['weight_kg'] / (dfnya['height_cm'] ** 2))*100

    #lingkarpinggang (ukuran perut)
    dfnya['new_waist_height_ratio']=dfnya['waist_cm'] / dfnya['height_cm']

    #kekuatan pompa jantung
    dfnya['new_pulse_preasure'] = dfnya['systolic']-dfnya['relaxation']

    #penglihatan_rata-rata
    dfnya['new_vision'] = (dfnya['eyesight_right']+dfnya['eyesight_left'])/2

    #hearing_rata-rata
    dfnya['new_hearing'] = (dfnya['hearing_right']+dfnya['hearing_left'])/2

    #good cholesterol ratio
    dfnya['new_good_chol_ratio'] = (dfnya['hdl'] / dfnya['cholesterol'])*100

    #bad-good cholesterol ratio
    dfnya['new_bad_good_chol_ratio'] = (dfnya['ldl'] / dfnya['hdl'])*100

    #liverEnzimeRatio
    dfnya['new_liverEnzimeRatio'] = (dfnya['ast'] / dfnya['alt'])*100

    return dfnya
#--------------------------------------------------------------------------


def load_model(filename):
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    print(f"Model loaded from {filename}")
    return model    

#--------------------------------------------------------------------------

def translate_smoker_status_to_text(predictions):
    results=[]
    for i, value in enumerate(predictions):
        if value == 1:
            results.append(f"SMOKER")
        else:
            results.append(f"Not Smoker")
    return results

#--------------------------------------------------------------------------

def runflow(dataDariForm):
    print('memasuki runflow() untuk model_df_M2_step04_train_xgboost_bestModel_AUC')

    data_dict = dataDariForm.to_dict(flat=True)
    df = pd.DataFrame([data_dict])
    df = df.apply(pd.to_numeric, errors='ignore')

    #print(df.columns)
    #print(df.shape)

    df.columns = [
        'age', 'height_cm',
        'weight_kg', 'waist_cm',
        'eyesight_left', 'eyesight_right',
        'hearing_left', 'hearing_right',
        'systolic', 'relaxation',
        'fasting_blood_sugar', 'cholesterol',
        'triglyceride', 'hdl',
        'ldl', 'hemoglobin',
        'urine_protein', 'serum_creatinine',
        'ast', 'alt', 'gtp',
        'dental_caries', 'model'
    ]
                         
    modelname = df.loc[0, 'model']
    df = df.drop(columns=['model'])

    # print(df.columns)
    # print(df.shape)


    impossible_thresholds = pd.DataFrame([
        {'feature': 'age', 'min': 0, 'max': 120},
        {'feature': 'height_cm', 'min': 120, 'max': 210},
        {'feature': 'weight_kg', 'min': 35, 'max': 200},
        {'feature': 'waist_cm', 'min': 50, 'max': 150},
        {'feature': 'eyesight_left', 'min': 0.1, 'max': 2.0},
        {'feature': 'eyesight_right', 'min': 0.1, 'max': 2.0},
        {'feature': 'hearing_left', 'min': 0, 'max': 2},
        {'feature': 'hearing_right', 'min': 0, 'max': 2},
        {'feature': 'systolic', 'min': 90, 'max': 180},
        {'feature': 'relaxation', 'min': 60, 'max': 120},
        {'feature': 'fasting_blood_sugar', 'min': 70, 'max': 126},
        {'feature': 'cholesterol', 'min': 125, 'max': 200},
        {'feature': 'triglyceride', 'min': 50, 'max': 150},
        {'feature': 'hdl', 'min': 40, 'max': 100},
        {'feature': 'ldl', 'min': 50, 'max': 130},
        {'feature': 'hemoglobin', 'min': 12.0, 'max': 17.5},
        {'feature': 'urine_protein', 'min': 0, 'max': 4},
        {'feature': 'serum_creatinine', 'min': 0.6, 'max': 1.3},
        {'feature': 'ast', 'min': 8, 'max': 33},
        {'feature': 'alt', 'min': 7, 'max': 56},
        {'feature': 'gtp', 'min': 8, 'max': 61},
        {'feature': 'dental_caries', 'min': 0, 'max': 1},
    ])

    df = capping_features_based_on_threshold(df,impossible_thresholds)
    df = add_combined_features(df)
    df_columns = df.columns

    # print(df.columns)
    # print(df.shape)

    scaler = load_model(os.path.join(os.path.dirname(__file__), 'model_M2_scalernya.pkl'))
    df = scaler.transform(df) 

    df = pd.DataFrame(df,columns=df_columns) #ubah numpy.ndarray hasil scaling kembali jadi panda dataframe

    # selected_columns = ['age', 'height_cm', 'weight_kg', 'waist_cm', 'hearing_left',
    #    'hearing_right', 'systolic', 'relaxation', 'fasting_blood_sugar',
    #    'triglyceride', 'hdl', 'hemoglobin', 'urine_protein',
    #    'serum_creatinine', 'gtp', 'dental_caries', 'new_vision',
    #    'new_good_chol_ratio', 'new_bad_good_chol_ratio',
    #    'new_liverEnzimeRatio', 'smoking']
    
    # df=df[[col for col in selected_columns if col in df.columns]]

    # print(df.columns)
    # print(df.shape)

    selected_columns = ['age','height_cm','waist_cm','hearing_left',
        'hearing_right','relaxation','fasting_blood_sugar',
        'triglyceride','hdl','hemoglobin',
        'serum_creatinine', 'gtp', 'dental_caries','new_vision',''
         'new_liverEnzimeRatio','smoking']


    df=df[[col for col in selected_columns if col in df.columns]]

    # #print(df.columns)
    # print(df.shape)

    model = load_model(os.path.join(os.path.dirname(__file__), 'model_df_M2_step04_train_xgboost_bestModel_AUC.pkl'))
    prediction = model.predict(df) 
 
    return translate_smoker_status_to_text(prediction)[0]

