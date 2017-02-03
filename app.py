
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators
from wtforms import  StringField, SubmitField

from os_queries import match_ip

app = Flask(__name__)


class ReusableForm(Form):
    ip = TextField('Floating IP:', validators=[validators.required()])


@app.route('/', methods=['GET', 'POST'])
def index():
    form = ReusableForm(request.form)
    if request.method == 'POST':

        ip=request.form['ip']
        if form.validate():
            info = match_ip(ip)
            return render_template('query.html', form=form, info=info)

    return render_template('query.html', form=form, info={"status":""})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
