import logging
try:
    from playwright._impl._api_types import Error, TimeoutError
except Exception as e:
    logging.getLogger().error(e)


class NoSuchOptionError(Error):
    ...
