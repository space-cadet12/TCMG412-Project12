''' The goal of this code is to connect to the API we've built previously and test each of the endpoints for functionality '''

# Import necessary modules
import requests
from sys import exit



# Set base URL
url = 'http://localhost:80'



# Using http's "GET" protocol to attain HTTP responses 
# Based off of the status code returned, we can tell if a HTTP call to an endpoint is returning us what we expect it to. 

# md5 tests
md5_text = requests.get(url+'/md5/test') # response should pass meaning it returns 200 status code
md5_boolean = requests.get(url+'/md5/True')
md5_number = requests.get(url+'/md5/0123')
md5_int = requests.get(url+'/md5/int(12)')

# factorial tests
fact_text = requests.get(url+'/factorial/test') # 500 status code expected
fact_number = requests.get(url+'/factorial/1234')

# fibonacci tests
fib_text = requests.get(url+'/fibonacci/test') 
fib_number = requests.get(url+'/fibonacci/01234') 

# is-prime tests
isprime_text = requests.get(url+'/is-prime/hi') # response should fail meaning it returns 404 status code
isprime_number = requests.get(url+'/is-prime/1') # 200 response code
isprime_0 = requests.get(url+'/is-prime/0')
isprime_negative = requests.get(url+'/is-prime/-1')

'''
# slack tests
slack_text = requests.get(url+'/slack-alert/hi_im_being_tested') 
slack_number = requests.get(url+'/slack-alert/12')
'''


# How to check the object that's returned to make sure it was a success. 
# You use the method 'status_code' on the object that you made with the get request
if md5_text.status_code != 200: # this check is to make sure sending a text request to the server passes, returning 200
    print(1)
    exit(1)
    
if md5_boolean.status_code != 200: 
    print(1)
    exit(1)    

if md5_number.status_code != 200: 
    print(1)
    exit(1)
    
if md5_int.status_code != 200:
    print(1)
    exit(1)
    
if fact_text.status_code != 500: # this check is to make sure sending a text request to the server fails, returning 500
    print(1)
    exit(1) 
    
if fact_number.status_code != 200: 
    print(1)
    exit(1)
    
if fib_text.status_code != 404: 
    print(1)
    exit(1)
    
if fib_number.status_code != 200: 
    print(1)
    exit(1)
    
if isprime_text.status_code != 404: # this check is to make sure sending a text request to the server fails, returning 404
    print(1)
    exit(1)
    
if isprime_number.status_code != 200: 
    print(1)
    exit(1) 

if isprime_0.status_code != 200:
    print(1)
    exit(1)

if isprime_negative.status_code != 404:
    print(1)
    exit(1)
'''
if slack_text.status_code != 200: 
    print(1)
    exit(1)
    
if slack_number.status_code != 200: 
    print(1)
    exit(1)
  '''  
    
# If everything above operates as expected, the program will close with printing 0 to terminal and also sets program exit code to 0    
print(0)
exit(0)