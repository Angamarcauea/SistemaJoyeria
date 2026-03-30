from fpdf import FPDF
import os


class ReporteService:
    @staticmethod
    def generar_pdf(lista_joyas):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(190, 10, "JOYERIA LUXURY - REPORTE DE INVENTARIO", ln=True, align='C')
        pdf.ln(10)

        # Encabezados
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(50, 10, "Producto", 1)
        pdf.cell(40, 10, "Material", 1)
        pdf.cell(40, 10, "Cant.", 1)
        pdf.cell(50, 10, "Precio", 1, ln=True)

        # Datos
        pdf.set_font("Arial", size=12)
        for j in lista_joyas:
            pdf.cell(50, 10, str(j.nombre), 1)
            pdf.cell(40, 10, str(j.material), 1)
            pdf.cell(40, 10, str(j.cantidad), 1)
            pdf.cell(50, 10, f"${j.precio}", 1, ln=True)

        # Lo guardamos en la carpeta static para que sea fácil de descargar
        ruta = os.path.join('static', 'reporte_luxury.pdf')
        pdf.output(ruta)
        return ruta