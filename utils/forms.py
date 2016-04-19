"""Utilities for working with forms"""

def bind_form_parameters(formclass, **formclass_kwargs):
    """Return a subclass of the input formclass with additional constructor
    parameters bound from formclass_kwargs.
    """
    class BoundClass(formclass):
        def __init__(self, *args, **kwargs):
            kwargs.update(formclass_kwargs)
            super(BoundClass, self).__init__(*args, **kwargs)
    return BoundClass

