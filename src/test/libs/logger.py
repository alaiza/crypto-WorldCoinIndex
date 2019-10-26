import logging
import logging.config
import os

import yaml


def factory_logger(logger_name, config_file_path=None):
    if config_file_path and os.path.exists(config_file_path):
        with open(config_file_path, 'r') as f:
            config = yaml.safe_load(f.read())
            _if_not_exist_create_log_file(config)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=logging.INFO)

    return logging.getLogger(logger_name)


def _if_not_exist_create_log_file(config):
    handlers = config['handlers']
    for handler_name in handlers:
        handler = handlers[handler_name]
        if 'class' in handler:
            if 'FileHandler' in handler['class']:
                path_file_log = handler['filename']
                dir_log = os.path.dirname(path_file_log)
                if not os.path.exists(dir_log):
                    os.mkdir(dir_log)
