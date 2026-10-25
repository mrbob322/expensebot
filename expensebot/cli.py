import argparse
import csv
import json
import os
import sys
from datetime import date, datetime

from . import ExpenseService, NotFoundError, ValidationError, StorageError, __version__


def _d(s):
    return datetime.strptime(s, "%Y-%m-%d").date()


def _out(rows, header, fmt, stream=sys.stdout):
    if fmt == "json":
        json.dump([dict(zip(header, map(str, r))) for r in rows], stream,
                  ensure_ascii=False, indent=2); stream.write("\n")
    elif fmt == "csv":
        w = csv.writer(stream); w.writerow(header); w.writerows(rows)
    else:
        stream.write("\t".join(header) + "\n")
        for r in rows:
            stream.write("\t".join(map(str, r)) + "\n")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="expensebot", description="Учёт расходов")
    p.add_argument("--version", action="version", version=__version__)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("-f", "--format", choices=["table", "json", "csv"], default="table")
    common.add_argument("-v", "--verbose", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add", parents=[common]); a.add_argument("amount"); a.add_argument("category")
    a.add_argument("-c", "--comment"); a.add_argument("-d", "--date", type=_d)
    for n in ("list", "report", "export"):
        s = sub.add_parser(n, parents=[common]); s.add_argument("--from", dest="date_from", type=_d)
        s.add_argument("--to", dest="date_to", type=_d)
        s.add_argument("--category"); s.add_argument("--limit", type=int, default=20)
        if n == "export":
            s.add_argument("-o", "--output")
    x = sub.add_parser("delete", parents=[common]); x.add_argument("id", type=int)
    sub.add_parser("categories", parents=[common]); sub.add_parser("run", parents=[common])
    try:
        args = p.parse_args(argv)
    except SystemExit as e:
        return int(e.code or 0)
    svc = None
    try:
        if args.cmd == "run":
            if not os.getenv("EXPENSEBOT_TOKEN"):
                print("Не задан EXPENSEBOT_TOKEN", file=sys.stderr); return 9
            print("Запуск Telegram-бота (подключите bot.py)"); return 0
        svc = ExpenseService(os.getenv("EXPENSEBOT_DB", "expenses.db"))
        if args.cmd == "add":
            e = svc.add(args.amount, args.category, args.comment, args.date)
            print(f"Добавлено: #{e.id} {e.amount} {e.category}")
        elif args.cmd == "list":
            rows = [(e.id, e.date, e.category, e.amount, e.comment or "")
                    for e in svc.list(args.limit, args.category, args.date_from, args.date_to)]
            _out(rows, ["id", "date", "category", "amount", "comment"], args.format)
        elif args.cmd == "delete":
            svc.delete(args.id); print("Удалено")
        elif args.cmd == "categories":
            _out([(c.id, c.name) for c in svc.categories()], ["id", "name"], args.format)
        elif args.cmd in ("report", "export"):
            d1 = args.date_from or date.today().replace(day=1)
            d2 = args.date_to or date.today()
            if args.cmd == "report":
                rows = sorted(svc.summary(d1, d2).items())
                _out(rows, ["category", "total"], args.format)
            else:
                rows = [(e.id, e.date, e.category, e.amount, e.comment or "")
                        for e in svc.list(100000, args.category, d1, d2)]
                if args.output:
                    with open(args.output, "w", newline="", encoding="utf-8") as f:
                        _out(rows, ["id", "date", "category", "amount", "comment"],
                             args.format, f)
                else:
                    _out(rows, ["id", "date", "category", "amount", "comment"], args.format)
        return 0
    except ValidationError as e:
        print(f"Ошибка: {e}", file=sys.stderr); return 3
    except NotFoundError as e:
        print(f"Ошибка: {e}", file=sys.stderr); return 4
    except StorageError as e:
        print(f"Ошибка БД: {e}", file=sys.stderr); return 6
    except OSError as e:
        print(f"Ошибка файла: {e}", file=sys.stderr); return 8
    except KeyboardInterrupt:
        return 10


if __name__ == "__main__":
    sys.exit(main())
