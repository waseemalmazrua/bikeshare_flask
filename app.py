from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def load_data(city):
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name().str.lower()
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    return df

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    city = request.form['city']
    df = load_data(city)

    stats = {
        'common_month': df['month'].mode()[0].title(),
        'common_day': df['day_of_week'].mode()[0].title(),
        'common_hour': df['Start Time'].dt.hour.mode()[0],
        'trip_combo': (df['Start Station'] + ' to ' + df['End Station']).mode()[0],
        'total_duration': df['Trip Duration'].sum(),
        'average_duration': df['Trip Duration'].mean(),
        'start_station': df['Start Station'].mode()[0],
        'end_station': df['End Station'].mode()[0],
        'user_types': df['User Type'].value_counts().to_dict(),
        'raw_data': df.head(10).to_html(classes='table table-striped', index=False)
    }

    if 'Gender' in df:
        stats['genders'] = df['Gender'].value_counts().to_dict()
    if 'Birth Year' in df:
        stats['earliest'] = int(df['Birth Year'].min())
        stats['recent'] = int(df['Birth Year'].max())
        stats['common_birth'] = int(df['Birth Year'].mode()[0])

    return render_template('results.html', city=city, stats=stats)

if __name__ == '__main__':
    app.run(debug=True)
