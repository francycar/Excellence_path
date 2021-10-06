(define (problem problem1)
	(:domain gripper)
	(:objects r1 r2 - location g - gripper b1 b2 - object)
	(:init
		(adj r1 r2)
		(at b1 r1)
		(at b2 r1)
		(atrob r1)
		(ball b1)
		(ball b2)
		(free g)
		(gripper g)
		(q1 r1 g r2)
		(room r1)
		(room r2)
		(turndomain))
	(:goal (oneof 
		(d2 (and(q3 b1 g r1 r2)))
		(d1 (and(q3 r1 g r2)))
		))
)
