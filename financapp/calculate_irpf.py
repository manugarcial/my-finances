import math
import sys

taxes_per_country_and_region = {
    "es": {
        "national": [
            (12000, 9.5),
            (20200, 12),
            (35200, 15),
            (60000, 18.5),
            (300000, 22.5),
            (float('inf'), 24.5),
        ],
        "vc": [
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
            (float('inf'), 29.5),
        ],
    },
    "us": {
        "national": [
            (9875, 10),
            (40125, 12),
            (85525, 22),
            (163300, 24),
            (207350, 32),
            (518400, 35),
            (float('inf'), 37),
        ],
        "default": []
    },
    "uk": {
        "national": [
            (12570, 0),
            (50270, 20),
            (150000, 40),
            (float('inf'), 45),
        ],
        "default": []
    }
}

irpf_deductions_per_country_and_region = {
    "es": {
        "national": [],
        "vc": {
            "health": [0.3, 150],
            "rent": [0.15, 550],
        },
    }
}

# impuestos_retirada_dividendos_spain = [0,0.19,0.21,0.23,0.27,0.28]
# tramos_retirada_dividendos_spain = [1000,6000,50000,200000,300000,'max']

def irpf_deduction(importe, deduccion, max=None):
    deduction = importe * deduccion
    if max is not None:
        return min(deduction, max)
    return deduction

def irpf_deductions(health, health_discount, max_health_discount, rent, rent_disccount, max_rent_discount):
    deductions = [0]
    deductions.append(irpf_deduction(float(health), float(health_discount), float(max_health_discount)))
    deductions.append(irpf_deduction(float(rent), float(rent_disccount), float(max_rent_discount)))

    return sum(deductions)

def calcular_irpf(ingreso, tramos):
    irpf_value = 0
    ingreso_restante = int(ingreso)

    for i, (limite, porcentaje) in enumerate(tramos):
        if ingreso_restante > 0:
            # Calcular la base imponible del tramo
            if i == 0:
                base_imponible = min(ingreso_restante, limite)
            else:
                base_imponible = min(ingreso_restante, limite - tramos[i-1][0])

            # Calcular el IRPF del tramo
            irpf_tramo = base_imponible * porcentaje / 100
            irpf_value += irpf_tramo
            
            # Restar la base imponible del ingreso restante
            ingreso_restante -= base_imponible

    return irpf_value

def calculate_irpf(salary, country_code, region_code, age, rent, health_discount):
    # Calculate the total tax (national + regional)
    irpf_estatal = calcular_irpf(salary, taxes_per_country_and_region[country_code]["national"])
    irpf_regional = calcular_irpf(salary, taxes_per_country_and_region[country_code][region_code])
    irpf_discounts = irpf_deductions(irpf_deductions_per_country_and_region[country_code][region_code]["health"][0], health_discount, irpf_deductions_per_country_and_region[country_code][region_code]["health"][1], rent, irpf_deductions_per_country_and_region[country_code][region_code]["rent"][0], irpf_deductions_per_country_and_region[country_code][region_code]["rent"][1])
    irpf_total = irpf_estatal + irpf_regional - irpf_discounts
    return irpf_total

if __name__ == "__main__":
    if len(sys.argv) != 8:
        print("Usage: calculate_irpf.py")
        sys.exit(1)

    salary = sys.argv[1]
    currency = sys.argv[2]
    country_code = sys.argv[3]
    region_code = sys.argv[4]
    age = sys.argv[5]
    anual_rent = sys.argv[6]
    health_discount = sys.argv[7]

    irpf = calculate_irpf(salary, country_code, region_code, age, anual_rent, health_discount)
    net_salary = float(salary) - float(irpf)
    salario_neto_mensual = math.ceil(net_salary*100/12)/100

    my_calculations = {
        "anual irpf": irpf,
        "net salary per month": salario_neto_mensual,
        "irpf salary percentage": math.ceil(irpf/net_salary*10000)/100,
        "mortgage loan / house rent": math.ceil(salario_neto_mensual*0.3*100)/100,
        "basic spendings": math.ceil(salario_neto_mensual*0.2*100)/100,
        "personal spendings": math.ceil(salario_neto_mensual*0.3*100)/100,
        "savings": math.ceil(salario_neto_mensual*0.1*100)/100,
        "investments": math.ceil(salario_neto_mensual*0.1*100)/100,
    }

    print(my_calculations)
