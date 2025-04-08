import os
import bs4
import pandas
import requests


class Timeline:

    def __init__(self):
        self.was_loaded = False
        self.file_path = "timeline.csv"
        self.url = "https://en.wikipedia.org/wiki/Timeline_of_space_exploration"
        self.timeline = pandas.DataFrame(columns = ("Date", "Event", "Country", "Researcher/Mission"))
        self.load_timeline()
        

    def load_timeline(self):
        if os.path.exists(self.file_path):
            self.timeline = pandas.read_csv(self.file_path)
        else:
            self.scrape_timeline()
    

    def scrape_table(self, table : bs4.element.Tag):
        rows = table.find_all("tr")[1:]
        for row in rows:
            row_data = row.find_all("td")
            individual_row_data = [data.text.strip() for data in row_data][:len(row_data) - 1]
            last_index = len(self.timeline)
            self.timeline.loc[last_index] = individual_row_data
    

    def scrape_timeline(self):
        try:
            response = requests.get(url = self.url)
            raw_html = response.text
            soup = bs4.BeautifulSoup(raw_html, "html.parser")

            all_tables = soup.find_all("table")
            all_tables = all_tables[1: len(all_tables) - 6]

            for table in all_tables:
                self.scrape_table(table)
            
            self.timeline.to_csv(self.file_path)
        
        except Exception as error:
            print(f"An error occured: {error}")