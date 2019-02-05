import requests
from exceptions import AuthenticationError



class Client:

    def __init__(self):
        self.base_url = 'https://api.forcemanager.net/api/v4'
        self.api_key = ""
        self.private_key = ""
        self.headers = {'Accept': '*/*', 'Content-Type': 'application/json'}
        self.fm_token = ""
        self.logged_in = False


    def login(self, username=None, password=None):
        _api_key = username or self.api_key
        _private_key = password or self.private_key


        response = requests.post('%s/login' % self.base_url, json={"username": _api_key, "password": _private_key})
        json = response.json()

        self.fm_token = json['token']
        self.headers["X-Session-Key"] = self.fm_token
        self.logged_in = True
        return True


    def request(self, entity, method, entityId=None, params=None, data=None):

        if not self.logged_in:
            _loginResponse = self.login()
            if not _loginResponse:
                raise AuthenticationError(errors=_loginResponse.text)

        _method = method.lower()
        json_payload = data

        if _method == "get":
            if entityId:
                url = '%s/%s/%s' % (self.base_url, entity, entityId)
            else:
                url = '%s/%s' % (self.base_url, entity)

            response = requests.get(url, headers=self.headers, params=params)
        elif _method == "post":
            response = requests.post('%s/%s' % (self.base_url, entity), headers=self.headers, data=json.dumps(json_payload), params=params)
        return response.json()


    def ListWebHooks(self, page=None):
        return self.response('hooks', 'get')


    def CreateWebHook(self, action, entity, name, url, **kwargs):
        payload = {"action": action, "entity": entity, "name": name, "url": url}
        for key, value in kwargs.items():
            payload[key] = value


    def ListAccounts(self, page=None, where=None, order=None):
        return self.request('accounts', 'get')


    def RetrieveAccount(self, account_id):
        return self.request('accounts', 'get', entityId=account_id)


    def ListSales(self, page=None, where=None, order=None):
        return self.request('sales', 'get')


    def RetrieveSale(self, sale_id):
        return self.request('sales', 'get', entityId=sale_id)


    def ListSales(self, page=None, where=None, order=None):
        return self.request('sales', 'get')


    def RetrieveProduct(self, product_id):
        return self.request('products', 'get', entityId=product_id)


    def ListProducts(self, page=None, where=None, order=None):
        return self.request('products', 'get')
