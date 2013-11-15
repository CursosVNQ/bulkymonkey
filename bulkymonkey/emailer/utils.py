# coding: utf-8

import string
import unicodedata


def cleanup_filename(filename):
    """
    from ñññññññṕṕ.jpg to nnnnnnnpp.jpg
    """
    filename = unicode(filename)
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    cleaned_filename = unicodedata.normalize('NFKD', filename)
    cleaned_filename = cleaned_filename.encode('ASCII', 'ignore')
    cleaned_filename = ''.join(c for c in cleaned_filename if c in valid_chars)
    return unicode(cleaned_filename.strip().replace(' ', '-').replace('(', '').replace(')', ''))


def get_filename_function(prefix):
    def inner(self, filename):
        filename = cleanup_filename(filename)
        return "{}/{}".format(prefix, filename)
    return inner
