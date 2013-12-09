from optparse import make_option
import getpass
import poplib
from email import message_from_string
from django.core.management.base import BaseCommand
from flufl.bounce import all_failures
from emailer.models import Email


class Command(BaseCommand):
    help = 'Connects to a POP3 mail server and scans for bounced emails, then removes bounced emails from django model'

    option_list = BaseCommand.option_list + (
        make_option('--delete',
                    action='store_true',
                    dest='delete',
                    default=False,
                    help='Remove bounced emails from database'),
    )

    def handle(self, *args, **options):
        user = raw_input('Email login: ')
        host = user.split('@')[1]
        passwd = getpass.getpass()
        mail_server = poplib.POP3_SSL(host)
        mail_server.user(user)
        mail_server.pass_(passwd)

        emails_to_delete = set()
        num_messages = len(mail_server.list()[1])
        for i in range(num_messages):
            msg = '\n'.join(mail_server.retr(i+1)[1])
            parsed_email = message_from_string(msg)
            try:
                temporary, permanent = all_failures(parsed_email)
            except Exception:
                self.stderr.write('Skipping message {} ({})\n'.format(parsed_email['Subject'], parsed_email['From']))
                continue

            if temporary:
                emails_to_delete |= temporary
                for email in temporary:
                    self.stdout.write("temporary bounce: {}\n".format(email))
            if permanent:
                emails_to_delete |= permanent
                for email in permanent:
                    self.stdout.write("permanent bounce: {}\n".format(email))

        self.stdout.write('Total {} emails\n'.format(len(emails_to_delete)))
        if options['delete']:
            queryset = Email.objects.filter(address__in=emails_to_delete)
            num_deleted_emails = queryset.count()
            queryset.delete()
            self.stdout.write('Deleted {} emails\n'.format(num_deleted_emails))

        mail_server.quit()
