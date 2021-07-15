import json
import base64
import os
import pandas as pd
import numpy as np
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go
import geopandas as gpd
import dash 
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import plotly.figure_factory as ff
import statsmodels.api as sm
from dash.dependencies import Input, Output


from layout_helper import run_standalone_app

text_style = {
    'color': "black",
    'font-family': 'Open Sans',
    'fontSize': 16
}



app_name = "CYP2D6"


#####################################
# Data
#####################################

df_haplotipos = pd.read_csv( "data/df_fund_facts.csv")
df_farmacos = pd.read_csv( "data/Farmacos.csv")
df = gpd.read_file( 'data/DATA_CYP2D6.geojson')
df.set_index("Region")


DATASETS = {
    'dataset_IM': df[df["Fenotipo"]=="IM"],
    'dataset_UM': df[df["Fenotipo"]=="UM"],
    'dataset_NM': df[df["Fenotipo"]=="NM"],
    'dataset_PM': df[df["Fenotipo"]=="PM"],
    'dataset2': df_haplotipos,
}
filtro = df.copy()

#def description():
#    return 'View multiple sequence alignments of genomic or protenomic sequences.'

def generate_table(df_haplotipos, max_rows=5):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in df_haplotipos.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(df_haplotipos.iloc[i][col]) for col in df_haplotipos.columns
            ]) for i in range(min(len(df_haplotipos), max_rows))
        ])
    ])
def generate_table_farmacos(df_farmacos, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in df_farmacos.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(df_farmacos.iloc[i][col]) for col in df_farmacos.columns
            ]) for i in range(min(len(df_farmacos), max_rows))
        ])
    ])


def header_colors():
    return {
        'bg_color': '#1ac1c4',
        'font_color': 'black',
    }



#####################################
# Layout
#####################################

def layout():
    return html.Div(id='alignment-body', className='app-body', children=[
        html.Div([
            html.Div(id='alignment-control-tabs', className='control-tabs',  style={'width': "40%",'height':'90vh'}, children=[
                dcc.Tabs(
                    id='alignment-tabs', value='what-is',
                    children=[
                        dcc.Tab(
                            label='Introducción',
                            value='what-is',
                            children=html.Div(className='control-tab', style={'color': 'black', 'fontSize': 16}, children=[
                                html.H4(
                                    className='what-is',
                                    children='Análisis de la distribución geográfica de polimorfismos de CYP2D6 como predictores de reacciones adversas en el tratamiento de la depresión'
                                ),
                                html.P(
                                    """
                                    De acuerdo con cifras de la Organizacion Mundial de la Salud (OMS), 
                                    las disfunciones cognitivas y neuropsiquiátricas afectan a 
                                    alrededor de 450 millones de personas en el mundo [1], 
                                    siendo la depresión  la enfermedad con mayor incidencia además,
                                    la OMS estima que para 2040 la depresión es será la primera causa 
                                    más común de dicapacidad generando perdidas económicas importantes. 
                                    Por esta razón la necesidad de disminuir esta y otras afecciones 
                                    de salud mental. Para este fin existe tratamientos eficaces para
                                    la depresión moderada y grave sin embargo, los pacientes con desórdenes
                                    neuropsiquiátricos pueden consumir entre 6 a 10 fármacos al día [2]
                                    con el consiguiente riesgo de interacciones farmacológicas no deseadas
                                    y efectos adversos, pues aproximadamente el 90% de los fármacos empleados
                                    como tratamiento son suceptibles de variaciones farmacogenéticas asociadas 
                                    a polimorfismos en el gen CYP2D6 que codifica enzimas encargadas de descomponer
                                    los medicamentos empleados como antidepresivos [3]. 
                                    De acuerdo con la cantidad de actividad que presenta esta enzima se pueden 
                                    clasificar cuatro fenotipos con diferente respuesta biológica a estos farmacos. 
                                    A continuación se muestra un resumen de los cuatro fenotipos asociados a la expresion 
                                    de CYP2D6 por regiones geograficas así como información util que puede ayudar
                                    en consideraciones terapéuticas y ajustes de dosis. 
                                    """
                                ),
                                html.P(
                                    """
                                   Para realizar este mapa empleamos los fenotipos de CYP2D6 como biomarcadores de riesgo 
                                   a falla terapéutica o reacciones adversas a fármacos antidepresivos en diferentes poblaciones, 
                                   utilizando los datos del Proyecto de los 1000 genomas [4]
                                   organizados en la base de conocimientos de farmacogenómica (PharmGKB)[5]
                                   
                                    """
                                ),

                            ])
                        ),
                        dcc.Tab(
                            label='Fenotipos',
                            value='alignment-tab-select',
                                                       
                            children=html.Div(className='control-tab', children=[
                                html.Div(className='app-controls-block', children=[
                                    html.Div(
                                        className='fullwidth-app-controls-name',
                                        children="Seleccione un fenotipo"
                                    ),
                                    html.P(
                                    """
                                    Para usar la aplicación seleccione un fenotipo de interés y visualice 
                                    la distribución identificada en cada región geográfica así como 
                                    recomendaciones y datos. 
                                   
                                    """
                                ),
                                  dcc.Dropdown(id="slct_feno",
                                        options=[
                                         {"label": "Ultrametabolizadores", "value": 'UM'},
                                         {"label":"Metabolizadores lentos", "value": 'PM'},
                                         {"label": "Normales", "value": 'NM'},
                                        {"label": "Intermedios", "value": 'IM'}],
                                                 multi=False,
                                                 value='UM',
                                                 style={'width': "60%"}
                                     ),
                                 html.Div(children=[
                                 html.H4(children='Fenotipos'),
                                 generate_table(df_haplotipos)]),
                                ]),
                            ]),
                        ),
                                
                        dcc.Tab(
                            label='Efectos adversos',
                            value='control-tab-select2',
                            children=html.Div(className='control-tab', children=[
                                html.H4(
                                className='what-is',
                                children=' Efectos adversos asociados a fenotipos de CYP2D6'),
                                html.P(
                                """
                                En la mayoría de las regiones continentales los metabolizadores intermedios (IM) 
                                son la segunda frecuencia más abundante,excepto en Oceanía en donde los 
                                ultra metabolizadores (UM) son mucho más abundantes (20%), en Asia del este también
                                hay un porcentaje importante de UM (9.5%). 
                                Por otro lado, otro de los fenotipos importantes en términos de reacciones adversas 
                                son los metabolizadores lentos (PM),  ya que se trata de enzimas sin actividad de 
                                depuración de los fármacos, presenta la frecuencia más elevada en población europea (6.5%). 
                                """
                                ),
                                html.P(
                                """
                                La información disponible de Latinoamérica indica que casi 60% de la población tendría
                                un fenotipo normal, casi 30% metabolismo intermedio y entre 3 y 4 % UM y PM.

                                Con respecto a los fármacos investigados, a continuación se resumen los fenotipos de 
                                riesgo y efectos adversos reportados en la literatura.

                                """
                                ),                                
                                 html.Div(children=[
                                 html.H4(children=''),                                 
                                 generate_table_farmacos(df_farmacos)]),

                                ]),
                            ),
                        dcc.Tab(
                            label='Más información',
                            value='control-tab-select-2',
                            children=html.Div(className='control-tab', children=[
                                html.H4(
                                className='what-is-',
                                children=' Referencias'),
                                html.P(
                                """
                                [1] World Health Organization 2008, The Global Burden of Disease 2004
                                update. http://www.who.int/healthinfo/global_burden_disease/GBD_
                                report_2004update_full.pdf Accessed 16.6.2012

                                """
                                ),
                                html.P(
                                """
                                [2] Cacabelos, R. (2020). Pharmacogenomics of Cognitive Dysfunction and Neuropsychiatric Disorders in Dementia.
                                  Int J Mol Sci, 21(9). doi:10.3390/ijms21093059
                                
                                """
                                ),
                                html.P(
                                """
                                [3] Hicks, J. K., Swen, J. J., Thorn, C. F., Sangkuhl, K., Kharasch, E. D., Ellingrod, V. L., . . .
                                 Clinical Pharmacogenetics Implementation, C. (2013). Clinical Pharmacogenetics Implementation Consortium 
                                 guideline for CYP2D6 and CYP2C19 genotypes and dosing of tricyclic antidepressants. Clin Pharmacol Ther,
                                 93(5), 402-408. doi:10.1038/clpt.2013.2

                                """
                                ),
                                html.P(
                                """
                                [4] Clarke, L., Zheng-Bradley, X., Smith, R., Kulesha, E., Xiao, C., Toneva, I., . . . 
                                Genomes Project, C. (2012). The 1000 Genomes Project: data management and community access. 
                                Nat Methods, 9(5), 459-462. doi:10.1038/nmeth.197

                                """
                                ),
                                html.P(
                                """
                                [5] Whirl-Carrillo, M., McDonagh, E. M., Hebert, J. M., Gong, L., Sangkuhl, K., Thorn, C. F., . . . Klein, T. E. 
                                (2012).  Pharmacogenomics knowledge for personalized medicine. Clin Pharmacol Ther, 92(4), 414-417. doi:10.1038/clpt.2012.96

                                """
                                ),                                         
                                html.H4(
                                className='what-is-',
                                children=' Recursos '),
                                html.P(
                                """
                                Para obtener más informacion se proporcionan los siguientes recursos: 
                                """
                                ),
                                html.H4(
                                className='what-is-',
                                children=' '),
                                html.A(id='ghh-link1',
                                 children=[ 'Manuscrito' ],
                                href="https://drive.google.com/file/d/1cCTt24htDxX25qvn7KculZTsBzxso5f2/view?usp=sharing"
                                "blob/master/tests/dashbio_demos/dash-{}/app.py".format(
                                app_name
                                 ),
                                 style={'color':  'black'}
                                ),
                                html.H4(
                                className='what-is-',
                                children=''),
                                html.A(id='ghh-link2',
                                 children=[ 'Proyecto 1000 Genomas' ],
                                href="https://www.internationalgenome.org/"
                                "blob/master/tests/dashbio_demos/dash-{}/app.py".format(
                                app_name
                                 ),
                                 style={'color':  'black'}
                                ),
                                html.H4(
                                className='what-is-',
                                children=''),                                
                                html.A(id='ghh-link3',
                                 children=[ 'PharmaGKB CYP2D6' ],
                                href="https://www.pharmgkb.org/gene/PA128"
                                "blob/master/tests/dashbio_demos/dash-{}/app.py".format(
                                app_name
                                 ),
                                 style={'color':  'black'}
                                ),  
                                html.H4(
                                className='what-is-',
                                children=''),                                
                                html.A(id='ghh-link5',
                                 children=[ 'Guia del Consorcio de Implementación de Farmacogenética Clínica' ],
                                href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3384438/"
                                "blob/master/tests/dashbio_demos/dash-{}/app.py".format(
                                app_name
                                 ),
                                 style={'color':  'black'}
                                ),
                                html.H4(
                                className='what-is-',
                                children=''),                                
                                html.A(id='ghh-link6',
                                 children=[ 'Guia del Grupo de Trabajo holandés de Farmacogenética (DPWG)' ],
                                href="https://www.nature.com/articles/s41431-019-0540-0"
                                "blob/master/tests/dashbio_demos/dash-{}/app.py".format(
                                app_name
                                 ),
                                 style={'color':  'black'}
                                ),    

                                ]),
                            ),


                     ]),  
             ]),
    ]),
    html.Div(id='output_container', children=[]),
    html.Br(),
    dcc.Graph(id='my_region_map', figure={},
    style={'height':'90vh', 'width':'55vw', 'float': 'right'}),
])



#####################################
# Callbacks
#####################################

def callbacks(_app):

    @_app.callback(
        [Output(component_id='output_container', component_property='children'),
         Output(component_id='my_region_map', component_property='figure')],
         [Input(component_id='slct_feno', component_property='value')]
         )

        #return container, fig    
    def update_graph(option_slctd):
        print(option_slctd)
        print(type(option_slctd))

        container = "Fenotipo seleccionado: {}".format(option_slctd)

        dff = df.copy()
        dff = dff[dff["Fenotipo"] == option_slctd]



        # Plotly Express
        fig = px.choropleth(dff,geojson=dff.geometry,
        locations=dff.index, color="Frecuencias", title='Distribución geográfica de polimorfismos de CYP2D6 como predictores de reacciones adversas en el tratamiento de la depresión')
        fig.update_geos(fitbounds="locations", visible=False)


        return container, fig


app = run_standalone_app(layout, callbacks, header_colors)

if __name__ == '__main__':
    app.run_server(debug=True)