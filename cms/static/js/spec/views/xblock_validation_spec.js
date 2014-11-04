define(['jquery', 'js/models/xblock_validation', 'js/views/xblock_validation', 'js/common_helpers/template_helpers'],
    function($, XBlockValidationModel, XBlockValidationView, TemplateHelpers) {

        beforeEach(function () {
           TemplateHelpers.installTemplate('xblock-validation-messages');
           appendSetFixtures(
               '<div class="wrapper-xblock-message xblock-validation-messages" data-locator="dummy-locator"/>'
           );
        });


        describe('XBlockValidationView helper methods', function() {
            var model, view;

            beforeEach(function () {
                model = new XBlockValidationModel({parse: true});
                view = new XBlockValidationView({model: model, ele: $(".xblock-validation-messages")});
                view.render();
            });

            it('has a getIcon method', function() {
                expect(view.getIcon(model, model.WARNING)).toBe('icon-warning-sign');
                expect(view.getIcon(model, model.NOT_CONFIGURED)).toBe('icon-warning-sign');
                expect(view.getIcon(model, model.ERROR)).toBe('icon-exclamation-sign');
                expect(view.getIcon(model, "unknown")).toBeNull();
            });

            it('has a getDisplayName method', function() {
                expect(view.getDisplayName(model, model.WARNING)).toBe("Warning");
                expect(view.getDisplayName(model, model.NOT_CONFIGURED)).toBe("Warning");
                expect(view.getDisplayName(model, model.ERROR)).toBe("Error");
                expect(view.getDisplayName(model, "unknown")).toBeNull();
            });

            it('can add additional classes', function() {
                var noContainerContent = "no-container-content", notConfiguredModel, nonRootView, rootView;

                expect(view.getAdditionalClasses()).toBe("");
                expect(view.$('.validation')).not.toHaveClass(noContainerContent);

                notConfiguredModel = new XBlockValidationModel({
                     "is_empty": false, "summary": {"text": "Not configured", "type": model.NOT_CONFIGURED},
                     "xblock_id": "id"
                    },
                    {parse: true}
                );

                nonRootView = new XBlockValidationView(
                    {model: notConfiguredModel, ele: $(".xblock-validation-messages")}
                );
                nonRootView.render();
                expect(nonRootView.getAdditionalClasses()).toBe("");
                expect(view.$('.validation')).not.toHaveClass(noContainerContent);

                rootView = new XBlockValidationView(
                    {model: notConfiguredModel, ele: $(".xblock-validation-messages"), is_root: true}
                );
                rootView.render();
                expect(rootView.getAdditionalClasses()).toBe(noContainerContent);
                expect(rootView.$('.validation')).toHaveClass(noContainerContent);
            });

        });

        describe('XBlockValidationView rendering', function() {
            var model, view;

            beforeEach(function () {
                model = new XBlockValidationModel({
                     "is_empty": false,
                     "summary": {
                         "text": "Summary message", "type": "error",
                         "action_label": "Summary Action", "action_class": "edit-button"
                     },
                     "messages": [
                         {
                             "text": "First message", "type": "warning",
                             "action_label": "First Message Action", "action_runtime_event": "fix-up"
                         },
                         {"text": "Second message", "type": "error"}
                     ],
                     "xblock_id": "id"
                    });
                view = new XBlockValidationView({model: model, ele: $(".xblock-validation-messages")});
                view.render();
            });

            it('renders summary and detailed messages types', function() {
                var details;

                expect(view.$('.xblock-message')).toHaveClass("has-errors");
                details = view.$('.xblock-message-item');
                expect(details.length).toBe(2);
                expect(details[0]).toHaveClass("warning");
                expect(details[1]).toHaveClass("error");
            });

            it('renders summary and detailed messages text', function() {
                var details;

                expect(view.$('.xblock-message').text()).toContain("Summary message");

                details = view.$('.xblock-message-item');
                expect(details.length).toBe(2);
                expect($(details[0]).text()).toContain("Warning");
                expect($(details[0]).text()).toContain("First message");
                expect($(details[1]).text()).toContain("Error");
                expect($(details[1]).text()).toContain("Second message");
            });

            it('renders action info', function() {
                var detailedAction;

                expect(view.$('a.edit-button .action-button-text').text()).toContain("Summary Action");

                detailedAction = view.$('a.notification-action-button .action-button-text');
                expect(detailedAction.text()).toContain("First Message Action");
                expect(detailedAction.data("notification-action").toBe("fix-up");
            });
        });
    }
);
