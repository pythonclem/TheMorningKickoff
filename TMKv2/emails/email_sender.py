from .get_email_data import usersAndTeams, generateEmailData, generate_html_block 
from .mailjet import sendEmail

def sendEmails():
    usersandteams = usersAndTeams()
    for user in usersandteams:
        emaildata = generateEmailData(user, usersandteams)
        generate_html_block(emaildata['matches'])
        sendEmail(emaildata['userinfo']['email'])