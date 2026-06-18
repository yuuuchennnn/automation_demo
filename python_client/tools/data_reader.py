import os
import yaml

"""
read yaml from path
"""
def yamlDataProvider(path):
    project_name = 'python_client'
    testDataPath = os.path.join(os.path.abspath(os.curdir).split(project_name)[0],project_name)
    if 'TestData' not in path:
        testDataPath = os.path.join(testDataPath,'TestData')
    path = os.path.join(testDataPath, path)
    case = []  # 存储测试用例名称
    case_info = []  # 存储测试用例信息
    test_data = []  # 存储测试参数
    check_data =[]  # 校验信息
    with open(path) as f:
        dat = yaml.load(f.read(), Loader=yaml.SafeLoader)
        for td in dat:
            test_id = td.get('testCase').get('testId')
            test_name = td.get('testCase').get('testName',{})
            case.append(test_id if test_id else test_name)
            case_info.append(td.get('testCase', {}))
            test_data.append({}) if td.get('testData') is None else test_data.append(td.get('testData', {}))
            test_data[-1]['caseid'] = test_id if test_id else test_name  #
    # return [pytest.param(test_data[x],id=case[x] ) for x in range(case)]

    return test_data