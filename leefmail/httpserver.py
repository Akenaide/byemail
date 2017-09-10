import os
import asyncio
import datetime

from sanic import Sanic
from sanic.response import json, redirect

from tinydb import Query

from leefmail.mailstore import storage

app = Sanic(__name__)

BASE_DIR = os.path.dirname(__file__)

app.static('/static', os.path.join(BASE_DIR, '../client/dist/static'))
app.static('/index.html', os.path.join(BASE_DIR, '../client/dist/index.html'))

@app.route('/')
async def index(request):
    return redirect('/index.html')

@app.route("/api/mailboxes")
async def mailboxes(request):
    mbxs = await storage.get_mailboxes()
    for m in mbxs:
        if isinstance(m['last_message'], datetime.datetime): # Also strange hack
            m['last_message'] = m['last_message'].isoformat()
    return json(mbxs)

@app.route("/api/mailbox/<mailbox_id>")
async def mailbox(request, mailbox_id):
    mailbox_to_return = await storage.get_mailbox(mailbox_id)
    for m in mailbox_to_return['messages']:
        if isinstance(m['date'], datetime.datetime): # Also strange hack
            m['date'] = m['date'].isoformat()
    return json(mailbox_to_return)

@app.route("/api/mail/<mail_id>")
async def mailb(request, mail_id):
    mail_to_return = await storage.get_mail(mail_id)
    if isinstance(mail_to_return['date'], datetime.datetime): # Also strange hack
        mail_to_return['date'] = mail_to_return['date'].isoformat()
    return json(mail_to_return)
