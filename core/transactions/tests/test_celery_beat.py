import pytest
from unittest.mock import patch
from django.core import mail
from transactions.tasks import send_borrow_ending_alert


@pytest.mark.django_db
def test_send_borrow_ending_alert(setup_checkouts):
    with patch('transactions.tasks.logger') as mock_logger:
        send_borrow_ending_alert()

        assert len(mail.outbox) == 1
        assert mail.outbox[0].to == [setup_checkouts.customer.email]

        email_body = mail.outbox[0].body
        assert 'you have only 2 days left' in email_body
        assert setup_checkouts.book.title in email_body
        assert setup_checkouts.customer.first_name in email_body

        mock_logger.info.assert_called_with(
            f"Sent borrow ending alert to {setup_checkouts.customer.email} for book {setup_checkouts.book.title}"
        )
