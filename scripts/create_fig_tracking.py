import tools 
import matplotlib.pyplot as plt
import argparse


def plot_player_trajectory(df_player, jogo_id, jogador_id, save=True):
    # Criar a figura e o eixo
    fig, ax = plt.subplots(figsize=(3, 3))  # Aumenta o tamanho para melhor visualização

    # Plotar a linha preta
    ax.plot(df_player['x'], df_player['y'], 'k', linewidth=1.5)  # Linha mais espessa para melhor visualização

    # Remover os ticks dos eixos
    ax.set_xticks([])
    ax.set_yticks([])

    # Remover bordas desnecessárias
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Adicionar título
    ax.set_title(f'Trajetória | Jogo {jogo_id} - Atleta {jogador_id}', fontsize=8, fontweight="bold")

    # Chamar a função para desenhar metade direita (se necessário)
    ax = tools.draw_half_right(ax)

    # Salvar a figura
    if save is True:
        folder = 'results/figures/tracking/'
        file = f'tracking_j{jogo_id}p{jogador_id}.png'
        tools.create_project_folder(folder)
        plt.savefig(f'{tools.get_project_dir()}/{folder}/{file}', dpi=150, bbox_inches="tight",transparent=False)
    # Exibir o gráfico
    # plt.show()


def create_fig_tracking(jogo_id,save=True):
    df_info = tools.get_match_info(jogo_id)
    list_atletas = df_info['atleta_id'].dropna().unique().astype(int)
    for jogador_id in list_atletas:
        print(' ')
        df_player = tools.get_match_player_data(jogo_id,jogador_id)
        plot_player_trajectory(df_player, jogo_id, jogador_id, save)


def main():
    """
    Configura argparse para rodar o script pelo terminal.
    """
    parser = argparse.ArgumentParser(description="Gerar figuras de tracking de jogadores.")
    
    # Argumentos obrigatórios
    parser.add_argument("--jogo_id", type=int, required=True, help="ID do jogo para processar.")
    
    # Argumento para salvar ou não as figuras
    parser.add_argument("--save", action="store_true", help="Salvar as figuras geradas.")
    parser.add_argument("--no-save", dest="save", action="store_false", help="Não salvar as figuras.")
    parser.set_defaults(save=True)  # Padrão: salvar as figuras

    # Parse dos argumentos
    args = parser.parse_args()

    # Chamar a função para gerar as figuras
    create_fig_tracking(jogo_id=args.jogo_id, save=args.save)



if __name__ == "__main__":
    main()