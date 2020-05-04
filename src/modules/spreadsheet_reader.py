import pandas as pd


def read_spreadsheet(file_path):
    """
    Read given spreadsheet as a dictionary of dataframes
    :param file_path: path to spreadsheet (.csv or .xlsx or .xls)
    :return: a dictionary of sheets in spreadsheet where key is sheet name and
    value is data in that sheet stored as a pandas dataframe
    """
    """
    Example returned dictionary:
    {'sheet1name': dataframeObject1, 'sheet2name':'dataframeObject2'
    """
    if file_path.endswith('csv'):
        dftmp = pd.read_csv(file_path)
        col_rename = {}
        for col_name in dftmp.columns:
            col_rename[col_name] = col_name.lower()
        dftmp = dftmp.rename(columns=col_rename)
        return {'csv':dftmp}

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
