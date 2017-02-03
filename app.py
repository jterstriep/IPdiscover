from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators
from wtforms import  StringField, SubmitField
from os_queries import match_ip

app = Flask(__name__)

class Reusableform(Form):
    ip = TextField('Floating IP:', validators=[validators.required()])


@app.route('/', methods=['GET', 'POST'])
def index():
    form = ReusableForm(request.form)

    print form.errors
    if request.method == 'POST':
        ip=request.form['ip']
        print "IP =", ip

        if form.validate():
            info = match_ip(ip)
            print info
            flash('found')
        else:
            flash('bad IP')

    return render_templates('query.html', form=form)


@app.route('/response')
def response():

    info = lookup_ip_info()
    if info:
        return render_template(
            "response.html",
            user=info['user'],
            user_email=info['user_email']
        )
    else:
        return render_template("unused.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
