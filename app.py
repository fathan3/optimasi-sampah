from flask import Flask, render_template, request, redirect, url_for
from models.scheduler import Scheduler

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title="OptiPro - Parameter")

@app.route('/process', methods=['POST'])
def process():
    # cek input batas waktu, kalau error default ke 60 menit
    try:
        max_time = int(request.form.get('max_time', 60))
        if max_time < 0: max_time = 60
    except ValueError:
        max_time = 60
    
    names = request.form.getlist('name[]')
    times = request.form.getlist('time_per_kg[]')
    values = request.form.getlist('value_per_kg[]')
    qtys = request.form.getlist('max_qty[]')
    
    # kumpulin dan ngecek data material dari form
    materials = []
    for i in range(len(names)):
        name = names[i].strip()
        if name:
            try:
                t_kg = int(times[i]) if i < len(times) else 0
                v_kg = int(values[i]) if i < len(values) else 0
                m_qty = int(qtys[i]) if i < len(qtys) else 0
                
                if t_kg > 0 and v_kg >= 0 and m_qty > 0:
                    materials.append({
                        'name': name,
                        'time_per_kg': t_kg,
                        'value_per_kg': v_kg,
                        'max_qty': m_qty
                    })
            except ValueError:
                continue
            
    # hitung total waktu dan estimasi nilai
    total_time_needed = 0
    total_value_expected = 0
    total_weight_expected = 0
    
    for m in materials:
        total_time_needed += (m['time_per_kg'] * m['max_qty'])
        total_value_expected += (m['value_per_kg'] * m['max_qty'])
        total_weight_expected += m['max_qty']
        
    # panggil fungsi optimasi kalau waktu pengerjaan lebih dari kapasitas mesin
    scheduler = Scheduler()
    result_dp = None
    result_rr = None
    
    if total_time_needed > max_time:
        result_dp = scheduler.calculate_dp(materials, max_time)
        result_rr = scheduler.calculate_round_robin(materials, max_time)
        
    return render_template('result.html', 
                           title="OptiPro - Hasil",
                           materials=materials,
                           max_time=max_time,
                           total_time_needed=total_time_needed,
                           total_value_expected=total_value_expected,
                           total_weight_expected=total_weight_expected,
                           resultDP=result_dp,
                           resultRR=result_rr)

if __name__ == '__main__':
    app.run(debug=True)
