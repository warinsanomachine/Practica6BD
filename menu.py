import psycopg2
import os
import time

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "consultorio")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASS = os.getenv("DB_PASS", "password123")

def conectar_db():
    while True:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS
            )
            return conn
        except psycopg2.OperationalError:
            print("Esperando a la base de datos...")
            time.sleep(2)

CONSULTAS = {
    "1": {
        "desc": "1. Operador Basico (Seleccion): Citas del 'Consultorio 1'",
        "algebra": "σ_consultorio='Consultorio 1'(citas)",
        "crt": "{t | citas(t) ∧ t.consultorio='Consultorio 1'}",
        "crd": "{si, hc, fc, cc, esc, hfc, p, d, r | citas(si, hc, fc, cc, esc, hfc, p, d, r) ∧ cc='Consultorio 1'}",
        "sql": "SELECT * FROM citas WHERE consultorio = 'Consultorio 1';"
    },
    "2": {
        "desc": "2. Operador Basico (Proyeccion): Correos de todos los usuarios",
        "algebra": "π_email(usuarios)",
        "crt": "{t.email | usuarios(t)}",
        "crd": "{e | ∃n, a, c, v (usuarios(n, a, e, c, v))}",
        "sql": "SELECT email FROM usuarios;"
    },
    "3": {
        "desc": "3. Reunion (Equi-Join): Doctores con su consultorio asignado",
        "algebra": "doctores ⨝_doctores.consultorio=consultorios.nombre consultorios",
        "crt": "{d.*, c.* | doctores(d) ∧ consultorios(c) ∧ d.consultorio=c.nombre}",
        "crd": "{es, fp, hp, hi, hf, con, ed, nc | doctores(es, fp, hp, hi, hf, con, ed) ∧ consultorios(nc) ∧ con=nc}",
        "sql": "SELECT * FROM doctores JOIN consultorios ON doctores.consultorio = consultorios.nombre;"
    }, 
    "4": {
        "desc": "4. Operador Basico (Union): Correos de doctores y usuarios registrados",
        "algebra": "π_email(doctores) U π_email(usuarios)",
        "crt": "{t.email | doctores(t) ∨ usuarios(t)}",
        "crd": "{e | ∃es,fp,hp,hi,hf,con (doctores(es,fp,hp,hi,hf,con,e)) ∨ ∃n,a,c,v (usuarios(n,a,e,c,v))}",
        "sql": "SELECT email FROM doctores UNION SELECT email FROM usuarios;"
    },
    "5": {
        "desc": "5. Operador Basico (Interseccion): Usuarios que han enviado y recibido mensajes",
        "algebra": "π_remitente(mensajes) ∩ π_destinatario(mensajes)",
        "crt": "{m1.remitente | mensajes(m1) ∧ ∃m2(mensajes(m2) ∧ m2.destinatario = m1.remitente)}",
        "crd": "{e | ∃f,h,d,m (mensajes(f,h,e,d,m)) ∧ ∃f2,h2,r,m2 (mensajes(f2,h2,r,e,m2))}",
        "sql": "SELECT remitente FROM mensajes INTERSECT SELECT destinatario FROM mensajes;"
    },
    "6": {
        "desc": "6. Operador Basico (Diferencia): Usuarios que NO son doctores",
        "algebra": "π_email(usuarios) - π_email(doctores)",
        "crt": "{u.email | usuarios(u) ∧ ¬∃d(doctores(d) ∧ d.email = u.email)}",
        "crd": "{e | ∃n,a,c,v (usuarios(n,a,e,c,v)) ∧ ¬∃es,fp,hp,hi,hf,con (doctores(es,fp,hp,hi,hf,con,e))}",
        "sql": "SELECT email FROM usuarios EXCEPT SELECT email FROM doctores;"
    },
    "7": {
        "desc": "7. Reunion (Left Join): Todos los usuarios y su consultorio (solo si son doctores)",
        "algebra": "usuarios ⟕_usuarios.email=doctores.email doctores",
        "crt": "{u.nombre, u.email, d.consultorio | usuarios(u) ∧ (doctores(d) ∧ d.email=u.email ∨ ¬∃d2(doctores(d2) ∧ d2.email=u.email) ∧ d.consultorio='NULL')}",
        "crd": "{n, e, con | (∃a,c,v,es,fp,hp,hi,hf (usuarios(n,a,e,c,v) ∧ doctores(es,fp,hp,hi,hf,con,e))) ∨ (∃a,c,v (usuarios(n,a,e,c,v) ∧ ¬∃es,fp,hp,hi,hf,con2 (doctores(es,fp,hp,hi,hf,con2,e)) ∧ con='NULL'))}",
        "sql": "SELECT u.nombre, u.email, d.consultorio FROM usuarios u LEFT JOIN doctores d ON u.email = d.email;"
    },
    "8": {
        "desc": "8. Reunion (Anti-Join): Consultorios que aun NO tienen citas asignadas",
        "algebra": "consultorios ▷_consultorios.nombre=citas.consultorio citas",
        "crt": "{c.nombre | consultorios(c) ∧ ¬∃ci(citas(ci) ∧ ci.consultorio=c.nombre)}",
        "crd": "{nc | consultorios(nc) ∧ ¬∃si,hc,fc,esc,hfc,p,d,r (citas(si,hc,fc,nc,esc,hfc,p,d,r))}",
        "sql": "SELECT nombre FROM consultorios WHERE nombre NOT IN (SELECT consultorio FROM citas);"
    },
    "9": {
        "desc": "9. Reunion (Multiple): Paciente, diagnostico y medicamento recetado",
        "algebra": "π_paciente, situacion, medicamento(citas ⨝ situaciones ⨝ medicamentos)",
        "crt": "{c.paciente, s.nombre, m.nombre, m.ingrediente_activo | citas(c) ∧ situaciones(s) ∧ medicamentos(m) ∧ c.situacion=s.nombre ∧ c.receta=m.nombre}",
        "crd": "{p, ns, nm, ia | ∃hc,fc,cc,esc,hfc,d (citas(ns,hc,fc,cc,esc,hfc,p,d,nm)) ∧ ∃dur,ess (situaciones(ns,dur,ess)) ∧ ∃mg,pres (medicamentos(nm,ia,mg,pres))}",
        "sql": "SELECT c.paciente, s.nombre AS diagnostico, m.nombre AS medicamento, m.ingrediente_activo FROM citas c JOIN situaciones s ON c.situacion = s.nombre JOIN medicamentos m ON c.receta = m.nombre;"
    },
    "10": {
        "desc": "10. Reunion (Self Join): Pares de doctores asignados al mismo consultorio",
        "algebra": "ρ_D1(doctores) ⨝_D1.consultorio=D2.consultorio ∧ D1.email!=D2.email ρ_D2(doctores)",
        "crt": "{d1.email, d2.email, d1.consultorio | doctores(d1) ∧ doctores(d2) ∧ d1.consultorio=d2.consultorio ∧ d1.email!=d2.email}",
        "crd": "{e1, e2, con | ∃es1,fp1,hp1,hi1,hf1,es2,fp2,hp2,hi2,hf2 (doctores(es1,fp1,hp1,hi1,hf1,con,e1) ∧ doctores(es2,fp2,hp2,hi2,hf2,con,e2) ∧ e1!=e2)}",
        "sql": "SELECT d1.email AS doctor_1, d2.email AS doctor_2, d1.consultorio FROM doctores d1 JOIN doctores d2 ON d1.consultorio = d2.consultorio AND d1.email != d2.email;"
    },
    "11": {
        "desc": "11. Agrupacion (Simple): Cantidad de citas agendadas por cada consultorio",
        "algebra": "consultorio γ_COUNT(id_cita)(citas)",
        "crt": "{c1.consultorio, COUNT(c2) | citas(c1) ∧ c2 ∈ {x | citas(x) ∧ x.consultorio=c1.consultorio}}",
        "crd": "{cc, COUNT(id) | ∃si,hc,fc,esc,hfc,p,d,r (citas(id,si,hc,fc,cc,esc,hfc,p,d,r))}",
        "sql": "SELECT consultorio, COUNT(id_cita) AS total_citas FROM citas GROUP BY consultorio;"
    },
    "12": {
        "desc": "12. Agrupacion (con JOIN): Promedio de miligramos recetados por especialidad",
        "algebra": "especialidad γ_AVG(miligramos)(citas ⨝ medicamentos)",
        "crt": "{c1.especialidad, AVG(m.miligramos) | citas(c1) ∧ medicamentos(m) ∧ c1.receta=m.nombre}",
        "crd": "{esc, AVG(mg) | ∃id,si,hc,fc,cc,hfc,p,d,nm,ia,pres (citas(id,si,hc,fc,cc,esc,hfc,p,d,nm) ∧ medicamentos(nm,ia,mg,pres))}",
        "sql": "SELECT c.especialidad, ROUND(AVG(m.miligramos), 2) AS promedio_mg FROM citas c JOIN medicamentos m ON c.receta = m.nombre GROUP BY c.especialidad;"
    },
    "13": {
        "desc": "13. Agrupacion (con HAVING): Situaciones cuya duracion total supera 100 minutos",
        "algebra": "σ_total>100 (situacion γ_SUM(duracion)->total (citas ⨝ situaciones))",
        "crt": "{c1.situacion, SUM(s.duracion) | citas(c1) ∧ situaciones(s) ∧ c1.situacion=s.nombre ∧ SUM(s.duracion) > 100}",
        "crd": "{si, SUM(dur) | ∃id,hc,fc,cc,esc,hfc,p,d,r,ess (citas(id,si,hc,fc,cc,esc,hfc,p,d,r) ∧ situaciones(si,dur,ess)) ∧ SUM(dur) > 100}",
        "sql": "SELECT c.situacion, SUM(s.duracion) as tiempo_total_invertido FROM citas c JOIN situaciones s ON c.situacion = s.nombre GROUP BY c.situacion HAVING SUM(s.duracion) > 100;"
    },
    "14": {
        "desc": "14. Agregacion (Multiple): Resumen general de la duracion de todas las situaciones",
        "algebra": "F_MIN(duracion), MAX(duracion), AVG(duracion)(situaciones)",
        "crt": "MIN({s.duracion | situaciones(s)}), MAX({s.duracion | situaciones(s)}), AVG({s.duracion | situaciones(s)})",
        "crd": "MIN({dur | ∃ns,ess(situaciones(ns,dur,ess))}), MAX({dur | ∃ns,ess(situaciones(ns,dur,ess))}), AVG({dur | ∃ns,ess(situaciones(ns,dur,ess))})",
        "sql": "SELECT MIN(duracion) as min_mins, MAX(duracion) as max_mins, ROUND(AVG(duracion), 2) as prom_mins FROM situaciones;"
    },
    "15": {
        "desc": "15. Agrupacion Anidada: Conteo maximo de citas que tiene un solo doctor",
        "algebra": "F_MAX(total_citas)(doctor γ_COUNT(id_cita)->total_citas (citas))",
        "crt": "MAX({COUNT(c2) | citas(c1) ∧ c2 ∈ {x | citas(x) ∧ x.doctor=c1.doctor}})",
        "crd": "MAX({COUNT(id) | ∃si,hc,fc,cc,esc,hfc,p,d,r(citas(id,si,hc,fc,cc,esc,hfc,p,d,r))})",
        "sql": "SELECT MAX(conteo) AS max_citas_asignadas FROM (SELECT doctor, COUNT(*) as conteo FROM citas GROUP BY doctor) as subconsulta;"
    },
    "16": {
        "desc": "16. Division (1): Pacientes que han sido atendidos en TODOS los consultorios",
        "algebra": "π_paciente, consultorio(citas) ÷ π_nombre(consultorios)",
        "crt": "{c1.paciente | citas(c1) ∧ ∀con(consultorios(con) → ∃c2(citas(c2) ∧ c2.paciente=c1.paciente ∧ c2.consultorio=con.nombre))}",
        "crd": "{p | ∀nc (consultorios(nc) → ∃id,si,hc,fc,esc,hfc,d,r (citas(id,si,hc,fc,nc,esc,hfc,p,d,r)))}",
        "sql": "SELECT paciente FROM citas GROUP BY paciente HAVING COUNT(DISTINCT consultorio) = (SELECT COUNT(*) FROM consultorios);"
    },
    "17": {
        "desc": "17. Division (2): Doctores que han diagnosticado TODAS las situaciones medicas del catalogo",
        "algebra": "π_doctor, situacion(citas) ÷ π_nombre(situaciones)",
        "crt": "{c1.doctor | citas(c1) ∧ ∀s(situaciones(s) → ∃c2(citas(c2) ∧ c2.doctor=c1.doctor ∧ c2.situacion=s.nombre))}",
        "crd": "{d | ∀ns (situaciones(ns,dur,ess) → ∃id,hc,fc,cc,esc,hfc,p,r (citas(id,ns,hc,fc,cc,esc,hfc,p,d,r)))}",
        "sql": "SELECT doctor FROM citas GROUP BY doctor HAVING COUNT(DISTINCT situacion) = (SELECT COUNT(*) FROM situaciones);"
    },
    "18": {
        "desc": "18. Division (3): Pacientes a los que se les han recetado TODOS los medicamentos del catalogo",
        "algebra": "π_paciente, receta(citas) ÷ π_nombre(medicamentos)",
        "crt": "{c1.paciente | citas(c1) ∧ ∀m(medicamentos(m) → ∃c2(citas(c2) ∧ c2.paciente=c1.paciente ∧ c2.receta=m.nombre))}",
        "crd": "{p | ∀nm (medicamentos(nm,ia,mg,pres) → ∃id,si,hc,fc,cc,esc,hfc,d (citas(id,si,hc,fc,cc,esc,hfc,p,d,nm)))}",
        "sql": "SELECT paciente FROM citas WHERE receta IS NOT NULL GROUP BY paciente HAVING COUNT(DISTINCT receta) = (SELECT COUNT(*) FROM medicamentos);"
    },
    "19": {
        "desc": "19. Cuantificador Universal (CRT): Remitentes que SOLO le han enviado mensajes al paciente 'juan.perez@mail.com'",
        "algebra": "{u | ∀m (mensajes(m) ∧ m.remitente=u -> m.destinatario='juan.perez@mail.com')}",
        "crt": "{m1.remitente | mensajes(m1) ∧ ∀m2(mensajes(m2) ∧ m2.remitente=m1.remitente → m2.destinatario='juan.perez@mail.com')}",
        "crd": "{rem | ∃id1,f1,h1,des1,msj1(mensajes(id1,f1,h1,rem,des1,msj1)) ∧ ∀id2,f2,h2,des2,msj2(mensajes(id2,f2,h2,rem,des2,msj2) → des2='juan.perez@mail.com')}",
        "sql": "SELECT DISTINCT remitente FROM mensajes m1 WHERE NOT EXISTS (SELECT 1 FROM mensajes m2 WHERE m2.remitente = m1.remitente AND m2.destinatario != 'juan.perez@mail.com');"
    },
    "20": {
        "desc": "20. Cuantificador Universal (CRT): Doctores que SOLO han recetado medicamentos de 500mg",
        "algebra": "{d | ∀c,m (citas(c) ∧ medicamentos(m) ∧ c.doctor=d ∧ c.receta=m.nombre -> m.miligramos=500)}",
        "crt": "{c1.doctor | citas(c1) ∧ ∀c2,m(citas(c2) ∧ medicamentos(m) ∧ c2.doctor=c1.doctor ∧ c2.receta=m.nombre → m.miligramos=500)}",
        "crd": "{d | ∃id1,si1,hc1,fc1,cc1,esc1,hfc1,p1,r1(citas(id1,si1,hc1,fc1,cc1,esc1,hfc1,p1,d,r1)) ∧ ∀id2,si2,hc2,fc2,cc2,esc2,hfc2,p2,nm,ia,mg,pres(citas(id2,si2,hc2,fc2,cc2,esc2,hfc2,p2,d,nm) ∧ medicamentos(nm,ia,mg,pres) → mg=500)}",
        "sql": "SELECT DISTINCT c1.doctor FROM citas c1 JOIN medicamentos m1 ON c1.receta = m1.nombre WHERE NOT EXISTS (SELECT 1 FROM citas c2 JOIN medicamentos m2 ON c2.receta = m2.nombre WHERE c2.doctor = c1.doctor AND m2.miligramos != 500);"
    }
}

def ejecutar_consulta(conn, num_consulta):
    if num_consulta not in CONSULTAS:
        print("\nOpcion no valida.")
        return
    
    info = CONSULTAS[num_consulta]
    print(f"\n--- {info['desc']} ---")
    print(f"Algebra Relacional: {info.get('algebra', 'N/A')}")
    print(f"Calculo de Tuplas (CRT): {info.get('crt', 'N/A')}")
    print(f"Calculo de Dominios (CRD): {info.get('crd', 'N/A')}")
    print(f"SQL: {info.get('sql', 'N/A')}\n")
    print("Resultados:")
    print("-" * 50)
    
    try:
        cur = conn.cursor()
        cur.execute(info['sql'])
        
        if cur.description: 
            colnames = [desc[0] for desc in cur.description]
            print(" | ".join(colnames))
            print("-" * 50)
            rows = cur.fetchall()
            for row in rows:
                print(" | ".join(str(val) for val in row))
        else:
            print("Consulta ejecutada correctamente (sin filas devueltas).")
            
        cur.close()
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        conn.rollback()
    
    print("-" * 50)
    input("\nPresiona Enter para continuar...")

def menu_principal():
    print("Iniciando conexion...")
    conn = conectar_db()
    print("Conexion exitosa!")
    
    while True:
        print("\n" + "="*50)
        print(" SISTEMA DE CONSULTORIO MEDICO - CASO INTEGRADOR ")
        print("="*50)
        
        for key, value in CONSULTAS.items():
            print(value['desc'])
            
        print("0. Salir")
        print("="*50)
        
        opcion = input("Selecciona el numero de la consulta que deseas ejecutar: ")
        
        if opcion == "0":
            print("Saliendo del sistema...")
            break
        
        ejecutar_consulta(conn, opcion)
        
    conn.close()

if __name__ == "__main__":
    menu_principal()