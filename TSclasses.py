import requests
class Thingspeak(object):                       # define a class called Thingspeak

    """
    More Info: https://la.mathworks.com/help/thingspeak/rest-api.html
    """
    def __init__(self, read_api_key=None, channel_id=0):

        self.channel_id = channel_id
        self.read_api_key = read_api_key

        # Private Var cannot change
        self.__url = 'http://api.thingspeak.com/update?api_key'
        self.__read_url = 'https://api.thingspeak.com/channels/{}/feeds.json?api_key='.format(channel_id)


        #self.feild1 = []
        #self.feild2 = []

    def read_one_sensor(self, result=2):
        try:
            """
            :param result: how many data you want to fetch accept interger
            :return: Two List which contains Sensor data
            """

            URL_R = self.__read_url
            read_key = self.read_api_key
            header_r = '&results={}'.format(result)

            new_read_url = URL_R + read_key + header_r

            data = requests.get(new_read_url).json()

            feeds = data['feeds']
            channel = data['channel']

            '''for x in feeds:
                self.feild1.append(x['field1'])
                self.feild2.append(x['field2'])'''

            return feeds,channel
        except:
            print('read_one_sensor failed!')