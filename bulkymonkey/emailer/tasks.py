import base64
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.core.mail import EmailMultiAlternatives, get_connection

from bulkymonkey.celery import app


def attach_remove_link(host, message, email):
        """
        Adds a link at the end of the message that allows the user to stop receiving emails
        """

        signed_email = base64.b64encode(email.address)
        remove_link_text = _(u'Click here to stop receiving emails from us')
        remove_link_url = 'http://' + host + reverse('bulkymonkey:delete-signed-email', args=(signed_email,))
        message += '<br><a href="{}">{}</a>'.format(remove_link_url, remove_link_text.encode('utf-8'))
        return message


@app.task(bind=True)
def send_mail_mandrill_worker(self, host, campaign, sector, campaign_log):

    # Build cache key to show progress
    cache_key = 'progress-campaign:{}'.format(campaign_log.id)
    body = campaign.html_mail.read()

    # Send to Mandrill
    for i, email in enumerate(sector.email_set.all()):
        # Build message
        msg = EmailMultiAlternatives(
            subject=campaign.title,
            body='',
            from_email=u"{from_name} <{from_email}>".format(from_name=campaign.from_name,
                                                            from_email=campaign.from_email),
        )

        # Optional Mandrill-specific extensions:
        msg.tags = campaign.get_tags()
        msg.async = True
        msg.track_opens = True
        msg.track_clicks = True
        msg.to = [email.address]
        msg.attach_alternative(attach_remove_link(host, body, email), "text/html")
        msg.send()
        cache.set(cache_key, i + 1, None)

    # Change status
    campaign_log.is_sent = True
    campaign_log.save()
    cache.delete(cache_key)


@app.task(bind=True)
def send_mail_worker(self, host, campaign, sector, campaign_log):
    # Build cache key to show progress
    cache_key = 'progress-campaign:{}'.format(campaign_log.id)
    body = campaign.html_mail.read()
    connection = get_connection()

    messages = []
    for email in sector.email_set.all():
        # Build message
        msg = EmailMultiAlternatives(
            subject=campaign.title,
            body='',
            from_email=u"{from_name} <{from_email}>".format(from_name=campaign.from_name,
                                                            from_email=campaign.from_email),
        )

        # Optional Mandrill-specific extensions:
        msg.tags = campaign.get_tags()
        msg.async = True
        msg.track_opens = True
        msg.track_clicks = True
        msg.to = [email.address]
        msg.attach_alternative(attach_remove_link(host, body, email), "text/html")
        messages.append(msg)

    # Send mass emails
    connection.send_messages(messages, cache_key)

    # Change status
    campaign_log.is_sent = True
    campaign_log.save()
    cache.delete(cache_key)
