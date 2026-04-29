import json
import pytest
import tracker
from tracker import load_price_history, save_price_history


@pytest.fixture(autouse=True)
def patch_history_file(tmp_path, monkeypatch):
    temp_file = tmp_path / "last_price.json"
    monkeypatch.setattr(tracker, "PRICE_HISTORY_FILE", str(temp_file))
    return temp_file


def test_load_returns_empty_dict_when_file_missing():
    result = load_price_history()
    assert result == {}


def test_load_returns_data_when_file_exists(patch_history_file):
    data = {"Pampers": 120.0, "Huggies": 45.5}
    patch_history_file.write_text(json.dumps(data))

    result = load_price_history()
    assert result == data


def test_save_writes_correct_json(patch_history_file):
    data = {"Pampers": 120.0}
    save_price_history(data)

    written = json.loads(patch_history_file.read_text())
    assert written == data


def test_save_and_load_round_trip():
    data = {"Pampers": 120.0, "Huggies": 45.5}
    save_price_history(data)

    result = load_price_history()
    assert result == data
