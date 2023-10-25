-- Crear tabla de Usuarios
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    contraseña VARCHAR(255) NOT NULL,
    fecha_registro DATE NOT NULL
);

-- Crear tabla de Elementos de Lista de Deseos
CREATE TABLE elementos_lista_deseos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    fecha_creacion DATE NOT NULL
);

-- Crear tabla de Intersección para Relación Muchos a Muchos (usuarios y elementos de lista de deseos)
CREATE TABLE usuarios_elementos_lista_deseos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    elemento_id INT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (elemento_id) REFERENCES elementos_lista_deseos(id)
);
