
一、框架组成部分
1.config下配置环境和数据库等配置信息
2.data配置用例的基本数据
3.db完成对数据库的操作
4.common.commomApi完成对接口的封装
5.zhibozhushouapi完成对api的驱动
6.service实现业务
7.testcase完成用例

二、依赖库
PyYaml requests pymysql pytest allure-pytest pytest_assume locust websocket jsonpath threadpool

三、使用allure运行
1.运行生成结果pytest ./testcase/test_sellApi.py --alluredir=./tmp/allure_results
2.生成报告：generate ./tmp/allure_results/ -o ./report/ --clean
3.打开报告：open -h 127.0.0.1 -p 8883 ./report/

