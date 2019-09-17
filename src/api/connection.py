import typing


class Connection:
    def __init__(self, api_token: str, host: str = 'https://api.gotinder.com/'):
        self.__api_token = api_token
        self.__host = host

    @property
    def host(self) -> str:
        return self.__host

    @property
    def headers(self) -> typing.Dict[str, str]:
        return {
            'app_version': '6.9.4',
            'platform': 'ios',
            'content-type': 'application/json',
            'User-agent': 'Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00)',
            'Accept': 'application/json',
            'X-Auth-Token': self.__api_token,
        }
