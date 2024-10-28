from airflow.decorators import dag, task
from pendulum import datetime
from datetime import datetime as dt

from charts_sketcher import draw_bm_plot, draw_inflacion_plot, draw_tna_plot, draw_country_risk_plot
from tweet_writer import post_bm_plot, post_inflacion_plot, post_tna_plot, post_country_risk_plot

today = dt.today()
# datetime(today.year, today.month, today.day, 18),
@dag(
    start_date=dt(today.year, today.month, today.day),
    schedule="@daily",
    tags=["charts"],
    catchup=False
)
def sketch_rp():
    @task
    def draw_rp():
        draw_country_risk_plot()
        print('rp drawn')
    # draw_rp()
    @task
    def post_rp():
        post_country_risk_plot()
        print('rp posted')
    draw_rp() >> post_rp()
sketch_rp()
    
@dag(
    start_date=datetime(today.year, today.month, today.day),
    schedule="@daily",
    tags=["charts"],
    catchup=False
)
def sketch_bm_tna():
    @task
    def draw_bm():
        draw_bm_plot()
        print('bm drawn')
    # draw_bm()
    @task
    def draw_tna():
        draw_tna_plot()
        print('tna drawn')
    # draw_tna()
    @task
    def post_bm():
        post_bm_plot()
        print('bm posted')
    # post_bm()
    draw_bm() >> post_bm()
    @task
    def post_tna():
        post_tna_plot()
        print('tna posted')
    draw_tna() >> post_tna()
    # draw_bm() >> draw_tna >> post_bm() >> post_tna()
sketch_bm_tna()

@dag(
    start_date=dt(today.year, today.month, today.day),
    schedule="@daily",
    tags=["charts"],
    catchup=False
)
def sketch_bm():
    @task
    def draw_bm():
        draw_bm_plot()
        print('bm drawn')
    # draw_rp()
    @task
    def post_bm():
        post_bm_plot()
        print('bm posted')
    draw_bm() >> post_bm()
sketch_bm()

@dag(
    start_date=datetime(today.year, today.month, today.day),
    schedule="@monthly",
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
    

