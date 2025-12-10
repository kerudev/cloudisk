# from copy import deepcopy
# from unittest.mock import patch

# import pytest

# from cloudisk.fs import metadata
# from cloudisk.fs.metadata import Metadata


# @pytest.fixture
# def fake_metadata():
#     with patch.object(metadata, "uuid4") as mock_uuid:
#         mock_uuid.return_value = "123e4567-e89b-12d3-a456-426655440000"

#         instance = Metadata(
#             content_type="text/plain",
#             file_path="/some/path/test.txt",
#             file_size=1234,
#         )

#         yield instance, mock_uuid


# @pytest.fixture
# def fake_content():
#     return {"available": True, "bar": "baz"}


# def test_create_metadata(fake_content, fake_metadata):
#     with (
#         patch.object(metadata, "_init_metadata_file") as mock_init,
#         patch.object(metadata, "_load") as mock_load,
#         patch.object(metadata, "_save", wraps=metadata._save) as mock_save,
#     ):
#         instance, mock_uuid = fake_metadata
#         mock_init.return_value = True
#         mock_load.return_value = {"foo": fake_content}

#         result = create_metadata("bar", instance)

#     instance.file_name = "bar"
#     mock_save.assert_called_once_with({"foo": fake_content, "bar": dict(instance)})

#     assert result == dict(instance)


# def test_create_metadata_raises_ValueError(fake_content, fake_metadata):
#     with (
#         patch.object(metadata, "_init_metadata_file") as mock_init,
#         patch.object(metadata, "_load") as mock_load,
#     ):
#         mock_init.return_value = True
#         mock_load.return_value = {"foo": fake_content}

#         with pytest.raises(ValueError):
#             create_metadata("foo", fake_metadata)


# def test_read_metadata_is_available(fake_content):
#     with patch.object(metadata, "_load") as mock_load:
#         mock_load.return_value = {"foo": fake_content}

#         result = read_metadata("foo")

#     assert result == fake_content


# def test_read_metadata_is_not_available(fake_content):
#     fake_content["available"] = False

#     with patch.object(metadata, "_load") as mock_load:
#         mock_load.return_value = {"foo": fake_content}

#         result = read_metadata("foo")

#     assert result == {}


# def test_read_metadata_raises_KeyError():
#     with patch.object(metadata, "_load") as mock_load:
#         mock_load.return_value = {"foo": "bar"}

#         with pytest.raises(KeyError):
#             read_metadata("baz")


# def test_file_exists_returns_True():
#     assert file_exists({"available": True}) is True


# def test_file_exists_returns_False():
#     assert file_exists({"available": False}) is False


# def test_file_exists_returns_False_without_key():
#     assert file_exists({}) is False


# def test_update_metadata_no_kwargs(fake_content):
#     with patch.object(metadata, "_load") as mock_load:
#         mock_load.return_value = {"foo": fake_content}

#         result = update_metadata("foo")

#     assert result == fake_content


# def test_update_metadata_with_kwargs(fake_content):
#     data = fake_content
#     data["extra"] = {"part": 1}

#     extra = {"author": "test", "description": "..."}

#     with patch.object(metadata, "_load") as mock_load:
#         mock_load.return_value = {"foo": fake_content}

#         result = update_metadata("foo", **extra)

#     expected = deepcopy(data)
#     expected["extra"].update(extra)

#     assert result == expected


# def test_update_metadata_creates_extra(fake_content):
#     extra = {"author": "test", "description": "..."}

#     with patch.object(metadata, "_load") as mock_load:
#         mock_load.return_value = {"foo": fake_content}

#         result = update_metadata("foo", **extra)

#     expected = deepcopy(fake_content)
#     expected["extra"] = extra

#     assert result == expected


# def test_update_metadata_raises_KeyError():
#     with patch.object(metadata, "_load") as mock_load:
#         mock_load.return_value = {"foo": "bar"}

#         with pytest.raises(KeyError):
#             update_metadata("baz")


# def test_delete_metadata():
#     with (
#         patch.object(metadata, "_load") as mock_load,
#         patch.object(metadata, "_save", wraps=metadata._save) as mock_save,
#     ):
#         mock_load.return_value = {"foo": "bar", "baz": "qux"}

#         delete_metadata("baz")

#     mock_save.assert_called_once_with({"foo": "bar"})


# def test_delete_metadata_removes_all_keys():
#     with (
#         patch.object(metadata, "_load") as mock_load,
#         patch.object(metadata, "_save", wraps=metadata._save) as mock_save,
#     ):
#         mock_load.return_value = {"foo": "bar"}
#         delete_metadata("foo")

#     mock_save.assert_called_once_with({})


# def test_delete_metadata_key_doesnt_exist():
#     with (
#         patch.object(metadata, "_load") as mock_load,
#         patch.object(metadata, "_save", wraps=metadata._save) as mock_save,
#     ):
#         mock_load.return_value = {"foo": "bar"}
#         delete_metadata("baz")

#     mock_save.assert_called_once_with({"foo": "bar"})


# def test_delete_metadata_loads_no_data():
#     with (
#         patch.object(metadata, "_load") as mock_load,
#         patch.object(metadata, "_save", wraps=metadata._save) as mock_save,
#     ):
#         mock_load.return_value = {}
#         delete_metadata("foo")

#     mock_save.assert_called_once_with({})


# def test_list_file_names():
#     data = {"foo": "bar"}

#     with patch.object(metadata, "_load") as mock_load:
#         mock_load.return_value = data

#         result = list_file_names()

#     assert result == list(data)


# def test_list_file_names_empty():
#     with patch.object(metadata, "_load") as mock_load:
#         mock_load.return_value = {}

#         result = list_file_names()

#     assert result == []
