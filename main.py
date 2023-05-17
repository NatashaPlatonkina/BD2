import psycopg2

#conn = psycopg2.connect(database='netology_db', user='postgres', password='3662075')

def create_db():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS customers(
        customers_id SERIAL PRIMARY KEY,
        f_name VARCHAR(30) NOT NULL,
        l_name VARCHAR(40) NOT NULL,
        email VARCHAR(50) NOT NULL
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phone_numbers(
        id SERIAL PRIMARY KEY,
        number VARCHAR(15) UNIQUE,
        customers_id int REFERENCES customers(customers_id)
        );
    """)

def add_new_customer(first_name, last_name, email):
    cur.execute("""
            INSERT INTO customers(f_name, l_name, email)
            VALUES(%s, %s, %s) RETURNING customers_id;
            """, (first_name, last_name, email))


# conn.commit()
def id_customer(e_mail):
    cur.execute("""
                SELECT * FROM customers
                WHERE email = %s
                ;
                """, (e_mail,))
    customers_id = cur.fetchone()[0]
    return customers_id


def id_number(number):
    cur.execute("""
                SELECT * FROM phone_numbers
                WHERE number = %s
                ;
                """, (number,))
    id = cur.fetchone()[0]
    return id


def add_phone_number(e_mail, pn):
    cur.execute("""
                INSERT INTO phone(num, client_id)
                VALUES(%s, %s);
                """, (pn, id_customer(e_mail)))


def change_customer(table, column, info, current):
    if table == 'phone_numbers':
        cur.execute("""
                    UPDATE phone_numbers SET number=%s WHERE id=%s
                    """, (info, id_number(current)))
    elif table == 'customer':
        if column == 'f_name':
            cur.execute("""
                        UPDATE customer SET f_name=%s WHERE customers_id=%s
                        """, (info, id_customer(current)))
        elif column == 'l_name':
            cur.execute("""
                        UPDATE customer SET l_name=%s WHERE customers_id=%s
                        """, (info, id_customer(current)))
        elif column == 'email':
            cur.execute("""
                        UPDATE customer SET email=%s WHERE customers_id=%s
                        """, (info, id_customer(current)))


def delete_phone_number(phone_numbers):
    cur.execute("""
                DELETE FROM phone_numbers WHERE number=%s
                """, (phone_numbers,))


def delete_customer(email):
    cur.execute("""
                DELETE FROM customers WHERE customers_id=%s
                """, (id_customer(email),))


def find_customer():
    current = input('Поиск по "customers" или "phone_number":')
    if current == 'customers':
        print(id_customer(input('Введите email:')))
    elif current == 'phone_number':
        print(id_number(input('Введите номер телефона:')))


with conn.cursor() as cur:
    cur.execute(""" DROP TABLE phone_number; DROP TABLE customers""")
    create_db()
    add_new_customer(first_name='Иван', last_name='Петров', email='Ivankapetr@gmail.com')
    add_phone_number('Ivankapetr@gmail.com', '+79067456434')
    change_customer('customers', 'email', 'Mishkaya45@yandex.ru', 'Ivankapetr@gmail.com')
    find_customer()
    delete_phone_number('+79067456434')
    delete_customer('Mishkaya45@yandex.ru')
    conn.commit()
    conn.close()
