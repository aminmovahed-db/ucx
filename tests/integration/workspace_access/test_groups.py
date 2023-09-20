from databricks.sdk import WorkspaceClient

from databricks.labs.ucx.config import GroupsConfig
from databricks.labs.ucx.workspace_access.groups import GroupManager


def test_prepare_environment(ws, make_ucx_group):
    ws_group, acc_group = make_ucx_group()

    group_manager = GroupManager(ws, GroupsConfig(selected=[ws_group.display_name]))
    group_manager.prepare_groups_in_environment()

    group_migration_state = group_manager.migration_groups_provider
    for _info in group_migration_state.groups:
        _ws = ws.groups.get(id=_info.workspace.id)
        _backup = ws.groups.get(id=_info.backup.id)
        _ws_members = sorted([m.value for m in _ws.members])
        _backup_members = sorted([m.value for m in _backup.members])
        assert _ws_members == _backup_members


def test_group_listing(ws: WorkspaceClient, make_ucx_group):
    ws_group, acc_group = make_ucx_group()
    manager = GroupManager(ws, GroupsConfig(selected=[ws_group.display_name]))
    assert ws_group.display_name in [g.display_name for g in manager._workspace_groups]
    assert acc_group.display_name in [g.display_name for g in manager._account_groups]


def test_id_validity(ws: WorkspaceClient, make_ucx_group):
    ws_group, acc_group = make_ucx_group()
    manager = GroupManager(ws, GroupsConfig(selected=[ws_group.display_name]))
    assert ws_group.id == manager._get_group(ws_group.display_name, "workspace").id
    assert acc_group.id == manager._get_group(acc_group.display_name, "account").id