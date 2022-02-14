from twilio.rest import Client
from config import ACC_ID, AUTH_TOKEN, FROM_PHONE_NUM, TO_PHONE_NUM

# def authenticate():
#     account_sid = ACC_ID
#     auth_token = AUTH_TOKEN
#     client = Client(account_sid, auth_token)
#     return client

# def sendMessage(text):
#     account_sid = ACC_ID
#     auth_token = AUTH_TOKEN
#     client = Client(account_sid, auth_token)
    
#     message = client.messages.create(
#                         body = text,
#                         from_ = FROM_PHONE_NUM,
#                         to = TO_PHONE_NUM)
#     message.sid

# sendMessage("text")

account_sid = ACC_ID
auth_token = AUTH_TOKEN
client = Client(account_sid, auth_token)

message = client.messages.create(
                    body = "Test",
                    from_ = FROM_PHONE_NUM,
                    to = TO_PHONE_NUM)
print(message.sid)