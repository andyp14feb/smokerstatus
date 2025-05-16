from flask import request
import pandas as pd

def testaja(stringnya):
    stringnya = stringnya.replace("i", "xxx")
    stringnya = stringnya.replace("a", "i")
    stringnya = stringnya.replace("xxx", "a")
    return stringnya


def runflow(dataDariForm):
    data_dict = dataDariForm.to_dict(flat=True)
    df = pd.DataFrame([data_dict])
    df = df.apply(pd.to_numeric, errors='ignore')
    print(df)


    dimodif = testaja(df.to_string(index=False))

    return dimodif
