from datetime import datetime, timedelta
from typing import List, Literal

from tgbot.models.sql_connector import RegistrationsDAO


def find_free_slot(events: List[tuple], duration: int, start_time: datetime, end_time: datetime) -> str:
    sorted_events = sorted(events, key=lambda x: x[0])
    for event in sorted_events:
        end_time = event[0]

        time_diff = datetime.combine(datetime.today(), end_time) - datetime.combine(datetime.today(), start_time)

        if time_diff >= timedelta(minutes=duration):
            return start_time.strftime("%H:%M")  # Found a free slot

        start_time = event[1]

    time_diff = datetime.combine(datetime.today(), end_time) - datetime.combine(datetime.today(), start_time)
    if time_diff >= timedelta(minutes=duration):
        return start_time.strftime("%H:%M")  # Found a free slot

    return None  # No free slot found


async def date_slots_checker(offset: int, duration: int) -> list:
    result = []
    counter = 0
    for i in range(offset + 1, 32):
        day = datetime.today() + timedelta(days=i)
        day_regs = await RegistrationsDAO.get_many(reg_date=day)
        reg_tuples = []
        for reg in day_regs:
            reg_tuples.append((reg["reg_time_start"], reg["reg_time_finish"]))
        start_time = datetime.strptime("9:00", "%H:%M").time()
        end_time = datetime.strptime("22:00", "%H:%M").time()
        day_slot = find_free_slot(events=reg_tuples, duration=duration, start_time=start_time, end_time=end_time)
        if day_slot:
            result.append(day)
            counter += 1
        if counter == 6:
            break
    return result


async def time_three_slots_checker(date: datetime, duration: int) -> list:
    result = []
    day_regs = await RegistrationsDAO.get_many(reg_date=date)
    reg_tuples = []
    for reg in day_regs:
        reg_tuples.append((reg["reg_time_start"], reg["reg_time_finish"]))
    for time_tuple in [("9:00", "12:00", "morning"), ("12:00", "18:00", "day"), ("18:00", "22:00", "evening")]:
        start_time = datetime.strptime(time_tuple[0], "%H:%M").time()
        if time_tuple[2] == "evening":
            end_time = datetime.strptime(time_tuple[1], "%H:%M").time()
        else:
            end_time = (datetime.strptime(time_tuple[1], "%H:%M") + timedelta(minutes=duration)).time()
        day_slot = find_free_slot(events=reg_tuples, duration=duration, start_time=start_time, end_time=end_time)
        if day_slot:
            result.append(time_tuple[2])
    return result


async def one_slot_checker(date: datetime, day_part: Literal["morning", "day", "evening"], duration: int):
    slots = {
        "morning": ("9:00", "12:00"),
        "day": ("12:00", "18:00"),
        "evening": ("18:00", "22:00"),
    }
    day_regs = await RegistrationsDAO.get_many(reg_date=date)
    reg_tuples = []
    for reg in day_regs:
        reg_tuples.append((reg["reg_time_start"], reg["reg_time_finish"]))
    start_time = datetime.strptime(slots[day_part][0], "%H:%M").time()
    if day_part == "evening":
        end_time = datetime.strptime(slots[day_part][1], "%H:%M").time()
    else:
        end_time = (datetime.strptime(slots[day_part][1], "%H:%M") + timedelta(minutes=duration)).time()
    day_slot = find_free_slot(events=reg_tuples, duration=duration, start_time=start_time, end_time=end_time)
    day_slot = datetime.strptime(day_slot, "%H:%M").time()
    return day_slot


async def check_free_slot(reg_date: datetime, reg_time: datetime, duration: int) -> str:
    regs_list = await RegistrationsDAO.get_many_created(reg_date=reg_date)
    end_time = (datetime.combine(datetime.today(), reg_time) + timedelta(minutes=duration)).time()
    free_slot = find_free_slot(events=regs_list, duration=duration, start_time=reg_time, end_time=end_time)
    return free_slot

