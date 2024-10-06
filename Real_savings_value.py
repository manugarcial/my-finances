import math

# Input values
investment_per_year = 2000  # euros invested per year
years = 30                  # number of years
annual_return = 0.08         # 8% annual return
commission_rate = 0.0333     # 3.33% commission

# Beneficio financiero de activos tras ajuste por inflación y descuento de los impuestos fiscales

inflacion_media_interanual = 0.031
# savings_per_year = 1000  # euros saved each year
# years_of_investment = 10
# months_of_investment = 10
# months_per_year = 12
# rendimiento_medio_del_capital_invertido = 0.06
# salario_en_el_momento_de_retiro = 30000

# Valor del dinero tras el ajuste por la inflación

def savings_with_inflation(savings_per_year, years, inflation_rate):
    total_value_today = 0
    
    for year in range(1, years + 1):
        # Calculate the value of the savings in today's money
        value_today = savings_per_year / ((1 + inflation_rate) ** year)
        total_value_today += value_today
    
    return total_value_today

# Retornos de inversiones en bolsa acumulada

def investment_growth(investment_per_year, years, annual_return, commission_rate):
    total_invested = 0
    total_value = 0
    
    for year in range(0, years + 1):
        # Net investment after commission
        net_investment = investment_per_year * (1 - commission_rate)
        total_invested += net_investment
        
        # Calculate the growth of the investment made in each year
        value_after_growth = net_investment * (1 + annual_return) ** (years - year + 1)
        total_value += value_after_growth
    
    return total_value, total_invested

def irpf_deduction(importe, deduccion, max=None):
    deduction = importe * deduccion
    if max is not None:
        return min(deduction, max)
    return deduction

moneda = 'euros'

class IRPF:
    salario = 38000
    pais = 'spain'
    listado_paises = {'España':'spain', 'Example':'sample'}
    region = 'valenciana'
    listado_regiones_spain = {'Comunidad Valenciana':'valenciana', 'Test':'test'}
    edad = 1
    monthly_rent = 0
    rent = monthly_rent * 12
    salud_deportiva = 300
    ahorro_personal = 0
    deduccion_gimnasio_valenciana = 0.3
    deduccion_rent_valenciana = [0.15,0.2]
    impuestos_retirada_dividendos_spain = [0,0.19,0.21,0.23,0.27,0.28]
    tramos_retirada_dividendos_spain = [1000,6000,50000,200000,300000,'max']
    tramos_dividendos_spain = [
        (1000, 0),
        (600, 19),
        (50000, 21),
        (200000, 23),
        (300000, 27),
        (float('inf'), 28)
    ]
    tramos_irpf_spain = [
        (12000, 9.5),
        (20200, 12),
        (35200, 15),
        (60000, 18.5),
        (300000, 22.5),
        (float('inf'), 24.5)
    ]
    tramos_irpf_spain_valenciana = [
        (12000, 9),
        (22000, 12),
        (32000, 15),
        (42000, 17.5),
        (52000, 20),
        (62000, 22.5),
        (72000, 25),
        (100000, 26.5),
        (150000, 27.5),
        (200000, 28.5),
        (float('inf'), 29.5)
    ]

    def irpf_deductions(self):
        deductions = [0]
        deductions.append(irpf_deduction(self.salud_deportiva, self.deduccion_gimnasio_valenciana))
        deductions.append(irpf_deduction(self.rent, self.deduccion_rent_valenciana[1],550))
        
        return sum(deductions)
    
    def calcular_irpf(self, ingreso, tramos):
        irpf_value = 0
        ingreso_restante = ingreso

        for i, (limite, porcentaje) in enumerate(tramos):
            if ingreso_restante > 0:
                # Calcular la base imponible del tramo
                if i == 0:  # Primer tramo
                    base_imponible = min(ingreso_restante, limite)
                else:  # Tramos posteriores
                    base_imponible = min(ingreso_restante, limite - tramos[i-1][0])

                # Calcular el IRPF del tramo
                irpf_tramo = base_imponible * porcentaje / 100
                irpf_value += irpf_tramo
                
                # Restar la base imponible del ingreso restante
                ingreso_restante -= base_imponible

        return irpf_value
    
    def irpf_total(self):
        irpf_estatal = mi_irpf.calcular_irpf(self.salario, self.tramos_irpf_spain)
        irpf_comunitario = mi_irpf.calcular_irpf(self.salario, self.tramos_irpf_spain_valenciana)
        iprf_deductions = mi_irpf.irpf_deductions()
        irpf_total = irpf_estatal + irpf_comunitario - iprf_deductions
        salario_neto_mensual = math.ceil((self.salario - irpf_total + iprf_deductions)/12*100)/100

        print('Costo de mi IRPF anual: ' + str(irpf_total) + ' ' + moneda)
        print('Salario neto mensual: ' + str(salario_neto_mensual) + ' ' + moneda)
        print('Porcentaje de IRPF sobre el sueldo: ' + str(math.ceil((irpf_total/self.salario*1000))/10) + '%')
        print('Del sueldo mensual puedo destinar a hipoteca o alquiler el 30%: ' + str(math.ceil(salario_neto_mensual*0.3*100)/100) + ' ' + moneda)
        print('Del sueldo mensual puedo destinar a gastos basicos (comida, agua, luz, internet) el 20%: ' + str(math.ceil(salario_neto_mensual*0.2*100)/100) + ' ' + moneda)
        print('Del sueldo mensual puedo destinar a gastos personales (ropa, viajes y ocio) el 30%: ' + str(math.ceil(salario_neto_mensual*0.3*100)/100) + ' ' + moneda)
        print('Del sueldo mensual puedo destinar a ahorros el 10%: ' + str(math.ceil(salario_neto_mensual*0.1*100)/100) + ' ' + moneda)
        print('Del sueldo mensual puedo destinar a inversion el 10%: ' + str(math.ceil(salario_neto_mensual*0.1*100)/100) + ' ' + moneda)

        # Calculate and print the total value of the savings in today's money
        # total_value = savings_with_inflation(math.ceil(salario_neto_mensual*0.1*100)/100*12, years, inflacion_media_interanual)
        total_value = savings_with_inflation(1000*12, 20, inflacion_media_interanual)
        print(f"Total value of savings in today's money: {total_value:.2f} euros")

        # Calculate total value and total invested amount
        # total_value, total_invested = investment_growth(math.ceil(salario_neto_mensual*0.1*100)/100*12, years, annual_return, commission_rate)
        total_value, total_invested = investment_growth(1000*12, 20, annual_return, commission_rate)
        gross_benefits = total_value-total_invested
        net_benefits = gross_benefits - mi_irpf.calcular_irpf(gross_benefits,self.tramos_dividendos_spain)

        # Print results
        print(f"Total value after {years} years: {total_value:.2f} euros")
        print(f"Total amount invested: {total_invested:.2f} euros")
        print(f"Gross benefits: {gross_benefits:.2f} euros")
        print(f"Gross benefits in %: {math.ceil((total_value/total_invested)*1000)/10} %")
        print(f"Net benefits: {net_benefits:.2f} euros")
        print(f"Net benefits in %: {math.ceil((net_benefits/total_invested)*1000)/10} %")
        print(f"Real value of invested money")

        return 

mi_irpf = IRPF()
mi_irpf.irpf_total()
