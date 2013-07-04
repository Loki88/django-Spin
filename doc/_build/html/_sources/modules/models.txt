Models
============
The Spin class is the center of the application. It represents what the users can condivide with other ones:

* simple Spin: only-text;
* multimedia Spin: text + multimedia (images or videos).

Since a Spin could contain etherogeneous contents, it's important to provide a robust implementation for it.
The way this can be achieved is to use a powerful trick offered by Django ORM: ereditariety.
.. Thinking at the main problem:

.. * a *multimedia Spin* is only a *simple Spin* that can contain multimedia;
.. * there is the need to provide different mechanisms and to define how a multimedia spin should act like;
.. * there is really the need to define a model for them?

.. Everything is relative! It depends on how we aim our app act like. This is a project choice and could be explained in some scenarios:

.. * Let's suppose that the multimedia is a link in the text contained in the spin. There's not the need to construct a model,
..   the multimedia can be stored with the content of the ribbit and the view can display it transparently to the database layer.
.. * Let's suppose now that the user want to include a photo from is personal computer. He have to perform an upload on a server and the
..   application needs to store it somewhere, catching and saving the path in related object in database. Somewhere in the views whe have
..   to make distinction between the insert of these objects.

.. Let's suppose we want both these scenarios, what could we do? First, we can provide a view mechanism to transform links in multimedia;
.. then we can provide ereditariety for Ribbit, transforming it in Ribbit++, consenting user to add a photo or video displaying this on
.. the application page.

----------------
Class Reference
----------------

UserProfile
______________
.. automodule:: spin_base.models.user
	:members:

Relationship
______________
.. automodule:: spin_base.models.relationship
	:members:

Spins
______________
.. automodule:: spin_base.models.spin
	:members:

Comments
______________
.. automodule:: spin_base.models.comment
	:members:

Reports
______________
.. automodule:: spin_base.models.report
	:members:

App Style
______________
.. automodule:: spin_base.models.style
	:members: