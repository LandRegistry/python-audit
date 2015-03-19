import os
import logging
import logging.config
import yaml

class LevelFilter(logging.Filter):
    def __init__(self, level=None):
        super().__init__()
        self.level = level

    def filter(self, record):
        if self.level is None:
            allow = True
        else:
            allow = (self.level == record.levelname)
        return allow

class AuditLogger(logging.getLoggerClass()):
    """ Custom logging class, to ensure that audit log calls always succeed. """

    def __init__(self, name):
        super().__init__(name)

    def audit(self, msg, *args, **kwargs):
        msg = "[AUDIT] " + msg
        super().critical(msg, *args, **kwargs)
        self._log(logging.CRITICAL, msg, args, **kwargs)


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
