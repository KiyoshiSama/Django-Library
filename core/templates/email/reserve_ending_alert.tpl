{% extends "mail_templated/base.tpl" %}

{% block subject %}
Reservation ending
{% endblock %}

{% block html %}
Warning, your reserve time is almost ending. you should return {{book_name}} book or take action to reserve the book again.
you have only {{days_remaining}} days left dear {{user_first_name}}

{% endblock %}