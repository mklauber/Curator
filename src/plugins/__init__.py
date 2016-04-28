import pkgutil

import logging
logger = logging.getLogger(__name__)

def load_plugins(window):
    logger.info("Loading plugins")
    for loader, name, ispkg in pkgutil.walk_packages(path=__path__, prefix=__name__+'.'):
          plugin = loader.find_module(name).load_module(name)
          plugin.apply(window)