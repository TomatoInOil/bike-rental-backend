from datetime import datetime, timezone

import pytest
from rest_framework.exceptions import ValidationError

from rental.models import RentalStatus
from rental.services import (
    calculate_total_cost,
    check_no_active_rental,
    record_rental_completion,
)


class TestCalculateRentalCost:
    @pytest.mark.parametrize(
        "start_time, end_time, rental_cost_per_hour, expectation",
        [
            (
                datetime(2024, 7, 5, 2, tzinfo=timezone.utc),
                datetime(2024, 7, 5, 4, tzinfo=timezone.utc),
                75.0,
                150.0,
            ),
            (
                datetime(2024, 7, 5, 23, tzinfo=timezone.utc),
                datetime(2024, 7, 6, 1, 30, tzinfo=timezone.utc),
                80.0,
                200.0,
            ),
            (
                datetime(2024, 7, 5, 1, 0, 0, 0, tzinfo=timezone.utc),
                datetime(2024, 7, 5, 1, 0, 1, 0, tzinfo=timezone.utc),
                100.0,
                0.03,
            ),
        ],
    )
    def test_calculate_total_cost(
        self, start_time, end_time, rental_cost_per_hour, expectation
    ):
        result = calculate_total_cost(start_time, end_time, rental_cost_per_hour)
        assert result == expectation

    @pytest.mark.parametrize(
        "start_time, end_time, rental_cost_per_hour, expectation",
        [
            (
                datetime(2024, 7, 6, 23, tzinfo=timezone.utc),
                datetime(2024, 7, 5, 1, 30, tzinfo=timezone.utc),
                80.0,
                pytest.raises(ValueError),
            ),
        ],
    )
    def test_calculate_total_cost_exceptions(
        self, start_time, end_time, rental_cost_per_hour, expectation
    ):
        with expectation:
            calculate_total_cost(start_time, end_time, rental_cost_per_hour)


class TestRentalCompletion:
    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "user_with_rental, rental_cost_per_hour, mock_now",
        [
            (
                "user_with_active_rental",
                50.0,
                datetime(2024, 7, 5, 12, tzinfo=timezone.utc),
            ),
        ],
    )
    def test_record_rental_completion(
        self, request, mocker, user_with_rental, rental_cost_per_hour, mock_now
    ):
        user, rental = request.getfixturevalue(user_with_rental)
        expected_total_cost = calculate_total_cost(
            rental.start_time, mock_now, rental_cost_per_hour
        )
        mocked_timezone_now = mocker.patch(
            "django.utils.timezone.now", return_value=mock_now
        )
        record_rental_completion(rental, rental_cost_per_hour)
        rental.refresh_from_db()
        assert rental.end_time == mock_now
        assert rental.total_cost == expected_total_cost
        assert rental.status == RentalStatus.ENDED
        mocked_timezone_now.assert_called_once()


class TestRentalStatusCheck:
    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "user",
        (
            "user_with_active_rental",
            "user_with_ended_rental",
        ),
    )
    def test_check_no_active_rental(self, request, user):
        user_obj, rental = request.getfixturevalue(user)
        try:
            check_no_active_rental(user_obj)
            assert (
                rental.status != RentalStatus.ACTIVE
            ), "Пользователь с активной арендой прошёл проверку на её отсутствие"
        except ValidationError:
            assert rental.status != RentalStatus.ENDED, (
                "Пользователь с завершенной арендой не прошёл проверку"
                " на отсутствие активной аренды."
            )
