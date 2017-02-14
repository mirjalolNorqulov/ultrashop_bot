from woocommerce import API

#CONSUMER_KEY = 'ck_08852daa0456f44c9f659bd04391156293a6f6f1'
#CONSUMER_SECRET = 'cs_01c17a813efa8db9ee5a6d705bd27aa9623fd93d'

# Local keys
CONSUMER_KEY = 'ck_7de61e0848ea441cdfb1c8ac0c2e18ec995d4ac2'
CONSUMER_SECRET = 'cs_240169e37f692c3186e85ae02d826a70c7dc04eb'

TOKEN = '325218756:AAHl5tLSDL4F7HBD3DbPRaqFGU1DA3LxtLY'

wcapi = API(
    url='http://ultrashop.local',
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    timeout=15,
    wp_api=True,
    version="wc/v1",
    verify_ssl=False,
    query_string_auth=False

)
