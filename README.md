# Zillow-Alerts-Scraper

A Zillow alerts scraper written in Python. Scrapes Zillow email alerts, then automatically writes data into a csv file. Useful for people looking for housing and want to compare listings.

--- 
Table of Contents
---
- [Introduction](#introduction)
- [Setup](#setup)
---

# Introduction

Zillow discontinued access to their API, thus restricting access directly to their listings database. The alternative would then be instead to get access to MLS streams, however that is not possible for anyone outside the real estate industry. The other way to do it is to scrape Zillow's website. However it is clearly stated in Zillow's TOS that it is illegal to scrape their website. Thus to get around this, this scraper takes advantage of Zillow's email alerts for new listings and scrapes that instead.

---

# Setup

## Zillow 
1. Go on Zillow and enter a search query like usual 
2. Specify whether or not the search query is for sales or rental listings, as well as other filters. Then click save search and set email frequency as instant.
3. You can find your saved searches under "Saved Searches" in the drop-down menu under your profile.

## Email

Setting up your email account for Zillow alerts is straight forward. It may be beneficial to create a dedicated inbox in the email account for the listing alerts and route all Zillow alert emails there. That way the scraper will only read certain emails instead of everything. Research how to create a new inbox/label for your email service and how to create rules to only include emails from the Zillow email addresses that send instant alerts. Specify the email credentials and inbox name in the config file and the scraper will attempt to use that information.

If you are using gmail, you will need to turn on unsafe apps access. Furthermore, if your account is secured with two-factor authentication, you will also need to create an app password and put that in the config file instead of your regular password.

## Dependencies

``` beautifulsoup4```, ``` pandas``` are required for this scraper.

## Running the code

To run the code, run ```script.py``` after installing python and dependencies. You may run the code automatically by simply wrapping the script in a while loop, setting a coroutine task on your operating system, or using services such as heroku to run the script on the cloud.
