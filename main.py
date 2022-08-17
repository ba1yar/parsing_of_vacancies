from flask import Flask, render_template, request, redirect
from headhunter import get_jobs
# from save import save_to_csv
# save_to_csv(hh_jobs)

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


if __name__ == "__main__":
    app.run()
