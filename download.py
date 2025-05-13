import os
import shutil

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any

import re
import json
import logging

from tqdm import tqdm
from prompt_toolkit.shortcuts import checkboxlist_dialog, radiolist_dialog

import requests
from bs4 import BeautifulSoup

from settings import FACULTIES_URL, BASE_URL, DATA_FOLDER, STYLE

logging.basicConfig(level=logging.INFO)


@dataclass
class Schedule:
    faculty_name: str
    faculty_short_name: str
    url: str
    form: str
    title: str
    path: Path = field(init=False)
    file: Path = field(init=False)

    def __post_init__(self):
        self.path = Path(DATA_FOLDER) / self.faculty_name / self.form
        self.file = self.path / f"{self.title}.xlsx"

    def __str__(self):
        return f"{self.faculty_short_name} {self.form} : {self.title}"


def _update_faculties() -> None:
    faculties = []

    short_title = lambda faculty_title: "".join(
        f[0].upper() for f in faculty_title.replace("-", " ").split()
    )

    response = requests.get(FACULTIES_URL)
    soup = BeautifulSoup(response.content, "html.parser")
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and "/universitet/fakultety" in href and "/raspisanie.html" in href:
            title = re.sub(r"[^А-Яа-я]\s+", "", link.text)
            url = BASE_URL.format(urn=href)
            short = short_title(title)
            faculties.append(
                {
                    "title": title,
                    "url": url,
                    "short": short,
                }
            )
    with open("faculties.json", "w", encoding="utf-8") as file:
        json.dump(faculties, file, indent=4, ensure_ascii=False)


def _clear_data_dir():
    if os.path.exists(DATA_FOLDER):
        shutil.rmtree(DATA_FOLDER)
    os.makedirs(DATA_FOLDER)


def _load_faculties_from_file() -> List[Dict[str, str]]:
    try:
        with open("faculties.json", "r", encoding="utf-8") as file:
            faculties = json.load(file)
        return faculties
    except FileNotFoundError:
        logging.warning("Файл faculties.json не найден")
        exit(1)
    except json.JSONDecodeError:
        logging.error("Ошибка при декодировании файла faculties.json")
        exit(1)


def _faculties_menu() -> List[Any]:
    faculties = _load_faculties_from_file()
    menu_options = [(faculty, faculty["title"]) for faculty in faculties]
    selected_items = checkboxlist_dialog(
        title="Выбор факультетов",
        text="Ок для выбора всего",
        values=menu_options,
        style=STYLE,
    ).run()

    if selected_items is None:
        exit(0)

    if not selected_items:
        return faculties

    return selected_items


def _form_menu() -> str:
    menu_options = [("all", "Все"), ("до", "ДО"), ("зо", "ЗО")]
    selected_item = radiolist_dialog(
        title="Выбор формы",
        values=menu_options,
        style=STYLE,
    ).run()

    if selected_item is None:
        exit(0)

    return selected_item


def _find_schedules(faculties: List[Dict[str, str]], form: str) -> List["Schedule"]:
    schedules: List["Schedule"] = []

    with tqdm(faculties, desc="Поиск расписаний", ncols=150) as progress_bar:
        for faculty in progress_bar:
            faculty_name = faculty["title"]
            faculty_short_name = faculty["short"]
            faculty_url = faculty["url"]

            progress_bar.set_description(f"Поиск в  '{faculty_name:<50}'")

            response = requests.get(faculty_url)
            soup = BeautifulSoup(response.content, "html.parser")
            for link in soup.find_all("a"):
                href = link.get("href")
                if (
                    href
                    and (".xlsx" in link.text or ".xlsx" in href)
                    and "Расписание" in link.text
                ):
                    url = BASE_URL.format(urn=href)

                    if "зфпо" in href.lower():
                        detected_form = "зо"
                    else:
                        detected_form = "до"

                    if form == "all" or detected_form == form:
                        schedules.append(
                            Schedule(
                                faculty_name=faculty_name,
                                faculty_short_name=faculty_short_name,
                                url=url,
                                form=detected_form,
                                title=link.text,
                            )
                        )
    return schedules


def _schedules_menu(schedules: List["Schedule"]) -> List:
    faculty_tmp = schedules[0].faculty_name
    form_tmp = schedules[0].form

    menu_options = []
    for sch in schedules:
        if faculty_tmp != sch.faculty_name:
            menu_options.append(("-1", ""))
            menu_options.append(("-1", "-" * 50))
            menu_options.append(("-1", ""))
            form_tmp = sch.form
        if form_tmp != sch.form:
            menu_options.append(("-1", ""))
        menu_options.append((sch, str(sch)))
        form_tmp = sch.form
        faculty_tmp = sch.faculty_name

    selected_items = checkboxlist_dialog(
        title="Выбор расписаний",
        text="Ок для выбора всего",
        values=menu_options,
        style=STYLE,
    ).run()

    if selected_items is None:
        exit(0)

    if not selected_items:
        return schedules

    return [item for item in selected_items if isinstance(item, Schedule)]


def _download_schedules(schedules: List["Schedule"]) -> None:
    format_description = lambda data: data[:47] + "..." if len(data) > 47 else data
    with tqdm(schedules, desc="Загрузка расписаний", ncols=150) as progress_bar:
        for schedule in progress_bar:
            response = requests.get(schedule.url, allow_redirects=True)

            description = format_description(str(schedule))
            progress_bar.set_description(f"Загрузка '{description:<50}'")

            if schedule.path and not os.path.exists(schedule.path):
                os.makedirs(schedule.path)
            with open(schedule.file, "wb") as file:
                file.write(response.content)


def download() -> None:
    if not os.path.exists("faculties.json"):
        _update_faculties()
    _clear_data_dir()
    selected_faculties = _faculties_menu()
    form = _form_menu()
    schedules = _find_schedules(selected_faculties, form)
    selected_schedules = _schedules_menu(schedules)
    _download_schedules(selected_schedules)


if __name__ == "__main__":
    download()
