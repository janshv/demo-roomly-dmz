import pytest
from datetime import date, timedelta


def test_successful_booking(page_factory):
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    booking = page_factory.booking_page()
    booking.fill_booking(
        room="medium",
        date=tomorrow,
        start_time="10:00",
        end_time="11:00",
        participants="5",
        name="Анна Петрова",
        email="anna@example.com",
    )
    booking.submit()

    booking.expect_success_contains(
        "Средняя", tomorrow, "10:00–11:00", "Анна Петрова"
    )
    # успешное сообщение не должно содержать ошибок
    booking.room.expect_no_error()


def test_negative_room_capacity_exceeded(page_factory):
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    booking = page_factory.booking_page()
    booking.fill_booking(
        room="small",            # Малая: до 4 человек
        date=tomorrow,
        start_time="10:00",
        end_time="11:00",
        participants="5",        # больше вместимости
        name="Иван",
        email="ivan@example.com",
    )
    booking.submit()

    booking.participants.expect_error("В комнате максимум 4 участника.")
    booking.expect_error_summary()


@pytest.mark.xfail(
    strict=True,
    reason="BUG-01: отсутствует проверка длительности встречи (30 мин – 4 часа)",
    raises=AssertionError,
)
def test_bug01_duration_less_than_30_minutes(page_factory):
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    booking = page_factory.booking_page()
    booking.fill_booking(
        room="medium",
        date=tomorrow,
        start_time="10:00",
        end_time="10:20",        # 20 минут — меньше минимума
        participants="3",
        name="Тест",
        email="test@example.com",
    )
    booking.submit()

    # Ожидаем ошибку, но фактически будет success → AssertionError
    booking.end_time.expect_error("Длительность должна быть от 30 минут до 4 часов.")
    booking.expect_error_summary()
