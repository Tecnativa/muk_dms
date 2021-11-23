# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


def convert_to_muk_security_groups(env):
    openupgrade.logged_query(
        env.cr,
        """
        INSERT INTO muk_security_groups (
            id,
            parent_left,
            parent_right,
            name,
            parent_group,
            perm_read,
            perm_create,
            perm_write,
            perm_unlink,
            create_uid,
            create_date,
            write_uid,
            write_date
        ) SELECT mdag.id,
            mdag.parent_left,
            mdag.parent_right,
            mdag.name,
            mdag.parent_group,
            mdag.perm_read,
            mdag.perm_create,
            mdag.perm_write,
            mdag.perm_unlink,
            mdag.create_uid,
            mdag.create_date,
            mdag.write_uid,
            mdag.write_date
        FROM muk_dms_access_groups AS mdag
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        INSERT INTO muk_security_groups_groups_rel (
            gid, rid
        ) SELECT mdggr.gid,
            mdggr.rid
        FROM muk_dms_groups_groups_rel AS mdggr
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        INSERT INTO muk_security_groups_users_rel (
            gid, uid
        ) SELECT mdgaur.gid,
            mdgaur.uid
        FROM muk_dms_groups_add_users_rel AS mdgaur
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        INSERT INTO muk_security_groups_explicit_users_rel (
            gid, uid
        ) SELECT mdgaur.gid,
            mdgaur.uid
        FROM muk_dms_groups_add_users_rel AS mdgaur
        """,
    )


@openupgrade.migrate()
def migrate(env, version):
    if openupgrade.table_exists(env.cr, "muk_dms_access_groups"):
        convert_to_muk_security_groups(env)
