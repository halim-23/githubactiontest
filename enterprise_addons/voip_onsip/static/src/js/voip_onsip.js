odoo.define("voip.onsip", function (require) {
  "use strict";

  const UserAgent = require("voip.UserAgent");

  UserAgent.include({
    // --------------------------------------------------------------------------
    // Private
    // --------------------------------------------------------------------------

    /**
     * @override
     */
    _getUaConfig(result) {
      const config = this._super(...arguments);
      config.authorizationUser = result.onsip_auth_user;
      return config;
    },
  });
});
