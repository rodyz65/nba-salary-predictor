from django.shortcuts import render
import joblib
import numpy as np
import sqlite3

regression_model = joblib.load('regression_model.pkl')
def predict_salary(request):
    predicted_salary = None
    actual_salary = None
    player_name = ''
    if request.method == 'POST':
        player_name = request.POST.get('player_name')
        ppg =request.POST.get('ppg')
        try:
            ppg = float(ppg)
            predicted_salary = regression_model.predict([[ppg]])[0]
            conn = sqlite3.connect('nba_salaries.db')
            cursor = conn.cursor()
            cursor.execute("SELECT Salary FROM salary_predictions WHERE player = ?", (player_name,))
            result = cursor.fetchone()
            if result:
                actual_salary = result[0]
            conn.close()
        except Exception as e:
            print("Error:", e)
    return render(request, 'salarypredictor/predict_salary.html', {
        'predicted_salary': predicted_salary,
        'actual_salary': actual_salary,
        'player_name': player_name
    })

def test_page(request):
    return render(request, 'salarypredictor/test.html')

# Create your views here.
