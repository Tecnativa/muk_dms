# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade  # pylint: disable=W7936

_model_renames = [
    ("muk_dms.settings", "muk_dms.storage"),
]
_table_renames = [
    ("muk_dms_settings", "muk_dms_storage"),
]
_field_renames = [
    ("muk_dms.directory", "muk_dms_directory", "settings", "storage"),
    ("muk_dms.file", "muk_dms_file", "settings", "storage"),
]


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_models(env.cr, _model_renames)
    for table in _table_renames:
        if openupgrade.table_exists(env.cr, table[0]):
            openupgrade.rename_tables(env.cr, [table])
    for field in _field_renames:
        if openupgrade.table_exists(env.cr, field[1]) and openupgrade.column_exists(
            env.cr, field[1], field[2]
        ):
            openupgrade.rename_fields(env, [field])
