(define (problem p1)
(:domain gripper)
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


)
(:goal (oneof

(d2 (and (atrob r2 ) (at b1 r2) (not(scratch))  ))
(d1 (and (atrob r2)  (scratch)))
)
)
)
