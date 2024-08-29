if(:x > 250)[
    if(:y >100)[
        :z = :z - :c1
        :y = :y - 100
        :x = :x - 50
    ]
    else[
        :z = :z + :c2
        :y = :y + 100
        :x = :x - 50
    ]
]
else[
    if(:y >100)[
        :z = :z - :c3
        :y = :y - 100
        :x = :x + 50
    ]
    else[
        :z = :z + :c4
        :y = :y + 100
        :x = :x + 50
    ]
]