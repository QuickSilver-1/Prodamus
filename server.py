from fastapi import FastAPI, Header, Body
from psycopg2 import connect
from bot import first_day_of_intensive
from uvicorn import run
from urllib import parse


app = FastAPI()


@app.post("/")
async def get_pay_answer(payment_status = Body()):
    payment_status = parse.parse_qs(parse.unquote(payment_status.decode()))

    try:
        tg_id = payment_status["order_num"][0][:-11]
    except:
        tg_id = payment_status["order_num"][0]
    print(tg_id)
    connection = connect(dbname='sofiasomova', user='roman', password='1234', host='45.81.226.118')
    cursor = connection.cursor()
    if payment_status["payment_status"][0] == 'success':
        cursor.execute(f'''SELECT COUNT(*) FROM "order" WHERE tg_id='{tg_id}';''')
    if cursor.fetchall()[0][0] >= 1:
        cursor.execute(f'''UPDATE "order" SET status = 'complete' WHERE tg_id='{tg_id}';''')
        connection.commit()
        await first_day_of_intensive(tg_id)

if __name__ =="__main__":
    run("server:app", host='45.81.226.118', port=81, log_level='info')
