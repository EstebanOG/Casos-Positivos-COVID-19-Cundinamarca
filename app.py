from flask import Flask, render_template
import pandas as pd
from sodapy import Socrata

# Connection with www.datos.gov.co

client = Socrata('www.datos.gov.co', None)
result = client.get('rik9-88u9',limit=300)

result_df = pd.DataFrame.from_records(result)
result_df.set_index('id_de_caso', inplace = True)

result_df.drop(columns= ["fecha_reporte_web","ubicacion","departamento", "departamento_nom", "fecha_de_notificaci_n", "unidad_medida","fecha_inicio_sintomas","fecha_recuperado","per_etn_","fecha_muerte","pais_viajo_1_cod","pais_viajo_1_nom", "nom_grupo_"], inplace = True)
app = Flask(__name__)


@app.route("/")
def main():
    return render_template('index.html',column_names=result_df.columns.values, row_data=list(result_df.values.tolist()), zip=zip)



if __name__ == '__main__':
    app.run(debug=True)