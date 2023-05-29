import json
import pymysql

# Connect to the RDS MySQL instance
def get_db_connection():
    return pymysql.connect(
        host='',
        user='',
        password='',
        database='mybooks',
        connect_timeout=5
    )

# Helper function to execute an SQL query
def execute_query(query, params=None):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
    connection.commit()
    connection.close()
    return result

# Create a book
def createBook(event, context):
    data = json.loads(event['body'])
    author = data['author']
    title = data['title']
    isbn = data['isbn']

    query = "INSERT INTO mybook (author, title, isbn) VALUES (%s, %s, %s)"
    params = (author, title, isbn)
    execute_query(query, params)

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Book created successfully'})
    }

# Get a book by ID
def getBook(event, context):
    book_id = event['pathParameters']['id']
    
    query = "SELECT * FROM mybook WHERE id = %s"
    params = (book_id,)
    result = execute_query(query, params)

    if result:
        book = {
            'id': result[0][0],
            'author': result[0][1],
            'title': result[0][2],
            'isbn': result[0][3]
        }
        return {
            'statusCode': 200,
            'body': json.dumps(book)
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Book not found'})
        }

def getBooks(event, context):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM mybook")
        books = cursor.fetchall()
        if books:
            return {
                'statusCode': 200,
                'body': json.dumps(books)
            }
        else:
            return {
                'statusCode': 404,
                'body': 'No books found'
            }

# Update a book by ID
def updateBook(event, context):
    book_id = event['pathParameters']['id']
    data = json.loads(event['body'])
    author = data['author']
    title = data['title']
    isbn = data['isbn']

    query = "UPDATE mybook SET author = %s, title = %s, isbn = %s WHERE id = %s"
    params = (author, title, isbn, book_id)
    execute_query(query, params)

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Book updated successfully'})
    }

# Delete a book by ID
def deleteBook(event, context):
    book_id = event['pathParameters']['id']
    
    query = "DELETE FROM mybook WHERE id = %s"
    params = (book_id,)
    execute_query(query, params)

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Book deleted successfully'})
    }
