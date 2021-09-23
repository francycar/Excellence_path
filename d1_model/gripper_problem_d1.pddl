(define (problem problem1)
  (:domain gripper)
  (:objects r1 r2 - location
            g - gripper
            b1 b2 - object
                )
  (:init
    (room r1)
    (adj  r1 r2)
    (ball  b1)
    (gripper g)
    (room r2)
    (ball b2)
    (atrob r1)
    (free g)
    (at b1 r1) 
    (at b2 r1)
    (atrob r1)
    
  
  
   

 )
  (:goal (and(atrob r2)(at b1 r2)))
)
