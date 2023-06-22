# Proyecto Individual: Sistema de Recomendación de Películas

Este repositorio es un proyecto individual cuyo objetivo es el desarrollo y despliegue de una API de recomendación de películas diseñada para proporcionar información diversa sobre películas, actores y directores. Ha sido construida utilizando el marco FastAPI y un conjunto de datos de películas estructurado y procesado con librerías de lenguaje Python. La API permite consultar información sobre películas, actores y directores a través de varias rutas y funcionalidades. Este proyecto fue desarrollado durante la etapa de Labs del _(bootcamp)_ de Henry. A continuación, se describen cada una de las etapas en las que se organizó el proyecto.

**`Preprocesamiento`**

Se realizaron algunas transformaciones a los datasets originales tales como:

+ Se eliminaron las filas integralmente duplicadas en ambos datasets y se identificaron los registros con datos inconsistentes.

+ Los valores nulos del campo **`budget`** fueron imputados con el número **`0`**. Se eliminaron los registros con valores nulos en las variables **`id`** y **`release_date`**.

+ Algunos campos tienen datos anidados por lo que se desanidaron y se extrajeron los datos necesarios. En el caso de la variable **`crew`** se extrajeron los nombres de todos los actores y para **`cast`**, se hizo lo propio con el nombre del director, creándose las variables **`actor`** y **`director`**, respectivamente.

+ Se realizó el cambio de formato en el campo **`release_date`** a **`AAAA-mm-dd`** y, posteriormente, se crearon los campos **`release_year`** y **`release_month`**, que corresponden al año y mes de estreno de cada película.

+ Se creó la columna con el retorno de inversión, llamada **`return`** como resultado de la relación entre con los campos **`revenue`** y **`budget`**. En los casos que la división no fue posible, se asignó el valor **`0`**.

+ Las columnas que no se utilizaron para en esta primera versión de la API, fueron eliminadas; a saber: **`video`**,**`imdb_id`**,**`adult`**,**`original_title`**,**`poster_path`** y **`homepage`**.

+ Los datasets fueron combinados a partir del campo **`id`**.

+ Se creó la variable **`recs`**, la cual contiene una lista de películas similares y que es utilizada por la API para el sistema de recomendación. La similaridad entre películas fue calculada a partir de una matriz de similaridad coseno utilizando la frecuencia de términos-frecuencia inversa del documento (**`tf-idf`**) en los campos **`title`** y **`overview`**.

+ Con la intención de volver más eficientes las consultas, se crearon datasets particulares para cada función de la API.

Estas tareas se realizaron en una [Jupyter Notebook](https://github.com/picassojp/Henry-PI-MLops/blob/a233f3ed614419a95a80772bd9061144ebad1989/Henry_PI_MLops.ipynb) en el entorno de Google Colab. Se utilizaron librerías como Pandas, Numpy, Json, Matplotlib.pyplot y Scikit-learn.

**`Análisis exploratorio de los datos`**: _(Exploratory Data Analysis-EDA)_

Como primera aproximación a los datos se realizó un resumen estadístico con medidas de tendencia central. Se analizaron las distribuciones de las variables de puntaje promedio (**`vote_average`**) y cantidad de votos/calificaciones (**`vote_count`**), encontrándose como más frecuentes las calificaciones entre 6 y 7 puntos, y una gran mayoría de películas con menos de 2000 calificaciones. En cuanto a los géneros, los 3 más frecuentes en términos relativos son drama (22.2%), comedia (14.5%) y _(thriller)_(8.4%).

También se analizaron las nubes de palabras de los campos **`overview`** y **`title`**.

Entre las variables de recaudación (**`revenue`**), presupuesto (**`budget`**) y retorno de inversión (**`return`**) se revisaron las correlaciones de _(pearson)_. Hallándose una correlación positiva (0.77) entre el presupuesto y la recaudación.

Al analizar las fechas de estreno, se detectó un crecimiento en la cantidad de lanzamientos hasta el año 2014. Posteriormente, la tendencia fue decreciente hasta el año 2020 (última película registrada). Esta tendencia puede reflejar una menor contabilización de películas luego del año 2014, es decir, una desactualización de la base de datos junto con una efectiva menor cantidad de estrenos. Se debería profundizar en futuros análisis.

Finalmente, se analizaron métricas relacionadas a los directores (**`budget`**) como cantidad de películas dirigidas, retorno total y promedio. Si bien entre las últimas dos métricas no se detectaron cambios en los primeron 10 puestos, los directores con mayor cantidad de películas resultaron muy diferentes.

Este EDA se puede consultar en la sección 4 de la [Jupyter Notebook](https://github.com/picassojp/Henry-PI-MLops/blob/a233f3ed614419a95a80772bd9061144ebad1989/Henry_PI_MLops.ipynb). Se utilizaron librerías como Pandas, Numpy, Json, Seaborn, Matplotlib.pyplot y Wordcloud.
#API


**`Desarrollo de la API y despliegue`**

La API fue desarrollada con el entorno de trabajo [FastAPI](https://fastapi.tiangolo.com/) en lenguaje Python. Se optó por este _(web framework)_ por su buena performance y la facilidad de poder ser construido en un lenguaje sumamente difundido con Python. El [código principal](https://github.com/picassojp/Henry-PI-MLops/blob/a233f3ed614419a95a80772bd9061144ebad1989/main.py) cuenta con las funciones para cada uno de los _(endpoints)_. Además, se pueden consultar las [librerías](https://github.com/picassojp/Henry-PI-MLops/blob/a233f3ed614419a95a80772bd9061144ebad1989/requirements.txt) necesarias para su funcionamiento.

El despliegue (_(deployment)_) lo realicé como un _(web service)_ en la nube de [Render](https://render.com/). La configuración utilizada se puede consultar [aquí](https://github.com/HX-FNegrete/render-fastapi-tutorial.git). Esta opción resultó sumamente ágil para los fines del presente proyecto, además de contar con un plan gratuito. La documentación sobre el servicio se encuentra disponible [aquí](https://pi-juanpablopicasso.onrender.com/docs).


Consultas disponibles de la [API](https://pi-juanpablopicasso.onrender.com)
+ Cantidad de filmaciones por mes: Permite consultar la cantidad de películas que fueron estrenadas en el mes consultado (en idioma español).
+ Cantidad de filmaciones por día de la semana: Permite consultar la cantidad de películas que fueron estrenadas en el día de la semana consultado (en idioma español).
+ Puntuación de una película: Permite consultar el título de la película consultada, el año de estreno y su puntuación en términos de popularidad según TMDB (TheMoviesDataBase).
+ Votos de una película: Devuelve el promedio de votos de la película consultada junto con el año de estreno y la cantidad total de votos según TMDB (TheMoviesDataBase). La película debe contar con al menos 2000 votos para ser considerada en la consulta.
+ Información de actores: Devuelve la cantidad de películas en las que el actor consultado ha participado, el retorno total conseguido y el retorno promedio por película.
+ Información de directores: Devuelve el retorno total conseguido por las películas del director consultado y un detalle con 5 de sus películas, incluyendo título, fecha de lanzamiento, retorno, presupuesto y recaudación de cada una.
+ Recomendación de películas: Devuelve 5 títulos de películas similares al título de la película consultada. Las recomendaciones se basan en el criterio detallado en la sección de **Preprocesamiento**.


**`Demo`**

Se encuentra disponible una [demo](https://youtu.be/YZQAjoHNTKk) sobre el funcionamiento de la API mediante ejemplos de consultas.

**`Fuente de datos`**
Los _(datasets)_ utilizados se encuentran disponibles en esta [carpeta](https://drive.google.com/drive/folders/1dx1scrL8qucZNLqYr2nHYN5e5F3RoBUx?usp=sharing) de Google Drive, separados en originales (sin transformaciones) y los resultantes del preprocesamiento. El diccionario de los datos originales se puede consultar [aquí](https://docs.google.com/spreadsheets/d/1jj7hjkZvZUYnUsAt4mYjYtyhENWs94r4/edit?usp=sharing&ouid=103874252439240375729&rtpof=true&sd=true).

**`Mantenimiento`**
Este proyecto está mantenido por Juan Pablo Picasso. Si tienes alguna pregunta o encuentras algún problema, por favor, [contactame](https://www.linkedin.com/in/picassojp).
