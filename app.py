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

app = Flask(__name__)


@app.route("/",methods=["GET","POST"])
def main():
    if request.method == 'POST':
        sexo = request.form.get("Sexo")
        estado = request.form.get("Estado")
        results_df = result_df
        if sexo == 'Mujer':
            results_df = results_df[results_df["Sexo"] == "F"]

        if sexo == 'Hombre':
            results_df = results_df[results_df["Sexo"] == "M"]
        
        if estado == 'Fallecido':
            results_df = results_df[results_df["Estado"] == "Fallecido"] 

        if estado == 'Leve':
            results_df = results_df[results_df["Estado"] == "Leve"]
            
        return render_template('index.html',column_names=result_df.columns.values, row_data=list(results_df.values.tolist()), zip=zip)
    else:
        return render_template('index.html',column_names=result_df.columns.values, row_data=list(result_df.values.tolist()), zip=zip)


if __name__ == '__main__':
    app.run(debug=True)