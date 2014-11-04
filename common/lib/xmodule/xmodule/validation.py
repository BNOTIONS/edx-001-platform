"""
Extension of XBlock Validation class to include information for presentation in Studio.
"""
from xblock.validation import Validation, ValidationMessageTypes


class StudioValidationMessageTypes (ValidationMessageTypes):
    """
    Supported validation message types.
    """

    # A special message type indicating that the xblock is not yet configured. This message may be rendered
    # in a different way within Studio.
    NOT_CONFIGURED = "not-configured"


class StudioValidation(Validation):
    """
    Extends `Validation` to add Studio-specific information.
    """

    MESSAGE_TYPES = StudioValidationMessageTypes()

    @classmethod
    def copy(cls, validation):
        """
        Copies the `Validation` object to a `StudioValidation` object. This is a shallow copy.
        """
        if not isinstance(validation, Validation):
            raise TypeError("Copy must be called with a Validation instance")
        studio_validation = cls(validation.xblock_id)
        studio_validation.messages = validation.messages
        return studio_validation

    @classmethod
    def create_message(
            cls, message_type, message_text, action_label=None, action_class=None, action_runtime_event=None
    ):  # pylint: disable=arguments-differ
        """
        Create a new message to add to the messages stored in a `StudioValidation` instance.

        :param message_type: the type associated with this message
        :type message_type: one of the types declared in subclass of `ValidationMessageTypes`
        :param message_text: the textual message
        :type message_text: unicode string
        :param action_label: text to show on a "fix-up" action (optional). If present, either `action_class`
            or `action_runtime_event` should be specified.
        :type action_label: unicode string
        :param action_class: a class to link to the "fix-up" action (optional). A click handler must be added
            for this class, unless it is "edit-button", "duplicate-button", or "delete-button" (which are all
            handled in general for xblock instances.
        :type action_class: string
        :param action_runtime_event: an event name to be triggered on the xblock client-side runtime when
            the "fix-up" action is clicked (optional).
        :type action_runtime_event: string
        """
        message = super(StudioValidation, cls).create_message(message_type, message_text)
        if action_label:
            if not isinstance(action_label, unicode):
                raise TypeError("Action label must be unicode.")
            message["action_label"] = action_label
        if action_class:
            if not isinstance(action_class, basestring):
                raise TypeError("Action class must be a string.")
            message["action_class"] = action_class
        if action_runtime_event:
            if not isinstance(action_runtime_event, basestring):
                raise TypeError("Action runtime event must be a string.")
            message["action_runtime_event"] = action_runtime_event
        return message

    def __init__(self, xblock_id):
        """
        Create a `StudioValidation` instance.

        :param xblock_id: the ID of the xblock for which this object was created
        :type xblock_id: an identification object that must support conversion to unicode
        """
        super(StudioValidation, self).__init__(xblock_id)
        self.summary = None

    def add(
            self, message_type, message_text,
            action_label=None, action_class=None, action_runtime_event=None
    ):  # pylint: disable=arguments-differ
        """
        Add a new validation message to this instance.

        :param message_type: the type associated with this message
        :type message_type: one of the types declared in subclass of `ValidationMessageTypes`
        :param message_text: the textual message
        :type message_text: unicode string
        :param action_label: text to show on a "fix-up" action (optional). If present, either `action_class`
            or `action_runtime_event` should be specified.
        :type action_label: unicode string
        :param action_class: a class to link to the "fix-up" action (optional). A click handler must be added
            for this class, unless it is "edit-button", "duplicate-button", or "delete-button" (which are all
            handled in general for xblock instances.
        :type action_class: string
        :param action_runtime_event: an event name to be triggered on the xblock client-side runtime when
            the "fix-up" action is clicked (optional).
        :type action_runtime_event: string
        """
        self.messages.append(
            self.create_message(message_type, message_text, action_label, action_class, action_runtime_event)
        )

    def set_summary(self, message_type, message_text, action_label=None, action_class=None, action_runtime_event=None):
        """
        Sets a summary message on this instance. The summary is optional.

        :param message_type: the type associated with this message
        :type message_type: one of the types declared in subclass of `ValidationMessageTypes`
        :param message_text: the textual message
        :type message_text: unicode string
        :param action_label: text to show on a "fix-up" action (optional). If present, either `action_class`
            or `action_runtime_event` should be specified.
        :type action_label: unicode string
        :param action_class: a class to link to the "fix-up" action (optional). A click handler must be added
            for this class, unless it is "edit-button", "duplicate-button", or "delete-button" (which are all
            handled in general for xblock instances.
        :type action_class: string
        :param action_runtime_event: an event name to be triggered on the xblock client-side runtime when
            the "fix-up" action is clicked (optional).
        :type action_runtime_event: string
        """
        self.summary = self.create_message(message_type, message_text, action_label, action_class, action_runtime_event)

    @property
    def is_empty(self):
        """
        Returns true iff this instance has no validation issues (both `messages` and `summary` are empty).
        """
        return super(StudioValidation, self).is_empty and not self.summary

    def to_json(self):
        """
        Convert to a json-serializable representation.
        """
        serialized = super(StudioValidation, self).to_json()
        if self.summary:
            serialized["summary"] = self.summary
        return serialized
