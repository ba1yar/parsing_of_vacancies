from headhunter import get_jobs
from save import save_to_csv

hh_jobs = get_jobs()
save_to_csv(hh_jobs)
