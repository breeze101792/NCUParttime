#!/usr/bin/env python3
import urllib.request
import http.cookiejar
import getpass
from optparse import OptionParser

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13'
url_login = 'https://portal.ncu.edu.tw/j_spring_security_check'
url_signin = 'http://140.115.182.62/PartTime/parttime.php/signin'
url_signout = 'http://140.115.182.62/PartTime/parttime.php/signout'
url_fake = 'http://140.115.182.62/PartTime/parttime.php/signout'

if __name__ == '__main__':
    parser = OptionParser(usage = 'Usage: login ......')
    parser.add_option("-n", "--user-name", dest="user_name", help="User name for log in", action="store")
    parser.add_option("-p", "--password", dest="user_password", help="User password for log in", action="store")
    parser.add_option("-s", "--serial-number", dest="serial_number", help="Project's serial number", action="store")
    parser.add_option("-a", dest="job_type_long", help="Job for logn term",default=False, action="store_true")
    parser.add_option("-w", dest="job_type_short", help="Job for short term",default=False, action="store_true")
    parser.add_option("-q", dest="quiet", help="Make script more quiet",default=False, action="store_true")
    parser.add_option("-i", "--sign-in", dest="sign_in", help="Sign in",default=False, action="store_true")
    parser.add_option("-o", "--sign-out", dest="sign_out", help="Sign out",default=False, action="store_true")
    '''
    parser.add_option("-P", "--project-name", dest="pj_name", help="Project name",default=False, action="store_true")
    parser.add_option("-P", "--project-name", dest="pj_name", help="Project name",default=False,  action="store_true")
    '''
    (options, args) = parser.parse_args()
    '''
    if len(args) < 2 :
        print("args !!")
        exit()
    '''
    if options.user_name == None and not options.quiet :
        user_name = input("Enter User Name:")
    else:
        user_name = options.user_name
    if options.user_password == None and not options.quiet :
        user_password = getpass.getpass("Enter password:")
    else:
        user_password = options.user_password
    
    if options.serial_number == None and not options.quiet:
        print("project's serial number not set!")
        serial_number = input("Enter Serial Number:")
    elif options.serial_number != None:
        serial_number = options.serial_number
    else:
        print("No serial number specify")
        exit()
    
    
    if options.job_type_long and options.job_type_short:
        print("get confused!")
    elif options.job_type_short:
        job_prefix = "ptw"
    else:
        job_prefix = "pta"

    if not options.sign_in and not options.sign_out and not options.quiet:
        print("checking method get confused!")
        exit()
    elif options.sign_in:
        check_method = "signin"
        url_target = url_signin
    elif options.sign_out:
        check_method = "signout"
        url_target = url_signout
    else:
        print("specify the checking method")
        exit()
    print(check_method)
    
    
    acc_info = {\
                'j_username':user_name,\
                'j_password':user_password,\
                'submit':'Login'\
                }
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-agent', user_agent)]
    urllib.request.install_opener(opener)
    data = urllib.parse.urlencode(acc_info).encode('UTF-8')
    request = urllib.request.Request(url=url_login, data=data)
    #login
    try:
        '''
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
        '''
        html = "login successful"
        if "login unsuccessful" in html:
            print("login unsuccessful")
        else:
            print("login successful")
            check = {\
                    check_method:job_prefix + serial_number\
                    }
            data = urllib.parse.urlencode(check).encode('UTF-8')
            
            request = urllib.request.Request(url=url_fake, data=data)
            response = urllib.request.urlopen(request)
            html = response.read().decode('utf-8')
            if "login unsuccessful" in html:
                print("login unsuccessful")
            else:
                print("login successful")
    
    except urllib.error.HTTPError as e:
        responseData = e.read().decode('utf8', 'ignore')
        responseFail = False

    except urllib.error.URLError:
        responseFail = True

    except socket.error:
        responseFail = True

    except socket.timeout:
        responseFail = True

    except UnicodeEncodeError:
        print("Encoding Error")
        responseFail = True
    print(responseData)
    exit()


