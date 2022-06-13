from flask import Flask, render_template
import pandas as pd
from sodapy import Socrata

# Connection with www.datos.gov.co

client = Socrata('www.datos.gov.co', None)
result = client.get('rik9-88u9',limit=100)

result_df = pd.DataFrame.from_records(result)
result_df

app = Flask(__name__)


@app.route("/")
def hello_world():
    #return render_template('index.html', tables=[result_df.to_html(classes='data')])
    return render_template('index.html',column_names=result_df.columns.values, row_data=list(result_df.values.tolist()), zip=zip)



if __name__ == '__main__':
    app.run(debug=True)