def test_hydra_version(hydra_admin):
    version = hydra_admin.version()
    assert version.startswith("v1.0."), version
