from requests import Session

import utils.info as info
import utils.urls as urls

from utils.exceptions import AuthorizationException, IncorrectInfoException

"""This module deals with the authentication part. Based on the environment variables (MEETUP_USERID and MEETUP_PASSWORD)"""

#to extract the session-token from the html string
def parse_token(page_html):

    offset = 7
    token = page_html.find("token")
    start = (page_html[token:]).find('value="') + token
    end = (page_html[start + offset:]).find('"') + start + offset

    return page_html[start + offset:end]

#used to authenticate into meetup.com returns session object and cookies
def signin(verbose=True):

    session = Session()
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = session.get(urls.LOGIN_URL, headers=headers)

    if (info.user_password is None) or (info.user_email is None):
        raise IncorrectInfoException()
    token = parse_token(r.text)
    data = {
        'email': info.user_email,
        'password': info.user_password,
        'submitButton': 'Log in',
        'token': token,
        'op': 'login',
        'returnUri': urls.MAIN_URL,
    }

    res = session.post(urls.LOGIN_URL, headers=headers, data=data)

    f = open('t.html', 'w')
    f.write(res.text)
    f.close()

    if res.text.find("password was entered incorrectly") is not -1:
        raise IncorrectInfoException()

    if int(session.cookies['memberId']) == 0:
        raise AuthorizationException()
    if verbose:
        print("Authorization complete!")
    cookies = session.cookies

    return session, token
