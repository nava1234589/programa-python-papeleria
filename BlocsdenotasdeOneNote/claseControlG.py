class ControlG:

    def __init__(self, x=0):

        self.registros = []

        self.total_ingresos = 0
        self.total_egresos = 0
        self.total_acumulado = 0


    def insertar(self, fecha, tipo, descripcion, cantidad):

        registro = [fecha, tipo, descripcion, cantidad]

        self.registros.append(registro)

        if tipo == "ingreso":
            self.total_ingresos += cantidad

        elif tipo == "egreso":
            self.total_egresos += cantidad


        self.total_acumulado = self.total_ingresos - self.total_egresos



    def eliminar(self, indice):

        registro = self.registros[indice]

        if registro[1] == "ingreso":
            self.total_ingresos -= registro[3]

        elif registro[1] == "egreso":
            self.total_egresos -= registro[3]


        self.registros.pop(indice)

        self.total_acumulado = self.total_ingresos - self.total_egresos



    def calcular_ganancia(self):

        return self.total_ingresos - self.total_egresos



    def determinar_resultado(self):

        if self.total_acumulado > 0:
            return "Ganancia"

        elif self.total_acumulado < 0:
            return "Pérdida"

        else:
            return "Sin movimientos"