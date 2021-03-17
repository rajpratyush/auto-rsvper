class Event:
    """
    This is to store the each event detail

    group_name : Name of the group organising this event.
    event_id : Unique id of this event.
    rsvp_status : Status of user's RSVP
    """

    def __init__(self, group_name, event_id, rsvp_status=False):
        self.group_name = group_name
        self.event_id = event_id
        self.rsvp_status = rsvp_status

    def __str__(self):
        return (self.group_name + ' : ' + self.rsvp_status)

    def __repr__(self):
        return self.__str__()

	#to directly parse a dictionary(containing the attributes of Event object) to construct an object of the class
    @classmethod
    def fromJson(cls, json):

        group_name = json['group_name']
        event_id = json['event_id']
        rsvp_status = json['rsvp_status']
        return cls(
            group_name=group_name,
            event_id=event_id,
            rsvp_status=rsvp_status)
