
from typing import Dict
import json

import aamras.driver.cookies as cookies
import aamras.util as util

cookie_data = {
    "domain": "example.com",
    "expiry": 2219773312,
    "httpOnly": True,
    "name": "q",
    "path": "/",
    "value": "",
    "secure": True
}

test_cookie_file = "cookies.test.json"

def create_cookie(domain: str = "example.com") -> Dict:
    cookie = dict(cookie_data)
    cookie["domain"] = domain

    return cookie

def test_with_valid_expiry_millis():
    cookie = create_cookie()
    cookie["expiry"] = 2219773.312

    cookie_adjusted = cookies.with_valid_expiry(cookie)
    assert cookie_adjusted["expiry"] == 2219773312

def test_with_valid_expiry_seconds():
    cookie = create_cookie()

    cookie_adjusted = cookies.with_valid_expiry(cookie)
    assert cookie_adjusted["expiry"] == cookie["expiry"]

def get_manager():
    return cookies.CookieManager(test_cookie_file)

def test_cookie_manager_get():
    with util.deleting(test_cookie_file):
        cookies = [cookie_data]

        with open(test_cookie_file, "w") as file_:
            file_.write(json.dumps(cookies))

        manager = get_manager()
        assert manager.get() == cookies

def test_cookie_manager_save_single():
    with util.deleting(test_cookie_file):
        get_manager().save(cookie_data)

        with open(test_cookie_file) as file_:
            assert file_.read() == json.dumps([cookie_data])

def test_cookie_manager_save_list():
    with util.deleting(test_cookie_file):
        get_manager().save([cookie_data])

        with open(test_cookie_file) as file_:
            assert file_.read() == json.dumps([cookie_data])

def test_cookie_manager_add_replaces():
    with util.deleting(test_cookie_file):
        manager = get_manager()
        new_cookie = create_cookie()
        new_cookie["httpOnly"] = False

        manager.add(cookie_data)
        manager.add(new_cookie)

        assert manager.get() == [new_cookie]

class Test(cookies.CookieManagerMixin, object):
    pass

def test_cookie_manager_mixin():
    test = Test()
    assert test.cookies
