from flask import Flask, render_template, request
import pandas as pd
from sodapy import Socrata

# Connection with www.datos.gov.co

client = Socrata('www.datos.gov.co', None)
result = client.get('rik9-88u9',limit=294)

result_df = pd.DataFrame.from_records(result)
result_df.set_index('id_de_caso', inplace = True)

# Clean columns
result_df.drop(columns= ["fecha_reporte_web","ubicacion","departamento", "departamento_nom", "fecha_de_notificaci_n", "unidad_medida","fecha_inicio_sintomas","fecha_recuperado","per_etn_","fecha_muerte","pais_viajo_1_cod","pais_viajo_1_nom", "nom_grupo_"], inplace = True)

# Rename columns
result_df.columns=['Código Municipio',
                    'Municipio',
                    'Edad',
                    'Sexo',
                    'Fuente de Contagio',
                    'Estado',
                    'Recuperado',
                    'Fecha de Diagnostico',
                    'Tipo de Recuperación']

lista_municipios = []
for i in result_df['Municipio']:
  if i not in lista_municipios:
    lista_municipios.append(i)

app = Flask(__name__)


@app.route("/",methods=["GET","POST"])
def main():
    if request.method == 'POST':
        sexo = request.form.get("Sexo")
        estado = request.form.get("Estado")
        edad = request.form.get("Edad")
        municipio = request.form.get("Municipio")
        results_df = result_df
        # SEXO
        if sexo == 'Mujer':
            results_df = results_df[results_df["Sexo"] == "F"]

        if sexo == 'Hombre':
            results_df = results_df[results_df["Sexo"] == "M"]
        
        # ESTADO
        if estado == 'Fallecido':
            results_df = results_df[results_df["Estado"] == "Fallecido"] 

        if estado == 'Leve':
            results_df = results_df[results_df["Estado"] == "Leve"]

        # EDAD
        if edad == 'PrimeraInfancia':
            results_df = results_df[pd.to_numeric(results_df['Edad']) <= 5]
        
        if edad == 'Infancia':
            results_df = results_df[(pd.to_numeric(results_df['Edad']) >= 6) & (pd.to_numeric(results_df['Edad']) <= 11)]

        if edad == 'Adolescencia':
            results_df = results_df[(pd.to_numeric(results_df['Edad']) >= 12) & (pd.to_numeric(results_df['Edad']) <= 18)]
        
        if edad == 'Juventud':
            results_df = results_df[(pd.to_numeric(results_df['Edad']) >= 19) & (pd.to_numeric(results_df['Edad']) <= 26)]
        
        if edad == 'Adultez':
            results_df = results_df[(pd.to_numeric(results_df['Edad']) >= 27) & (pd.to_numeric(results_df['Edad']) <= 59)]

        if edad == 'PersonaMayor':
            results_df = results_df[ pd.to_numeric(results_df['Edad']) >= 60 ]
        
        # MUNICIPIO
        if municipio in lista_municipios:
            results_df = results_df[results_df["Municipio"] == municipio]

        return render_template('index.html',column_names=result_df.columns.values, row_data=list(results_df.values.tolist()), zip=zip, municipios = lista_municipios)
    else:
        return render_template('index.html',column_names=result_df.columns.values, row_data=list(result_df.values.tolist()), zip=zip, municipios = lista_municipios)


if __name__ == '__main__':
    app.run(debug=True)