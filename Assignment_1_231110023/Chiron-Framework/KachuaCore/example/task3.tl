if :x >= 50 [
    if :y >= 60 [
        if :x <= 120 [
            right(45)
            forward(5)
        ] else [
            left(90)
        ]
    ] else [
        if :y <= 100 [
            left(45)
            backward(15)
        ] else [
            right(30)
            forward(10)
        ]
    ]
] else [
    if :x <= 50 [
        if :y <= 50 [
            if :y >= 30 [
                right(45)
                forward(5)
            ] else [
                left(45)
                backward(15)
            ]
        ] else [
            if :y <= 50 [
                right(45)
                forward(5)
            ] else [
                left(45)
                backward(15)
            ]
        ]
    ] else [
        forward(10)
        if :y <= 50 [
            backward(10)
        ] else [
            right(45)
            forward(10)
        ]
    ]
]
