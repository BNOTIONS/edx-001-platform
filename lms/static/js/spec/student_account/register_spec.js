define([
    'jquery',
    'js/common_helpers/template_helpers',
    'js/common_helpers/ajax_helpers',
    'js/student_account/models/RegisterModel',
    'js/student_account/views/RegisterView'
], function($, TemplateHelpers, AjaxHelpers, RegisterModel, RegisterView) {
        describe('edx.student.account.RegisterView', function() {
            'use strict';

            var view = null,
                requests = null,
                PLATFORM_NAME = 'edX',
                USER_DATA = {
                    email: 'xsy@edx.org',
                    name: 'Xsy M. Education',
                    username: 'Xsy',
                    password: 'xsyisawesome',
                    level_of_education: 'p',
                    gender: 'm',
                    year_of_birth: 2014,
                    mailing_address: '141 Portland'
                    goals: 'To boldly learn what no letter of the alphabet has learned before'
                    terms_of_service: true
                },
                THIRD_PARTY_AUTH = {
                    currentProvider: null,
                    providers: [{
                        name: 'Google',
                        iconClass: 'icon-google-plus',
                        loginUrl: '/auth/login/google-oauth2/?auth_entry=account_login',
                        registerUrl: '/auth/login/google-oauth2/?auth_entry=account_register'
                    }]
                },
                FORM_DESCRIPTION = {
                    method: 'post',
                    submit_url: '/user_api/v1/account/registration/',
                    fields: [
                        {
                            name: 'email',
                            label: 'Email',
                            defaultValue: '',
                            type: 'email',
                            required: true,
                            placeholder: 'place@holder.org',
                            instructions: 'Enter your email.',
                            restrictions: {}
                        },
                        {
                            name: 'name',
                            label: 'Full Name',
                            defaultValue: '',
                            type: 'text',
                            required: true,
                            instructions: 'Enter your username.',
                            restrictions: {}
                        },
                        {
                            name: 'username',
                            label: 'Username',
                            defaultValue: '',
                            type: 'text',
                            required: true,
                            instructions: 'Enter your username.',
                            restrictions: {}
                        },
                        {
                            name: 'password',
                            label: 'Password',
                            defaultValue: '',
                            type: 'password',
                            required: true,
                            instructions: 'Enter your password.',
                            restrictions: {}
                        },
                        {
                            name: 'level_of_education',
                            label: 'Highest Level of Education Completed',
                            defaultValue: '',
                            type: 'select',
                            options: [
                                {value: "", name: "--"},
                                {value: "p", name: "Doctorate"},
                                {value: "m", name: "Master's or professional degree"},
                                {value: "b", name: "Bachelor's degree"},
                            ],
                            required: false,
                            type: 'select',
                            instructions: 'Select your education level.',
                            restrictions: {}
                        },
                        {
                            name: 'gender',
                            label: 'Gender',
                            defaultValue: '',
                            options: [
                                {value: "", name: "--"},
                                {value: "m", name: "Male"},
                                {value: "f", name: "Female"},
                                {value: "o", name: "Other"},
                            ],
                            required: false,
                            instructions: 'Select your gender.',
                            restrictions: {}
                        },
                        {
                            name: 'year_of_birth',
                            label: 'Year of Birth',
                            defaultValue: '',
                            type: 'select',
                            options: [
                                {value: "", name: "--"},
                                {value: 1900, name: "1900"},
                                {value: 1950, name: "1950"},
                                {value: 2014, name: "2014"},
                            ],
                            required: false,
                            instructions: 'Select your year of birth.',
                            restrictions: {}
                        },
                        {
                            name: 'mailing_address',
                            label: 'Mailing Address',
                            defaultValue: '',
                            type: 'textarea',
                            required: false,
                            instructions: 'Enter your mailing address.',
                            restrictions: {}
                        },
                        {
                            name: 'goals',
                            label: 'Goals',
                            defaultValue: '',
                            type: 'textarea',
                            required: false,
                            instructions: "If you'd like, tell us why you're interested in edX.",
                            restrictions: {}
                        },
                        {
                            name: 'terms_of_service',
                            label: 'Terms of Service',
                            defaultValue: '',
                            type: 'checkbox',
                            required: true,
                            instructions: "Agree to the terms of service.",
                            restrictions: {}
                        },
                    ]
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

            var submitForm = function(validationSuccess) {
                // Simulate manual entry of registration form data
                $('#register-email').val(USER_DATA.email);
                $('#register-name').val(USER_DATA.name);
                $('#register-username').val(USER_DATA.username);
                $('#register-password').val(USER_DATA.password);
                $('#register-level_of_education').val(USER_DATA.level_of_education);
                $('#register-gender').val(USER_DATA.gender);
                $('#register-year_of_birth').val(USER_DATA.year_of_birth);
                $('#register-mailing_address').val(USER_DATA.mailing_address);
                $('#register-goals').val(USER_DATA.goals);
                $('#register-terms_of_service').val(USER_DATA.terms_of_service);

                // Create a fake click event
                var clickEvent = $.Event('click');

                // If validationSuccess isn't passed, we avoid
                // spying on `view.validate` twice
                if (typeof validationSuccess !== 'undefined') {
                    // Force validation to return as expected
                    spyOn(view, 'validate').andReturn({
                        isValid: validationSuccess,
                        message: 'We\'re all good.'
                    });
                }

                // Submit the email address
                view.submitForm(clickEvent);
            };

            beforeEach(function() {
                setFixtures('<div id="register-form"></div>');
                TemplateHelpers.installTemplate('templates/student_account/register');
                TemplateHelpers.installTemplate('templates/student_account/form_field');
            });

            it('registers a new user', function() {
                createRegisterView(this);

                submitForm(true);

                // Verify that the client contacts the server with the expected data
                AjaxHelpers.expectRequest(
                    requests, 'POST', FORM_DESCRIPTION.submit_url, $.param(
                        $.extend({url: FORM_DESCRIPTION.submit_url}, USER_DATA)
                    )
                );
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
