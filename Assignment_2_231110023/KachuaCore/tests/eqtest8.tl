:z = 0
if(:x > 250)[
    :z = :z + 5
]
else[
    :z = :z + 5
    if(:x>20)[
        :x = (:x - :y) + 8
        :x = :y
    ]
    
]