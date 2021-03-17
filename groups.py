from bs4 import BeautifulSoup
import json

import utils.urls as urls
import utils.authentication as authentication
from utils.exceptions import AuthorizationException, IncorrectInfoException

from utils.group import Group

#store selected group to 'selected_group.json' file
def group_store(groupList):

	sel_grp = json.dumps([groups[i - 1].__dict__ for x in groupList])

	#stores selected groups in json
    with open('groups.json', "w") as f:
        f.seek(0)
        f.write(sel_grp)
        f.truncate()


#shows all the groups and let's user choose the groups who's events are to be RSPVed
def get_all_groups(session, token):

	res = session.get(urls.ALL_GROUPS_URL)

	soup = BeautifulSoup(res.text, 'html.parser')

	page = soup.find('div', {'id': 'simple-view'})
	temp = page.find_all('ul',)[0]
	list_of_groups = temp.find_all('li')

	groups = []
	print("Select the groups to be auto RSVP'ed : ")
	for i, group in enumerate(list_of_groups):
		tmp = Group(
		    group_name=group.get('data-name'),
		    group_url=group.get('data-urlname'))
		groups.append(tmp)

		print(f"{i+1}. " + str(tmp))

	selected_groups = input(
		"Enter the respective numbers of the group (single space seperated): ")
	selected_array = [int(x) for x in selected_groups.strip().split(' ')]

	print("Selected Groups are-")
	for i in selected_array:
		print(groups[i - 1])

	group_store(selected_array)

	#creates an empty file if does not exist, else nothing.
	with open('rsvped_events.json', 'w'):
		pass

#driver function
def main():
    try:
        logged_in_session, token = authentication.signin()
    except AuthorizationException:
        return
    except IncorrectInfoException:
        return

    get_all_groups(logged_in_session, token)
    print("configuration settings successfully updated! :thumbs up:")


if __name__ == '__main__':
    main()
