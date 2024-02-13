from datetime import date
from typing import List
from sqlalchemy.orm import Session
from Backend.db.models import Shift
from Backend.db.repositories.base_repository import BaseRepository
from Backend.db.repositories.shiftWorkers_repository import ShiftWorkersRepository


class ShiftsRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, Shift)

    def get_shift_by_day_and_part_and_workplace(self, day: str, part: str, workplace: int):
        return self.db.query(Shift).filter(Shift.shiftDay == day, Shift.shiftPart == part, Shift.workPlaceID == workplace).first()

    def get_all_shifts_since_date(self, given_date: date):
        """
        Retrieves all shifts of a worker since a given date.

        Parameters:
            given_date (date): Date to retrieve the shifts since.

        Returns:
            List of shifts of the worker since the given date.
        """
        return self.db.query(Shift).filter(
            Shift.shiftDate >= given_date
        ).all()

    def get_all_shifts_since_date_for_given_worker(self, date: date, worker_id: str) -> List[Shift]:
        """
        Retrieves all shifts of a worker since a given date.
        Args:
            date (date): Date to retrieve the shifts since.
            worker_id (str): ID of the worker to retrieve shifts for.

        Returns: List of shifts of the worker since the given date.
        """
        # Reuse the get_all_shifts_since_date function
        shifts = self.get_all_shifts_since_date(date)

        # Get the shift workers repository
        shift_workers_repository = ShiftWorkersRepository(self.db)

        # Filter shifts based on the given worker ID
        shifts_for_worker = [shift for shift in shifts if
                             shift_workers_repository.is_shift_assigned_to_worker(shift.id, worker_id)]
        return shifts_for_worker

    def get_all_shifts_since_date_for_given_workplace(self, given_date: date, workplace_id: str) -> List[Shift]:
        """
        Retrieves all shifts of a workplace since a given date.
        Args:
            given_date (date): Date to retrieve the shifts since.
            workplace_id (str): ID of the workplace to retrieve shifts for.

        Returns: List of shifts of the workplace since the given date.
        """
        # Reuse the get_all_shifts_since_date function
        shifts = self.get_all_shifts_since_date(given_date)

        # Filter shifts based on the given workplace ID
        shifts_for_workplace = [shift for shift in shifts if shift.workPlaceID == workplace_id]
        return shifts_for_workplace
