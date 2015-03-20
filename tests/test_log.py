import unittest
import os
import logging
import shutil
import setup_logging


class TestCentralLogger(unittest.TestCase):

    def setUp(self):

        # Remove 'logs' directory.
        self.logs_dir = setup_logging.get_log_path()
        shutil.rmtree(self.logs_dir, ignore_errors=True)

        # Standard LR configuration.
        logging.shutdown()
        setup_logging.setup_logging()

        # N.B.: this will return the same logger each time, so we need to reset.
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.NOTSET)

    def tearDown(self):
        shutil.rmtree(self.logs_dir, ignore_errors=True)

    def test_logs_dir_exists(self):
        assert os.access(self.logs_dir, os.F_OK) == True

    def test_audit_level(self):
        self.logger.setLevel(logging.AUDIT)
        assert self.logger.isEnabledFor(logging.AUDIT) == True

    def test_audit_name(self):
        assert logging.getLevelName(logging.AUDIT) == 'AUDIT'

    def test_setup_again_with_logs(self):
        """ 'logs' directory already exists """

        setup_logging.setup_logging()

    def test_setup_again_without_cfg(self):
        """ BasicConfig """

        setup_logging.setup_logging(default_cfg='logging.XXX')
        self.logger = logging.getLogger(__name__)
        assert self.logger.isEnabledFor(logging.INFO) == True

