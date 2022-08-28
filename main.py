from flask import Flask, render_template, request, redirect, send_file
from headhunter import get_jobs
from save import save_to_csv


app = Flask('jobScrapper')

db = {}


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/report')
def report():
    keyword = request.args.get('keyword')
    if keyword is not None:
        keyword = keyword.lower()
        get_db = db.get(keyword)
        if get_db:
            jobs = get_db
        else:
            jobs = get_jobs(keyword)
            db[keyword] = jobs
        print(jobs)
    else:
        return redirect('/')

    return render_template('report.html', searchBy=keyword, number_result=len(jobs), jobs=jobs)


@app.route('/export')
def export():
    try:
        keyword = request.args.get('keyword')
        if not keyword:
            raise Exception()
        keyword = keyword.lower()
        jobs = db.get(keyword)
        if not jobs:
            raise Exception()
        save_to_csv(jobs)
        return send_file('jobs.csv')
    except:
        return redirect('/')


if __name__ == "__main__":
    app.run()
