import configparser
from scraper import EmailScraper
import pandas as pd
import os.path


def write_to_csv(data, path):
    #create csv if no existing file exists, else update existing file
    if os.path.exists(path):
            df = pd.read_csv(path)
            df = df.append(data, ignore_index = True)
            df = df.drop_duplicates('Link', keep = 'last')
            
    else:
        df = pd.DataFrame(data)
        
        df.to_csv(path, index = False)
        return f'{len(data)} entries created/updated'

    

config = configparser.ConfigParser()
config.read('config.ini')


mail = EmailScraper(server = config['EMAIL']['server'], 
                    inbox = config['EMAIL']['inbox'], 
                    user = config['EMAIL']['user'], 
                    password = config['EMAIL']['password'], 
                    )

scraper = mail.scrape_mail()
if type(scraper) is list:

    print(write_to_csv(scraper, config['PATH']['csv']))

else:
    print(scraper)




