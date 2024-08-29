if :x >= 120 [
    if :y >= 100 [
        if :x <= 200 [
            right(45)
            forward(5)
        ] else [
            left(90)
        ]
    ] else [
        if :y <= 80 [
            left(45)
            backward(15)
        ] else [
            right(30)
            forward(10)
        ]
    ]
] else [
    if :x <= 120 [
        if :y <= 100 [
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
