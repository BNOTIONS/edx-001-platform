define(["backbone", "gettext"], function (Backbone, gettext) {
    /**
     * Model for xblock validation messages as displayed in Studio.
     */
    var XBlockValidationModel = Backbone.Model.extend({
        defaults: {
            summary: {},
            messages: [],
            is_empty: true,
            xblock_id: null
        },

        WARNING : "warning",
        ERROR: "error",
        NOT_CONFIGURED: "not-configured",

        parse: function(response) {
            if (!response.is_empty) {
                var summary = "summary" in response ? response.summary : {};
                var messages = "messages" in response ? response.messages : [];
                if (!("text" in summary)) {
                    summary.text = gettext("This component has validation issues.");
                }
                if (!("type" in summary) || summary.type === null) {
                    summary.type = this.WARNING;
                    // Possible types are ERROR, WARNING, and NOT_CONFIGURED. NOT_CONFIGURED is treated as a warning.
                    for (var i = 0; i < messages.length; i++) {
                        if (messages[i].type === this.ERROR) {
                            summary.type = this.ERROR;
                            break;
                        }
                    }
                }
                response.summary = summary;
                if (response.showSummaryOnly) {
                    messages = [];
                }
                response.messages = messages;
            }

            return response;
        }
    });
    return XBlockValidationModel;
});

