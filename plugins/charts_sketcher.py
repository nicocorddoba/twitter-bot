import matplotlib.axes
import pandas as pd
import requests
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from datetime import datetime

from seaborn_styling_func import set_seaborn_style
set_seaborn_style('Cambria', background_color='#242c4f', grid_color='#546476', text_color='#d7dbe3')


today = datetime.today()
oneyback = datetime(today.year -1, today.month, today.day).strftime('%Y-%m-%d')
twoyback = datetime(today.year -2, today.month, today.day)
todaystr = today.strftime('%Y-%m-%d')


def request_to_dict(url:str) -> pd.DataFrame:
    """Consumes an API with the url and creats a pandas Dataframe with that information"""
    try:
        req = requests.get(url, verify=False)
        if req.status_code == 200:
            df = pd.DataFrame(req.json())
            # df['fecha'] = pd.to_datetime(df['fecha'], format='%Y-%m-%d')
        return df
    except Exception as e:
        print(e)


def request_to_dict_bcra(url:str) -> pd.DataFrame:
    """Consumes an API with the url and creats a pandas Dataframe with that information"""
    try:
        req = requests.get(url, verify=False)
        if req.status_code == 200:
            df = pd.DataFrame(req.json()['results'])
            # df['fecha'] = pd.to_datetime(df['fecha'], format='%Y-%m-%d')
            return df
    except Exception as e:
        print(e)


def draw_lineplot(ax:matplotlib.axes.Axes, data:pd.DataFrame, x:str, y:str, color:str, label:str):
    ax = sns.lineplot(data=data, x=x, y=y, color=color, label=label)
    ax.axhline(y=data['valor'].iloc[-1],color=color,linestyle="-.")
    ax.text(x=data['fecha'].iloc[-1],y=data['valor'].iloc[-1],s=data['valor'].iloc[-1],color=color, fontsize=12, ha='left', va='top', weight='bold')


def draw_country_risk_plot():
    # procesing
    rp_df = request_to_dict("https://api.argentinadatos.com/v1/finanzas/indices/riesgo-pais/")
    rp_df['fecha'] = pd.to_datetime(rp_df['fecha'], format='%Y-%m-%d')
    rp_df =rp_df[(rp_df['fecha'] < today) & (rp_df['fecha'] > oneyback)]
    
    # plotting
    fig = plt.figure(figsize=(15,8))
    ax_rp = fig.subplots()
    draw_lineplot(ax=ax_rp,data=rp_df, x='fecha', y='valor', color='#d7dbe3', label='Último valor')
    ax_rp.set_title('Riesgo País', fontsize=34, pad=12, weight='bold')
    ax_rp.set_xlabel('Fecha', fontsize=12, labelpad=12)
    ax_rp.set_ylabel('')
    fig.savefig('./images/rp.png')


def draw_inflacion_plot():
    interanual_df = request_to_dict("https://api.argentinadatos.com/v1/finanzas/indices/inflacionInteranual/")
    interanual_df =interanual_df[(interanual_df['fecha'] < today.strftime("%Y-%m-%d")) & (interanual_df['fecha'] > twoyback.strftime("%Y-%m-%d"))]
    inflacion_df = request_to_dict("https://api.argentinadatos.com/v1/finanzas/indices/inflacion/")
    inflacion_df = inflacion_df[(inflacion_df['fecha'] < today.strftime("%Y-%m-%d")) & (inflacion_df['fecha'] > twoyback.strftime("%Y-%m-%d"))]

    #plotting
    fig_inf,ax_men = plt.subplots(figsize=(15,8))
    # Inflacion Mensual
    plt.xticks(rotation=90)
    ax_men = sns.barplot(data=inflacion_df,x='fecha', y = 'valor', color='#8c9cad', edgecolor="#d7dbe3", linewidth=1.5)
    for index, row in inflacion_df.iterrows():
        ax_men.text(row['fecha'], row['valor']/2, row['valor'], horizontalalignment='center',verticalalignment='center', weight='bold')
    ax_men.set_ylabel('Inflación Mensual (%)', fontdict={'size':12}, labelpad=10)
    ax_men.grid(True)
    ax_men.set_title('Inflación', fontsize=34, pad=10, weight='bold')
    ax_men.set_xlabel('Fecha', fontdict={'size':12}, labelpad=10)
    ax_int = ax_men.twinx()
    #Inflacion Interanual
    draw_lineplot(ax=ax_int,data=interanual_df,x='fecha',y='valor',color='#d7dbe3',label='Inflación Interanual')
    ax_int.set_ylabel('Inflación Interanual (%)', fontdict={'size':12}, labelpad=10)
    ax_int.grid(False)
    ax_int.legend(loc='upper right', labels=['Inflación Interanual', 'Inflación Mensual'])
    fig_inf.savefig('./images/inflacion.png')


def draw_tna_plot():
    #procesing
    tnapf = request_to_dict_bcra(f'https://api.bcra.gob.ar/estadisticas/v2.0/DatosVariable/12/{oneyback}/{todaystr}')
    tnapf['fecha'] = pd.to_datetime(tnapf['fecha'], format='%Y-%m-%d')
    tnappersonales = request_to_dict_bcra(f'https://api.bcra.gob.ar/estadisticas/v2.0/DatosVariable/14/{oneyback}/{todaystr}')
    tnappersonales['fecha'] = pd.to_datetime(tnappersonales['fecha'], format='%Y-%m-%d')
    fig_tna,ax_tnapf = plt.subplots(figsize=(15,8))
    #plotting
    draw_lineplot(ax=ax_tnapf, data=tnapf,x='fecha', y='valor', color="#d0d7e0", label="TNA por depositos a 30 días en entidades financieras (BCRA)")
    #TNA Prestamos Personales
    draw_lineplot(ax=ax_tnapf, data=tnappersonales,x='fecha', y='valor', color="#7C9878", label="TNA de prestamos personales")
    ax_tnapf.set_title('Tasa de depositos y prestamos personales', fontsize=34, pad=10, weight='bold')
    ax_tnapf.set_xlabel('Fecha', fontdict={'size':12}, labelpad=10)
    ax_tnapf.set_ylabel('')
    fig_tna.savefig('./images/tna.png')


def draw_bm_plot():
    #procesing
    base_monetaria = request_to_dict_bcra(f"https://api.bcra.gob.ar/estadisticas/v2.0/DatosVariable/15/{oneyback}/{todaystr}/")
    base_monetaria['fecha'] = pd.to_datetime(base_monetaria['fecha'], format='%Y-%m-%d')
    circulante = request_to_dict_bcra(f"https://api.bcra.gob.ar/estadisticas/v2.0/DatosVariable/16/{oneyback}/{todaystr}/")
    circulante['fecha'] = pd.to_datetime(circulante['fecha'], format='%Y-%m-%d')
    #plotting
    fig_bm,ax_bm = plt.subplots(figsize=(15,8))
    ax_bm.ticklabel_format(style='plain')
    draw_lineplot(ax=ax_bm, data=base_monetaria, x="fecha", y="valor", color="#d0d7e0", label="Base monetaria")
    draw_lineplot(ax=ax_bm, data=circulante, x="fecha", y="valor", color="#7C9878", label="Circulación Monetaria")
    ax_bm.set_title('Base Monetaria en Millones de Pesos', fontsize=34, pad=12, weight='bold')
    ax_bm.set_ylabel('')
    ax_bm.set_xlabel('Fecha', fontdict={'size':12}, labelpad=10)
    fig_bm.savefig('./images/bm.png')