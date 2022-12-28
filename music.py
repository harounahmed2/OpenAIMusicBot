class MusicBot:
    ''' This object eases markdown and display of welcome message
    '''

    WELCOME_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "Hello Haroun!  Welcome to musicBot, your friendly music explorer powered by OpenAI! - how may I be of service? :grin:\n\n"
                "*Please see options below:*"
            ),
        },
    }

    DIVIDER_BLOCK = {"type": "divider"}

    OPTIONS_BLOCK = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": (
                    " *Choose from the following options* :arrow_down:\n"
                    "*Time Machine* :clock1: : Discover music from artists from a year in the past\n"
                    "*Genre* :raised_hands: : Discover music based on a genre\n"
                    "*Global Explorer* :earth_americas: : Discover music based on a geographic location \n"
                    "*Popular* :mega: : Discover popular music \n"
                    "*Surprise Me* :interrobang: : Discover music based on random criteria \n"
                ),
            },
        }


    def __init__(self, channel):
        self.channel = channel
        self.username = "musicBot"
        self.timestamp = ''
        self.icon_emoji = ":musical_note:"

    def get_welcomeMessage_payload(self):
        return {
                "ts": self.timestamp,
                "channel": self.channel,
                "username": self.username,
                "icon_emoji": self.icon_emoji,
                "blocks": [
                    self.WELCOME_BLOCK,
                    self.DIVIDER_BLOCK,
                    self.OPTIONS_BLOCK,
                ],
            }
