ALTER SEQUENCE lecciones_leccion_id_seq RESTART;

INSERT INTO lecciones_leccion (nombre)
VALUES
 ('Introducción e Historia'),
 ('El Perceptrón Simple'),
 ('El Perceptrón Multicapa'),
 ('Redes Neuronales Recurrentes'),
 ('Redes de Creencia Profunda'),
 ('Redes Generativas Antagónicas')
 
ALTER SEQUENCE lecciones_tema_id_seq RESTART;

INSERT INTO lecciones_tema (nombre,leccion_id)
VALUES
 ('Introducción', (SELECT id from lecciones_leccion where nombre='Introducción e Historia')),
 ('Historia', (SELECT id from lecciones_leccion where nombre='Introducción e Historia')),
 ('Definición y Limitaciones', (SELECT id from lecciones_leccion where nombre='El Perceptrón Simple')),
 ('Entrenamiento', (SELECT id from lecciones_leccion where nombre='El Perceptrón Simple')),
 ('Definición y Limitaciones', (SELECT id from lecciones_leccion where nombre='El Perceptrón Multicapa')),
 ('Diseño y Propagación de las entradas', (SELECT id from lecciones_leccion where nombre='El Perceptrón Multicapa')),
 ('Entrenamiento y Early Stopping', (SELECT id from lecciones_leccion where nombre='El Perceptrón Multicapa')),
 ('Definición', (SELECT id from lecciones_leccion where nombre='Redes Neuronales Recurrentes')),
 ('Entrenamiento y LSTM', (SELECT id from lecciones_leccion where nombre='Redes Neuronales Recurrentes')),
 ('Máquina de Boltzmann Restringida', (SELECT id from lecciones_leccion where nombre='Redes de Creencia Profunda')),
 ('Divergencia Contrastiva', (SELECT id from lecciones_leccion where nombre='Redes de Creencia Profunda')),
 ('Definición y Entrenamiento', (SELECT id from lecciones_leccion where nombre='Redes de Creencia Profunda')),
 ('Definición', (SELECT id from lecciones_leccion where nombre='Redes Generativas Antagónicas')),
 ('Entrenamiento y Limitaciones', (SELECT id from lecciones_leccion where nombre='Redes Generativas Antagónicas'))
 
 
 
 



