import logging, time

from django.db.models.signals 	import post_save
from django.template.loader 	import render_to_string
from django.dispatch 			import receiver

from requests import HTTPError, status_codes

from feedback_requests.config 	import TELEGRAM_SEND_NOTIFICATIONS
from feedback_requests.models 	import FeedbackRequest
from core.models.general 		import TelegramSendingChannel


_logger = logging.getLogger(__name__)


@receiver(post_save, sender = FeedbackRequest)
def send_new_request_notification_into_telegram(sender, instance: FeedbackRequest, created, **kwargs):
	if not created:
		return

	specialization = TelegramSendingChannel.Specialization.NEW_REQUEST_NOTIFICATIONS
	telegram_sending_channel = TelegramSendingChannel.get_by_specialization(specialization)

	if not telegram_sending_channel:
		return

	message = render_to_string(
		TELEGRAM_SEND_NOTIFICATIONS.TG_MESSAGE_TEMPLATE_NAME,
		{'request': instance}
	)

	error_message: str = ""
	for _ in range(0, TELEGRAM_SEND_NOTIFICATIONS.ATTEMPTS_COUNT):
		# Эта функция будет выполнятся в отдельном потоке, так что всё путём
		success, ex = telegram_sending_channel.try_send_message(message)

		if success:
			# Завершаем работу функции
			instance.seen = True
			instance.save()
			_logger.debug(f"Успешно отправил уведомление о новой заявке в телеграмм.")
			return


		error_message = str(ex)
		# Это ошибка статуса (raise_for_status())
		if isinstance(ex, HTTPError):
			error_message = f"{ex.response.status_code}: {ex.response.json()['description']}"

			status_code: int = ex.response.status_code
			status_group = status_code // 100

			code_allow_retry = lambda code: code in TELEGRAM_SEND_NOTIFICATIONS.RETRY_ATTEMPT_HTTP_CODES
			if not any(map(code_allow_retry, (status_group, status_code))):
				_logger.debug(
					f'Это HTTPError и кода ошибки нет в списке для прекращения попыток отправить сообщение')
				break

			TOO_MANY_REQUESTS = 429
			if status_code == TOO_MANY_REQUESTS:
				pause_time = TELEGRAM_SEND_NOTIFICATIONS.SLEEP_TIME_ON_TOO_MANY_REQUESTS

				_logger.debug(f"Это Too Many Requests, ухожу в \"спячку\" на {pause_time}.")
				time.sleep(pause_time)

	# Все ошибки будут обработаны тут
	_logger.error(f"Не смог отправить уведомление о создании новой заявки в телеграм: {error_message}")
