from app.core.config import Config
import pandas as pd
import os

from app.services.plotting import generate_plots

OUTPUT_DIR = Config.UPLOAD_DIR

def process_excel_file(file_path: str,  control_name: str, normalization_name: str, experiment_name:str, has_control:bool, has_normalization:bool ) -> (str, list[str]):
    dest_file = os.path.join(OUTPUT_DIR, f'{experiment_name}.xlsx')
    df = pd.read_excel(file_path, 'Results', header=None).dropna(axis=1, how='all')
    writer = pd.ExcelWriter(dest_file, engine='xlsxwriter')
    metadata = {}
    well_data_start_index = 0

    for i, row in df.iterrows():
        if pd.isna(row[0]):
            well_data_start_index = i + 1
            break
        metadata[row[0]] = row[1]

    well_data = df.iloc[well_data_start_index+1:]
    well_data.columns = list(df.iloc[well_data_start_index])

    well_data = well_data.dropna(how='all').reset_index(drop=True)
    well_data = well_data[~well_data['Ct Mean'].isna()]

    sample = well_data.groupby(['Target Name', 'Sample Name'])[['Ct Mean']].apply(lambda x : x.mean()).reset_index()
    pivot_df = sample.pivot_table(index='Sample Name', columns='Target Name', values='Ct Mean', aggfunc='first')
    pivot_df.to_excel(writer, sheet_name='Mean values')

    pivot_df = pivot_df.subtract(pivot_df[normalization_name], axis=0)
    del pivot_df[normalization_name]
    pivot_df.to_excel(writer, sheet_name='Delta Ct')

    pow2 = 2**(-pivot_df)
    pow2.to_excel(writer, sheet_name='2^(-delta_ct)')

    if has_control:
        norm = pow2.divide(pow2.loc[control_name])
        norm.to_excel(writer, sheet_name='Normalized 2^(-delta_ct)')

    writer.close()

    return dest_file
