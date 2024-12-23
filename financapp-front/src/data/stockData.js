const stockData = [
  { ticker: "AAPL", name: "Apple Inc." },
  { ticker: "GOOGL", name: "Alphabet Inc." },
  { ticker: "AMZN", name: "Amazon.com, Inc." },
  { ticker: "META", name: "Meta Platforms, Inc." },
  { ticker: "TSLA", name: "Tesla, Inc." },
  { ticker: "NFLX", name: "Netflix, Inc." },
  { ticker: "BRK.B", name: "Berkshire Hathaway Inc." },
  { ticker: "JNJ", name: "Johnson & Johnson" },
  { ticker: "V", name: "Visa Inc." },
  { ticker: "JPM", name: "JPMorgan Chase & Co." },
  { ticker: "UNH", name: "UnitedHealth Group Incorporated" },
  { ticker: "HD", name: "The Home Depot, Inc." },
  { ticker: "DIS", name: "The Walt Disney Company" },
  { ticker: "NVDA", name: "NVIDIA Corporation" },
  { ticker: "PYPL", name: "PayPal Holdings, Inc." },
  { ticker: "CMCSA", name: "Comcast Corporation" },
  { ticker: "PEP", name: "PepsiCo, Inc." },
  { ticker: "VZ", name: "Verizon Communications Inc." },
  { ticker: "INTC", name: "Intel Corporation" },
  { ticker: "MRK", name: "Merck & Co., Inc." },
  { ticker: "T", name: "AT&T Inc." },
  { ticker: "XOM", name: "Exxon Mobil Corporation" },
  { ticker: "NKE", name: "Nike, Inc." },
  { ticker: "PFE", name: "Pfizer Inc." },
  { ticker: "CSCO", name: "Cisco Systems, Inc." },
  { ticker: "CVX", name: "Chevron Corporation" },
  { ticker: "LLY", name: "Eli Lilly and Company" },
  { ticker: "MDT", name: "Medtronic plc" },
  { ticker: "CRM", name: "Salesforce, Inc." },
  { ticker: "HON", name: "Honeywell International Inc." },
  { ticker: "IBM", name: "International Business Machines Corporation" },
  { ticker: "TXN", name: "Texas Instruments Incorporated" },
  { ticker: "COST", name: "Costco Wholesale Corporation" },
  { ticker: "QCOM", name: "Qualcomm Incorporated" },
  { ticker: "NOW", name: "ServiceNow, Inc." },
  { ticker: "AMGN", name: "Amgen Inc." },
  { ticker: "MDLZ", name: "Mondelez International, Inc." },
  { ticker: "SBUX", name: "Starbucks Corporation" },
  { ticker: "ISRG", name: "Intuitive Surgical, Inc." },
  { ticker: "ATVI", name: "Activision Blizzard, Inc." },
  { ticker: "GILD", name: "Gilead Sciences, Inc." },
  { ticker: "FISV", name: "FISV, Inc." },
  { ticker: "SYY", name: "Sysco Corporation" },
  { ticker: "DE", name: "Deere & Company" },
  { ticker: "TROW", name: "T. Rowe Price Group, Inc." },
  { ticker: "LMT", name: "Lockheed Martin Corporation" },
  { ticker: "SYK", name: "Stryker Corporation" },
  { ticker: "SPGI", name: "S&P Global Inc." },
  { ticker: "NEM", name: "Newmont Corporation" },
  { ticker: "FIS", name: "Fidelity National Information Services, Inc." },
  { ticker: "DHR", name: "Danaher Corporation" },
  { ticker: "CME", name: "CME Group Inc." },
  { ticker: "ZTS", name: "Zoetis Inc." },
  { ticker: "ADI", name: "Analog Devices, Inc." },
  { ticker: "TAP", name: "Molson Coors Beverage Company" },
  { ticker: "FANG", name: "Diamondback Energy, Inc." },
  { ticker: "KMB", name: "Kimberly-Clark Corporation" },
  { ticker: "CL", name: "Colgate-Palmolive Company" },
  { ticker: "PCAR", name: "PACCAR Inc." },
  { ticker: "WBA", name: "Walgreens Boots Alliance, Inc." },
  { ticker: "BKNG", name: "Booking Holdings Inc." },
  { ticker: "NWL", name: "Newell Brands Inc." },
  { ticker: "EXC", name: "Exelon Corporation" },
  { ticker: "VRSN", name: "VeriSign, Inc." },
  { ticker: "ANTM", name: "Anthem, Inc." },
  { ticker: "PGR", name: "The Progressive Corporation" },
  { ticker: "WMT", name: "Walmart Inc." },
  { ticker: "MMC", name: "Marsh & McLennan Companies, Inc." },
  { ticker: "XRX", name: "Xerox Holdings Corporation" },
  { ticker: "TRV", name: "The Travelers Companies, Inc." },
  { ticker: "CAT", name: "Caterpillar Inc." },
  { ticker: "ETR", name: "Entergy Corporation" },
  { ticker: "SHW", name: "The Sherwin-Williams Company" },
  { ticker: "ADP", name: "Automatic Data Processing, Inc." },
  { ticker: "AON", name: "Aon plc" },
  { ticker: "NTRS", name: "Northern Trust Corporation" },
  { ticker: "RMD", name: "ResMed Inc." },
  { ticker: "ZBRA", name: "Zebra Technologies Corporation" },
  { ticker: "DLR", name: "Digital Realty Trust, Inc." },
  { ticker: "CHRW", name: "C.H. Robinson Worldwide, Inc." },
  { ticker: "AFL", name: "Aflac Incorporated" },
  { ticker: "BBY", name: "Best Buy Co., Inc." },
  { ticker: "DTE", name: "DTE Energy Company" },
  { ticker: "COO", name: "The Cooper Companies, Inc." },
  { ticker: "CARR", name: "Carrier Global Corporation" },
  { ticker: "MCO", name: "Moody's Corporation" },
  { ticker: "WDC", name: "Western Digital Corporation" },
  { ticker: "ADBE", name: "Adobe Inc." },
  { ticker: "ATVI", name: "Activision Blizzard, Inc." },
  { ticker: "COST", name: "Costco Wholesale Corporation" },
  { ticker: "CSCO", name: "Cisco Systems, Inc." },
  { ticker: "DIS", name: "The Walt Disney Company" },
  { ticker: "EBAY", name: "eBay Inc." },
  { ticker: "ILMN", name: "Illumina, Inc." },
  { ticker: "JD", name: "JD.com, Inc." },
  { ticker: "KDP", name: "Keurig Dr Pepper Inc." },
  { ticker: "KHC", name: "The Kraft Heinz Company" },
  { ticker: "LRCX", name: "Lam Research Corporation" },
  { ticker: "MAR", name: "Marriott International, Inc." },
  { ticker: "MDLZ", name: "Mondelez International, Inc." },
  { ticker: "MSFT", name: "Microsoft Corporation" },
  { ticker: "NFLX", name: "Netflix, Inc." },
  { ticker: "PYPL", name: "PayPal Holdings, Inc." },
  { ticker: "QCOM", name: "Qualcomm Incorporated" },
  { ticker: "REGN", name: "Regeneron Pharmaceuticals, Inc." },
  { ticker: "SBUX", name: "Starbucks Corporation" },
  { ticker: "VRSN", name: "VeriSign, Inc." },
  { ticker: "ZM", name: "Zoom Video Communications, Inc." },
  { ticker: "ORCL", name: "Oracle Corporation Inc." },
];

export default stockData;
