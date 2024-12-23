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
        "an": [
            (13000, 9.5),
            (21000, 12),
            (35200, 15),
            (50000, 18.5),
            (float('inf'), 22.5),
        ],
        "ar": [
            (13972, 9.5),
            (21209, 12),
            (36959, 15),
            (52499, 18.5),
            (59999, 20.5),
            (79999, 23),
            (89999, 24),
            (129999, 25),
            (float('inf'), 25.5),
        ],
        "as": [
            (12450, 10),
            (17707, 12),
            (33007, 14),
            (53407, 18.5),
            (70000, 21.5),
            (90000, 22.5),
            (175000, 25),
            (float('inf'), 25.5),
        ],
        "ib": [
            (10000, 9),
            (18000, 11.25),
            (30000, 14.25),
            (48000, 17.5),
            (70000, 19),
            (90000, 21.75),
            (120000, 22.75),
            (175000, 23.75),
            (float('inf'), 29.5),
        ],
        "cn": [
            (12450, 9),
            (17707, 11.5),
            (33008, 14),
            (53407, 18.5),
            (90000, 23.5),
            (120000, 25),
            (float('inf'), 26),
        ],
        "cb": [
            (13000, 8.5),
            (21000, 11),
            (35200, 14.5),
            (60000, 18),
            (90000, 22.5),
            (float('inf'), 24.5),
        ],
        "cl": [
            (12450, 9),
            (20200, 12),
            (35200, 14),
            (53407, 18.5),
            (float('inf'), 21.5),
        ],
        "cm": [
            (12450, 9),
            (20200, 12),
            (35200, 14),
            (53407, 18.5),
            (float('inf'), 22.5),
        ],
        "ct": [
            (12450, 10.5),
            (17707, 12),
            (21000, 14),
            (33007, 15),
            (53407, 18.8),
            (90000, 21.5),
            (120000, 23.5),
            (175000, 24.5),
            (float('inf'), 25.5),
        ],
        "md": [
            (13362, 8.5),
            (18004, 10.7),
            (35425, 12.8),
            (57320, 17.4),
            (float('inf'), 20.5),
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
        "ex": [
            (12450, 8),
            (20200, 10),
            (24200, 16),
            (35200, 17.5),
            (60000, 21),
            (80200, 23.5),
            (99200, 24),
            (120000, 24.5),
            (float('inf'), 25),
        ],
        "ga": [
            (12985, 9),
            (21068, 11.65),
            (35200, 14.9),
            (47600, 18.4),
            (float('inf'), 22.5),
        ],
        "ri": [
            (12450, 8),
            (20200, 10.6),
            (24200, 13.6),
            (35200, 17.8),
            (60000, 18.5),
            (80200, 19),
            (120000, 24.5),
            (float('inf'), 27),
        ],
        "mu": [
            (12450, 9.5),
            (20200, 11.2),
            (34000, 13.3),
            (60000, 17.9),
            (float('inf'), 22.5),
        ],
        "na": [
            (4458, 13),
            (10030, 22),
            (21175, 25),
            (35663, 28),
            (51266, 35.5),
            (66869, 41.5),
            (89159, 44),
            (139310, 47),
            (195034, 49),
            (334344, 50.5),
            (float('inf'), 54),
        ],
        "pv": [
            (17720, 23),
            (35440, 28),
            (53160, 35),
            (75910, 40),
            (105130, 45),
            (140130, 46),
            (204270, 47),
            (float('inf'), 49),
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
        "an": {
            "health": [0, 0],
            "rent": [0, 0],
        },
        "ar": {
            "health": [0, 0],
            "rent": [0, 0],
        },
        "as": {
            "health": [0, 0],
            "rent": [0, 0],
        },
        "ib": {
            "health": [0, 0],
            "rent": [0, 0],
        },
        "cn": {
            "health": [0, 0],
            "rent": [0, 0],
        },
        "cb": {
            "health": [0, 0],
            "rent": [0, 0],
        },
        "cl": {
            "health": [0, 0],
            "rent": [0, 0],
        },
        "cm": {
            "health": [0, 0],
            "rent": [0, 0],
        },
        "ct": {
            "health": [0, 0],
            "rent": [0, 0],
        },
        "md": {
            "health": [0, 0],
            "rent": [0, 0],
        },
        "vc": {
            "health": [0.3, 150],
            "rent": [0.15, 550],
        },
        "ex": {
            "health": [0, 0],
            "rent": [0, 0],
        },
        "ga": {
            "health": [0, 0],
            "rent": [0, 0],
        },
        "ri": {
            "health": [0, 0],
            "rent": [0, 0],
        },
        "mu": {
            "health": [0, 0],
            "rent": [0, 0],
        },
        "na": {
            "health": [0, 0],
            "rent": [0, 0],
        },
        "pv": {
            "health": [0, 0],
            "rent": [0, 0],
        },
    }
}

# impuestos_retirada_dividendos_spain = [0,0.19,0.21,0.23,0.27,0.28]
# tramos_retirada_dividendos_spain = [1000,6000,50000,200000,300000,'max']