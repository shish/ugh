REPORT_CAUSE_SPAM = 1
REPORT_CAUSE_INAPPROPRIATE = 2

GENDER_MALE = 0
GENDER_FEMALE = 1

GENDER_MAP = {u'male': GENDER_MALE, u'female': GENDER_FEMALE}
GENDER_MAP_REVERSE = {GENDER_MALE: u'male', GENDER_FEMALE: u'female'}

PROFILE_FIELDS = [
    'gender', 'age_filter_min', 'age_filter_max', 'distance_filter',
    'bio', 'interested_in',
]

GLOBAL_HEADERS = {
    'app_version': '3',
    'platform': 'ios',
    'user-agent': 'Tinder/4.0.4 (iPhone; iOS 7.1.1; Scale/2.00)',
}

DEFAULT_AUTH_FILE_PATH = '~/.pytinder.json'
