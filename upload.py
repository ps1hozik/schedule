from tqdm import tqdm

from settings import logging
from database import connection
from parse_xlsx import get_parsed_data, Group, Pair, ExamCredit


def insert_groups(groups: list[Group]):
    try:
        with connection.cursor() as cursor:
            with tqdm(groups, desc="Вставка групп", ncols=150) as progress_bar:
                for group in progress_bar:
                    for subgroup in group.subgroups:
                        cursor.execute(
                            """
                            INSERT IGNORE INTO subgroups(faculty_name, group_name, course, specialty, form, subgroup_name) 
                            VALUES (%s, %s, %s, %s, %s, %s);
                            """,
                            (
                                group.faculty,
                                group.name,
                                group.course,
                                group.specialty,
                                group.form,
                                subgroup,
                            ),
                        )
        connection.commit()
    except Exception as e:
        logging.error(f"Ошибка вставки групп: {e}")
        connection.rollback()


def insert_pairs(pairs: list[Pair]):
    try:
        with connection.cursor() as cursor:
            temp_pair = Pair("", "1 января 1970 г.", 0, "", "", "", "")
            with tqdm(pairs, desc="Вставка пар", ncols=150) as progress_bar:
                for pair in progress_bar:
                    if (
                        temp_pair.date != pair.date
                        or temp_pair.subgroup != pair.subgroup
                    ):
                        cursor.execute(
                            "DELETE FROM pairs WHERE date = %s AND subgroup_name = %s;",
                            (pair.date, pair.subgroup),
                        )
                        temp_pair = pair
                    cursor.execute(
                        """
                        INSERT INTO pairs(week_day, date, number, teacher, auditorium, name, subgroup_name, specialty)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                        """,
                        (
                            pair.week_day,
                            pair.date,
                            pair.number,
                            pair.teacher,
                            pair.auditorium,
                            pair.name,
                            pair.subgroup,
                            pair.specialty,
                        ),
                    )
            connection.commit()
    except Exception as e:
        logging.error(f"Ошибка вставки пар: {e}")
        connection.rollback()


def insert_exams_credits(exams_credits: list[ExamCredit]):
    try:
        with connection.cursor() as cursor:
            temp_pair = ExamCredit("", "01.01.1970", "", "", "", "", "")
            with tqdm(
                exams_credits, desc="Вставка экзаменов/зачетов", ncols=150
            ) as progress_bar:
                for exam_credit in progress_bar:
                    if (
                        temp_pair.date != exam_credit.date
                        or temp_pair.subgroup != exam_credit.subgroup
                    ):
                        cursor.execute(
                            "DELETE FROM exams_credits WHERE date = %s AND subgroup_name = %s;",
                            (exam_credit.date, exam_credit.subgroup),
                        )
                        temp_pair = exam_credit
                    cursor.execute(
                        """
                        INSERT INTO exams_credits(week_day, date, teacher, auditorium, name, time, subgroup_name, specialty)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                        """,
                        (
                            exam_credit.week_day,
                            exam_credit.date,
                            exam_credit.teacher,
                            exam_credit.auditorium,
                            exam_credit.name,
                            exam_credit.time,
                            exam_credit.subgroup,
                            exam_credit.specialty,
                        ),
                    )
            connection.commit()
    except Exception as e:
        logging.error(f"Ошибка вставки экзаменов/зачетов: {e}")
        connection.rollback()


if __name__ == "__main__":
    groups, pairs, exams_credits = get_parsed_data()
    insert_groups(groups)
    insert_pairs(pairs)
    insert_exams_credits(exams_credits)
