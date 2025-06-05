import pytest
from unittest.mock import patch, Mock

from src.headHunterAPI import HeadHunterAPI


@pytest.fixture
def hh_api():
    return HeadHunterAPI()

def test_init_attrs(hh_api):
    assert hh_api.url == "https://api.hh.ru/vacancies"
    assert "User-Agent" in hh_api.headers
    assert isinstance(hh_api.params, dict)
    assert hh_api.vacancies == []

@patch("requests.get")
def test_connect_success(mock_get, hh_api):
    fake_response = Mock()
    fake_response.status_code = 200
    fake_response.json.return_value = {
        "items": [{"id": 1}, {"id": 2}]
    }
    mock_get.return_value = fake_response

    hh_api._connect("Python")

    assert len(hh_api.vacancies) > 0
    for e in hh_api.vacancies:
        assert "id" in e

@patch("requests.get")
def test_connect_bad_status_code(mock_get, hh_api):
    fake_response = Mock()
    fake_response.status_code = 404
    mock_get.return_value = fake_response

    with pytest.raises(ValueError):
        hh_api._connect("Python")

@patch("requests.get")
def test_connect_multiple_pages(mock_get, hh_api):
    fake_response_1 = Mock()
    fake_response_1.status_code = 200
    fake_response_1.json.return_value = {"items": [{"id": 1}]}
    fake_response_2 = Mock()
    fake_response_2.status_code = 200
    fake_response_2.json.return_value = {"items": []}
    mock_get.side_effect = [fake_response_1, fake_response_2]

    hh_api._connect("Python")
    assert len(hh_api.vacancies) == 1

