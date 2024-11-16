import math
import sys
from salary_data import taxes_per_country_and_region, irpf_deductions_per_country_and_region

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
    ingreso_restante = ingreso

    for i, (limite, porcentaje) in enumerate(tramos):
        if ingreso_restante > 0:
            if i == 0:
                base_imponible = min(ingreso_restante, limite)
            else:
                base_imponible = min(ingreso_restante, limite - tramos[i-1][0])

            irpf_tramo = base_imponible * porcentaje / 100
            irpf_value += irpf_tramo
            ingreso_restante -= base_imponible

    return irpf_value

def calculate_irpf(salary, country_code, region_code, rent, health_discount):
    try:
        if(taxes_per_country_and_region[country_code].get(region_code, [])!="na" and taxes_per_country_and_region[country_code].get(region_code, [])!="pv"):
            irpf_national = calcular_irpf(salary, taxes_per_country_and_region[country_code]["national"])
        irpf_regional = calcular_irpf(salary, taxes_per_country_and_region[country_code].get(region_code, []))
        irpf_discounts = irpf_deductions(irpf_deductions_per_country_and_region[country_code][region_code]["health"][0], health_discount, irpf_deductions_per_country_and_region[country_code][region_code]["health"][1], rent, irpf_deductions_per_country_and_region[country_code][region_code]["rent"][0], irpf_deductions_per_country_and_region[country_code][region_code]["rent"][1])

        total_irpf = irpf_national + irpf_regional - irpf_discounts
        return total_irpf

    except KeyError as e:
        print(f"Error: Missing data for {e}. Please check your input.")
        return 0

if __name__ == "__main__":
    if len(sys.argv) != 7:
        print("Usage: calculate_irpf.py <salary> <currency> <country_code> <region_code> <annual_rent> <health_expenses>")
        sys.exit(1)

    try:
        salary = float(sys.argv[1])
        currency = sys.argv[2]
        country_code = sys.argv[3].lower()
        region_code = sys.argv[4].lower()
        annual_rent = float(sys.argv[5])
        health_expenses = float(sys.argv[6])

        # Check if currency is supported
        if currency not in ["eur", "usd", "gbp"]:
            print(f"Warning: Currency '{currency}' may not be supported. Proceeding with calculations.")

        irpf = calculate_irpf(salary, country_code, region_code, annual_rent, health_expenses)
        net_salary = salary - irpf
        monthly_net_salary = math.ceil(net_salary * 100 / 12) / 100

        financial_plan = {
            "annual_irpf": irpf,
            "monthly_net_salary": monthly_net_salary,
            "irpf_salary_percentage": round((irpf / salary) * 100, 2),
            "mortgage_or_rent_budget": round(monthly_net_salary * 0.3, 2),
            "basic_expenses_budget": round(monthly_net_salary * 0.2, 2),
            "personal_expenses_budget": round(monthly_net_salary * 0.3, 2),
            "savings_budget": round(monthly_net_salary * 0.1, 2),
            "investment_budget": round(monthly_net_salary * 0.1, 2),
        }

        print(financial_plan)

    except ValueError as e:
        print(f"Input Error: {e}. Ensure salary, rent, and health expenses are numbers.")