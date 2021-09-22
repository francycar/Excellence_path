(define (domain gripper)
	(:requirements :typing)
	(:types 
		 location gripper objects
	)
	(:constants 
		b1 b2 - objects
 		g - gripper
 		r1 r2 - location
	)
	(:predicates
		(room ?r - location)
		(gripper ?g - gripper)
		(scratch)
		(ball ?b - objects)
		(atrob ?r - location)
		(carry ?o - objects ?g - gripper)
		(at ?o - objects ?r - location)
		(free ?g - gripper)
		(adj ?r1 - location ?r2 - location)
	)
	(:action move 
		:parameters (?from - location ?to - location)
		:precondition (and  (at ?from) (adj ?from ?to) (room ?from))
		:effect (oneof (d2 (and (not (atrob ?from)) (atrob ?to)))
		 (d1 (and (not (atrob ?from)) (atrob ?to) (scratch)))
		)
	)
	(:action pick 
		:parameters (?b - objects ?r - room ?g - gripper)
		:precondition (and  (atrob ?r) (ball ?b) (gripper ?g) (at ?b ?r) (free ?g))
		:effect (oneof (d2 (and (carry ?b ?g) (not (at ?b ?r)) (not (free ?g))))
		 (d1 (and (at ?b ?r) (free ?g) (not (carry ?b ?g))))
		)
	)
	(:action drop 
		:parameters (?b - objects ?r - room ?g - gripper)
		:precondition (and  (ball ?b) (room ?r) (gripper ?g) (atrob ?r) (carry ?b ?g))
		:effect (oneof (d2 (and (at ?b ?r) (free ?g) (not (carry ?b ?g))))
		 (d1 (and (at ?b ?r) (not (free ?g)) (carry ?b ?g)))
		)
	)
)
