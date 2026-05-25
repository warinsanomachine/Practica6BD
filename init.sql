
CREATE SCHEMA IF NOT EXISTS public;

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', 'public', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;


-- Tabla: consultorios
DROP TABLE IF EXISTS public.consultorios CASCADE;
CREATE TABLE public.consultorios (
    nombre VARCHAR(40) PRIMARY KEY
);

-- Tabla: especialidad
DROP TABLE IF EXISTS public.especialidad CASCADE;
CREATE TABLE public.especialidad (
    nombre VARCHAR(40) PRIMARY KEY
);

-- Tabla: situaciones
DROP TABLE IF EXISTS public.situaciones CASCADE;
CREATE TABLE public.situaciones (
    nombre VARCHAR(40) PRIMARY KEY,
    duracion INTEGER,
    especialidad VARCHAR(40) REFERENCES public.especialidad(nombre)
);

-- Tabla: medicamentos (La octava tabla)
DROP TABLE IF EXISTS public.medicamentos CASCADE;
CREATE TABLE public.medicamentos (
    nombre VARCHAR(50) PRIMARY KEY,
    ingrediente_activo VARCHAR(50),
    miligramos INTEGER,
    presentacion VARCHAR(40)
);

-- Tabla: usuarios
DROP TABLE IF EXISTS public.usuarios CASCADE;
CREATE TABLE public.usuarios (
    email VARCHAR(200) PRIMARY KEY,
    nombre VARCHAR(20),
    apellidos VARCHAR(20),
    contra VARCHAR(30),
    nivel INTEGER
);

-- Tabla: doctores
DROP TABLE IF EXISTS public.doctores CASCADE;
CREATE TABLE public.doctores (
    email VARCHAR(200) PRIMARY KEY REFERENCES public.usuarios(email),
    especialidad VARCHAR(40) REFERENCES public.especialidad(nombre),
    feproxc DATE,
    hoproxc INTEGER,
    hori INTEGER,
    horf INTEGER,
    consultorio VARCHAR(40) REFERENCES public.consultorios(nombre)
);

-- Tabla: citas
DROP TABLE IF EXISTS public.citas CASCADE;
CREATE TABLE public.citas (
    id_cita SERIAL PRIMARY KEY,
    situacion VARCHAR(40) REFERENCES public.situaciones(nombre),
    hora INTEGER,
    fecha DATE,
    consultorio VARCHAR(40) REFERENCES public.consultorios(nombre),
    especialidad VARCHAR(40) REFERENCES public.especialidad(nombre),
    horaf INTEGER,
    paciente VARCHAR(200) REFERENCES public.usuarios(email),
    doctor VARCHAR(200) REFERENCES public.doctores(email),
    receta VARCHAR(50) REFERENCES public.medicamentos(nombre)
);

-- Tabla: mensajes
DROP TABLE IF EXISTS public.mensajes CASCADE;
CREATE TABLE public.mensajes (
    id_mensaje SERIAL PRIMARY KEY,
    fecha DATE,
    hora INTEGER,
    remitente VARCHAR(200) REFERENCES public.usuarios(email),
    destinatario VARCHAR(200) REFERENCES public.usuarios(email),
    mensaje VARCHAR(1000)
);



INSERT INTO public.consultorios (nombre) VALUES 
('Consultorio 1'),
('Consultorio 23'),
('Consultorio 5'),
('Consultorio 7'),
('Consultorio 10');

INSERT INTO public.especialidad (nombre) VALUES 
('Pediatra'),
('Cardiologo'),
('Medico General'),
('Dermatologo'),
('Neurologo');

INSERT INTO public.situaciones (nombre, duracion, especialidad) VALUES 
('Gripa', 30, 'Pediatra'),
('Chequeo Anual', 45, 'Medico General'),
('Hipertension', 40, 'Cardiologo'),
('Alergia Cutanea', 20, 'Dermatologo'),
('Migraña', 50, 'Neurologo'),
('Vacunacion', 15, 'Pediatra'),
('Dolor de estomago', 25, 'Medico General'),
('Arritmia', 60, 'Cardiologo'),
('Acne', 30, 'Dermatologo'),
('Epilepsia', 60, 'Neurologo');

INSERT INTO public.medicamentos (nombre, ingrediente_activo, miligramos, presentacion) VALUES 
('Tempra', 'Paracetamol', 500, 'Tabletas'),
('Advil', 'Ibuprofeno', 400, 'Capsulas'),
('Amoxil', 'Amoxicilina', 500, 'Capsulas'),
('Clarityne', 'Loratadina', 10, 'Tabletas'),
('Micardis', 'Telmisartan', 40, 'Tabletas'),
('Aspirina', 'Acido Acetilsalicilico', 100, 'Tabletas'),
('Eucerin', 'Dexpantenol', 0, 'Pomada'),
('Keppra', 'Levetiracetam', 500, 'Tabletas'),
('Pepto Bismol', 'Bismuto', 262, 'Suspension'),
('Tylenol', 'Paracetamol', 650, 'Tabletas');

INSERT INTO public.usuarios (nombre, apellidos, email, contra, nivel) VALUES 
('admin', 'admin', 'admin@gmail.com', '456654', 3),
('Mrvh', 'Orshc', 'doctor@gmail.com', '456654', 2),
('Mrvh', 'Khuqdqghc', 'Jose@gmail.com', '45677654', 2),
('Ana', 'Lopez', 'ana.cardio@gmail.com', 'pass123', 2),
('Carlos', 'Ruiz', 'carlos.general@gmail.com', 'pass123', 2),
('Laura', 'Gomez', 'laura.derma@gmail.com', 'pass123', 2),
('Miguel', 'Torres', 'miguel.neuro@gmail.com', 'pass123', 2),
('Elena', 'Vargas', 'elena.pediatra@gmail.com', 'pass123', 2),
('Jorge', 'Diaz', 'jorge.cardio@gmail.com', 'pass123', 2),
('Sofia', 'Rios', 'sofia.general@gmail.com', 'pass123', 2),
('Dxjxvwr', 'Ioruhv', 'augustofv.2012@gmail.com', '45677654', 1),
('Usuario', 'Prueba', 'yo@gmail.com', 'pass1', 1),
('Juan', 'Perez', 'juan.perez@mail.com', 'pass1', 1),
('Maria', 'Sanchez', 'maria.s@mail.com', 'pass1', 1),
('Pedro', 'Martinez', 'pedro.m@mail.com', 'pass1', 1),
('Lucia', 'Fernandez', 'lucia.f@mail.com', 'pass1', 1),
('Raul', 'Gutierrez', 'raul.g@mail.com', 'pass1', 1),
('Carmen', 'Ortiz', 'carmen.o@mail.com', 'pass1', 1),
('Andres', 'Luna', 'andres.l@mail.com', 'pass1', 1),
('Patricia', 'Vega', 'patricia.v@mail.com', 'pass1', 1);

INSERT INTO public.doctores (especialidad, feproxc, hoproxc, hori, horf, consultorio, email) VALUES 
('Pediatra', NULL, NULL, 840, 1320, 'Consultorio 1', 'doctor@gmail.com'),
('Pediatra', NULL, NULL, 480, 960, 'Consultorio 23', 'Jose@gmail.com'),
('Cardiologo', NULL, NULL, 500, 1000, 'Consultorio 5', 'ana.cardio@gmail.com'),
('Medico General', NULL, NULL, 600, 1200, 'Consultorio 7', 'carlos.general@gmail.com'),
('Dermatologo', NULL, NULL, 700, 1300, 'Consultorio 10', 'laura.derma@gmail.com'),
('Neurologo', NULL, NULL, 800, 1400, 'Consultorio 1', 'miguel.neuro@gmail.com'),
('Pediatra', NULL, NULL, 600, 1200, 'Consultorio 5', 'elena.pediatra@gmail.com'),
('Cardiologo', NULL, NULL, 700, 1300, 'Consultorio 23', 'jorge.cardio@gmail.com'),
('Medico General', NULL, NULL, 800, 1400, 'Consultorio 10', 'sofia.general@gmail.com');

INSERT INTO public.citas (situacion, hora, fecha, consultorio, especialidad, horaf, paciente, doctor, receta) VALUES 
('Gripa', 1110, '2026-03-18', 'Consultorio 1', 'Pediatra', 1140, 'augustofv.2012@gmail.com', 'doctor@gmail.com', 'Tempra'),
('Gripa', 870, '2026-04-27', 'Consultorio 1', 'Pediatra', 900, 'yo@gmail.com', 'doctor@gmail.com', NULL),
('Hipertension', 600, '2026-05-10', 'Consultorio 5', 'Cardiologo', 640, 'juan.perez@mail.com', 'ana.cardio@gmail.com', 'Micardis'),
('Chequeo Anual', 700, '2026-05-11', 'Consultorio 7', 'Medico General', 745, 'maria.s@mail.com', 'carlos.general@gmail.com', NULL),
('Alergia Cutanea', 800, '2026-05-12', 'Consultorio 10', 'Dermatologo', 820, 'pedro.m@mail.com', 'laura.derma@gmail.com', 'Clarityne'),
('Migraña', 900, '2026-05-13', 'Consultorio 1', 'Neurologo', 950, 'lucia.f@mail.com', 'miguel.neuro@gmail.com', 'Advil'),
('Vacunacion', 1000, '2026-05-14', 'Consultorio 5', 'Pediatra', 1015, 'raul.g@mail.com', 'elena.pediatra@gmail.com', 'Tempra'),
('Dolor de estomago', 1100, '2026-05-15', 'Consultorio 10', 'Medico General', 1125, 'carmen.o@mail.com', 'sofia.general@gmail.com', 'Pepto Bismol'),
('Arritmia', 1200, '2026-05-16', 'Consultorio 23', 'Cardiologo', 1260, 'andres.l@mail.com', 'jorge.cardio@gmail.com', 'Aspirina'),
('Acne', 1300, '2026-05-17', 'Consultorio 10', 'Dermatologo', 1330, 'patricia.v@mail.com', 'laura.derma@gmail.com', 'Eucerin'),
('Gripa', 900, '2026-05-20', 'Consultorio 23', 'Pediatra', 930, 'maria.s@mail.com', 'Jose@gmail.com', 'Amoxil'),
('Chequeo Anual', 950, '2026-05-20', 'Consultorio 7', 'Medico General', 995, 'juan.perez@mail.com', 'carlos.general@gmail.com', NULL),
('Hipertension', 1000, '2026-05-21', 'Consultorio 23', 'Cardiologo', 1040, 'pedro.m@mail.com', 'jorge.cardio@gmail.com', 'Micardis'),
('Alergia Cutanea', 850, '2026-05-21', 'Consultorio 10', 'Dermatologo', 870, 'lucia.f@mail.com', 'laura.derma@gmail.com', 'Clarityne'),
('Epilepsia', 900, '2026-05-22', 'Consultorio 1', 'Neurologo', 960, 'raul.g@mail.com', 'miguel.neuro@gmail.com', 'Keppra'),
('Vacunacion', 1050, '2026-05-22', 'Consultorio 1', 'Pediatra', 1065, 'carmen.o@mail.com', 'doctor@gmail.com', NULL),
('Dolor de estomago', 1100, '2026-05-23', 'Consultorio 7', 'Medico General', 1125, 'andres.l@mail.com', 'carlos.general@gmail.com', 'Pepto Bismol'),
('Arritmia', 650, '2026-05-23', 'Consultorio 5', 'Cardiologo', 710, 'patricia.v@mail.com', 'ana.cardio@gmail.com', 'Aspirina'),
('Acne', 750, '2026-05-24', 'Consultorio 10', 'Dermatologo', 780, 'augustofv.2012@gmail.com', 'laura.derma@gmail.com', 'Eucerin'),
('Gripa', 1150, '2026-05-24', 'Consultorio 5', 'Pediatra', 1180, 'yo@gmail.com', 'elena.pediatra@gmail.com', 'Tylenol'),
('Chequeo Anual', 1200, '2026-05-25', 'Consultorio 10', 'Medico General', 1245, 'juan.perez@mail.com', 'sofia.general@gmail.com', NULL),
('Hipertension', 800, '2026-05-25', 'Consultorio 5', 'Cardiologo', 840, 'maria.s@mail.com', 'ana.cardio@gmail.com', 'Micardis'),
('Alergia Cutanea', 900, '2026-05-26', 'Consultorio 10', 'Dermatologo', 920, 'pedro.m@mail.com', 'laura.derma@gmail.com', 'Clarityne'),
('Migraña', 1000, '2026-05-26', 'Consultorio 1', 'Neurologo', 1050, 'lucia.f@mail.com', 'miguel.neuro@gmail.com', 'Advil'),
('Vacunacion', 1100, '2026-05-27', 'Consultorio 23', 'Pediatra', 1115, 'raul.g@mail.com', 'Jose@gmail.com', 'Tempra'),
('Dolor de estomago', 1200, '2026-05-27', 'Consultorio 7', 'Medico General', 1225, 'carmen.o@mail.com', 'carlos.general@gmail.com', 'Pepto Bismol'),
('Arritmia', 1300, '2026-05-28', 'Consultorio 23', 'Cardiologo', 1360, 'andres.l@mail.com', 'jorge.cardio@gmail.com', 'Aspirina'),
('Acne', 1400, '2026-05-28', 'Consultorio 10', 'Dermatologo', 1430, 'patricia.v@mail.com', 'laura.derma@gmail.com', 'Eucerin'),
('Gripa', 950, '2026-05-29', 'Consultorio 1', 'Pediatra', 980, 'augustofv.2012@gmail.com', 'doctor@gmail.com', 'Tempra'),
('Chequeo Anual', 1050, '2026-05-29', 'Consultorio 10', 'Medico General', 1095, 'yo@gmail.com', 'sofia.general@gmail.com', NULL),
('Hipertension', 1150, '2026-05-30', 'Consultorio 5', 'Cardiologo', 1190, 'juan.perez@mail.com', 'ana.cardio@gmail.com', 'Micardis');

INSERT INTO public.mensajes (fecha, hora, remitente, destinatario, mensaje) VALUES 
('2026-03-04', 754, 'augustofv.2012@gmail.com', 'doctor@gmail.com', 'HOLA'),
('2026-03-04', 754, 'doctor@gmail.com', 'augustofv.2012@gmail.com', 'hola'),
('2026-05-01', 800, 'juan.perez@mail.com', 'ana.cardio@gmail.com', 'Duda sobre medicamento'),
('2026-05-01', 815, 'ana.cardio@gmail.com', 'juan.perez@mail.com', 'Tomelo cada 12 horas'),
('2026-05-02', 900, 'maria.s@mail.com', 'carlos.general@gmail.com', 'Necesito reagendar'),
('2026-05-02', 930, 'carlos.general@gmail.com', 'maria.s@mail.com', 'Comuniquese a recepcion'),
('2026-05-03', 1000, 'pedro.m@mail.com', 'laura.derma@gmail.com', 'La crema irrita'),
('2026-05-03', 1010, 'laura.derma@gmail.com', 'pedro.m@mail.com', 'Suspenda el uso'),
('2026-05-04', 1100, 'lucia.f@mail.com', 'miguel.neuro@gmail.com', 'Mejoría notable'),
('2026-05-04', 1120, 'miguel.neuro@gmail.com', 'lucia.f@mail.com', 'Excelente noticia'),
('2026-05-05', 1200, 'raul.g@mail.com', 'elena.pediatra@gmail.com', 'Fiebre despues de vacuna'),
('2026-05-05', 1205, 'elena.pediatra@gmail.com', 'raul.g@mail.com', 'Dele Tempra 10ml'),
('2026-05-06', 1300, 'carmen.o@mail.com', 'sofia.general@gmail.com', 'Sigo con dolor'),
('2026-05-06', 1330, 'sofia.general@gmail.com', 'carmen.o@mail.com', 'Venga a urgencias'),
('2026-05-07', 1400, 'andres.l@mail.com', 'jorge.cardio@gmail.com', 'Resultados listos');