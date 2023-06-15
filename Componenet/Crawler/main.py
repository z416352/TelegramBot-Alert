import Crawler
import sqlite3



# 连接到 SQLite 数据库
conn = sqlite3.connect('crypto_alerts.sqlite')
cursor = conn.cursor()


# 执行 INSERT 语句插入数据
def insert_data(coin, price, alert_mode, alerted):
    query = f"INSERT INTO crypto_alerts (coin, price, alert_mode, alerted) VALUES ('{coin}', {price}, '{alert_mode}', {alerted})"
    cursor.execute(query)
    conn.commit()
    print('数据已插入')


def select_all_data():
    query = "SELECT * FROM crypto_alerts"
    cursor.execute(query)
    rows = cursor.fetchall()

    # 打印查询结果
    for row in rows:
        print(f"Coin: {row[0]}, Price: {row[1]}, Alert Mode: {row[2]}, Alerted: {row[3]}")


if __name__ == '__main__':
    # 创建表格
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crypto_alerts (
            coin TEXT,
            price REAL,
            alert_mode TEXT,
            alerted INTEGER DEFAULT 0
        )
    ''')


    # 测试
    # insert_data('Bitcoin', 50000, 'Email', 0)
    # insert_data('Ethereum', 3000, 'SMS', 0)

    # select_all_data()

    # 关闭数据库连接
    cursor.close()
    conn.close()


    l = Crawler.get_kline(symbol = "BTCUSDT", interval = "15m")
    # print(type(int(float(l[1]))))