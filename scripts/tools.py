from pathlib import Path
import pandas as pd 
import os 
from scipy.signal import butter, filtfilt, firwin
import numpy as np
from matplotlib.patches import Circle, Rectangle, Arc
from scipy.interpolate import UnivariateSpline


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
        new_column_names = [f"j{i//2 + 1}{'x' if i % 2 == 0 else 'y'}" for i in range(num_cols - 1)]  # Ajuste no range
        df.columns = ['frames'] + new_column_names  # Assign 'frames' only to the first column

        # Remove fully empty columns
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



def apply_filter(data, sample_rate, method='butterworth', cutoff=5, order=4, numtaps=255, padlen=128):
    """Apply a specified filter to the data with padding."""
    nyquist = 0.5 * sample_rate
    normal_cutoff = cutoff / nyquist

    if method == 'butterworth':
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        padded_data = np.pad(data, ((padlen, padlen), (0, 0)), mode='reflect')
        filtered_data = filtfilt(b, a, padded_data, axis=0)
        filtered_data = filtered_data[padlen:-padlen, :]

    elif method == 'fir':
        fir_coeff = firwin(numtaps, normal_cutoff, window='blackman')
        padded_data = np.pad(data, ((padlen, padlen), (0, 0)), mode='reflect')
        filtered_data = filtfilt(fir_coeff, 1.0, padded_data, axis=0)
        filtered_data = filtered_data[padlen:-padlen, :]

    else:
        raise ValueError("Method must be 'butterworth' or 'fir'")

    return filtered_data



def draw_half_right(ax=None, linecolor='white', lw=1.5, outer_lines=False, courtcolor='#CC5500', remove_axis=False):
    if ax is None:
        ax = plt.gca()
    
    court_width, court_height = 15.05, 14.2  # Dimensões da quadra

    # Contorno da quadra
    outer_lines = Rectangle((0, 0), court_height, court_width, linewidth=lw, color=linecolor, fill=False)

    # Cesta no centro da altura e uma certa distância da linha de fundo
    hoop = Circle((court_height - 1.2, court_width / 2), radius=0.20, linewidth=lw, color=linecolor, fill=False)

    # Tabela
    backboard_distance_from_baseline = 1.2
    backboard = Rectangle((court_height - backboard_distance_from_baseline + 0.5, court_width / 2 - 1), 0.1, 2, linewidth=lw, color=linecolor)
    
    # Área pintada
    paint_width = 4.9
    paint_height = 5.8
    outer_box = Rectangle((court_height - paint_height, court_width / 2 - paint_width / 2), paint_height, paint_width, linewidth=lw, color=linecolor, fill=False)
    inner_box_width = 3.6
    inner_box = Rectangle((court_height - paint_height, court_width / 2 - inner_box_width / 2), paint_height, inner_box_width, linewidth=lw, color=linecolor, fill=False)

    # Arco superior do lance livre
    top_free_throw = Arc((court_height - paint_height, court_width / 2), inner_box_width, inner_box_width, theta1=90, theta2=270, linewidth=lw, color=linecolor, fill=False)

    # Arco inferior do lance livre (tracejado)
    bottom_free_throw = Arc((court_height - paint_height, court_width / 2), inner_box_width, inner_box_width, theta1=270, theta2=90, linewidth=lw, color=linecolor, linestyle='dashed')

    # Área restrita
    restricted_radius = 2
    restricted = Arc((court_height - backboard_distance_from_baseline, court_width / 2), restricted_radius*1.3, restricted_radius*1.3, theta1=90, theta2=270, linewidth=lw, color=linecolor)

    # Linha dos 3 pontos
    three_point_radius = 6.75  # Aproximação para a quadra adaptada
    three_arc = Arc((court_height - backboard_distance_from_baseline - 1, court_width / 2), three_point_radius * 2.1, three_point_radius*2, theta1=90, theta2=270, linewidth=lw, color=linecolor)

    # Círculo central (não aplicável para meia quadra, mas mantido para completude)
    center_circle_radius = 2
    center_outer_arc = Arc((0, court_width / 2), center_circle_radius * 2, center_circle_radius * 2, theta1=270, theta2=90, linewidth=lw, color=linecolor)
    center_inner_arc = Arc((0, court_width / 2), center_circle_radius, center_circle_radius, theta1=270, theta2=90, linewidth=lw, color=linecolor)
    
    # Three point line
    # Create the side 3pt lines, they are 14ft long before they begin to arc
    corner_three_a = Rectangle((11.5, 0.77), 2.5, 0, linewidth=lw,
                                color=linecolor)
    corner_three_b = Rectangle((11.5, court_width-0.78), 2.5, 0, linewidth=lw,
                                color=linecolor)
    
    court_elements = [  hoop, backboard, outer_box, inner_box, top_free_throw, bottom_free_throw, restricted, three_arc, center_outer_arc, center_inner_arc,
                        corner_three_a,corner_three_b]

    if outer_lines:
        court_elements.append(outer_lines)

    for element in court_elements:
        ax.add_patch(element)

    ax.set_xlim(-1, court_height+1)
    ax.set_ylim(-1, court_width+1)
    ax.set_aspect('equal')
    ax.set_facecolor(courtcolor)
    if remove_axis: 
        ax.set_xticks([])
        ax.set_yticks([])
    return ax



def spline_interpolation(array, k=3, s=0):
    """
    Realiza interpolação spline para preencher valores faltantes em um array.

    Parâmetros:
    - array: np.ndarray, array contendo valores, incluindo np.nan para valores faltantes.
    - k: int, opcional, grau do spline (padrão é 3 para spline cúbico).
    - s: float, opcional, fator de suavização. Se s=0, o spline passará por todos os pontos.

    Retorna:
    - array_interpolated: np.ndarray, array com os valores faltantes preenchidos.
    """
    # Identificar os índices de valores não faltantes e faltantes
    x = np.arange(len(array))
    mask = ~np.isnan(array)
    x_known = x[mask]
    y_known = array[mask]
    x_missing = x[~mask]

    # Criar um spline a partir dos dados conhecidos
    spline = UnivariateSpline(x_known, y_known, k=k, s=s)

    # Usar o spline para interpolar os valores faltantes
    array_interpolated = array.copy()
    array_interpolated[~mask] = spline(x_missing)
    
    return array_interpolated



def get_match_player_data(jogo_id, jogador_id):
    try:
        df_info = get_match_info(jogo_id)
        df_tracking = load_tracking(jogo_id)
        frame_start = int(df_info['frame_inicial'][0])
        frame_final = int(df_info['frame_final'][0])
        df_tracking_cut = df_tracking.iloc[frame_start:frame_final]
        df_j = df_tracking_cut.filter(like=f'j{jogador_id}', axis=1)
        dat_x = df_j.filter(like='x', axis=1).iloc[:, 0].to_numpy()
        dat_y = df_j.filter(like='y', axis=1).iloc[:, 0].to_numpy()

        dat_x_int = spline_interpolation(dat_x)
        dat_y_int = spline_interpolation(dat_y)

        df_j = pd.DataFrame(data={'x': dat_x_int, 'y': dat_y_int})
        array_filt = apply_filter(df_j, sample_rate=30, cutoff=0.5)
        df_jf = pd.DataFrame(array_filt, columns=['x', 'y'])
        print(f'Successfully loaded tracking data for: Match {jogo_id} - Player {jogador_id}.')
        return df_jf
    except: 
        print(f'Error in loading: Match {jogo_id} - Player {jogador_id}.')



def create_project_folder(folder_name): # create project folder
    os.makedirs(f'{get_project_dir()}/{folder_name}',exist_ok=True)