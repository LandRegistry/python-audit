import os
import logging.config
import yaml
import pdb

def get_log_path(name=None):
    log_path = os.getenv('LOG_PATH', 'logs')
    # return log_path if name is None else os.path.join(log_path, name)
    return log_path if name is None else log_path + '/' + name

def setup_logging(default_path='logging.yaml', default_level=logging.INFO, env_key='LOG_CFG'):
    """Setup logging configuration. """

    pdb.set_trace()
    path = os.getenv(env_key, default_path)
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.load(f.read())

        # Make sure that directory for logs exists.
        try:
            os.mkdir(get_log_path())
        except OSError as e:
            pass

        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
