import urllib2
import urllib
import cookielib
from HTMLParser import HTMLParser

class JoomlaHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.tag_results = {}
    def handle_starttag(self, tag, attrs):
        if tag == "input":
            tag_name = None
            tag_value = None
            for name,value in attrs:
                if name == "name":
                    tag_name = value
                if name == "value":
                    tag_value = value
                if tag_name is not None:
                    self.tag_results[tag_name] = value

def check_login(username,password):
    target_url = "http://www.thecartridgeconnection.net/internet_tv/index.php"
    jar = cookielib.FileCookieJar("cookies")
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
    response = opener.open(target_url)
    page = response.read()
    parser = JoomlaHTMLParser()
    parser.feed(page)
    post_tags = parser.tag_results
    post_tags['username'] = username
    post_tags['password'] = password

    login_data = urllib.urlencode(post_tags)
    login_response = opener.open(target_url, login_data)
    login_result = login_response.read()

    if ('Home - members' in login_result) and ('re-activate your account' not in login_result):
        return 1;
    elif ('Home - members' in login_result) and ('re-activate your account' in login_result):
        return 0;
    else:
        return -1;


