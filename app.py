import pickle

from flask import Flask, render_template, request
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
model = pickle.load(open('Random_forest_regressor_model.pkl', 'rb'))


@app.route('/', methods=['GET'])
def Home():
    return render_template('cardekho.html')


standard_to = StandardScaler()


@app.route("/Prediction_page", methods=['POST'])
def predict():
    Fuel_Type_Diesel = 0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Year = 2020 - Year
        Present_Price = float(request.form['Price'])
        Kms_Driven = int(request.form['Kms_driven'])
        Owner = int(request.form['Owner'])
        Fuel_Type_Petrol = request.form['Fuel_Type_Petrol']
        if Fuel_Type_Petrol == 'Petrol':
            Fuel_Type_Petrol = 1
            Fuel_Type_Diesel = 0
        elif Fuel_Type_Petrol == 'Diesel':
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 1
        else:
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 0

        Seller_Type_Individual = request.form['Seller_Type']
        if Seller_Type_Individual == 'Individual':
            Seller_Type_Individual = 1
        else:
            Seller_Type_Individual = 0
        Transmission_Manual = request.form['Transmission_type']
        if Transmission_Manual == 'Manual':
            Transmission_Manual = 1
        else:
            Transmission_Manual = 0

    prediction = model.predict([[Present_Price, Kms_Driven, Owner, Year, Fuel_Type_Diesel, Fuel_Type_Petrol,
                                 Seller_Type_Individual, Transmission_Manual]])
    print(prediction)
    output = round(prediction[0], 2)

    if output > 0:
        return render_template('cardekho.html', prediction_text="You Can Sell The Car at {} lakhs".format(output))
    else:
        return render_template('cardekho.html', prediction_text="Sorry you cannot sell this car")

    return render_template('cardekho.html')


if __name__ == "__main__":
    app.run(debug=True)
