import xmlrpclib

XMLRPC_SERVER = ""

class CookieTransport(xmlrpclib.Transport):
   def send_content(self, connection, request_body):
     if hasattr(self,'cookiename'):
       connection.putheader('Cookie', "%s=%s" % (self.cookiename, self.cookievalue))
     if hasattr(self,'token'):
       connection.putheader('X-CSRF-Token', "%s" % (self.token))
     return xmlrpclib.Transport.send_content(self, connection, request_body)


class User:
  def __init__(self, user):
    self.me = user
    self.uid = user['uid']
    self.username = user['name']
    self.surname = user['field_cognome']['und'][0]['value']
    self.name = user['field_nome']['und'][0]['value']
    self.dots = user['field_dots']['und'][0]['value']

  def getMe(self):
    return self.me

  def getUid(self):
    return int(self.uid)

  def getDots(self):
    return float(self.dots)

  def getName(self):
    return self.name

  def getSurname(self):
    return self.surname

  def getUsername(self):
    return self.username

  def setDots(self, dots):
    self.me['field_dots']['und'][0]['value'] = dots


class DrupalConnector():
  def __init__(self):
    self.transport = CookieTransport()
    self.server = xmlrpclib.Server(XMLRPC_SERVER , self.transport)

  def connect(self):
    self.server.system.connect()

  def login(self, username, password):
    print (">>> Login with user {}".format(username))
    self.user = self.server.user.login(username, password)
    self.transport.cookievalue = self.user['sessid']
    self.transport.cookiename = self.user['session_name']
    token = self.server.user.token()
    self.transport.token = token['token']

  def card_exists(self, cid): # true if exists, false if not exists
    userId = self.server.user.get_index(cid)    
    return (userId != False)

  def get_user(self, cid):
    print (">>> Get user with card {}".format(cid))
    userId = self.server.user.get_index(cid)
    if (userId == False):
      raise Exception("The card is not associated to any user")
    return self.server.user.retrieve(int(userId))

  def activate(self, username, cardId, notify):
    print (">>> {} -> {}".format(cardId, username))
    if (self.card_exists(cardId)):
      raise Exception("Card already associated to another user")

    userId = self.server.user.index(0, "uid", { 'name' : username }, 1)
    
    if (len(userId) < 1): # no person named 'username'
      raise Exception("No person named \"{}\"".format(username))

    uid = int(userId[0]['uid'])
    u = self.server.user.retrieve(uid)
    u['status'] = '1'
    u['notify'] = '1' if (notify == True) else '0'
    u['field_id'] = {'und': [{'safe_value': '' + str(cardId) + '', 'value': '' + str(cardId) + '', 'format': ''}]}
    self.server.user.update(uid,u)
    return True

  def update(self, user):
    print (">>> Updating user")
    uid = user.getUid()
    obj = user.getMe()
    return self.server.user.update(uid, obj)

  def create(self, user):
    print (">>> Creating user")
    return self.server.user.create(user)


