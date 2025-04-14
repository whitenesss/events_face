import requests
import json
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from ...models import SyncResult
from src.events.models import Event


class Command(BaseCommand):
    help = 'Синхронизирует события с events-provider'

    def add_arguments(self, parser):
        parser.add_argument(
            '--date',
            type=str,
            help='Дата для синхронизации в формате YYYY-MM-DD'
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Синхронизировать все события'
        )

    def handle(self, *args, **options):
        sync_date = None
        sync_all = options['all']

        if options['date']:
            try:
                sync_date = datetime.strptime(options['date'], '%Y-%m-%d').date()
            except ValueError:
                self.stdout.write(self.style.ERROR('Неверный формат даты. Используйте YYYY-MM-DD'))
                return
        elif not sync_all:
            sync_date = (timezone.now() - timedelta(days=1)).date()

        sync_result = SyncResult.objects.create(
            date_filter=sync_date,
            sync_all=sync_all
        )

        try:
            base_url = 'https://events.k3scluster.tech/api/events/'
            params = {}

            if sync_date and not sync_all:
                params['changed_at'] = sync_date.strftime('%Y-%m-%d')

            self.stdout.write(f"Начало синхронизации {'всех событий' if sync_all else 'за ' + str(sync_date)}")

            new_count = 0
            updated_count = 0
            next_page = base_url

            while next_page:
                response = requests.get(next_page, params=params)
                response.raise_for_status()

                try:
                    data = response.json()
                except json.JSONDecodeError:
                    raise ValueError("Неверный формат ответа от API: ожидался JSON")

                if not isinstance(data, dict) or 'results' not in data:
                    raise ValueError(f"Неожиданная структура ответа: {data}")

                events_data = data['results']

                for event_data in events_data:
                    if not isinstance(event_data, dict):
                        self.stdout.write(self.style.WARNING(f"Пропущен невалидный элемент: {event_data}"))
                        continue

                    try:
                        # Конвертируем статус
                        status = (
                            Event.Status.OPEN
                            if str(event_data.get('status', '')).lower() == 'open'
                            else Event.Status.CLOSED
                        )

                        # Конвертируем дату события
                        event_time = datetime.fromisoformat(event_data['event_time'])

                        # Создаем или обновляем событие
                        event, created = Event.objects.update_or_create(
                            id=event_data['id'],
                            defaults={
                                'name': event_data['name'],
                                'date': event_time,
                                'status': status,
                                'venue': None  # В API нет информации о площадках
                            }
                        )

                        if created:
                            new_count += 1
                        else:
                            updated_count += 1

                    except Exception as e:
                        self.stdout.write(self.style.WARNING(
                            f"Ошибка обработки события {event_data.get('id')}: {str(e)}"
                        ))
                        continue

                # Получаем следующую страницу
                next_page = data.get('next')
                params = {}  # Для последующих запросов параметры уже в URL

            # Обновляем результат синхронизации
            sync_result.finished_at = timezone.now()
            sync_result.new_events_count = new_count
            sync_result.updated_events_count = updated_count
            sync_result.is_success = True
            sync_result.save()

            self.stdout.write(self.style.SUCCESS(
                f"Синхронизация завершена успешно. "
                f"Новых событий: {new_count}, обновленных: {updated_count}"
            ))

        except requests.RequestException as e:
            sync_result.finished_at = timezone.now()
            sync_result.error_message = str(e)
            sync_result.save()
            self.stdout.write(self.style.ERROR(f"Ошибка при синхронизации: {str(e)}"))

        except Exception as e:
            sync_result.finished_at = timezone.now()
            sync_result.error_message = str(e)
            sync_result.save()
            self.stdout.write(self.style.ERROR(f"Неожиданная ошибка: {str(e)}"))