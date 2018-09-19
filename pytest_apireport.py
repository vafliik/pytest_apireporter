# -*- coding: utf-8 -*-

import pytest
import requests

project_id = 0
build_nr = 0
api_url = ''
test_run_id = 0

def pytest_addoption(parser):
    group = parser.getgroup('apireport')
    group.addoption(
        '--build',
        action='store',
        dest='build_nr',
        default='custom',
        help='Specify the build number under test'
    )

    parser.addini('project_id', 'Project ID')
    parser.addini('api_url', 'Api URL')

def pytest_configure(config):
    global api_url, build_nr, project_id
    build_nr = config.getoption('build_nr')
    project_id = config.getini('project_id')
    api_url = config.getini('api_url')

def report_start_test(test_names):
    build_info = {'build_nr': build_nr, 'comment': "XThis will fail for sure"}
    test_run_info = {'status': 'Running', 'comment': "Now really with tests"}
    r=requests.post(f'{api_url}/projects/{project_id}/builds', json=build_info)
    r=requests.post(f'{api_url}/projects/{project_id}/builds/{build_nr}/runs', json=test_run_info)
    global test_run_id
    test_run_id = r.json()["id"]
    tests_info = {'test_names': test_names, 'test_run_id': test_run_id}
    r=requests.post(f'{api_url}/projects/{project_id}/tests', json=tests_info)

    print("[API Report] Sending collected tests ({}) for build #{}".format(len(test_names), build_nr))

def pytest_runtest_logstart(nodeid, location):
    test_name = location[2].split('.')[-1]
    r = requests.patch(f'{api_url}/projects/{project_id}/results/{test_run_id}/{test_name}', json={"status": "Running"})

def pytest_runtest_logreport(report):
    #TODO: This will NOT report errors during setup/teardown
    if report.when == "call":
        test_name = report.location[2].split('.')[-1]
        status = report.outcome.capitalize()
        r = requests.patch(f'{api_url}/projects/{project_id}/results/{test_run_id}/{test_name}', json={"status": status})

def pytest_sessionfinish(session, exitstatus):
    status = "Passed" if exitstatus == 0 else "Failed"
    comment = f"Tests failed: {session.testsfailed}"
    r = requests.patch(f'{api_url}/projects/{project_id}/builds/{build_nr}/runs/{test_run_id}',
                       json={"status": status, "comment": comment})

def pytest_collection_finish(session):
    test_names = [item.name for item in session.items]

    # alfred.build_nr=pytest.config.getoption('xbuildname')
    report_start_test(test_names)

def pytest_terminal_summary(terminalreporter):
    """add additional section in terminal summary reporting
    :param terminalreporter:
    :return:
    """

    terminalreporter.write_sep('*', f"Reports sent to {api_url}!")


@pytest.fixture
def bar(request):
    return request.config.option.dest_foo
