# Copyright 2026 Innovyou
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


def migrate(cr, version):
    """The customer signature of fieldservice_digitized_signature (16.0) is
    now provided by fieldservice itself, with the same field names: merge the
    module so the signatures (stored as attachments) and the signer data are
    kept."""
    if not version or not openupgrade.is_module_installed(
        cr, "fieldservice_digitized_signature"
    ):
        return
    # The old views target the 16.0 form and duplicate the core fields
    openupgrade.logged_query(
        cr,
        """
        DELETE FROM ir_ui_view
        WHERE id IN (
            SELECT res_id
            FROM ir_model_data
            WHERE module = 'fieldservice_digitized_signature'
                AND model = 'ir.ui.view'
        )
        """,
    )
    openupgrade.logged_query(
        cr,
        """
        DELETE FROM ir_model_data
        WHERE module = 'fieldservice_digitized_signature'
            AND model = 'ir.ui.view'
        """,
    )
    openupgrade.update_module_names(
        cr,
        [("fieldservice_digitized_signature", "fieldservice")],
        merge_modules=True,
    )
