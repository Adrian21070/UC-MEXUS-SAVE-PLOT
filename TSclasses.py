'''
----------------------------------------------------------
    @file: TSclasses.py
    @date: Sept 2021
    @date_modif: Dec 22, 2021
    @author: Soumil shah
    @e-mail:soushah@my.bridgeport.edu 
    @modified by: Raul Dominguez
    @e-mail: a01065986@itesm.mx
    @brief: Modified version of the script masterclass.py from Soumil shah. This version only retrieves the
            information from a thingspeak channel
----------------------------------------------------------
'''
import requests
class Thingspeak(object):                       # define a class called Thingspeak

    """
    More Info: https://la.mathworks.com/help/thingspeak/rest-api.html
    """
    def __init__(self, read_api_key=None, channel_id=0):
        # We need this format to extract data with a range of time.
        # https://api.thingspeak.com/channels/1336916/feeds.csv?api_key=F2K1DV64M1Z75VU4&start=2022-03-11%2010:10:10&end=2022-03-14%2011:11:11

        self.channel_id = channel_id
        self.read_api_key = read_api_key

        # Private Var cannot change
        #self.__url = 'http://api.thingspeak.com/update?api_key'
        self.__read_url = 'https://api.thingspeak.com/channels/{}/feeds.json?api_key='.format(channel_id)

    def read_one_sensor(self, start='2022-03-10', end='2022-03-11'):
        try:
            """
            @param result: how many data you want to fetch accept interger
            @return: Two List which contains Sensor data
            """

            URL_R = self.__read_url
            read_key = self.read_api_key
            
            header_t = '&start={}'.format(start)
            header_t2 = '&end={}'.format(end)
            #header_r = '&results={}'.format(result)

            #new_read_url = URL_R + read_key + header_r
            new_read_url = URL_R + read_key + header_t + header_t2

            data = requests.get(new_read_url).json()

            feeds = data['feeds']
            channel = data['channel']

            '''for x in feeds:
                self.feild1.append(x['field1'])
                self.feild2.append(x['field2'])'''

            return feeds,channel
        except:
            print('read_one_sensor failed!')