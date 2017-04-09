import smtplib
import ConfigParser
import os
from datetime import datetime, timedelta

def send_email(user, pwd, subject, body, smtp_server, smtp_port):
    FROM = user
    TO = [user]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print 'successfully sent the mail'
    except:
        # TODO: give a more helpful error message
        print "failed to send mail"

if __name__ == "__main__":

    # open the config object
    this_dir = os.path.dirname(os.path.realpath(__file__))
    cp = ConfigParser.SafeConfigParser()
    cp.readfp(open(os.path.join(this_dir, 'config')))

    # check whether there are any files / folders to worry about
    # TODO: handle incorrect path
    unexplained = os.listdir(cp.get("Locations", "tracked_directory"))
    tracking_file = open(cp.get("Locations", "tracking_file"))
    for line in tracking_file:
        if line[0] == '#':
            unexplained = [i for i in unexplained if i not in line]

    # check whether it's appropriate to send the email or to wait.
    last_email_string = cp.get("Email", "last_email")
    last_email = datetime.strptime(last_email_string, "%Y-%m-%d %H:%M:%S.%f")
    waiting_days = int(cp.get("Email", "waiting_days"))
    waiting_seconds = int(cp.get("Email", "waiting_seconds"))
    email_waiting = timedelta(waiting_days, waiting_seconds)
    if (last_email + email_waiting < datetime.now()):
        # build the parts of the email
        subject = "Watchful McGrupp {}/{}".format(
            datetime.now().month, datetime.now().day)
        if len(unexplained) == 1:
            unexplained_insert = "an explanation for '" + unexplained[0] + "'"
        else:
            unexplained_insert = "explanations for '" + \
                "', '".join(unexplained[:-1]) + "', and '" + \
                unexplained[-1] + "'"
        body = "Watchful McGrupp notes that you're missing some explanations "\
            + "in your {} folder.\nIn particular, you are missing {}.".format(
                cp.get("Locations", "tracked_directory"), unexplained_insert)
        # send the actual email
        send_email(
            cp.get("Email", "username"), 
            cp.get("Email", "password"), 
            subject,
            body,
            cp.get("Email", "smtp_server"),
            cp.get("Email", "smtp_port")
        )
        # write that you indeed sent the email
        cp.set("Email", "last_email", datetime.now().__str__())
        cp.write(open(os.path.join(this_dir, 'config'), 'w'))