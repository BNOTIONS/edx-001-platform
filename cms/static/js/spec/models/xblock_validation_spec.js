define(['js/models/xblock_validation'],
    function(XBlockValidationModel) {
        var verifyModel;

        verifyModel = function(model, expected_is_empty, expected_summary, expected_messages, expected_xblock_id) {
            expect(model.get("is_empty")).toBe(expected_is_empty);
            expect(model.get("summary")).toEqual(expected_summary);
            expect(model.get("messages")).toEqual(expected_messages);
            expect(model.get("xblock_id")).toBe(expected_xblock_id);

        };

        describe('XBlockValidationModel', function() {
            it('handles is_empty variable', function() {
                verifyModel(new XBlockValidationModel({parse: true}), true, {}, [], null);
                verifyModel(new XBlockValidationModel({"is_empty": true}, {parse: true}), true, {}, [], null);

                // It is assumed that the "is_empty" state on the JSON object passed in is correct
                // (no attempt is made to correct other variables based on "is_empty"==true).
                verifyModel(
                    new XBlockValidationModel(
                        {"is_empty": true, "messages": [{"text": "Bad JSON case"}], "xblock_id": "id"},
                        {parse: true}
                    ),
                    true,
                    {},
                    [{"text": "Bad JSON case"}], "id"
                );
            });

            it('creates a summary if not defined', function() {
                verifyModel(
                    new XBlockValidationModel({
                        "is_empty": false,
                        "xblock_id": "id"
                    }, {parse: true}),
                    false,
                    {"text": "This component has validation issues.", "type": "warning"},
                    [],
                    "id"
                );
                verifyModel(
                    new XBlockValidationModel({
                        "is_empty": false,
                        "messages": [{"text": "one", "type": "not-configured"}, {"text": "two", "type": "warning"}],
                        "xblock_id": "id"
                    }, {parse: true}),
                    false,
                    {"text": "This component has validation issues.", "type": "warning"},
                    [{"text": "one", "type": "not-configured"}, {"text": "two", "type": "warning"}],
                    "id"
                );
                verifyModel(
                    new XBlockValidationModel({
                        "is_empty": false,
                        "messages": [{"text": "one", "type": "warning"}, {"text": "two", "type": "error"}],
                        "xblock_id": "id"
                    }, {parse: true}),
                    false,
                    {"text": "This component has validation issues.", "type": "error"},
                    [{"text": "one", "type": "warning"}, {"text": "two", "type": "error"}],
                    "id"
                );
            });

            it('respects summary properties that are defined', function() {
                verifyModel(
                    new XBlockValidationModel({
                        "is_empty": false,
                        "xblock_id": "id",
                        "summary": {"text": "my summary", "type": "custom type"}
                    }, {parse: true}),
                    false,
                    {"text": "my summary", "type": "custom type"},
                    [],
                    "id"
                );
                verifyModel(
                    new XBlockValidationModel({
                        "is_empty": false,
                        "xblock_id": "id",
                        "summary": {"text": "my summary"}
                    }, {parse: true}),
                    false,
                    {"text": "my summary", "type": "warning"},
                    [],
                    "id"
                );
                verifyModel(
                    new XBlockValidationModel({
                        "is_empty": false,
                        "summary": {"text": "my summary", "type": "custom type"},
                        "messages": [{"text": "one", "type": "not-configured"}, {"text": "two", "type": "warning"}],
                        "xblock_id": "id"
                    }, {parse: true}),
                    false,
                    {"text": "my summary", "type": "custom type"},
                    [{"text": "one", "type": "not-configured"}, {"text": "two", "type": "warning"}],
                    "id"
                );
                verifyModel(
                    new XBlockValidationModel({
                        "is_empty": false,
                        "summary": {"text": "my summary"},
                        "messages": [{"text": "one", "type": "warning"}, {"text": "two", "type": "error"}],
                        "xblock_id": "id"
                    }, {parse: true}),
                    false,
                    {"text": "my summary", "type": "error"},
                    [{"text": "one", "type": "warning"}, {"text": "two", "type": "error"}],
                    "id"
                );
            });

            it('clears messages if showSummaryOnly is true', function() {
                verifyModel(
                    new XBlockValidationModel({
                        "is_empty": false,
                        "xblock_id": "id",
                        "summary": {"text": "my summary"},
                        "messages": [{"text": "one", "type": "warning"}, {"text": "two", "type": "error"}],
                        "showSummaryOnly": true
                    }, {parse: true}),
                    false,
                    {"text": "my summary", "type": "error"},
                    [],
                    "id"
                );

                verifyModel(
                    new XBlockValidationModel({
                        "is_empty": false,
                        "xblock_id": "id",
                        "summary": {"text": "my summary"},
                        "messages": [{"text": "one", "type": "warning"}, {"text": "two", "type": "error"}],
                        "showSummaryOnly": false
                    }, {parse: true}),
                    false,
                    {"text": "my summary", "type": "error"},
                    [{"text": "one", "type": "warning"}, {"text": "two", "type": "error"}],
                    "id"
                );
            });
        });
    }
);
