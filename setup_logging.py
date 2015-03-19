import os
import logging
import logging.config
import yaml

class AuditLogger(logging.getLoggerClass()):
    """ Custom logging class, to ensure that audit log calls always succeed.

        Refer to super()._log() directly to ensure correct stack frame.
    """

    def __init__(self, name):
        # super() call is required here but 'logging.' preferred, as class may not have relevant functions etc.
        super().__init__(name)

        try:
            logging.getLevelName(logging.AUDIT)
        except AttributeError as e:
            setattr(logging, 'AUDIT', logging.CRITICAL * 10)
            logging.addLevelName(logging.AUDIT, 'AUDIT')

    def audit(self, msg, *args, **kwargs):
        """ Add AUDIT level and ensure that it is enabled. """

        # This code derived from logging.log() call.
        if self.isEnabledFor(logging.AUDIT):
            super()._log(logging.AUDIT, msg, args, **kwargs)
        else:
            raise RuntimeError("logging.AUDIT level is disabled")


    def error(self, msg, *args, **kwargs):
        """ Add exception details to error() call. """

        # This code derived from logging.log() call.
        if self.isEnabledFor(logging.ERROR):
            kwargs["exc_info"] = True
            super()._log(logging.ERROR, msg, args, **kwargs)


def get_log_path(name=None):

    # 'logs' directory name is assumed - see "logging.yaml".
    log_path = 'logs'
    return log_path if name is None else log_path + '/' + name

def setup_logging(default_cfg='logging.yaml', default_level=logging.INFO, env_key='LOG_CFG'):
    """Setup logging configuration. """

    logging.setLoggerClass(AuditLogger)

    directory = os.path.dirname(__file__)
    default_cfg_path = os.path.join(directory, default_cfg)
    cfg_path = os.getenv(env_key, default_cfg_path)
    if os.path.exists(cfg_path):
        with open(cfg_path, 'rt') as f:
            config = yaml.load(f.read())

        # Make sure that directory for logs exists.
        try:
            os.mkdir(get_log_path())
        except OSError as e:
            pass

        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
