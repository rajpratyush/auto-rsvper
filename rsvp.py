from bs4 import BeautifulSoup
import json
import argparse

import utils.urls as urls
import utils.authentication as authentication
import utils.headers as headers

from utils.group import Group
from utils.event import Event

"""This is the main module used to perform the automatic RSVP of selected groups."""

parser = argparse.ArgumentParser(
    description='This module performs the automatic RSVP of selected groups.')

parser.add_argument(
    '--dry_run', help='an integer for the accumulator, to dry run without rspving', action='store_true', default=False)
args = parser.parse_args()

#reads the rsvped_events.json file and parses the list of Groups
def get_rsvped_events_string():

    with open('rsvped_events.json', "r") as f:
        f.seek(0)
        eventList = f.read()

    return eventList


#reads the groups.json file created by groups.py and parses the list of Groups
def get_selected_groups():

    with open('groups.json', "r") as f:
        f.seek(0)
        groupList = f.read()

    selected_groups = [Group.fromJson(x) for x in json.loads(groupList)]
    return selected_groups

#to get the event page url for the group
def get_event_url(group):
	return urls.MAIN_URL + group.group_url + '/events/'

#to get the events RSPVed of a particular group and returns the list of events
def get_event_rsvped(rsvped_events_string, session, group):

	url = get_event_url(group)
	res = session.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    all_events = soup.find_all('a', {'id': 'attendButton'})

	rsvped_events = []
    for event in all_events:
        session.headers = base_headers.RSVP_GET
        id = event.get('href').split('/')[-2]
        rsvp_endpoint = urls.MAIN_URL + \
            event.get('href')+'action=rsvp&response=yes'

        if id in rsvped_events_string:
            continue

        if not args.dry_run:
            params = (
                ('action', 'rsvp'),
                ('response', 'yes'),
            )

            res = session.get(urls.MAIN_URL + event.get('href'), params=params)

            session.headers = base_headers.RSVP_POST
            session.headers['x-mwp-csrf'] = session.cookies['x-mwp-csrf-header']
            session.headers['referer'] = rsvp_endpoint

            query = '(endpoint:' + group.group_url + "/events/" + id + "/rsvps" + ',meta:(method:post),params:(eventId:' + id + \
                ',fields:rsvp_counts,response:yes,urlname:' + group.group_url + \
                '),ref:rsvpAction' + "_" + group.group_url + '_' + id + ')'

            data = {
                'queries': query
            }
            res = session.post(
                'https://www.meetup.com/mu_api/urlname/events/eventId', data=data)

            if res.status_code == 200:
                rsvp_event = Event(group.group_name, id, True)
                rsvped_events.append(rsvp_event)
	return rsvped_events

#used to write RSVPed events into 'rsvped_events.json' file.
def rsvp_events(session, token, group):

    rsvped_events_string = get_rsvped_events_string()

	rsvped_events = get_event_rsvped(rsvped_events_string, session, group)
    
    old_rsvped_events = [Event.fromJson(x)
                         for x in json.loads(rsvped_events_string)]
    rsvped_events += old_rsvped_events
    rsvpList = json.dumps([x.__dict__ for x in rsvped_events])

    with open('rsvped_events.json', "w") as f:
        f.seek(0)
        f.write(rsvpList)
        f.truncate()


#driver function
def main():

    selected_groups = get_selected_groups()
    logged_in_session, token = authentication.signin(verbose=False)

    for group in selected_groups:
        rsvp_events(logged_in_session, token, group)


if __name__ == "__main__":
    main()
