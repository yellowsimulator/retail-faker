t5_models = {
    "small": {
        "name": "t5-small",
        "parameters": 60_000_000,
        "description": "Smallest T5 model with a good balance between performance and computational resources."
    },
    "base": {
        "name": "t5-base",
        "parameters": 220_000_000,
        "description": "Larger T5 model offering better performance but requiring more computational resources."
    },
    "large": {
        "name": "t5-large",
        "parameters": 770_000_000,
        "description": "Significantly larger T5 model with even better performance but increased resource demands."
    },
    "3B": {
        "name": "t5-3B",
        "parameters": 3_000_000_000,
        "description": "Extremely large T5 model with state-of-the-art performance but massive computational requirements."
    },
    "11B": {
        "name": "t5-11B",
        "parameters": 11_000_000_000,
        "description": "Largest T5 model with the best performance but nearly impossible to use without specialized hardware and infrastructure."
    }
}
