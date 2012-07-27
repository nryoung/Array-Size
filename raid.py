from flask import Flask, render_template, url_for, request
from wtforms import Form, DecimalField, validators, RadioField
import os
app = Flask(__name__)

class RaidForm(Form):
    """
    Form class that represents main form in the arraysize app.
    """
    num_disks = DecimalField(u'Number of Disks:', [validators.Required(), validators.NumberRange(min=1)], places=2)
    sod = DecimalField(u'Size of Disks:', [validators.Required(), validators.NumberRange(min=1)], places=2)
    raid_type = RadioField(u'Raid Type', choices=[('1', 'RAID 0:'), ('2', 'RAID 1:'), ('3', 'RAID 10:'), ('4', 'RAID 5:'), ('5', 'RAID 6:')])

def calc_array_size(num_disks, sod, raid_type):
    """
    Function that calculates RAID array size.
    
    Uses lambda functions and converts the result in to a float
    for a more accurate size.
    """
    x = 0
    array_size = {
       1 : lambda x: float(num_disks * sod),
       2 : lambda x: float(sod),
       3 : lambda x: float((num_disks * sod) / 2),
       4 : lambda x: float((sod * (num_disks - 1))),
       5 : lambda x: float((sod * (num_disks - 2))),
    }[raid_type](x)

    ads = float((array_size * 1000000000) / 1073741824)
    return { 'array_size' : array_size, 'ads' : ads }

@app.route('/', methods=['GET', 'POST'])
def raid():
    """
    Main function in the ArraySize app.

    Renders the main page and passes all the correct vars. if POST.
    """
    form = RaidForm(request.form)

    if request.method == 'POST' and form.validate():
        num_disks = int(form.num_disks.data)
        sod = int(form.sod.data)
        raid_type = int(form.raid_type.data)
        result = calc_array_size(num_disks, sod, raid_type)    
        arrs = result['array_size']
        acds = result['ads']
        variables = {
            'array_size' : arrs,
            'ads' : acds,
        }
        return render_template('main_page.html', form=form, **variables) 

    else:
        return render_template('main_page.html', form=form)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
