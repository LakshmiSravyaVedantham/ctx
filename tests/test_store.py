import pytest
from pathlib import Path
from ctx.store import PackStore, Pack


def test_save_global_pack(tmp_path):
    store = PackStore(global_dir=tmp_path / "packs")
    pack = Pack(name="myproject", content="# myproject\n\nPython API project.")
    store.save(pack, scope="global")
    assert (tmp_path / "packs" / "myproject.md").exists()


def test_save_local_pack(tmp_path):
    store = PackStore(global_dir=tmp_path / "packs")
    pack = Pack(name="myproject", content="# myproject\n\nPython API project.")
    store.save(pack, scope="local", local_dir=tmp_path / ".ctx")
    assert (tmp_path / ".ctx" / "myproject.md").exists()


def test_load_global_pack(tmp_path):
    store = PackStore(global_dir=tmp_path / "packs")
    pack = Pack(name="myproject", content="# myproject\n\nPython API project.")
    store.save(pack, scope="global")
    loaded = store.load("myproject", local_dir=tmp_path / ".ctx")
    assert loaded is not None
    assert loaded.content == "# myproject\n\nPython API project."


def test_load_local_takes_priority(tmp_path):
    store = PackStore(global_dir=tmp_path / "packs")
    store.save(Pack(name="myproject", content="global content"), scope="global")
    store.save(Pack(name="myproject", content="local content"), scope="local", local_dir=tmp_path / ".ctx")
    loaded = store.load("myproject", local_dir=tmp_path / ".ctx")
    assert loaded is not None
    assert loaded.content == "local content"


def test_list_packs(tmp_path):
    store = PackStore(global_dir=tmp_path / "packs")
    store.save(Pack(name="proj1", content="a"), scope="global")
    store.save(Pack(name="proj2", content="b"), scope="global")
    packs = store.list_all(local_dir=tmp_path / ".ctx")
    names = [p.name for p in packs]
    assert "proj1" in names
    assert "proj2" in names


def test_delete_pack(tmp_path):
    store = PackStore(global_dir=tmp_path / "packs")
    store.save(Pack(name="myproject", content="x"), scope="global")
    store.delete("myproject", local_dir=tmp_path / ".ctx")
    assert store.load("myproject", local_dir=tmp_path / ".ctx") is None


def test_load_missing_returns_none(tmp_path):
    store = PackStore(global_dir=tmp_path / "packs")
    result = store.load("nonexistent", local_dir=tmp_path / ".ctx")
    assert result is None
