from html2text import HTML2Text
ORG_EMAIL   = "@gmail.com"
FROM_EMAIL  = "" + ORG_EMAIL  # username
FROM_PWD    = ""  # password
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993
H2T = HTML2Text()
H2T.ignore_images = True
H2T.ignore_links = True
H2T.ignore_tables = True
H2T.ignore_emphasis = True