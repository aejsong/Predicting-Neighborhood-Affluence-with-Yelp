from flask import Flask, render_template, request, g, session
import pandas as pd
import numpy as np
import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import json
import requests
import pickle
import folium

# create flask app
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# secret key to perform certain actions
app.secret_key = 'sdfgsdgfdgfgfdgd'



# create index
@app.route('/')
def index():
    la_coord = (34.0522, -118.2437)
    maps = folium.Map(location=la_coord, zoom_start=11)

    maps.save('./static/maps.html')

    return render_template("index.html",map_source='./static/maps.html')



# team page
@app.route('/team/')
def team():

    return render_template("team.html")




# prediction function
def affluency_predictor(to_predict):
    # format the variable
    session_int = int(to_predict.strip())
    df = pd.read_csv("../data/X_cluster.csv")
    df = df[['zip_code', 'count', 'review_count', 'price*review_count', 'price_1', 'price_2',
     'price_3', 'price_4', 'rating_0.0', 'rating_1.0', 'rating_1.5',
      'rating_2.0', 'rating_2.5', 'rating_3.0', 'rating_3.5', 'rating_4.0',
      'rating_4.5', 'rating_5', 'cluster_0', 'cluster_1', 'cluster_2',
      'cluster_3', 'cluster_4', 'cluster_5', 'cluster_6', 'cluster_7',
      'cluster_8', 'cluster_9', 'cluster_10', 'cluster_11', 'cluster_12',
      'cluster_13', 'cluster_14', 'cluster_15', 'cluster_16', 'cluster_17',
      'cluster_18', 'cluster_19', 'cluster_20', 'cluster_21', 'cluster_22',
      'cluster_23', 'cluster_24', 'cluster_25', 'cluster_26', 'cluster_27',
      'cluster_28', 'cluster_29', 'cluster_30', 'cluster_31', 'cluster_32',
      'cluster_33', 'cluster_34', 'cluster_35', 'cluster_36', 'cluster_37',
      'cluster_38', 'cluster_39', 'cluster_40', 'cluster_41', 'cluster_42',
      'cluster_43', 'cluster_44', 'cluster_45']]
    # create array from dataframe row
    predict_array = df[df['zip_code'] == session_int]
    print(predict_array)
    # load trained model
    loaded_model = pickle.load(open("model.p", "rb"))
    # predict
    result = loaded_model.predict(predict_array)
    print(result)
    print('------------')

    map_df = pd.read_csv('../data/data_zipcode.csv')
    la_coord = (34.0522, -118.2437)
    maps = folium.Map(location=la_coord, zoom_start=11)

    maps.save('./static/maps.html')

    for each in map_df.iterrows():
        if int(each[1]['zip_code']) == session_int:
            popup_text = folium.Html(f"""
                <strong>Zip Code: {each[1]["zip_code"].astype(int)}</strong>
                </br>Avg. 2013 IRS Income (Thousands): {each[1]["ave_agi"].round(3)}
                </br>Predicted Income (Thousands): {np.exp(result[0]).round(2)}
                </br>Avg. $ of Businesses: {each[1]["price"].round(3)}
                </br> Number of Businesses: {int(each[1]["count"])}""",
                script=True)

            popup = folium.Popup(popup_text, max_width=2650, show=True)

            coord = (each[1]['latitude'],each[1]['longitude'])

            maps = folium.Map(location=coord, zoom_start=13)


            folium.Marker(
                location = [each[1]['latitude'],each[1]['longitude']],
                popup=popup,
                clustered_marker = True).add_to(maps)

            maps.save('./static/maps.html')




    return result[0]



# when submit a zipcode
@app.route('/process', methods=["POST"])
def process():
    if request.method == 'POST':

        results = np.exp(affluency_predictor(request.form['rawtext']))

        # session variable
        session['text'] = request.form['rawtext']

        print(results)

        df2 = pd.read_csv('../data/X_cluster.csv')

        index = df2['zip_code'].values.tolist().index(int(session['text'].strip())) #returns 0

        listofprices = []
        for i in range(0, 1):
            p1 = df2['price_1'][index]
            listofprices.append(p1)

            p2 = df2['price_2'][index]
            listofprices.append(p2)

            p3 = df2['price_3'][index]
            listofprices.append(p3)

            p4 = df2['price_4'][index]
            listofprices.append(p4)

            objects = ['$', '$$', '$$$', '$$$$']

            y = listofprices


        fig = go.Figure(data = [
            go.Bar(
            x=objects, y=listofprices
            )
        ])

        fig.update_layout(
            title="Yelp $ Dist. for Zip Code",
            xaxis_title="Number of $ on Yelp",
            yaxis_title="Number of Businesses",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="#7f7f7f"
            )
        )



        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        bargraph=graphJSON

        count = df2[df2['zip_code'] == int(session['text'].strip())]['count']

        return render_template("index.html",results=np.round(results,2), map_source='./static/maps.html', plot=bargraph, count=int(count))





if __name__ == "__main__":
    app.run(debug=True)
