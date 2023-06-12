import pandas as pd
import datetime
from datetime import datetime
from fastapi import FastAPI
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import joblib
import ast 

#app = FastAPI()
description = """
Este sistema de recomendación de películas permite conocer los títulos. 🚀

## Items


## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

app = FastAPI(
    title="Sistema de Recomendación de Películas",
    description=description,
    version="0.0.1",
    contacto={
        "name": "Juan Pablo Picasso",
        "GitHub": "https://github.com/picassojp",
        "email": "picassojuanpablo@gmail.com",
    },
)
# Se carga el df con los datos de las peliculas
# df_movies = pd.read_csv(r'Datasets/movies_dataset_v2.csv', sep = ',', header = 0, parse_dates=["release_date"])
#df_movies = pd.read_csv(r'Datasets/movies_dataset_v2.csv', sep = ',', header = 0, usecols=['id', 'title', 'release_date', 'cast', 'director', 'overview', 'popularity', 'vote_average', 'vote_count', 'return', 'release_year', 'budget', 'revenue'], parse_dates=["release_date"])

df_movies_mesydia = pd.read_csv(r'Datasets/movies_dataset_v2_mesydia.csv', sep = ',', header = 0, parse_dates=["release_date"])
df_movies_score = pd.read_csv(r'Datasets/movies_dataset_v2_score.csv', sep = ',', header = 0)
df_movies_votos = pd.read_csv(r'Datasets/movies_dataset_v2_votos.csv', sep = ',', header = 0)
df_movies_actor = pd.read_csv(r'Datasets/movies_dataset_v2_actor.csv', sep = ',', header = 0)
df_movies_director = pd.read_csv(r'Datasets/movies_dataset_v2_director.csv', sep = ',', header = 0)
df_movies_director=df_movies_director.loc[-df_movies_director.director.isna()]
df_movies_recs = pd.read_csv(r'Datasets/movies_dataset_v2_recs.csv', sep = ',', header = 0)

# Funciones 
@app.get('/') #ruta raíz
def get_root():
    return 'API para consulta de datos de películas'

# cantidad_filmaciones_mes
@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes:str):
    """
    Esta función devuelve la cantidad de películas que fueron estrenadas en el mes consultado (en idioma español)
    """
    # función para convertir el mes en idioma español al formato adecuado para la consulta
    def mes_to_numero(mes):
        # Diccionario para mapear los nombres de los meses en español a su equivalente en inglés
            meses_ingles = {
                'enero': 'January',
                'febrero': 'February',
                'marzo': 'March',
                'abril': 'April',
                'mayo': 'May',
                'junio': 'June',
                'julio': 'July',
                'agosto': 'August',
                'septiembre': 'September',
                'octubre': 'October',
                'noviembre': 'November',
                'diciembre': 'December'
            }
            
            # se verifica si el mes se ingreso como str
            #if isinstance(mes,str):
            mes = mes.lower() #se pasa a minuscula
            # else:
            #     return print("Ingrese el nombre del mes que desea consultar. Ejemplo: 'julio'.")
                    
            #if mes in meses_ingles: #Verificar si el nombre del mes está en el diccionario
            mes_ingles = meses_ingles[mes]
                # Convertir el nombre del mes a formato de fecha
            numero_mes = int(datetime.strptime(mes_ingles, "%B").strftime("%m"))
            return numero_mes            
            #     return print("Ingrese el nombre del mes que desea consultar. Ejemplo: 'julio'.")
    
    n_mes = mes_to_numero(mes)
    cant = int(df_movies_mesydia[df_movies_mesydia.release_date.dt.month == n_mes].id.count())
      
    return {'mes': mes, 'cantidad': cant}  
    # return f'{str(df_movies[df_movies.release_date.dt.month == mes_to_numero(mes)].id.count())} películas se estrenaron en el mes de {mes}'

# cantidad_filmaciones_dia
@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia:str):
    """
    Esta función devuelve la cantidad de películas que fueron estrenadas en el día consultado (en idioma español)
    """
    # función para convertir el mes en idioma español al formato adecuado para la consulta    
    def eng_day(dia):
    # Diccionario para mapear los nombres de los días en español con el número (inicio semana lunes = 0)
        dias_ingles = {
            'lunes': 0,
            'martes': 1,
            'miércoles': 2,
            'jueves': 3,
            'viernes': 4,
            'sábado': 5,
            'domingo': 6
        }
        # se verifica si el dia se ingreso como str
        if isinstance(dia,str):
            dia = dia.lower() #se pasa a minuscula
        # else:
        #     return print("Ingrese el nombre del día que desea consultar. Ejemplo: 'martes'.")
        if dia in dias_ingles: #Verificar si el día es correcto
            dia_ingles = dias_ingles[dia]          
            return int(dia_ingles)
        # else:
        #     return print("Ingrese el nombre del día que desea consultar. Ejemplo: 'martes'.")
    n_dia = eng_day(dia)
    cant = int(df_movies_mesydia[df_movies_mesydia.release_date.dt.weekday == n_dia].shape[0])
    # return f'{str(df_movies[df_movies.release_date.dt.weekday == eng_day(dia)].shape[0])} películas se estrenaron en un día {dia}'
    return {'dia': dia, 'cantidad': cant}

@app.get("/score_titulo/{titulo}")
def score_titulo(titulo:str): 
    """
    Esta funcion devuelve el título de la película consultada junto con el año de estreno y el score
    """
    # se verifica si el titulo es un str
    if isinstance(titulo,str):
        titulo = titulo.lower() #se pasa a minuscula
    else:
        return f'No fue posible encontrar el título {str(titulo)} en nuestra base de datos. Verificar si es correcto o probar con un título alternativo en español.'
    df_score = df_movies_score.loc[df_movies_score.title.str.lower().str.contains(titulo),["title", "release_year", "popularity"]].iloc[0]
    print(df_score)
    titulo = str(df_score.title)
    anio = int(df_score.release_year)
    score = float(df_score.popularity.round(2))
    if anio is None:
        return f'No fue posible encontrar el título {titulo} en nuestra base de datos. Verificar si es correcto o probar con un título alternativo en español.'
    else:
        # return f'La película "{titulo}" fue estrenada en el año {str(year)} y tiene una popularidad de {str(score)}'
        return {'titulo': titulo, 'anio': anio, 'popularidad': score}

@app.get("/votos_titulo/{titulo}")
def votos_titulo(titulo:str):
    """
    Esta funcion devuelve el promedio de votos de la pelicula junto con la cantidad de votos. En caso de ser una cantidad de votos menor a 2000, se informa solamente el incumplimiento de esta condición.
    """ 
    # se verifica si el titulo es un str
    if isinstance(titulo,str):
        titulo = titulo.lower() #se pasa a minuscula
    else:
        return f'No fue posible encontrar el título {titulo} en nuestra base de datos. Verificar si es correcto o probar con un título alternativo en español.'
    
    df_votos = df_movies_votos.loc[df_movies_votos.title.str.lower().str.contains(titulo),["title", "release_year", "vote_average", "vote_count"]].iloc[0]
    titulo = str(df_votos.title)
    anio = int(df_votos["release_year"])
    voto_promedio = float(df_votos.vote_average.round(2))
    voto_total = int(df_votos["vote_count"])
    
    if anio is None:
        return f'No fue posible encontrar el título {titulo} en nuestra base de datos. Verificar si es correcto o probar con un título alternativo en español.'
    elif voto_total < 2000:
        return f'El título {titulo} no cuenta con la cantidad suficiente de valoraciones por lo que no es posible informar la valoración promedio.'
    else:
        #return f'La película "{titulo}" fue estrenada en el año {year}. La valoración promedio es de {voto_promedio}, resultado de {votos_cant} votaciones.'
        return {'titulo': titulo, 'anio': anio, 'voto_total': voto_total, 'voto_promedio': voto_promedio}


@app.get("/get_actor/{nombre_actor}")
def get_actor(nombre_actor:str): 
    """
    Esta funcion devuelve el actor consultado junto con la cantidad de peliculas en las que participo, el retorno total conseguido y el retorno promedio por película.
    """
    if isinstance(nombre_actor,str):
        nombre_actor = nombre_actor.lower() #se pasa a minuscula
    else:
        return f'No fue posible encontrar el actor "{nombre_actor}" en nuestra base de datos. Verificar si es correcto o probar con un nombre alternativo en español.'
    
    fila = ast.literal_eval(df_movies_actor.loc[df_movies_actor.actor.str.lower().str.contains(nombre_actor),"actor"].iloc[0])
    for i in fila:
        if nombre_actor in i.lower():
            nombre_actor = i
            print(nombre_actor)
    cant = int(df_movies_actor.loc[df_movies_actor.actor.str.contains(nombre_actor),"id"].shape[0])
    retorno_total = float(df_movies_actor.loc[df_movies_actor.actor.str.contains(nombre_actor),"return"].sum().round(2))
    retorno_prom = float(df_movies_actor.loc[df_movies_actor.actor.str.contains(nombre_actor),"return"].mean().round(2))
    
    if cant is None:
        return f'No fue posible encontrar películas del actor "{nombre_actor}" en nuestra base de datos. Verificar si es correcto o probar con un nombre alternativo en español.'
    else:
        return {'actor': nombre_actor, 'cantidad_filmaciones': cant, 'retorno_total': retorno_total, 'retorno_promedio': retorno_prom}

@app.get("/get_director/{nombre_director}")
def get_director(nombre_director:str):
    """
    Esta funcion devuelve el director consultado junto el retorno total conseguido por sus películas y un detalle de sus películas con fecha de lanzamiento, retorno, costo y ganancia.
    """
    if isinstance(nombre_director,str):
        nombre_director = nombre_director.lower() #se pasa a minuscula
    else:
        return f'No fue posible encontrar el director "{nombre_director}" en nuestra base de datos. Verificar si es correcto o probar con un nombre alternativo en español.'
    
    df_director = df_movies_director.loc[-df_movies_director.director.isna()]
    
    nombre_director = str(df_director.loc[df_director.director.str.lower().str.contains(nombre_director),"director"].iloc[0]) #se obtiene el nombre del director
    cant = int(df_director.loc[df_director.director==nombre_director,"id"].shape[0]) #se revisa la cantidad de registros de ese director
    retorno_total = float(df_director.loc[df_director.director==nombre_director,"return"].sum().round(2)) #se calcula el retorno total del director
    
    df_peliculas = df_director.loc[df_director.director == nombre_director,["title", "release_year", "return", "budget", "revenue", "director"]].head(5).sort_values(by="release_year", ascending=False) #se limita la cantidad de peliculas
    
    #se pasan las variables a formato lista
    peliculas = df_peliculas.title.tolist()
    anios = df_peliculas.release_year.tolist()
    retornos = df_peliculas['return'].tolist()
    budget = df_peliculas.budget.tolist()
    revenue = df_peliculas.revenue.tolist()
    
    if cant is None:
        return f'No fue posible encontrar películas del director "{nombre_director}" en nuestra base de datos. Verificar si es correcto o probar con un nombre alternativo en español.'
    else:
        # return f'El director "{nombre_director}" ha alcanzado un retorno total de {retorno_total} con sus películas, lo que da una idea de su éxito. Las películas que dirigió fueron: \n {peliculas}'
        return {'director': nombre_director, 'retorno_total_director': retorno_total, 'peliculas': peliculas, 'anio': anios, 'retorno_pelicula': retornos,'budget_pelicula':budget,'revenue_pelicula':revenue}


@app.get("/recomendacion/{titulo}")
def recomendacion(titulo:str):
    recs = df_movies_recs.loc[df_movies_recs.title.str.lower().str.contains(titulo), 'recs'].iloc[0]
    recs = ast.literal_eval(recs)
    return {'lista recomendada': recs}
 
# Deta Details
"""
{
        "name": "PI-JuanPabloPicasso",
        "id": "",
        "project": "default",
        "runtime": "python3.10",
        "endpoint": "",
        "region": "us-east-1",
        "dependencies": [
                "fastapi",
                "pandas",
                "datetime",
                "ast"
        ],
        "visor": "disabled",
        "http_auth": "disabled"
}
"""