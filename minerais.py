import datetime

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

from PIL import Image, ImageOps
import pandas as pd
import numpy as np
import io
import base64
import tensorflow.keras




data = np.ndarray(shape=(1,224,224,3), dtype=np.float32)
size = (224, 224)

model = tensorflow.keras.models.load_model('keras_model.h5')

#external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/sketchy/bootstrap.min.css']

app = dash.Dash(__name__) #, external_stylesheets=external_stylesheets
server = app.server

app.title = 'Classificador de minerais'

app.layout = html.Div(children=[
    dcc.Upload(
        id='upload-image',
        children=html.Div([
            'Arraste e solte ou ',
            html.A(style={'color':'blue','text-decoration': 'underline'},children='clique aqui'),
            ' para selecionar uma imagem da sua máquina'
        ]),
        className="bloco",
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-image-upload'),
    
])


def parse_contents(contents, filename, date):

    _ , content_string = contents.split(',')

    decoded = base64.b64decode(content_string)


    image = Image.open(io.BytesIO(decoded))

    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    image_array = np.asarray(image)

    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    data[0] = normalized_image_array

    dados = pd.read_csv('labels.txt', sep=" ", header=None)
    dados.columns = ["Minerais"]
    dados['Probabilidade (%)'] = np.zeros(dados.shape[0])

    prediction = model.predict(data)
    dados['Probabilidade (%)'][:] = prediction[0,:]*100
    dados.sort_values(by=['Probabilidade (%)','Minerais'],ascending=False, inplace=True)
    dados_final = dados

    return html.Div([
        html.H5('Nome do arquivo:'),
        html.H5(filename),
        html.H5('Data e hora:'),
        html.H6(datetime.datetime.fromtimestamp(date)),

        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        html.Img(src=contents,style={'width':'500px','height':'500px'}),
        html.Hr(),
        #html.Div(data.head(10)),
        html.H4('Resultado da classificação:'),
        dash_table.DataTable(id='table',style_cell={'font-size': '22px','font-family': 'sans-serif'}, columns=[{'name':i,'id':i} for i in dados_final.columns],
        data=dados_final.to_dict('records'))
        
    ])


@app.callback(Output('output-image-upload', 'children'),
              Input('upload-image', 'contents'),
              State('upload-image', 'filename'),
              State('upload-image', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


if __name__ == '__main__':
    app.run_server(debug=True)