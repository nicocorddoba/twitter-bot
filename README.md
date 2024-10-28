# twitter-bot: Bot de Twitter

Uso
------------
Debes crear un archivo '.env' en la carpeta plugins con los siguientes campos (obtenidos en https://developer.x.com/en/portal/):

    consumer_key=
    consumer_secret=
    access_token=
    access_token_secret=
    bearer_token=
    
¡Necesitas tener instalado Docker!

Primero debes clonar el proyecto:

    git clone https://github.com/nicocorddoba/twitter-bot
    
En la consola, con docker iniciado, debes ejecutar el siguiente comando en la carpeta del proyecto para construir la imagen de docker necesaria:

    docker build -t airflow-image .

Luego necesitas inicializarlo con:

    docker compuse airflow-init

Y por último deberas ejecutar:

    docker compuse up
