# coding=utf-8
import pymysql
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts
import inspect
import time

def get_post():
    print("%s invoked" % (inspect.stack()[1][3]))
    conn = pymysql.connect(host='localhost',
                           port=3306,
                           user='root',
                           passwd='',
                           db='scrapy_db',
                           charset='utf8mb4')
    cursor = conn.cursor()
    sql_post = """
    select
      id,
      origin_url,
      cate,
      title,
      imgs,
      content,
      RAND() as rand
    from recipes where id not in (select id from backup)
order by rand
    """
    cursor.execute(sql_post)
    return cursor.fetchall()


def update_post(id):
    print("%s invoked" % (inspect.stack()[1][3]))
    conn = pymysql.connect(host='localhost',
                           port=3306,
                           user='root',
                           passwd='',
                           db='scrapy_db',
                           charset='utf8mb4')
    cursor = conn.cursor()
    sql_post = """
    insert into backup VALUES ({id})
    """
    cursor.execute(sql_post.format(id=id))
    conn.commit()


def publish(results):
    try:
        print("%s invoked" % (inspect.stack()[1][3]))
        wp_client = Client('http://www.bbgo321.com/xmlrpc.php', 'jkdcdlly', 'mfYU6wnXuWBYSgOWVu')
        for result in results:
            time.sleep(5)
            id, origin_url, cate, title, imgs, content, rand = result
            print(id)
            word_press_post = WordPressPost()
            word_press_post.title = title
            word_press_post.content = content
            word_press_post.terms_names = {
                'category': [cate]
            }
            word_press_post.post_status = 'publish'
            word_press_post.id = wp_client.call(posts.NewPost(word_press_post))
            update_post(id)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    results = get_post()
    publish(results)
