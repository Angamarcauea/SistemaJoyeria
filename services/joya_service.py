# services/joya_service.py
from models.joya import Joya, db

class JoyaService:
    @staticmethod
    def listar_todo():
        # Esta función es la que llama tu ruta /inventario
        return Joya.query.all()

    @staticmethod
    def crear_joya(n, m, c, p):
        # Esta función es la que usa tu formulario para guardar en MySQL
        nueva = Joya(nombre=n, material=m, cantidad=c, precio=p)
        db.session.add(nueva)
        db.session.commit()
        return nueva

    @staticmethod
    def eliminar_joya(id_joya):
        # Esta es necesaria para el CRUD completo
        joya = Joya.query.get(id_joya)
        if joya:
            db.session.delete(joya)
            db.session.commit()
            return True
        return False