import os
import sys
import logging
import logging.config
import yaml

LOGS_DIR = 'logs'


# This filter is defined here, for reference within the 'logging.yaml' configuration file.
class LevelFilter(object):
    def __init__(self, level):
        # Get logging level for give name; note that getLevelName can return either int or str!
        self.__level = logging.getLevelName(level)
        assert isinstance(self.__level, int), "Level should be string"

    def filter(self, logRecord):
        return logRecord.levelno == self.__level

class AuditLogger(logging.getLoggerClass()):
    """ Custom logging class, to ensure that audit log calls always succeed.

        Refer to super()._log() directly to ensure correct stack frame.
    """

    def __init__(self, name):
        # super() call is preferred but we need to cater for Python 2 usage as well.
        super(AuditLogger, self).__init__(name)

        try:
            logging.getLevelName(logging.AUDIT)
        except AttributeError as e:
            setattr(logging, 'AUDIT', logging.CRITICAL * 10)
            logging.addLevelName(logging.AUDIT, 'AUDIT')

        if not self.isEnabledFor(logging.AUDIT):
            raise RuntimeError("logging.AUDIT level is disabled")

    def audit(self, msg, *args, **kwargs):
        """ Add AUDIT level and ensure that it is enabled. """

        # This code derived from logging.log() call.
        if self.isEnabledFor(logging.AUDIT):
            super(AuditLogger, self)._log(logging.AUDIT, msg, args, **kwargs)
        else:
            raise RuntimeError("logging.AUDIT level is disabled")


def setup_logging(default_level=logging.INFO):
    """Setup logging configuration. """

    # Make sure that directory for logs exists, before loading YAML file.
    try:
        os.mkdir(LOGS_DIR)
    except OSError as e:
        pass

    yaml_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
    yaml_path = os.getenv('LOGGING_YAML', os.path.join(yaml_dir, 'logging.yaml'))

    if os.path.exists(yaml_path):
        with open(yaml_path, 'rt') as f:
            config = yaml.load(f.read())
            logging.config.dictConfig(config)
    else:
        raise FileNotFoundError(log_path)

    logging.setLoggerClass(AuditLogger)
    logging.basicConfig(level=default_level)
