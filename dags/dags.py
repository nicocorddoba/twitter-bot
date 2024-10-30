from airflow.decorators import dag, task
from pendulum import datetime

from charts_sketcher import draw_bm_plot, draw_inflacion_plot, draw_tna_plot, draw_country_risk_plot
from tweet_writer import post_bm_plot, post_inflacion_plot, post_tna_plot, post_country_risk_plot

# today = dt.today()

# Riesgo País
@dag(
    start_date=datetime(2024, 10, 29),
    # schedule="@daily",
    schedule_interval="30 20 * * 1-5",
    tags=["charts"],
    catchup=False
)
def sketch_rp():
    @task
    def draw_rp():
        return draw_country_risk_plot()
    
    @task
    def post_rp(fecha):
        post_country_risk_plot(fecha)
        print('rp posted')
    post_rp(draw_rp())
sketch_rp()
    
# (Base Monetaria y Circulación Monetaria), (Tasa de depositos y prestamos personales)
@dag(
    start_date=datetime(2024, 10, 29),
    schedule_interval="0 21 * * 1",
    tags=["charts"],
    catchup=False
)
def sketch_bm_tna():
    @task
    def draw_bm():
        draw_bm_plot()
        print('bm drawn')
    # draw_bm()
    # @task
    # def draw_tna():
    #     draw_tna_plot()
    #     print('tna drawn')
    # # draw_tna()
    @task
    def post_bm():
        post_bm_plot()
        print('bm posted')
    # post_bm()
    draw_bm() >> post_bm()
    # @task
    # def post_tna():
    #     post_tna_plot()
    #     print('tna posted')
    # draw_tna() >> post_tna()
    # draw_bm() >> draw_tna >> post_bm() >> post_tna()
sketch_bm_tna()

# Inflacion
@dag(
    start_date=datetime(2024, 10, 29),
    schedule_interval="1 19 10 * *",
    tags=["charts"],
    catchup=False
)
def sketch_inflation():
    @task
    def draw_inflation():
        draw_inflacion_plot()
        print('inflation drawn')
    # draw_rp()
    @task
    def post_inflation():
        post_inflacion_plot()
        print('inflation posted')
    draw_inflation() >> post_inflation()
sketch_inflation()
    

