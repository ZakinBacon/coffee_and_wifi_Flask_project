from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

#Setting up the form
class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Location (Google Maps link)', validators=[DataRequired(), URL()]) # Makes sure the input is a URL
    open_time = SelectField("Opening time", choices=[('5am'),('6am'),('7am'),('8am'),('9am'),('10am'),('11am'),('12pm'),], validators=[DataRequired()])
    closing_time = SelectField("Closing time",
                            choices=[('5pm'), ('6pm'), ('7pm'), ('8pm'), ('9pm'), ('10pm'), ('11pm'), ('12am'), ],
                            validators=[DataRequired()])

    coffee = SelectField('Coffee', choices=[('☕'), ('☕☕'), ('☕☕☕'), ('☕☕☕☕'), ('☕☕☕☕☕'), ('✘')], validators=[DataRequired()])
    wifi = SelectField('Wifi Strength', choices=[('💪'), ('💪💪'), ('💪💪💪'), ('💪💪💪💪'), ('💪💪💪💪💪'), ('✘')], validators=[DataRequired()])
    power = SelectField('Selection of Outlets', choices=[('🔌'), ('🔌🔌'), ('🔌🔌🔌'), ('🔌🔌🔌🔌'), ('🔌🔌🔌🔌🔌'),('✘')], validators=[DataRequired()])

    submit = SubmitField('Submit')

# all Flask routes
@app.route("/")
def home():
    return render_template("index.html")


# Route for adding new cafes
@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open('./cafe-data.csv', "a", newline='', encoding='utf-8') as csv_file:
            formwriter = csv.writer(csv_file)
            form_data = [] # List to write to the CSV
            # Adding all the form data to the list
            form_data.append(form.cafe.data)
            form_data.append(form.location.data)
            form_data.append(form.open_time.data)
            form_data.append(form.closing_time.data)
            form_data.append(form.coffee.data)
            form_data.append(form.wifi.data)
            form_data.append(form.power.data)
            formwriter.writerow(form_data) # Writes to the CSV
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('./cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
