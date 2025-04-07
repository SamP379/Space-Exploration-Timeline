import bs4
import pandas
import requests


TIMELINE_URL = "https://en.wikipedia.org/wiki/Timeline_of_space_exploration"
DATAFRAME_COLUMN_HEADERS = ("Date", "Event", "Country", "Researcher/Mission") 
TIMELINE_FILE_PATH = "timeline.csv"


global timeline
timeline = pandas.DataFrame(columns = DATAFRAME_COLUMN_HEADERS)


def scrape_table(table : bs4.element.Tag):
    rows = table.find_all("tr")[1:]
    for row in rows:
        row_data = row.find_all("td")
        individual_row_data = [data.text.strip() for data in row_data][:len(row_data) - 1]
        last_index = len(timeline)
        timeline.loc[last_index] = individual_row_data


def scrape_timeline():
    try :
        response = requests.get(url = TIMELINE_URL)
        raw_html = response.text
        soup = bs4.BeautifulSoup(raw_html, "html.parser")

        all_tables = soup.find_all("table")
        all_tables = all_tables[1: len(all_tables) - 6]

        for table in all_tables:
            scrape_table(table)

    except Exception as error:
        print(f"An error occured: {error}")


def main():
    scrape_timeline()
    timeline = timeline.drop_duplicates()
    print(timeline)
    timeline.to_csv(TIMELINE_FILE_PATH)


if __name__ == "__main__":
    main()