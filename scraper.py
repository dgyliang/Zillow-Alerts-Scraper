import numpy as np
import imaplib
import email
from bs4 import BeautifulSoup
import re
import html
import pandas as pd
import io
import sys
import os

class EmailScraper(object):

    def __init__(self, server, inbox, user, password):
        self.server = server
        self.inbox = inbox
        self.user = user
        self.password = password
        self.mail = imaplib.IMAP4_SSL(self.server)

    #read email inbox
    def check_mail(self):
        output_list = []
        #try to log into email
        try:
            self.mail.login(self.user, self.password)
        except:
            return sys.exc_info()[1]
            sys.exit(1)
        #try to read inbox
        try:
            status, num_emails = self.mail.select(self.inbox)
            status, messages = self.mail.search(None, 'UNSEEN')
        except:
            return 'error accessing inbox or mail'
            
        msg_list = messages[0].split()
        #create list of bytes of unread emails if found
        if len(msg_list) > 0:
            for num in msg_list:
                typ, data = self.mail.fetch(num, '(RFC822)')
                msg = email.message_from_bytes(data[0][1])
                output_list.append(msg)
            return output_list
        else:
            return 'No New Messages'

    #scrape mail
    def scrape_mail(self):
        #check mail
        checked_mail = self.check_mail()
        #if unread mails were found, scrape mail
        if type(checked_mail) == list:
            self.dicts_list = []
            
            #scrape relevant information for each mail
            for msg in checked_mail:
                time_received = msg['date']
                date = re.search('(?<=, )[^\s]+\s[^\s]+\s[^\s]+', time_received).group(0)
                subject = msg['subject']
                #if the mail subject contains the word "result," then skip, since it is not a new listing
                if 'Result' in subject or '(undisclosed Address)' in subject:
                    continue

                #decode mail
                msg_html = msg.get_payload(1).get_payload(decode = True)
                soup = BeautifulSoup(msg_html, 'html.parser')
                
                property_type = soup.find_all('td', {'aria-label': re.compile('Property type')})[0].text.strip()
                
                address = soup.find_all('td', {'aria-label': re.compile('Property address')})[0].text.strip()
                address = address.encode('ascii', 'ignore')
                address = address.decode().replace('\r\n', '')
                street_address = address.split(',')[0]
                street_address = street_address.split()
                address_number = street_address[0]
                #split address/property number, as some properties have a range of numbers.
                try:
                    number = address_number.split('-')
                    number = [float(x) for x in number]
                except:
                    number = None
                street = street_address[1].upper()
                
                #zillow property id, used as the listing's unique identifier
                link = soup.find('td', {'aria-label' : 'Property photo'}).find('a', href = True)['href']
                
                try:
                    seller = soup.find('td', {'aria-label': re.compile('mlsdetails', re.IGNORECASE)}).text.strip()
                    seller = html.unescape(seller)
                    seller = seller.encode('ascii', 'ignore')
                    seller = seller.decode()
                except:
                    seller = None
                
                facts = soup.find_all('td', {'aria-label': re.compile('Property facts')})[0].text.strip()
                facts = html.unescape(facts).replace('\r\n', '')
                if 'Studio' in facts:
                    beds = 'Studio'
                else:
                    beds = re.search( '.*(?= bd)', facts).group(0)
                    beds = float(beds) if not beds == '--' else None
                baths = re.search( '(?<= \| ).*(?= ba)', facts).group(0)
                baths = float(baths) if not baths == '--' else None
                size = re.search( '(?<=a \| ).*(?= sqft)', facts).group(0)
                size = float(size.replace(',', '')) if not size == '--' else None
                if property_type == 'For Sale':
                    cost = soup.find_all('td', {'aria-label': re.compile('Property price')})[0].text.strip()
                    cost = float(cost[1:].replace(',', ''))
                else:
                    cost = soup.find_all('td', {'aria-label': re.compile('Property price')})[0].text.strip()
                    cost = cost[1:].replace('/mo', '')
                    cost = float(cost.replace(',', ''))

                #if property size exists, then find the price per square foot ratio
                if type(size) == float:
                    price_per_sqft = round(cost / size, 2)
                else:
                    price_per_sqft = None
                

                #create unique name for listing
                name = property_type + ':' + address + ' ' +  date
                name = name.replace(',', '')
                
                #append found information as a dictionary
                self.dicts_list.append( {
                                        'Name' : name,
                                        'Timestamp': time_received,
                                        'Date' : date,
                                        'ListingType': property_type,
                                        'Address': address,
                                        'AddressNumber' : address_number,
                                        'Street' : street_address[1] + '_' + street_address[2],
                                        'Link': link, 
                                        'Cost' : cost,
                                        'Beds': beds,
                                        'Baths': baths,
                                        'Size': size,
                                        'PricePerSqft' : price_per_sqft
                                        })
                
            return self.dicts_list
        
        else:
            #no unread mail found
            return checked_mail
        
            