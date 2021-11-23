# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


def convert_to_muk_security_access_groups(env):
    openupgrade.logged_query(
        env.cr,
        """
        INSERT INTO muk_security_access_groups (
            id,
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
        ) SELECT msg.id,
            msg.name,
            msg.parent_group,
            msg.perm_read,
            msg.perm_create,
            msg.perm_write,
            msg.perm_unlink,
            msg.create_uid,
            msg.create_date,
            msg.write_uid,
            msg.write_date
        FROM muk_security_groups AS msg
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        INSERT INTO muk_security_access_groups_groups_rel (
            gid, rid
        ) SELECT msggr.gid,
            msggr.rid
        FROM muk_security_groups_groups_rel AS msggr
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """
        INSERT INTO muk_security_access_groups_users_rel (
            gid, uid
        ) SELECT msgur.gid,
            msgur.uid
        FROM muk_security_groups_users_rel AS msgur
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """CREATE TABLE muk_dms_directory_groups_rel (aid integer, gid integer)"""
    )
    openupgrade.logged_query(
        env.cr,
        """
        INSERT INTO muk_dms_directory_groups_rel (
            aid, gid
        ) SELECT mgdr.aid,
            mgdr.gid
        FROM muk_groups_directory_rel AS mgdr
        """,
    )
    openupgrade.logged_query(
        env.cr,
        """CREATE TABLE muk_dms_directory_complete_groups_rel (aid integer, gid integer)"""
    )
    openupgrade.logged_query(
        env.cr,
        """
        INSERT INTO muk_dms_directory_complete_groups_rel (
            aid, gid
        ) SELECT mgcdr.aid,
            mgcdr.gid
        FROM muk_groups_complete_directory_rel AS mgcdr
        """,
    )


@openupgrade.migrate()
def migrate(env, version):
    if openupgrade.table_exists(env.cr, "muk_security_groups"):
        convert_to_muk_security_access_groups(env)
