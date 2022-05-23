odoo.define("voip.PhoneCallActivitiesTab", function (require) {
  "use strict";

  const PhoneCallTab = require("voip.PhoneCallTab");

  const PhoneCallActivitiesTab = PhoneCallTab.extend({
    /**
     * @override
     */
    init() {
      this._super(...arguments);
      this.isAutoCallMode = false;
    },

    // --------------------------------------------------------------------------
    // Public
    // --------------------------------------------------------------------------

    /**
     * When the user clicks on the call button when on activity tab, enter autocall mode
     *
     * @override
     * @returns {Promise}
     */
    callFromTab() {
      return this._autoCall();
    },
    /**
     * Function called when a phonenumber is clicked in the activity widget.
     * If the phonecall with the activityId given in the parameter
     * can't be found in the displayed list, we make a rpc to get the
     * related phonecall.
     *
     * @param {Object} param0
     * @param {integer} param0.activityId
     * @returns {Promise}
     */
    async callFromActivityWidget({activityId}) {
      this.isAutoCallMode = false;
      const currentPhoneCall = this._getCurrentPhoneCall();
      this._currentPhoneCallId = currentPhoneCall && currentPhoneCall.id;
      if (this._currentPhoneCallId) {
        return this._selectPhoneCall(this._currentPhoneCallId);
      }
      const phoneCallData = await this._rpc({
        model: "voip.phonecall",
        method: "get_from_activity_id",
        args: [activityId],
      });
      const phoneCallId = await this._displayInQueue(phoneCallData);
      this._currentPhoneCallId = phoneCallId;
      return this._selectPhoneCall(phoneCallId);
    },
    /**
     * Escape string in order to use it in a regex
     * source: https://stackoverflow.com/questions/3446170/escape-string-for-use-in-javascript-regex
     *
     * @param {String} string
     * @returns {String}
     */
    escapeRegExp(string) {
      // $& means the whole matched string
      return string.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    },
    /**
     * @override
     * @returns {Promise}
     */
    async hangupPhonecall() {
      await this._super(...arguments);
      if (this.isAutoCallMode) {
        return this._autoCall();
      }
    },
    /**
     * @override
     * @returns {Promise}
     */
    async initPhoneCall() {
      const _super = this._super.bind(this, ...arguments); // Limitation of class.js
      if (!this._currentPhoneCallId) {
        return;
      }
      const currentPhoneCall = this._getCurrentPhoneCall();
      currentPhoneCall.callTries += 1;
      await this._rpc({
        model: "voip.phonecall",
        method: "init_call",
        args: [this._currentPhoneCallId],
      });
      _super();
    },
    /**
     * @override
     * @param {String} search
     * @returns {Promise}
     */
    async searchPhoneCall(search) {
      // Regular expression used to do a case insensitive search
      const escSearch = this.escapeRegExp(search);
      const expr = new RegExp(escSearch, "i");
      // For each phonecall, check if the search is in phonecall name or the partner name
      for (const phoneCall of this._phoneCalls) {
        const flagPartner =
          phoneCall.partnerName && phoneCall.partnerName.search(expr) > -1;
        let flagName = false;
        if (phoneCall.name) {
          flagName = phoneCall.name.search(expr) > -1;
        }
        phoneCall.$el.toggle(flagPartner || flagName);
      }
    },

    // --------------------------------------------------------------------------
    // Private
    // --------------------------------------------------------------------------

    /**
     * Select the next call to do
     *
     * @private
     * @returns {Promise}
     */
    async _autoCall() {
      this.isAutoCallMode = true;
      const todoPhoneCalls = this._phoneCalls.filter(
        (phoneCall) => phoneCall.state !== "done"
      );
      if (todoPhoneCalls.length > 0) {
        const nextCall = _.min(todoPhoneCalls, (phoneCall) => phoneCall.callTries);
        return this._selectPhoneCall(nextCall.id);
      }
        this.isAutoCallMode = false;
        if (this._selectedPhoneCallId) {
          return this._closePhoneDetails();
        }

    },
    /**
     * @private
     * @override
     */
    async _closePhoneDetails() {
      this.isAutoCallMode = false;
      return this._super(...arguments);
    },

    // --------------------------------------------------------------------------
    // Handlers
    // --------------------------------------------------------------------------

    /**
     * @private
     * @override
     * @returns {Promise}
     */
    async _onCancelActivity() {
      if (this.isAutoCallMode) {
        await this.refreshPhonecallsStatus();
        return this._autoCall();
      }
        return this._closePhoneDetails();

    },
    /**
     * @private
     * @override
     * @returns {Promise}
     */
    async _onMarkActivityDone() {
      if (this.isAutoCallMode) {
        await this.refreshPhonecallsStatus();
        return this._autoCall();
      }
    },
  });

  return PhoneCallActivitiesTab;
});
