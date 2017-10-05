# Do first page checks here
# since the module should only be loaded once this isn't performance critical here
# These commands should create legally required static files
import logging

logging.debug("performing basic init checks")
"""
if Profile.objects.all().count() < 1:
    from .magic import init_db
    logging.warning("(RE-)Initialized the database")
"""
