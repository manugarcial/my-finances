import math
import sys
from salary_data import taxes_per_country_and_region
import logging
logging.basicConfig(level=logging.DEBUG)

tax_brackets = taxes_per_country_and_region

def calculate_irpf_and_gross(net_salary, region):
    # Check if the region is excluded from combining with national taxes
    # if region in ["na", "pv"]:
    #     region_only = True
    #     regional_brackets = tax_brackets["es"][region]
    #     brackets = regional_brackets
    # else:
    #     region_only = False
        # national_brackets = tax_brackets["es"]["national"]
        # regional_brackets = tax_brackets["es"].get(region, [])
        # brackets = merge_brackets(national_brackets, regional_brackets)

    # Calculate national IRPF separately
    national_brackets = tax_brackets["es"]["national"]
    # logging.debug(f"national_brackets: {national_brackets}")
    national_monthly_brackets = [(limit / 12, rate) for limit, rate in national_brackets]
    # logging.debug(f"national_monthly_brackets: {national_monthly_brackets}")
    gross_salary_national = calculate_gross_salary(net_salary, national_monthly_brackets)
    logging.debug(f"Gross Salary (National): {gross_salary_national}")
    national_tax = calculate_tax(gross_salary_national, national_monthly_brackets)
    logging.debug(f"National Tax: {national_tax}")

    # If region-only, return regional calculations directly
    # if region_only:
    #     logging.debug(f"region_only")
    #     monthly_brackets = [(limit / 12, rate) for limit, rate in brackets]
    #     logging.debug(f"monthly_brackets: {monthly_brackets}")
    #     gross_salary = calculate_gross_salary(net_salary, monthly_brackets)
    #     logging.debug(f"gross_salary: {gross_salary}")
    #     irpf_percentage = (gross_salary - net_salary) / gross_salary * 100
    #     logging.debug(f"irpf_percentage: {irpf_percentage}")
    #     return {"gross_salary": round(gross_salary, 2), "irpf": round(irpf_percentage, 2)}

    # # Calculate regional tax
    # regional_brackets = tax_brackets["es"][region]
    # logging.debug(f"regional_brackets: {regional_brackets}")
    # regional_monthly_brackets = [(limit / 12, rate) for limit, rate in regional_brackets]
    # logging.debug(f"regional_monthly_brackets: {regional_monthly_brackets}")
    # gross_salary_regional = calculate_gross_salary(net_salary, regional_monthly_brackets)
    # logging.debug(f"Gross Salary (National): {gross_salary_regional}")
    # regional_tax = calculate_tax(gross_salary_regional, regional_monthly_brackets)
    # logging.debug(f"regional_tax: {regional_tax}")

    # Total tax and gross salary
    # total_tax = national_tax + regional_tax
    total_tax = national_tax
    logging.debug(f"total_tax: {total_tax}")
    gross_salary_total = net_salary + total_tax
    logging.debug(f"gross_salary_total: {gross_salary_total}")

    # Calculate IRPF percentage
    irpf_percentage = total_tax / gross_salary_total * 100
    logging.debug(f"irpf_percentage: {irpf_percentage}")

    return {"gross_salary": round(gross_salary_total, 2), "irpf": round(irpf_percentage, 2)}


def merge_brackets(national, regional):
    """
    Merge national and regional tax brackets.
    """
    merged = []
    i, j = 0, 0
    while i < len(national) and j < len(regional):
        if national[i][0] < regional[j][0]:
            merged.append(national[i])
            i += 1
        elif national[i][0] == regional[j][0]:
            merged.append((national[i][0], national[i][1] + regional[j][1]))
            i += 1
            j += 1
        else:
            merged.append(regional[j])
            j += 1
    merged.extend(national[i:])
    merged.extend(regional[j:])
    return merged

# TO DO: Fix this function call and calculation
def calculate_tax(gross_salary, brackets):
    """
    Calculate tax based on the brackets.
    """
    logging.debug(f"gross_salary in tax: {gross_salary}")
    tax = 0
    remaining_salary = gross_salary
    for limit, rate in brackets:
        logging.debug(f"rate: {rate}")
        if remaining_salary > limit:
            tax += limit * (rate / 100)
            logging.debug(f"if tax: {tax}")
            remaining_salary -= limit
            logging.debug(f"remaining_salary: {remaining_salary}")
        else:
            tax += remaining_salary * (rate / 100)
            logging.debug(f"else tax: {tax}")
            break
    return tax


def calculate_gross_salary(net_salary, brackets):
    """
    Calculate gross salary iteratively for given tax brackets.
    """
    # logging.debug(f"calculate_gross_salary")
    logging.debug(f"----------------------------------------------------------------------------------------")
    step = 0.01  # Precision for the calculation
    gross_salary = net_salary  # Start with net salary as minimum estimate
    logging.debug(f"net_salary: {net_salary}")
    while True:
        tax = calculate_tax(gross_salary, brackets)
        # logging.debug(f"tax: {tax}")
        calculated_net_salary = gross_salary - tax
        # logging.debug(f"calculated_net_salary: {calculated_net_salary}")
        if abs(calculated_net_salary - net_salary) < step:
            break
        gross_salary += step
    
    logging.debug(f"gross_salary: {gross_salary}")
    return gross_salary


# Example usage
net_salary = 2386  # Monthly net salary
region = "vc"  # Replace with region code (e.g., "an", "pv", etc.)
result = calculate_irpf_and_gross(net_salary, region)
print(f"Gross Salary: €{result['gross_salary']}")
print(f"IRPF: {result['irpf']}%")
