import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import joblib
import pandas as pd
import numpy as np 
import plotly.express as px


modelo = joblib.load(r'.\Modelo\modelo_credito.pkl')


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, 'assets/style.css'])


formulario = dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.CardGroup([
                    dbc.Label('Idade: '),
                    dbc.Input(id='mes', type='number', value=None),
                ], class_name='mb-3'),
                dbc.CardGroup([
                    dbc.Label('Salário anual: '),
                    dbc.Input(id='salario', type='number', value=None),
                ], class_name='mb-3'),
                dbc.CardGroup([
                    dbc.Label('Número de contas: '),
                    dbc.Input(id='num_contas', type='number', value=None),
                ], class_name='mb-3'),
                dbc.CardGroup([
                    dbc.Label('Número de cartões: '),
                    dbc.Input(id='num_cartoes', type='number', value=None),
                ], class_name='mb-3'),
                dbc.CardGroup([
                    dbc.Label('Juros no emprestimo: '),
                    dbc.Input(id='juros_emprestimo', type='number', value=None),
                ], class_name='mb-3'),
                dbc.CardGroup([
                    dbc.Label('Número de emprestimos: '),
                    dbc.Input(id='num_emprestimo', type='number', value=None),
                ], class_name='mb-3'),
                dbc.CardGroup([
                    dbc.Label('Dias de atraso no pagamento: '),
                    dbc.Input(id='dias_atraso', type='number', value=None),
                ], class_name='mb-3'),
                dbc.CardGroup([
                    dbc.Label('Número de pagamentos atrasados: '),
                    dbc.Input(id='num_pgmt_atrasado', type='number', value=None),
                ], class_name='mb-3'),
                dbc.CardGroup([
                    dbc.Label('Número de verificações de crédito: '),
                    dbc.Input(id='num_verificacoes', type='number', value=None),
                ], class_name='mb-3'),
                dbc.CardGroup([
                    dbc.Label('Mix de crédito: '),
                    dbc.Select(id='mix_credito', options=[{'label': 'Bom', 'value': '0'},
                                                        {'label': 'Normal', 'value': '1'},
                                                        {'label': 'Ruim', 'value': '2'}]),
                ], class_name='mb-3'),
                dbc.CardGroup([
                    dbc.Label('Dívida total: '),
                    dbc.Input(id='divida_total', type='number', value=None),
                ], class_name='mb-3'),
            ]),
            dbc.Col([
                dbc.CardGroup([
                    dbc.Label('Taxa de uso de crédito: '),
                    dbc.Input(id='taxa_uso_credito', type='number', value=None),
                ], class_name='mb-3'),
                dbc.CardGroup([
                    dbc.Label('Idade do histórico de crédito(em meses): '),
                    dbc.Input(id='idade_hist_credito', type='number', value=None),
                ], class_name='mb-3'),
                dbc.CardGroup([
                    dbc.Label('Investimento mensal: '),
                    dbc.Input(id='investimento_mensal', type='number', value=None),
                ], class_name='mb-3'),
                dbc.CardGroup([
                    dbc.Label('Comportamento de pagamento: '),
                    dbc.Select(id='comportamento_pgmt', options=[{'label': 'alto gasto pagamento baixo', 'value': '0'},
                                                        {'label': 'baixo gasto pagamento alto', 'value': '1'},
                                                        {'label': 'baixo gasto pagamento medio', 'value': '2'},
                                                        {'label': 'baixo gasto pagamento baixo', 'value': '3'},
                                                        {'label': 'alto gasto pagamento medio', 'value': '4'},
                                                        {'label': 'alto gasto pagamento alto', 'value': '5'},]),
                ], class_name='mb-3'),
                dbc.CardGroup([
                    dbc.Label('Saldo final no mês: '),
                    dbc.Input(id='saldo_final_mes', type='number', value=None),
                ], class_name='mb-3'),
                dbc.CardGroup([
                    dbc.Label('Tem emprestimo de carro: '),
                    dbc.Select(id='emprestimo_carro', options=[{'label': 'Sim', 'value': '1'},
                                                        {'label': 'Não', 'value': '0'},]),
                ], class_name='mb-3'),
                dbc.CardGroup([
                    dbc.Label('Tem emprestimo de casa: '),
                    dbc.Select(id='emprestimo_casa', options=[{'label': 'Sim', 'value': '1'},
                                                        {'label': 'Não', 'value': '0'},]),
                ], class_name='mb-3'),
                dbc.CardGroup([
                    dbc.Label('Tem emprestimo pessoal: '),
                    dbc.Select(id='emprestimo_pessoal', options=[{'label': 'Sim', 'value': '1'},
                                                        {'label': 'Não', 'value': '0'},]),
                ], class_name='mb-3'),
                dbc.CardGroup([
                    dbc.Label('Tem emprestimo de crédito: '),
                    dbc.Select(id='emprestimo_creditoo', options=[{'label': 'Sim', 'value': '1'},
                                                        {'label': 'Não', 'value': '0'},]),
                ], class_name='mb-3'),
                dbc.CardGroup([
                    dbc.Label('Tem emprestimo estudantil: '),
                    dbc.Select(id='emprestimo_estudantil', options=[{'label': 'Sim', 'value': '1'},
                                                        {'label': 'Não', 'value': '0'},]),
                ], class_name='mb-3'),
                dbc.CardGroup([
                    dbc.Button('Prever', id='botao-prever', n_clicks=0),
                ], class_name='d-flex justify-content-center'),
            ]),
        ]),
    ])


app.layout = html.Div([
    html.H1('Sistema de análise de Crédito', className='text-center mb-4', style={'margin-top': '20px'}),
    html.H5('Preencha os dados abaixo para saber se o cliente está apto a receber crédito', className='text-center', style={'margin-bottom': '40px'}),
    formulario,
    html.Div(id='previsao', className='text-center', style={'margin-top': '80px'}),
])


@app.callback(
    Output('previsao', 'children'),
    Input('botao-prever', 'n_clicks'),
    State('mes', 'value'),
    State('salario', 'value'),
    State('num_contas', 'value'),
    State('num_cartoes', 'value'),
    State('juros_emprestimo', 'value'),
    State('num_emprestimo', 'value'),
    State('dias_atraso', 'value'),
    State('num_pgmt_atrasado', 'value'),
    State('num_verificacoes', 'value'),
    State('mix_credito', 'value'),
    State('divida_total', 'value'),
    State('taxa_uso_credito', 'value'),
    State('idade_hist_credito', 'value'),
    State('investimento_mensal', 'value'),
    State('comportamento_pgmt', 'value'),
    State('saldo_final_mes', 'value'),
    State('emprestimo_carro', 'value'),
    State('emprestimo_casa', 'value'),
    State('emprestimo_pessoal', 'value'),
    State('emprestimo_creditoo', 'value'),
    State('emprestimo_estudantil', 'value')
)


def prever_risco(n_clicks, mes, salario, num_contas, num_cartoes, juros_emprestimo, num_emprestimo, dias_atraso, num_pgmt_atrasado, num_verificacoes, mix_credito, divida_total, taxa_uso_credito, idade_hist_credito, investimento_mensal, comportamento_pgmt, saldo_final_mes, emprestimo_carro, emprestimo_casa, emprestimo_pessoal, emprestimo_creditoo, emprestimo_estudantil):


    # Verifica se o botão foi clicado
    if n_clicks == 0:
        return ''

    # Verifica se todos os campos foram preenchidos
    float_columns = ['salario', 'divida_total', 'taxa_uso_credito', 'investimento_mensal', 'saldo_final_mes']



    # Converte os valores de entrada para o formato correto

    entradas_usuario = pd.DataFrame(
        data = [[mes, salario, num_contas, num_cartoes, juros_emprestimo, num_emprestimo, dias_atraso, num_pgmt_atrasado, num_verificacoes, mix_credito, divida_total, taxa_uso_credito, idade_hist_credito, investimento_mensal, comportamento_pgmt, saldo_final_mes, emprestimo_carro, emprestimo_casa, emprestimo_pessoal, emprestimo_creditoo, emprestimo_estudantil]],
        columns = [['mes', 'salario', 'num_contas', 'num_cartoes', 'juros_emprestimo', 'num_emprestimo', 'dias_atraso', 'num_pgmt_atrasado', 'num_verificacoes', 'mix_credito', 'divida_total', 'taxa_uso_credito', 'idade_hist_credito', 'investimento_mensal', 'comportamento_pgmt', 'saldo_final_mes', 'emprestimo_carro', 'emprestimo_casa', 'emprestimo_pessoal', 'emprestimo_creditoo', 'emprestimo_estudantil']]
    )


    for col in float_columns:
        entradas_usuario[col] = entradas_usuario[col].astype(float)

    for col in entradas_usuario.columns:
        if entradas_usuario[col].dtype != np.float64:
            entradas_usuario[col] = entradas_usuario[col].astype(int)

    previsao = modelo.predict(entradas_usuario)[0]

    if previsao == 0:
        return html.H2('O score do cliente é baixo - O cliente não está apto a receber crédito.'), grafico_probabilidade(entradas_usuario) 
    elif previsao == 1:
        return html.H2('O score do cliente é médio - Confira as probabilidades de risco do cliente para decisão final'), grafico_probabilidade(entradas_usuario)        
    elif previsao == 2:
        return html.H2('O Score do cliente é alto - O cliente está apto a receber crédito.'), grafico_probabilidade(entradas_usuario)


def grafico_probabilidade(entradas_usuario):
    probabilidade = modelo.predict_proba(entradas_usuario)[0]
    probabilidade_df = pd.DataFrame(probabilidade, columns=['Probabilidade'])
    probabilidade_df.index = ['Baixo', 'Médio', 'Alto']
    return html.Div([
        dcc.Graph(
            figure=px.bar(probabilidade_df, x=probabilidade_df.index, y='Probabilidade', title='Probabilidades do Score de crédito do cliente',
                          labels={'index': 'Score'})
        )
    ])

app.run_server(debug=True)