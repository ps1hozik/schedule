from download import download
from parse_xlsx import get_parsed_data
from upload import insert_exams_credits, insert_pairs, insert_groups

if __name__ == "__main__":
    ask = lambda msg: input(f"{msg} (y/n): ").lower().strip()
    is_yes = lambda response: response in {"y", "yes", "д", "да"}

    if is_yes(ask("Скачать расписания?")):
        download()

    if is_yes(ask("Загрузить в бд?")):
        groups, pairs, exams_credits = get_parsed_data()
        if not groups:
            exit(0)
        insert_groups(groups)
        if pairs:
            insert_pairs(pairs)
        if exams_credits:
            insert_exams_credits(exams_credits)
