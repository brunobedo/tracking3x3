from pathlib import Path
import pandas as pd 
import os 



# Get project folder
def get_project_dir():
    return str(Path.cwd().parent).replace('\\','/')



def get_match_info(jogo_id): 
    try:
        # Construct file path
        file = Path(f"{get_project_dir()}/data/info/match_info_jogo{jogo_id}.xlsx")

        # Check if the file exists before trying to open it
        if not file.exists():
            print(f"Error: File not found - {file}")
            return None

        # Load the Excel file
        df_match_info = pd.read_excel(file, engine='openpyxl')
        print(f"Successfully loaded match info for match {jogo_id}.")
        return df_match_info

    except FileNotFoundError:
        print(f"Error: File not found - {file}")
        return None

    except pd.errors.EmptyDataError:
        print(f"Error: File is empty or corrupted - {file}")
        return None

    except Exception as e:
        print(f"Unexpected error while loading match info: {e}")
        return None



def load_tracking(jogo_id):
    try:
        file = Path(f'{get_project_dir()}/data/2d/jogo{jogo_id}.2d')
        # Check if the file exists before trying to open it
        if not file.exists():
            print(f"Error: File not found - {file}")
            return None

        # Load the Excel file
        df = pd.read_csv(file, delim_whitespace=True, header=None)
        print(f"Successfully loaded tracking data for match {jogo_id}.")
        num_cols = df.shape[1]
        new_column_names = [f"j{i//2 + 1}{'x' if i % 2 == 0 else 'y'}" for i in range(num_cols)]
        df.columns = new_column_names
        df = df.dropna(axis=1, how='all')
        return df

    except FileNotFoundError:
        print(f"Error: File not found - {file}")
        return None

    except pd.errors.EmptyDataError:
        print(f"Error: File is empty or corrupted - {file}")
        return None

    except Exception as e:
        print(f"Unexpected error while loading match info: {e}")
        return None