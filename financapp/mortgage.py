import math
import sys

# Calculo de la hipoteca con cancelacion
def mortgage_cancelation(principal, start_extra_payment_year, additional_payment, monthly_interest_rate, monthly_payment):
    # Simulación del pago con las cancelaciones anuales de 6000 euros
    # print("hey")
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

    mortgage_results = {
        "years": years_taken,
        "months": months_taken
    }

    return mortgage_results

if __name__ == "__main__":
    if len(sys.argv) != 10:
        print("Usage: amortizacion_con_cancelacion.py")
        sys.exit(1)

    # Datos iniciales
    principal = int(sys.argv[1])  # capital inicial de la hipoteca
    annual_interest_rate = float(sys.argv[2])/100  # tasa de interés anual
    years = int(sys.argv[3])  # duración original de la hipoteca en años
    additional_payment = int(sys.argv[4])  # pago adicional anual a partir del tercer año
    start_extra_payment_year = int(sys.argv[5])  # año en el que se empiezan los pagos adicionales
    impuesto_compraventa = float(sys.argv[6])/100 # En alc, 8%
    valor_compraventa = int(sys.argv[7]) # ejemplo: 190.000
    porcentaje_financiacion_banco = float(sys.argv[8])/100 # ejemplo 0.65 -> 65%
    comision_agencia = float(sys.argv[9])/100 # ejemplo 0.02 -> 2%

    notaria = 0.005
    gravamen_ibi = 0.0025
    basuras = 50 

    monthly_interest_rate = annual_interest_rate / 12
    months = years * 12
    # Fórmula para la cuota mensual: M = P * (r(1+r)^n) / ((1+r)^n - 1)
    monthly_payment = principal * (monthly_interest_rate * (1 + monthly_interest_rate)**months) / ((1 + monthly_interest_rate)**months - 1)

    mortgage_time = mortgage_cancelation(principal, start_extra_payment_year, additional_payment, monthly_interest_rate, monthly_payment)
    resell_price = math.ceil(((mortgage_time["years"] - start_extra_payment_year)*additional_payment 
                                        + mortgage_time["years"]*monthly_payment*12 
                                        + mortgage_time["months"]*monthly_payment 
                                        + valor_compraventa-principal
                                        + valor_compraventa*impuesto_compraventa 
                                        + valor_compraventa*comision_agencia 
                                        + valor_compraventa*notaria)*1.1*1.02*100)/100

    my_mortgage_data = {
        "mortgage_years": mortgage_time["years"],
        "mortgage_months": mortgage_time["months"],
        "total_loan_value": math.ceil(years * 12 * monthly_payment * 100)/100,
        "sell_buy_tax": valor_compraventa * impuesto_compraventa,
        "minimal_money_needed": valor_compraventa * (1-porcentaje_financiacion_banco) + comision_agencia * valor_compraventa + notaria * valor_compraventa,
        "annual_taxes": valor_compraventa * gravamen_ibi + basuras,
        "total_mortgage_value_no_cancelations": math.ceil((years * 12 * monthly_payment + valor_compraventa-principal + valor_compraventa*impuesto_compraventa + valor_compraventa*comision_agencia + valor_compraventa*notaria)*100)/100,
        "total_mortgage_value_with_cancelations": math.ceil(((mortgage_time["years"] - start_extra_payment_year)*additional_payment + mortgage_time["years"]*monthly_payment*12 + mortgage_time["months"]*monthly_payment + valor_compraventa-principal + valor_compraventa*impuesto_compraventa + valor_compraventa*comision_agencia + valor_compraventa*notaria)*100)/100,
        "minimun_resell_price": resell_price,
        "resell_percentage_rise": round((math.ceil((resell_price / valor_compraventa) * 10000) / 100) - 100, 2),
    }

    print(my_mortgage_data)