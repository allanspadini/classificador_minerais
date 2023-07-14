import gradio as gr
import pandas as pd

df = pd.read_csv('assets/busca_propriedades.csv')

def seleciona(Cor,Brilho,Traço):
    df_f = df
    if Cor=='Variável' or None:
        pass
    else:
        df_f = df_f[df_f['Cor']==Cor]

    if Brilho=='Variável' or None:
        pass
    else:
        df_f= df_f[df_f['Brilho']==Brilho]

    if Traço=='Variável' or None:
        pass
    else:
        df_f= df_f[df_f['Traço']==Traço]


    df_r = df_f['Nome']
    return pd.DataFrame(df_r)

#gr.Dropdown(list(df['Cor'].unique())),gr.Dropdown(list(df['Brilho'].unique()))
demo = gr.Interface(seleciona,[
    gr.Dropdown(list(df['Cor'].unique()),value='Variável'),
    gr.Dropdown(list(df['Brilho'].unique()),value='Variável'),
    gr.Dropdown(list(df['Traço'].unique()),value='Variável')]
    , "dataframe",description="Escolha as propriedades que você conhece sobre o mineral ou rocha")


if __name__ == "__main__":

    demo.launch()