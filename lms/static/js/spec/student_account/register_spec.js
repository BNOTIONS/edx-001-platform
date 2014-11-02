define([
    'jquery',
    'underscore',
    'underscore.string',
    'js/common_helpers/template_helpers',
    'js/common_helpers/ajax_helpers',
    'js/student_account/models/RegisterModel',
    'js/student_account/views/RegisterView'
], function($, _, _s, TemplateHelpers, AjaxHelpers, RegisterModel, RegisterView) {
        describe('edx.student.account.RegisterView', function() {
            'use strict';

            var view = null,
                requests = null,
                PLATFORM_NAME = 'edX',
                THIRD_PARTY_AUTH = {
                    currentProvider: null,
                    providers: [{
                        name: 'Google',
                        iconClass: 'icon-google-plus',
                        loginUrl: '/auth/login/google-oauth2/?auth_entry=account_login',
                        registerUrl: '/auth/login/google-oauth2/?auth_entry=account_register'
                    }]
                    // providers: []
                },
                FORM_DESCRIPTION = {
                    method: 'post',
                    submit_url: '/user_api/v1/account/registration/',
                    fields: [{
                        name: 'email',
                        label: 'Email',
                        defaultValue: '',
                        type: 'text',
                        required: true,
                        placeholder: 'place@holder.org',
                        instructions: 'Enter your email.',
                        restrictions: {}
                    }]
                };

            var model = new RegisterModel({
                url: FORM_DESCRIPTION.submit_url
            });

            var createRegisterView = function(that) {
                // Initialize the password reset view
                view = new RegisterView({
                    fields: FORM_DESCRIPTION.fields,
                    model: model,
                    thirdPartyAuth: THIRD_PARTY_AUTH,
                    platformName: PLATFORM_NAME
                });

                // Spy on AJAX requests
                requests = AjaxHelpers.requests(that);
            };

            beforeEach(function() {
                setFixtures('<div></div>');
                TemplateHelpers.installTemplate('templates/student_account/register');
                TemplateHelpers.installTemplate('templates/student_account/form_field');
            });

            it('registers a new user', function() {
                createRegisterView(this);
            });

            it('displays third party auth registration buttons', function() {
                // TODO
            });

            it('validates form fields', function() {
                // TODO
            });

            it('displays registration errors', function() {
                // TODO
            });

            it('displays an error if the form definition could not be loaded', function() {
                // TODO
            });

            it('displays an error if the server could not be contacted while registering', function() {
                // TODO
            });
        });
    }
);
