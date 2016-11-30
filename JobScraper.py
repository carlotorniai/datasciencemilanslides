import mechanize
import re
from bs4 import BeautifulSoup
import pdb
import pandas as pd
import sys


def get_mechanized_soup(url):
    ''' Returns a soup object retrieved through mechanized
    '''
    br = mechanize.Browser()
    br.addheaders = [('User-agent','Mozilla/5.0')]
    br.set_handle_robots(False)
    html = br.open(url)
    html = html.read().lower()
    html = unicode(html,errors='ignore') 
    return BeautifulSoup(html)


def parse_page(page_soup):
    ''' parse a linkedin page of job results'''
    for job in page_soup.findAll("div", {"class": "content"}):
        print "==="*20
        try:
            job_title = job.find("a", {"class": "title"}).get_text()
            job_url = job.find("a", {"class": "title"})['href'].split("?")[0]
            job_date = job.find("span", {"itemprop" : "dateposted"}).get_text()
            
       

    
            # Here I need to get the soup for the job_html
            job_soup = get_mechanized_soup(job_url)
            for detail in job_soup.findAll("li", {"class" : "detail"}):
                try:
                    if detail.find("div", {"class" : "label"}).get_text() == 'experience':
                        job_experience = detail.find("div", {"class" : "value"}).get_text()
                    elif detail.find("div", {"class" : "label"}).get_text() == 'job function':
                        job_function = detail.find("div", {"class" : "value"}).get_text()
                    elif detail.find("div", {"class" : "label"}).get_text() == 'employment type':
                        job_employment_type = detail.find("div", {"class" : "value"}).get_text()
                    elif detail.find("div", {"class" : "label"}).get_text() == 'employer job id':
                        job_employer_id = detail.find("div", {"class" : "value"}).get_text()
                    elif detail.find("div", {"class" : "label"}).get_text() == 'job id':
                        job_id = detail.find("div", {"class" : "value"}).get_text()
                except:
                    print "Bongola"
                    #print job_experience, job_function, job_employment_type, job_employer_id, job_id

                # Here get the text 
                content  = job_soup.find("div", {"class" : "description-section"})

                # Here get text
                for html_text in content.findAll("div", {"itemprop" : "description"}):
                    job_html_desc = html_text
                    job_text_desc = html_text.get_text()
        
            print "Job Posting date:", job_date
            print "Job Title: ", job_title
            print "Job URL: ", job_url
            print "Job Experience", job_experience
            print "Job Function: ", job_function
            print "Job Employment: ", job_employment_type
            print "Job Employer ID: ", job_employer_id
            print "Job ID: ", job_id
            print "Job Desc text: ", job_text_desc
        except:
            print "Something wrong did go on: ", job.find("a", {"class": "title"})





def check_next(page_soup):
    ''' check if there is the next link in the page and if so returns url else returns null'''
    
    # Get div class pagination
    next_url = None
    try:
        pagination = page_soup.find("div", {"class": "pagination"})
        #print pagination

        # Here get all the li and check if the value is text
        for detail in pagination.findAll("li"):
            for links in detail.findAll("a"):
                 if "next" in links.get_text():
                        print "Found Next:"
                        next_url = links['href']
                        print next_url
    except:
        print "Something wrong did go in next url.. "

    return next_url



def parse_page_dict(page_soup, job_dict):
    ''' parse a linkedin page of job results'''
    debug = False
    for job in page_soup.findAll("div", {"class": "content"}):
        print "==="*20
        # pdb.set_trace()
        try:
            job_title = job.find("a", {"class": "title"}).get_text()
            job_url = job.find("a", {"class": "title"})['href'].split("?")[0]
            job_date = job.find("span", {"itemprop" : "dateposted"}).get_text()
            
            
            # Here part withthe location
            
            # Here I need to get the soup for the job_html
            job_soup = get_mechanized_soup(job_url)
            
            # Here part about the Region address
            for address in job_soup.findAll("span", {"itemprop": "address"}):  
               
                for addr_info in address.findAll("meta"):
                    if addr_info['itemprop'] == 'addresslocality':
                        job_city =  addr_info['content']
                      
                    elif addr_info['itemprop'] == 'addressregion':
                        job_region =  addr_info['content']
                    
                    elif addr_info['itemprop'] == 'addresscountry':
                        job_country =  addr_info['content']


            
            for detail in job_soup.findAll("li", {"class" : "detail"}):
                #print detail
                try:
                    if detail.find("div", {"class" : "label"}).get_text() == 'experience' or detail.find("div", {"class" : "label"}).get_text() == 'exprience' :
                        job_experience = detail.find("div", {"class" : "value"}).get_text()
                       
                except:
                    print "something wrong did go while experience on : ", detail
                    job_experience=None
                try:
                    if detail.find("div", {"class" : "label"}).get_text() == 'job function':
                        job_function = detail.find("div", {"class" : "value"}).get_text()
                except:
                    print "something wrong did go while job_function on : ", detail
                    job_function=None
                    
                try:
                    if detail.find("div", {"class" : "label"}).get_text() == 'employment type':
                        job_employment_type = detail.find("div", {"class" : "value"}).get_text()
                except:
                    print "something wrong did go while job_employment_type on : ", detail
                    job_employment_type=None
                    
                try:
                    if detail.find("div", {"class" : "label"}).get_text() == 'employer job id':
                        job_employer_id = detail.find("div", {"class" : "value"}).get_text()
                except:
                    print "something wrong did go while job_employer_id on : ", detail
                    job_employer_id=None
                
                try:
                    if detail.find("div", {"class" : "label"}).get_text() == 'job id':
                        job_id = detail.find("div", {"class" : "value"}).get_text()
                except:
                    print "something wrong did go while job_id on : ", detail
                    job_id=None
                    #print job_experience, job_function, job_employment_type, job_employer_id, job_id

                # Here get the text 
                content  = job_soup.find("div", {"class" : "description-section"})

                # Here get text
                for html_text in content.findAll("div", {"itemprop" : "description"}):
                    job_html_desc = html_text
                    job_text_desc = html_text.get_text()
            
            job_dict[job_id]= dict()
            print "Job Posting date:", job_date
            print "Job Title: ", job_title
            # Here assignign the calues for the Address parts
            job_dict[job_id]['city'] = job_city
            print "Job City: ", job_city
            job_dict[job_id]['region'] = job_region
            print "Job Region: ", job_region
            job_dict[job_id]['country'] = job_country
            print "Job Country: ", job_country
            print "Job URL: ", job_url
            print "Job Experience", job_experience
            print "Job Function: ", job_function
            print "Job Employment: ", job_employment_type
            print "Job Employer ID: ", job_employer_id
            print "Job ID: ", job_id
            #print "Job Desc text: ", job_text_desc
           
            job_dict[job_id]['job_date'] = job_date
            job_dict[job_id]['job_title'] = job_title
            job_dict[job_id]['job_url'] = job_url
            job_dict[job_id]['job_experience'] = job_experience
            job_dict[job_id]['job_function'] = job_function
            job_dict[job_id]['job_employment_type'] = job_employment_type
            job_dict[job_id]['job_employer_id'] = job_employer_id
            #job_dict[job_id]['job_html_desc'] = job_html_desc
            job_dict[job_id]['job_text_desc'] = job_text_desc
            
        except:
            print "Something wrong did go on: ", job.find("a", {"class": "title"})
        
    return job_dict


def get_job_region(company, country):
    ''' Gets the jobs for a particular Region'''
    #base_url = 'https://linkedin.com/job/'
    # https://fr.linkedin.com/
    #base_url = 'https://'+country+'.linkedin.com/job/'
    base_url = 'https://linkedin.com/job/'
    initial_url = base_url+company+'/jobs/?country='+country+'&sort=date'
    print initial_url
    next_url = initial_url
    # Here I want to create a dictionary that is empty and probably pass it to 
    # the parse page
    job_dict = dict()
    while next_url is not None:
        print next_url
        # Here parse curent url
        current_soup = get_mechanized_soup(next_url)
        job_dict = parse_page_dict(current_soup, job_dict)
        next_url = check_next(current_soup)
    
    # Here it saves the dict 
    #pd.to_pickle(job_dict, './data/job_dict_'+country+'.pkl')
    # Here saves the DataFrame too
    job_df = pd.DataFrame.from_dict(job_dict).transpose()
    # Here adding the company 
    job_df['company'] = company
    try:
        job_df.to_pickle('./data/'+company+'_'+country+'job_df.pkl')
    except:
        print 'Saving pickle failed'
    return job_df


def main():
	# Here get the parameters

	print "Starting"
	# Here need to parse the parameters like company and 
	# Country
	if len(sys.argv)<2:
		print "Usage: %s, [company] [country]"%(sys.argv[0])
	company = sys.argv[1]


if __name__ == "__main__":
	main()
