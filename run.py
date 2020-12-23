
import pytest
import os
import sys
from testcase.testcasebase import Testcasebase

if __name__ == '__main__':
    pytest.main(['-q','./testcase/test_sellApi.py'])
    # pytest.main(['-q', './testcase/test_v2_create_user.py'])

