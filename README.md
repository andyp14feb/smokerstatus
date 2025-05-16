# Smoker Status Prediction — Web Interface Manual

This web application allows users to **predict smoking status** (Smoker or Non-Smoker) based on biometric and clinical data input. The prediction is powered by machine learning models trained on health datasets.

---

![Form Layout](https://github.com/andyp14feb/IndonesiaAI_ML_Batch7_Project_04/raw/main/docs/2025-05-15_202815_001__DokumentasiUntukManual.jpg)

## Table of Contents

1. [Input Form (No. 1)](#1-input-form)
2. [Model Selector (No. 2)](#2-model-selector)
3. [Submit Button (No. 3)](#3-submit-button)
4. [Clear Button (No. 4)](#4-clear-button)
5. [Fill Sample Button (No. 5)](#5-fill-sample-button)
6. [Prediction Result (No. 6)](#6-prediction-result)
7. [Reference Info (No. 7)](#7-reference-info)

---

## 1. Input Form

**Location:** Top section of the page

Enter biometric and medical data of the subject/patient.  
These include:

- Age (in 5-year intervals)
- Height (cm)
- Weight (kg)
- Waist circumference (cm)
- Eyesight (Left & Right)
- Hearing (Left & Right)
- Blood pressure (Systolic & Diastolic)
- Fasting blood sugar (mg/dL)
- Cholesterol (Total, HDL, LDL, Triglyceride)
- Hemoglobin (g/dL)
- Urine protein level (0–4)
- Serum creatinine (mg/dL)
- Liver enzymes (AST, ALT, GTP)
- Dental caries (0 = no, 1 = yes)

Refer to the reference section below for valid value ranges.

---

## 2. Model Selector

**Location:** Dropdown below the form

Choose a trained machine learning model to perform prediction.  
Available options include models like:

- Logistic Regression
- Random Forest
- XGBoost

---

## 3. Submit Button

**Label:** `Submit`

Click this to send the input data to the selected ML model.  
The model will return a prediction of whether the subject is a **Smoker** or **Non-Smoker**.

---

## 4. Clear Button

**Label:** `Clear`

This button will **clear all fields** in the form.  
Useful if you want to reset the form before entering new data.

---

## 5. Fill Sample Button

**Label:** `Fill with Example`

Click this to **autofill** the form with a random sample from the dataset.  
This is helpful for testing the app or demoing predictions.  
Note: It will exclude the actual `smoking` status during prediction.

---

## 6. Prediction Result

**Location:** Below the Submit button

- If the model predicts `Non-Smoker`, the result box will appear **green**.
- If the model predicts `Smoker`, it will appear **red**.

Use this prediction to guide further analysis or decision-making.

---

## 7. Reference Info

**Located:** At the bottom of the page

Provides:

- **Dataset origin:** [Binary Prediction of Smoker Status using Bio-Signals | Kaggle](https://www.kaggle.com/competitions/playground-series-s3e24/overview)
- **Field descriptions:** What each input represents and how it relates to smoking status

---

## Notes

- **Target:** The goal is to predict the `smoking` status (0 = Non-Smoker, 1 = Smoker)
- **Outlier Handling:** Backend has safeguards for invalid inputs

---

*Created as part of the Smoker Status Prediction Project — Machine Learning Batch 7*
