/* eslint-disable */
import { createApp } from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router";
import store from "./store";
import { createI18n } from 'vue-i18n'

// Translations
const messages = {
    en: {
        net_salary_title: 'Net Salary calculation',
        mortgage: 'Mortgage calculation',
        anual_salary: "Anual gross salary",
        annual_irpf_cost: "Annual IRPF Cost",
        net_salary_per_month: "Net Salary per Month",
        irpf_percentage: "IRPF Percentage",
        loan_rent: "Loan Rent",
        basic_spendings: "Basic Spendings",
        personal_spendings: "Personal Spendings",
        savings: "Savings",
        investments: "Investments",
        tax_country: "Tax Country",
        spain: "spain",
        united_states: "United States of America",
        united_kingdom: "United Kingdom",
        autonomous_region: "Autonomous Region",
        anual_rent: "Anual Rent",
        health_expenses: "Health expenses (Gym, private health)",
        calculate: "Calculate",
        capital_lend: "Capital lend by the bank",
        anual_interest: "Anual interest rate",
        mortgage_years: "Total mortgage years",
        mortgage_months: "Total mortgage months",
        additional_yearly_pay: "Additional yearly payment",
        start_payment_year: "Start payment year",
        buy_selling_tax: "Buy / Selling Regional Tax",
        sell_price: "Property sell price",
        bank_loan: "Bank percentaje financiation",
        agency_commission: "Agency commission",
        total_loan_value: "Total loan value",
        minimal_savings: "Minimal savings needed",
        anual_taxes_expected: "Anual property taxes expected",
        total_expenses_no_cancel: "Total expense without anual mortgage cancelations",
        total_expenses_with_cancel: "Total expense with anual mortgage cancelations",
        minimun_resell_price: "Minimun resell price needed",
        resell_perc_rise: "Resell percentage rise needed",
        home: "Home",
        my_stocks: "My stocks list",
        stock_search: "Stock search",
        global_economy_data: "Global economy data"
    },
    es: {
        net_salary_title: 'Cálculo de salario neto',
        mortgage: 'Cálculo de hipoteca',
        anual_salary: "Salario bruto anual",
        annual_irpf_cost: "IRPF total anual",
        net_salary_per_month: "Salario neto mensual",
        irpf_percentage: "Porcentaje de IRPF",
        loan_rent: "Alquiler",
        basic_spendings: "Gastos básicos",
        personal_spendings: "Gastos personales",
        savings: "Ahorros",
        investments: "Inversión recomendada",
        tax_country: "País de tributación",
        spain: "España",
        united_states: "Estados Unidos de América",
        united_kingdom: "Reino Unido",
        autonomous_region: "Región Autónoma",
        anual_rent: "Alquiler anual",
        health_expenses: "Gastos en salud (gimnasios, medicina privada)",
        calculate: "Calcular",
        capital_lend: "Capital adeudado por el banco",
        anual_interest: "Tasa de interés anual (Euribor + tasas)",
        mortgage_years: "Años de hipoteca totales",
        mortgage_months: "Meses extra de hipoteca",
        additional_yearly_pay: "Pago anual adicional",
        start_payment_year: "Año de inicio del pago adicional",
        buy_selling_tax: "Impuesto regional de compra-venta",
        sell_price: "Precio de venta de la propiedad",
        bank_loan: "Porcentaje de financiación del banco",
        agency_commission: "Comisión de la agencia",
        total_loan_value: "Valor total del préstamo",
        minimal_savings: "Valor mínimo de ahorros necesario",
        anual_taxes_expected: "Impuestos anuales sobre la propiedad",
        total_expenses_no_cancel: "Gastos totales sin cancelaciones anuales de la hipoteca",
        total_expenses_with_cancel: "Gastos totales con cancelaciones anuales de la hipoteca",
        minimun_resell_price: "Precio mínimo de reventa",
        resell_perc_rise: "Porcentaje mínimo de reventa",
        home: "Principal",
        my_stocks: "Mi lista de stocks",
        stock_search: "Buscar stock",
        global_economy_data: "Datos macroeconómicos"
    }
}

// Create Vue I18n instance
const i18n = createI18n({
    locale: 'es',  // Default language
    fallbackLocale: 'en',
    messages,  // Set locale messages
});

createApp(App).use(store).use(router).use(i18n).mount("#app");
