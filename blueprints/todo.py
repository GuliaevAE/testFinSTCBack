from flask import Blueprint, request
import  psycopg2
from psycopg2.extras import RealDictCursor
from  config import host, user, password, db_name


from datetime import datetime
todo = Blueprint('todo', __name__)

@todo.route('/todos', methods=['GET'])
def get_todos():
    if request.method == 'GET':
        try:
            connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
            )
            print('connect')
            with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM todos;")
                
                fetch = cursor.fetchall()
                obj = {}
                arr =[]
                for stock in fetch:
                    obj['id'] = stock['id']
                    obj['title'] = stock['title']
                    obj['status'] = stock['status']
                    obj['time'] = stock['time']
                    arr.append(obj.copy())

                arr = sorted(
                arr,
                key=lambda x: datetime.strftime(x['time'], '%Y-%m-%d %H:%M:%S'), reverse=False)
                return arr
           
        except Exception as e:
            return {'message' : str(e)}, 401
        finally:
            if connection:
                connection.close()
                print('connection closed')

@todo.route('/addTodo', methods=['POST'])
# @token_required
def add_todo():
    if request.method == 'POST':
        try:
            connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
            )
            print('connectAddTodo')
            data = request.get_json()
            title = data['title']
            status = data['status']
            time = data['time']
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO todos (title, status, time) values (%s, %s, %s) RETURNING *;',(title,status,time))
                connection.commit()

            return 'добавлено'
           
        except Exception as e:
            return {'message' : str(e)}, 401
        finally:
            if connection:
                connection.close()
                print('connection closed')

@todo.route('/deleteTodo', methods=['POST'])
def delete_todo():
    if request.method == 'POST':
        try:
            connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
            )
            data = request.get_json() 
            id = data['id']
            with connection.cursor() as cursor:
                cursor.execute('DELETE FROM todos where id = %s',[id])
                connection.commit()          
            return 'удалено'
           
        except Exception as e:
            return {'message' : str(e)}, 401
        finally:
            if connection:
                connection.close()
                print('connection closed')

@todo.route('/changeStatus', methods=['POST'])
def shange_status():
    if request.method == 'POST':
        try:
            connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
            )
            data = request.get_json() 
            id = data['id']
            with connection.cursor() as cursor:
                cursor.execute('UPDATE  todos SET status = NOT status where id = %s',[id])
                connection.commit()          
            return 'статус изменен'
           
        except Exception as e:
            return {'message' : str(e)}, 401
        finally:
            if connection:
                connection.close()
                print('connection closed')

