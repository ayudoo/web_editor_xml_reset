from odoo import http
from odoo.http import request
from odoo.addons.web_editor.controllers.main import Web_Editor


class WebEditorXmlReset(Web_Editor):
    @http.route(
        "/web_editor/get_assets_editor_resources",
        type="json",
        auth="user",
        website=True,
    )
    def get_assets_editor_resources(self, *args, **kwargs):
        result = super().get_assets_editor_resources(*args, **kwargs)

        for view_data in result.get("views", []):
            view = request.env["ir.ui.view"].browse(view_data["id"])
            view_data["customized"] = view.website_id and True or False

        return result

    @http.route(
        "/web_editor_xml_reset/reset_asset", type="json", auth="user", website=True
    )
    def web_editor_xml_reset_asset(self, res_id):
        website_id = request.website.get_current_website().id
        if not website_id:
            return False

        templates = request.env["ir.ui.view"].search(
            [("id", "=", res_id), ("website_id", "=", website_id)]
        )
        if not templates.exists():
            return False

        self._web_editor_xml_reset_recursive_unlink(templates)

        return True

    def _web_editor_xml_reset_recursive_unlink(self, templates):
        for template in templates:
            self._web_editor_xml_reset_recursive_unlink(template.inherit_children_ids)
            template.unlink()
