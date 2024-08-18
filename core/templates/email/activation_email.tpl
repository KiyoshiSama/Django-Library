{% extends "mail_templated/base.tpl" %}

{% block subject %}
Account activation
{% endblock %}

{% block html %}
your code is {{verification_code}}

{% endblock %}