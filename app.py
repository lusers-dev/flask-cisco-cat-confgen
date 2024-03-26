import sys
import os
import re
from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = "this-secret-is-for-flask-fcc4901b8046255f1591e982be51fc3d"


def replace_words(base_text, device_values):
    for key, val in list(device_values.items()):
        base_text = base_text.replace(key, val)
    return base_text


@app.route("/")
def index():
    flash("Enter Information Below")
    return render_template("index.html")


@app.route("/process", methods=['POST', 'GET'])
def process():
    output = None
    device = {}
    device["##hostname##"] = str(request.form['sw_name'])
    device["##ip_add##"] = str(request.form['sw_ip'])
    device["##mask_add##"] = str(request.form['sw_netmask'])
    device["##gw_add##"] = str(request.form['sw_gateway'])
    device["##location##"] = re.sub('_',' ',str(request.form['sw_location']))
    device["##location##"] = re.sub('@','&',device["##location##"])
          
    device["##mgmt_vlan##"] = str(request.form['sw_mgmt_vlan'])
    device["##voip_vlan##"] = str(request.form['data_voip_vlan'])
    device["##auth_vlan##"] = str(request.form['data_auth_vlan'])
    device["##general_vlan##"] = str(request.form['data_gen_vlan'])

    try:
        template_file = None
        template_file = '{}/{}'.format(
                         'templates',
                         str(request.form['template'])
                         )
        t = open(template_file, 'r')
        tempstr = t.read()
        t.close()

        output = replace_words(tempstr, device)
        flash(output)

    except Exception as e:
        flash(e)
        pass
      
    return render_template("process.html")


