if :y > :x
    [ :z = 60
      if :x < 50
        [   left :z
            forward(5)]
      else
        [   :z = 90
            if :x < 100
                [   right :z
                    forward(10)]
            else
                [   right :z
                    backward(15)]]]
else
    [   :z = 120
        if :x < 50
            [   left :z
                forward(12)]
        else
            [   :z  = 150
                if :x < 100
                    [   right :z
                        forward(8)]
                else
                    [   right :z
                        backward(4)]]]
