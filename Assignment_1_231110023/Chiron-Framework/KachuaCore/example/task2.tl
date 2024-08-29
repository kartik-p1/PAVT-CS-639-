if :x <=40 [
    if :y >=50 [
        if :x > 90 [
            left(90)
            forward(10)
        ] else [
            left(30)
            forward(5)
        ]
    ] else [
        if :y < 90 [
            right(30)
        ] else [
            right(45)
            forward(10)
        ]
    ]
] else [
    if :x >=100 [
        if :x > 50 [
            left(45)
            forward(15)
        ] else [
            right(70)
        ]
    ] else [
        if :y < 25 [
            right(30)
            backward(10)
        ] else [
            left(40)
            forward(5)
        ]
    ]
]
