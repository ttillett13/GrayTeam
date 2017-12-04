import smtplib

from email.utils import formatdate
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

from email import encoders
import os, datetime

#config = fileutil.social


def send_invite(param):
    CRLF = "\r\n"
    attendees = ','.join(param['to'])
    fro = "sourceiron.confirmation@gmail.com"

    msg = MIMEMultipart('mixed')
    msg['Reply-To'] = fro
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = param['subject']
    msg['From'] = fro
    msg['To'] = attendees

    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    f = os.path.join(__location__, 'invite.ics')
    ics_content = open(f).read()

    replaced_contents = ics_content.replace('startDate', param['startDate'])
    replaced_contents = replaced_contents.replace('endDate', param['endDate'])
    replaced_contents = replaced_contents.replace('telephonic', param['location'])
    replaced_contents = replaced_contents.replace('token', param['token'])
    replaced_contents = replaced_contents.replace('now', datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ"))

    if param.get('describe') is not None:
        description = param.get('describe') + "\\n\\n"
        description += "Attached Group Links\\n"
        for link in param['links']:
            description += (link.display_text + ": " + link.link) + "\\n"
        replaced_contents = replaced_contents.replace('describe', description)
    else:
        replaced_contents = replaced_contents.replace('describe', '')
    replaced_contents = replaced_contents.replace('attend', ','.join(msg['To']))
    replaced_contents = replaced_contents.replace('subject', param['subject'])
    part_email = MIMEText(replaced_contents, 'calendar;method=REQUEST')

    start_datetime = datetime.datetime.strptime(param['startDate'], "%Y%m%dT%H%M%SZ").strftime('%m/%d/%Y %I:%M %p')
    end_datetime = datetime.datetime.strptime(param['endDate'], "%Y%m%dT%H%M%SZ").strftime('%m/%d/%Y %I:%M %p')
    body = "You have been invited to a CramCom Group Study Session \"" + param['session_name'] + "\" for the group \"" + param['group_name'] + "\"\n"
    body += "Meeting Time: " + start_datetime + " - " + end_datetime + "\n\n"

    # Attach the group links
    body += "Group Attached Links:\n"
    for link in param['links']:
        body += (link.display_text + ": " + link.link + "\n")
    msg.attach(MIMEText(body, 'plain'))

    msgAlternative = MIMEMultipart('alternative')

    ical_atch = MIMEBase('text/calendar', ' ;name="%s"' % "invitation.ics")
    ical_atch.set_payload(replaced_contents)
    encoders.encode_base64(ical_atch)
    ical_atch.add_header('Content-Disposition', 'attachment; filename="%s"' % f)

    msgAlternative.attach(part_email)
    #msgAlternative.attach(ical_atch)
    msg.attach(msgAlternative)
    mailServer = smtplib.SMTP('email-smtp.us-west-2.amazonaws.com', 25)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login('AKIAJF3Y2UR6X33EJASA', 'Ag73aslUyhmZbFHB4nb+CRioHOJF5lvRoRYmU6gkMvaY')
    mailServer.sendmail(fro, param['to'], msg.as_string())


    mailServer.close()
