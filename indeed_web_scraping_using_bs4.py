from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import csv

base_url = 'https://in.indeed.com'
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36","X-Requested-With": "XMLHttpRequest"}

def get_links(keyword):
      keyword = '+'.join(keyword.split(' '))
      url_to_scrape = base_url + "/jobs?q=" + keyword
      
      links = []
      for i in range(0, 5):
            extention = ""
            if i != 0:
                  extention = "&start=" + str(i * 10)
            url = url_to_scrape + extention
            req = Request(url, headers = headers)
            web_byte = urlopen(req).read()
            webpage = web_byte.decode('utf-8')
            soup_req=BeautifulSoup(webpage,"html.parser")
            joblisting = soup_req.find_all('div',{'class': 'job_seen_beacon'})
            for job in joblisting:
                  href = job.find('a',{'class':'jcs-JobTitle css-jspxzf eu4oa1w0'} ,href=True)
                  complete_link = base_url + href['href']
                  links.append(complete_link)
      return links

def parse_job(url):
      req = Request(url, headers = headers)
      web_byte = urlopen(req).read()
      webpage = web_byte.decode('utf-8')
      soup_req = BeautifulSoup(webpage,"html.parser")
      title = soup_req.find('h1',{'class': 'icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title'}).text.strip()
      try:
        salary = soup_req.find('span',{'class': 'icl-u-xs-mr--xs attribute_snippet'}).text.strip()
      except:
        salary = 'None'
      desc = soup_req.find('div',{'class':'jobsearch-jobDescriptionText'}).text.strip('').replace('\n', ' ')
      company = soup_req.find('a',{'target': '_blank'}).text.strip('')
      urls = url
      jobs = {
        'position': title,
        'company': company,
        'salary': salary,
        'description': desc,
        'link' : urls,
        }
      return jobs

def save_csv(results):
      keys = results[0].keys()
      with open('indeed_data.csv', 'a', newline='', encoding="utf-8") as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)

results = []
def main():
      keywords = input('Enter job position keyword: ')
      links = get_links(keywords)
      for link in links:
            results.append(parse_job(link))
      save_csv(results)

# if __name__ == '__main__':
#       main()
#       print('-----------Extraction of data is complete. Check the csv file.-----------')