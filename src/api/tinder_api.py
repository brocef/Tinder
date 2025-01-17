import json
import requests
from src.api.connection import Connection


# def get_auth_token(fb_auth_token, fb_user_id):
#     if "error" in fb_auth_token:
#         return {"error": "could not retrieve fb_auth_token"}
#     if "error" in fb_user_id:
#         return {"error": "could not retrieve fb_user_id"}
#     url = config.host + '/auth'
#     req = requests.post(url,
#                         headers=self.connection.headers,
#                         data=json.dumps(
#                             {'facebook_token': fb_auth_token, 'facebook_id': fb_user_id})
#                         )
#     try:
#         tinder_auth_token = req.json()["token"]
#         headers.update({"X-Auth-Token": tinder_auth_token})
#         print("You have been successfully authorized!")
#         return tinder_auth_token
#     except Exception as e:
#         print(e)
#         return {"error": "Something went wrong. Sorry, but we could not authorize you."}
#
#
# def authverif():
#     res = get_auth_token(config.fb_access_token, config.fb_user_id)
#     if "error" in res:
#         return False
#     return True


class TinderAPI:
    def __init__(self, connection: Connection):
        self.__connection = connection

    @property
    def connection(self) -> Connection:
        return self.__connection

    def build_url(self, *path_components: str):
        return self.connection.host + '/'.join(path_components)

    def get_top_picks(self):
        try:
            url = self.build_url('v2', 'top-picks', 'preview')
            r = requests.get(url, headers=self.connection.headers)
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong with getting recommendations:", e)

    def get_recommendations(self):
        """
        Returns a list of users that you can swipe on
        """
        try:
            url = self.build_url('user', 'recs')
            r = requests.get(url, headers=self.connection.headers)
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong with getting recommendations:", e)

    def get_updates(self, last_activity_date=""):
        """
        Returns all updates since the given activity date.
        The last activity date is defaulted at the beginning of time.
        Format for last_activity_date: "2017-07-09T10:28:13.392Z"
        """
        try:
            url = self.build_url('updates')
            r = requests.post(url,
                              headers=self.connection.headers,
                              data=json.dumps({"last_activity_date": last_activity_date})
                              )
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong with getting updates:", e)

    def get_self(self):
        """
        Returns your own profile data
        """
        try:
            url = self.build_url('profile')
            r = requests.get(url, headers=self.connection.headers)
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not get your data:", e)

    def change_preferences(self, **kwargs):
        """
        ex: change_preferences(age_filter_min=30, gender=0)
        kwargs: a dictionary - whose keys become separate keyword arguments and the values become values of these arguments
        age_filter_min: 18..46
        age_filter_max: 22..55
        age_filter_min <= age_filter_max - 4
        gender: 0 == seeking males, 1 == seeking females
        distance_filter: 1..100
        discoverable: true | false
        {"photo_optimizer_enabled":false}
        """
        try:
            url = self.build_url('profile')
            r = requests.post(url, headers=self.connection.headers, data=json.dumps(kwargs))
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not change your preferences:", e)

    def get_meta(self):
        """
        Returns meta data on yourself. Including the following keys:
        ['globals', 'client_resources', 'versions', 'purchases',
        'status', 'groups', 'products', 'rating', 'tutorials',
        'travel', 'notifications', 'user']
        """
        try:
            url = self.build_url('meta')
            r = requests.get(url, headers=self.connection.headers)
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not get your metadata:", e)

    def get_meta_v2(self):
        """
        Returns meta data on yourself from V2 API. Including the following keys:
        ['account', 'client_resources', 'plus_screen', 'boost',
        'fast_match', 'top_picks', 'paywall', 'merchandising', 'places',
        'typing_indicator', 'profile', 'recs']
        """
        try:
            url = self.build_url('v2', 'meta')
            r = requests.get(url, headers=self.connection.headers)
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not get your metadata:", e)

    def update_physical_location(self, lat: float, lon: float):
        """
        Updates your location to the given float inputs, as if you were there.
        Note: This does NOT require a passport / Tinder Plus
        """
        try:
            url = self.build_url('v2', 'meta')
            data = {
                "lat": lat,
                "lon": lon,
                "force_fetch_resources": False
            }
            r = requests.post(url, headers=self.connection.headers, data=json.dumps(data))
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not update your physical location:", e)

    def update_passport_location(self, lat: float, lon: float):
        """
        Updates your location to the given float inputs
        Note: Requires a passport / Tinder Plus
        """
        try:
            url = self.build_url('passport', 'user', 'travel')
            r = requests.post(url, headers=self.connection.headers, data=json.dumps({"lat": lat, "lon": lon}))
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not update your passport location:", e)

    def reset_real_location(self):
        try:
            url = self.build_url('passport', 'user', 'reset')
            r = requests.post(url, headers=self.connection.headers)
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not update your location:", e)

    def get_recs_v2(self):
        """
        This works more consistently then the normal get_recommendations becuase it seeems to check new location
        """
        try:
            url = self.build_url('v2', 'recs', 'core')
            r = requests.get(url, headers=self.connection.headers, params={'locale': 'en-US'})
            return r.json()
        except Exception as e:
            print('excepted')

    def set_webprofileusername(self, username: str):
        """
        Sets the username for the webprofile: https://www.gotinder.com/@YOURUSERNAME
        """
        try:
            url = self.build_url('profile', 'username')
            r = requests.put(url, headers=self.connection.headers,
                             data=json.dumps({"username": username}))
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not set webprofile username:", e)

    def reset_webprofileusername(self):
        """
        Resets the username for the webprofile
        """
        try:
            url = self.build_url('profile', 'username')
            r = requests.delete(url, headers=self.connection.headers)
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not delete webprofile username:", e)

    def get_person(self, profile_id: str):
        """
        Gets a user's profile via their profile_id
        """
        try:
            url = self.build_url('user', profile_id)
            r = requests.get(url, headers=self.connection.headers)
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not get that person:", e)

    def send_msg(self, match_id: str, msg: str):
        try:
            url = self.build_url('user', 'matches', match_id)
            r = requests.post(url, headers=self.connection.headers,
                              data=json.dumps({"message": msg}))
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not send your message:", e)

    def unmatch(self, match_id: str):
        try:
            url = self.build_url('user', 'matches', match_id)
            r = requests.delete(url, headers=self.connection.headers)
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not unmatch person:", e)

    def superlike(self, person_id: str):
        try:
            url = self.build_url('like', person_id, 'super')
            r = requests.post(url, headers=self.connection.headers)
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not superlike:", e)

    '''
    Sample response:
    
    {'match': {'_id': '5ac6f6ad0c8b3b6122ccd4cb5d78768166e7e3dc6b90e59f', 'closed': False, 'common_friend_count': 0, 'common_like_count':
    0, 'created_date': '2019-09-23T20:41:55.895Z', 'dead': False, 'last_activity_date': '2019-09-23T20:41:55.895Z', 'message_count': 0, 'm
    essages': [], 'participants': ['5d78768166e7e3dc6b90e59f', '5ac6f6ad0c8b3b6122ccd4cb'], 'pending': False, 'is_super_like': False, 'is_
    boost_match': False, 'is_super_boost_match': False, 'is_fast_match': False, 'is_top_pick': False, 'following': True, 'following_moment
    s': True}, 'likes_remaining': 100, 'X-Padding': '{*meta*:{*code*:200,*requestId*:*59a45921351e3d43b07028b5*},*response*:{*venue*:{*id*
    :*412d2800f964a520df0c1fe3*,*name*:*Central Park*,*contact*:{*phone*:*2123106600*,*formattedPhone*:*(212) 310-6600*,*twitter*:*central
    parknyc*,*instagram*:*centralparknyc*,*facebook*:*37965424481*,*facebookUsername*:*centralparknyc*,*facebookName*:*Central Park*},*loc
    ation*:{*address*:*59th St to 110th St*,*crossStreet*:*5th Ave to Central Park West*,*lat*:40.78408342593807,*lng*:-73.96485328674316,
    *postalCode*:*10028*,*cc*:*US*,*city*:*New York*,*state*:*NY*,*country*:*United States*,*formattedAddress*:[*59th St to 110th St (5th
    Ave to Central Park West)*,*New York, NY 10028*,*United States*]},*canonicalUrl*:*https://foursquare.com/v/central-park/412d2800f964a5
    20df0c1fe3*,*categories*:[{*id*:*4bf58dd8d48988d163941735*,*name*:*Park*,*pluralName*:*Parks*,*shortName*:*Park*,*icon*:{*prefix*:*htt
    ps://ss3.4sqi.net/img/categories_v2/parks_outdoors/park_*,*suffix*:*.png*},*primary*:true}],*verified*:true,*stats*:{*checkinsCount*:3
    64591,*usersCount*:311634,*tipCount*:1583,*visitsCount*:854553},*url*:*http://www.centralparknyc.org*,*likes*:{*count*:17370,*summary*
    :*17370 Likes*},*rating*:9.8,*ratingColor*'}
    '''
    def like(self, person_id: str):
        try:
            url = self.build_url('like', person_id)
            r = requests.get(url, headers=self.connection.headers)
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not like:", e)

    def dislike(self, person_id: str):
        try:
            url = self.build_url('pass', person_id)
            r = requests.get(url, headers=self.connection.headers)
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not dislike:", e)

    def report(self, person_id: str, cause, explanation=''):
        """
        There are three options for cause:
            0 : Other and requires an explanation
            1 : Feels like spam and no explanation
            4 : Inappropriate Photos and no explanation
        """
        try:
            url = self.build_url('report', person_id)
            r = requests.post(url, headers=self.connection.headers, data={
                "cause": cause, "text": explanation})
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not report:", e)

    def match_info(self, match_id: str):
        try:
            url = self.build_url('matches', match_id)
            r = requests.get(url, headers=self.connection.headers)
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not get your match info:", e)

    def all_matches(self):
        try:
            url = self.build_url('v2', 'matches')
            r = requests.get(url, headers=self.connection.headers)
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not get your match info:", e)

    def fast_match_info(self):
        try:
            url = self.build_url('v2', 'fast-match', 'preview')
            r = requests.get(url, headers=self.connection.headers)
            count = r.headers['fast-match-count']
            # image is in the response but its in hex..
            return count
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not get your fast-match count:", e)

    def fast_match_teasers(self):
        try:
            url = self.build_url('v2', 'fast-match', 'teasers')
            r = requests.get(url, headers=self.connection.headers)
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not get your fast-match count:", e)

    def trending_gifs(self, limit: int = 3):
        try:
            url = self.build_url('giphy', 'trending')
            r = requests.get(url, headers=self.connection.headers, params={'limit': limit})
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not get the trending gifs:", e)

    def gif_query(self, query: str, limit=3):
        try:
            url = self.build_url('giphy', 'search')
            params = {
                'limit': limit,
                'query': query,
            }
            r = requests.get(url, headers=self.connection.headers, params=params)
            return r.json()
        except requests.exceptions.RequestException as e:
            print("Something went wrong. Could not get your gifs:", e)
