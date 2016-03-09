import os

_configuration = os.environ.get('DJANGO_CONFIGURATION', 'production').lower()

#
# Note that the order of module imports is important as each module needs boilerplate imports of preceding settings
#

# Always set production settings
from project.settings_prod import * # noqa

# Override with development settings if running dev-configuration
if _configuration == 'development':
    from project.settings_dev import * # noqa

# Replace Django's logging configuration completely by disabling it and manually setting our log configuration
# See http://stackoverflow.com/a/22336174/302484
import logging.config # noqa
logging.config.dictConfig(LOGGING)
LOGGING_CONFIG = None
