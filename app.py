from flask import Flask, render_template, request
import psycopg2
import json

app = Flask(__name__)


def get_connection(cfg):
    return psycopg2.connect(**cfg)


def get_tables(conn):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        return [row[0] for row in cur.fetchall()]


def get_table_definition(conn, table):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = %s
            ORDER BY ordinal_position;
        """, (table,))
        return cur.fetchall()


def get_table_data(conn, table):
    with conn.cursor() as cur:
        cur.execute(f"SELECT * FROM {table} ORDER BY 1;")
        return cur.fetchall()


@app.route("/", methods=["GET", "POST"])
def compare_databases():
    if request.method == "GET":
        return render_template("db_form.html")

    # Получаем настройки подключения из формы
    DB1 = {
        "dbname": request.form["db1_name"],
        "user": request.form["db1_user"],
        "password": request.form["db1_pass"],
        "host": request.form["db1_host"],
        "port": request.form["db1_port"]
    }
    DB2 = {
        "dbname": request.form["db2_name"],
        "user": request.form["db2_user"],
        "password": request.form["db2_pass"],
        "host": request.form["db2_host"],
        "port": request.form["db2_port"]
    }

    conn1 = get_connection(DB1)
    conn2 = get_connection(DB2)

    host1 = DB1.get("host", "База 1")
    host2 = DB2.get("host", "База 2")

    # Получаем список таблиц
    tables1 = get_tables(conn1)
    tables2 = get_tables(conn2)
    all_tables = sorted(set(tables1) | set(tables2))

    tables_diff = []
    for table in all_tables:
        t1 = "Есть" if table in tables1 else "Нет"
        t2 = "Есть" if table in tables2 else "Нет"
        tables_diff.append({
            "table": table,
            "val1": t1,
            "val2": t2,
            "is_match": (t1 == t2)
        })

    # Сравнение структур
    structure_diff = []
    for table in sorted(set(tables1) & set(tables2)):
        struct1 = get_table_definition(conn1, table)
        struct2 = get_table_definition(conn2, table)

        rows = []
        max_len = max(len(struct1), len(struct2))
        for i in range(max_len):
            col1 = struct1[i] if i < len(struct1) else ""
            col2 = struct2[i] if i < len(struct2) else ""
            is_match = (col1 == col2)
            rows.append({
                "crit": f"Колонка {i+1}",
                "val1": str(col1),
                "val2": str(col2),
                "is_match": is_match
            })

        structure_diff.append({
            "table": table,
            "rows": rows,
            "match_count": sum(1 for r in rows if r["is_match"]),
            "diff_count": sum(1 for r in rows if not r["is_match"])
        })

    # Сравнение данных
    data_diff = []
    for table in sorted(set(tables1) & set(tables2)):
        data1 = get_table_data(conn1, table)
        data2 = get_table_data(conn2, table)

        if data1 != data2:
            rows = []
            max_len = max(len(data1), len(data2))
            for i in range(max_len):
                row1 = data1[i] if i < len(data1) else ""
                row2 = data2[i] if i < len(data2) else ""
                is_match = (row1 == row2)
                rows.append({
                    "crit": f"Запись {i+1}",
                    "val1": str(row1),
                    "val2": str(row2),
                    "is_match": is_match
                })

            data_diff.append({
                "table": table,
                "rows": rows,
                "match_count": sum(1 for r in rows if r["is_match"]),
                "diff_count": sum(1 for r in rows if not r["is_match"])
            })

    conn1.close()
    conn2.close()

    return render_template(
        "diff_report.html",
        host1=host1,
        host2=host2,
        tables_diff=tables_diff,
        structure_diff=structure_diff,
        data_diff=data_diff
    )


if __name__ == "__main__":
    app.run(debug=True)
