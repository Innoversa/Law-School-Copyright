import pandas as pd

def read_spreadsheet(file_path):
    if file_path.endswith('csv'):
        return {'csv':pd.read_csv(file_path)}

    excel_file = pd.ExcelFile(file_path)
    result = {}
    for sheet_name in excel_file.sheet_names:
        dftmp = pd.read_excel(excel_file, sheet_name)
        col_rename = {}
        for col_name in dftmp.columns:
            col_rename[col_name] = col_name.lower()
        dftmp = dftmp.rename(columns=col_rename)
        result[sheet_name] = dftmp
    return result