
class Group:
    """
    This is to store the each group detail

    group_name : name of the group
    group_url : url of this group

    """

    def __init__(self, group_name, group_url):
        self.group_name = group_name
        self.group_url = group_url

    def __str__(self):
        return (self.group_name + ' : ' + self.group_url)

    def __repr__(self):
        return self.__str__()

	#to directly parse a dictionary(containing the attributes of Group object) to construct an object of the class
    @classmethod
    def fromJson(cls, json):

        group_name = json['group_name']
        group_url = json['group_url']
        return cls(group_name=group_name, group_url=group_url)
