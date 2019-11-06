import logging
from mailjet_rest import Client


_logger = logging.getLogger(__name__)


class EMailService:

    def __init__(self,email_api_key,email_secret_key, email_version):
        self.__api_key = email_api_key
        self.__api_secret = email_secret_key
        self.__mailjet = Client(auth=(self.__api_key , self.__api_secret), version='v3.1')
        self.__data = ''


    def Genemail(self, daystored, num_cryptos, num_rows):
        self.__data = {
            'Messages': [
                {
                    "From": {
                        "Email": "alaiza.projects@gmail.com",
                        "Name": "Jorge"
                    },
                    "To": [
                        {
                            "Email": "kokealaiza@gmail.com",
                            "Name": "Jorge"
                        }
                    ],
                    "Subject": "Statistics for ending day: "+daystored,
                    "TextPart": "My first Mailjet email",
                    "HTMLPart": "<h3>Dear Alaiza, here you have your crypto-stats"
                                "<br /> Number of cryptos being downloaded: "+num_cryptos+
                                "<br /> Number of rows downloaded: "+num_rows,
                    "CustomID": "AppGettingStartedTest"
                }
            ]
        }
        self.__mailjet.send.create(data=self.__data)






