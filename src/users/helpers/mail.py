import os

def send_register_mail(user_id, code):
    # TODO add API to send mail
    url = f'{os.getenv("BASE_URL")}/users/confirm/{user_id}_{code}'
    # connet with API to send mail
    print(url)
