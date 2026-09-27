import hashlib
import requests
import argparse
from requests.exceptions import ConnectionError, Timeout

# here i want the user to write their password first (step 1)
 
def sha(password):
    return hashlib.sha1(password.encode()).hexdigest().upper()
    
# now usking the k anotimity trick here ........(step 2)
# split the hash we got into the suffix or the prefix ...(step2)

def sha_split(password_hash):
    prefix_sha = password_hash[:5]       
    suffix_sha = password_hash[5:]
    return prefix_sha , suffix_sha  

# now its time for the api call here ......(step 3)
# we can do api calls by using of the requests library ...(step 3)

def get_breach_data(prefix_sha):
    try:
        response =  requests.get(f"https://api.pwnedpasswords.com/range/{prefix_sha}")
        content = response.text
        return(content)
    except Timeout :
        print("actually this is happened  due to the low server coneection , try again  ") 
        return None            
    except ConnectionError:
        print("check the internet coneection")
        return None

# now its time to check the suffix part from the actual breach data ...(step 4,5)

def find_suffix(breach_data , suffix_sha):
    lines = breach_data.strip().split("\n")
    for line  in lines:
        parts = line.split(":")
        if parts[0] ==suffix_sha:
            return (parts[1])
    return 0
# now it the time to 
def show_result(suf):
    integer_suffix = int(suf)
    if integer_suffix == 0:
        print("~ ~ ~ oh ! wow ! ~ ~ ~ \n "
        " NO PASSWORD BREACH IS THERE ...")
    else:
        print(f"---- oh  no..!! ---- \n PASSWORD HAS BREACHED  {integer_suffix}  many times .....")    


def get_password():    
    parser = argparse.ArgumentParser()
    parser.add_argument("--password", type=str, help = "Paswword for the checking of his breaches ")
    args = parser.parse_args()
    if args.password:
        return args.password 
    else:        
        password = input("Enter the password:- ")
        return password 
if __name__ == "__main__":
    password = get_password()    
    password_hash = sha(password)
    print(password_hash)

    prefix, suffix = sha_split(password_hash)   
    print("Prefix:", prefix)
    print("Suffix:", suffix)

    breach_data = get_breach_data(prefix) 
    if breach_data == None:
        print(" invanlid we cannot go ahead... ")
    else:
        print(" yes we can proceed with the breach data ")
        suf = find_suffix(breach_data, suffix)
        show_result(suf)

