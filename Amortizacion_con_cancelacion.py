import math

# Datos iniciales
principal = 100000  # capital inicial de la hipoteca
annual_interest_rate = 0.035  # tasa de interés anual
years = 25  # duración original de la hipoteca en años
additional_payment = 6000  # pago adicional anual a partir del tercer año
start_extra_payment_year = 3  # año en el que se empiezan los pagos adicionales
impuesto_compraventa = 0.08
valor_compraventa = 190000
comision_agencia = 0.02
notaria = 0.005
gravamen_ibi = 0.0025
basuras = 50 
porcentaje_financiacion_banco = 0.65

# Cálculo de la cuota mensual sin pagos adicionales
monthly_interest_rate = annual_interest_rate / 12
months = years * 12

# Fórmula para la cuota mensual: M = P * (r(1+r)^n) / ((1+r)^n - 1)
monthly_payment = principal * (monthly_interest_rate * (1 + monthly_interest_rate)**months) / ((1 + monthly_interest_rate)**months - 1)

# Simulación del pago con las cancelaciones anuales de 6000 euros
remaining_principal = principal
month = 0
while remaining_principal > 0:
    # Aplicar el pago mensual
    interest_payment = remaining_principal * monthly_interest_rate
    principal_payment = monthly_payment - interest_payment
    remaining_principal -= principal_payment
    
    # Si es el momento de hacer el pago adicional (después del tercer año)
    if (month // 12) + 1 >= start_extra_payment_year and month % 12 == 0:
        remaining_principal -= additional_payment
    
    month += 1

# Convertir el número de meses en años y meses
years_taken = month // 12
months_taken = month % 12

print('Capital a amortizar: ' + str(principal) + '\n' + 'Interés hipotecario fijo: ' + str(annual_interest_rate) + '\n' + 'Capital total adeudado: ' + str(math.ceil(years * 12 * monthly_payment * 100)/100) + '\n' + 'Años de hipoteca: ' + str(years) + '\n' + 'Años de cancelación con comisión: ' + str(start_extra_payment_year) + '\n' + 'Cancelación anual aportada: ' + str(additional_payment) + '\n' + 'Impuesto sobre la compraventa de inmuebles: ' + str(valor_compraventa*impuesto_compraventa) + '\n' + 'Comisión de agencia + Notaría: ' + str(comision_agencia*valor_compraventa + notaria*valor_compraventa) + '\n' + 'Capital inicial a aportar (Entrada, impuestos y comisiones): ' + str(valor_compraventa*(1-porcentaje_financiacion_banco) + comision_agencia*valor_compraventa + notaria*valor_compraventa) + '\n' + 'Impuestos anuales: ' + str(valor_compraventa*gravamen_ibi + basuras))
print('Años totales: ' + str(years_taken) + '\n' + 'Meses totales: ' + str(months_taken) + '\n' + 'Pago mensual: ' + str(monthly_payment) + '\n' + 'Montante principal restante: ' + str(remaining_principal))
print('Total a pagar con cancelaciones: ' + str(
    math.ceil(((years - years_taken - start_extra_payment_year)*additional_payment 
                                        + years_taken*monthly_payment*12 
                                        + months_taken*monthly_payment 
                                        + valor_compraventa*(1-porcentaje_financiacion_banco) 
                                        + valor_compraventa*impuesto_compraventa 
                                        + valor_compraventa*comision_agencia 
                                        + valor_compraventa*notaria)*100)/100
                                        ))
print('Total a pagar sin cancelaciones: ' + str(math.ceil((years * 12 * monthly_payment + valor_compraventa*(1-porcentaje_financiacion_banco) 
                                        + valor_compraventa*impuesto_compraventa 
                                        + valor_compraventa*comision_agencia 
                                        + valor_compraventa*notaria)*100)/100))
precio_reventa = math.ceil(((years - years_taken - start_extra_payment_year)*additional_payment 
                                        + years_taken*monthly_payment*12 
                                        + months_taken*monthly_payment 
                                        + valor_compraventa*(1-porcentaje_financiacion_banco) 
                                        + valor_compraventa*impuesto_compraventa 
                                        + valor_compraventa*comision_agencia 
                                        + valor_compraventa*notaria)*1.1*1.02*100)/100
print('Precio de venta del bien para sacar beneficio: ' + str(math.ceil(precio_reventa*100)/100))
print('Subida de precio en %: ' + str(math.ceil((precio_reventa/valor_compraventa)*1000)/10-100))