import email
from email.message import Message
from html import parser
from typing import List, Union
import config
import imaplib
import quopri
import textwrap
import argparse


def auth(host: str, email_addr: str, email_pwd: str):
    mail = imaplib.IMAP4_SSL(host)
    response = mail.login(email_addr, email_pwd)
    response_msg = response[-1][0]
    if isinstance(response_msg, bytes):
        response_msg = response_msg.decode("utf-8")
    # print(response_msg)

    mail.select("inbox")

    return mail


def get_message(mail: imaplib.IMAP4_SSL, mail_id: int):
    data = mail.fetch(str(mail_id), 'RFC822')
    info_list = []
    for response_part in data:
        arr = response_part[0]
        if isinstance(arr, tuple):
            msg = email.message_from_string(arr[1].decode(encoding="utf-8"))
            info = {
                "subject": msg["Subject"],
                "date": msg["Date"],
                "from": msg["From"],
                "to": msg["To"],
                "content": process_payload(msg.get_payload()),
            }
            info_list.append(info)
    return info_list


def process_payload(content: Union[Message, List[Message]]):

    if isinstance(content, Message):
        content = [content]

    finallist = []
    for part in content:
        finallist.append({
            "type": part.get_content_type(),
            "payload": decode_quotes_printable(part.get_payload())
        })

    return finallist


def decode_quotes_printable(s: str):
    return quopri.decodestring(s.encode("utf-8")).decode("utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("idx", type=int)
    parser.add_argument("--no-format", action="store_true",
                        help="Whether to reduce format.")
    args = parser.parse_args()
    mail = auth(config.SMTP_SERVER, config.FROM_EMAIL, config.FROM_PWD)
    idx = args.idx
    msg = get_message(mail, idx)[0]
    clean_text = None
    for c in msg["content"]:
        if c["type"] == "text/html":
            clean_text = config.H2T.handle(c["payload"])
        elif clean_text is None and c["type"] == "text/plain":
            clean_text = c["payload"]

    print("{:10s} {}".format("From:", msg["from"]))
    print("{:10s} {}".format("Date:", msg["date"]))
    print("{:10s} {}".format("Subject:", msg["subject"]))
    print("{:10s} {}".format("To:", msg["to"]))
    print("{:10s}".format("Content:"))
    if args.no_format:
        print(textwrap.fill(clean_text, initial_indent='\t', subsequent_indent='\t'))
    else:
        print(clean_text)
