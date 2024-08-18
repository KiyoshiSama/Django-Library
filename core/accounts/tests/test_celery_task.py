import pytest
from unittest.mock import patch, MagicMock
from django.core.cache import cache
from accounts.tasks import send_verification_code_task
from mail_templated import EmailMessage

@pytest.mark.django_db
def test_send_verification_code_task_success(user):
    user_id = user.id

    # Mock cache and email sending
    with patch.object(cache, 'set') as mock_cache_set, \
         patch.object(EmailMessage, 'send') as mock_email_send, \
         patch('accounts.tasks.logger') as mock_logger:

        mock_email_send.return_value = True

        result = send_verification_code_task(user_id)

        assert mock_cache_set.called
        cached_args = mock_cache_set.call_args[0]
        assert cached_args[0] == str(user_id)
        assert 10000 <= int(cached_args[1]) <= 99999
        assert cached_args[2] == 120

        assert mock_email_send.called

        assert mock_logger.info.called
        log_args = mock_logger.info.call_args[0][0]
        assert f"Sent activation email to {user.email}" in log_args

        assert result == True

@pytest.mark.django_db
def test_send_verification_code_task_user_not_exist():
    user_id = 9999  # Non-existent user ID

    with patch('accounts.tasks.logger') as mock_logger:

        result = send_verification_code_task(user_id)

        assert mock_logger.error.called
        log_args = mock_logger.error.call_args[0][0]
        assert f"User with id {user_id} does not exist." in log_args

        assert result == False

@pytest.mark.django_db
def test_send_verification_code_task_email_failure(user):
    user_id = user.id

    with patch.object(cache, 'set') as mock_cache_set, \
         patch.object(EmailMessage, 'send', side_effect=Exception('Email failure')) as mock_email_send, \
         patch('accounts.tasks.logger') as mock_logger:

        result = send_verification_code_task(user_id)

        assert mock_cache_set.called

        assert mock_email_send.called

        assert mock_logger.error.called
        log_args = mock_logger.error.call_args[0][0]
        assert "Failed to send activation email: Email failure" in log_args

        assert result == False
