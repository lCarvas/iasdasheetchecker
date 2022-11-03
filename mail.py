import imaplib
import email

imap_server = "imap.gmail.com"
email_address = "mmiasdalmada@gmail.com"
password = "2022iasdamm"

imap = imaplib.IMAP4_SSL(imap_server)
imap.login(email_address, password)