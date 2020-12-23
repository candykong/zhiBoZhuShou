import pytest
import yaml
import  json

from common.commonTemplate import CommonTemplate
from testcase.testcasebase import Testcasebase



class Test_v2_create_user(Testcasebase):
    token = {'token': Testcasebase().getToken()}
    @pytest.mark.parametrize('casedata', yaml.safe_load(open("./data/data_v2_create_user.yaml")))
    # @pytest.mark.parametrize('casedata',[{'mobile': 3425,'username': 1500}])
    def test_sell_count(self, casedata):
        """
        批量创建账号
        """
        self.casedata=casedata
        self.data = casedata.update(self.token)
        self.data = CommonTemplate().template("./zhibozhushouApi/v2-create-user.yaml", self.casedata)
        self.getResponse(self.data)
        result_json = json.loads(self.r.text, strict=False)
        result = result_json["result"]
        msg = result["msg"]
        assert (self.r.status_code == 200)
        pytest.assume(msg == "success")


