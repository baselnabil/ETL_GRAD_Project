import csv
import pandas as pd
from jobspy import scrape_jobs

def scrape_and_merge_jobs(locations, site_name, search_term, results_wanted, hours_old, country_indeed, output_file):
    all_jobs = pd.DataFrame()
    
    for location in locations:
        try:
            jobs = scrape_jobs(
                site_name=site_name,
                search_term=search_term,
                location=location,
                results_wanted=results_wanted,
                hours_old=hours_old,
                country_indeed=country_indeed,
            )
            all_jobs = pd.concat([all_jobs, jobs], ignore_index=True)
        except Exception as e:
            print(f"Error scraping jobs for location {location}: {e}")
    
    if all_jobs.empty:
        print("No jobs found to save to CSV.")
    else:
        print(f"Found {len(all_jobs)} jobs in total")
        all_jobs.to_csv(output_file, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False)