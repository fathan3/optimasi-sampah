from flask import Flask, render_template, request, redirect, url_for
from models.scheduler import Scheduler

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title="Form Parameter Produksi")

@app.route('/process', methods=['POST'])
def process():
    max_time = int(request.form.get('max_time', 60))
    
    names = request.form.getlist('name[]')
    times = request.form.getlist('time_per_kg[]')
    values = request.form.getlist('value_per_kg[]')
    qtys = request.form.getlist('max_qty[]')
    
    materials = []
    for i in range(len(names)):
        if names[i].strip():
            materials.append({
                'name': names[i],
                'time_per_kg': int(times[i]),
                'value_per_kg': int(values[i]),
                'max_qty': int(qtys[i])
            })
            
    total_time_needed = 0
    total_value_expected = 0
    total_weight_expected = 0
    
    for m in materials:
        total_time_needed += (m['time_per_kg'] * m['max_qty'])
        total_value_expected += (m['value_per_kg'] * m['max_qty'])
        total_weight_expected += m['max_qty']
        
    scheduler = Scheduler()
    result_dp = None
    result_rr = None
    
    if total_time_needed > max_time:
        result_dp = scheduler.calculate_dp(materials, max_time)
        result_rr = scheduler.calculate_round_robin(materials, max_time)
        
    return render_template('result.html', 
                           title="Hasil Komparasi Penjadwalan",
                           materials=materials,
                           max_time=max_time,
                           total_time_needed=total_time_needed,
                           total_value_expected=total_value_expected,
                           total_weight_expected=total_weight_expected,
                           resultDP=result_dp,
                           resultRR=result_rr)

if __name__ == '__main__':
    app.run(debug=True)
