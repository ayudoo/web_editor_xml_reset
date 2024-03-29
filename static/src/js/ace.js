odoo.define('web_editor_xml_reset.ace', function(require) {
  'use strict';

  const WebsiteAceEditor = require(
    '@website/components/ace_editor/ace_editor'
  ).WebsiteAceEditor;

  WebsiteAceEditor.include({
    _resetResource: function (resID, type) {
      var _super = this._super.bind(this);

      if (this.currentType === 'xml') {
        var resource = this.views[resID];
        return this._rpc({
          route: '/web_editor_xml_reset/reset_asset',
          params: {
            res_id: resID,
          },
        }).then(function() {
          window.location.hash = '';
        });
      } else {
        return _super(...arguments);
      }
    },
    _displayResource: function (resID, type) {
      this._super(...arguments);
      if (this.currentType === 'xml' && this.views) {
        var template = this.views[resID];
        if (template && template.customized && this.$resetButton.hasClass('d-none')) {
          this.$resetButton.removeClass('d-none');
        }
      }
    }
  });

  return WebsiteAceEditor;
});
