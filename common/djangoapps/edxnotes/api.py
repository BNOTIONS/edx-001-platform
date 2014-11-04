import datetime
from uuid import uuid4
from xmodule.modulestore.exceptions import ItemNotFoundError


# Replace these with your details
CONSUMER_KEY = 'yourconsumerkey'
CONSUMER_SECRET = 'yourconsumersecret'
DEFAULT_TTL = 86400


class EdxNotes(object):
    """docstring for EdxNotes"""
    def __init__(self):
        super(EdxNotes, self).__init__()

    @staticmethod
    def create(note_info):
        note_info['id'] = uuid4().hex
        LIST.append(note_info)
        return note_info

    @staticmethod
    def read(note_id, user):
        result = EdxNotes.filter_by_id(note_id)
        if result:
            return result
        else:
            raise ItemNotFoundError()

    @staticmethod
    def update(note_id, note_info):
        result = EdxNotes.filter_by_id(note_id)
        if result:
            return result
        else:
            raise ItemNotFoundError()

    @staticmethod
    def delete(note_id):
        result = EdxNotes.filter_by_id(note_id)
        if not result:
            raise ItemNotFoundError()

    @staticmethod
    def search(user, usage_id):
        results = EdxNotes.filter_by_user(user)
        return {
            'total': len(results),
            'rows': results
        }

    @staticmethod
    def filter_by_id(note_id):
        return EdxNotes.filter_by('id', note_id)

    @staticmethod
    def filter_by_user(user):
        return EdxNotes.filter_by('user', user)

    @staticmethod
    def filter_by(field_name, value):
        return filter(lambda note: note.get(field_name) == value, LIST)


def _now():
    return datetime.datetime.utcnow().replace(microsecond=0)


def get_prefix():
    return 'http://127.0.0.1:8042/api/v1' or '/edxnotes/api'


def get_user_id():
    return 'edx_user'


def get_usage_id():
    return ''


def get_course_id():
    return 'course_id'


def generate_uid():
    return uuid4().int


LIST = [
    {
        "id": "39fc339cf058bd22176771b3e3187329",  # unique id (added by backend)
        "annotator_schema_version": "v1.0",        # schema version: default v1.0
        "created": "2011-05-24T18:52:08.036814",   # created datetime in iso8601 format (added by backend)
        "updated": "2011-05-26T12:17:05.012544",   # updated datetime in iso8601 format (added by backend)
        "text": "A note I wrote",                  # content of annotation
        "quote": "the basics",                     # the annotated text (added by frontend)
        "ranges": [                                # list of ranges covered by annotation (usually only one entry)
            {
                "start": "/p[1]",                  # (relative) XPath to start element
                "end": "/p[1]",                    # (relative) XPath to end element
                "startOffset": 81,                 # character offset within start element
                "endOffset": 91                    # character offset within end element
            }
        ],
        "user": "user",                           # user id of annotation owner (can also be an object with an 'id' property)
        "usage_id": "usage_id",                    # usage id of a component (added by frontend)
        "course_id": "course_id",                  # course id
    },
    {
        "id": "39fc339cf058bd22176771b3e3187330",  # unique id (added by backend)
        "annotator_schema_version": "v1.0",        # schema version: default v1.0
        "created": "2014-05-24T18:52:08.036814",   # created datetime in iso8601 format (added by backend)
        "updated": "2014-05-26T12:17:05.012544",   # updated datetime in iso8601 format (added by backend)
        "text": "Test note",                  # content of annotation
        "quote": "We",    # the annotated text (added by frontend)
        "ranges": [                                # list of ranges covered by annotation (usually only one entry)
            {
                "start": "/p[1]",                  # (relative) XPath to start element
                "end": "/p[1]",                    # (relative) XPath to end element
                "startOffset": 52,                 # character offset within start element
                "endOffset": 54                    # character offset within end element
            }
        ],
        "user": "edx_user",                        # user id of annotation owner (can also be an object with an 'id' property)
        "usage_id": "usage_id",                    # usage id of a component (added by frontend)
        "course_id": "course_id",                  # course id
    }

]
