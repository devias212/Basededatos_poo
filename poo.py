import mysql.connector

class Libro:

    def __init__(self, titulo, autor, isbn):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.disponible = True

    def prestar(self):
        self.disponible = False

class Usuario:

    def __init__(self, nombre, apellido, cedula):
        self.nombre = nombre
        self.apellido = apellido
        self.cedula = cedula

class Biblioteca:

    def __init__(self):
        self.libros = []
        self.usuarios = []

    def agregar_libro(self, libro):
        self.libros.append(libro)

    def mostrar_libros_disponibles(self):
        for libro in self.libros:
            if libro.disponible:
                print(f'{libro.titulo} de {libro.autor}')

    def buscar_libros(self, filtro):
        # Conectarse a la base de datos
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password',
            database='biblioteca'
        )

        # Crear un cursor
        cursor = connection.cursor()

        # Construir la consulta SQL
        sql = 'SELECT * FROM libros WHERE ' + filtro

        # Ejecutar la consulta
        cursor.execute(sql)

        # Iterar sobre los resultados
        for row in cursor:
            # Crear el objeto Libro
            libro = Libro(row[1], row[2], row[3])

            # Agregar el libro a la lista
            self.libros.append(libro)

        # Cerrar la conexión a la base de datos
        connection.close()

    def prestar_libro(self, libro, usuario):
        # Conectarse a la base de datos
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password',
            database='biblioteca'
        )

        # Crear un cursor
        cursor = connection.cursor()

        # Actualizar el estado del libro
        cursor.execute(
            'UPDATE libros SET disponible = False WHERE titulo = %s AND autor = %s AND isbn = %s',
            (libro.titulo, libro.autor, libro.isbn)
        )

        # Actualizar la fecha de préstamo
        cursor.execute(
            'UPDATE prestamos SET fecha_prestamo = NOW() WHERE libro_id = %s AND usuario_id = %s',
            (libro.id, usuario.id)
        )

        # Cerrar la conexión a la base de datos
        connection.close()

    def mostrar_usuarios(self):
        for usuario in self.usuarios:
            print(f'{usuario.nombre} {usuario.apellido} - {usuario.cedula}')

    def agregar_usuario(self, usuario):
        self.usuarios.append(usuario)

    def agregar_usuario_manualmente(self):
        # Solicitar los datos del usuario
        nombre = input('Ingresa el nombre del usuario: ')
        apellido = input('Ingresa el apellido del usuario: ')
        cedula = input('Ingresa la cédula del usuario: ')

        # Crear el objeto Usuario
        usuario = Usuario(nombre, apellido, cedula)

        # Agregar el usuario a la lista
        self.usuarios.append(usuario)

def main():

    # Conectarse a la base de datos
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='password',
        database='biblioteca'
    )

    # Crear una tabla de usuarios
    cursor = connection.cursor()
    cursor.execute(
        'CREATE TABLE usuarios ('
        'id INT AUTO_INCREMENT PRIMARY KEY,'
        'nombre VARCHAR(255) NOT NULL,'
        'apellido VARCHAR(25) not NULL'
    )
