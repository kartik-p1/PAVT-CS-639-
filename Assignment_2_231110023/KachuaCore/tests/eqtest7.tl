:z = 0
if(:x > 250)[
    :z = :z + :c1
]
else[
    :z = :z + :c2
    if(:x > 20)[
        :x = (:x - :y) + :c1
        :x = :y
    ]
]