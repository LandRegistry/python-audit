import os
import logging
import logging.config
import yaml


def get_log_path(name=None):

    # 'logs' directory name is assumed - see "logging.yaml".
    log_path = 'logs'
    return log_path if name is None else log_path + '/' + name

def setup_logging(default_cfg='logging.yaml', default_level=logging.INFO, env_key='LOG_CFG'):
    """Setup logging configuration. """

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
