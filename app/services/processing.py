from app.core.config import Config
import pandas as pd
import os

from app.services.plotting import generate_plots

OUTPUT_DIR = Config.UPLOAD_DIR
def combine_notebook(df_mean, df_std):
    df_mean = df_mean.copy()
    df_std = df_std.copy()
    df_mean.columns = pd.MultiIndex.from_product([df_mean.columns, ["Mean"]])
    df_std.columns = pd.MultiIndex.from_product([df_std.columns, ["SD"]])

    combined= (
        pd.concat([df_mean, df_std], axis=1)     # side‑by‑side
          .sort_index(axis=1, level=0)           # interleave: HLADR‑mean, HLADR‑std, …
    )
    return combined
def process_excel_file(file_path: str,  control_name: str, normalization_name: str, experiment_name:str, has_control:bool=True, has_normalization:bool=True ) -> (str, list[str]):
    try:
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
        well_data_std = well_data[~well_data['Ct SD'].isna()]
        well_data_mean = well_data[~well_data['Ct Mean'].isna()]
    
    
        sample_mean = well_data_mean.groupby(['Target Name', 'Sample Name'])[['Ct Mean']].apply(lambda x : x.mean()).reset_index()
        sample_std = well_data_std.groupby(['Target Name', 'Sample Name'])[['Ct SD']].apply(lambda x : x.mean()).reset_index()

        pivot_df_sd = sample_std.pivot_table(columns='Sample Name', index='Target Name', values='Ct SD', aggfunc='first')
        pivot_df_mean = sample_mean.pivot_table(columns='Sample Name', index='Target Name', values='Ct Mean', aggfunc='first')
        
        pivot_df_combined = combine_notebook(df_mean=pivot_df_mean, df_std=pivot_df_sd)
        pivot_df_combined.to_excel(writer, sheet_name='Mean values')

        print(pivot_df_mean)
        pivot_df_mean = pivot_df_mean.subtract(pivot_df_mean.loc[normalization_name,:], axis=1)
        pivot_df_sd = pivot_df_sd.subtract(pivot_df_sd.loc[normalization_name,:], axis=1)
        
        del pivot_df_mean.loc[normalization_name,:]
        del pivot_df_sd.loc[normalization_name,:]
    
        pivot_df_combined = combine_notebook(df_mean=pivot_df_mean, df_std=pivot_df_sd)
        pivot_df_combined.to_excel(writer, sheet_name='Delta Ct')
        
        pow2_mean = 2**(-pivot_df_mean)
        pow2_sd = 2**(-pivot_df_sd)
    
        pow2_combined = combine_notebook(df_mean=pow2_mean, df_std=pow2_sd)
        pow2_combined.to_excel(writer, sheet_name='2^(-delta_ct)')
        
        if has_control:
            norm_mean = pow2_mean.divide(pow2_mean[control_name])
            norm_sd = pow2_sd.divide(pow2_sd[control_name])

            norm_combined = combine_notebook(df_mean=norm_mean, df_std=norm_sd)
            norm_combined.to_excel(writer, sheet_name='Normalized 2^(-delta_ct)')
    
    
        return dest_file
    finally:
        writer.close()
