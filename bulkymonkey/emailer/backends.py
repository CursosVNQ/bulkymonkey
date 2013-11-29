from django.core.mail.backends.smtp import EmailBackend
from django.core.cache import cache


class BulkyMonkeyEmailBackend(EmailBackend):
    """
    Custom EmailBackend that push current state to cache
    """

    def send_messages(self, email_messages, cache_key=None):
        """
        Sends one or more EmailMessage objects and returns the number of email
        messages sent.
        """
        if not email_messages:
            return
        with self._lock:
            new_conn_created = self.open()
            if not self.connection:
                # We failed silently on open().
                # Trying to send would be pointless.
                return
            num_sent = 0
            for message in email_messages:
                sent = self._send(message)
                if sent:
                    num_sent += 1
                    if cache_key:
                        cache.set(cache_key, num_sent, None)
            if new_conn_created:
                self.close()
        return num_sent
