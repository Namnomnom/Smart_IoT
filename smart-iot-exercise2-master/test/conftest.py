
def pytest_addoption(parser):
    parser.addoption("--url", action="store", default="http://localhost:8086")
    parser.addoption("--org", action="store", default="my-org")
    parser.addoption("--bucket", action="store", default="my-bucket")
    parser.addoption("--token", action="store", default="-Z8Px5qfHrg52MmKUgBmGz0i2KhsLyg48_WV5PmEg7W3XLLacgY7I28MAFiG1iskJ4w9dL44s6N1eqPToZCQ9A==")


def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    option_value = metafunc.config.option.url
    if 'url' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("url", [option_value])
    option_value = metafunc.config.option.org
    if 'org' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("org", [option_value])
    option_value = metafunc.config.option.bucket
    if 'bucket' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("bucket", [option_value])
    option_value = metafunc.config.option.token
    if 'token' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("token", [option_value])