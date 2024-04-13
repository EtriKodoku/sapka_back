import resend
from config import CONFIG

resend.api_key = CONFIG.resend_connection.get_secret_value()


template = 'Вітаємо, я Віра, ваш помічник. Для авторизації перейдіть <a href="{link}">за цим посиланням</a>'


def make_message(link, key):
    link = link.format(key=key)
    msg_with_link = template.format(link=link)
    return msg_with_link


def send_conf_mail_to(to: str, msg: str):
    params = {
        "from": "VIRA <vira@mail.ig4er.link>",
        "to": [to],
        "subject": "VIRA login",
        "html": msg
    }
    try:
        _ = resend.Emails.send(params)
    except Exception as E:
        print(E)
        return False
    return True
